from __future__ import print_function
import os
import sys

# case=str(sys.argv[1])
nw=int(sys.argv[1])

dirs=["p336","p70"]
# dirs=["p70","b3n3h6","water"]
# dirs=["p336","b3n3h6","water"]
# dirs=["p32","p336","p36","p70","b3n3h6","water"]

data={}
for dir in dirs:
  os.system("cd %s; grep \"energy without entropy\" OUTCAR | tail -1 | awk '{print $5}' >OUTCAR.E.o"%(dir))
  f = open("%s/OUTCAR.E.o"%(dir),'r')
  data[dir]=float(f.read())/27.212
  print(dir,data[dir])

conv=1000*27.212

if len(dirs)>1 and len(dirs)<4:
  p90diff=data[dirs[0]]
  for i in range(1,len(dirs)):
    p90diff=p90diff-data[dirs[i]]
  p90diff*=(conv/nw)
  print("water-b3n3h6"," (meV): ",p90diff)

mstrout=""
for i in range(0,len(dirs)):
  mstrout=mstrout+"%f "%(data[dirs[i]]/nw)
if len(dirs)>1 and len(dirs)<4:
  mstrout=mstrout+"%f "%(p90diff)
print(mstrout)
