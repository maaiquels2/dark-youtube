const S=[["ideia","Ideia"],["roteiro","Roteiro"],["cenas","Cenas"],["montagem","Montagem"],["publicacao","Publicação"]];
let P={scenes:[]};const $=id=>document.getElementById(id);
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function go(k){S.forEach(([s])=>{$("s-"+s).classList.toggle("on",s==k)});[...$("nav").children].forEach((b,i)=>b.classList.toggle("on",S[i][0]==k));if(k=="cenas")renderCenas();}
$("nav").innerHTML=S.map(([k,n],i)=>`<button onclick="go('${k}')">${i+1}. ${n}</button>`).join("");
function msg(t,cls="err"){$("msg").innerHTML=t?`<div class="${cls}">${esc(t)}</div>`:"";}
async function api(path,body){msg("Aguarde, falando com o ChatGPT...","warn");
 const r=await fetch(path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
 const d=await r.json();if(!r.ok){msg(d.error||"Erro");throw d;}msg("");return d;}
function form(){return{niche:$("niche").value,language:$("language").value,theme:$("theme").value,minutes:+$("minutes").value};}
async function titles(){const d=await api("/api/titles",form());
 $("titles").innerHTML=(d.titles||[]).map((t,i)=>`<div class="card"><b>${esc(t.title)}</b><br><span class="muted">${esc(t.hook)}</span><br><button class="btn" onclick="pick(${i})">Usar este</button></div>`).join("");window._t=d.titles;}
function pick(i){$("title").value=window._t[i].title;go("roteiro");}
async function script(){const d=await api("/api/script",{...form(),title:$("title").value});
 P={...P,...form(),title:d.title||$("title").value,description:d.description,scenes:d.scenes||[]};renderScenes();}
function renderScenes(){const w=P.scenes.reduce((a,s)=>a+(s.narration||"").split(/\s+/).length,0);
 $("stats").textContent=` ${P.scenes.length} cenas · ~${w} palavras · ~${(w/145).toFixed(1)} min`;
 $("scenes").innerHTML=P.scenes.map((s,i)=>`<div class="card"><b>Cena ${i+1}</b><label>Narração</label><textarea rows="3" oninput="P.scenes[${i}].narration=this.value">${esc(s.narration)}</textarea><label>Prompt visual (Grok Imagine)</label><textarea rows="2" oninput="P.scenes[${i}].visual_prompt=this.value">${esc(s.visual_prompt)}</textarea></div>`).join("");}
function renderCenas(){$("cenas").innerHTML=P.scenes.length?P.scenes.map((s,i)=>`<div class="card"><b>Cena ${i+1}</b> <span class="muted">[clipe: pendente]</span><br>${esc(s.visual_prompt)}</div>`).join(""):"<p class='muted'>Gere ou abra um roteiro primeiro.</p>";}
async function save(){P.title=$("title").value||P.title;const d=await api("/api/save",P);P=d;msg("Projeto salvo: "+d.id,"warn");loadProjects();}
async function open_(id){P=await (await fetch("/api/projects/"+id)).json();["niche","language","theme","minutes","title"].forEach(k=>{if(P[k]!=null)$(k).value=P[k]});renderScenes();go("roteiro");}
async function loadProjects(){const l=await (await fetch("/api/projects")).json();
 $("projects").innerHTML=l.length?l.map(p=>`<div class="card" style="cursor:pointer" onclick="open_('${esc(p.id)}')">${esc(p.title)} <span class="muted">(${esc(p.language)} · ${esc(p.updated_at)})</span></div>`).join(""):"<p class='muted'>Nenhum projeto ainda.</p>";}
(async()=>{const s=await (await fetch("/api/status")).json();
 if(!s.has_key)$("keymsg").innerHTML=`<div class="err"><b>Chave da OpenAI não configurada.</b> Copie <code>.env.example</code> para <code>.env</code>, coloque sua OPENAI_API_KEY e reinicie o app. Sem ela, Ideia e Roteiro não funcionam.</div>`;
 go("ideia");loadProjects();})();
