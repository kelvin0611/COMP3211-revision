// usage: node shot.js <file.html> [full]   (run inside _src; checks out/<file>)
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const f=process.argv[2];
for(const w of [390,820]){const p=await b.newPage({viewport:{width:w,height:800}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.cwd()+'/out/'+f);
await p.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true));
const ov=await p.evaluate(()=>{const W=document.documentElement.clientWidth;return [...document.querySelectorAll('main *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>W+1&&!e.closest('.tw,pre,nav,.diawrap,.uml,.katex-display,.fx')}).map(e=>e.tagName+'.'+e.className+':'+(e.textContent||'').slice(0,30)).slice(0,10)});
const sw=await p.evaluate(()=>document.documentElement.scrollWidth);
console.log(w,'scrollWidth',sw,'overflow:',JSON.stringify(ov),'errs:',errs,'questions:',await p.$$eval('.mq',x=>x.length));
if(w==390&&process.argv[3]){await p.screenshot({path:`/home/claude/fr/${f}-full.png`,fullPage:true});}
}await b.close()})();
