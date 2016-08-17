from __future__ import print_function
import os
import sys

case=str(sys.argv[1])
nw=int(sys.argv[2])

# dirs=["p34","p90"]
dirs=["p90","c6h6","water"]

data={}
for dir in dirs:
  os.system("cd %s; grep \"SCF ENDED\" %s.crystal.o | awk '{print $9}'>%s.crystal.E.o"%(dir,case,case))
  f = open("%s/%s.crystal.E.o"%(dir,case),'r')
  data[dir]=float(f.read())
  print(dir,data[dir])

conv=1000*27.212

if len(dirs)>1:
  p90diff=data[dirs[0]]
  for i in range(1,len(dirs)):
    p90diff=p90diff-data[dirs[i]]
  p90diff*=(conv/nw)
  print("water-%s"%case," (meV): ",p90diff)

mstrout=""
for i in range(0,len(dirs)):
  mstrout=mstrout+"%f "%(data[dirs[i]]/nw)
if len(dirs)>1:
  mstrout=mstrout+"%f "%(p90diff)
print(mstrout)
