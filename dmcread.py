import re
import math
import numpy as np
import sys
import os.path
def diff(a,b):
  diffavg=a[0]-b[0]
  diffvar=math.sqrt(a[1]**2+b[1]**2)
  return diffavg,diffvar


def get_crystal_en(filename):
  enline=""
  if not os.path.isfile(filename):
    return ("","")

  for line in open(filename, 'r'):
    if re.search('SCF ENDED', line):
       enline=line
       break
  spl=enline.split()
  if len(spl)> 9:
    return (float(spl[8]),0.0)
  else:
    return ("","")


def get_gosling_en(filename):
  enline=""
  for line in open(filename, 'r'):
    if re.search('total_energy0', line):
      enline=line
      break
  spl=enline.split()
  return (float(spl[1]),float(spl[3]))

def average_kpoints(basename,weights,numbers=None,method="vmc"):
  nkpt=len(weights)
  if(numbers==None):
    numbers=range(0,nkpt)
  totweight=np.sum(weights)
  ens=[]
  for i in range(0,nkpt):
    fname=basename+str(numbers[i])+"."+method+".log.stdout"
    if not os.path.isfile(fname):
#      print("couldn't find ",fname)
      return ("","")
    ens.append(get_gosling_en(fname))
  
  avgen=0.0
  for k in range(0,nkpt):
    weights[k]/=totweight
    avgen+=weights[k]*ens[k][0]
  avgerr=0.0
  for k in range(0,nkpt):
    avgerr+=(weights[k]*ens[k][1])**2
  avgerr=math.sqrt(avgerr)
  return (avgen,avgerr) 
