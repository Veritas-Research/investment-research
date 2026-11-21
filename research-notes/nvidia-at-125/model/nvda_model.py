"""Rebuild of Damodaran's valuation spreadsheet logic (AnthropicIPO.xlsx 'Valuation output'),
generalised so the same engine values NVIDIA. Verified against his file before use."""
def value(base_rev, g1, g25, m1, target_m, conv=5, sc=3.0, sc2=None, coc0=0.1055, rf=0.049,
          mature_erp=0.0423, eff_tax=0.0, marg_tax=0.25, roic_T=0.15, p_fail=0.0, fail_pct=0.5,
          debt=0.0, cash=0.0, ipo=0.0, cross=0.0, minority=0.0, options=0.0, shares=1.0,
          haircut=0.0):
    sc2 = sc if sc2 is None else sc2
    coc_T = rf + mature_erp
    g=[g1]+[g25]*4+[g25-(g25-rf)/5*k for k in range(1,6)]
    rev=[base_rev]
    for x in g: rev.append(rev[-1]*(1+x))
    rev=[rev[0]]+[r*(1-haircut) for r in rev[1:]]       # permanent revenue loss on every future year
    revT=rev[10]*(1+rf)
    m=[m1 if t==1 else (target_m if t>conv else target_m-((target_m-m1)/conv)*(conv-t)) for t in range(1,11)]
    tax=[eff_tax]*5+[eff_tax+(marg_tax-eff_tax)/5*k for k in range(1,6)]
    coc=[coc0]*5+[coc0-(coc0-coc_T)/5*k for k in range(1,6)]
    df=1;pv=0;rows=[]
    for t in range(10):
        ebit=m[t]*rev[t+1]; nopat=ebit*(1-tax[t]) if ebit>0 else ebit
        nxt=rev[t+2] if t<9 else revT
        s=sc if t<5 else sc2
        reinv=(nxt-rev[t+1])/s
        fcff=nopat-reinv
        df/=(1+coc[t]); pv+=fcff*df
        rows.append((t+1,rev[t+1],m[t],ebit,nopat,reinv,fcff,coc[t],df))
    nopatT=target_m*revT*(1-marg_tax); fcffT=nopatT-(rf/roic_T)*nopatT
    tv=fcffT/(coc_T-rf); pvtv=tv*df
    s=pv+pvtv
    op=s*(1-p_fail)+s*fail_pct*p_fail
    eq=op-debt+cash+ipo+cross-minority-options
    return dict(rev1=rev[1],rev5=rev[5],rev10=rev[10],pv10=pv,pvtv=pvtv,op=op,equity=eq,
                per_share=eq/shares,tv_share=pvtv/s,rows=rows)

if __name__=='__main__':
    # Check 1: reproduce Damodaran's Anthropic file (equity $1,450,478M)
    a=value(35286,1.9,0.42,0.05,0.275,sc=3.0,coc0=0.0974,rf=0.049,eff_tax=0.0,marg_tax=0.25,roic_T=0.15,
            p_fail=0.10,fail_pct=0.5,debt=485319.787,cash=112389,ipo=100000,cross=3929,options=472.3002)
    print('Anthropic check, equity $M:', round(a['equity'],1), '(file: 1,450,478.5)')
