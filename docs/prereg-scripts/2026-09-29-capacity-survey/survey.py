import numpy as np, time, itertools, sys
from fractions import Fraction
sys.stdout.reconfigure(newline=chr(10))
F32=np.float32
def prep(boards):
    Y=np.asarray(boards).reshape(len(boards),-1)
    Pi=np.stack([np.flatnonzero(y==1) for y in Y]); Ni=np.stack([np.flatnonzero(y==0) for y in Y])
    return Pi,Ni
def best_auc(boards,S,T,K=500,steps=800,seed=0,chunk_pairs=3.0e8):
    """Search dynamics in float32 (identical to previous run); every 100 steps the exact count is taken
    in float64 from the float64-cast params: wins d>0, ties d==0, no tolerance.
    returns best count per board, n_pairs, best member per board (float64 a,b,u,v)."""
    boards=np.asarray(boards); nb=len(boards); Pi,Ni=prep(boards)
    npr,nn=Pi.shape[1],Ni.shape[1]; npairs=npr*nn
    per_board=max(1,int(chunk_pairs/(K*npairs*4*3)))
    out=np.zeros(nb); mem=[None]*nb; rng=np.random.default_rng(seed)
    for c0 in range(0,nb,per_board):
        idx=np.arange(c0,min(nb,c0+per_board)); B=len(idx)*K
        bo=np.repeat(np.arange(len(idx)),K); P_=Pi[idx][bo]; N_=Ni[idx][bo]
        P=[rng.normal(size=(B,k)).astype(F32) for k in (S,T,S,T)]
        M=[np.zeros_like(p) for p in P]; V=[np.zeros_like(p) for p in P]
        lr=F32(0.05)
        bestc=np.full(len(idx),-1.0); bestm=[None]*len(idx)
        def sc(P,dt=None):
            a,b,u,v=P
            if dt: a,b,u,v=[x.astype(dt) for x in P]
            return (a[:,:,None]+b[:,None,:]+u[:,:,None]*v[:,None,:]).reshape(B,-1)
        for i in range(steps):
            a,b,u,v=P; Sf=sc(P)
            Sp=np.take_along_axis(Sf,P_,1); Sn=np.take_along_axis(Sf,N_,1)
            temp=F32(0.01**(i/steps))
            d=(Sp[:,:,None]-Sn[:,None,:])/temp
            sg=1/(1+np.exp(-np.clip(d,-30,30))); W=sg*(1-sg)/temp
            Gf=np.zeros_like(Sf)
            np.put_along_axis(Gf,P_,-W.sum(2),1); np.put_along_axis(Gf,N_,W.sum(1),1)
            G=Gf.reshape(B,S,T)
            gr=[G.sum(2),G.sum(1),(G*v[:,None,:]).sum(2),(G*u[:,:,None]).sum(1)]
            for k in range(4):
                M[k]=0.9*M[k]+0.1*gr[k]; V[k]=0.999*V[k]+0.001*gr[k]**2
                P[k]=P[k]-lr*(M[k]/(1-0.9**(i+1)))/(np.sqrt(V[k]/(1-0.999**(i+1)))+1e-8)
            if i%100==99 or i==steps-1:
                Sf=sc(P,np.float64); Sp=np.take_along_axis(Sf,P_,1); Sn=np.take_along_axis(Sf,N_,1)
                d=Sp[:,:,None]-Sn[:,None,:]
                cnt=((d>0).sum((1,2))*2+(d==0).sum((1,2)))/2
                cb=cnt.reshape(len(idx),K); am=cb.argmax(1); mx=cb.max(1)
                for j in range(len(idx)):
                    if mx[j]>bestc[j]:
                        bestc[j]=mx[j]; k=j*K+am[j]
                        bestm[j]=[P[q][k].astype(np.float64).copy() for q in range(4)]
        out[idx]=bestc
        for j,g in enumerate(idx): mem[g]=bestm[j]
    return out,npairs,mem
def frac_count(Y,a,b,u,v):
    S,T=Y.shape
    sc=[[Fraction(float(a[i]))+Fraction(float(b[j]))+Fraction(float(u[i]))*Fraction(float(v[j])) for j in range(T)] for i in range(S)]
    P=[sc[i][j] for i in range(S) for j in range(T) if Y[i,j]==1]; N=[sc[i][j] for i in range(S) for j in range(T) if Y[i,j]==0]
    w=0
    for p in P:
        for q in N:
            w+=2 if p>q else (1 if p==q else 0)
    return w/2
def rand_board(rng,S,T,k):
    Y=np.zeros((S,T),int)
    for s in range(S): Y[s,rng.choice(T,k,replace=False)]=1
    return Y
def flat_board(rng,S,T,k):
    nf=rng.integers(1,3); Y=np.zeros((S,T),int); cols=rng.permutation(T)
    on=cols[:nf]; off=cols[nf:2*nf]; rest=cols[2*nf:]
    Y[:,on]=1
    for s in range(S): Y[s,rng.choice(rest,k-nf,replace=False)]=1
    return Y
def wh():
    H=np.array([[1]])
    for _ in range(3): H=np.block([[H,H],[H,-H]])
    return H
def show(Y): return [np.flatnonzero(r).tolist() for r in Y]
def is_circulant(Y):
    S,T=Y.shape
    if S!=T: return False
    return all((Y[s]==np.roll(Y[0],s)).all() for s in range(S)) or all((Y[s]==np.roll(Y[0],-s)).all() for s in range(S))
