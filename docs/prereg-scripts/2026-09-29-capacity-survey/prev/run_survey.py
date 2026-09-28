import numpy as np, time, itertools, json
from survey import *
rng=np.random.default_rng(2026)
STEPS=500
def pct(x): return dict(min=float(np.min(x)),p5=float(np.percentile(x,5)),median=float(np.median(x)),max=float(np.max(x)))
def stage(name,boards,S,T,k,K1=100,K2=500,nlow=8,reps=5):
    t0=time.time()
    o,n=best_auc(boards,S,T,K=K1,steps=STEPS,seed=11)
    t1=time.time()-t0
    order=np.argsort(o)[:nlow]
    # refine lowest with K2 starts, reps seeds
    R=np.zeros((nlow,reps)); t2=time.time()
    for r in range(reps):
        R[:,r],_=best_auc([boards[i] for i in order],S,T,K=K2,steps=STEPS,seed=100+r)
    t2=time.time()-t2
    final=o.copy()
    for j,i in enumerate(order): final[i]=max(o[i],R[j].max())
    print(f'\n### {name}: {len(boards)} boards, npairs={n}; stage1 K={K1} {t1:.0f}s; refine {nlow} lowest x{reps} seeds K={K2} {t2:.0f}s')
    print('distribution of best-found (stage1 K=%d):'%K1,{a:round(b/n,4) for a,b in pct(o).items()})
    print('distribution after refinement of lowest:',{a:round(b/n,4) for a,b in pct(final).items()})
    print('lowest boards (refined best count, per-seed counts, spread):')
    for j,i in enumerate(order[:5]):
        print(f'  board#{i} stage1={o[i]:.1f} refined best={final[i]:.1f}/{n} = {final[i]/n:.4f}; seeds={R[j].tolist()} spread={R[j].max()-R[j].min():.1f}; rows={show(boards[i])}')
    unstable=[(int(i),float(R[j].max()-R[j].min())) for j,i in enumerate(order) if R[j].max()-R[j].min()>2]
    print('boards among lowest with rerun spread >2/400-equivalent (2 counts on 400 scale = %.1f counts here): %s'%(2*n/400,[(i,s) for i,s in unstable if s>2*n/400]))
    print('any final <0.90:',int((final<0.9*n).sum()),' <=0.85:',int((final<=0.85*n).sum()),' min',final.min()/n,flush=True)
    return final,n
# ---- 5x8
boards=[];tags=[]
for _ in range(300): boards.append(rand_board(rng,5,8,4)); tags.append('rand')
H=wh(); rows=[(H[i]==1).astype(int) for i in range(1,8)]
for c in itertools.combinations(range(7),5): boards.append(np.array([rows[i] for i in c])); tags.append('WH')
aff=[r for r in rows]+[1-r for r in rows]
for _ in range(150):
    c=rng.choice(14,5,replace=False); boards.append(np.array([aff[i] for i in c])); tags.append('WH+-')
for _ in range(100): boards.append(flat_board(rng,5,8,4)); tags.append('flat')
final,n=stage('5x8, 4 per row',boards,5,8,4,K1=100,nlow=10)
tags=np.array(tags)
for tg in ('rand','WH','WH+-','flat'):
    print(' ',tg,{a:round(b/n,4) for a,b in pct(final[tags==tg]).items()})
# ---- larger
def circ(T,k): 
    base=np.zeros(T,int); base[rng.choice(T,k,replace=False)]=1
    return np.array([np.roll(base,s) for s in range(T)])
def paley13():
    qr={(x*x)%13 for x in range(1,13)}; base=np.array([1 if i in qr else 0 for i in range(13)])
    return np.array([np.roll(base,s) for s in range(13)])
for (S,T,k,nb) in ((8,8,4,150),(10,10,5,120),(13,13,6,60)):
    bs=[rand_board(rng,S,T,k) for _ in range(nb)]
    bs+= [circ(T,k) for _ in range(20)]
    bs+= [flat_board(rng,S,T,k) for _ in range(20)]
    if S==8:
        aff=[r for r in rows]+[1-r for r in rows]
        for _ in range(30):
            c=rng.choice(14,8,replace=False); bs.append(np.array([aff[i] for i in c]))
    if S==13: bs.append(paley13())
    stage(f'{S}x{T}, {k} per row',bs,S,T,k,K1=100,K2=300 if S==13 else 500,nlow=6)
