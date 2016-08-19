import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import numpy.random as nprand
from scipy import stats
import math
from hodmc import *

plt.rc('text',usetex=True)
plt.rc('lines',linewidth=1)
plt.rc('legend',fontsize=10)
plt.rc('mathtext',fontset='cm')
plt.rc('font',**{'family':'serif','serif':['Times New Roman'],'size':18},weight='bold')
plt.rc('font',weight='bold')

nw=10000
dt=0.04
normal_guess=False #Change this to get different initial guesses
enforce_node=True  #Change this to enforce node boundaries 
guess_sigma=0.5
plot_range=5
ho=HOdmc(nw=nw, dt=dt, normal_guess=normal_guess, enforce_node=enforce_node, guess_sigma=guess_sigma, plot_range=plot_range)

nstep=100
nw_plot=100
ylim_psi=1.0

fig,axes=plt.subplots(2,2,figsize=(8,6),sharey=False,sharex=True)

axes[0][0].plot(np.linspace(-ho.plot_range,ho.plot_range,200),ho.V(np.linspace(-ho.plot_range,ho.plot_range,200)),linestyle="-",linewidth=1.5,marker='',markersize=7,fillstyle='none',mew=1.5,color='b')
axes[0][0].set_xlabel("x")
axes[0][0].get_xaxis().set_ticks([])
axes[0][0].get_yaxis().set_ticks([])
axes[0][0].annotate("$V(x)$",xy=(0.0*ho.plot_range,ho.V(0.75*ho.plot_range)),ha='center')


xplot=np.linspace(-ho.plot_range,ho.plot_range,200)
axes[1][0].plot(xplot,np.zeros(xplot.shape),linestyle="--",linewidth=1.5,marker='',markersize=7,fillstyle='none',mew=1.5,color='k')
if ho.normal_guess:
    axes[1][0].plot(xplot,ho.psi_guide(xplot)*np.exp(-xplot**2/(2*ho.guess_sigma**2))/(ho.guess_sigma*np.sqrt(2*math.pi)),label="$\Psi_T$(x)",color='b')
else:
    axes[1][0].plot(xplot,ho.psi_guide(xplot)/(2*ho.plot_range),label="$\Psi_T$(x)",color='b')

axes[1][0].annotate("$\Psi_T(x)$",xy=(-0.9*ho.plot_range,0.20))
axes[1][0].set_xlabel("x")
axes[1][0].get_xaxis().set_ticks([])
axes[1][0].get_yaxis().set_ticks([0.0])
axes[1][0].set_xlim([-ho.plot_range,ho.plot_range])
axes[1][0].set_ylim([-ylim_psi,ylim_psi])


axes[0][1].set_xlabel("x")
axes[0][1].set_ylabel(r"Evolution $\rightarrow$")
axes[0][1].get_xaxis().set_ticks([])
axes[0][1].get_yaxis().set_ticks([])


for s in range(0,nstep):
    #plot the first nw_plot walker positions
    axes[0][1].plot(ho.x[0:nw_plot],np.ones(nw_plot)*s*ho.dt,marker='o',markersize=1,color='r',linestyle="")
    axes[0][1].set_xlim([-ho.plot_range,ho.plot_range])
    axes[0][1].set_ylim([-ho.dt,ho.dt*nstep])

    #Plot the 'histogram' of the walker positions
    axes[1][1].clear()
    spc=np.linspace(-ho.plot_range,ho.plot_range,200)
    axes[1][1].plot(spc,np.zeros(spc.shape),'k--',linewidth=1)
    axes[1][1].plot(spc,ho.histogram(spc))
    axes[1][1].set_xlim([-ho.plot_range,ho.plot_range])
    axes[1][1].set_ylim([-ylim_psi,ylim_psi])
    axes[1][1].set_xlabel("x")
    axes[1][1].annotate(r"$\Psi_T(x)\rho(x)$",xy=(-0.9*plot_range,0.2))
    axes[1][1].get_xaxis().set_ticks([])
    axes[1][1].get_yaxis().set_ticks([])

    plt.savefig("frame%.4i.png"%s)

    ho.netx_step()
    print(ho.x.shape[0])
    print("nconf %d eref %f"%(ho.x.shape[0],ho.eref))
