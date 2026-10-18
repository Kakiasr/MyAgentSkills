import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url));
const args=process.argv.slice(2);
if(args.length && (args.length!==2 || args[0]!=='--output-dir'))throw Error('Usage: node validate-five-step-chests.mjs [--output-dir <directory>]');
const output=resolve(args[1]||'artifacts/five-step-model');
mkdirSync(output,{recursive:true});
// Paper/reference model only. This does not implement the game's UI or engine.
const boxes={wood:{cost:1,reward:4},iron:{cost:2,reward:9},gold:{cost:3,reward:12}};
const start=(runId='run-1')=>({runId,phase:'playing',keys:1,coins:0,left:5,opened:[],accepted:[]});
function act(previous,action,requestId,runId=previous.runId){
 const s=structuredClone(previous);
 if(runId!==s.runId||s.accepted.includes(requestId)||s.phase!=='playing'||s.left<=0)return s;
 if(action==='supply')s.keys+=1;
 else{
  const box=boxes[action];
  if(!box||s.opened.includes(action)||s.keys<box.cost)return s;
  s.keys-=box.cost;s.coins+=box.reward;s.opened.push(action);
 }
 s.left-=1;s.accepted.push(requestId);
 if(s.coins>=13)s.phase='won';else if(s.left===0)s.phase='lost';
 return s;
}
const values=s=>[s.keys,s.coins,s.left,s.phase];
const play=actions=>actions.reduce((s,a,i)=>act(s,a,'op-'+i),start());
let tests=0;
function check(actual,expected){assert.deepEqual(actual,expected);tests++;}
check(values(start()),[1,0,5,'playing']);
check(values(play(['supply'])),[2,0,4,'playing']);
check(values(play(['wood'])),[0,4,4,'playing']);
check(play(['iron']),start());
check(values(play(['wood','wood'])),[0,4,4,'playing']);
let supplied=act(start(),'supply','same');
check(act(supplied,'supply','same'),supplied);
check(values(play(['supply','supply'])),[3,0,3,'playing']);
check(values(play(['supply','iron','supply','wood'])),[0,13,1,'won']);
check(values(play(['supply','supply','gold','supply','wood'])),[0,16,0,'won']);
check(values(play(Array(5).fill('supply'))),[6,0,0,'lost']);
let won=play(['supply','iron','supply','wood']);
check(act(won,'supply','later'),won);
check(act(start('new'),'supply','stale','old'),start('new'));
check(act(start(),'missing','invalid'),start());
let terminalPaths=0,wins=0,losses=0,minWin=Infinity,maxWin=0;const finalCoins=new Set();
function explore(s,path=[]){
 assert(s.keys>=0&&s.keys<=6&&s.coins>=0&&s.coins<=25&&s.left>=0&&s.left<=5);
 assert(new Set(s.opened).size===s.opened.length);
 assert(s.accepted.length===5-s.left);
 if(s.phase!=='playing'){
  terminalPaths++;
  if(s.phase==='won'){wins++;minWin=Math.min(minWin,path.length);maxWin=Math.max(maxWin,path.length);finalCoins.add(s.coins);}
  else losses++;
  return;
 }
 for(const action of ['supply',...Object.keys(boxes).filter(id=>!s.opened.includes(id)&&s.keys>=boxes[id].cost)])
  explore(act(s,action,'path-'+path.join('-')+'-'+action),[...path,action]);
}
explore(start());assert(wins>0&&losses>0);check(minWin,4);check(maxWin,5);check([...finalCoins].sort((a,b)=>a-b),[13,16]);
const text=readFileSync(`${base}/five-step-chests.md`,'utf8');
let columns=null;const tableErrors=[];
text.split('\n').forEach((line,i)=>{if(!line.startsWith('|')){columns=null;return;}const n=line.split('|').length;if(columns!==null&&n!==columns)tableErrors.push(i+1);columns=n;});
check(tableErrors,[]);
const report={model:'paper reference model, not engine/UI implementation',pass:true,asserted_examples:tests,terminal_legal_action_paths:terminalPaths,winning_paths:wins,losing_paths:losses,minimum_winning_actions:minWin,maximum_winning_actions:maxWin,winning_final_coin_totals:[...finalCoins].sort((a,b)=>a-b),markdown_table_errors:tableErrors,engine_tests_executed:false,player_tests_executed:false};
writeFileSync(`${output}/five-step-chests-validation.json`,JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
