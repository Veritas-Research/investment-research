/* Same math as nvda_model.py (a rebuild of Damodaran's valuation spreadsheet), with NVIDIA's inputs. */
const NV={base:361808,m1:0.63,sc:3.0,coc0:0.1055,rf:0.049,erp:0.0423,eff:13730/79017,mt:0.25,roic:0.15,debt:32371,cash:53512,cross:109747,shares:24186};
function nvValue(g1,g25,tm,hc){
  const P=NV,cocT=P.rf+P.erp,g=[g1,g25,g25,g25,g25];
  for(let k=1;k<=5;k++)g.push(g25-(g25-P.rf)/5*k);
  let rev=[P.base];for(const x of g)rev.push(rev[rev.length-1]*(1+x));
  rev=rev.map((r,i)=>i?r*(1-hc):r);
  const revT=rev[10]*(1+P.rf);let df=1,pv=0;
  for(let t=0;t<10;t++){
    const y=t+1,m=y===1?P.m1:(y>5?tm:tm-((tm-P.m1)/5)*(5-y));
    const tax=y<=5?P.eff:P.eff+(P.mt-P.eff)/5*(y-5);
    const coc=y<=5?P.coc0:P.coc0-(P.coc0-cocT)/5*(y-5);
    const ebit=m*rev[y],nopat=ebit>0?ebit*(1-tax):ebit,nxt=y<10?rev[y+1]:revT;
    const fcff=nopat-(nxt-rev[y])/P.sc;df/=(1+coc);pv+=fcff*df;
  }
  const nT=tm*revT*(1-P.mt),fT=nT-(P.rf/P.roic)*nT,pvtv=fT/(cocT-P.rf)*df;
  return (pv+pvtv-P.debt+P.cash+P.cross)/P.shares;
}
function solve(f,lo,hi,target){
  if((f(lo)-target)*(f(hi)-target)>0)return null;
  for(let i=0;i<80;i++){const m=(lo+hi)/2;if((f(lo)-target)*(f(m)-target)<=0)hi=m;else lo=m}
  return (lo+hi)/2;
}
if(typeof module!=="undefined")module.exports={nvValue,solve};
