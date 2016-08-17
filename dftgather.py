from __future__ import print_function
import os

data={}
for dir in ["p90","c6h6","water"]:
  os.system("cd %s; grep \"Total =\" c6h6.fdf.out | awk '{print $4}'>c6h6.fdf.E.out"%dir)
  f = open("%s/c6h6.fdf.E.out"%dir,'r')
  data[dir]=float(f.read())
  print(dir,data[dir])
 
conv=1000

p90diff=(data["p90"]-data["c6h6"]-data["water"])*conv
print("water-benzene at large separation - isolated molecules (meV): ",p90diff)
