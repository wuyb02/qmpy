from __future__ import print_function
from dmcread import * 
from math import sqrt
import os

qmc=str(sys.argv[1])
N=int(sys.argv[2])
reblock=int(sys.argv[3])
nw=int(sys.argv[4])

# dirs=["p70","g","water"]
dirs=["p36","p70"]
# dirs=["p336","p70","b3n3h6","water"]
# dirs=["p336","p70"]

data={}
datai={}
for dir in dirs:
  weights=[0.00694,0.01389,0.01389,0.01389,0.01389,0.01389,0.00694,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.01389,0.00694,0.01389,0.01389,0.01389,0.01389,0.01389,0.00694]
  if N==1:
    weights=[1.0]
  print(dir)
  data[dir]=[0.0,0.0]
  for i in range(0,N):
    filename="qwalk_%d.%s"%(i,qmc)
    if N==1:
      filename="qwalk.%s"%(qmc)
    os.system("cd %s; /u/sciteam/ywu27/software/qwalk-Dec2014mklucas-gnu/qwalk/bin/gosling -reblock %d %s.log > %s.log.stdout"%(dir,reblock,filename,filename))
    datai=np.array(get_gosling_en("%s/%s.log.stdout"%(dir,filename)))
    print(i,datai[0],datai[1])
    data[dir][0]+=datai[0]*weights[i]
    data[dir][1]+=datai[1]*datai[1]*weights[i]*weights[i]
  data[dir][1]=sqrt(data[dir][1])
  print(dir,data[dir][0],data[dir][1])
 
conv=27.212*1000

if len(dirs)>1 and len(dirs)<4:
  p90diff=data[dirs[0]]
  for i in range(1,len(dirs)):
    p90diff=np.array(diff(p90diff,data[dirs[i]]))
## p90diff=np.array(diff(p90diff,data['waterzbox30k661mp02']))
  p90diff*=(conv/nw)
  print("g-w (meV): ",p90diff[0],"+/-",p90diff[1])

mstrout=""
for i in range(0,len(dirs)):
  mstrout=mstrout+"%f %f "%(data[dirs[i]][0],data[dirs[i]][1])
if len(dirs)>1 and len(dirs)<4:
  mstrout=mstrout+"%f %f "%(p90diff[0],p90diff[1])
print(mstrout)
