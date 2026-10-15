import json
import subprocess
import time
import urllib.request
import tempfile
import uuid
import websocket

PORT = 9555
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE = f"{tempfile.gettempdir()}/day-sun-verify-{uuid.uuid4().hex}"
proc = subprocess.Popen([
    CHROME, "--headless=new", "--disable-gpu", "--disable-background-networking",
    "--remote-allow-origins=*", f"--remote-debugging-port={PORT}",
    f"--user-data-dir={PROFILE}", "about:blank"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

ws = None
try:
    tabs = None
    for _ in range(120):
        try:
            tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list", timeout=1))
            if tabs:
                break
        except Exception:
            time.sleep(0.1)
    if not tabs:
        raise RuntimeError("Chrome DevTools endpoint did not start")
    page_tabs = [tab for tab in tabs if tab.get("type") == "page" and tab.get("url") == "about:blank"]
    if not page_tabs:
        page_tabs = [tab for tab in tabs if tab.get("type") == "page" and not tab.get("url", "").startswith("chrome-extension://")]
    if not page_tabs:
        raise RuntimeError(f"No controllable page target: {tabs}")
    ws = websocket.create_connection(page_tabs[0]["webSocketDebuggerUrl"], timeout=20)
    counter = 0

    def command(method, params=None):
        nonlocal_counter = None
        global counter
        counter += 1
        current = counter
        ws.send(json.dumps({"id": current, "method": method, "params": params or {}}))
        while True:
            message = json.loads(ws.recv())
            if message.get("id") == current:
                if "error" in message:
                    raise RuntimeError(message["error"])
                return message.get("result", {})

    def evaluate(expression):
        result = command("Runtime.evaluate", {"expression": expression, "returnByValue": True, "awaitPromise": True})
        return result["result"].get("value")

    command("Page.enable")
    command("Runtime.enable")
    command("Page.navigate", {"url": "http://127.0.0.1:4173/"})
    for _ in range(80):
        if evaluate("document.readyState === 'complete' && document.title === 'A Day in the Sun'"):
            break
        time.sleep(0.1)
    else:
        load_state = evaluate("location.href + ' | ' + document.readyState + ' | ' + document.title")
        raise RuntimeError(f"Page did not load: {load_state}")
    time.sleep(0.25)

    report = evaluate("""(() => {
      const duplicateIds = [...document.querySelectorAll('[id]')]
        .map(el => el.id).filter((id, i, ids) => ids.indexOf(id) !== i);
      const tableRows = [...document.querySelectorAll('.data-access tbody tr')].length;
      const desktopHarm = document.querySelector('#sticky-stage [data-scene-panel="harm"]');
      const desktopUse = document.querySelector('#sticky-stage [data-scene-panel="use"]');
      const desktopPriority = document.querySelector('#sticky-stage [data-scene-panel="priorities"]');
      const activeCount = panel => panel ? panel.querySelectorAll('.mini-person.active').length : -1;
      const result = {
        title: document.title,
        duplicateIds,
        tableRows,
        harmPeople: desktopHarm?.querySelectorAll('.mini-person').length,
        harmActive: activeCount(desktopHarm),
        usePeople: desktopUse?.querySelectorAll('.mini-person').length,
        useActiveInitial: activeCount(desktopUse),
        useModeInitial: desktopUse?.dataset.mode,
        priorityInitial: desktopPriority?.dataset.priority,
        priorityButtons: desktopPriority?.querySelectorAll('.priority-row').length,
        methodsLink: document.querySelector('a[href="#methods"]') !== null,
        noHorizontalOverflow: document.documentElement.scrollWidth <= innerWidth,
        reducedMotionRulePresent: [...document.styleSheets].some(sheet => {
          try { return [...sheet.cssRules].some(rule => rule.media?.mediaText?.includes('prefers-reduced-motion')); }
          catch (_) { return false; }
        })
      };
      desktopUse?.querySelector('[data-use-mode="skin"]')?.click();
      result.useModeAfterClick = desktopUse?.dataset.mode;
      result.useActiveAfterClick = activeCount(desktopUse);
      result.useValueAfterClick = desktopUse?.querySelector('.use-stat strong')?.textContent.trim();
      desktopPriority?.querySelector('[data-priority="spray"]')?.click();
      result.priorityAfterClick = desktopPriority?.dataset.priority;
      result.priorityDescriptionAfterClick = desktopPriority?.querySelector('.product-figure p')?.textContent.trim();
      return result;
    })()""")

    expected = {
        "title": "A Day in the Sun",
        "duplicateIds": [],
        "tableRows": 10,
        "harmPeople": 100,
        "harmActive": 82,
        "usePeople": 100,
        "useActiveInitial": 31,
        "useModeInitial": "face",
        "priorityInitial": "ingredients",
        "priorityButtons": 4,
        "methodsLink": True,
        "noHorizontalOverflow": True,
        "reducedMotionRulePresent": True,
        "useModeAfterClick": "skin",
        "useActiveAfterClick": 28,
        "useValueAfterClick": "27.6%",
        "priorityAfterClick": "spray",
        "priorityDescriptionAfterClick": "37.6% rate spray application moderately or very important. This is a purchase consideration, not a spray-use rate."
    }
    failures = {key: {"expected": value, "actual": report.get(key)} for key, value in expected.items() if report.get(key) != value}
    print(json.dumps({"report": report, "failures": failures, "passed": not failures}, indent=2))
finally:
    if ws:
        ws.close()
    proc.terminate()
