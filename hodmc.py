import numpy as np
import numpy.random as nprand
from scipy import stats
import math

class HOdmc(object):
    def __init__(self, dt=0.04, nw=10000, normal_guess=False, enforce_node=False, x0=None, guess_sigma=0.5, plot_range=5):
        self.dt=dt
        self.nw=nw
        self.normal_guess=normal_guess
        self.enforce_node=enforce_node
        self.guess_sigma=guess_sigma
        self.plot_range=plot_range
        
        if x0==None:
            if(normal_guess):
                self.x=nprand.randn(nw)*guess_sigma
            else:
                self.x=2*plot_range*(nprand.random(nw)-0.5)
        else:
            this.x=x0

        self.eref=np.sum(self.V(self.x))/nw
            
    def V(self,x):
        return 0.2*x**2
    
    def psi_guide(self,x):
        psi=np.ones(x.shape)
        if self.enforce_node:
            psi[x<0]=-1
        return psi
    
    def histogram(self,spc):
        kernel=stats.gaussian_kde(self.x,0.01*self.plot_range)
        return kernel.evaluate(spc)*self.psi_guide(spc)

    def netx_step(self):
        x=self.x
        dt=self.dt
        eref=self.eref
        currnw=x.shape[0]
        sdt=np.sqrt(dt)
        next_x=x+sdt*nprand.randn(currnw)
        #fixed node
        psi_old=self.psi_guide(x)
        psi_new=self.psi_guide(next_x)
        not_changed= np.equal(psi_old,psi_new)
        x=next_x[not_changed]
        currnw=x.shape[0]
        #branching
        v=self.V(x)
        weight=np.exp(-dt*(v-eref))
        branch=np.floor(weight+nprand.random(currnw))
        newx=[]
        for i,j in zip(x,branch):
            for k in range(int(j)):
                newx.append(i)
        x=np.array(newx)
        self.x=x
        self.nw=x.shape[0]
        self.eref=eref-dt*np.log(float(x.shape[0])/self.nw) 
        
    def __str__(self):
        return "dt:%f, nw:%d, normal_guess:%r, enforce_node:%r" %(self.dt, self.nw, self.normal_guess, self.enforce_node)

    def __len__(self):
        return self.nw

    def __del__(self):
        print("A HOdmc instance is destroyed")
