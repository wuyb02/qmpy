import os
import csv
import numpy as np

pdefaults={'system':'g-w','cellsize':2,'nw':1,'omega0':'y'}

runs=['p32','p34','p36','p38','p45','p60','p70','g','w']
zo={'p32':3.2,'p34':3.4,'p36':3.6,'p38':3.8,'p45':4.5,'p60':6.0,'p70':7.0,'g':'','w':''}
methods=['pbe','hf','hfc','rf','acfdt']

def get_E(filename):
  enline=""
  for line in open(filename, 'r'):
    if 'energy  without entropy' in line:
      enline=line
      break
  spl=enline.split()
  return (float(spl[6])/27.212)

def get_Eacfdt(filename):
  enline=""
  for line in open(filename, 'r'):
    if 'converged value' in line:
      enline=line
      break
  spl=enline.split()
  return (float(spl[2])/27.212)

def get_Ehfc(filename):
  enline=""
  for line in open(filename, 'r'):
    if 'HF-correction' in line:
      enline=line
      break
  spl=enline.split()
  return (float(spl[3])/27.212)

def get_Para(filename,para,ipos):
  enline=""
  for line in open(filename, 'r'):
    if para in line:
      enline=line
      break
  spl=enline.split()
  return (float(spl[ipos]))

def get_Paraln(filename,iline,ipos):
  enline=""
  for i,line in enumerate(open(filename, 'r')):
    if i==iline:
      enline=line
      break
  spl=enline.split()
  return (float(spl[ipos]))

def get_Parabool(filename,para,ipos):
  enline=""
  iline=-1
  for i,line in enumerate(open(filename, 'r')):
    if para in line:
      enline=line
      iline=i
  bpara='n'
  if iline>0 and iline<i:
    spl=enline.split()
    if spl[ipos]=='T':
      bpara='y'
  return (bpara)

data=[]
for r in runs:
  for m in methods:
    dir=r+m
    if os.path.isfile(dir+"/OUTCAR") and os.path.isfile(dir+"/INCAR") and os.path.isfile(dir+"/POSCAR") and os.path.isfile(dir+"/KPOINTS"):
      if r=='g' or r=='w':
        sys=r
      else:
        sys=pdefaults['system']
      zbox=get_Paraln(dir+"/POSCAR",4,2)
      ecut=get_Para(dir+"/INCAR",'ENCUT',2)
      ediff=get_Para(dir+"/INCAR",'EDIFF',2)
      if m!='acfdt' and m!='hfc':
        ismear=int(get_Para(dir+"/INCAR",'ISMEAR',2))
      sigma=get_Para(dir+"/INCAR",'SIGMA',2)
      ispin=int(get_Para(dir+"/INCAR",'ISPIN',2))
      idipl=get_Para(dir+"/INCAR",'IDIPOL',2)
      ldipl=get_Parabool(dir+"/INCAR",'LDIPOL',2)
      if ldipl=='y':
        dipl=get_Para(dir+"/INCAR",'DIPOL = 0',4)
      else:
        dipl=''
      kgrid=get_Paraln(dir+"/KPOINTS",3,0)
      ecutgw=''
      nomega=''
      omega0=''
      if m=='acfdt':
        ecutgw=get_Para(dir+"/INCAR",'ENCUTGW',2)
        nomega=get_Para(dir+"/INCAR",'NOMEGA',2)
        en=get_Eacfdt(dir+"/OUTCAR")
        omega0=pdefaults['omega0']
      elif m=='rf':
        omega0=pdefaults['omega0']
        en=get_E(dir+"/OUTCAR")
      elif m=='hfc':
        en=get_Ehfc(dir+"/OUTCAR")
      else:
        en=get_E(dir+"/OUTCAR")
      print(dir,en)
      data.append( {'system':sys,
                    'cellsize':pdefaults['cellsize'],
                    'nw':pdefaults['nw'],
                    'natdope':0,
                    # 'rdope':0,
                    'zo':zo[r],
                    'method':m,
                    'Ecut':ecut,
                    'Ecutgw':ecutgw,
                    'Ediff':ediff,
                    'zbox':zbox,
                    'ismear':ismear,
                    'sigma':sigma,
                    'nomega':nomega,
                    'omega0':omega0,
                    'ispin':ispin,
                    'kgrid':kgrid,
                    'idipl':idipl,
                    'ldipl':ldipl,
                    'dipl':dipl,
                    'energy':en,
                    'final':'y'})

with open('g-w.rpa.csv','w') as csvfile:
  fieldnames = ['system','cellsize','nw','natdope','zdope','zo','method','Ecut','Ecutgw','Ediff','zbox','ismear','sigma','nomega','omega0','ispin','kgrid','idipl','ldipl','dipl','energy','final']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

  # writer.writeheader()
  writer.writerow(dict(zip(fieldnames,fieldnames)))
  writer.writerows(data)
