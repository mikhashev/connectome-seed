import numpy as np, time, itertools, json, csv, sys
from survey import *
rng=np.random.default_rng(2026)
STEPS=500
CSVROWS=[]
def pct(x): return dict(min=float(np.min(x)),p5=float(np.percentile(x,5)),median=float(np.median(x)),max=float(np.max(x)))
def stage(shape,boards,tags,S,T,K1=100,K2=500,nlow=10,reps=5,deep_reps=2,deep_steps=1200):
    tag=np.array(tags); nb=len(boards); tt=time.time()
    t0=time.time(); o,n,mem=best_auc(boards,S,T,K=K1,steps=STEPS,seed=11); t1=time.time()-t0
    best=o.copy(); bm=list(mem)
    order=np.argsort(o,kind='stable')[:nlow]
    rr_min=np.full(nb,np.nan); rr_max=np.full(nb,np.nan); dp_min=np.full(nb,np.nan); dp_max=np.full(nb,np.nan)
    R=np.zeros((nlow,reps)); t2=time.time()
    for r in range(reps):
        c,_,m=best_auc([boards[i] for i in order],S,T,K=K2,steps=STEPS,seed=100+r)
        R[:,r]=c
        for j,i in enumerate(order):
            if c[j]>best[i]: best[i]=c[j]; bm[i]=m[j]
    t2=time.time()-t2
    for j,i in enumerate(order): rr_min[i]=R[j].min(); rr_max[i]=R[j].max()
    # deep pass on the lowest nlow after refinement
    order2=np.argsort(best,kind='stable')[:nlow]; D=np.zeros((nlow,deep_reps)); t3=time.time()
    for r in range(deep_reps):
        c,_,m=best_auc([boards[i] for i in order2],S,T,K=K2,steps=deep_steps,seed=200+r)
        D[:,r]=c
        for j,i in enumerate(order2):
            if c[j]>best[i]: best[i]=c[j]; bm[i]=m[j]
    t3=time.time()-t3
    for j,i in enumerate(order2): dp_min[i]=D[j].min(); dp_max[i]=D[j].max()
    # exact rational recheck of every stored member
    t4=time.time(); fin=np.zeros(nb); mism=[]
    for i in range(nb):
        fc=frac_count(boards[i],*bm[i]); fin[i]=fc
        if fc!=best[i]: mism.append((i,float(best[i]),fc))
    t4=time.time()-t4
    json.dump({str(i):dict(rows=show(boards[i]),group=tags[i],count=float(fin[i]),n_pairs=int(n),a=bm[i][0].tolist(),b=bm[i][1].tolist(),u=bm[i][2].tolist(),v=bm[i][3].tolist()) for i in range(nb)},open(f'members_{shape}.json','w',newline='\n'))
    print(f'\n### {shape}: {nb} boards, npairs={n}; stage1 K={K1} steps={STEPS} {t1:.0f}s; refine {nlow} lowest x{reps} seeds K={K2} {t2:.0f}s; deep {nlow} lowest x{deep_reps} seeds K={K2} steps={deep_steps} {t3:.0f}s; Fraction recheck {t4:.0f}s; total {time.time()-tt:.0f}s')
    print('float64/search count vs exact Fraction recount of stored member: mismatches =',mism)
    print('stage1 distribution (K=%d):'%K1,{a:round(b/n,4) for a,b in pct(o).items()})
    print('final distribution:',{a:round(b/n,4) for a,b in pct(fin).items()})
    for g in sorted(set(tags)): print('   group',g,len(fin[tag==g]),{a:round(b/n,4) for a,b in pct(fin[tag==g]).items()})
    print('10 lowest boards (final best count; stage1; refine 5 seeds min-max; deep 2 seeds min-max; rows):')
    for i in np.argsort(fin,kind='stable')[:10]:
        print(f'  board#{i} [{tag[i]}] final={fin[i]:.1f}/{n}={fin[i]/n:.4f} stage1={o[i]:.1f} refine={rr_min[i]}-{rr_max[i]} deep={dp_min[i]}-{dp_max[i]} circulant={is_circulant(boards[i])} rows={show(boards[i])}')
    print('final <0.90:',int((fin<0.9*n).sum()),' <=0.85:',int((fin<=0.85*n).sum()),' min',fin.min(),fin.min()/n)
    thr=2*n/400
    sp=[]
    for i in range(nb):
        v=[x for x in (rr_min[i],rr_max[i],dp_min[i],dp_max[i]) if not np.isnan(x)]
        if v and max(v)-min(v)>thr: sp.append((i,float(max(v)-min(v))))
    print('boards with rerun spread (refine+deep, min..max) > 2/400-equivalent (%.2f counts):'%thr,sp)
    if S==13:
        print('13x13 boards with final <=0.85 (0.85*n=%.1f):'%(0.85*n))
        for i in np.flatnonzero(fin<=0.85*n): print(f'   board#{i} [{tag[i]}] {fin[i]}/{n} circulant={is_circulant(boards[i])}')
        print('   non-circulant among them:',[int(i) for i in np.flatnonzero(fin<=0.85*n) if not is_circulant(boards[i])])
    sys.stdout.flush()
    for i in range(nb):
        allr=[x for x in (rr_min[i],rr_max[i],dp_min[i],dp_max[i]) if not np.isnan(x)]
        CSVROWS.append([shape,i,tags[i],json.dumps(show(boards[i]),separators=(',',':')),fin[i],int(n),min(allr) if allr else '',max(allr) if allr else '',f'members_{shape}.json#{i}'])
    return fin
# ---- 5x8 (board generation order identical to previous run)
boards=[];tags=[]
for _ in range(300): boards.append(rand_board(rng,5,8,4)); tags.append('rand')
H=wh(); rows=[(H[i]==1).astype(int) for i in range(1,8)]
for c in itertools.combinations(range(7),5): boards.append(np.array([rows[i] for i in c])); tags.append('WH')
aff=[r for r in rows]+[1-r for r in rows]
for _ in range(150):
    c=rng.choice(14,5,replace=False); boards.append(np.array([aff[i] for i in c])); tags.append('WH+-')
for _ in range(100): boards.append(flat_board(rng,5,8,4)); tags.append('flat')
stage('5x8',boards,tags,5,8)
def circ(T,k):
    base=np.zeros(T,int); base[rng.choice(T,k,replace=False)]=1
    return np.array([np.roll(base,s) for s in range(T)])
def paley13():
    qr={(x*x)%13 for x in range(1,13)}; base=np.array([1 if i in qr else 0 for i in range(13)])
    return np.array([np.roll(base,s) for s in range(13)])
for (S,T,k,nb) in ((8,8,4,150),(10,10,5,120),(13,13,6,60)):
    bs=[rand_board(rng,S,T,k) for _ in range(nb)]; tg=['rand']*nb
    bs+= [circ(T,k) for _ in range(20)]; tg+=['circ']*20
    bs+= [flat_board(rng,S,T,k) for _ in range(20)]; tg+=['flat']*20
    if S==8:
        for _ in range(30):
            c=rng.choice(14,8,replace=False); bs.append(np.array([aff[i] for i in c])); tg.append('WH+-')
    if S==13: bs.append(paley13()); tg.append('paley')
    stage(f'{S}x{T}',bs,tg,S,T,K2=300 if S==13 else 500)
with open('survey_boards.csv','w',newline='') as f:
    w=csv.writer(f,lineterminator='\n'); w.writerow(['shape','board_id','group','rows_present_cols','best_count','n_pairs','reruns_min','reruns_max','member_json'])
    w.writerows(CSVROWS)
print('done')
