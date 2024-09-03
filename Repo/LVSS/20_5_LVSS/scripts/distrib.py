import numpy as np

def erfv(x,slope=20,scale=1,sep=5,center=0):
    y=np.zeros_like(x)
    p=0
    for i in x:
        y[p]=scale*(0.5*np.math.erfc(slope*(x[p]-center+sep))+0.5*np.math.erfc(slope*(-x[p]+sep+center)))

        p+=1
    return y
def erfvd(x,slope=20,scalea=1,scaleb=1,sep=5,center=0):
    y=np.zeros_like(x)
    p=0
    for i in x:
        y[p]=scalea*0.5*np.math.erfc(slope*(x[p]-center+sep))+scaleb*0.5*np.math.erfc(slope*(-x[p]+sep+center))

        p+=1
    return y

def gaussian(x,center,tau,scale):
    y=scale*(np.exp(-((x-center)**2)/2/tau/tau))/np.sqrt(2*np.pi)/tau 

    return y

def erfv_stepr(x,slope=20,scale=1,sep=5,center=0):
    y=np.zeros_like(x)
    p=0
    for i in x:
        y[p]=scale*(0.5*np.math.erfc(slope*(-x[p]+sep+center)))

        p+=1
    return y
def erfv_stepl(x,slope=20,scale=1,sep=5,center=0):
    y=np.zeros_like(x)
    p=0
    for i in x:
        y[p]=scale*(0.5*np.math.erfc(slope*(x[p]-center+sep)))

        p+=1
    return y

        
def mserf(x,slope=20,scale=1,sep=5,center=0,halfwidth=60):
    y=np.zeros_like(x)
    p=0
    #for i in x:
    y=(erfv_stepr(x,slope,scale,sep,center-(halfwidth+1))*erfv_stepl(x,slope,scale,sep,center+(halfwidth+1)))**.5
    
    #    p+=1
    return y
