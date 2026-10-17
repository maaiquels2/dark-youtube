let TITLES_META={};
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
const STEPS=[["ideia","Ideia"],["pesquisa","Pesquisa"],["roteiro","Roteiro"],["imagens","Imagens reais"],["prompts","Prompts Grok"],["cenas","Cenas"],["validacao","Validação"],["montagem","Montagem"],["publicacao","Publicação"]];
Object.assign(I,{pesquisa:'<circle cx="11" cy="11" r="7"/><path d="M21 21l-5-5"/>',imagens:'<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 17l-6-6-9 8"/>',prompts:'<path d="M4 6h16M4 12h10M4 18h7"/><path d="M17 15l2 2 3-4"/>',validacao:'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>'});
const NST=STEPS.length;
const $=id=>document.getElementById(id);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const words=t=>(t||"").trim().split(/\s+/).filter(Boolean).length;
let P={scenes:[]},TITLES=[],VIEW="projetos",HASKEY=true;

function toast(t,kind="ok"){const d=document.createElement("div");d.className="toast "+kind;d.innerHTML=svg(kind=="err"?"alert":"check")+`<div>${esc(t)}</div>`;$("toasts").append(d);setTimeout(()=>d.remove(),kind=="err"?7000:3500);}
function stepDone(k){const st=P._stages||{};if(["pesquisa","imagens","prompts","validacao"].includes(k))return !!st[k];if(k=="ideia")return !!P.title;if(k=="roteiro")return P.scenes.length>0;if(k=="cenas")return !!st.cenas||(P.scenes.length>0&&P.scenes.every(s=>s.status=="pronto"&&s.file));if(k=="montagem")return !!st.montagem||!!(MONT&&MONT.final);if(k=="publicacao")return (P.status=="publicado"||P.status=="agendado")&&!!P.published_url;return false;}
function renderNav(){
 $("steps").innerHTML=STEPS.map(([k,n,s],i)=>`<button class="nav-item${VIEW==k?" active":""}" onclick="go('${k}')">${svg(k)}<span>${n}</span>${s?'<span class="tag">em breve</span>':`<i class="dot${stepDone(k)?" done":""}"></i>`}</button>`).join("");
 document.querySelector('[data-view=projetos]').classList.toggle("active",VIEW=="projetos");
 const idx=STEPS.findIndex(s=>s[0]==VIEW);const done=STEPS.filter(s=>stepDone(s[0])).length;
 $("progressText").textContent=idx<0||done==NST?`${done} de ${NST} etapas concluídas${P.status=="publicado"?" · Publicado":P.status=="agendado"?" · Agendado "+fmtSched(P.scheduled_at):""}`:`Etapa ${idx+1} de ${NST} · ${STEPS[idx][1]}`;
 $("progressBar").style.width=(done/NST*100)+"%";{const hc=$("crumbCover");if(hc){if(P&&P.id&&P._cover){hc.src=`/files/${encodeURIComponent(P.id)}/cover?v=${encodeURIComponent(P._cover)}`;hc.style.display="";}else hc.style.display="none";}}
 $("crumbStep").textContent=idx<0?"Projetos":STEPS[idx][1];
 $("crumbProject").textContent=P.title||(P.id?"Projeto sem título":"Novo projeto");
}
function go(k){if(["pesquisa","imagens","prompts","validacao"].includes(k))setTimeout(()=>renderStage(k),30);if(k=="publicacao")setTimeout(renderPub,30);if(k=="montagem")setTimeout(()=>{montRefresh().then(()=>{if(MONT.running)montPoll();});},50);if(k=="cenas"&&VIEW!="cenas"){const u=P.scenes.filter(s=>!s.reviewed).length;if(u&&!confirm(`${u} de ${P.scenes.length} cenas ainda não foram revisadas (fatos e fontes). Ir para Cenas mesmo assim?`))return;}
VIEW=k;document.querySelectorAll(".view").forEach(v=>v.classList.toggle("on",v.id=="v-"+k));document.body.classList.remove("nav-open");
 if(k=="cenas"){renderCenas();if(P.scenes.some(s=>s.status=="gerando"))startPoll();}if(k=="projetos")loadProjects();renderNav();window.scrollTo(0,0);}
document.querySelector('[data-view=projetos]').onclick=()=>go("projetos");

async function api(path,body){const r=await fetch(path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
 let d;try{d=await r.json()}catch{d={error:"Resposta inválida do servidor"}}if(!r.ok)throw new Error(d.error||"Erro");return d;}
function busy(btn,on,label){btn.disabled=on;if(on){btn.dataset.h=btn.innerHTML;btn.innerHTML=`<span class="spin"></span>${label}`}else btn.innerHTML=btn.dataset.h;}
function form(){return{niche:$("niche").value.trim(),language:$("language").value,theme:$("theme").value.trim(),minutes:+$("minutes").value||10};}
function fill(){["niche","language","theme","minutes","title"].forEach(k=>{if(P[k]!=null)$(k).value=P[k]});}

function emptyTitles(){$("titles").innerHTML=`<div class="empty"><div class="ill">${svg("spark")}</div><b>Nenhuma sugestão ainda</b><p>Preencha nicho, língua e tema e clique em “Sugerir títulos”. As opções aparecem aqui para você escolher.</p></div>`;$("titlesCount").textContent="";}
/* Regras de clique (PADRAO_VIDEOS.md): avisa quando o titulo foge do padrao */
function titleWarn(t){const w=[],s=(t||"").trim();if(!s)return w;
 if(s.length>60)w.push(`${s.length} caracteres (máx. 60)`);
 if(/^[^:]{2,40}:\s/.test(s)&&!/^the\b/i.test(s))w.push("formato manchete “Nome: …”");
 if(/^(the )?rise and fall/i.test(s))w.push("“rise and fall” é título de assunto, não de história");
 return w;}
const FORMULA={A:"Personagem + valor + contradição",B:"Pergunta com “Actually”",C:"Explicado de forma simples"};
function renderTitles(){if(!TITLES.length)return emptyTitles();$("titlesCount").textContent=`${TITLES.length} opções`;
 const M=TITLES_META||{},dem={alta:"Procura alta",media:"Procura média",baixa:"Procura baixa (tema pouco buscado)"}[M.demand]||"";
 const head=(dem||M.series)?`<div class="card" style="margin-bottom:10px">${dem?`<p><b>${esc(dem)}</b>${M.demand_why?` · ${esc(M.demand_why)}`:""}</p>`:""}${M.series?`<p class="muted">Série sugerida: <b>${esc(M.series)}</b></p>`:""}</div>`:"";
 $("titles").innerHTML=head+TITLES.map((t,i)=>{const w=titleWarn(t.title);return `<div class="title-opt${P.title==t.title?" sel":""}" onclick="pick(${i})"><div class="n">${i+1}</div><div><b>${esc(t.title)}</b><p>${esc(t.hook)}</p>${t.why?`<p class="why">${svg("check")}${esc(t.why)}</p>`:""}${t.formula?`<span class="chip sm">${esc(FORMULA[t.formula]||t.formula)}</span>`:""}${t.thumb_text?` <span class="chip sm">Capa: ${esc(t.thumb_text)}</span>`:""}${w.length?`<p class="why" style="color:#d9822b">⚠ ${esc(w.join(" · "))}</p>`:""}</div><span class="go">${svg("arrow")}</span></div>`}).join("");}
async function titles(){const f=form();if(!f.niche&&!f.theme)return toast("Preencha pelo menos o nicho ou o tema.","err");
 const b=$("btnTitles");busy(b,true,"Gerando títulos...");$("titles").innerHTML='<div class="skel t"></div>'.repeat(5);
 try{const R=await api("/api/titles",f);TITLES=R.titles||[];TITLES_META={demand:R.demand,demand_why:R.demand_why,series:R.series};Object.assign(P,f);renderTitles();}catch(e){toast(e.message,"err");renderTitles();}finally{busy(b,false)}}
function pick(i){Object.assign(P,form(),{title:TITLES[i].title});$("title").value=P.title;dirty();go("roteiro");toast("Título escolhido. Agora gere o roteiro.");}

function renderScenes(){renderOverview();const n=P.scenes.length,w=P.scenes.reduce((a,s)=>a+words(s.narration),0);
 $("stats").innerHTML=n?[["Cenas",n],["Palavras",w.toLocaleString("pt-BR")],["Duração estimada",(w/150).toFixed(1).replace(".",",")+" min"],["Meta",(P.minutes||form().minutes)+" min"],["Revisadas",`${P.scenes.filter(s=>s.reviewed).length}/${n}`],["A checar",P.scenes.filter(s=>s.needs_check).length]].map(([a,b])=>`<div class="stat"><small>${a}</small><b>${b}</b></div>`).join(""):"";
 $("savebar").style.display=n||P.title?"flex":"none";
 $("scenes").innerHTML=n?P.scenes.map((s,i)=>`<div class="card scene${s.reviewed?" reviewed":""}${s.needs_check?" check":""}"><div class="num">${i+1}</div>
  <div class="field"><label>Narração</label><textarea rows="4" oninput="edit(${i},'narration',this)">${esc(s.narration)}</textarea><div class="counter" id="c${i}">${words(s.narration)} palavras · ~${Math.round(words(s.narration)/150*60)}s</div></div>
  <div class="field"><label>Descrição da cena</label><textarea rows="3" class="desc-sm" oninput="edit(${i},'visual_prompt',this)">${esc(s.visual_prompt)}</textarea></div><div class="field prompt-row"><div class="prompt-head"><label>Prompt completo (Grok Imagine)</label><button class="btn primary sm" onclick="copyPrompt(${i})">Copiar prompt completo</button></div><div class="full-prompt" id="gp${i}">${esc(buildGrokPrompt(s))}</div></div>
  <div class="facts"><div><label>Fatos-chave</label><ul>${(s.key_facts||[]).map(f=>`<li>${esc(f)}</li>`).join("")||'<li class="muted">—</li>'}</ul></div>
  <div><label>Fontes</label><ul>${(s.sources||[]).map(x=>`<li>${x.url&&/^https?:/.test(x.url)?`<a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(x.title||x.url)}</a>`:`${esc(x.title||"")} <span class="chip warn sm">verificar</span>`}</li>`).join("")||'<li class="muted">Nenhuma fonte</li>'}</ul></div>
  <div class="gfx-row"><label>Gráficos na tela ${s.chapter?`<span class="chip ok sm">Capítulo: ${esc(s.chapter)}</span>`:""}</label><div class="gfx-chips">${(s.gfx||[]).map(g=>`<span class="chip gfx-${esc(g.type)}">${esc(GFXN[g.type]||g.type)}${g.name?": "+esc(g.name):g.text?": "+esc(String(g.text).slice(0,40)):g.title?": "+esc(String(g.title).slice(0,40)):g.amount?": "+esc(g.amount):g.company?": "+esc(g.company):""}</span>`).join("")||'<span class="muted">nenhum</span>'}</div>
   <details><summary>Editar gráficos (JSON)</summary><textarea rows="5" class="mono" onchange="gfxEdit(${i},this)">${esc(JSON.stringify(s.gfx||[],null,1))}</textarea></details></div>
  <div class="rev">${s.needs_check?'<span class="chip warn">Checar afirmações</span>':""}<label class="checkbox" title="Mostrar o logo (se ativado na Montagem) durante esta cena"><input type="checkbox" ${s.logo?"checked":""} onchange="P.scenes[${i}].logo=this.checked;dirty()">Logo nesta cena</label><label class="checkbox"><input type="checkbox" ${s.reviewed?"checked":""} onchange="review(${i},this.checked)">Revisado</label></div></div></div>`).join("")
  :`<div class="empty"><div class="ill">${svg("roteiro")}</div><b>Sem roteiro ainda</b><p>Com o título definido, clique em “Gerar roteiro”. O ChatGPT divide o texto em cenas de 6 a 10 segundos.</p></div>`;renderNav();}
const GFXN={chapter:"Capítulo",timeline:"Linha do tempo",chart:"Gráfico",document:"Documento",quote:"Citação",relmap:"Mapa de relações",scale:"Escala",headline:"Manchete",lower_third:"Pessoa",logo:"Logo",callout:"Valor",parties:"Envolvidos",citation:"Fonte"};
function gfxEdit(i,el){try{P.scenes[i].gfx=JSON.parse(el.value||"[]");el.classList.remove("err");dirty();}catch(e){el.classList.add("err");toast("JSON inválido: "+e.message,"err");}}
async function gfxRender(){try{await save();const d=await api("/api/gfx/render",{id:P.id});toast(`Gráficos: ${d.full} telas cheias, ${d.overlays} sobreposições.`);const r=await fetch("/api/projects/"+encodeURIComponent(P.id));P=await r.json();renderMont();}catch(e){toast(e.message,"err");}}
function review(i,v){P.scenes[i].reviewed=v;dirty();renderScenes();}
function renderOverview(){$("overview").innerHTML=P.hook||(P.retention_beats||[]).length?`<div class="card overview"><div><label>Gancho (primeiros 30s)</label><p>${esc(P.hook)}</p></div><div><label>Pontos de retenção</label><ol>${(P.retention_beats||[]).map(b=>`<li>${esc(b)}</li>`).join("")}</ol></div></div>`:"";}
function edit(i,k,el){P.scenes[i][k]=el.value;if(k=="visual_prompt"||k=="narration"){const g=$("gp"+i);if(g)g.textContent=buildGrokPrompt(P.scenes[i]);}if(k=="narration"){const w=words(el.value);$("c"+i).textContent=`${w} palavras · ~${Math.round(w/150*60)}s`;}dirty();}
function dirty(){$("savebar").classList.remove("saved");$("saveState").textContent="Alterações não salvas";}
async function script(){const t=$("title").value.trim();if(!t)return toast("Defina um título primeiro.","err");
 const b=$("btnScript");busy(b,true,"Escrevendo roteiro...");$("scenes").innerHTML='<div class="skel s"></div>'.repeat(3);$("stats").innerHTML="";
 try{const d=await api("/api/script",{...form(),...pickForm(),title:t});Object.assign(P,{title:t||d.title,description:d.description,hook:d.hook,retention_beats:d.retention_beats||[],scenes:(d.scenes||[]).map(s=>({...s,reviewed:false}))});$("title").value=P.title;renderScenes();dirty();toast(`Roteiro gerado com ${P.scenes.length} cenas.`);}
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
if($("pipeMontagem"))pipe("pipeMontagem",[["mic","Narração completa","Roteiro inteiro em uma única voz via OpenAI TTS, sem cortes de tom."],["film","Clipes sincronizados","Cada clipe do Grok ajustado à duração do seu trecho de narração."],["music","Trilha sonora","Música ambiente dark mixada abaixo da voz."],["cc","Legendas e export","ffmpeg gera MP4 1920×1080 com legendas embutidas."]]);
if($("pipePublicacao"))pipe("pipePublicacao",[["img","Thumbnail","Imagem 1280×720 de alto contraste a partir da cena mais forte."],["text","Título e descrição","Na língua do vídeo, com capítulos e gancho no começo."],["hash","Tags","Palavras-chave do nicho para busca e sugeridos."],["globe","Pronto para enviar","Pacote final para subir no YouTube Studio."]]);

async function loadProjects(){$("projects").innerHTML='<div class="skel" style="height:240px"></div>'.repeat(3);
 let l=[];try{l=await (await fetch("/api/projects")).json()}catch{}
 const nw=`<button class="new-proj" onclick="newProject()"><div><div class="ill" style="margin:0 auto 10px;width:44px;height:44px;border-radius:12px;background:var(--card2);display:grid;place-items:center">${svg("spark")}</div><b style="color:var(--text)">Novo projeto</b><div style="font-size:13px">Comece por uma ideia</div></div></button>`;
 $("projects").innerHTML=nw+l.map(p=>`<div class="card proj" onclick="openProj('${esc(p.id)}')"><div class="cover">${p.cover?`<img src="/files/${encodeURIComponent(p.id)}/cover?v=${encodeURIComponent(p.updated_at||"")}" alt="">`:svg("film")}</div><div class="body">${p.status=="publicado"?'<span class="st-chip ok">Publicado</span>':p.status=="agendado"?`<span class="st-chip warn">Agendado · ${esc(fmtSched(p.scheduled_at))}</span>`:""}<b>${esc(p.title||"Sem título")}</b><div class="meta"><span class="chip">${esc(p.language||"—")}</span><span class="chip">${p.stages_done||0}/${NST} etapas</span>${p.yt&&p.yt.views!=null?`<span class="chip ok">${EYE_SVG}${nf(p.yt.views)}</span>`:""}<span>${esc(p.updated_at||"")}</span></div>${ytBtns(p)}</div></div>`).join("");}
async function openProj(id,view){try{const r=await fetch("/api/projects/"+encodeURIComponent(id));if(!r.ok)throw 0;P=await r.json();P.scenes=P.scenes||[];fill();TITLES=[];renderTitles();renderScenes();$("savebar").classList.add("saved");$("saveState").textContent="Salvo";go(view||"roteiro");}catch{toast("Não foi possível abrir o projeto.","err")}}
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

// espelho de app.build_grok_prompt (manter igual ao Python)
const GROK_STYLE="Style: photorealistic cinematic documentary reconstruction, natural film look, subtle film grain, clear clean air, no letterbox bars, full-frame edge-to-edge image, premium business documentary aesthetic.";
const GROK_NEG="Avoid: no text, no captions, no watermark, no logos, no emblems, no brand marks or trademarks, blank unbranded walls and screens, no real person likeness, no distorted faces or hands, no extra limbs, no cartoon look, no blur artifacts, no subtitles or quotes on screen, no letterbox or black bars.";
const GROK_TEXT_GUARD="Papers, screens and signs are blank, blurred or turned away; people only from behind or in silhouette.";
const ACT_LOOK={act1:["confident, prosperous momentum","warm golden key light, rich amber tones with soft teal accents, lively but controlled contrast"],
 act2:["uneasy, investigative suspicion","cool blue-grey light, low-key contrast, deepening shadows, restrained teal palette"],
 act3:["grave, heavy, human cost","hard light and deep shadows, desaturated cold palette with small red accents"],
 after:["quiet, reflective aftermath","soft dawn or overcast light, muted desaturated palette, calm stillness"]};
const DEFAULT_LOOK=["tense, investigative business documentary atmosphere","moody low-key lighting with deep shadows and cold teal-and-amber contrast"];
const SHOT_COMPOSITION=[["over-the-shoulder","over-the-shoulder framing from behind an anonymous figure toward what they are looking at, focus on the object of attention"],
 ["macro","macro detail, one object filling the frame, very shallow depth of field"],["close","close-up, one subject filling most of the frame, shallow depth of field, soft background"],
 ["detail","detail shot, one object filling the frame, shallow depth of field"],["overhead","top-down overhead composition, clean graphic arrangement of objects, even focus"],
 ["top-down","top-down overhead composition, clean graphic arrangement of objects, even focus"],["aerial","high aerial composition, clear geography and scale, deep focus"],
 ["low-angle","low-angle composition looking up, conveying authority and scale"],["tracking","tracking shot following one subject through the space, subject held on a third"],
 ["medium","medium shot, one subject and its immediate surroundings, clean separation from the background"],["wide","wide establishing composition, clear focal subject on a rule-of-thirds line, deep focus"]];
function shotComposition(shot){const t=(shot||"").toLowerCase();const m=SHOT_COMPOSITION.find(([k])=>t.includes(k));return m?m[1]:"clear single focal subject, strong leading lines, rule of thirds";}
const NEG_HEAD=/^\s*(?:and\s+|with\s+|while\s+)?(?:no\b|without\b|never\b|nothing\b|keep(?:ing)?\b|all\s+\w+\s+(?:remain|are|is|stay)|every\s+\w+\s+(?:remains?|is|stays?)|not\s+(?:a\s+)?(?:depict|represent|recreat))/i;
const NEG_TOPIC=/logo|text|letter|label|sign|brand|readab|legib|likeness|identif|face|watermark|seal|flag|emblem|nameplate|placard|marking|caption|portrait|appearance|interface|numbers|figures|dates|recogni|trademark|badge|crest|inscription/i;
function stripNegations(t){const i=t.indexOf("STRICT:");const head=i<0?t:t.slice(0,i),tail=i<0?"":t.slice(i);const out=[];
 for(const sent of head.trim().split(/(?<=[.!?])\s+/)){const body=sent.replace(/[.!? ]+$/,"");const cl=[];let dropping=false;for(const c of body.split(/[,;]\s+/)){if(NEG_HEAD.test(c)&&NEG_TOPIC.test(c)){dropping=true;continue;}if(dropping&&c.split(/\s+/).length<=5&&(NEG_TOPIC.test(c)||/^\s*(or|nor)\b/i.test(c)))continue;dropping=false;cl.push(c);}if(cl.length)out.push(cl.join(", ").trim()+".");}
 return (out.join(" ")+(tail?" "+tail:"")).trim();}
function cleanSubject(vp){let t=(vp||"").trim().replace(/\b(dark\s+)?cinematic\s+16:9\s*/i,"").trim();t=t.replace(/,?\s*no logos?,?\s*(no text,?)?\s*(no identifiable people\.?)?\s*$/i,"").replace(/^[\s,.]+|[\s,.]+$/g,"");t=t.split(" | ")[0];if(t)t=stripNegations(t).replace(/^[\s,.]+|[\s,.]+$/g,"");return t?t[0].toUpperCase()+t.slice(1):"Atmospheric establishing shot that illustrates the narration";}
function sent_(x){return String(x||"").replace(/\s+/g," ").trim().replace(/\.+$/,"")+".";}
function buildGrokPrompt(s){const narr=(s.narration||"").replace(/\s+/g," ").trim();const [mood,look]=ACT_LOOK[s.act]||DEFAULT_LOOK;const p=[`Subject: ${sent_(cleanSubject(s.visual_prompt))}`];
 if(typeof s.beat=="string"&&s.beat.trim())p.push(`Story beat: ${sent_(s.beat)}`);
 if(s.mood)p.push(`Mood: ${sent_(s.mood)}`);else if(narr)p.push(`Mood: ${mood}.`);
 if(s.camera&&s.mode!="video")p.push(`Camera: ${sent_(s.camera)}`);
 p.push(`Composition: ${shotComposition(s.shot)}.`,`${GROK_STYLE} Light and color: ${look}.`);
 if(s.mode=="video"){const w=narr?narr.split(" ").length:0;const d=Math.min(15,Math.max(1,Math.ceil(Math.max(1,w/150*60))));let mv;
  if(s.camera){p.push(`Camera move: one continuous move only: ${sent_(s.camera)}`);mv="One simple, clearly visible subject action that completes within the clip, the rest of the scene stays still, realistic physics, no cuts, no morphing.";}
  else mv="Motion: slow cinematic camera movement (gentle dolly-in or slow parallax pan), one simple subject action, the rest of the scene stays still, smooth and stable, no cuts, no morphing.";
  p.push(`${mv} Duration: about ${d} seconds (max 15s), no audio.`,"Format: video, aspect ratio 16:9, 1920x1080, high resolution, ultra detailed.");}
 else p.push("Format: still image, aspect ratio 16:9, 1920x1080, high resolution, ultra detailed, sharp focus.");
 p.push(GROK_TEXT_GUARD,GROK_NEG);return p.join(" ");}
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

let MONT={},MONTPOLL=null;
const VOICES=["onyx","cedar","ash","echo","ballad","verse","fable","sage","marin","alloy","coral","nova","shimmer"];
const MSTEP={narracao:"Gerando narração",clipes:"Renderizando clipes",audio:"Montando narração",juncao:"Juntando cenas",final:"Codificando final.mp4"};
function fmtDur(s){s=Math.round(s||0);return `${Math.floor(s/60)}:${String(s%60).padStart(2,"0")}`;}
function renderMont(){const el=$("montPanel");if(!el)return;if(!P||!P.id){el.innerHTML='<div class="card empty"><b>Abra um projeto</b></div>';return;}
 const m=MONT,c=m.config||{},run=m.running,cost=((m.audio_seconds||m.chars/15)/60*(c.tts_price_per_min_usd||0.015));
 const st=m.state?`<div class="auto-state ${m.state}"><b>${run?(MSTEP[m.step]||"Rodando"):({done:"Concluído",error:"Erro",stopped:"Parado",interrupted:"Interrompido"}[m.state]||m.state)}</b> · ${esc(m.message||"")}${run?` · ${m.progress||0}%`:""}${m.updated_at?` <span class="muted">(${m.updated_at})</span>`:""}
  ${run?`<div class="progress" style="margin-top:10px"><div style="width:${m.progress||0}%"></div></div>`:""}</div>`:"";
 el.innerHTML=`<div class="mont-grid">
 <div class="card"><h3>1. Narração</h3>
  <div class="mont-stats"><div><span>Cenas com áudio</span><b>${m.audio_done||0}/${m.scenes||0}</b></div><div><span>Caracteres</span><b>${(m.chars||0).toLocaleString("pt-BR")}</b></div><div><span>Custo TTS (est.)</span><b>US$ ${cost.toFixed(2)}</b></div></div>
  <div class="field"><label>Voz</label><select id="mVoice">${VOICES.map(v=>`<option${v==c.voice?" selected":""}>${v}</option>`).join("")}</select></div>
  <div class="field"><label>Modelo TTS</label><input id="mModel" value="${esc(c.tts_model||"gpt-4o-mini-tts")}"></div>
  <div class="field"><label>Instruções de tom</label><textarea id="mInstr" rows="3">${esc(c.instructions||"")}</textarea></div>
  <div class="auto-btns"><button class="btn ghost" ${run?"disabled":""} onclick="montCfg().then(()=>montStart('tts',true))">Regerar narração</button></div></div>
 <div class="card"><h3>2. Montagem</h3>
  <div class="mont-stats"><div><span>Cenas com mídia</span><b>${m.media_done||0}/${m.scenes||0}</b></div><div><span>Duração</span><b>${fmtDur(m.duration_seconds||m.audio_seconds)}</b></div><div><span>Render</span><b>${m.render_seconds?fmtDur(m.render_seconds):"-"}</b></div></div>
  <div class="field"><label>Trilha de fundo (opcional)</label><div class="row-inline"><span class="muted">${m.music?esc(m.music):"Nenhuma — o vídeo sai só com narração"}</span>
   <label class="btn ghost sm upl">${m.music?"Trocar":"Enviar MP3"}<input type="file" accept="audio/*" hidden onchange="montMusic(this.files[0])"></label></div></div>
  <div class="field logo-field"><label>Logo da empresa (opcional)</label>${(()=>{const lg=P.logo||{};return `<div class="row-inline">${lg.has?`<img class="logo-prev" src="/files/${encodeURIComponent(P.id)}/assets/logo.png?v=${Date.now()}" alt="logo">`:`<span class="muted">Nenhum logo</span>`}<label class="btn ghost sm upl">${lg.has?"Trocar PNG":"Enviar PNG"}<input type="file" accept="image/png" hidden onchange="montLogo(this.files[0])"></label></div>
   <label><input type="checkbox" id="mLogo" ${lg.enabled?"checked":""} onchange="logoSet('enabled',this.checked)"> Sobrepor logo (canto sup. esquerdo, ${lg.width_pct||9}% da largura, ${Math.round((lg.opacity||0.85)*100)}% opacidade) na abertura (${lg.intro_seconds||15}s) e em ${P.scenes.filter(s=>s.logo).length} cenas marcadas no Roteiro</label><label><input type="checkbox" ${lg.plate!==false?"checked":""} onchange="logoSet('plate',this.checked)"> Placa clara atrás do logo (arredondada, ~90% opacidade)</label>${lg.source?`<div class="muted sm">Fonte: <a href="${esc(lg.source)}" target="_blank" rel="noopener">${esc(lg.source)}</a> · ${esc(lg.license||"")}</div>`:""}`;})()}</div>
  <div class="field"><label>Motion graphics</label><div class="row-inline"><span class="muted">${P.scenes.filter(s=>(s.gfx||[]).length).length} cenas com gráficos · ${P.scenes.filter(s=>s.source=="gfx").length} telas cheias prontas</span><button class="btn ghost sm" onclick="gfxRender()">Gerar gráficos</button></div></div>
  <div class="field"><label>Trilha (música única, com ducking sob a narração; só a primeira é usada)</label>${(P.music_tracks||[]).length?`<ul class="tracks">${P.music_tracks.map(t=>`<li><b>Cena ${t.from_scene}+</b> · ${esc(t.title||t.file)} <span class="muted">${esc(t.license||"")}</span></li>`).join("")}</ul>`:'<span class="muted">Nenhuma trilha por ato definida</span>'}</div>
  <div class="field"><label><input type="checkbox" id="mBurn" ${c.burn_subtitles?"checked":""}> Queimar legendas no vídeo (padrão: só o arquivo .srt)</label></div>
  <div class="auto-btns">${run?`<button class="btn ghost danger" onclick="montStop()">Parar</button>`:`<button class="btn primary" onclick="montCfg().then(()=>montStart('all'))">Gerar narração e montar</button><button class="btn ghost" onclick="montCfg().then(()=>montStart('render'))">Só remontar vídeo</button>`}</div></div></div>
 ${st}
 ${m.final?`<div class="card mont-out"><h3>Resultado</h3><video controls preload="metadata" src="/files/${encodeURIComponent(P.id)}/output/final.mp4?v=${m.updated_at||""}"></video>
  <div class="auto-btns"><a class="btn primary" href="/files/${encodeURIComponent(P.id)}/output/final.mp4?dl=1">Baixar final.mp4 (${m.final_mb} MB)</a>${m.srt?`<a class="btn ghost" href="/files/${encodeURIComponent(P.id)}/output/final.srt">Baixar legendas .srt</a>`:""}</div></div>`:""}`;}
async function montRefresh(){if(!P||!P.id)return;try{MONT=await (await fetch("/api/montage?id="+encodeURIComponent(P.id))).json();}catch{return;}
 if(!MONT.running&&MONTPOLL){clearInterval(MONTPOLL);MONTPOLL=null;}if(VIEW=="montagem")renderMont();}
function montPoll(){if(!MONTPOLL)MONTPOLL=setInterval(montRefresh,3000);montRefresh();}
async function montCfg(){await api("/api/montage/config",{voice:$("mVoice").value,tts_model:$("mModel").value.trim(),instructions:$("mInstr").value.trim(),burn_subtitles:$("mBurn").checked});}
async function montStart(step,force){try{await api("/api/montage/start",{id:P.id,step,force_tts:!!force});toast("Montagem iniciada.");montPoll();}catch(e){toast(e.message);}}
async function logoSet(k,v){P.logo=Object.assign({file:"assets/logo.png",position:"top-left",width_pct:9,opacity:0.85,intro_seconds:15},P.logo||{});P.logo[k]=v;await save();renderMont();}
async function montLogo(f){if(!f)return;const r=await fetch(`/api/montage/logo?id=${encodeURIComponent(P.id)}&name=${encodeURIComponent(f.name)}`,{method:"POST",body:f});const d=await r.json();if(!r.ok)return toast(d.error,"err");P.logo=Object.assign(P.logo||{},{file:"assets/logo.png",has:true,source:"upload manual",license:""});await save();toast("Logo salvo.");renderMont();}
async function montStop(){await api("/api/montage/stop",{id:P.id});toast("Parando...");}
async function montMusic(f){if(!f)return;const r=await fetch(`/api/montage/music?id=${encodeURIComponent(P.id)}&name=${encodeURIComponent(f.name)}`,{method:"POST",body:f});const d=await r.json();if(!r.ok)return toast(d.error);toast("Trilha salva.");montRefresh();}

function fmtSched(s){if(!s)return "";const m=s.match(/^(\d{4})-(\d\d)-(\d\d)[ T](\d\d:\d\d)/);return m?`${m[3]}/${m[2]} ${m[4]}`:s;}
function renderPub(){const el=$("pubPanel");if(!el||!P)return;const sch=P.status=="agendado"&&P.published_url;const pub=(P.status=="publicado"||sch)&&P.published_url;
 el.innerHTML=`<div class="card pub-card">${P._cover?`<img class="pub-thumb" src="/files/${encodeURIComponent(P.id)}/cover?v=${Date.now()}" alt="">`:""}
 <div class="pub-body"><h3>${sch?`🗓️ Agendado para ${esc(fmtSched(P.scheduled_at))} (BRT)`:pub?"✅ Vídeo publicado":"Publicar no YouTube"}</h3>
 <p class="muted">${sch?"O vídeo fica privado até o horário agendado e vira público automaticamente.":pub?`Publicado em ${esc(P.published_at||"")}`:"Depois de subir o final.mp4 no YouTube Studio, cole aqui o link e marque como publicado. Isso conclui a etapa 5."}</p>
 <div class="field"><label>Link do vídeo publicado</label><input id="pubUrl" placeholder="https://www.youtube.com/watch?v=..." value="${esc(P.published_url||"")}"></div>
 <div class="field"><label>Agendado para (opcional, horário de Brasília)</label><input id="pubSched" type="datetime-local" value="${esc((P.scheduled_at||"").replace(" ","T"))}"></div>
 <div class="auto-btns"><button class="btn primary" onclick="doPublish()">${pub?"Atualizar link":"Marcar como publicado"}</button>${pub?`<button class="btn ghost" onclick="doPublish(true)">Desmarcar</button>`:""}</div>${pub?ytBtns(P):""}</div></div>${pub?`<div id="ytPanel" class="card yt-card"><div class="muted">Carregando estatísticas do YouTube…</div></div>`:""}`;if(pub)ytLoad(false);}
function nf(n){return n==null?"—":Number(n).toLocaleString("pt-BR");}
async function ytLoad(force){const el=$("ytPanel");if(!el)return;let d;try{d=await (await fetch(`/api/ytstats?id=${encodeURIComponent(P.id)}${force?"&force=1":""}`)).json();}catch{d={error:"Falha ao consultar"};}
 const head=`<div class="yt-head"><div><h3>Desempenho no YouTube</h3><p class="muted">${d.yt_title?esc(d.yt_title)+" · ":""}Atualizado ${d.fetched_at?esc(d.fetched_at):"nunca"} · atualiza sozinho 1×/dia</p></div><button class="btn primary" onclick="ytLoad(true)">Atualizar</button></div>`;
 const big=`<div class="yt-stats"><div><span>Visualizações</span><b>${nf(d.views)}</b></div><div><span>Curtidas</span><b>${nf(d.likes)}</b></div><div><span>Comentários</span><b>${nf(d.comments)}</b></div></div>`;
 const h=(d.history||[]).slice(-30),mx=Math.max(1,...h.map(x=>x.views||0));
 const chart=h.length>1?`<div class="yt-chart">${h.map(x=>`<div title="${esc(x.date)}: ${nf(x.views)}" style="height:${Math.max(3,(x.views||0)/mx*100)}%"></div>`).join("")}</div><div class="muted sm">Visualizações por dia (últimos ${h.length})</div>`:"";
 const err=d.error=="no_key"?`<div class="auto-state error"><b>Falta a chave da API do YouTube.</b> Crie uma chave (YouTube Data API v3) e coloque <code>YOUTUBE_API_KEY=...</code> no arquivo <code>.env</code>. Depois clique em Atualizar.</div>`:d.error&&P.status=="agendado"?`<div class="auto-state">Vídeo agendado: fica privado até ${esc(fmtSched(P.scheduled_at))} (BRT). As estatísticas aparecem depois que ele ficar público.</div>`:d.error?`<div class="auto-state error">${esc(d.error)}</div>`:"";
 el.innerHTML=head+err+big+chart;}
async function doPublish(un){try{const sc=$("pubSched")&&$("pubSched").value;const d=await api("/api/publish",{id:P.id,url:$("pubUrl").value,unpublish:!!un,scheduled_at:un?null:(sc||null)});P.status=d.status;P.scheduled_at=d.scheduled_at;P.published_url=d.published_url;P.published_at=d.published_at;P._stages=d._stages;P._cover=d._cover;toast(un?"Desmarcado.":"Marcado como publicado.");renderPub();go(VIEW);}catch(e){toast(e.message,"err");}}

// ---------- etapas do fluxo: Pesquisa / Imagens reais / Prompts Grok / Validação ----------
async function runStage(st,extra){const b=$("stBtn");if(b){b.disabled=true;b.textContent="Rodando…";}
 try{const r=await api("/api/pipeline/"+st,Object.assign({id:P.id},extra||{}));toast("Etapa concluída.");await openProj(P.id,VIEW);return r;}
 catch(e){toast(e.message,"err");await openProj(P.id,VIEW);}finally{if(b)b.disabled=false;}}
const fimg=(rel)=>rel?`/files/${encodeURIComponent(P.id)}/entities/${encodeURIComponent(rel.split("/").pop())}`:"";
function renderStage(k){const el=$("st-"+k);if(!el||!P)return;let h="";
 if(k=="pesquisa"){const D=P.dossier;
  h=`<div class="card"><div class="field"><label>Notas de pesquisa (fatos, datas, valores, pessoas, empresas, órgãos, com URL da fonte)</label><textarea id="resNotes" class="textarea mono" rows="8">${esc(P.research_notes||P.facts||"")}</textarea></div>
  <div class="row"><button class="btn ghost" onclick="api('/api/pipeline/notes',{id:P.id,notes:$('resNotes').value}).then(()=>toast('Notas salvas.'))">Salvar notas</button>
  <button class="btn primary" id="stBtn" onclick="api('/api/pipeline/notes',{id:P.id,notes:$('resNotes').value}).then(()=>runStage('research'))">Gerar dossiê</button>
  ${D?`<button class="btn" onclick="if(confirm('Refazer o roteiro a partir do dossiê? O roteiro atual será substituído.'))runStage('script').then(()=>go('roteiro'))">Gerar roteiro do dossiê</button>`:""}</div></div>`;
  if(D){h+=`<div class="card"><div class="meta"><span class="chip ok">${(D.chapters||[]).length} capítulos</span><span class="chip">${(D.chapters||[]).reduce((a,c)=>a+(c.facts||[]).length,0)} fatos</span><span class="chip ${D.sources_ok==D.sources_checked?"ok":"warn"}">fontes ok ${D.sources_ok}/${D.sources_checked}</span><span class="chip">${(D.people||[]).length} pessoas</span><span class="chip">${(D.companies||[]).length} empresas</span><span class="chip">${(D.agencies||[]).length+(D.courts||[]).length} órgãos/tribunais</span></div></div>`;
   h+=(D.chapters||[]).map((c,i)=>`<div class="card dos-ch"><h3>Capítulo ${i+1} · ${esc(c.title)}</h3><p class="muted">${esc(c.summary||"")}</p><table class="dos">${(c.facts||[]).map(f=>`<tr><td class="d">${esc(f.date||"")}</td><td>${f.allegation?'<span class="chip warn">alegação</span> ':""}${esc(f.text)}${f.amount?` <b class="amt">${esc(f.amount)}</b>`:""}</td><td class="u">${f.url?`<a href="${esc(f.url)}" target="_blank">${f.url_ok===false?"⚠ ":"✓ "}${esc(new URL(f.url).hostname.replace("www.",""))}</a>`:""}</td></tr>`).join("")}</table></div>`).join("");
   const L=(t,a)=>a&&a.length?`<div class="card"><h3>${t}</h3><div class="gfx-chips">${a.map(x=>`<span class="chip">${esc(x.name)}${x.role||x.full_name?` · ${esc(x.full_name||x.role)}`:""}${x.status?` · ${esc(x.status)}`:""}</span>`).join("")}</div></div>`:"";
   h+=`<div class="two-col">${L("Pessoas",D.people)}${L("Empresas",D.companies)}${L("Órgãos",D.agencies)}${L("Tribunais",D.courts)}</div>`;}}
 if(k=="imagens"){const E=P.entities||[];
  h=`<div class="card"><p class="muted">Logos oficiais, selos de órgãos (domínio público), fotos de sedes e pessoas de fontes licenciadas (Wikimedia Commons) com crédito. Entidades sem imagem real recebem cartão com nome.</p><button class="btn primary" id="stBtn" onclick="runStage('images')">Coletar imagens</button>
  <span class="chip ok">${E.filter(e=>e.logo||e.seal||e.photo||e.hq_photo).length}/${E.length} com visual real</span></div><div class="ent-grid">${E.map(e=>{const im=e.logo||e.seal||e.photo;const cr=e.credits||{};
   return `<div class="card ent"><div class="ent-mark">${im?`<img src="${fimg(im)}">`:`<b>${esc(e.name)}</b>`}</div>${e.hq_photo?`<img class="ent-hq" src="${fimg(e.hq_photo)}">`:""}<div class="ent-b"><b>${esc(e.full_name||e.name)}</b><span class="chip">${esc(e.kind)}</span><div class="muted">${esc(e.role||"")}</div>
   ${e.kind=="person"?`<details class="fu"${e.photo_license=="fair_use"?" open":""}><summary><label><input type="checkbox" ${e.photo_license=="fair_use"?"checked":""} onchange="fuSave('${esc(e.name)}',this.checked,this.closest('details'))"> Uso justo (foto de not?cia)</label></summary>
   <input class="input" placeholder="URL da imagem" data-k="image_url" value="${esc(cr.photo_image_url||"")}"><input class="input" placeholder="URL da matéria que nomeia a pessoa" data-k="source_url" value="${esc(cr.photo_source||"")}"><input class="input" placeholder="Veículo / cr?dito (ex.: Bloomberg/Michael Nagle)" data-k="outlet" value="${esc(cr.photo_short||"")}">
   <button class="btn ghost" onclick="fuSave('${esc(e.name)}',true,this.closest('details'))">Salvar</button><div class="muted small">Só dentro do cartão da pessoa, ~4s, moldura polaroid, cr?dito no cart?o e na descri??o.</div></details>`:""}
   <div class="cred">${Object.keys(cr).filter(x=>!x.endsWith("_source")&&x!="photo_short"&&x!="photo_image_url").map(x=>`<a target="_blank" href="${esc(cr[x+"_source"]||"#")}">${esc(x)}: ${esc(cr[x])}</a>`).join("<br>")||(im?"":"Sem imagem licenciada · cartão com nome")}</div></div></div>`}).join("")}</div>`;}
 if(k=="prompts"){const S=P.scenes||[];
  h=`<div class="card"><p class="muted">Prompts do Grok derivados das batidas da história de cada cena (beat, plano, câmera, luz, clima). Cenas com gráfico de tela cheia não usam Grok.</p><button class="btn primary" id="stBtn" onclick="runStage('prompts')">Gerar prompts ricos</button> <span class="chip">${S.filter(s=>s.beat).length}/${S.length} cenas com beat</span></div>
  <div class="card"><table class="dos">${S.map((s,i)=>`<tr><td class="d">#${i+1}<br><span class="chip">${esc(s.shot||"")}</span></td><td><b>${esc(s.beat||"")}</b><div class="muted">${esc(s.narration)}</div><div class="mono small">${esc(s.visual_prompt||"")}</div></td></tr>`).join("")}</table></div>`;}
 if(k=="validacao"){const V=P.validation;
  h=`<div class="card"><p class="muted">Cada nome, sigla e valor citado na narração precisa de um visual na mesma cena (cartão da entidade, logo, selo, foto, callout do valor). Lacunas bloqueiam o render.</p><button class="btn primary" id="stBtn" onclick="runStage('validate')">Validar e corrigir</button></div>`;
  if(V){h+=`<div class="card"><div class="meta"><span class="chip ${V.ok?"ok":"err"}">${V.ok?"APROVADO · render liberado":"BLOQUEADO · "+V.gaps.length+" lacuna(s)"}</span><span class="chip">${V.mentions} menções</span><span class="chip">+${V.entity_cards_added} cartões de entidade</span><span class="chip">+${V.amount_callouts_added} callouts de valor</span>${(V.name_card_only||[]).length?`<span class="chip warn">só cartão com nome: ${esc(V.name_card_only.join(", "))}</span>`:""}${(V.title_check||[]).length?`<span class="chip warn">título: ${esc(V.title_check.join(" · "))}</span>`:""}${(V.gfx_rules||[]).length?`<span class="chip warn" title="${esc(V.gfx_rules.map(x=>"cena "+x.scene).join(", "))}">${V.gfx_rules.length} gráfico(s) com uma barra só</span>`:""}${(V.gfx_hints||[]).length?`<span class="chip" title="${esc(V.gfx_hints.map(x=>"cena "+x.scene+": "+x.gfx+" - "+x.why).join(" | "))}">${V.gfx_hints.length} sugestão(ões) de gráfico</span>`:""}</div></div>`;
   if(V.gaps.length)h+=`<div class="card"><table class="dos">${V.gaps.map(g=>`<tr><td class="d">Cena ${g.scene}</td><td>${g.missing.map(m=>`<span class="chip err">${esc(m)}</span>`).join(" ")}<div class="muted">${esc(g.narration||"")}</div></td></tr>`).join("")}</table></div>`;}}
 el.innerHTML=h;}

async function fuSave(name,on,box){const b={id:P.id,name,enabled:on};box.querySelectorAll("input[data-k]").forEach(i=>b[i.dataset.k]=i.value.trim());
 try{await api("/api/pipeline/fairuse",b);toast(on?"Foto (uso justo) salva.":"Uso justo removido.");await openProj(P.id,"imagens");}catch(e){toast(e.message,"err");}}

function ytId(u){const m=String(u||"").match(/(?:v=|youtu\.be\/|shorts\/|video\/)([\w-]{11})/);return m?m[1]:"";}
const YT_SVG='<svg class="yt-ic" viewBox="0 0 28 20" width="28" height="20" aria-hidden="true"><rect width="28" height="20" rx="5" fill="#fff"/><path d="M11 5.5v9l8-4.5z" fill="#ff0033"/></svg>';
const STUDIO_SVG='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/></svg>';
const EYE_SVG='<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:-2px;margin-right:4px" aria-hidden="true"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8S1 12 1 12z"/><circle cx="12" cy="12" r="3"/></svg>';
function ytBtns(p){if(!p||!p.published_url||!["publicado","agendado"].includes(p.status))return "";const id=ytId(p.published_url);
 return `<div class="yt-btns" onclick="event.stopPropagation()"><a class="yt-watch" href="${esc(p.published_url)}" target="_blank" rel="noopener">${YT_SVG}<span>Assistir no YouTube</span></a>${id?`<a class="yt-studio" href="https://studio.youtube.com/video/${id}/edit" target="_blank" rel="noopener" title="Abrir no YouTube Studio">${STUDIO_SVG}<span class="yt-st-l">YouTube Studio</span></a>`:""}</div>`;}
