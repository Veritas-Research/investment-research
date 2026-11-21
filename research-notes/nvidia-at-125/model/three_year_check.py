"""The 3 year check in Part 5: value = multiple x year 4 earnings per share, discounted 3 years,
plus cash earned in years 1 to 3, plus cash and stakes in other companies minus debt.
Uses the same revenue, margin and tax paths as nvda_model.py. $ millions; shares in millions."""
base=361808; rf=.049; eff=13730/79017; mt=.25; sc=3; coc=.1055; sh=24186
net=53512+109747-32371
def path(g1,g25,tm,h,m1=.63):
    g=[g1]+[g25]*4+[g25-(g25-rf)/5*k for k in range(1,6)]
    rev=[base]
    for x in g: rev.append(rev[-1]*(1+x))
    rev=[rev[0]]+[r*(1-h) for r in rev[1:]]
    out=[]
    for t in range(1,11):
        m=m1 if t==1 else (tm if t>5 else tm-((tm-m1)/5)*(5-t))
        tax=eff if t<=5 else eff+(mt-eff)/5*(t-5)
        nopat=m*rev[t]*(1-tax); reinv=(rev[t+1]-rev[t])/sc if t<10 else 0
        out.append(dict(t=t,rev=rev[t],m=m,eps=nopat/sh,fcf=(nopat-reinv)/sh))
    return out
STORIES={'Gloomy (a fifth of revenue lost, margin falling to 45%)':(.5,.08,.45,.217),
         'Middle (cooling, margin 57%)':(.5,.08,.57,0),
         'Guidance (75% next year, margin 57%)':(.75,.15,.57,0)}
if __name__=='__main__':
    for k,v in STORIES.items():
        p=path(*v); pvcash=sum(p[i]['fcf']/(1+coc)**(i+1) for i in range(3))
        vals=[mult*p[3]['eps']/(1+coc)**3+pvcash+net/sh for mult in (15,20,25)]
        print(f"{k}: EPS year 4 ${p[3]['eps']:.2f}; at 15x/20x/25x: "+' / '.join(f'${x:.0f}' for x in vals))
