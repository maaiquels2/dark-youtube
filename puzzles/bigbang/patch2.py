s = open("template.html", encoding="utf-8").read()
add = r'''
const IMGSRC=__IMGS__,IM={};for(const k in IMGSRC){const i=new Image();i.src=IMGSRC[k];IM[k]=i}
function layer(k,z,rot,dx,dy,alpha,addm){const im=IM[k];if(!im||!im.complete)return;x.save();if(addm)x.globalCompositeOperation="lighter";x.globalAlpha=x.globalAlpha*alpha;x.translate(540+dx,960+dy);x.rotate(rot);x.scale(z,z);x.drawImage(im,-540,-960,1080,1920);x.restore()}
function embers(cx,cy,t,n,col){add(()=>{for(let i=0;i<n;i++){const a=hash(i)*TAU,sp=.3+hash(i+5)*1.2,ph=(hash(i+9)+t*.18*sp)%1,r=ph*ph*1100+20,len=14+ph*70;ln(cx+Math.cos(a)*(r-len),cy+Math.sin(a)*(r-len),cx+Math.cos(a)*r,cy+Math.sin(a)*r,"rgba(255,"+(170+hash(i+3)*70|0)+",90,"+(.9*(1-ph))+")",1.5+2*(1-ph))}})}
function shock(cx,cy,bt,n){add(()=>{for(let k=0;k<n;k++){const p=clamp((bt-.15-k*.7)/2.4);if(p<=0||p>=1)continue;x.save();x.shadowColor="#ffb060";x.shadowBlur=30;ring(cx,cy,ease(p)*900,"rgba(255,200,130,1)",10*(1-p)+2,.55*(1-p));x.restore()}})}
function flashAt(bt,dur,cx,cy,rgb){if(bt<0||bt>=dur)return;const f=1-bt/dur,g=x.createRadialGradient(cx,cy,0,cx,cy,900);g.addColorStop(0,"rgba(255,255,255,"+f+")");g.addColorStop(1,"rgba("+rgb+","+(f*.5)+")");x.fillStyle=g;x.fillRect(0,0,1080,1920);const c=x.canvas;x.save();x.globalCompositeOperation="screen";x.globalAlpha=.4*f;x.drawImage(c,30*f,0);x.drawImage(c,-30*f,0);x.restore()}
function bangScene(t,bt,fade){x.save();x.globalAlpha=fade;const sh=Math.max(0,1-bt/1.6),dx=Math.sin(bt*63)*20*sh,dy=Math.cos(bt*55)*14*sh,p=ease(bt/6);
 layer("01_bang",1.05+.35*p,p*.035,dx,dy,1,false);layer("01_bang",(1.05+.35*p)*1.09,p*.035,dx,dy,.3+.1*Math.sin(bt*9),true);shock(540,840,bt,4);embers(540,840,bt,160);flashAt(bt,.7,540,840,"255,200,120");x.restore()}
function sceneVoid2(t,bt,u){const ts=wt("expansion",B[0]),fade=1-ease((t-ts+.5)/.9);
 if(fade>0){bangScene(t,bt,fade);const k=ease((t-wt("explosion",B[0])+.2)/.6)*fade;txt("NOT THIS",CX,520,46,"#ff6b5a",null,k);ln(CX-150,520,CX+150,520,"#ff6b5a",5,k)}
 x.save();x.globalAlpha=1-fade;sceneVoid2g(t,bt,u,ts);x.restore()}
function sceneVoid2g(t,bt,u,ts){const a=1+1.1*ease((t-ts)/4.2),g=62*a,R=330,al=1;
 x.save();x.beginPath();x.arc(CX,CY,R,0,TAU);x.clip();
 for(let k=-8;k<=8;k++){ln(CX+k*g,CY-R,CX+k*g,CY+R,"rgba(110,160,255,.38)",2);ln(CX-R,CY+k*g,CX+R,CY+k*g,"rgba(110,160,255,.38)",2)}
 for(let i=-6;i<=6;i++)for(let j=-6;j<=6;j++){if((i*7+j*3)%4)continue;const px=CX+i*g,py=CY+j*g;add(()=>glow(px,py,22,"rgba(255,200,120,A)",.7));dot(px,py,5,"#ffd9a0")}
 x.restore();ring(CX,CY,R,"rgba(160,190,255,.5)",3,al);txt("SPACE ITSELF EXPANDS",CX,1135,40,"#ffb454",null,al)}
function scenePoint2(t,bt,u){const p=ease(u);layer("02_point",1.0+.45*p,0,0,-20*p,1,false);
 const k=ease((u-.1)/.5),r=mix(330,5,k);ring(CX,CY,r,"rgba(150,200,255,.85)",4);ring(CX,CY,r*1.1,"rgba(150,200,255,.3)",2);if(u<.6)txt("one atom",CX,CY+r+44,34,"#9fc4ff",null,1-k);
 add(()=>{for(let i=0;i<110;i++){const ph=(hash(i)+t*.35*(.6+hash(i+4)))%1,rr=(1-ph)*400*(1-.55*k),a=hash(i+11)*TAU+ph*9;dot(CX+Math.cos(a)*rr,CY+Math.sin(a)*rr*.9,1.2+ph*2.4,"#ffd7a8",.2+.6*ph)}});
 for(let i=0;i<4;i++){const rp=((t*.8+i/4)%1);ring(CX,CY,40+rp*260,"rgba(255,200,140,1)",2,.5*(1-rp)*k)}
 txt("13.8 billion years ago",CX,520,38,"#f2efe6",null,ease(u*3));const T=Math.floor(t*14)%7;txt("temperature: "+["∞","∞","∞°","∞","∞","∞°","∞"][T],CX,1060,34,"#ff9d6a",null,k)}
function sceneInfl2(t,bt,u){const p=ease(bt/6),sh=Math.max(0,1-bt/1.4),dx=Math.sin(bt*66)*18*sh,dy=Math.cos(bt*57)*12*sh;
 for(let k=0;k<9;k++){layer("03_inflation",1.0+.4*p+k*.03*(.4+p),p*.05,dx,dy,k===0?1:.09,k>0)}
 add(()=>{for(let i=0;i<120;i++){const a=hash(i)*TAU,sp=.5+hash(i+4),ph=(hash(i+7)+bt*.5*sp)%1,r=ph*ph*1300+30,len=40+ph*220;ln(CX+Math.cos(a)*(r-len),770+Math.sin(a)*(r-len),CX+Math.cos(a)*r,770+Math.sin(a)*r,"rgba("+(150+hash(i+2)*100|0)+",200,255,"+(.8*(1-ph*.6))+")",1.5+3*ph)}glow(CX,770,170+50*Math.sin(bt*7),"rgba(255,255,255,A)",.5)});
 flashAt(bt,.6,CX,770,"150,190,255");
 const ex=36-Math.round(4*ease(u*1.3));txt("t = 10"+sup(-ex)+" s",CX,520,44,"#9fc4ff");txt("× 10"+sup(Math.round(26*ease(u*1.1))),CX,1060,64,"#ffb454");txt("faster than light",CX,1120,30,"#f2efe6",null,ease((u-.3)*3))}
function sceneFusion2(t,bt,u){layer("04_plasma",1.05+.25*ease(u),Math.sin(t*.3)*.02,Math.sin(t*.4)*20,0,.85,false);x.save();x.globalAlpha=.9;sceneFusion(t,bt,u);x.restore()}
function sceneRecomb2(t,bt,u){const tE=wt("electrons",B[4]),tL=wt("light",B[4]),tC=wt("cosmic",B[4]);
 const fog=1-ease((t-tE-.8)/(tL-tE));layer("04_plasma",1.2+.1*ease(u),Math.sin(t*.3)*.02,0,0,.9*fog,false);
 sceneRecombCore(t,bt,u,tE,tL,tC);
 if(t>=tC-.4){const k=ease((t-tC+.4)/1.4);x.save();x.globalAlpha=k;x.fillStyle="#02030a";x.fillRect(0,0,1080,1920);layer("05_cmb",1.5+.3*ease((t-tC)/6),0,0,-40,1,false);x.restore();
  txt("COSMIC MICROWAVE BACKGROUND",CX,1000,32,"#ffb454",null,k);txt("the oldest light there is",CX,1045,26,"#cfd8ff",null,k*.8)}}
function sceneWeb2(t,bt,u){const tS=B[5]+3.8,k=ease((t-tS)/1.2);
 x.save();x.globalAlpha=1-k;layer("06_web",1.05+.35*ease(u),t*.01,Math.sin(t*.5)*20,-30*u,1,false);layer("06_web",1.15+.45*ease(u),t*.012,Math.sin(t*.5)*34,-50*u,.25,true);x.restore();
 if(k>0){x.save();x.globalAlpha=k;layer("07_stars",1.05+.22*ease((t-tS)/6),Math.sin(t*.4)*.012,Math.sin(t*.5)*14,0,1,false);
  add(()=>{for(let i=0;i<14;i++){const a=i*.4488+t*.08,l=700+300*hash(i),g=x.createLinearGradient(CX,780,CX+Math.cos(a)*l,780+Math.sin(a)*l);g.addColorStop(0,"rgba(190,225,255,.22)");g.addColorStop(1,"rgba(190,225,255,0)");x.strokeStyle=g;x.lineWidth=3+8*hash(i+3);x.beginPath();x.moveTo(CX,780);x.lineTo(CX+Math.cos(a)*l,780+Math.sin(a)*l);x.stroke()}
   for(let i=0;i<46;i++){const px=hash(i)*1080,py=hash(i+50)*1700+80,tw=Math.max(0,Math.sin(t*(1.5+hash(i+9)*3)+i*5)),r=6+22*tw*hash(i+2);if(tw<.15)continue;dot(px,py,1.5+2*tw,"#d2e6ff",.25+.6*tw);ln(px-r,py,px+r,py,"#dcebff",1.5,.5*tw);ln(px,py-r,px,py+r,"#dcebff",1.5,.5*tw)}});x.restore()}
 txt(t<tS?"gravity pulls the gas into clumps":"the first stars ignite",CX,520,34,t<tS?"#9fc4ff":"#ffffff")}
function sceneHubble2(t,bt,u){layer("06_web",1.3,t*.008,0,0,.28,false);sceneHubble(t,bt,u)}
'''
s = s.replace("// ---- legendas", add + "\n// ---- legendas", 1)
# recomb: separar o miolo (sem a elipse do CMB)
i0 = s.index("function sceneRecomb(t,bt,u){"); i1 = s.index("const FIL=[]")
rec = s[i0:i1]
core_end = rec.index(" if(t>=tC-.4){")
core = rec[:core_end].replace("function sceneRecomb(t,bt,u){ // 4: nevoa, atomos, luz livre, CMB\n const tE=wt(\"electrons\",B[4]),tL=wt(\"light\",B[4]),tC=wt(\"cosmic\",B[4]);\n", "function sceneRecombCore(t,bt,u,tE,tL,tC){\n")
assert "sceneRecombCore" in core, core[:200]
s = s[:i0] + core + "}\n" + s[i1:]
s = s.replace("const SCENES=[sceneVoid,sceneAtom,sceneInflation,sceneFusion,sceneRecomb,sceneWeb,sceneHubble];", "const SCENES=[sceneVoid2,scenePoint2,sceneInfl2,sceneFusion2,sceneRecomb2,sceneWeb2,sceneHubble2];")
s = s.replace("backdrop(t,b===5||b===4?.35:1);", "backdrop(t,b===5||b===4||b===1||b===2||b===3||b===0?.0:.35);if(b===0&&t>1)backdrop(t,.6);")
open("template2.html", "w", encoding="utf-8").write(s)
print("ok")
