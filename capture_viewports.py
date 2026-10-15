import os
import signal
import subprocess
import time
import tempfile
import uuid
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / ".impeccable" / "review"
OUT.mkdir(parents=True, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

captures = [
    ("desktop-hero.png", 1440, 1000, ""),
    ("desktop-harm.png", 1440, 1000, "?capture=harm"),
    ("desktop-association.png", 1440, 1000, "?capture=association"),
    ("desktop-closing.png", 1440, 1000, "?capture=closing"),
    ("mobile.png", 390, 844, ""),
    ("mobile-priorities.png", 390, 844, "?capture=priorities"),
]

for filename, width, height, query in captures:
    output = OUT / filename
    output.unlink(missing_ok=True)
    profile = f"{tempfile.gettempdir()}/chrome-shot-{uuid.uuid4().hex}"
    command = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--disable-background-networking",
        "--disable-component-update",
        "--disable-sync",
        "--metrics-recording-only",
        "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={profile}",
        f"--window-size={width},{height}",
        "--force-device-scale-factor=1",
        "--virtual-time-budget=2500",
        f"--screenshot={output}",
        f"http://127.0.0.1:4173/{query}",
    ]
    proc = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    deadline = time.time() + 18
    while time.time() < deadline and not output.exists():
        if proc.poll() is not None:
            break
        time.sleep(0.2)
    if proc.poll() is None:
        os.killpg(proc.pid, signal.SIGTERM)
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
    if not output.exists():
        raise RuntimeError(f"Screenshot was not created: {filename}")
    print(f"{filename}: {output.stat().st_size} bytes")
