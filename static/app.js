const I={
 ideia:'<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.5 1 2.5h6c0-1 .3-1.8 1-2.5A6 6 0 0 0 12 3z"/>',
 roteiro:'<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z"/><path d="M14 3v5h5M8 13h8M8 17h5"/>',
 cenas:'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M10 9l5 3-5 3z"/>',
 montagem:'<path d="M6 3v18M18 3v18M3 8h6M15 8h6M3 16h6M15 16h6"/>',
 publicacao:'<path d="M12 15V3M7 8l5-5 5 5M5 15v4a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-4"/>',
 film:'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M7 5v14M17 5v14M3 9h4M17 9h4M3 15h4M17 15h4"/>',
 spark:'<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/>',
 key:'<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3"/>',x:'<path d="M6 6l12 12M18 6L6 18"/>',
 check:'<path d="M5 12l5 5 9-10"/>',alert:'<path d="M12 9v4M12 17h.01M10.3 3.9L2 18a2 2 0 0 0 1.7 3h16.6a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>',
 mic:'<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',music:'<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
 cc:'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M10 10a2 2 0 1 0 0 4M17 10a2 2 0 1 0 0 4"/>',img:'<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-5L5 20"/>',
 text:'<path d="M4 6h16M4 12h10M4 18h7"/>',hash:'<path d="M5 9h14M5 15h14M10 3L8 21M16 3l-2 18"/>',globe:'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
 arrow:'<path d="M5 12h14M13 6l6 6-6 6"/>'};
const svg=k=>`<svg viewBox="0 0 24 24">${I[k]}</svg>`;
const STEPS=[["ideia","Ideia"],["roteiro","Roteiro"],["cenas","Cenas"],["montagem","Montagem","soon"],["publicacao","Publicação","soon"]];
const $=id=>document.getElementById(id);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const words=t=>(t||"").trim().split(/\s+/).filter(Boolean).length;
let P={scenes:[]},TITLES=[],VIEW="projetos",HASKEY=true;

function toast(t,kind="ok"){const d=document.createElement("div");d.className="toast "+kind;d.innerHTML=svg(kind=="err"?"alert":"check")+`<div>${esc(t)}</div>`;$("toasts").append(d);setTimeout(()=>d.remove(),kind=="err"?7000:3500);}
function stepDone(k){return k=="ideia"?!!P.title:k=="roteiro"?P.scenes.length>0:false;}
function renderNav(){
 $("steps").innerHTML=STEPS.map(([k,n,s],i)=>`<button class="nav-item${VIEW==k?" active":""}" onclick="go('${k}')">${svg(k)}<span>${n}</span>${s?'<span class="tag">em breve</span>':`<i class="dot${stepDone(k)?" done":""}"></i>`}</button>`).join("");
 document.querySelector('[data-view=projetos]').classList.toggle("active",VIEW=="projetos");
 const idx=STEPS.findIndex(s=>s[0]==VIEW);const done=STEPS.filter(s=>stepDone(s[0])).length;
 $("progressText").textContent=idx<0?`${done} de 5 etapas concluídas`:`Etapa ${idx+1} de 5 · ${STEPS[idx][1]}`;
 $("progressBar").style.width=(done/5*100)+"%";
 $("crumbStep").textContent=idx<0?"Projetos":STEPS[idx][1];
 $("crumbProject").textContent=P.title||(P.id?"Projeto sem título":"Novo projeto");
}
function go(k){if(k=="cenas"&&VIEW!="cenas"){const u=P.scenes.filter(s=>!s.reviewed).length;if(u&&!confirm(`${u} de ${P.scenes.length} cenas ainda não foram revisadas (fatos e fontes). Ir para Cenas mesmo assim?`))return;}
VIEW=k;document.querySelectorAll(".view").forEach(v=>v.classList.toggle("on",v.id=="v-"+k));document.body.classList.remove("nav-open");
 if(k=="cenas")renderCenas();if(k=="projetos")loadProjects();renderNav();window.scrollTo(0,0);}
document.querySelector('[data-view=projetos]').onclick=()=>go("projetos");

async function api(path,body){const r=await fetch(path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
 let d;try{d=await r.json()}catch{d={error:"Resposta inválida do servidor"}}if(!r.ok)throw new Error(d.error||"Erro");return d;}
function busy(btn,on,label){btn.disabled=on;if(on){btn.dataset.h=btn.innerHTML;btn.innerHTML=`<span class="spin"></span>${label}`}else btn.innerHTML=btn.dataset.h;}
function form(){return{niche:$("niche").value.trim(),language:$("language").value,theme:$("theme").value.trim(),minutes:+$("minutes").value||10};}
function fill(){["niche","language","theme","minutes","title"].forEach(k=>{if(P[k]!=null)$(k).value=P[k]});}

function emptyTitles(){$("titles").innerHTML=`<div class="empty"><div class="ill">${svg("spark")}</div><b>Nenhuma sugestão ainda</b><p>Preencha nicho, língua e tema e clique em “Sugerir títulos”. As opções aparecem aqui para você escolher.</p></div>`;$("titlesCount").textContent="";}
function renderTitles(){if(!TITLES.length)return emptyTitles();$("titlesCount").textContent=`${TITLES.length} opções`;
 $("titles").innerHTML=TITLES.map((t,i)=>`<div class="title-opt${P.title==t.title?" sel":""}" onclick="pick(${i})"><div class="n">${i+1}</div><div><b>${esc(t.title)}</b><p>${esc(t.hook)}</p>${t.why?`<p class="why">${svg("check")}${esc(t.why)}</p>`:""}${t.formula?`<span class="chip sm">${esc(t.formula)}</span>`:""}</div><span class="go">${svg("arrow")}</span></div>`).join("");}
async function titles(){const f=form();if(!f.niche&&!f.theme)return toast("Preencha pelo menos o nicho ou o tema.","err");
 const b=$("btnTitles");busy(b,true,"Gerando títulos...");$("titles").innerHTML='<div class="skel t"></div>'.repeat(5);
 try{TITLES=(await api("/api/titles",f)).titles||[];Object.assign(P,f);renderTitles();}catch(e){toast(e.message,"err");renderTitles();}finally{busy(b,false)}}
function pick(i){Object.assign(P,form(),{title:TITLES[i].title});$("title").value=P.title;dirty();go("roteiro");toast("Título escolhido. Agora gere o roteiro.");}

function renderScenes(){renderOverview();const n=P.scenes.length,w=P.scenes.reduce((a,s)=>a+words(s.narration),0);
 $("stats").innerHTML=n?[["Cenas",n],["Palavras",w.toLocaleString("pt-BR")],["Duração estimada",(w/150).toFixed(1).replace(".",",")+" min"],["Meta",(P.minutes||form().minutes)+" min"],["Revisadas",`${P.scenes.filter(s=>s.reviewed).length}/${n}`],["A checar",P.scenes.filter(s=>s.needs_check).length]].map(([a,b])=>`<div class="stat"><small>${a}</small><b>${b}</b></div>`).join(""):"";
 $("savebar").style.display=n||P.title?"flex":"none";
 $("scenes").innerHTML=n?P.scenes.map((s,i)=>`<div class="card scene${s.reviewed?" reviewed":""}${s.needs_check?" check":""}"><div class="num">${i+1}</div>
  <div class="field"><label>Narração</label><textarea rows="4" oninput="edit(${i},'narration',this)">${esc(s.narration)}</textarea><div class="counter" id="c${i}">${words(s.narration)} palavras · ~${Math.round(words(s.narration)/150*60)}s</div></div>
  <div class="field"><label>Prompt visual (Grok Imagine)</label><textarea rows="4" oninput="edit(${i},'visual_prompt',this)">${esc(s.visual_prompt)}</textarea></div>
  <div class="facts"><div><label>Fatos-chave</label><ul>${(s.key_facts||[]).map(f=>`<li>${esc(f)}</li>`).join("")||'<li class="muted">—</li>'}</ul></div>
  <div><label>Fontes</label><ul>${(s.sources||[]).map(x=>`<li>${x.url&&/^https?:/.test(x.url)?`<a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(x.title||x.url)}</a>`:`${esc(x.title||"")} <span class="chip warn sm">verificar</span>`}</li>`).join("")||'<li class="muted">Nenhuma fonte</li>'}</ul></div>
  <div class="rev">${s.needs_check?'<span class="chip warn">Checar afirmações</span>':""}<label class="checkbox"><input type="checkbox" ${s.reviewed?"checked":""} onchange="review(${i},this.checked)">Revisado</label></div></div></div>`).join("")
  :`<div class="empty"><div class="ill">${svg("roteiro")}</div><b>Sem roteiro ainda</b><p>Com o título definido, clique em “Gerar roteiro”. O ChatGPT divide o texto em cenas de 6 a 10 segundos.</p></div>`;renderNav();}
function review(i,v){P.scenes[i].reviewed=v;dirty();renderScenes();}
function renderOverview(){$("overview").innerHTML=P.hook||(P.retention_beats||[]).length?`<div class="card overview"><div><label>Gancho (primeiros 30s)</label><p>${esc(P.hook)}</p></div><div><label>Pontos de retenção</label><ol>${(P.retention_beats||[]).map(b=>`<li>${esc(b)}</li>`).join("")}</ol></div></div>`:"";}
function edit(i,k,el){P.scenes[i][k]=el.value;if(k=="narration"){const w=words(el.value);$("c"+i).textContent=`${w} palavras · ~${Math.round(w/150*60)}s`;}dirty();}
function dirty(){$("savebar").classList.remove("saved");$("saveState").textContent="Alterações não salvas";}
async function script(){const t=$("title").value.trim();if(!t)return toast("Defina um título primeiro.","err");
 const b=$("btnScript");busy(b,true,"Escrevendo roteiro...");$("scenes").innerHTML='<div class="skel s"></div>'.repeat(3);$("stats").innerHTML="";
 try{const d=await api("/api/script",{...form(),...pickForm(),title:t});Object.assign(P,{title:d.title||t,description:d.description,hook:d.hook,retention_beats:d.retention_beats||[],scenes:(d.scenes||[]).map(s=>({...s,reviewed:false}))});$("title").value=P.title;renderScenes();dirty();toast(`Roteiro gerado com ${P.scenes.length} cenas.`);}
 catch(e){toast(e.message,"err");renderScenes();}finally{busy(b,false)}}
function pickForm(){return{niche:P.niche||form().niche,language:P.language||form().language,minutes:P.minutes||form().minutes};}
async function save(){P.title=$("title").value.trim()||P.title;try{P=await api("/api/save",P);$("savebar").classList.add("saved");$("saveState").textContent="Salvo às "+new Date().toLocaleTimeString("pt-BR",{hour:"2-digit",minute:"2-digit"});toast("Projeto salvo.");renderNav();}catch(e){toast(e.message,"err")}}

function renderCenas(){$("cenas").innerHTML=P.scenes.length?P.scenes.map((s,i)=>`<div class="card thumb"><div class="frame"><span class="k">Cena ${i+1}</span>${svg("film")}</div><div class="body"><span class="chip">Aguardando clipe</span><p>${esc(s.visual_prompt)}</p></div></div>`).join("")
 :`<div class="empty" style="grid-column:1/-1"><div class="ill">${svg("cenas")}</div><b>Nenhuma cena</b><p>Gere ou abra um roteiro para ver aqui um quadro por cena.</p><button class="btn ghost sm" onclick="go('roteiro')">Ir para Roteiro</button></div>`;}
function pipe(id,items){$(id).innerHTML=items.map(([ic,t,d],i)=>`<div class="card pstep"><div class="ic">${svg(ic)}</div><small>PASSO ${i+1}</small><b>${t}</b><p>${d}</p></div>`).join("");}
pipe("pipeMontagem",[["mic","Narração completa","Roteiro inteiro em uma única voz via OpenAI TTS, sem cortes de tom."],["film","Clipes sincronizados","Cada clipe do Grok ajustado à duração do seu trecho de narração."],["music","Trilha sonora","Música ambiente dark mixada abaixo da voz."],["cc","Legendas e export","ffmpeg gera MP4 1920×1080 com legendas embutidas."]]);
pipe("pipePublicacao",[["img","Thumbnail","Imagem 1280×720 de alto contraste a partir da cena mais forte."],["text","Título e descrição","Na língua do vídeo, com capítulos e gancho no começo."],["hash","Tags","Palavras-chave do nicho para busca e sugeridos."],["globe","Pronto para enviar","Pacote final para subir no YouTube Studio."]]);

async function loadProjects(){$("projects").innerHTML='<div class="skel" style="height:240px"></div>'.repeat(3);
 let l=[];try{l=await (await fetch("/api/projects")).json()}catch{}
 const nw=`<button class="new-proj" onclick="newProject()"><div><div class="ill" style="margin:0 auto 10px;width:44px;height:44px;border-radius:12px;background:var(--card2);display:grid;place-items:center">${svg("spark")}</div><b style="color:var(--text)">Novo projeto</b><div style="font-size:13px">Comece por uma ideia</div></div></button>`;
 $("projects").innerHTML=nw+l.map(p=>`<div class="card proj" onclick="openProj('${esc(p.id)}')"><div class="cover">${svg("film")}</div><div class="body"><b>${esc(p.title||"Sem título")}</b><div class="meta"><span class="chip">${esc(p.language||"—")}</span><span>${esc(p.updated_at||"")}</span></div></div></div>`).join("");}
async function openProj(id){try{const r=await fetch("/api/projects/"+encodeURIComponent(id));if(!r.ok)throw 0;P=await r.json();P.scenes=P.scenes||[];fill();TITLES=[];renderTitles();renderScenes();$("savebar").classList.add("saved");$("saveState").textContent="Salvo";go("roteiro");}catch{toast("Não foi possível abrir o projeto.","err")}}
function newProject(){P={scenes:[]};TITLES=[];["theme","title"].forEach(k=>$(k).value="");$("niche").value="Business & Finance Documentary";$("language").value="English";$("minutes").value=10;renderTitles();renderScenes();go("ideia");}

function notice(){if(HASKEY||sessionStorage.dyHide){$("notice").innerHTML="";return}
 $("notice").innerHTML=`<div class="card notice"><span class="ic">${svg("key")}</span><div><b>Chave da OpenAI não configurada</b><p>Sem ela, as sugestões de título e o roteiro não funcionam. <a onclick="this.closest('.notice').querySelector('ol').hidden^=1">Ver como configurar</a></p>
 <ol hidden><li>Na pasta do app, copie <code>.env.example</code> para <code>.env</code></li><li>Coloque sua chave em <code>OPENAI_API_KEY=</code></li><li>Feche e abra o app de novo</li></ol></div><button class="icon-btn" title="Dispensar" onclick="sessionStorage.dyHide=1;notice()">${svg("x")}</button></div>`;}
const PRESETS=[["Fraude & golpes","Fraud & Scams"],["Ascensão e queda de empresas","Rise and Fall of Companies"],["Dark truth de impérios","The Dark Truth About Business Empires"],["Bilionários","Billionaires"],["História do dinheiro","History of Money"]];
$("presets").innerHTML=PRESETS.map(([a,b],i)=>`<button class="preset" onclick="preset(${i},this)">${a}</button>`).join("");
function preset(i,el){document.querySelectorAll(".preset").forEach(b=>b.classList.toggle("on",b==el));$("niche").value="Business & Finance Documentary — "+PRESETS[i][1];}
(async()=>{try{const s=await (await fetch("/api/status")).json();HASKEY=s.has_key;
 $("keyStatus").innerHTML=s.has_key?`<i class="dot done"></i>OpenAI conectada · ${esc(s.model)}`:`<i class="dot" style="background:var(--warn)"></i>Chave OpenAI ausente`;}catch{}
 notice();emptyTitles();renderScenes();const h=location.hash.slice(1);if(h.startsWith("p=")){openProj(decodeURIComponent(h.slice(2)));return;}go(STEPS.some(s=>s[0]==h)?h:"projetos");})();
