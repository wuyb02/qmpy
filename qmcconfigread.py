from __future__ import print_function
import os
import sys

def getconfig(qmc):
  f = open("%s.config.iblockxyz"%(qmc),'r')
  A=f.read()
  D=A.split("\n")
  D.remove('');
  ZZ={}
  for k in range(0,len(D)):
    E=D[k].split(" ")
    E.remove('');
    F={}
    for l in range(0,3):
      F[l]=float(E[l])
    ZZ[k]=F

  return (ZZ)

def configtransz(ZZ,zd,dzm,dzp):
  for k in range(0,len(ZZ)):
    Z=ZZ[k]
    if Z[0]>zd:
      Z[0]=Z[0]+dzp
    else:
      Z[0]=Z[0]+dzm

def printconfig(ZZ):
  mstrout=""
  for k in range(0,len(ZZ)):
    Z=ZZ[k]
    mstrout=mstrout+"%.15f %.15f %.15f"%(Z[0],Z[1],Z[2])
    if k!=(len(ZZ)-1):
      mstrout=mstrout+"\n"

  return (mstrout)
