import json, subprocess, tempfile, time, urllib.request, uuid
import websocket

PORT=9444
chrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
profile=f'{tempfile.gettempdir()}/day-sun-audit-{uuid.uuid4().hex}'
proc=subprocess.Popen([chrome,'--headless=new','--disable-gpu','--disable-background-networking','--remote-allow-origins=*',f'--remote-debugging-port={PORT}',f'--user-data-dir={profile}','about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
  tabs=None
  for _ in range(100):
    try:
      tabs=json.load(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json/list',timeout=1));
      if tabs: break
    except Exception: time.sleep(.1)
  ws=websocket.create_connection(tabs[0]['webSocketDebuggerUrl'],timeout=20)
  i=0
  def cmd(method,params=None):
    global i
    i+=1; current=i
    ws.send(json.dumps({'id':current,'method':method,'params':params or {}}))
    while True:
      m=json.loads(ws.recv())
      if m.get('id')==current:return m.get('result',{})
  def ev(expr):
    return cmd('Runtime.evaluate',{'expression':expr,'returnByValue':True,'awaitPromise':True})['result'].get('value')
  cmd('Page.enable');cmd('Runtime.enable')
  cmd('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'screenWidth':390,'screenHeight':844,'deviceScaleFactor':1,'mobile':False})
  cmd('Page.navigate',{'url':'http://127.0.0.1:4173/'});time.sleep(1)
  report=ev("""(() => ({
    innerWidth, scrollWidth: document.documentElement.scrollWidth,
    bodyWidth: document.body.getBoundingClientRect().width,
    overflowers: [...document.querySelectorAll('body *')].map(el=>{const r=el.getBoundingClientRect();return {tag:el.tagName,cls:el.className||'',text:(el.textContent||'').trim().slice(0,60),left:Math.round(r.left),right:Math.round(r.right),width:Math.round(r.width)}}).filter(x=>x.right>innerWidth+1||x.left<-1).slice(0,40)
  }))()""")
  print(json.dumps(report,indent=2))
finally:
  try: ws.close()
  except: pass
  proc.terminate()
