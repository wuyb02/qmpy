from __future__ import print_function
from dmcread import * 
import os

data={}
for dir in ["p90","c6h6","water"]:
  os.system("cd %s; /u/sciteam/ywu27/software/qwalk-Dec2014mklucas-gnu/qwalk/bin/gosling -reblock 1 qwalk.vmc.log > qwalk.vmc.log.stdout"%dir)
  data[dir]=np.array(get_gosling_en("%s/qwalk.vmc.log.stdout"%dir))
  print(dir,data[dir][0],data[dir][1])
 
conv=27.212*1000

p90diff=diff(data['p90'],data['c6h6'])
p90diff=np.array(diff(p90diff,data['water']))
p90diff*=conv
print("water-benzene at large separation - isolated molecules (meV): ",p90diff[0],"+/-",p90diff[1])
print(data["p90"][0],data["p90"][1],data["c6h6"][0],data["c6h6"][1],data["water"][0],data["water"][1],p90diff[0],p90diff[1])
