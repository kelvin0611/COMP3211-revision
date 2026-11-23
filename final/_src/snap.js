// node snap.js <file> <css selector> [width]  -> screenshots each match to /home/claude/fr/snap-<i>.png
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const [f,sel,w]=process.argv.slice(2);
const p=await b.newPage({viewport:{width:+(w||390),height:900},deviceScaleFactor:1});
await p.goto('file://'+process.cwd()+'/out/'+f);
await p.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true));
const els=await p.$$(sel);let i=0;for(const e of els){await e.screenshot({path:`/home/claude/fr/snap-${i}.png`});i++}
console.log('snapped',i);await b.close()})();
