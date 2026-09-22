import numpy as np
def decode(d,f,c):
 E,R,W,A=d["E"],d["R__sym16"],d["W__sym32"]*.17,d["A__sym16"]
 n=np.cumsum(d["L"])[:-1]
 M,X=np.split(d["O"],n),np.split(np.exp(.35*d["P__sym16"]),n)
 z=[m for m,x in enumerate(M)if x.tolist()==[[0,0]]]
 b=z[0]if z else np.bincount(R[:,2],minlength=len(M)).argmax()
 p,o=[],[]
 for s,t in c:
  F=np.flatnonzero(E[s,R[:,0]]&E[t,R[:,1]])
  p+=[1-(1-2**-(1+A[-1]/2))*np.prod(1-(R[F,4]+.5)/16)]
  m,g,w=b,0,W[-1]
  if len(F):j=F[np.argmax(R[F,4]*400-R[F,0]*20-R[F,1])];m,g,w=R[j,2],R[j,3],W[j]
  u,v=M[m].T
  for _ in range(g//2):u,v=u+v,-u
  if g%2:u,v=v,u
  x=X[m]
  o+=[dict(zip(zip(u,v),np.exp(w+A[s]/4+A[65+t]/4-4)*x/x.sum()))]
 return{"p_exist":np.clip(p,.001,.999),"offsets":o,"sign":np.where(d["S"][c[:,0]],1,-1)}
