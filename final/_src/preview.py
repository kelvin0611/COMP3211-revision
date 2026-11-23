import sys, uml, diagrams, importlib
from playwright.sync_api import sync_playwright
keys=sys.argv[1:]
html='<html><head><meta charset="utf-8"></head><body style="margin:0;background:#F2F4F7;font-family:sans-serif">'+''.join('<div style="margin:10px">'+uml.render(diagrams.D[k])+'</div>' for k in keys)+'</body></html>'
open('/home/claude/fr/prev.html','w').write(html)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':900,'height':800})
    pg.goto('file:///home/claude/fr/prev.html'); pg.screenshot(path='/home/claude/fr/prev.png',full_page=True); b.close()
