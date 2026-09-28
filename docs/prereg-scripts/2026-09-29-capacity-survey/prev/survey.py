import numpy as np, time, itertools, sys, json
F32=np.float32
def prep(boards):
    Y=np.asarray(boards).reshape(len(boards),-1)
    Pi=np.stack([np.flatnonzero(y==1) for y in Y]); Ni=np.stack([np.flatnonzero(y==0) for y in Y])
    return Pi,Ni
def best_auc(boards,S,T,K=500,steps=800,seed=0,chunk_pairs=3.0e8):
    """returns best exact count for each board (max over K starts) and n pairs"""
    boards=np.asarray(boards); nb=len(boards); Pi,Ni=prep(boards)
    npr,nn=Pi.shape[1],Ni.shape[1]; npairs=npr*nn
    per_board=max(1,int(chunk_pairs/(K*npairs*4*3)))  # boards per chunk
    out=np.zeros(nb); rng=np.random.default_rng(seed)
    for c0 in range(0,nb,per_board):
        idx=np.arange(c0,min(nb,c0+per_board)); B=len(idx)*K
        bo=np.repeat(np.arange(len(idx)),K); P_=Pi[idx][bo]; N_=Ni[idx][bo]
        P=[rng.normal(size=(B,k)).astype(F32) for k in (S,T,S,T)]
        M=[np.zeros_like(p) for p in P]; V=[np.zeros_like(p) for p in P]
        best=np.full(B,-1.0); lr=F32(0.05)
        def sc(P): a,b,u,v=P; return (a[:,:,None]+b[:,None,:]+u[:,:,None]*v[:,None,:]).reshape(B,-1)
        for i in range(steps):
            a,b,u,v=P; Sf=sc(P)
            Sp=np.take_along_axis(Sf,P_,1); Sn=np.take_along_axis(Sf,N_,1)
            temp=F32(0.01**(i/steps))
            d=(Sp[:,:,None]-Sn[:,None,:])/temp
            sg=1/(1+np.exp(-np.clip(d,-30,30))); W=sg*(1-sg)/temp
            Gf=np.zeros_like(Sf)
            np.put_along_axis(Gf,P_,-W.sum(2),1); np.put_along_axis(Gf,N_,W.sum(1),1)  # loss=-sum sigmoid
            G=Gf.reshape(B,S,T)
            gr=[G.sum(2),G.sum(1),(G*v[:,None,:]).sum(2),(G*u[:,:,None]).sum(1)]
            for k in range(4):
                M[k]=0.9*M[k]+0.1*gr[k]; V[k]=0.999*V[k]+0.001*gr[k]**2
                P[k]=P[k]-lr*(M[k]/(1-0.9**(i+1)))/(np.sqrt(V[k]/(1-0.999**(i+1)))+1e-8)
            if i%100==99 or i==steps-1:
                Sf=sc(P); Sp=np.take_along_axis(Sf,P_,1); Sn=np.take_along_axis(Sf,N_,1)
                d=Sp[:,:,None]-Sn[:,None,:]
                cnt=((d>1e-6).sum((1,2))*2+(np.abs(d)<=1e-6).sum((1,2)))/2
                best=np.maximum(best,cnt)
        out[idx]=best.reshape(len(idx),K).max(1)
    return out,npairs
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
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='test':
        rng=np.random.default_rng(1)
        F=np.array([[1,1,0,0,1,1,0,0],[0,0,1,1,1,0,1,0],[1,0,1,0,0,1,0,1],[1,1,0,1,0,0,1,0],[0,1,1,1,0,0,0,1]])
        for steps in (400,800,1500):
            t=time.time(); o,n=best_auc([F],5,8,K=500,steps=steps,seed=3); print(steps,o,time.time()-t)
        bs=[rand_board(rng,5,8,4) for _ in range(20)]
        for steps in (400,800):
            t=time.time(); o,n=best_auc(bs,5,8,K=500,steps=steps,seed=3); print(steps,o.mean(),o.min(),time.time()-t)
