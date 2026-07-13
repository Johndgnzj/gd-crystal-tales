// 水晶戰記 v2 全流程 E2E：序章→劇情戰→回鎮→登錄→委託→森林頭目→回報
import http from "http"; import fs from "fs"; import path from "path";
import { createRequire } from "module";
import { fileURLToPath } from "url";
const _gdroot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../..");  // GDevelop 工作區根（可攜）
const require = createRequire(path.join(_gdroot, "gdevelop-mcp/package.json"));
const puppeteer = require("puppeteer");
const DIR = process.argv[2], OUT = process.argv[3];
const MIME = {".html":"text/html",".js":"text/javascript",".json":"application/json",".png":"image/png",".jpg":"image/jpeg",".tmj":"application/json",".wav":"audio/wav"};
const srv = http.createServer((q,r)=>{const u=decodeURIComponent(q.url.split("?")[0]);let fp=path.join(DIR,u==="/"?"index.html":u);if(!fs.existsSync(fp)){r.writeHead(404);r.end();return;}r.writeHead(200,{"Content-Type":MIME[path.extname(fp)]||"application/octet-stream"});fs.createReadStream(fp).pipe(r);});
await new Promise(r=>srv.listen(8803,"127.0.0.1",r));
const br = await puppeteer.launch({headless:true,args:["--mute-audio"]});
const pg = await br.newPage(); await pg.setViewport({width:1280,height:720});
const errs=[]; pg.on("pageerror",e=>errs.push(String(e.message).slice(0,200)));
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const W=()=>pg.evaluate(()=>window.__W||null);
const B=()=>pg.evaluate(()=>window.__B?{state:window.__B.state,enc:window.__B.enc,round:window.__B.round,
  foes:window.__B.foes.map(f=>f.name+":"+f.hp+(f.alive?"":"倒")),
  heroes:window.__B.heroes.map(h=>h.name+"Lv"+h.lv+":"+h.hp)}:null);
async function hold(k,ms){await pg.keyboard.down(k);await sleep(ms);await pg.keyboard.up(k);await sleep(90);}
async function spc(){await pg.keyboard.press("Space",{delay:90});await sleep(240);}
const log={shots:[]};
async function shot(n){const p2=`${OUT}/e_${n}.png`;await pg.screenshot({path:p2});log.shots.push(n);}

// 通用：打完一場戰鬥（策略：從最後一個活敵打起；處理升級加點與繼續）
async function doBattle(maxIter=200){
  const FOE=[[300,250],[470,340],[260,430],[440,190]];
  for(let i=0;i<maxIter;i++){
    const b=await B();
    if(!b) return "left";            // 已離開戰鬥場景
    if(b.state==="alloc"){await pg.mouse.click(450,496);await sleep(220);continue;}
    if(b.state==="win"){await shot("win_"+b.enc);await pg.mouse.click(640,642);await sleep(1300);continue;}
    if(b.state==="lose"){await pg.mouse.click(640,642);await sleep(1300);return "lose";}
    if(b.state==="menu"){
      await pg.mouse.click(120,610);await sleep(230);   // 攻擊
      const b2=await B();
      if(b2&&b2.state==="target"){
        let idx=-1;
        for(let j=b2.foes.length-1;j>=0;j--){if(!b2.foes[j].includes("倒")){idx=j;break;}}
        if(idx>=0){const pos=(b2.foes.length===1)?[360,330]:FOE[idx];await pg.mouse.click(pos[0],pos[1]);}
      }
    }
    await sleep(340);
  }
  return "timeout";
}
// 通用：把劇情/對話全部按掉
async function clearCut(max=14){
  for(let i=0;i<max;i++){
    const w=await W(); if(!w) {await sleep(250); continue;}
    if(w.lock){await spc();} else break;
  }
}

function dump(){try{console.log(JSON.stringify({errs,log},null,1));}catch(e){}}
process.on("SIGTERM",()=>{dump();process.exit(1);});
process.on("SIGINT",()=>{dump();process.exit(1);});
try{
await pg.goto("http://127.0.0.1:8803/",{waitUntil:"load"}); await sleep(2800);
await shot("title");
await pg.mouse.click(640,455); await sleep(2000);          // 開始冒險 → Mine
log.mineStart=await W(); await shot("prologue_mine");
await clearCut();                                          // 序章開場對白

// --- 教學戰：往北走，途中拐進碎石地 ---
let fought=false;
for(let i=0;i<40&&!fought;i++){
  const b=await B(); if(b){fought=true;break;}
  const w=await W(); if(!w){await sleep(250);continue;}
  if(w.lock){await spc();continue;}
  if(w.y>15*32){await hold("ArrowUp",450);}
  else{ if(!w.inEnc){await hold(i%2?"ArrowLeft":"ArrowUp",380);} else {await hold(i%2?"ArrowLeft":"ArrowRight",420);} }
}
log.tutorialBattle=await B(); await shot("tutorial_battle");
log.tutorialResult=await doBattle();
await sleep(600); await clearCut();

// --- 走到礦坑口 → Cave ---
for(let i=0;i<50;i++){
  const w=await W(); if(!w){await sleep(250);continue;}
  if(w.scene==="Cave")break;
  if(w.lock){await spc();continue;}
  const b=await B(); if(b){await doBattle();await sleep(400);continue;}
  // 先回到通道(feet 要在 672-735 → x 636-700)再往北
  if(w.x<636)await hold("ArrowRight",280);
  else if(w.x>700)await hold("ArrowLeft",280);
  else await hold("ArrowUp",480);
}
log.caveEnter=await W(); await shot("cave");
await clearCut();

// --- 深入洞穴 → 魔影劇情戰 ---
for(let i=0;i<50;i++){
  const b=await B();
  if(b&&b.enc==="prologue_demon")break;
  const w=await W(); if(!w){await sleep(250);continue;}
  if(w.lock){await spc();continue;}
  if(b){await doBattle();await sleep(400);continue;}
  if(w.x<516)await hold("ArrowRight",280);
  else if(w.x>604)await hold("ArrowLeft",280);
  else await hold("ArrowUp",470);
}
log.demonBattle=await B(); await shot("demon_battle");
// 劇情戰：攻擊直到自動結束
for(let i=0;i<80;i++){
  const b=await B(); if(!b)break;
  if(b.state==="menu"){await pg.mouse.click(120,610);await sleep(230);
    const b2=await B(); if(b2&&b2.state==="target"){await pg.mouse.click(360,330);}}
  await sleep(340);
}
await sleep(800); await clearCut();                        // demon_post 對白＋轉場
await sleep(1500);
log.afterPrologue=await W(); await shot("town_arrive");
await clearCut();                                          // town_start 瑪琳入隊
log.afterTownCut=await W();

// --- 去公會找緹娜（登錄+接委託）---
async function goTo(tx,ty,maxIter=60){
  for(let i=0;i<maxIter;i++){
    const w=await W(); if(!w){await sleep(250);continue;}
    if(w.lock){await spc();continue;}
    const dx=tx-w.x, dy=ty-w.y;
    if(Math.abs(dx)<26&&Math.abs(dy)<26)return true;
    if(Math.abs(dx)>Math.abs(dy)){await hold(dx>0?"ArrowRight":"ArrowLeft",Math.min(500,Math.abs(dx)*4));}
    else{await hold(dy>0?"ArrowDown":"ArrowUp",Math.min(500,Math.abs(dy)*4));}
  }
  return false;
}
await goTo(268,300);                                        // 緹娜旁
await spc(); await clearCut();                              // 登錄
log.afterReg=await W(); await shot("registered");
await spc(); await clearCut();                              // 接委託
log.afterQuest=await W();

// --- 往東之森 ---
await goTo(700,460);                                        // 走回大路
for(let i=0;i<60;i++){
  const w=await W(); if(!w){await sleep(250);continue;}
  if(w.scene==="Forest")break;
  if(w.lock){await spc();continue;}
  if(w.y<430)await hold("ArrowDown",250);
  else if(w.y>530)await hold("ArrowUp",250);
  else await hold("ArrowRight",480);
}
log.forest=await W(); await shot("forest");

// --- 沿路向東找頭目 ---
let bossFought=false;
for(let i=0;i<70;i++){
  const b=await B();
  if(b&&b.enc==="ch1_boss"){bossFought=true;break;}
  if(b){await doBattle();await sleep(400);continue;}
  const w=await W(); if(!w){await sleep(250);continue;}
  if(w.lock){await spc();continue;}
  if(w.y<450)await hold("ArrowDown",250);
  else if(w.y>530)await hold("ArrowUp",250);
  else await hold("ArrowRight",480);
}
log.bossBattle=await B(); await shot("boss_battle");
log.bossResult=await doBattle(300);
await sleep(700);
log.afterBoss=await W(); await shot("after_boss");

// --- 回鎮回報 ---
for(let i=0;i<70;i++){
  const w=await W(); if(!w){await sleep(250);continue;}
  if(w.scene==="Town")break;
  if(w.lock){await spc();continue;}
  const b=await B(); if(b){await doBattle();await sleep(400);continue;}
  if(w.y<450)await hold("ArrowDown",250);
  else if(w.y>530)await hold("ArrowUp",250);
  else await hold("ArrowLeft",480);
}
await goTo(268,300);
await spc(); await clearCut();                              // 回報領賞
log.final=await W(); await shot("final");
}catch(e){log.EXC=String(e&&e.stack||e).slice(0,400);}
dump();
await br.close(); srv.close(); process.exit(0);
