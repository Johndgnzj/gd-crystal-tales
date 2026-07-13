// 水晶戰記 v3 E2E：序章(亞倫跟隨/立繪)→鍵盤教學戰→魔影→回鎮(瑪琳入隊)→選單五頁/配點→委託→頭目→回報
import http from "http"; import fs from "fs"; import path from "path";
import { createRequire } from "module";
const require = createRequire("/Users/john/Projects/60_soho/30_Personal/GameCreator/GDevelop/gdevelop-mcp/package.json");
const puppeteer = require("puppeteer");
const DIR = process.argv[2], OUT = process.argv[3];
const MIME = {".html":"text/html",".js":"text/javascript",".json":"application/json",".png":"image/png",".jpg":"image/jpeg",".tmj":"application/json",".wav":"audio/wav",".mp3":"audio/mpeg"};
const srv = http.createServer((q,r)=>{const u=decodeURIComponent(q.url.split("?")[0]);let fp=path.join(DIR,u==="/"?"index.html":u);if(!fs.existsSync(fp)){r.writeHead(404);r.end();return;}r.writeHead(200,{"Content-Type":MIME[path.extname(fp)]||"application/octet-stream"});fs.createReadStream(fp).pipe(r);});
await new Promise(r=>srv.listen(8804,"127.0.0.1",r));
const br = await puppeteer.launch({headless:true,args:["--mute-audio"]});
const pg = await br.newPage(); await pg.setViewport({width:1280,height:720});
const errs=[]; pg.on("pageerror",e=>errs.push(String(e.message).slice(0,200)));
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const W=()=>pg.evaluate(()=>window.__W||null);
const B=()=>pg.evaluate(()=>window.__B?{state:window.__B.state,enc:window.__B.enc,round:window.__B.round,sel:window.__B.sel,
  foes:window.__B.foes.map(f=>f.name+":"+f.hp+(f.alive?"":"倒")),
  heroes:window.__B.heroes.map(h=>h.name+"Lv"+h.lv+":"+h.hp+" sk"+JSON.stringify(h.sk||{}))}:null);
async function hold(k,ms){await pg.keyboard.down(k);await sleep(ms);await pg.keyboard.up(k);await sleep(90);}
async function spc(){await pg.keyboard.press("Space",{delay:90});await sleep(240);}
async function key(k){await pg.keyboard.press(k,{delay:70});await sleep(200);}
const log={shots:[]};
async function shot(n){const p2=`${OUT}/e_${n}.png`;await pg.screenshot({path:p2});log.shots.push(n);}

// 打完一場戰鬥（全鍵盤：Enter=攻擊→Enter=第一個目標；結算 Enter 繼續）
async function doBattle(maxIter=200){
  for(let i=0;i<maxIter;i++){
    const b=await B();
    if(!b) return "left";
    if(b.state==="win"){await shot("win_"+b.enc);await key("Enter");await sleep(1300);continue;}
    if(b.state==="lose"){await key("Enter");await sleep(1300);return "lose";}
    if(b.state==="menu"){await key("Enter");await sleep(150);
      const b2=await B();
      if(b2&&b2.state==="target"){await key("Enter");}
    }
    await sleep(340);
  }
  return "timeout";
}
async function clearCut(max=14){
  for(let i=0;i<max;i++){
    const w=await W(); if(!w) {await sleep(250); continue;}
    if(w.lock&&!w.menu){await spc();} else break;
  }
}
function dump(){try{console.log(JSON.stringify({errs,log},null,1));}catch(e){}}
process.on("SIGTERM",()=>{dump();process.exit(1);});
try{
await pg.goto("http://127.0.0.1:8804/",{waitUntil:"load"}); await sleep(2800);
await shot("title");
await pg.mouse.click(640,455); await sleep(2200);          // 開始冒險 → Town(序章)
log.townStart=await W();
await spc(); await spc(); await shot("prologue_dlg_face"); // 立繪：瑪琳/路德對話中
await clearCut();
// 序章：亞倫應該排在路德身後跟隨
for(let i=0;i<6;i++)await hold(i%2?"ArrowRight":"ArrowUp",300);
log.prologueFollowers=(await W());
await shot("follower_aaron");
// 往北出口 → Mine
for(let i=0;i<50;i++){
  const w=await W(); if(!w){await sleep(250);continue;}
  if(w.scene==="Mine")break;
  if(w.lock){await spc();continue;}
  if(w.x<640)await hold("ArrowRight",250);
  else if(w.x>736)await hold("ArrowLeft",250);
  else await hold("ArrowUp",470);
}
log.mine=await W(); await shot("mine_lpc_cavemouth");
await clearCut();
// 教學戰（鍵盤操作）
let fought=false;
for(let i=0;i<40&&!fought;i++){
  const b=await B(); if(b){fought=true;break;}
  const w=await W(); if(!w){await sleep(250);continue;}
  if(w.lock){await spc();continue;}
  if(w.y>15*32){await hold("ArrowUp",450);}
  else{ if(!w.inEnc){await hold(i%2?"ArrowLeft":"ArrowUp",380);} else {await hold(i%2?"ArrowLeft":"ArrowRight",420);} }
}
log.tutorialBattle=await B(); await shot("battle_big_heroes");
// 測鍵盤技能路徑：→ 選「技能」→ Enter → Enter(第一招) → Enter(目標)
{ const b=await B();
  if(b&&b.state==="menu"){await key("ArrowRight");await key("Enter");await sleep(200);
    log.skillState=await B(); await shot("battle_skill_kb");
    await key("Enter"); await sleep(200);
    const b3=await B(); if(b3&&b3.state==="target"){await key("Enter");}
  }
}
log.tutorialResult=await doBattle();
await sleep(600); await clearCut();
// 進洞穴（先對齊通道中線 x≈660 再北上）
for(let i=0;i<90;i++){
  const b=await B(); if(b){await doBattle();await sleep(400);continue;}
  const w=await W(); if(!w){await sleep(250);continue;}
  if(w.scene==="Cave")break;
  if(w.lock){await spc();continue;}
  if(w.x<648)await hold("ArrowRight",200);
  else if(w.x>676)await hold("ArrowLeft",200);
  else await hold("ArrowUp",420);
}
log.caveEnter=await W(); await shot("cave_bricks");
await clearCut();
// 魔影劇情戰
for(let i=0;i<90;i++){
  const b=await B();
  if(b&&b.enc==="prologue_demon")break;
  if(b){await doBattle();await sleep(400);continue;}
  const w=await W(); if(!w){await sleep(250);continue;}
  if(w.lock){await spc();continue;}
  if(w.x<544)await hold("ArrowRight",200);
  else if(w.x>592)await hold("ArrowLeft",200);
  else await hold("ArrowUp",420);
}
log.demonBattle=await B(); await shot("demon");
for(let i=0;i<80;i++){
  const b=await B(); if(!b)break;
  if(b.state==="menu"){await key("Enter");await sleep(150);
    const b2=await B(); if(b2&&b2.state==="target"){await key("Enter");}}
  await sleep(340);
}
await sleep(800); await clearCut(); await sleep(1500);
log.afterPrologue=await W();
await spc(); await shot("marin_join_face");                 // 瑪琳入隊過場（立繪）
await clearCut();
log.afterTownCut=await W();

// ===== 選單五頁測試 =====
await key("m"); await sleep(300);
log.menuOpen=await W(); await shot("menu_tab_char");
await key("Enter"); await sleep(250);                       // 進角色詳情（路德）
log.menuMember=await W(); await shot("menu_member_face");
await key("1"); await key("1"); await key("Enter");         // 配2點力量+投1技能點(若有)
log.menuAfterAlloc=await W();
await key("Escape"); await sleep(200);                      // 回列表
await key("ArrowRight"); await sleep(200); await shot("menu_tab_item");   // 道具
await key("Enter"); await sleep(200);                       // 對路德用藥水（滿血會取消音）
await key("ArrowRight"); await sleep(200); await shot("menu_tab_map");    // 地圖
log.menuMap=await W();
await key("ArrowRight"); await sleep(200);                                 // 稱號
await key("ArrowDown"); await key("Enter"); await sleep(200);              // 佩戴 F級冒險者
await shot("menu_tab_title");
log.menuTitle=await W();
await key("ArrowRight"); await sleep(200); await shot("menu_tab_system"); // 系統
await key("Escape"); await sleep(300);
log.menuClosed=await W();

// 瑪琳跟隨確認
for(let i=0;i<6;i++)await hold(i%2?"ArrowDown":"ArrowRight",300);
log.marinFollower=await W(); await shot("follower_marin");

// ===== 公會登錄→委託→頭目 =====
async function goTo(tx,ty,maxIter=70){
  for(let i=0;i<maxIter;i++){
    const w=await W(); if(!w){await sleep(250);continue;}
    if(w.lock&&!w.menu){await spc();continue;}
    const dx=tx-w.x, dy=ty-w.y;
    if(Math.abs(dx)<18&&Math.abs(dy)<18)return true;
    if(Math.abs(dx)>Math.abs(dy)){await hold(dx>0?"ArrowRight":"ArrowLeft",Math.min(450,Math.max(110,Math.abs(dx)*4)));}
    else{await hold(dy>0?"ArrowDown":"ArrowUp",Math.min(450,Math.max(110,Math.abs(dy)*4)));}
  }
  return false;
}
await goTo(245,285); await shot("town_lpc_buildings");
await spc(); await clearCut();                              // 登錄
log.afterReg=await W();
await spc(); await clearCut();                              // 接委託
log.afterQuest=await W();
// 往東之森
await goTo(700,460);
for(let i=0;i<60;i++){
  const w=await W(); if(!w){await sleep(250);continue;}
  if(w.scene==="Forest")break;
  if(w.lock){await spc();continue;}
  if(w.y<430)await hold("ArrowDown",250);
  else if(w.y>530)await hold("ArrowUp",250);
  else await hold("ArrowRight",480);
}
log.forest=await W();
let bossFound=false;
for(let i=0;i<70;i++){
  const b=await B();
  if(b&&b.enc==="ch1_boss"){bossFound=true;break;}
  if(b){await doBattle();await sleep(400);continue;}
  const w=await W(); if(!w){await sleep(250);continue;}
  if(w.lock){await spc();continue;}
  if(w.y<450)await hold("ArrowDown",250);
  else if(w.y>530)await hold("ArrowUp",250);
  else await hold("ArrowRight",480);
}
log.bossBattle=await B(); await shot("boss");
log.bossResult=await doBattle(300);
await sleep(700);
log.afterBoss=await W();
// 升級後：選單→角色→配點與技能點消費驗證
await key("m"); await sleep(300);
await key("Enter"); await sleep(250);
await key("1"); await key("2"); await key("Enter"); await sleep(200);
log.allocAfterBoss=await W(); await shot("menu_alloc_after_levelup");
await key("Escape"); await key("Escape"); await sleep(300);
// 回鎮回報
for(let i=0;i<70;i++){
  const w=await W(); if(!w){await sleep(250);continue;}
  if(w.scene==="Town")break;
  if(w.lock){await spc();continue;}
  const b=await B(); if(b){await doBattle();await sleep(400);continue;}
  if(w.y<450)await hold("ArrowDown",250);
  else if(w.y>530)await hold("ArrowUp",250);
  else await hold("ArrowLeft",480);
}
await goTo(245,285);
await spc(); await clearCut();
log.final=await W(); await shot("final");
}catch(e){log.EXC=String(e&&e.stack||e).slice(0,400);}
dump();
await br.close(); srv.close(); process.exit(0);
