import json,csv,numpy as np
from fractions import Fraction
bad=0;tot=0
for shape in ('5x8','8x8','10x10','13x13'):
    M=json.load(open(f'members_{shape}.json'))
    for k,m in M.items():
        S=len(m['rows']); T=int(shape.split('x')[1]); Y=np.zeros((S,T),int)
        for s,r in enumerate(m['rows']): Y[s,r]=1
        sc=[[Fraction(m['a'][i])+Fraction(m['b'][j])+Fraction(m['u'][i])*Fraction(m['v'][j]) for j in range(T)] for i in range(S)]
        P=[sc[i][j] for i in range(S) for j in range(T) if Y[i,j]]; N=[sc[i][j] for i in range(S) for j in range(T) if not Y[i,j]]
        w=sum(2 if p>q else 1 if p==q else 0 for p in P for q in N)/2
        tot+=1; bad+= (w!=m['count'])
rows=list(csv.DictReader(open('survey_boards.csv')))
byk={(r['shape'],r['board_id']):float(r['best_count']) for r in rows}
mm=0
for shape in ('5x8','8x8','10x10','13x13'):
    M=json.load(open(f'members_{shape}.json'))
    for k,m in M.items(): mm+= byk[(shape,k)]!=m['count']
print('members rechecked',tot,'count mismatches vs json',bad,'csv rows',len(rows),'csv-vs-json mismatches',mm)
