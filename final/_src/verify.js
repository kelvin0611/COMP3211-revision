const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const f of process.argv.slice(2)){const p=await b.newPage({viewport:{width:390,height:900}});
await p.goto('file://'+process.cwd()+'/out/'+f);
const r=await p.evaluate(async()=>{const out=[];
 document.querySelectorAll('.practice.fill').forEach((box,i)=>{const s=box.querySelector('[data-show]'),c=box.querySelector('[data-check]');if(s&&c){s.click();c.click();out.push((box.querySelector('.fillmsg')||{}).textContent)}});
 let bad=[];document.querySelectorAll('.mcq').forEach(m=>{const d=JSON.parse(m.querySelector('script').textContent);d.forEach((q,i)=>{const n=(q.o||[0,0]).length;const as=Array.isArray(q.a)?q.a:[q.a];if(as.some(x=>x<0||x>=n)||!q.e)bad.push(m.dataset.set+(i+1))})});
 const det=document.querySelectorAll('details').length;
 return {fills:out,bad,det,tf:[...document.querySelectorAll('.mq .num')].filter(x=>x.textContent.includes('T/F')).length,mc:[...document.querySelectorAll('.mq .num')].filter(x=>!x.textContent.includes('T/F')).length}});
console.log(f,JSON.stringify(r));await p.close()}
await b.close()})();
