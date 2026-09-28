import numpy as np, time
def board(rows,n=8):
    Y=np.zeros((len(rows),n),int)
    for s,r in enumerate(rows): Y[s,list(r)]=1
    return Y
F=board([{0,1,4,5},{2,3,4,6},{0,2,5,7},{0,1,3,6},{1,2,3,7}])
RL2=board([{0,1,2,3}]*3+[{0,1,4,5}]*2)
def scores(a,b,u,v): return a[:,:,None]+b[:,None,:]+u[:,:,None]*v[:,None,:]
def exact_batch(S,Y):
    m=Y.reshape(-1)==1; Sf=S.reshape(S.shape[0],-1)
    d=Sf[:,m][:,:,None]-Sf[:,~m][:,None,:]
    return ((d>1e-9).sum((1,2))*2+(np.abs(d)<=1e-9).sum((1,2)))/2
def cont(Y,loss,B=2000,steps=1500,seed=0):
    rng=np.random.default_rng(seed); S,T=Y.shape; m=Y.reshape(-1)==1
    P=[rng.normal(size=(B,k)) for k in (S,T,S,T)]
    M=[np.zeros_like(p) for p in P]; V=[np.zeros_like(p) for p in P]
    best=-1;bp=None;lr=0.05
    for i in range(steps):
        a,b,u,v=P; Sc=scores(a,b,u,v)
        if loss=='auc':
            temp=1.0*(0.01)**(i/steps)
            Sf=Sc.reshape(B,-1); d=(Sf[:,m][:,:,None]-Sf[:,~m][:,None,:])/temp
            sg=1/(1+np.exp(-np.clip(d,-50,50))); W=sg*(1-sg)/temp   # d(sigmoid)/d(d) ; maximize -> gradient ascent
            Gf=np.zeros_like(Sf); Gf[:,m]=W.sum(2); Gf[:,~m]=-W.sum(1)
            G=-Gf.reshape(B,S,T)/ (m.sum()*(~m).sum())*1000  # loss gradient
        else:
            G=(1/(1+np.exp(-Sc))-Y)
        gr=[G.sum(2),G.sum(1),(G*v[:,None,:]).sum(2),(G*u[:,:,None]).sum(1)]
        for k in range(4):
            M[k]=0.9*M[k]+0.1*gr[k]; V[k]=0.999*V[k]+0.001*gr[k]**2
            P[k]=P[k]-lr*(M[k]/(1-0.9**(i+1)))/(np.sqrt(V[k]/(1-0.999**(i+1)))+1e-8)
        if i%50==49 or i==steps-1:
            c=exact_batch(scores(*P),Y); k=c.argmax()
            if c[k]>best: best=c[k]; bp=[p[k].copy() for p in P]
    return best,bp
def exact_np(Y,a,b,u,v):
    return exact_batch(scores(a[None],b[None],u[None],v[None]),Y)[0]
def discrete(Y,iters,seed=0,R=3):
    rng=np.random.default_rng(seed); S,T=Y.shape; best=-1;bp=None
    f=lambda p: exact_np(Y,*p)
    for it in range(iters):
        p=[rng.integers(-R,R+1,S).astype(float),rng.integers(-R,R+1,T).astype(float),
           rng.integers(-1,2,S).astype(float),rng.integers(-R,R+1,T).astype(float)]
        cur=f(p); imp=True
        while imp:
            imp=False
            for k in rng.permutation(4):
                lo,hi=(-1,1) if k==2 else (-R,R)
                for j in rng.permutation(len(p[k])):
                    old=p[k][j]; bv=old
                    for val in range(lo,hi+1):
                        p[k][j]=val; c=f(p)
                        if c>cur: cur=c;bv=val;imp=True
                    p[k][j]=bv
        if cur>best: best=cur;bp=[x.copy() for x in p]
    return best,bp
def run(name,Y,di):
    n=Y.sum()*(Y.size-Y.sum())
    print('=====',name); print(Y); print('row sums',Y.sum(1),'col sums',Y.sum(0),'npairs',n,flush=True)
    res=[]
    for loss,ns in (('auc',3),('logit',2)):
        for sd in range(ns):
            t=time.time(); c,p=cont(Y,loss,seed=sd); print(f'{loss} seed{sd} (2000 starts): best {c}/{n}={c/n:.4f} ({time.time()-t:.0f}s)',flush=True); res.append((c,'cont-'+loss,p))
    t=time.time(); c,p=discrete(Y,di); print(f'discrete ({di} restarts, a,b,v in [-3,3], u in {{-1,0,1}}): best {c}/{n}={c/n:.4f} ({time.time()-t:.0f}s)',flush=True); res.append((c,'discrete',p))
    c,mth,p=max(res,key=lambda r:r[0])
    print('BEST',mth,c,c/n,'recheck',exact_np(Y,*p)); print('a,b,u,v=',[np.round(x,3).tolist() for x in p])
run('F',F,600); run('RL2',RL2,200)
