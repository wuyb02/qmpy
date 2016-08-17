from __future__ import print_function
from qmcconfigread import * 
from math import sqrt
import os

qmc=str(sys.argv[1])
nelec=int(sys.argv[2])
nwalker=int(sys.argv[3])
zd=float(sys.argv[4])
dzm=float(sys.argv[5])
dzp=float(sys.argv[6])

nhead=2
ntail=1

for iwalker in range(0,nwalker):
  ilen=nelec+nhead+ntail
  istart=iwalker*ilen+1
  iend=(iwalker+1)*ilen
  os.system("head -%d %s.config | tail -%d >%s.config.iblock"%(iend,qmc,ilen,qmc))
  if iwalker==0:
    os.system("cat %s.config.iblock | head -%d >%s.config.new"%(qmc,nhead,qmc))
  else:
    os.system("cat %s.config.iblock | head -%d >>%s.config.new"%(qmc,nhead,qmc))
  os.system("cat %s.config.iblock | head -%d | tail -%d >%s.config.iblockxyz"%(qmc,nhead+nelec,nelec,qmc))
  ZZ=getconfig(qmc)
  configtransz(ZZ,zd,dzm,dzp)
  mstout=printconfig(ZZ)
  os.system("echo \"%s\" >>%s.config.new"%(mstout,qmc))
  os.system("cat %s.config.iblock | tail -%d >>%s.config.new"%(qmc,ntail,qmc))
  if iwalker%100==0:
    print(iwalker)
