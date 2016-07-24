from __future__ import print_function
import os
import sys

# case=str(sys.argv[1])
nw=int(sys.argv[1])

# dirs=["p36pbe","p70pbe"]
# dirs=["p36rf","p70rf"]
dirs=["p36hf","p70hf"]
# dirs=["p36acfdt","p70acfdt"]

data={}
for dir in dirs:
  os.system("cd %s; grep \"free  energy   TOTEN\" OUTCAR | awk '{print $5}' >OUTCAR.E.o"%(dir))
  # os.system("cd %s; grep \"converged value\" OUTCAR | awk '{print $3}' >OUTCAR.E.o"%(dir))
  f = open("%s/OUTCAR.E.o"%(dir),'r')
  data[dir]=float(f.read())/27.212
  print(dir,data[dir])

conv=1000*27.212

if len(dirs)>1 and len(dirs)<4:
  p90diff=data[dirs[0]]
  for i in range(1,len(dirs)):
    p90diff=p90diff-data[dirs[i]]
  p90diff*=(conv/nw)
  print("g-w"," (meV): ",p90diff)

mstrout=""
for i in range(0,len(dirs)):
  mstrout=mstrout+"%.9f "%(data[dirs[i]])
if len(dirs)>1 and len(dirs)<4:
  mstrout=mstrout+"%.2f "%(p90diff)
print(mstrout)
