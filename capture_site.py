import base64
import json
import os
import subprocess
import time
import urllib.request
import tempfile
import uuid
from pathlib import Path

import websocket
from PIL import Image

ROOT = Path(__file__).parent
OUT = ROOT / ".impeccable" / "review"
OUT.mkdir(parents=True, exist_ok=True)
PORT = 9333
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE = f"{tempfile.gettempdir()}/a-day-in-sun-chrome-{uuid.uuid4().hex}"

proc = subprocess.Popen([
    CHROME,
    "--headless=new",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    "--remote-allow-origins=*",
    "--remote-debugging-address=127.0.0.1",
    f"--remote-debugging-port={PORT}",
    f"--user-data-dir={PROFILE}",
    "about:blank",
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    for _ in range(100):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list", timeout=1) as response:
                tabs = json.load(response)
            if tabs:
                break
        except Exception:
            time.sleep(0.2)
    else:
        raise RuntimeError("Chrome DevTools endpoint did not start")

    ws = websocket.create_connection(tabs[0]["webSocketDebuggerUrl"], timeout=60)
    next_id = 0
    events = []

    def command(method, params=None):
        nonlocal_id = None
        global next_id
        next_id += 1
        nonlocal_id = next_id
        ws.send(json.dumps({"id": nonlocal_id, "method": method, "params": params or {}}))
        while True:
            message = json.loads(ws.recv())
            if message.get("id") == nonlocal_id:
                if "error" in message:
                    raise RuntimeError(message["error"])
                return message.get("result", {})
            events.append(message)

    def evaluate(expression):
        result = command("Runtime.evaluate", {"expression": expression, "returnByValue": True, "awaitPromise": True})
        return result.get("result", {}).get("value")

    def set_viewport(width, height, mobile=False, scale=1):
        command("Emulation.setDeviceMetricsOverride", {
            "width": width,
            "height": height,
            "deviceScaleFactor": scale,
            "mobile": mobile,
        })

    def navigate(url):
        command("Page.navigate", {"url": url})
        time.sleep(1.2)

    def screenshot(path, viewport_width, viewport_height):
        total_height = int(evaluate("document.documentElement.scrollHeight"))
        slices = []
        y = 0
        while y < total_height:
            evaluate(f"window.scrollTo(0, {y})")
            time.sleep(0.18)
            data = command("Page.captureScreenshot", {"format": "png", "fromSurface": True})["data"]
            slice_path = OUT / f".{path.stem}-{y}.png"
            slice_path.write_bytes(base64.b64decode(data))
            image = Image.open(slice_path).convert("RGB")
            slices.append((y, image.copy(), slice_path))
            y += viewport_height

        canvas = Image.new("RGB", (viewport_width, total_height), "white")
        for y, image, slice_path in slices:
            remaining = total_height - y
            crop_height = min(viewport_height, remaining)
            canvas.paste(image.crop((0, 0, viewport_width, crop_height)), (0, y))
            slice_path.unlink(missing_ok=True)
        canvas.save(path)
        evaluate("window.scrollTo(0, 0)")
        return {"width": viewport_width, "height": total_height}

    command("Page.enable")
    command("Runtime.enable")

    set_viewport(1440, 1000)
    navigate("http://127.0.0.1:4173/")
    desktop_size = screenshot(OUT / "desktop.png", 1440, 1000)

    checks = evaluate("""(() => {
      document.querySelector('[data-use-mode="skin"]').click();
      document.querySelector('.priority-row[data-priority="spray"]').click();
      const useValues = [...document.querySelectorAll('[data-use-value]')].map(n => n.textContent.trim());
      const descriptions = [...document.querySelectorAll('[data-priority-description]')].map(n => n.textContent.trim());
      return {
        title: document.title,
        panels: document.querySelectorAll('.visual-panel').length,
        steps: document.querySelectorAll('.step').length,
        useValues,
        descriptions,
        horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth,
        fullHeight: document.documentElement.scrollHeight,
        detailsCount: document.querySelectorAll('details').length
      };
    })()""")

    set_viewport(390, 844, True, 1)
    navigate("http://127.0.0.1:4173/")
    mobile_size = screenshot(OUT / "mobile.png", 390, 844)
    mobile_checks = evaluate("""({
      horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth,
      mobileVisuals: [...document.querySelectorAll('.mobile-visual')].filter(n => getComputedStyle(n).display !== 'none').length,
      stickyDisplay: getComputedStyle(document.querySelector('.stage-column')).display,
      heroHeight: Math.round(document.querySelector('.hero').getBoundingClientRect().height),
      viewportHeight: innerHeight
    })""")

    exceptions = [event for event in events if event.get("method") == "Runtime.exceptionThrown"]
    print(json.dumps({
        "desktop": desktop_size,
        "mobile": mobile_size,
        "checks": checks,
        "mobileChecks": mobile_checks,
        "runtimeExceptions": len(exceptions),
        "screenshots": [str(OUT / "desktop.png"), str(OUT / "mobile.png")]
    }, indent=2))
finally:
    try:
        ws.close()
    except Exception:
        pass
    proc.terminate()
    try:
        proc.wait(timeout=4)
    except subprocess.TimeoutExpired:
        proc.kill()
