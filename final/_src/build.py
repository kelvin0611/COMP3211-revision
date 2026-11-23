import json, re, sys, pathlib
PAGES = [("index.html","總覽"),("P1-UML.html","P1 UML 圖"),("P2-Testing.html","P2 Testing"),
         ("P3-Process-Agile.html","P3 Process"),("P4-Requirements.html","P4 Requirements"),
         ("P5-Architecture.html","P5 Architecture"),("P6-Evolution-Reuse.html","P6 Evolution"),("P7-Design-OO.html","P7 Design")]
CSS = r"""
:root{color-scheme:light;--bg:#F2F4F7;--card:#FFFFFF;--ink:#15202B;--mut:#566273;--line:#D2D9E1;--acc:#BF4A14;--acc2:#0B7472;--soft:#D9EFEE;--ok:#17733A;--okbg:#DCF1E3;--bad:#B42318;--badbg:#FADFDB;--code:#E9EDF2;--warn:#8F6200;--warnbg:#F6EBCB}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.7 -apple-system,BlinkMacSystemFont,"PingFang HK","Noto Sans HK","Microsoft JhengHei",sans-serif}
nav.top{position:sticky;top:0;z-index:20;background:var(--bg);border-bottom:1px solid var(--line);display:flex;gap:4px;overflow-x:auto;padding:8px 12px;scrollbar-width:none}
nav.top::-webkit-scrollbar{display:none}
nav.top a{flex:none;text-decoration:none;color:var(--mut);font-size:14px;padding:5px 11px;border-radius:999px;border:1px solid var(--line);white-space:nowrap}
nav.top a.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
main{max-width:860px;margin:0 auto;padding:20px 16px 80px}
h1{font-size:26px;line-height:1.3;margin:12px 0 4px}h2{font-size:21px;margin:40px 0 10px;padding-top:8px;border-top:2px solid var(--ink)}
h3{font-size:17px;margin:26px 0 8px}h4{font-size:15px;margin:18px 0 6px;color:var(--acc2)}
.sub{color:var(--mut);margin:0 0 16px}
p,li{overflow-wrap:anywhere}
a{color:var(--acc2)}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.88em;background:var(--code);padding:1px 5px;border-radius:4px}
pre{background:var(--code);border:1px solid var(--line);border-radius:8px;padding:12px;overflow-x:auto;font-size:13.5px;line-height:1.55;margin:10px 0}
pre code{background:none;padding:0;font-size:inherit}
.tw{overflow-x:auto;margin:10px 0;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;font-size:14.5px}
th,td{border:1px solid var(--line);padding:6px 9px;text-align:left;vertical-align:top}
th{background:var(--soft);font-weight:600}
td.c,th.c{text-align:center}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:14px 0}
.toc{columns:2;column-gap:20px;font-size:14.5px;padding-left:18px}@media(max-width:560px){.toc{columns:1}}
.tag{display:inline-block;white-space:nowrap;font-size:12px;padding:1px 8px;border-radius:999px;border:1px solid var(--line);color:var(--mut);margin-right:4px;vertical-align:middle}
.t-must{background:var(--badbg);color:var(--bad);border-color:transparent}
.t-likely{background:var(--warnbg);color:var(--warn);border-color:transparent}
.t-know{background:var(--okbg);color:var(--ok);border-color:transparent}
.tip,.warn,.memo{border-radius:0;padding:10px 14px;margin:12px 0;border-left:4px solid}
.tip{background:var(--soft);border-color:var(--acc2)}.warn{background:var(--warnbg);border-color:var(--warn)}.memo{background:var(--okbg);border-color:var(--ok)}
.tip b:first-child,.warn b:first-child,.memo b:first-child{display:block;margin-bottom:2px}
details.ans{border:1px dashed var(--acc);border-radius:10px;margin:10px 0;background:var(--card)}
details.ans>summary{cursor:pointer;padding:8px 14px;color:var(--acc);font-weight:600;list-style:none}
details.ans>summary::-webkit-details-marker{display:none}
details.ans>summary::before{content:"▸ "}details.ans[open]>summary::before{content:"▾ "}
details.ans>div{padding:0 14px 12px}
.q{font-weight:600;margin-top:18px}
.faq dt{font-weight:600;margin-top:14px}.faq dd{margin:4px 0 0 0;padding-left:12px;border-left:2px solid var(--line)}
svg{max-width:100%;height:auto;display:block;margin:10px auto}
svg text{fill:var(--ink);font-family:inherit}
svg .ln{stroke:var(--ink);fill:none;stroke-width:1.4}
svg .bx{fill:var(--card);stroke:var(--ink);stroke-width:1.2}
svg .hl{fill:var(--soft);stroke:var(--acc2);stroke-width:1.4}
svg .ac{fill:var(--badbg);stroke:var(--acc);stroke-width:1.4}
.done{display:flex;align-items:center;gap:8px;font-size:14px;color:var(--mut);margin:6px 0 0}
.done input{width:18px;height:18px}
.mcq{margin:18px 0}
.mcq .bar{position:sticky;top:46px;z-index:5;background:var(--bg);display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid var(--line);font-size:14px}
.mcq .bar button{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:8px;padding:3px 10px;cursor:pointer}
.mq{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:12px 0}
.mq .stem{margin-bottom:8px}.mq .stem p{margin:4px 0}
.mq .num{font-size:12px;color:var(--mut)}
.opt{display:flex;gap:8px;width:100%;text-align:left;font:inherit;font-size:15px;background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px 10px;margin:6px 0;cursor:pointer}
.opt>span:first-child{font-weight:700;color:var(--mut);flex:none}.opt>span:last-child{overflow-wrap:anywhere}
.opt.right{background:var(--okbg);border-color:var(--ok)}.opt.wrong{background:var(--badbg);border-color:var(--bad)}
.opt:disabled{cursor:default;opacity:1}
.opt.sel{background:var(--soft);border-color:var(--acc2)}.opt.miss{border-style:dashed}
.mq .btn{margin-top:4px}
.exp{margin-top:8px;padding:8px 10px;border-radius:8px;background:var(--soft);font-size:14.5px;overflow-wrap:anywhere}
.exp .v{font-weight:700}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media(max-width:600px){.grid2{grid-template-columns:1fr}}
.prog{display:flex;flex-direction:column;gap:6px}.prog .row{display:flex;justify-content:space-between;gap:10px;font-size:14.5px;border-bottom:1px solid var(--line);padding:4px 0}
.mflow{display:flex;gap:10px;align-items:stretch;margin:10px 0}.mfcol{flex:1;min-width:0}.mfh{font-weight:700;font-size:14px;margin-bottom:6px}.fb{border:1px solid var(--line);background:var(--card);border-radius:8px;padding:6px 9px;margin-bottom:6px;font-size:13px;line-height:1.5;font-family:ui-monospace,Menlo,monospace;overflow-wrap:anywhere}.fb b{font-family:inherit}.hl2{background:var(--soft);border-color:var(--acc2)}.ac2{background:var(--badbg);border-color:var(--acc)}.mfarr{align-self:center;color:var(--mut);font-size:20px}.mfarr::before{content:"→"}@media(max-width:640px){.mflow{flex-direction:column}.mfarr{text-align:center}.mfarr::before{content:"↓"}}

:root{--surface:var(--card);--muted:var(--mut);--accent:var(--acc);--accent-soft:var(--badbg);--map:var(--acc2);--map-soft:var(--soft);--shuf:var(--warn);--shuf-soft:var(--warnbg);--red:#3D4BAA;--red-soft:#E2E6F8;--ok-soft:var(--okbg);--bad-soft:var(--badbg);--code-bg:var(--code);--code-ink:var(--ink);--code-dim:var(--mut);--f-mono:ui-monospace,Menlo,monospace}

.fmap{fill:var(--map-soft);stroke:var(--map);stroke-width:1.2}.fshuf{fill:var(--shuf-soft);stroke:var(--shuf);stroke-width:1.2}.fred{fill:var(--red-soft);stroke:var(--red);stroke-width:1.2}.facc{fill:var(--accent-soft);stroke:var(--accent);stroke-width:1.2}.tacc{fill:var(--accent);font-weight:600}
svg .arr{stroke:var(--ink);stroke-width:1.6;fill:none}.ah{fill:var(--ink)}.dash{stroke:var(--muted);stroke-width:1.4;stroke-dasharray:5 5;fill:none}
svg .small{font-size:11.5px;fill:var(--muted)}svg.dia{width:100%;height:auto}.mono{font-family:var(--f-mono);font-size:12.5px}
.diawrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;margin:10px 0}.w700{min-width:640px}
span.hl{background:var(--accent-soft);color:var(--accent);border-radius:3px;padding:0 2px;font-weight:600}
.dp table{width:auto}.num{font-variant-numeric:tabular-nums}td.brk code{white-space:normal}
.practice{border:1px solid var(--line);border-radius:14px;background:var(--card);padding:14px 16px;margin:16px 0}
.practice .src{font-family:var(--f-mono);font-size:12px;color:var(--mut);display:block}
.practice h4{margin-top:6px}
input.blank{font-family:var(--f-mono);font-size:13px;background:var(--card);color:var(--ink);border:1px solid var(--acc);border-radius:5px;padding:1px 4px;margin:0 1px;max-width:100%}
input.blank.ok{border-color:var(--ok);background:var(--okbg)}input.blank.bad{border-color:var(--bad);background:var(--badbg)}input.blank.shown{border-style:dashed}
.bn{display:inline-block;min-width:1.35em;text-align:center;font-size:10.5px;font-weight:600;color:var(--card);background:var(--acc);border-radius:999px;margin-right:2px}
.fillbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:6px}
.btn{font:inherit;font-size:13.5px;font-weight:600;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:8px;padding:6px 12px;cursor:pointer}.btn.pri{background:var(--acc);border-color:var(--acc);color:var(--card)}
.fillmsg{font-size:13.5px;color:var(--mut)}


.key{background:#FAE6DA;border-left:4px solid var(--acc);padding:12px 16px;margin:14px 0}
.key>b:first-child{display:block;color:var(--acc);margin-bottom:4px}
.key ul{margin:4px 0;padding-left:20px}
.fx{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:6px 12px;margin:12px 0;overflow-x:auto;text-align:center}@media(max-width:480px){.fx .katex-display>.katex{font-size:.86em}}
.concept{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:6px 16px 12px;margin:18px 0}
.concept>h3{margin-top:14px}
.lab{display:inline-block;font-size:12.5px;font-weight:700;color:#fff;background:var(--acc2);border-radius:6px;padding:1px 8px;margin:14px 0 4px}
.lab.why{background:#3D4BAA}.lab.pic{background:#8F6200}.lab.eg{background:var(--acc)}.lab.trap{background:var(--bad)}
figure.fig{margin:14px 0;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px}
figure.fig figcaption{font-size:13.5px;color:var(--mut);text-align:center;margin-top:6px}
.scroll{overflow-x:auto}
ol.steps{padding-left:0;list-style:none;counter-reset:s}
ol.steps>li{counter-increment:s;position:relative;padding:8px 10px 8px 42px;margin:8px 0;background:var(--card);border:1px solid var(--line);border-radius:10px}
ol.steps>li::before{content:counter(s);position:absolute;left:10px;top:8px;width:22px;height:22px;border-radius:50%;background:var(--acc2);color:#fff;font-size:13px;font-weight:700;text-align:center;line-height:22px}
.katex-display{margin:.4em 0;overflow-x:auto;overflow-y:hidden;padding:4px 0}
@media(max-width:600px){table.stack thead{display:none}table.stack tr:first-child:has(th){display:none}table.stack,table.stack tbody,table.stack tr,table.stack td{display:block;width:100%}
table.stack tr{border:1px solid var(--line);border-radius:10px;margin:0 0 10px;background:var(--card);padding:4px 0}
table.stack td{border:0;border-bottom:1px dashed var(--line);padding:6px 12px}table.stack td:last-child{border-bottom:0}
table.stack td::before{content:attr(data-label);display:block;font-size:12px;font-weight:700;color:var(--acc2)}}


/* COMP3211 additions */
.uml{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:8px;margin:12px 0;overflow-x:auto;-webkit-overflow-scrolling:touch}
.uml svg{margin:0 auto}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:13px;color:var(--mut);margin:6px 0}
.legend i{display:inline-block;width:14px;height:14px;border-radius:3px;vertical-align:-2px;margin-right:4px;border:1px solid var(--line)}
table.pt td,table.pt th{text-align:center;white-space:nowrap;font-family:ui-monospace,Menlo,monospace;font-size:13px}
table.pt td,table.pt th{padding:4px 3px;font-size:12.5px}table.pt input.blank{width:3ch!important;padding:1px 1px;text-align:center;font-size:12.5px}table.pt td.ex input.blank{width:7ch!important}
.wl{font-size:12.5px;color:var(--mut)}.scrollhint{text-align:center;margin-top:-6px}@media(min-width:760px){.scrollhint{display:none}}
.frow{border-bottom:1px dashed var(--line);padding:6px 0 10px}.frow p{margin:4px 0 6px}.fin{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:14px;color:var(--mut)}
.ansbox{background:var(--okbg);border-left:4px solid var(--ok);padding:10px 14px;margin:8px 0}
.ansbox>b:first-child{display:block;color:var(--ok);margin-bottom:2px}
footer{color:var(--mut);font-size:13px;text-align:center;margin-top:50px}
"""
JS = r"""
(function(){
var PAGE=document.body.dataset.page;
function ld(k,d){try{var v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}}
function sv(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
// section done checkboxes
document.querySelectorAll('h2[id]').forEach(function(h){
  var key='done:'+PAGE+':'+h.id;var l=document.createElement('label');l.className='done';
  var c=document.createElement('input');c.type='checkbox';c.checked=!!ld(key,false);
  c.onchange=function(){sv(key,c.checked)};l.appendChild(c);l.appendChild(document.createTextNode('呢部分溫完'));
  h.insertAdjacentElement('afterend',l);
});
// MCQ / TF / multi-select
function same(x,y){if(Array.isArray(y)){return Array.isArray(x)&&x.slice().sort().join()==y.slice().sort().join()}return x===y}
document.querySelectorAll('.mcq').forEach(function(box){
  var id=box.dataset.set, data=JSON.parse(box.querySelector('script').textContent);
  var key='mcq:'+PAGE+':'+id, st=ld(key,{});
  var bar=document.createElement('div');bar.className='bar';
  var sc=document.createElement('span');var rs=document.createElement('button');rs.textContent='重做呢套';
  bar.appendChild(sc);bar.appendChild(rs);box.appendChild(bar);
  function score(){var a=0,c=0;data.forEach(function(q,i){if(st[i]!==undefined){a++;if(same(st[i],q.a))c++}});
    sc.textContent='答咗 '+a+'/'+data.length+' · 啱 '+c;sv(key,st);sv('mcqsum:'+PAGE+':'+id,{a:a,c:c,n:data.length})}
  data.forEach(function(q,i){
    var tf=!q.o, opts=q.o||['True','False'], multi=Array.isArray(q.a), L=tf?'TF':'ABCDEFG';
    var kind=tf?'T/F':(multi?'多選：揀晒所有啱嘅':'MC');
    var d=document.createElement('div');d.className='mq';
    d.innerHTML='<div class="num">'+id+(i+1)+' · '+kind+(q.t?' · '+q.t:'')+'</div><div class="stem">'+q.s+'</div>';
    var btns=[], sel=[];
    opts.forEach(function(o,j){var b=document.createElement('button');b.className='opt';
      b.innerHTML='<span>'+L[j]+'</span><span>'+o+'</span>';
      b.onclick=function(){if(st[i]!==undefined)return;
        if(multi){var k=sel.indexOf(j);if(k<0)sel.push(j);else sel.splice(k,1);b.classList.toggle('sel')}
        else{st[i]=j;show();score()}};
      btns.push(b);d.appendChild(b)});
    var chk=null;if(multi){chk=document.createElement('button');chk.className='btn pri';chk.textContent='對答案';
      chk.onclick=function(){if(!sel.length)return;st[i]=sel.slice();show();score()};d.appendChild(chk)}
    var ex=document.createElement('div');ex.className='exp';ex.hidden=true;d.appendChild(ex);
    function lab(a){return Array.isArray(a)?a.map(function(x){return L[x]}).sort().join('、'):L[a]}
    function show(){if(st[i]===undefined){sel=[];btns.forEach(function(b){b.disabled=false;b.className='opt'});if(chk)chk.hidden=false;ex.hidden=true;return}
      var mine=st[i];if(chk)chk.hidden=true;
      btns.forEach(function(b,j){var inA=multi?q.a.indexOf(j)>=0:j===q.a, picked=multi?mine.indexOf(j)>=0:j===mine;
        b.disabled=true;b.className='opt'+(inA?' right':(picked?' wrong':''))+(multi&&inA&&!picked?' miss':'')});
      ex.hidden=false;ex.innerHTML=(same(mine,q.a)?'<span class="v" style="color:var(--ok)">答啱！</span> ':'<span class="v" style="color:var(--bad)">答錯，正確答案係 '+lab(q.a)+'。</span> ')+q.e}
    d._show=show;show();box.appendChild(d);
  });
  rs.onclick=function(){st={};box.querySelectorAll('.mq').forEach(function(d){d._show()});score()};
  score();
});

function norm(s){return s.replace(/[“”"]/g,"'").replace(/[‘’]/g,"'").replace(/\s+/g,'').toLowerCase()}
document.querySelectorAll('input.blank').forEach(function(inp){var alts=inp.dataset.ans.split('§');var w=Math.max.apply(null,alts.map(function(a){return a.length}));inp.style.width=(Math.max(w,3)+2)+'ch';inp.addEventListener('input',function(){inp.classList.remove('ok','bad','shown')})});
document.querySelectorAll('.fill').forEach(function(box){var inputs=box.querySelectorAll('input.blank');var msg=box.querySelector('.fillmsg');
 box.querySelector('[data-check]').addEventListener('click',function(){var r=0;inputs.forEach(function(inp){var v=norm(inp.value);var ok=inp.dataset.ans.split('§').some(function(a){return norm(a)===v});inp.classList.remove('ok','bad','shown');inp.classList.add(ok?'ok':'bad');if(ok)r++});msg.textContent='答啱 '+r+' / '+inputs.length+(r===inputs.length?'，全對！':'：紅色格再諗下，或者撳「顯示答案」。')});
 box.querySelector('[data-show]').addEventListener('click',function(){inputs.forEach(function(inp){inp.value=inp.dataset.ans.split('§')[0];inp.classList.remove('ok','bad');inp.classList.add('shown')});msg.textContent='已填入答案（虛線格）。'});
 box.querySelector('[data-clear]').addEventListener('click',function(){inputs.forEach(function(inp){inp.value='';inp.classList.remove('ok','bad','shown')});msg.textContent=''})});



document.querySelectorAll('.tw > table:not(.stack)').forEach(function(t){if(t.closest('.dp')||t.classList.contains('nostack'))return;
 var hr=t.querySelector('tr');if(!hr)return;var nh=hr.querySelectorAll('th').length;if(nh<3)return;
 var cells=t.querySelectorAll('td'),L=0;cells.forEach(function(c){L+=c.textContent.trim().length});
 if(cells.length&&L/cells.length>14)t.classList.add('stack')});
document.querySelectorAll('table.stack').forEach(function(t){var hs=[].map.call(t.querySelectorAll('tr:first-child th'),function(h){return h.textContent});
 t.querySelectorAll('tr').forEach(function(r,i){if(i===0)return;[].forEach.call(r.children,function(c,j){if(hs[j])c.setAttribute('data-label',hs[j])})})});

// progress panel on index
var pp=document.getElementById('progress');
if(pp){var pages=JSON.parse(pp.dataset.pages);var html='';
  pages.forEach(function(p){var n=0,m=0,a=0,c=0;
    for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);
      if(k.indexOf('done:'+p[0]+':')===0&&ld(k,false))n++;
      if(k.indexOf('mcqsum:'+p[0]+':')===0){var s=ld(k,{});a+=s.a||0;c+=s.c||0;m+=s.n||0}}
    html+='<div class="row"><a href="'+p[0]+'">'+p[1]+'</a><span>'+(m||n?'溫完 '+n+' 部分 · MCQ '+a+'/'+m+'（啱 '+c+'）':'未開始')+'</span></div>'});
  pp.innerHTML=html}
})();
"""


import uml, diagrams
def expand(body):
    body=re.sub(r'(?m)^\$\$(.+?)\$\$\s*$',lambda m:'<div class="fx">$$'+m.group(1)+'$$</div>',body)
    body=re.sub(r'\{\{UML:([\w-]+)\}\}',lambda m:uml.render(diagrams.D[m.group(1)]),body)
    return body

def build(fname):
    part = pathlib.Path("parts")/fname
    body = expand(part.read_text())
    title = re.search(r'<h1>(.*?)</h1>', body).group(1)
    title = re.sub('<.*?>','',title)
    nav = "".join(f'<a href="{f}"{" class=on" if f==fname else ""}>{n}</a>' for f,n in PAGES)
    body = body.replace("{{PAGES}}", json.dumps(PAGES, ensure_ascii=False).replace('"','&quot;'))
    html = f"""<!DOCTYPE html><html lang="zh-HK"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>{title}</title><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css"><style>{CSS}</style></head><body data-page="{fname}"><nav class="top">{nav}</nav><main>{body}<footer>COMP3211 Software Engineering Final 溫習包 · 考試 2026-12-05</footer></main><script>{JS}</script><script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script><script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js" onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'\\\\(',right:'\\\\)',display:false}}],ignoredClasses:['mcq','uml'],throwOnError:false}})"></script></body></html>"""
    pathlib.Path("out").mkdir(exist_ok=True)
    (pathlib.Path("out")/fname).write_text(html)
    print(fname, len(html))
for f in sys.argv[1:]: build(f)
