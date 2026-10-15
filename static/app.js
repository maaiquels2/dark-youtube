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
 if(k=="cenas"){renderCenas();if(P.scenes.some(s=>s.status=="gerando"))startPoll();}if(k=="projetos")loadProjects();renderNav();window.scrollTo(0,0);}
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
  <div class="field"><label>Descrição da cena</label><textarea rows="3" class="desc-sm" oninput="edit(${i},'visual_prompt',this)">${esc(s.visual_prompt)}</textarea></div><div class="field prompt-row"><div class="prompt-head"><label>Prompt completo (Grok Imagine)</label><button class="btn primary sm" onclick="copyPrompt(${i})">Copiar prompt completo</button></div><div class="full-prompt" id="gp${i}">${esc(buildGrokPrompt(s))}</div></div>
  <div class="facts"><div><label>Fatos-chave</label><ul>${(s.key_facts||[]).map(f=>`<li>${esc(f)}</li>`).join("")||'<li class="muted">—</li>'}</ul></div>
  <div><label>Fontes</label><ul>${(s.sources||[]).map(x=>`<li>${x.url&&/^https?:/.test(x.url)?`<a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(x.title||x.url)}</a>`:`${esc(x.title||"")} <span class="chip warn sm">verificar</span>`}</li>`).join("")||'<li class="muted">Nenhuma fonte</li>'}</ul></div>
  <div class="rev">${s.needs_check?'<span class="chip warn">Checar afirmações</span>':""}<label class="checkbox"><input type="checkbox" ${s.reviewed?"checked":""} onchange="review(${i},this.checked)">Revisado</label></div></div></div>`).join("")
  :`<div class="empty"><div class="ill">${svg("roteiro")}</div><b>Sem roteiro ainda</b><p>Com o título definido, clique em “Gerar roteiro”. O ChatGPT divide o texto em cenas de 6 a 10 segundos.</p></div>`;renderNav();}
function review(i,v){P.scenes[i].reviewed=v;dirty();renderScenes();}
function renderOverview(){$("overview").innerHTML=P.hook||(P.retention_beats||[]).length?`<div class="card overview"><div><label>Gancho (primeiros 30s)</label><p>${esc(P.hook)}</p></div><div><label>Pontos de retenção</label><ol>${(P.retention_beats||[]).map(b=>`<li>${esc(b)}</li>`).join("")}</ol></div></div>`:"";}
function edit(i,k,el){P.scenes[i][k]=el.value;if(k=="visual_prompt"||k=="narration"){const g=$("gp"+i);if(g)g.textContent=buildGrokPrompt(P.scenes[i]);}if(k=="narration"){const w=words(el.value);$("c"+i).textContent=`${w} palavras · ~${Math.round(w/150*60)}s`;}dirty();}
function dirty(){$("savebar").classList.remove("saved");$("saveState").textContent="Alterações não salvas";}
async function script(){const t=$("title").value.trim();if(!t)return toast("Defina um título primeiro.","err");
 const b=$("btnScript");busy(b,true,"Escrevendo roteiro...");$("scenes").innerHTML='<div class="skel s"></div>'.repeat(3);$("stats").innerHTML="";
 try{const d=await api("/api/script",{...form(),...pickForm(),title:t});Object.assign(P,{title:d.title||t,description:d.description,hook:d.hook,retention_beats:d.retention_beats||[],scenes:(d.scenes||[]).map(s=>({...s,reviewed:false}))});$("title").value=P.title;renderScenes();dirty();toast(`Roteiro gerado com ${P.scenes.length} cenas.`);}
 catch(e){toast(e.message,"err");renderScenes();}finally{busy(b,false)}}
function pickForm(){return{niche:P.niche||form().niche,language:P.language||form().language,minutes:P.minutes||form().minutes};}
async function save(){P.title=$("title").value.trim()||P.title;try{P=await api("/api/save",P);$("savebar").classList.add("saved");$("saveState").textContent="Salvo às "+new Date().toLocaleTimeString("pt-BR",{hour:"2-digit",minute:"2-digit"});toast("Projeto salvo.");renderNav();}catch(e){toast(e.message,"err")}}

let PRICE=null,HASXAI=false,SEL=new Set(),POLL=null;
const MODELS={video:["grok-imagine-video-1.5-lite","grok-imagine-video","grok-imagine-video-1.5"],image:["grok-imagine-image","grok-imagine-image-2.0","grok-imagine-image-quality"]};
const ST={pendente:["Pendente",""],gerando:["Gerando","warn"],pronto:["Pronto","ok"],erro:["Erro","err"]};
function fillModels(id,mode,val){$(id).innerHTML=MODELS[mode].map(m=>`<option${m==val?" selected":""}>${m}</option>`).join("");}
function secs(s){return Math.max(1,words(s.narration)/((PRICE&&PRICE.words_per_minute)||150)*60);}
function vidSecs(s){const mx=(PRICE&&PRICE.video_max_seconds)||15;return Math.min(mx,Math.max(1,Math.ceil(secs(s))));}
function defaultPlan(){const n=P.scenes.length,hot=new Set();let t=0;P.scenes.forEach((s,i)=>{if(t<30)hot.add(i);t+=secs(s);});
 const B=(P.retention_beats||[]).length;for(let k=0;k<B;k++)hot.add(Math.min(n-1,Math.round((k+1)*n/(B+1))));return hot;}
function ensurePlan(force){const hot=defaultPlan();let ch=false;P.scenes.forEach((s,i)=>{if(force||!s.mode){s.mode=hot.has(i)?"video":"image";s.source="api";s.model=s.mode=="video"?"grok-imagine-video-1.5-lite":"grok-imagine-image";s.beat=hot.has(i);ch=true;}if(!s.status)s.status="pendente";});return ch;}
function estCost(s){if(!PRICE||s.source=="site")return 0;return s.mode=="video"?vidSecs(s)*(PRICE.video_per_second[s.model]||0):(PRICE.image[s.model]||0);}
const usd=v=>"US$ "+v.toFixed(2).replace(".",",");
function renderCost(){if(!PRICE)return;const g={};let tot=0,site=0,spent=0;
 P.scenes.forEach(s=>{const c=estCost(s);tot+=c;if(s.source=="site"){site++;return;}const k=s.model;g[k]=g[k]||{n:0,s:0,c:0};g[k].n++;g[k].c+=c;if(s.mode=="video")g[k].s+=vidSecs(s);});
 P.scenes.forEach(s=>spent+=s.cost_usd||0);const buf=tot*(PRICE.retry_buffer||0);
 $("cost").innerHTML=`<h3>Custo estimado</h3><div class="cost-total"><b>${usd(tot+buf)}</b><span class="muted">com +${Math.round((PRICE.retry_buffer||0)*100)}% para refazer cenas</span></div>
 <table class="cost-tbl">${Object.entries(g).map(([m,v])=>`<tr><td>${m}</td><td class="muted">${v.n} ${v.s?`· ${v.s}s`:"img"}</td><td>${usd(v.c)}</td></tr>`).join("")}
 ${site?`<tr><td>Site do Grok</td><td class="muted">${site} cenas</td><td>US$ 0,00</td></tr>`:""}
 <tr class="sub"><td>Subtotal</td><td></td><td>${usd(tot)}</td></tr><tr class="sub"><td>Folga (${Math.round((PRICE.retry_buffer||0)*100)}%)</td><td></td><td>${usd(buf)}</td></tr>
 <tr class="sub"><td>Já gasto</td><td></td><td>${usd(spent)}</td></tr></table><p class="hint">Preços em config/pricing.json (docs.x.ai, 15/10/2026).</p>`;}
function selectAll(v){SEL=new Set(v?P.scenes.map((_,i)=>i):[]);renderCenas();}
function toggleSel(i,v){v?SEL.add(i):SEL.delete(i);$("selCount").textContent=SEL.size?`${SEL.size} selecionadas`:"";renderCost();}
function applyBulk(onlySel){if(onlySel&&!SEL.size)return toast("Selecione pelo menos uma cena.","err");const m=$("bMode").value,src=$("bSource").value,mo=$("bModel").value;
 P.scenes.forEach((s,i)=>{if(!onlySel||SEL.has(i)){s.mode=m;s.source=src;s.model=mo;}});dirty();autoSave();renderCenas();toast("Plano atualizado.");}
function resetDefaults(){if(!confirm("Voltar todas as cenas para o plano padrão (gancho e retenção em vídeo, o resto em imagem animada)?"))return;ensurePlan(true);autoSave();renderCenas();}
function setScene(i,k,v){const s=P.scenes[i];s[k]=v;if(k=="mode")s.model=MODELS[v][0];autoSave();renderCenas();}
let saveT=null;function autoSave(){clearTimeout(saveT);saveT=setTimeout(()=>{if(P.id)api("/api/save",P).then(d=>{P.updated_at=d.updated_at}).catch(e=>toast(e.message,"err"))},500);}
function preview(s){if(!s.file)return svg(s.mode=="video"?"film":"img");const u=`/media/${encodeURIComponent(P.id)}/${encodeURIComponent(s.file.split("/").pop())}?t=${encodeURIComponent(P.updated_at||"")}${s.gen_seconds||""}`;
 return /\.(mp4|webm|mov)$/i.test(s.file)?`<video src="${u}" muted loop playsinline onmouseenter="this.play()" onmouseleave="this.pause()"></video>`:`<img src="${u}" alt="">`;}
function renderCenas(){renderAuto();if(!P.scenes.length){$("cost").innerHTML="";$("cenas").innerHTML=`<div class="empty" style="grid-column:1/-1"><div class="ill">${svg("cenas")}</div><b>Nenhuma cena</b><p>Gere ou abra um roteiro para ver aqui um quadro por cena.</p><button class="btn ghost sm" onclick="go('roteiro')">Ir para Roteiro</button></div>`;return;}
 if(ensurePlan(false))autoSave();renderCost();
 const done=P.scenes.filter(s=>s.status=="pronto").length,run=P.scenes.filter(s=>s.status=="gerando").length,err=P.scenes.filter(s=>s.status=="erro").length;
 $("genProgress").innerHTML=`<div class="progress"><div style="width:${done/P.scenes.length*100}%"></div></div><span>${done}/${P.scenes.length} prontas${run?` · ${run} gerando`:""}${err?` · ${err} com erro`:""}</span>`;
 $("selCount").textContent=SEL.size?`${SEL.size} selecionadas`:"";$("selAll").checked=SEL.size==P.scenes.length;
 $("cenas").innerHTML=P.scenes.map((s,i)=>{const [lab,cls]=ST[s.status]||ST.pendente;const busy=s.status=="gerando";
 return `<div class="card thumb${SEL.has(i)?" sel":""}"><div class="frame">${preview(s)}<span class="k">Cena ${i+1} · ${Math.round(secs(s))}s</span>${s.beat?'<span class="beat">gancho/retenção</span>':""}
  <input type="checkbox" class="pick" ${SEL.has(i)?"checked":""} onchange="toggleSel(${i},this.checked);this.closest('.thumb').classList.toggle('sel',this.checked)">${busy?'<div class="overlay"><span class="spin"></span></div>':""}</div>
  <div class="body"><div class="thumb-head"><span class="chip ${cls}">${lab}</span>${autoChip(i)}<span class="muted">${s.source=="site"?"US$ 0":usd(estCost(s))}${s.cost_usd!=null&&s.status=="pronto"?` · gasto ${usd(s.cost_usd)}`:""}</span></div>
  <div class="mini"><select onchange="setScene(${i},'mode',this.value)" ${busy?"disabled":""}><option value="video"${s.mode=="video"?" selected":""}>Vídeo</option><option value="image"${s.mode=="image"?" selected":""}>Imagem animada</option></select>
  <select onchange="setScene(${i},'source',this.value)" ${busy?"disabled":""}><option value="api"${s.source=="api"?" selected":""}>API xAI</option><option value="site"${s.source=="site"?" selected":""}>Site do Grok</option></select></div>
  ${s.source=="api"?`<select class="model" onchange="setScene(${i},'model',this.value)" ${busy?"disabled":""}>${MODELS[s.mode].map(m=>`<option${m==s.model?" selected":""}>${m}</option>`).join("")}</select>`:""}
  <div class="full-prompt sm">${esc(buildGrokPrompt(s))}</div><button class="btn ghost sm" onclick="copyPrompt(${i})">Copiar prompt completo</button>${s.error?`<div class="scene-err">${esc(s.error)}</div>`:""}
  <div class="thumb-actions">${s.source=="api"?`<button class="btn ${s.file?"ghost":"primary"} sm" ${busy?"disabled":""} onclick="genOne(${i})">${busy?"Gerando...":s.file?"Regenerar":s.status=="erro"?"Tentar de novo":"Gerar"}</button>`
   :`<button class="btn primary sm" onclick="openGrok(${i})">Copiar prompt e abrir Grok</button>`}
  <label class="btn ghost sm upl">${s.file?"Substituir":"Enviar arquivo"}<input type="file" accept="video/*,image/*" hidden onchange="upload(${i},this.files[0])"></label></div></div></div>`;}).join("");}
async function genOne(i){if(!HASXAI)return toast("Configure XAI_API_KEY no .env para gerar pela API.","err");if(P.scenes[i].file&&!confirm(`Regenerar a cena ${i+1}? Custa ${usd(estCost(P.scenes[i]))}.`))return;await startGen([i]);}
async function genPending(){if(!HASXAI)return toast("Configure XAI_API_KEY no .env para gerar pela API.","err");
 const idx=P.scenes.map((s,i)=>i).filter(i=>{const s=P.scenes[i];return s.source=="api"&&s.status!="pronto"&&s.status!="gerando"});
 if(!idx.length)return toast("Não há cenas pendentes para a API.");const c=idx.reduce((a,i)=>a+estCost(P.scenes[i]),0);
 if(!confirm(`Gerar ${idx.length} cenas pela API da xAI? Custo estimado: ${usd(c)}.`))return;await startGen(idx);}
async function startGen(idx){try{await api("/api/save",P);const r=await api("/api/generate",{id:P.id,scenes:idx});toast(`${r.started.length} cena(s) na fila.`);await refresh();startPoll();}catch(e){toast(e.message,"err")}}
async function refresh(){const d=await (await fetch("/api/projects/"+encodeURIComponent(P.id))).json();
 d.scenes.forEach((s,i)=>{if(P.scenes[i])["status","file","error","cost_usd","gen_seconds","media_duration","generated_with"].forEach(k=>{if(k in s)P.scenes[i][k]=s[k];else delete P.scenes[i][k];});});
 P.updated_at=d.updated_at;if(VIEW=="cenas")renderCenas();return d;}
function startPoll(){if(POLL)return;POLL=setInterval(async()=>{try{await refresh();if(!P.scenes.some(s=>s.status=="gerando")){clearInterval(POLL);POLL=null;toast("Geração concluída.");}}catch{}},4000);}
async function openGrok(i){try{await save();}catch{}const t=buildGrokPrompt(P.scenes[i]);try{await navigator.clipboard.writeText(t);toast("Prompt copiado. Cole no Grok Imagine.");}catch{prompt("Copie o prompt:",t);}
 window.open("https://grok.com/imagine","_blank","noopener");}
async function upload(i,f){if(!f)return;if(!P.id)await save();try{const r=await fetch(`/api/upload?id=${encodeURIComponent(P.id)}&i=${i}&name=${encodeURIComponent(f.name)}`,{method:"POST",body:f});const d=await r.json();if(!r.ok)throw new Error(d.error);await refresh();toast(`Arquivo anexado à cena ${i+1}.`);}catch(e){toast(e.message,"err")}}
function xaiNotice(){$("xaiNotice").innerHTML=HASXAI?"":`<div class="card notice"><span class="ic">${svg("key")}</span><div><b>Chave da xAI não configurada</b><p>Sem ela, só dá para usar o Site do Grok e enviar os arquivos à mão. Para gerar pela API, coloque <code>XAI_API_KEY=</code> no arquivo <code>.env</code> e reinicie o app.</p></div></div>`;}
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
(async()=>{try{PRICE=await (await fetch("/api/pricing")).json();fillModels("bModel","video");}catch{}try{const s=await (await fetch("/api/status")).json();HASKEY=s.has_key;HASXAI=!!s.has_xai;xaiNotice();
 $("keyStatus").innerHTML=s.has_key?`<i class="dot done"></i>OpenAI conectada · ${esc(s.model)}`:`<i class="dot" style="background:var(--warn)"></i>Chave OpenAI ausente`;}catch{}
 notice();emptyTitles();renderScenes();const h=location.hash.slice(1);if(h.startsWith("p=")){const [pid,v]=decodeURIComponent(h.slice(2)).split("|");openProj(pid).then(()=>{if(v){if(v=="cenas")VIEW="cenas";go(v)}});return;}go(STEPS.some(s=>s[0]==h)?h:"projetos");})();

const GROK_STYLE="Style: dark cinematic documentary, moody low-key lighting with deep shadows and cold teal-and-amber contrast, volumetric haze, shallow depth of field, anamorphic lens look, subtle film grain, photorealistic, premium Netflix-style business documentary aesthetic.";
const GROK_NEG="Avoid: no text, no captions, no watermark, no logos or trademarks, no real person likeness, no distorted faces or hands, no extra limbs, no cartoon look, no blur artifacts.";
function cleanSubject(vp){let t=(vp||"").trim().replace(/\b(dark\s+)?cinematic\s+16:9\s*/i,"").trim();t=t.replace(/,?\s*no logos?,?\s*(no text,?)?\s*(no identifiable people\.?)?\s*$/i,"").replace(/^[\s,.]+|[\s,.]+$/g,"");t=t.split(" | ")[0];return t?t[0].toUpperCase()+t.slice(1):"Atmospheric establishing shot that illustrates the narration";}
function buildGrokPrompt(s){const narr=(s.narration||"").replace(/\s+/g," ").trim();const p=[`Subject: ${cleanSubject(s.visual_prompt)}.`];
 if(narr)p.push(`Context (illustrate this narration, do not write it on screen): "${narr.slice(0,240).replace(/\.+$/,"")}".`);
 p.push("Composition: wide cinematic framing, strong leading lines, clear focal subject, rule of thirds.",GROK_STYLE);
 if(s.mode=="video"){const w=narr?narr.split(" ").length:0;const d=Math.min(15,Math.max(1,Math.ceil(Math.max(1,w/150*60))));
  p.push(`Motion: slow cinematic camera movement (gentle dolly-in or slow parallax pan), subtle atmospheric motion (drifting haze, flickering lights), smooth and stable, no cuts. Duration: about ${d} seconds (max 15s), no audio.`,"Format: video, aspect ratio 16:9, 1920x1080, high resolution, ultra detailed.");}
 else p.push("Format: still image, aspect ratio 16:9, 1920x1080, high resolution, ultra detailed, sharp focus.");
 p.push(GROK_NEG);return p.join(" ");}
async function copyPrompt(i){const t=buildGrokPrompt(P.scenes[i]);try{await navigator.clipboard.writeText(t);toast("Prompt completo copiado.");}catch{prompt("Copie o prompt:",t);}}

let AUTO={},AUTOPOLL=null;
const AUTOLAB={starting:"Iniciando",running:"Gerando",paused:"Pausado",needs_user:"Precisa de você",done:"Concluído",stopped:"Parado",error:"Erro"};
function autoChip(i){const a=(AUTO.scenes||{})[i];if(!a||!AUTO.running&&a.status=="pronto")return"";const c={"gerando":"run","na fila":"","pronto":"ok","erro":"err"}[a.status]||"";return `<span class="chip auto ${c}" title="${esc(a.error||"")}">Grok auto: ${esc(a.status)}</span>`;}
function renderAuto(){const el=$("autoPanel");if(!el)return;const st=AUTO.state,run=AUTO.running,paused=AUTO.control=="pause";
 const sc=Object.values(AUTO.scenes||{}),ok=sc.filter(x=>x.status=="pronto").length,er=sc.filter(x=>x.status=="erro").length;
 el.innerHTML=`<div class="auto-head"><div><h3>Gerar no Grok (automático)</h3><p class="muted">Usa um Chrome só do Dark Studio, logado na sua conta do Grok. Abre até ${AUTO.concurrency||2} abas, cola o prompt completo, gera e baixa cada cena.</p></div>
 <div class="auto-btns"><button class="btn ghost" onclick="autoLogin()">Abrir Chrome do Grok (login)</button>
 ${run?`${paused?`<button class="btn primary" onclick="autoCtl('run')">Retomar</button>`:`<button class="btn ghost" onclick="autoCtl('pause')">Pausar</button>`}<button class="btn ghost danger" onclick="autoCtl('stop')">Parar</button>`
  :`<button class="btn primary" onclick="autoStart()">Gerar no Grok (automático)</button>`}</div></div>
 ${st?`<div class="auto-state ${st}"><b>${AUTOLAB[st]||st}</b> · ${esc(AUTO.message||"")}${sc.length?` · ${ok}/${sc.length} prontas${er?` · ${er} com erro`:""}`:""}${AUTO.updated_at?` <span class="muted">(${AUTO.updated_at})</span>`:""}</div>`:""}`;}
async function autoRefresh(){if(!P.id)return;try{AUTO=await (await fetch("/api/grok_auto?id="+encodeURIComponent(P.id))).json();}catch{return;}
 if(VIEW=="cenas"){await refresh().catch(()=>{});}
 if(!AUTO.running&&AUTOPOLL){clearInterval(AUTOPOLL);AUTOPOLL=null;}renderAuto();}
function autoPoll(){if(!AUTOPOLL)AUTOPOLL=setInterval(autoRefresh,4000);autoRefresh();}
async function autoStart(){if(!P.id)await save();const sel=[...SEL];try{await api("/api/grok_auto/start",{id:P.id,scenes:sel.length?sel:null});toast(sel.length?`Gerando ${sel.length} cenas no Grok.`:"Gerando cenas pendentes no Grok.");autoPoll();}catch(e){toast(e.message);}}
async function autoCtl(a){try{AUTO=await api("/api/grok_auto/control",{id:P.id,action:a});renderAuto();toast({run:"Retomado.",pause:"Pausado.",stop:"Parando..."}[a]);autoPoll();}catch(e){toast(e.message);}}
async function autoLogin(){try{await api("/api/grok_auto/login",{});toast("Chrome do Dark Studio aberto no Grok. Faça login uma vez.");}catch(e){toast(e.message);}}
setTimeout(()=>{if(P&&P.id)autoRefresh().then(()=>{if(AUTO.running)autoPoll();});},1500);
