import numpy as np
def decode(d,f,c):
 Q,k,L=d["Q__sym32"]-16.,d["c"],d["L"].tolist()
 a,b,u,v,x,y=Q[:390].reshape(6,65)/16*k[[1,1,2,2,3,3],None]
 A,B=Q[390:520].reshape(2,65).astype(int)+16
 W=Q[520:536].reshape(4,4)/16*k[4]
 S,i=[],0
 while i<len(L):n=L[i];S+=[list(zip(L[i+1:i+1+n],L[i+1+n:i+1+2*n]))];i+=1+2*n
 m=dict(zip(sorted({o for q in S for o in q}),(Q[536:]+16)/31*k[5]))
 g=np.where(f[:,0]>1,3,f[:,2])
 e=d["e__sym8"]
 s,t=c.T
 z=k[0]+a[s]+b[t]+u[s]*v[t]+W[g[s],g[t]]
 o=[{q:np.expm1(m[q]+x[p]+y[r])for q in S[B[r]if e[65+r]>e[p]else A[p]]}for p,r in c.tolist()]
 return{"p_exist":1/(1+np.exp(-z)),"offsets":o,"sign":np.where(d["s"][s],1,-1)}
