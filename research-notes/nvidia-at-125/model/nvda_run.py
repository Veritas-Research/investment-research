import json
from nvda_model import value
NV=dict(base_rev=361808, m1=0.63, sc=3.0, coc0=0.1055, rf=0.049, mature_erp=0.0423,
        eff_tax=13730/79017, marg_tax=0.25, roic_T=0.15, debt=32371, cash=53512, cross=109747, shares=24186)
PRICE=125.53
STORIES={'A: guidance, then fade':dict(g1=0.75,g25=0.15),
         'B: cooling':dict(g1=0.50,g25=0.08)}
MARG={'45%':0.45,'57%':0.57,'64%':0.64}
BUF={'none':0.0,'low 5.1%':0.051,'mid 11.9%':0.119,'high 21.7%':0.217}
out={}
for sn,sv in STORIES.items():
    for mk,mv in MARG.items():
        for bk,bv in BUF.items():
            r=value(**NV,**sv,target_m=mv,haircut=bv)
            out[f'{sn}|{mk}|{bk}']=dict(ps=r['per_share'],rev10=r['rev10'],rev1=r['rev1'],tvs=r['tv_share'],eq=r['equity'])
for sn in STORIES:
    print('\n',sn)
    print('buffer       ', '  '.join(f'{m:>8}' for m in MARG))
    for bk in BUF:
        print(f'{bk:12}', '  '.join(f"${out[f'{sn}|{m}|{bk}']['ps']:7.0f}" for m in MARG))
    r=out[f'{sn}|57%|none']; print(f"  yr1 rev {r['rev1']/1e3:.0f}B, 2036 rev {r['rev10']/1e3:.0f}B, after-2036 share {r['tvs']:.0%}, equity {r['eq']/1e6:.2f}T")
# reverse DCF: solve years 2-5 growth so value = price, g1 at guidance 0.75 and at 0.50
def solve(g1,tm):
    lo,hi=-0.3,0.6
    for _ in range(80):
        mid=(lo+hi)/2
        if value(**NV,g1=g1,g25=mid,target_m=tm)['per_share']<PRICE: lo=mid
        else: hi=mid
    r=value(**NV,g1=g1,g25=hi,target_m=tm); return hi,r['rev10'],r['rev5']
print('\nReverse DCF at $%.2f'%PRICE)
rev={}
for g1 in (0.75,0.50):
    for mk,mv in MARG.items():
        g,r10,r5=solve(g1,mv); rev[f'{g1}|{mk}']=(g,r10,r5)
        print(f' yr1 growth {g1:.0%}, margin {mk}: yrs2-5 growth {g:+.1%}, 2036 revenue {r10/1e3:.0f}B, yr5 {r5/1e3:.0f}B')
# sensitivities on story B mid margin
base=value(**NV,**STORIES['B: cooling'],target_m=0.57)['per_share']
sens={'cost of capital 9.5%':dict(coc0=0.095),'cost of capital 11.5%':dict(coc0=0.115),
      'riskfree 5.15%':dict(rf=0.0515),'sales to capital 2':dict(sc=2.0),'sales to capital 4':dict(sc=4.0),
      'return after yr10 20%':dict(roic_T=0.20),'commitments as debt (+$102B)':dict(debt=32371+102000),
      'guarantee loss $26B + slow pay $5.1B':dict(debt=32371+26000+5100)}
print('\nSensitivities (story B, 57 pct margin, no buffer): base $'+format(base,'.0f'))
S={}
for k,v in sens.items():
    p=dict(NV);p.update(v); x=value(**p,**STORIES['B: cooling'],target_m=0.57)['per_share']; S[k]=x
    print(f' {k:38} ${x:6.0f} ({x/base-1:+.1%})')
json.dump(dict(grid=out,reverse={k:list(v) for k,v in rev.items()},sens=S,base=base),open('nvda_results.json','w'),indent=1)
