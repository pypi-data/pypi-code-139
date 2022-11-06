#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   optimize.py
@Time    :   2020/02/10 16:55:28
@Author  :   sk zhao 
@Version :   1.0
@Contact :   2396776980@qq.com
@License :   (C)Copyright 2017-2018, Zhaogroup-iop
@Desc    :   None
'''

# here put the import lib
import time, numpy as np, matplotlib.pyplot as plt
from scipy import fftpack
from sklearn.cluster import KMeans
from scipy.optimize import least_squares as ls, curve_fit, basinhopping as bh
from scipy import signal
import asyncio, scipy
import sympy as sy
import dataTools as dtl
from collections import Counter
xvar = sy.Symbol('x',real=True)

'''
主要采用了全局优化的思想进行拟合
相比于optimize_old模块，该模块的思想是利用全局最优化算法进行数据拟合，方法采自scipy.optimize模块，以basinhopping为例，就是来最小化残差函数，
相比于最小二乘法，他要求残差函数返回的为每一点的残差平方和，该法对初始值相对不敏感，精度高。
'''


# func_willBeused = {'Expfunc':Exp_Fit().func}


################################################################################
### 拟合参数边界
################################################################################

class MyBounds(object):
    def __init__(self, xmax=[1.1,1.1], xmin=[-1.1,-1.1] ):
        self.xmax = np.array(xmax)
        self.xmin = np.array(xmin)
    def __call__(self, **kwargs):
        x = kwargs["x_new"]
        tmax = bool(np.all(x <= self.xmax))
        tmin = bool(np.all(x >= self.xmin))
        return tmax and tmin
        
################################################################################
### 生数据预处理  exeFit
###################### ##########################################################

class RowToRipe():
    def __init__(self):
        pass
    def space(self,y):
        ymean, ymax, ymin = np.mean(y), np.max(y), np.min(y)
        d = y[np.abs(y-ymean)>0.05*(ymax-ymin)]
        if len(d) < 0.9*len(y):
            return len(d) + int(len(y)*0.1)
        else:
            return len(y)
    
    def errspace(self,func,paras,args):

        return (func(args['x'],paras)-args['y'])**2

    def deductPhase(self,x,y):
        if np.ndim(y) != 2:
            y = [y]
        s = []
        for i in y:
            phi = np.unwrap(np.angle(i), 0.9 * np.pi)
            phase = np.poly1d(np.polyfit(x, phi, 1))
            base = i / np.exp(1j * phase(x))
            s.append(base)
        return x, np.array(s)

    def manipulation(self,volt,freq,s,which='min',dosmooth=False,f0=0.25,axis=1):
        manfunc = np.argmin if which == 'min' else np.argmax
        s_abs = np.abs(s) 
         
        if dosmooth: 
            s_abs = self.smooth(s_abs,axis=axis,f0=f0)
            # min_index = []      
            # for i in range(np.shape(s)[axis]):
            #     z = s_abs[i,:]
            #     # loc = freq[manfunc(z)]
            #     z_smooth = self.movingAverage(z,smoothnum)
            #     # t,index = self.firstMax(freq,z_smooth,num=loc,peakpercent=0.9,insitu=True)
            #     index = manfunc(z_smooth)
            #     min_index.append(index)
        # else:
        #     min_index = manfunc(s_abs,axis=axis)     
        min_index = manfunc(s_abs,axis=axis)         
        x, y = np.array(volt), np.array([freq[j] for j in min_index]) 
        return x,y

    def extension(self,s,ax=0,periodic_extension=0,padding=0):
        axis = np.shape(s)

        if len(axis) == 2:
            if periodic_extension:
                if ax == 1:
                    s = np.array((list(s)+list(s[:,::-1]))*periodic_extension)
                if ax == 0:
                    s = np.array((list(np.array(s).T)+list(np.array(s[::-1,:]).T))*periodic_extension).T
            shape = (axis[0]*2*periodic_extension+padding,axis[1]) if ax == 1 else (axis[0],axis[1]*2*periodic_extension+padding)
            data = np.zeros(shape)
            rows, cols = np.shape(s)
            print(shape)
            data[:rows,:cols] = s
        else:
            if periodic_extension:
                if ax == 0:
                    s = np.array((list(s)+list(s[::-1]))*periodic_extension)
            shape = (axis[0]*2*periodic_extension+padding,)
            data = np.zeros(shape)
            rows = len(s)
            data[:rows] = s
        return data
  
    def firstMax(self,x,y,num=0,peakpercent=0.9,insitu=False,mean=True,which='max'):
        """
        x:       线性扫描点
        insitu:  如果为True，截取peak值为x为num时对应的值乘以peakpercent，False为最大值乘以peakpercent
        """
        if which != 'max':
            y = np.abs(y-y.max())
        index0 = np.argmin(np.abs(x-num))
        y = y - np.min(y)
        peak = peakpercent*y[index0] if insitu else peakpercent*np.max(y)
        c = np.argwhere(y>peak)
        cdiff = np.diff(c[:,0])
        n_clusters = len(np.argwhere(cdiff>np.mean(cdiff))) + 1
        S = c[:,0]
        d = np.mat(list(zip(S,S)))

        kmeans = KMeans(n_clusters=n_clusters,max_iter=100,tol=0.001)
        yfit = kmeans.fit_predict(d)
        xaxis = S[yfit==yfit[np.argmin(np.abs(S-index0))]]
        index =  int(np.mean(xaxis)) if mean else int(xaxis[np.argmax(y[xaxis])])
        bias0 = round(x[index],5)
        return bias0 ,index

    def smooth(self,y,f0=0.1,axis=-1):
        b, a = signal.butter(3,f0)
        z = signal.filtfilt(b,a,y,axis=axis)
        return z

    def movingAverage(self,data,num2mean=5,ratio=1):
        x = np.exp(np.arange(num2mean))
        window = (x / np.sum(x))
    #     window = np.ones(num2mean)/num2mean
        ynew1 = np.convolve(data, window, 'same')
        ynew1[:num2mean] = data[:num2mean]
        ynew2 = np.convolve(data[::-1], window, 'same')
        ynew2[:num2mean] = data[::-1][:num2mean]
        ynew = (ynew1+ynew2[::-1])/2
        return ynew

    def resample(self,x,y,num=1001):
        down = len(x)
        up = num
        x_new = np.linspace(min(x),max(x),up)
        z = signal.resample_poly(y,up,down)
        return x_new, z

    def findPeaks(self,y,width=None,f0=0.015,h=0.15,threshold=None,prominence=None,plateau_size=None,rel_height=0):
        detrend = np.mean(y - signal.detrend(y))
        # mask = y > (np.max(y)+np.min(y))/2
        z = y if np.max(y)-detrend>detrend-np.min(y) else -y
        background = self.smooth(z,f0=f0)
        height0 = (np.max(z)-np.min(z))
        height = (background+h*height0,background+(1+h)*height0)
        threshold = threshold if threshold == None else threshold*height0
        property_peaks = signal.find_peaks(z,height=height,threshold=threshold,plateau_size=plateau_size)
        index = property_peaks[0]
        half_widths = signal.peak_widths(z,index,rel_height=rel_height)
        print(index,half_widths[0])
        # side = (index+int(half_widths[0]), index-int(half_widths[0]))
        side = 0
        prominence = signal.peak_prominences(z,index)
        return index, side, prominence
    
    def spectrum(self,x,y,method='normal',window='boxcar',detrend='constant',axis=-1,scaling='density',average='mean',shift=True):
        '''
        scaling:
            'density':power spectral density V**2/Hz
            'spcetrum': power spectrum V**2
        '''
        fs = (len(x)-1)/(np.max(x)-np.min(x))
        if method == 'normal':
            f, Pxx = signal.periodogram(y,fs,window=window,detrend=detrend,axis=axis,scaling=scaling)
        if method == 'welch':
            f, Pxx = signal.welch(y,fs,window=window,detrend=detrend,axis=axis,scaling=scaling,average=average)
        f, Pxx = (np.fft.fftshift(f), np.fft.fftshift(Pxx)) if shift else (f, Pxx)
        index = np.argmax(Pxx,axis=axis)
        w = f[index]
        return w, f, Pxx
    
    def cross_psd(self,x,y,z,window='hann',detrend='constant',scaling='density',axis=-1,average='mean'):
        fs = (len(x)-1)/(np.max(x)-np.min(x))
        f, Pxy = signal.csd(y,z,fs,window=window,detrend=detrend,scaling=scaling,axis=axis,average=average)
        return f, Pxy
    
    def ftspectrum(self,x,y,window='hann',detrend='constant',scaling='density',axis=-1,mode='psd'):
        '''
        mode:
            'psd':
            'complex':==stft
            'magnitude':==abs(stft)
            'angle':with unwrapping
            'phase':without unwraping
        '''
        fs = (len(x)-1)/(np.max(x)-np.min(x))
        f, t, Sxx = signal.spectrigram(y,fs,window=window,detrend=detrend,scaling=scaling,axis=axis,mode=mode)
        return f, t, Sxx
    
    def stft(self,x,y,window='hann',detrend=False,axis=-1,boundary='zeros',padded=True,nperseg=256):
        '''
        boundary:you can choose ['even','odd','constant','zeros',None]
        padded: True Or False          
        '''
        fs = (len(x)-1)/(np.max(x)-np.min(x))
        f, t, Zxx = signal.stft(y,fs,window=window,detrend=detrend,axis=axis,boundary=boundary,padded=padded,nperseg=nperseg)
        return f, t, Zxx
     
    def istft(self,x,Zxx,window='hann',boundary=True,time_axis=-1,freq_axis=-2):
        fs = (len(x)-1)/(np.max(x)-np.min(x))
        t, y = signal.stft(Zxx,fs,window=window,boundary=boundary,time_axis=time_axis,freq_axis=freq_axis)
        return t, y


    def fourier(self,x,y,axis=-1,shift=True):
        y = signal.detrend(y,axis=axis,type='constant')
        sample = (np.max(x) - np.min(x))/(len(x) - 1)
        # sample = 100
        # if shift:
        #     yt  = np.fft.rfftshift(np.fft.rfftfreq(np.shape(y)[axis])) / sample
        #     amp = np.fft.rfftshift(np.fft.rfft(y,axis=axis))
        # else:
        yt  = np.fft.rfftfreq(np.shape(y)[axis],sample)
        amp = np.fft.rfft(y,axis=axis)
        w = np.abs(yt[np.argmax(np.abs(amp),axis=axis)])
        # w = self.firstMax(yt,np.abs(amp),peakpercent=0.8)
        return w, yt, np.abs(amp)
        
    def envelope(self,y,responsetime=100):
        mold, out, rc = 0, [], responsetime
        out.append(np.abs(y[0]))
        for j, i in enumerate(y[1:],start=1):
            i = np.abs(i)
            if i > out[j-1]:
                mold = i
            else:
                mold = (out[j-1] * rc)/(rc + 1)
            out.append(mold)
        return out

    def envelope_Hilbert(self,y,axis=0):
        ym = signal.detrend(y,type='constant',axis=axis)
        yh = signal.hilbert(ym,axis=axis) 
        out = np.abs(ym + 1j*yh) + y.mean()
        return out

    def freq_Hilbert(self,x,y,axis=0):
        ym = signal.detrend(y,type='constant',axis=axis)
        yh = signal.hilbert(ym,axis=axis) 
        phase = np.unwrap(np.angle(ym+1j*yh))
        res, func = self.poly(x,phase,1)
        w = res[0]
        return w, phase, func

    def profile(self,v,f,s,peak,axis=1,classify=False):
        if classify:
            index = np.argwhere(np.abs(s)>peak)
            v = v[index[:,0]]
            f = f[index[:,1]]
        else:
            if axis == 1:
                v = v[np.abs(s).max(axis=1)>peak]
                s = s[np.abs(s).max(axis=1)>peak]
                f = f[np.abs(s).argmax(axis=1)]
            if axis == 0:
                f = f[np.abs(s).max(axis=0)>peak]
                s = s[:,np.abs(s).max(axis=0)>peak]
                v = v[np.abs(s).argmax(axis=0)]
        return v, f

    def profile1(self,v,f,s,peak,axis=1,classify=False):
        
        v = v[np.abs(s).max(axis=1)>peak]
        s = s[np.abs(s).max(axis=1)>peak]
        f = f[np.abs(s).argmax(axis=1)]
        if axis == 0:
            f = f[np.abs(s).max(axis=0)>peak]
            s = s[:,np.abs(s).max(axis=0)>peak]
            v = v[np.abs(s).argmax(axis=0)]
        return v, f

    def poly(self,x,y,num=1):
        z = np.polyfit(x, y, num)
        func = np.poly1d(z)
        return z, func

################################################################################
### 拟合Exp函数
################################################################################

class Exp_Fit(RowToRipe):
    
    def __init__(self,funcname=None):
        self.funcname = funcname

    def func(self,x,paras):

        if self.funcname == 'gauss':
            A, B, T1, T2 = paras
            return A * np.exp(-T2*x**2-x*T1) + B 
        else:
            A, B, T1 = paras
            return A * np.exp(-x*T1) + B 
    
    def errExp(self,paras, x, y):
        
        if self.funcname == 'gauss':
            return np.sum((self.func(x,paras) - y)**2)
        else:
            return np.sum((self.func(x,paras) - y)**2)

    def guessExp(self,x,y):
        ymin = y.min()
        y = y-y.min()
        mask = y > 0.05*y.max()
        if self.funcname == 'gauss':
            a = np.polyfit(x[mask], np.log(y[mask]), 2)
            return [np.exp(a[2]), ymin, -a[1], -a[0]]
        else:
            a = np.polyfit(x[mask], np.log(y[mask]), 1)
            return [np.exp(a[1]), ymin, -a[0]]

    def fitExp(self,x,y):
        p0 = self.guessExp(x,y)
        # res = ls(self.errExp, p0, args=(x, y)) 
        res = bh(self.errExp,p0,niter = 500,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y)}) 
        return res, self.func
func_willBeused = {'Expfunc':Exp_Fit().func}
################################################################################
### 拟合Gaussian函数
################################################################################

class Gaussian_Fit(RowToRipe):
    
    def __init__(self):
        pass

    def func(self,x,paras):
        A, B, sigma, mu = paras
        return A/sigma/np.sqrt(2*np.pi)*np.exp(-(x-mu)**2/2/sigma**2) + B

    def errGaussian(self,paras, x, y,weight):
        return np.sum(weight*(self.func(x,paras) - y)**2)

    def errGaussian_ls(self,paras, x, y,weight):
        return weight*(self.func(x,paras) - y)

    def guessGaussian(self,x,y):
        background = np.mean(y - signal.detrend(y,type='constant'))
        height = (np.max(y)+np.min(y))/2
        B = y.min()
        mu = np.mean(x[y>height]) if y[len(y)//2] > background else np.mean(x[y<height])
        sigma = (np.max(x[y>height]) - np.min(x[y>height])) if y[len(y)//2] > background else (np.max(x[y<height]) - np.min(x[y<height])) 
        A = (np.max(y)-np.min(y))*sigma*np.sqrt(2*np.pi) if y[len(y)//2] > background else -(np.max(y)-np.min(y))*sigma*np.sqrt(2*np.pi)
        return [A, B, sigma,mu]

    def fitGaussian(self,x_old,y_old,correct=False):
        l = len(y_old)
        reslst, cost = [], []
        for i in [0,l//6,-l//6]:
            x , y = (x_old[i:], y_old[i:]) if i >=0 else (x_old[:i], y_old[:i])
            for ratio in [1,-1]:
                A, B, sigma, mu = self.guessGaussian(x,y)
                # weight = (self.func(x,(A,0,sigma,mu))/np.max(self.func(x,(A,0,sigma,mu))))**10
                weight = 1
                A *= ratio
                p0 = A, B, sigma, mu
                # print(p0)
                # mybounds = MyBounds(xmin=[-10,-10,-np.inf,-np.inf,-np.inf,-np.inf],xmax=[10,10,-np.inf,-np.inf,-np.inf,-np.inf])
                res = bh(self.errGaussian,p0,niter = 200,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y,weight)})    
                reslst.append(res)
                cost.append(res.fun)
        index = np.argmin(cost)
        if correct:
            res = ls(self.errGaussian_ls,reslst[index].x,args=(x_old, y_old,weight))
            return res, self.func
        else:
            return reslst[index], self.func

################################################################################
### 拟合双Gaussian函数
################################################################################

class Gaussian2_Fit(RowToRipe):
    
    def __init__(self):
        pass

    def func(self,x,paras):
        amp, mu, sigma = paras
        return np.sum(amp*np.exp(-(x[:,None]-mu)/2/sigma**2),axis=-1)

    def errGaussian(self,paras, x, y,weight):
        return np.sum(weight*(self.func(x,paras) - y)**2)

    def errGaussian_ls(self,paras, x, y,weight):
        return weight*(self.func(x,paras) - y)

    def guessGaussian(self,x,y):
        background = np.mean(y - signal.detrend(y,type='constant'))
        height = (np.max(y)+np.min(y))/2
        B = y.min()
        mu = np.mean(x[y>height]) if y[len(y)//2] > background else np.mean(x[y<height])
        sigma = (np.max(x[y>height]) - np.min(x[y>height])) if y[len(y)//2] > background else (np.max(x[y<height]) - np.min(x[y<height])) 
        A = (np.max(y)-np.min(y))*sigma*np.sqrt(2*np.pi) if y[len(y)//2] > background else -(np.max(y)-np.min(y))*sigma*np.sqrt(2*np.pi)
        return [A, B, sigma,mu]

    def fitGaussian(self,x_old,y_old,correct=False):
        l = len(y_old)
        reslst, cost = [], []
        for i in [0,l//6,-l//6]:
            x , y = (x_old[i:], y_old[i:]) if i >=0 else (x_old[:i], y_old[:i])
            for ratio in [1,-1]:
                A, B, sigma, mu = self.guessGaussian(x,y)
                # weight = (self.func(x,(A,0,sigma,mu))/np.max(self.func(x,(A,0,sigma,mu))))**10
                weight = 1
                A *= ratio
                p0 = A, B, sigma, mu
                # print(p0)
                # mybounds = MyBounds(xmin=[-10,-10,-np.inf,-np.inf,-np.inf,-np.inf],xmax=[10,10,-np.inf,-np.inf,-np.inf,-np.inf])
                res = bh(self.errGaussian,p0,niter = 200,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y,weight)})    
                reslst.append(res)
                cost.append(res.fun)
        index = np.argmin(cost)
        if correct:
            res = ls(self.errGaussian_ls,reslst[index].x,args=(x_old, y_old,weight))
            return res, self.func
        else:
            return reslst[index], self.func

################################################################################
### 拟合Cos函数
################################################################################

class Cos_Fit(RowToRipe):

    def __init__(self,phi=None):
        self.phi = phi
        pass

    def func(self,x,paras):
        A,C,W,phi = paras  
        return A*np.cos(2*np.pi*W*x+phi)+C

    def errCos(self,paras,x,y,kind):      
        if kind == 'bh':       
            return  np.sum((self.func(x,paras)-y)**2)  
        if kind == 'ls':
            return self.func(x,paras) - y

    def guessCos(self,x,y):
        x, y = np.array(x), np.array(y)
        # sample = (np.max(x) - np.min(x))/(len(x) - 1)
        Ag, Cg= np.abs(y-np.mean(y)).max(), np.mean(y) 
        # yt  = np.fft.fftshift(np.fft.fftfreq(len(y))) / sample
        # amp = np.fft.fftshift(np.fft.fft(y))
        Wg,yt,amp = RowToRipe().fourier(x, y)
        z = np.abs(amp[yt!=0])
        ytz = yt[yt!=0]
        # Wg = np.abs(ytz[np.argmax(z)])
        phig =  np.mean(np.arccos((y - Cg)/Ag) - 2*np.pi*Wg*x) % (2*np.pi)
        return Ag, Cg, Wg, 0

    def fitCos(self,volt,s):
        x, y = volt, s
        if x[0] / 1e9 > 1:
            raise 'I hate the large number, please divided by 1e9, processing x in GHz'
        Ag, Cg, Wg, phig = self.guessCos(x,y)
        phig = phig if self.phi is None else self.phi
        p0 = Ag, Cg, Wg, phig
        # print(Ag, Cg, Wg, phig)
        # res = ls(self.errCos, [Ag,Cg,Wg,phig], args=(x, y)) 
        mybounds = MyBounds(xmin=[-np.inf,-np.inf,0,-np.pi],xmax=[np.inf,np.inf,1.5*Wg,np.pi])    
        res = bh(self.errCos,p0,niter=80,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y,'bh')},accept_test=mybounds)   
        res = ls(self.errCos, res.x, args=(x, y,'ls')) 

        return res, self.func

################################################################################
### 拟合洛伦兹函数
################################################################################

class Lorentz_Fit(RowToRipe):
    '''
    I hate the large number
    processing x in GHz
    '''
    def __init__(self):
        pass

    def func(self,x,paras):
        a,b,c,d = paras
        return a/(1.0+c*(x-b)**2)+d

    def errLorentz(self,paras,x,y):
        return np.sum((self.func(x,paras)-y)**2)

    def guessLorentz(self,x,y):
        # index, prominences, widths = self.findPeaks(y)
        z = np.sort(np.abs(y))
        d = np.mean(z[:int(len(z)/2)])
        y = np.abs(y)- d
        b = x[np.abs(y).argmax()]
        # b1, b = x[index]
        bw = (np.max(x[y>0.5*(np.max(y)-np.min(y))])-np.min(x[y>0.5*(np.max(y)-np.min(y))]))/2
        # bw1, bw = widths
        a = np.abs(y).max()
        # a1, a = prominences
        c = 1 / bw**2
        return a,b,c,d

    def fitLorentz(self,x,y):
        if x[0] / 1e9 > 1:
            raise 'I hate the large number, please divided by 1e9, processing x in GHz'
        para = self.guessLorentz(x,y)
        # mybounds = MyBounds(xmin=[-np.inf,-np.inf,-np.inf,-np.inf,0,0],xmax=[np.inf,np.inf,np.inf,np.inf,1.5*w,2*np.pi])    
        res = bh(self.errLorentz,para,niter=20,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y)})
        # res = ls(self.errLorentz,para,args=(x,y))
        a,b,c,d = res.x
        return res,self.func,np.sqrt(np.abs(1/c))*2e3

################################################################################
### 拟合T1
################################################################################

class T1_Fit():
    "A, T1"
    def __init__(self,T1_limt=100e3):
        self.T1_limt = T1_limt
    
    def func(self,x,paras):
        A, T1,B = paras
        f = A * np.exp(-x/T1) +B
        return f

    def errT1(self,paras, x, y):
        return np.sum((self.func(x,paras) - y)**2)

    def errT1_ls(self,paras, x, y):
        return self.func(x,paras) - y

    def errT1_cf(self,x,A, T1,B):
        paras = A, T1,B
        return self.func(x,paras) 

    def guessT1(self,x,y):
        y = y/y.max()
        y = RowToRipe().smooth(y,f0=0.25)
        B = y.min()
        y = y-y.min()
        # mask = y > y.min()
        a = np.polyfit(x, np.log(y), 1)
        T1 = np.abs(1/a[0]) if np.abs(1/a[0]) < self.T1_limt else 0.99*self.T1_limt
        A = np.exp(a[1]) if np.exp(a[1]) > 0.95 and np.exp(a[1])<1.1 else 1
        # A, T1, B = 1,x[np.abs(y-np.exp(-1))<0.1][0], 0
        return [A, T1,B]

    def fitT1(self,x,y,s=None):
        """[fit T1 or 2d-T1]

        Args:
            x ([1d-array]): [if s is None,x is time, else voltage or frequency of qubit in 2d-T1]
            y ([1d-array]): [if s is None,y is population of |1>, else time in 2d-T1]
            s ([2d-array]): [population of |1>]. Defaults to None.

        Returns:
            [res, func]: [if s is None]
            [res_lst]: [if s is not None]
        """
        if s is None:
            p0 = self.guessT1(x,y)
            print(p0)
            mybounds = MyBounds(xmin=[0.95,0,0],xmax=[1.1,self.T1_limt,0.25])    
            res = bh(self.errT1,p0,niter = 50,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y)},accept_test=mybounds) 
            return res,self.func,0
            # res = ls(self.errT1_ls,p0,args=(x,y))
            # popt,pcov = curve_fit(self.errT1_cf,x,y,p0,bounds=([0.95,0,0],[1.1,self.T1_limt,0.25]))
            # return popt, self.func, np.sqrt(np.diag(pcov))
        else:
            T1_lst = []
            pcov_lst = []
            for i in range(len(x)):
                p0 = self.guessT1(y,s[i,:])
                mybounds = MyBounds(xmin=[0.95,0,0],xmax=[1.1,self.T1_limt,0.25])    
                res = bh(self.errT1,p0,niter = 50,minimizer_kwargs={"method":"Nelder-Mead","args":(y,s[i,:])},accept_test=mybounds) 
                T1_lst.append(res.x[1])
                pcov_lst.append(res.fun)
                # res = ls(self.errT1_ls,p0,args=(y,s[i,:]))
                # popt,pcov = curve_fit(self.errT1_cf,y,s[i,:],p0,bounds=([0.95,0,0],[1.1,self.T1_limt,0.25]))
                # T1_lst.append(popt[1])
                # pcov_lst.append(np.sqrt(np.diag(pcov)))
            return T1_lst, pcov_lst

################################################################################
### 拟合指数包络函数
################################################################################

class T2_Fit(Exp_Fit,Cos_Fit):
    '''
    #############
    example:
    import imp
    import optimize
    op = imp.reload(optimize)
    try: 
        fT2 = op.T2_Fit(funcname='gauss',envelopemethod='hilbert')
        A,B,T1,T2,w,phi = fT2.fitT2(t,y)
    finally:
        pass
    ##############
    '''
    def __init__(self,responsetime=100,T1=35000,phi=0,funcname=None,envelopemethod=None):
        Exp_Fit.__init__(self,funcname)
        self.responsetime = responsetime
        self.T1 = T1
        self.phi = phi
        self.envelopemethod = envelopemethod
    
    def guessT2(self,x,y_new,y):
 
        res, _ = self.fitExp(x[5:-5],y_new[5:-5])
        A, B, T1, T2 = res.x
        T1 = 1 / T1 / 2
        if np.abs(self.T1-T1)>5000:
            T1 = self.T1
        Ag, Cg, Wg, phig = self.guessCos(x,y)
        return A, B, T1, np.sqrt(np.abs(1/T2)), Wg, phig

    def func_T2(self,x,para):
        A,B,T1,T2,w,phi = para
        return A*np.exp(-(x/T2)**2-x/T1/2)*np.cos(2*np.pi*w*x+phi) + B

    def errT2(self,para,x,y):
        return np.sum((self.func_T2(x,para) - y)**2)

    def fitT2(self,x,y):
        '''
        几个参数的限制范围还需要考究，A，T1，T2
        '''
        d = self.space(y)
        if self.envelopemethod == 'hilbert':
            out = self.envelope_Hilbert(y)
        else:
            out = self.envelope(y)
        A,B,T1,T2,w,phi = self.guessT2(x,out,y)
        env = A,B,T1,T2,out
        if T2 > 0.8*x[d-1] and d < 0.8*len(y):
            T2 = 0.37*x[d-1]
        amp = (np.max(y)-np.min(y)) / 2
        A = A if np.abs(A-amp) < 0.1*amp else amp
        p0 = A,B,T1,T2,w,self.phi
        print(p0)
        # res = ls(self.errT2, p0, args=(x, y)) 
        mybounds = MyBounds(xmin=[0,-np.inf,0,0,0,-np.pi],xmax=[np.inf,np.inf,100000,100000,1.5*w,np.pi])    
        res = bh(self.errT2,p0,niter = 80,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y)},accept_test=mybounds)     
        A,B,T1,T2,w,phi = res.x
        return res, self.func_T2

class T2Envelope_Fit(Exp_Fit,Cos_Fit):
    '''
    #############
    example:
    import imp
    import optimize
    op = imp.reload(optimize)
    try: 
        fT2 = op.T2_Fit(funcname='gauss',envelopemethod='hilbert')
        A,B,T1,T2,w,phi = fT2.fitT2(t,y)
    finally:
        pass
    ##############
    '''
    def __init__(self,funcname=None):
        Exp_Fit.__init__(self,funcname)
    
    def guessT2Envelope(self,x,y):
 
        res, _ = self.fitExp(x,y)
        A, B, T1, T2 = res.x
        T1 = 1 / T1 / 2
        return A, B, T1, np.sqrt(np.abs(1/T2))

    def func_T2Envelope(self,x,para):
        A,B,T1,T2 = para
        return A*np.exp(-(x/T2)**2-x/T1/2) + B

    def errT2Envelope(self,para,x,y):
        return np.sum((self.func_T2Envelope(x,para) - y)**2)

    def fitT2Envelope(self,x,y):
        '''
        几个参数的限制范围还需要考究，A，T1，T2
        '''
        A,B,T1,T2 = self.guessT2Envelope(x,y)
        # env = A,B,T1,T2,out
        # if T2 > 0.8*x[d-1] and d < 0.8*len(y):
        #     T2 = 0.37*x[d-1]
        # amp = (np.max(y)-np.min(y)) / 2
        # A = A if np.abs(A-amp) < 0.1*amp else amp
        p0 = A,B,T1,T2
        print(p0)
        # res = ls(self.errT2, p0, args=(x, y)) 
        mybounds = MyBounds(xmin=[0,-np.inf,0,0],xmax=[np.inf,np.inf,100000,100000])    
        res = bh(self.errT2Envelope,p0,niter = 80,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y)},accept_test=mybounds)     
        A,B,T1,T2 = res.x
        return res, self.func_T2Envelope

class Rabi_Fit(T2_Fit):

    def __init__(self,responsetime=100,T1=20000,phi=np.pi/2,funcname=None,envelopemethod=None):
        T2_Fit.__init__(self,responsetime,T1,phi,funcname,envelopemethod)
        
    
    def guessRabi(self,x,y_new,y):
 
        res, _ = self.fitExp(x[5:-5],y_new[5:-5])
        A, B, T1 = res
        T1 = 1 / T1
        if np.abs(self.T1-T1)>5000:
            T1 = self.T1
        Ag, Cg, Wg, phig = self.guessCos(x,y)
        return A, B, T1, Wg, phig

    def errRabi(self,para,x,y):
        A,B,T1,w,phi = para
        return np.sum((A*np.exp(-x/T1)*np.cos(2*np.pi*w*x+phi) + B - y)**2)

    def fitRabi(self,x,y):
        if self.envelopemethod == 'hilbert':
            out = self.envelope_Hilbert(y)
        else:
            out = self.envelope(y)
        A,B,T1,w,phi = self.guessRabi(x,out,y)
        env = (A,B,T1,out)
        amp = (np.max(y)-np.min(y)) / 2
        A = A if np.abs(A-amp) < 0.1*amp else amp
        B = B if np.abs(B-np.mean(y)) < 0.1*np.mean(y) else np.mean(y)
        p0 = A,B,T1,w,self.phi
        print(p0)
        # res = ls(self.errRabi, p0, args=(np.array(x), np.array(y)))   
        mybounds = MyBounds(xmin=[0,-np.inf,100,0,0],xmax=[np.inf,np.inf,100e3,1.5*w,2*np.pi])
        res = bh(self.errRabi,p0,niter=30,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y)},accept_test=mybounds)      
        A,B,T1,w,phi = res.x
        return A,B,T1,w,phi,env

################################################################################
### 拟合二维谱
################################################################################

class Spec2d_Fit(Cos_Fit):

    def __init__(self,peak=15,threshold=0.001):
        Cos_Fit.__init__(self,phi=None)
        self.peak = peak
        self.threshold = threshold
    
    def profile(self,v,f,s,classify=False):
        if classify:
            index = np.argwhere(s>self.peak)
            v = v[index[:,0]]
            f = f[index[:,1]]
        else:
            v = v[s.max(axis=1)>self.peak]
            # s = s[s.max(axis=1)>self.peak]
            # f = f[s.argmax(axis=1)]
            idx = s > self.peak
            f = [f[i][-1] for i in idx if np.any(i) == True]
        return v, np.array(f)
    def func_f01(self,x,paras):
        voffset, vperiod, ejs, ec, d = paras
        tmp = np.pi*(x-voffset)/vperiod
        f01 = np.sqrt(8*ejs*ec*np.abs(np.cos(tmp))*np.sqrt(1+d**2*np.tan(tmp)**2))-ec
        return f01
    def err(self,paras,x,y):
        # A, C, w, phi = paras
        # f01 = np.sqrt(A*np.abs(np.cos(w*x+phi))) + C
        f01 = self.func_f01(x,paras)
        return np.sum((f01 - y)**2)

    def fitSpec2d(self,v,f,s=None,classify=False):
        if s is not None:
            v,f = self.profile(v,f,s,classify)
            # print(list(v),list(f))
        paras, func = self.fitCos(v,f)
        A, C, W, phi = paras.x
        try:
            voffset = self.firstMax(v,f,num=0)[0]
        except:
            voffset  =  v[np.argmax(f)]
        vperiod, ec, d = 1/W, 0.2, 0.5
        ejs = (np.max(f)+ec)**2/8/ec
        p0 = [voffset, vperiod,ejs,ec,d]
        res, func = self.poly(v,f,2)
        space = np.abs(func(v)-f)
        if np.max(space) > self.threshold:
            # print(space)
            v = v[space<self.threshold]
            f = f[space<self.threshold]

        while 1:
            print(p0)
            # print(list(v),list(f))
            mybounds = MyBounds(xmin=[0.5*voffset,0,0,0,0],xmax=[1.5*voffset,1.5*vperiod,2*ejs,2*ec,1000])
            res = bh(self.err,p0,niter = 200,minimizer_kwargs={"method":"Nelder-Mead","args":(v, f)},accept_test=mybounds) 
            # res = ls(self.err,res.x,args=(v, f)) 
            voffset, vperiod, ejs, ec, d = res.x
            space = self.errspace(self.func_f01,res.x,{'x':v,'y':f})
            if np.max(space) > self.threshold:
                # print(space)
                v = v[space<self.threshold]
                f = f[space<self.threshold]
                p0 = res.x
                # print(len(v),(space<0.001))
            else:
                return f, v, res, self.func_f01
        # return f, v, voffset, vperiod, ejs, ec, d

################################################################################
### 拟合腔频调制曲线
################################################################################

class Cavitymodulation_Fit(Spec2d_Fit):

    def __init__(self,peak=15,phi=None):
        Cos_Fit.__init__(self,phi=phi)
        self.peak = peak

    def func_s(self,x,paras):
        voffset, vperiod, ejs, ec, d, g, fc = paras
        tmp = np.pi*(x-voffset)/vperiod
        f01 = np.sqrt(8*ejs*ec*np.abs(np.cos(tmp))*np.sqrt(1+d**2*np.tan(tmp)**2))-ec
        fr = (fc+f01+np.sqrt(4*g**2+(f01-fc)**2))/2
        # fr = fc - g**2/(f01-fc)
        return fr

    def err(self,paras,x,y):
        return np.sum((self.func_s(x,paras) - y)**2)

    def fitCavitymodulation(self,v,f,s,classify=False):
        v,f = self.manipulation(v,f,s)
        paras, func = self.fitCos(v,f)
        A, C, W, phi = paras.x
        voffset, vperiod, ec, d= self.firstMax(v,f,num=0), 1/W, 0.1*np.min(f), 1
        # g = np.min(f)-fc
        ejs = (np.max(f)+ec)**2/8/ec
        g, fc = ec, np.mean(f)
        p0 = [voffset, vperiod, ejs, ec, d, g, fc]
        print(p0)
        mybounds = MyBounds(xmin=[-0.25*vperiod,0,0,0,0,0,0],xmax=[0.25*vperiod,1.5*vperiod,2*ejs,2*ec,2,2*g,2*fc])
        res = bh(self.err,p0,niter = 200,minimizer_kwargs={"method":"Nelder-Mead","args":(v, f)},accept_test=mybounds)
        # res = ls(self.err,res.x,args=(v, f)) 
        # A, C, W, phi = res.x
        voffset, vperiod, ejs, ec, d, g, fc = res.x
        return f, v, res, self.func_s

################################################################################
### crosstalk直线拟合
################################################################################

class Crosstalk_Fit(Spec2d_Fit):

    def __init__(self,peak=15):
        self.peak = peak

    def two_line(self,f,v):
        fv = []
        for i,j in enumerate(f):
            fv.append([j,v[i]])
        fv = sorted(fv)
        ff = sorted(list(Counter(f).keys()))
        F = [0]*len(ff)
        for i,j in enumerate(ff):
            F_m=[]
            for k,l in enumerate(fv):
                if j==l[0]:
                    F_m.append(l[1])
            F[i]=sorted(F_m )

            
        FF_1 = [0]*len(F)
        FF_2 = [0]*len(F)
        FF_m = [0]*len(F)
        for k,i in enumerate(F):
            F_1 = []
            F_2 = []
            for j in i:
                if j<i[-1]-0.05:
                    F_2.append(j)
                else:
                    F_1.append(j)
            if len(F_2)==len(i):
                FF_m[k]=F_2.copy()
                F_2 = []
            if len(F_1)==len(i):
                FF_m[k]=F_1.copy()
                F_1 = []
                
            FF_1[k] = F_1
            FF_2[k] = F_2

        vm=[]
        for j, i in enumerate(FF_m):
            if i==0:
                vm.append(j)

        FF_m1 = (FF_m[:vm[0]])
        v_m1 = (ff[:vm[0]])
        FF_m2 = (FF_m[vm[-1]+1:])
        v_m2 = (ff[vm[-1]+1:])
                
        c1=[]
        v1=[]
        for j, i in enumerate(FF_1):
            c1+=len(i)*[1*ff[j]]
            v1+=i
            
        c2=[]
        v2=[]
        for j, i in enumerate(FF_2):
            c2+=len(i)*[1*ff[j]]
            v2+=i


        cm1=[]
        vm1=[]
        for j, i in enumerate(FF_m1):
            cm1+=len(i)*[1*v_m1[j]]
            vm1+=i
            
        cm2=[]
        vm2=[]
        for j, i in enumerate(FF_m2):
            cm2+=len(i)*[1*v_m2[j]]
            vm2+=i


        p1 = np.array([np.polyfit(c1, v1 ,1)[1],np.polyfit(c2, v2 ,1)[1]])-np.polyfit(cm1, vm1 ,1)[1]
        p2 = np.array([np.polyfit(c1, v1 ,1)[1],np.polyfit(c2, v2 ,1)[1]])-np.polyfit(cm2, vm2 ,1)[1]

        if abs(p2[1])<abs(p2[0]):
            v2+=vm2
            c2+=cm2
        if abs(p2[1])>abs(p2[0]):
            v1+=vm2
            c1+=cm2

        if abs(p1[1])<abs(p1[0]):
            v2+=vm1
            c2+=cm1
        if abs(p1[1])>abs(p1[0]):
            v1+=vm1
            c1+=cm1
        return v1,c1,v2,c2
        
    def fitCrosstalk(self,v,f,s,classify=False):
        v,f = self.profile(v,f,s,classify)
        res = np.polyfit(f,v,1)
        return v, f, res

################################################################################
### 单比特tomo
################################################################################

def pTorho(plist):
    pz_list, px_list, py_list = plist
    rho_list = []
    for i in range(np.shape(pz_list)[0]):
        pop_z, pop_x, pop_y = pz_list.T[i], px_list.T[i], py_list.T[i]
        rho_00, rho_01 = 1 - pop_z, (2*pop_x - 2j*pop_y - 1 + 1j) / 2j
        rho_10, rho_11 = (1 + 1j - 2*pop_x - 2j*pop_y) / 2j, pop_z
        rho = np.array([[rho_00,rho_01],[rho_10,rho_11]])
        rho_list.append(rho)
    pass

################################################################################
### RB
################################################################################

class RB_Fit:
    def __init__(self):
        pass
    def func_rb(self,x,paras):
        A,B,p = paras
        return A*p**x+B
    def err(self,paras,x,y):
        return self.func_rb(x,paras)-y
    def guess(self,x,y):
        B = np.min(y)
        y = y - np.min(y)
        mask = y > 0
        a = np.polyfit(x[mask], np.log(y[mask]), 1)
        return np.exp(np.abs(a[1])), B, 1/np.exp(np.abs(a[0]))
    def fitRB(self,x,y):
        p0 = self.guess(x,y)
        res = ls(self.err, p0, args=(x, y)) 
        A,B,p = res.x
        return res, self.func_rb

################################################################################
### 双指数拟合
################################################################################

# class TwoExp_Fit(Exp_Fit):
#     def __init__(self,funcname=None,percent=0.2):
#         Exp_Fit.__init__(self,funcname)
#         self.percent = percent
#     def err(self,paras,x,y):
#         a, b, c, d, e = paras
#         return np.sum((a*np.exp(b*x) + c*np.exp(d*x) + e - y)**2)
#     def guess(self,x,y):
#         a,e,b = self.fitExp(x,y)
#         b *= -1
#         e = np.min(y) if a > 0 else np.max(y)
#         return a,b,a*self.percent,b*self.percent,e
#     def fitTwoexp(self,x,y):
#         p0 = self.guess(x,y)
#         a, b, c, d, e = p0
#         lower = [0.95*i if i > 0 else 1.05*i for i in p0]
#         higher = [1.05*i if i > 0 else 0.95*i for i in p0]
#         lower[2], lower[3] = -np.abs(a)*self.percent, -np.abs(b)*self.percent
#         higher[2], higher[3] = self.percent*np.abs(a), self.percent*np.abs(b)
#         print(p0)
#         # res = ls(self.err,p0,args=(x,y),bounds=(lower,higher))
#         res = bh(self.err,p0,niter = 50,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y)})

#         return res.x

class TwoExp_Fit(Exp_Fit):
    def __init__(self,funcname=None,percent=0.2):
        Exp_Fit.__init__(self,funcname)
        self.percent = percent
    def fitfunc(self,x,p):
        return (p[0] + np.sum(p[1::2,None]*np.exp(-p[2::2,None]*x[None,:]), axis=0))
    def err(self,paras,x,y):
        return np.sum(((self.fitfunc(x,paras) - y)*(1.0+0.5*scipy.special.erf(0.4*(x-paras[2])))**5)**2)
    def guess(self,x,y,paras):
        offset = np.min(y)
        alist = np.max(y) - np.min(y)
        blist = np.max(x)-np.min(x)
        paras[0] = offset
        paras[1::2] = alist
        paras[2::2] = 1/blist
        return paras
    def fitTwoexp(self,x,y,num=2):
        paras = np.zeros((2*num+1,))
        xmin, xmax = np.zeros((2*num+1,)), np.zeros((2*num+1,))
        p0 = self.guess(x,y,paras)
        xmin[0], xmax[0] = p0[0]*0.5, p0[0]*1.5
        xmin[1::2], xmin[2::2] = p0[1::2]*0.5, -(np.max(x)-np.min(x))*2
        xmax[1::2], xmax[2::2] = p0[1::2]*1.5, (np.max(x)-np.min(x))*2
        mybounds = MyBounds(xmin=xmin,xmax=xmax)
        res = bh(self.err,p0,niter = 50,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y)})
        # res = bh(self.err,res.x,niter = 50,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y)},accept_test=mybounds)
        p0 = res.x
        print(xmin)
        # res = ls(self.err, p0, args=(np.array(x), np.array(y)))  
        return res.x

################################################################################
## 误差函数拟合
################################################################################

class Erf_fit(RowToRipe):
    def __init__(self):
        RowToRipe.__init__(self)
    def func(self,x,paras):
        sigma1, sigma2, center1, center2, a, b = paras
        return a*(scipy.special.erf((x-center1)/sigma1)+np.abs(scipy.special.erf((x-center2)/sigma2)-1))+b
    def err(self,paras,x,y):
        return np.sum((y-self.func(x,paras))**2)
    def guess(self,x,y):
        height = np.max(y) - np.min(y)
        mask = x[y < (np.max(y)+np.min(y))/2]
        center1, center2 = mask[-1], mask[0]
        b = np.mean(y - signal.detrend(y,type='constant'))
        a = (np.max(y) - np.min(y)) if y[len(y)//2] < np.mean(y) else -(np.max(y) - np.min(y))
        z, ynew = x[(np.min(y)+0.1*height)<y], y[(np.min(y)+0.1*height)<y]
        z = z[ynew<(np.max(ynew)-0.2*height)]
        sigma2 = (z[z<np.mean(z)][-1]-z[z<np.mean(z)][0])
        sigma1 = (z[z>np.mean(z)][-1]-z[z>np.mean(z)][0])
        return sigma1, sigma2, center1, center2, a, b
    def fitErf(self,x,y):
        l = len(y)
        reslst, cost = [], []
        for i in [0,l//6,-l//6]:
            x , y = (x[i:], y[i:]) if i >=0 else (x[:i], y[:i])
            for ratio in [1,-1]:
                sigma1, sigma2, center1, center2, a, b = self.guess(x,y)
                a *= ratio
                paras = sigma1, sigma2, center1, center2, a, b
                print(paras)
                # mybounds = MyBounds(xmin=[-10,-10,-np.inf,-np.inf,-np.inf,-np.inf],xmax=[10,10,-np.inf,-np.inf,-np.inf,-np.inf])
                res = bh(self.err,paras,niter = 100,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y)}) 
                reslst.append(res)
                cost.append(res.fun)
        index = np.argmin(cost)
        return reslst[index], self.func

################################################################################
## 拟合单个误差函数
################################################################################

class singleErf_fit(RowToRipe):
    def __init__(self):
        RowToRipe.__init__(self)
    def func(self,x,paras):
        sigma1, center1, a, b = paras
        return a*scipy.special.erf((x-center1)/sigma1)+b
    def err(self,paras,x,y):
        return np.sum((y-self.func(x,paras))**2)
    def guess(self,x,y):
        mask = x[y < y.mean()]
        center1 = mask[-1]
        b = np.mean(y - signal.detrend(y))
        a = np.max(y) - np.min(y)
        z = np.abs(y - np.mean(y))
        xnew = x[z<(np.max(z)+np.min(z))/2]
        sigma1 = xnew[-1] - xnew[0]
        return sigma1, center1, a, b
    def fitErf(self,x,y):
        l = len(y)
        reslst, cost = [], []
        for i in [0,l//6,-l//6]:
            x , y = (x[i:], y[i:]) if i >=0 else (x[:i], y[:i])
            for ratio in [1,-1]:
                sigma1, center1, a, b = self.guess(x,y)
                a *= ratio
                paras = sigma1, center1, a, b
                # print(paras)
                res = bh(self.err,paras,niter = 100,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y)}) 
                reslst.append(res)
                cost.append(res.fun)
        index = np.argmin(cost)
        return reslst[index], self.func

################################################################################
## 拟合圆
################################################################################

class Circle_Fit():
    def __init__(self):
        pass
    def func(self,paras):
        xc, yc, R = paras
        theta = np.linspace(0,2*np.pi,1001)
        x = R*np.cos(theta) + xc
        y = R*np.sin(theta) + yc
        return x, y
    def errfunc(self,paras,x,y):
        xc, yc, R = paras
        return (x - xc)**2 + (y - yc)**2 - R**2
    def guess(self,x,y):
        xc = (np.max(x)+np.min(x))/2
        yc = (np.max(y)+np.min(y))/2
        R = np.sqrt((x-xc)**2+(y-yc)**2)
        return xc, yc, np.mean(R)
    def fitCircle(self,x,y):
        p0 = self.guess(x,y)
        res = ls(self.errfunc,p0,args=(x,y)) 
        return res, self.func

################################################################################
## 拟合贝塞尔函数绝对值
################################################################################

class Bessel_fit(RowToRipe):
    def __init__(self):
        RowToRipe.__init__(self)
    def func(self,x,paras):
        alpha, a = paras
        return a*np.abs(scipy.special.jv(0,alpha*x))
    def err(self,paras,x,y,kind='bh'):
        if kind == 'bh':
            return np.sum((y-self.func(x,paras))**2)
        if kind == 'ls':
            return y-self.func(x,paras)
    def guess(self,x,y):
        b = np.min(y)
        a = np.max(y)
        alpha = 2.4048/x[np.argmin(y)]
        return alpha, a
    def fitBessel(self,x,y):

        paras = self.guess(x,y)
        print(paras)
        # res = bh(self.err,paras,niter = 100,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y)}) 
        # return res, self.func
        while 1:
            # print(p0)
            res = bh(self.err,paras,niter = 100,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y,'bh')}) 
            res = ls(self.err,res.x,args=(x,y,'ls')) 
            # space = self.errspace(self.func,res.x,{'x':x,'y':y})
            # if np.max(space) > 0.001:
            #     x = x[space<0.001]
            #     y = y[space<0.001]
            #     paras = res.x
                # print(len(v),(space<0.001))
            # else:
            return res, self.func

################################################################################
## 拟合zPulse核函数
################################################################################

# class zKernel_fit(RowToRipe):
#     def __init__(self,timeconstants =0,polyNum = 17,tCut = 90,height = 0.9,sigma = 0.4,tstart = 0,tshift = 0,polyRatio = 1,expNum = 1,tCut1 = 0):
#         self.polyNum = 17 #10  polyNum阶多项式拟合
#         self.expNum = 1 #######################目前固定为1,多项式拟合时的指数
#         self.timeconstants =0 # expNum阶指数拟合
#         self.tCut = 90#100 ,200  polyNUm的拟合范围
#         self.tCut1 = 0
#         self.tshift = 0
#         # self.height = eval(tags[1])
#         self.height = 0.9

#         self.polyRatio = 1
#         self.sigma = 0.4
#         self.tstart = 0

#     def fitfunc(t, p):
#         return (t >= 0) *(p[0] + np.sum(p[1::2,None]*np.exp(-p[2::2,None]*t[None,:]), axis=0))
#     def errfunc(p):
#         return (fitfunc(data[:,0], p) - data[:,1])*(1.0+0.5*scipy.special.erf(0.4*(data[:,0]-tCut)))**5

#     p0 = np.zeros(2*timeconstants+1)
#     p0[1::2] = -np.linspace(0, 0.02, timeconstants)
#     p0[2::2] = np.linspace(0, 0.5, timeconstants)
#     # print(p0)
#     p, _ = scipy.optimize.leastsq(errfunc,p0,maxfev=5000)
#     ts = np.arange(0,data[-1,0]*5,0.02)
#     p[0] = 0

#     plt.figure()
#     plt.subplot(211)
#     plt.plot(data[:,0],data[:,1],'bo')
#     plt.plot(ts,fitfunc(ts,p),'k-')

#     data1 = np.copy(data)
#     restData = data[:,1]-fitfunc(data[:,0], p)
#     restData = restData[data1[:,0]<=tCut]
#     data1 = data1[data1[:,0]<=tCut,:]
#     def fitfunc1(t, p):
#         pExp = p[:expNum*2]
#         pPoly = p[expNum*2:]
#         if np.iterable(t):
#             return np.sum(pExp[0::2,None]*np.exp(-pExp[1::2,None]*t[None,:]), axis=0)*np.polyval(pPoly,t)*(t<=tCut+20)
#         else:
#             return np.sum(pExp[0::2]*np.exp(-pExp[1::2]*t))*np.polyval(pPoly,t)*(t<=tCut)
#     def errfunc1(p):
#         return (fitfunc1(data1[:,0], p) - restData)
#     def smoothFuncATtCut(ts,tCut,tshift):    
#         return (0.5-0.5*scipy.special.erf(sigma*(ts-tCut+tshift)))*(0.5+0.5*scipy.special.erf(4.0*(ts-data[0,0]+0.5)))
#     pExp0 = np.zeros(2*expNum)
#     pExp0[1::2] = np.linspace(0.001, 0.03, expNum)
#     pPoly0 = np.zeros(polyNum)
#     pPoly0[-1] = 1.0
#     pAll0 = np.hstack([pExp0,pPoly0])
#     p2, _ = scipy.optimize.leastsq(errfunc1, pAll0)
#     smoothData = fitfunc1(ts,p2)*smoothFuncATtCut(ts,tCut,tshift)*polyRatio
#     timeFunData0 = smoothData+fitfunc(ts,p)
#     paras= {'p':p,'p2':p2,'tCut':tCut,'tshift':tshift,'sigma':sigma}
#     plt.subplot(212)
#     plt.plot(data1[:,0],restData,'bo')
#     # plt.plot(ts,smoothData,'r-')
#     plt.plot(ts,fitfunc1(ts,p2))
#     plt.xlabel('Time (ns)')
#     plt.grid(True)
#     plt.subplot(211)
#     plt.plot(ts,timeFunData0,'r-')
#     plt.grid(True)
#     p2 = np.asarray(p2)
#     p = np.asarray(p)
#     p_uniform = np.copy(p)
#     p2_uniform = np.copy(p2)
#     p_uniform[1::2] = p_uniform[1::2]/height
#     pExp = p2_uniform[:expNum*2]
#     pPoly = p2_uniform[expNum*2:]
#     pExp[0::2] = pExp[0::2]/height*polyRatio
#     p2_uniform[:expNum*2] = pExp

################################################################################
## 真空拉比拟合
################################################################################

class Vcrabi_fit():
    def __init__(self,length=None):
        self.length = length
    def func(self,x,paras):
        g, A0, Z0 = paras
        return np.sqrt(4*(g)**2+A0**2*(x-Z0)**2)
    def err(self,paras,x,y):
        return np.sum((self.func(x,paras)-y)**2)
    def guess(self,x,y):
        Z0 = x[np.argmin(y)]
        g = np.min(y)/2
        x, y = x[x!=Z0], y[x!=Z0]
        A0 = np.mean(np.sqrt(y**2-4*(g)**2)/(x-Z0))
        return g, A0, Z0
    def fitVcrabi(self,x,y):
        if self.length is None:
            p0 = self.guess(x,y)
            mybounds = MyBounds(xmin=[0,0,-1.1],xmax=[0.1,np.inf,1.1])
            res = bh(self.err,p0,niter=100,minimizer_kwargs={"method":"Nelder-Mead","args":(x, y)},accept_test=mybounds)
            return res, self.func
        else:
            index = len(y)//2
            start, end = index-self.length, index+self.length
            x0, y0 = x[start:end], y[start:end]
            p0 = self.guess(x0,y0)
            mybounds = MyBounds(xmin=[0,0,-1.1],xmax=[0.1,np.inf,1.1])
            res = bh(self.err,p0,niter=100,minimizer_kwargs={"method":"Nelder-Mead","args":(x0, y0)},accept_test=mybounds)
            
            space = np.abs(y-self.func(x,res.x)) < 0.1*np.abs(self.func(x,res.x))
            x0, y0 = x[space], y[space]
            p0 = self.guess(x0,y0)
            mybounds = MyBounds(xmin=[0,0,-1.1],xmax=[0.1,np.inf,1.1])
            res = bh(self.err,p0,niter=100,minimizer_kwargs={"method":"Nelder-Mead","args":(x0, y0)},accept_test=mybounds)
            return res, self.func

################################################################################
## 拟合Q值
################################################################################

class Cavity_fit(RowToRipe):
    def __init__(self):
        pass

    def circleLeastFit(self,x, y):
        def circle_err(params, x, y):
            xc, yc, R = params
            return (x - xc)**2 + (y - yc)**2 - R**2

        p0 = [
            x.mean(),
            y.mean(),
            np.sqrt(((x - x.mean())**2 + (y - y.mean())**2).mean())
        ]
        res = ls(circle_err, p0, args=(x, y))
        return res.x

    def guessParams(self,x,s):
        
        y = np.abs(1 / s)
        f0 = x[y.argmax()]
        _bw = x[y > 0.5 * (y.max() + y.min())]
        FWHM = np.max(_bw) - np.min(_bw)
        Qi = f0 / FWHM
        _, _, R = self.circleLeastFit(np.real(1 / s), np.imag(1 / s))
        Qe = Qi / (2 * R)
        QL = 1 / (1 / Qi + 1 / Qe)

        return [f0, Qi, Qe, 0, QL]

    def invS21(self, f, f0, Qi, Qe, phi):
        #QL = 1/(1/Qi+1/Qe)
        return 1 + (Qi / Qe * np.exp(1j * phi)) / (
            1 + 2j * Qi * (np.abs(f) / np.abs(f0) - 1))
    
    def err(self,params,f,s21):
        f0, Qi, Qe, phi = params
        y = np.abs(s21) - np.abs(self.invS21(f, f0, Qi, Qe, phi) )
        return np.sum(np.abs(y)**2)

    def fitCavity(self,x,y):
        f, s = self.deductPhase(x,y)
        s = s[0]/np.max(np.abs(s[0]))
        f0, Qi, Qe, phi, QL = self.guessParams(f,s)
        res = bh(self.err,(f0, Qi, Qe, phi),niter = 100,\
            minimizer_kwargs={"method":"Nelder-Mead","args":(f, 1/s)}) 
        f0, Qi, Qe, phi = res.x
        QL = 1 / (1 / Qi + 1 / Qe)
        return f0, Qi, Qe, QL, phi, f, s

def amp_opt(y,s,radio=0.5):
    s0=[]
    s1=[]
    for i in range(len(s)):
        s1 = (s[i]>(np.max(s[i])*radio+np.min(s[i])*(1-radio)))
        if i ==0:
            s0 = (s[i]>(np.max(s[i])*radio+np.min(s[i])*(1-radio))) 
        if list(s0)!=list(s1):
            for i,j in enumerate(s0):
                if j==False:
                    s1[i]=j
        s0=s1
    val = []
    indexs=[]
    for i,j in enumerate(s0):
        if j:
            val.append(y[i])
            indexs.append(i)
    indexw = np.argmax([np.mean(s[:,i]) for i in indexs])
    return y[indexs[indexw]]

    

def run_points(s0,si,idx=0,radio=0.5):
    s1 = (si>(np.max(si)*radio+np.min(si)*(1-radio)))
    if idx ==0:
        s0 = (si>(np.max(si)*radio+np.min(si)*(1-radio))) 
    if list(s0)!=list(s1):
        for n,j in enumerate(s1):
            if j==False:
                s0[n]=j
    return s0

################################################################################
## 执行拟合
################################################################################

def exeFit(measure,title,data,args):
    qname = measure.qubitToread
    # num = measure.qubitToread.index(q_target[0])
    qubits = measure.qubits
    if title == 'S21':
        f_s21, s_s21 = data[0], np.abs(data[1])
        fig, axes = plt.subplots(ncols=2,nrows=1,figsize=(9,4))
        axes[0].plot(f_s21,20*np.log10(np.abs(s_s21)))
        axes[0].vlines(measure.f_lo+measure.delta,np.max(20*np.log10(np.abs(s_s21))),np.min(20*np.log10(np.abs(s_s21))),'r')
        axes[1].vlines(measure.f_lo+measure.delta,np.max(np.angle(s_s21)),np.min(np.angle(s_s21)),'r')
        axes[1].plot(f_s21,np.angle(s_s21))
        plt.show()
    
    if title == 'singlespec':
        f_ss, s_ss = data[0], np.abs(data[1])
        # x,y= f_ss, s_ss
        x, y =f_ss, np.abs( signal.detrend(np.abs(s_ss),axis=0))
        index = np.abs(y).argmax(axis=0)
        f_rabi = np.array([x[:,i][j] for i, j in enumerate(index)])
        peak = np.array([y[:,i][j] for i, j in enumerate(index)])
        plt.figure()
        plt.plot(x,np.abs(y),'-')
        plt.plot(np.array(f_rabi).flatten(),np.array(peak).flatten(),'o')
        plt.title(qname[0]+f',f_ex={np.around(f_rabi/1e9,3)}')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((qname[0],'_',title))))
        plt.close()
        return {j: {'f_ex':f_rabi[i]} for i, j in enumerate(qname)}

    if title == 'T1':
        exstates = args['exstate'][0]
        nums = [measure.qubitToread.index(i) for i in exstates]
        t_t,s_t = data
        T1s = []
        fig, axes = plt.subplots(ncols=2,nrows=1,figsize=(9,4))
        # for num in range(np.shape(s_t)[1]):
        for num in nums:
            res, func = Exp_Fit().fitExp(t_t[:,num],np.abs(s_t[:,num]))
            A, B, T1 = res.x
            T1s.append(T1)
            # A, B, T1 = op.T1_Fit().fitT1(t_t[:,num],np.abs(s_t[:,num]))
            z = A * np.exp(-t_t[:,num]*T1) + B
            axes[0].plot(t_t,np.abs(s_t),'o',markersize=2)
            axes[0].plot(t_t[:,0],z)
        axes[0].set_title('$T1=%.1fus$'%(1/T1/1000))
        axes[1].plot(t_t,np.angle(s_t))
        plt.show()
        return {j: {'T1':T1s[i]} for i, j in enumerate(exstates)}

    # if title == 'rabi':
    #     v_rp,s_rp = data
    #     fig, axes = plt.subplots(ncols=2,nrows=1,figsize=(9,3))
    #     t_op = []
    #     for i in range(np.shape(s_rp)[1]):
    #         x, y = v_rp[:,i], np.abs(s_rp[:,i])
    #         t_op.append(RowToRipe().firstMax(x,y,num=0,peakpercent=0.8))
    #         A,B,T1,w,phi,out = Rabi_Fit(envelopemethod='hilbert',phi=0).fitRabi(np.abs(x),np.abs(y))
    #         z = A*np.exp(-x/T1)*np.cos(2*np.pi*w*x+phi) + B
    #         env = A*np.exp(-x/T1) + B
    #         axes[0].plot(x,y,'-o',markersize=3)
    #         axes[0].plot(x,z)
    #         axes[0].plot(x,env)
    #         axes[0].set_title(f'pi={t_op}mv')
    #     plt.show()
    #     plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((qname[0],'_',title))))
    #     return {j: {'amp':t_op[i]} for i, j in enumerate(qname)}

    # if title == 'ramsey':
    #     x, y = t_ram[:,num], np.abs(s_ram[:,num])
    #     res, func = T2_Fit(T1=10000,funcname='gauss',envelopemethod='hilbert').fitT2(x,np.abs(y))
    #     A,B,T1,T2,w,phi = res.x

    #     z = func(x,res.x)
    #     z_env = A*np.exp(-(x/T2)**2-x/T1/2) + B
    #     # w,yt,amp = op.RowToRipe().fourier(x,y)
    #     fig, axes = plt.subplots(ncols=2,nrows=1,figsize=(9,3))
    #     axes[0].plot(t_ram,np.abs(s_ram),'-o',markersize=3)
    #     axes[0].plot(x,z)
    #     axes[0].plot(x,z_env)
    #     axes[0].set_title('$T_{2}^{*}=%.2fns,\omega=%.2fMHz$'%(T2,w*1e3))
    #     # axes[1].plot(yt[yt!=0],np.abs(amp[yt!=0]))
    #     plt.show()
    #     q_target = measure.qubits[q_target[0]]
    #     A_W.append([q_target.f_ex,w*1e9-measure.qubits[q_target.q_name].detune])

    #     if len(A_W)>1:
    #         A_W = sorted(A_W,key=lambda sublist: abs(sublist[1]))
    #         if len(A_W)>2:
    #             A_W.pop()
    #         q_target.f_ex = np.polyfit(np.array(A_W)[:,1],np.array(A_W)[:,0],1)[1]
    #     else:
    #         q_target.f_ex = q_target.f_ex + (w*1e9-q_target.detune)
    #     print(q_target.f_ex)

    if title == 'specbias_awg':
        f_ss, s_ss = data[0], np.abs(data[1])
        index = np.abs(s_ss).argmax(axis=0)
        x,y= f_ss, s_ss
        f_rabi = np.array([x[:,i][j] for i, j in enumerate(index)])
        peak = np.array([y[:,i][j] for i, j in enumerate(index)])
        z, band = [], []
        for i in range(np.shape(s_ss)[1]):
            res,func, e = Lorentz_Fit().fitLorentz(x[:,i],np.abs(y[:,i]))
            a,b,c,d = res.x
            b = b if np.abs(b-f_rabi[i])<0.001 else f_rabi[i]
            band.append(b)
            z.append(func(x[:,i],res.x))
        z = np.array(z).T
        
        plt.figure()
        plt.plot(x,np.abs(y),'-o',markersize=2)
        plt.plot(x,z)
        plt.plot(np.array(f_rabi).flatten(),np.array(peak).flatten(),'ro')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((qname[0],'_',title))))
        plt.close()
        return {j: {'volt':band[i]} for i, j in enumerate(qname)}

    if title == 'rabi':
        qubitparas = {}
        q_target = args['exstate'][0]
        readnum = qname.index(q_target)

        v_rp, s_rp = data[0], np.abs(data[1])
        s_rp = np.abs(s_rp-s_rp[0,:])
        t_op, t_fit, peak = [], [], []
        y_smooth = []
        for i in range(np.shape(s_rp)[1]):
            x, y = v_rp[:,i], np.abs(s_rp[:,i])
            y0 = RowToRipe().smooth(y,f0=0.25)
            y_smooth.append(y0)
            t = RowToRipe().firstMax(x,y0,num=0,peakpercent=0.8)
            # w,yt,amp = RowToRipe().fourier(x,y0)
            # t = 0.5/w 
            peak.append(dtl.nearest(x,t,y)[1])
            t_op.append(t)
        plt.figure()
        plt.plot(v_rp,s_rp,'-')
        plt.plot(v_rp,np.array(y_smooth).T,'-')
        plt.plot(t_op,peak,'o')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((q_target,'_',title))))
        plt.close()
        qubitparas[q_target] = {'amp':t_op[readnum]}
        return qubitparas

    if title == 'Ramsey':
        qubitparas = {}
        q_target = args['exstate'][0]
        readnum = qname.index(q_target)
        t_ram, s_ram = data[0], np.abs(data[1])
        x, y = t_ram[:,readnum], s_ram[:,readnum]
        res, func = T2_Fit(T1=10000,funcname='gauss',envelopemethod='hilbert').fitT2(x,np.abs(y))
        A,B,T1,T2,w,phi = res.x
        z = func(x,res.x)
        z_env = A*np.exp(-(x/T2)**2-x/T1/2) + B
        w_f,yt,amp = RowToRipe().fourier(x,y)
        w = w if np.abs(w-w_f)<0.5e6 else w_f
        fig, axes = plt.subplots(ncols=2,nrows=1,figsize=(9,3))
        axes[0].plot(t_ram,np.abs(s_ram),'-o',markersize=3)
        axes[0].plot(x,z)
        axes[0].plot(x,z_env)
        axes[0].set_title('$T_{2}^{*}=%.2fns,\omega=%.2fMHz$'%(T2,w*1e3))
        axes[0].set_ylim(-0.1,1.1)
        axes[1].plot(yt[yt!=0],np.abs(amp[yt!=0]))
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((q_target,'_',title))))
        plt.close()
        f_ex = qubits[q_target].f_ex -w*1e9+qubits[q_target].detune
        qubitparas[q_target] = {'f_ex':f_ex}
        return qubitparas

    if title == 'singleZpulse':
        qubit = measure.qubits[qname[0]]
        t_shift, s_z = data
        plt.figure()
        for i in range(np.shape(s_z)[1]):
            x, y = t_shift[:,i], np.abs(s_z[:,i])
            func = scipy.interpolate.interp1d(x,y)
            x = np.linspace(min(x),max(x),1001)
            y = func(x)
            y0 = RowToRipe().smooth(y,f0=0.2)
            res, func = Erf_fit().fitErf(x, y0)
            paras = res.x
            loc = (paras[2]+paras[3])/2
            plt.plot(x,y,'-o',markersize=3)
            plt.plot(x,func(x,paras))
            plt.vlines(loc,np.min(y),np.max(y)) 
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((qname[0],'_',title))))
        plt.close()
        zbigxy = loc-1000
        qubit.timing['z>xy'] = (zbigxy*1e-9)
        return {j: {'timing':qubit.timing} for i, j in enumerate(qname)}


    if title == 'XYZ_timing':
        q_target = args['exstate'][0]   ###yhs
        readnum = qname.index(q_target)
        qubit = measure.qubits[qname[readnum]]    ##zsk

        # qubit = measure.qubits[qname[0]]    ##zsk
        t_shift, s_z = data
        
        plt.figure()
        for i in range(np.shape(s_z)[1]):
            if i==readnum:
                x, y = t_shift[:,i], np.abs(s_z[:,i])
                func = scipy.interpolate.interp1d(x,y)
                x = np.linspace(min(x),max(x),501)
                y = func(x)
                y0 = RowToRipe().smooth(y,f0=0.15)
                res, func = Erf_fit().fitErf(x, y0)
                paras = res.x
                loc = (paras[2]+paras[3])/2
                plt.plot(x,y,'-o',markersize=3)
                plt.plot(x,func(x,paras))
                plt.vlines(loc,np.min(y),np.max(y)) 
            
        # plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((qname[0],'_',title))))  ##zsk
        plt.title(f'Q%d:z>xy={(loc-1000*0)*1e-9}'%(qubit.index+1))
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((qname[readnum],'_',title))))  ##yhs
        plt.close()
        zbigxy = loc-1000*0
        qubit.timing['z>xy'] = (zbigxy*1e-9)
        # return {j: {'timing':qubit.timing} for i, j in enumerate(qname)}    ##zsk
        QT={j: {'timing':measure.qubits[j].timing} for i, j in enumerate(qname)}
        # print(QT)
        return QT    ##yhs

    if title == 'qqTiming':
        qubit = measure.qubits[args['dcstate'][0]]
        readnum = measure.qubitToread.index(args['dcstate'][0])
        t_shift, s_z = data
        plt.figure()
        loc, cost = [], []
        for i in range(np.shape(s_z)[1]):
            if i in [readnum,readnum-1]:
                x, y = t_shift[:,i], np.abs(s_z[:,i])
                func = scipy.interpolate.interp1d(x,y)
                x = np.linspace(min(x),max(x),201)
                y = func(x)
                y0 = RowToRipe().smooth(y,f0=0.2)
                res, func = Erf_fit().fitErf(x, y0)
                paras = res.x
                loc.append((paras[2]+paras[3])/2)
                # res, func = Gaussian_Fit().fitGaussian(x, y0)
                # paras = res.x
                # loc.append((paras[-1]))
                cost.append(res.fun)
                plt.plot(x,y,'-o',markersize=3)
                plt.plot(x,func(x,paras))
        plt.vlines(loc,[np.min(y)]*2,[np.max(y)]*2)
        loc = loc[np.argmin(cost)]
        plt.vlines(loc,np.min(y),np.max(y),color='r')
        plt.title(f'Q%d:read>xy={(loc-1000)*1e-9}'%(qubit.index+1))
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((args['dcstate'][0],'_',title))))
        plt.close()
        zbigxy = loc - 1000
        qubit.timing['read>xy'] -= (zbigxy*1e-9)
        return {j: {'timing':qubit.timing} for i, j in enumerate(args['dcstate'])}

    if title == 'iswap_optzpa_pop':
        qubit = measure.qubits[args['exstate'][0]]
        readnum = measure.qubitToread.index(args['exstate'][0])
        v, fid = data

        x = v[:,0]
        y = fid[:,readnum,0]
        res, f = Gaussian_Fit().fitGaussian(x,y)
        plt.figure()
        plt.plot(x,y,'-o')
        plt.plot(x,f(x,res.x))
        plt.vlines(res.x[-1],np.min(y),np.max(y))

        plt.title(f'{qubit.q_name}.volt_swap={res.x[-1]}')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((args['exstate'][0],'_',title,'_',str(args['nf'])))))
        plt.close()

        return {j: {'volt_swap':res.x[-1]} for i, j in enumerate(args['exstate'])}

    if title == 'iswap_optduring_pop':
        qubit = measure.qubits[args['exstate'][0]]
        q_dc = measure.qubits[args['zname'][0]]
        readnum = measure.qubitToread.index(args['exstate'][0])
        t, fid = data

        x = t[:,2]
        dur = []
        y = fid[:,readnum,0]
        ynew = RowToRipe().smooth(y,f0=0.25)
        dur = x[np.argmax(ynew)]

        plt.figure()
        plt.plot(x,y,'-o')
        plt.plot(x,ynew)
        plt.vlines(dur,np.min(y),np.max(y))

        plt.title(f'during_swap={dur*1e9}ns')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((args['exstate'][0],'_',args['zname'][0],'_',title,'-',str(args['nf'])))))
        plt.close()

        return {j: {'during_swap':dur} for i, j in enumerate(args['exstate']+args['zname'])}

    if title == 'coordinatePhase':
        qubit = measure.qubits[args['exstate'][0]]
        readnum = measure.qubitToread.index(args['exstate'][0])
        phi,pop = data

        p = pop
        phi_new = np.linspace(np.min(phi),np.max(phi),1001)
        res1, f1 = Cos_Fit(phi=np.pi/2).fitCos(phi[:,0],p[:,1])
        res2, f2 = Cos_Fit(phi=0).fitCos(phi[:,0],p[:,2])
        index = scipy.signal.argrelmin(np.abs(f1(phi_new,res1.x)-f2(phi_new,res2.x)))[0][0]
        
        plt.figure()
        plt.plot(phi[:,0],p[:,0])
        plt.plot(phi[:,0],p[:,1])
        plt.plot(phi[:,0],p[:,2])
        plt.plot(phi[:,0],p[:,3])
        plt.plot(phi_new,f1(phi_new,res1.x))
        plt.plot(phi_new,f2(phi_new,res2.x))
        plt.plot(phi_new[index],f2(phi_new,res2.x)[index],'ro')
        plt.title(f'phi={phi_new[index]}')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((args['exstate'][0],'_',args['zname'][0],'_',title,'_',str(args['nf'])))))
        plt.close()

        measure.qubits[args['zname'][0]].coordinatePhase += phi_new[index]
        print(measure.qubits[args['zname'][0]].q_name,measure.qubits[args['zname'][0]].coordinatePhase)
        print(measure.qubits[args['exstate'][0]].q_name,measure.qubits[args['exstate'][0]].coordinatePhase)

        return {args['zname'][0]: {'coordinatePhase':measure.qubits[args['zname'][0]].coordinatePhase}}

    if title == 'T1_2d_coupling':
        # vv, tv, sv = data
        # plt.figure()
        # for i in range(np.shape(s_z)[1]):
        #     x, y, s = vv[:,i], tv[0,:,i], np.abs(sv[:,:,i]).T
        #     extent = [min(x),max(x),min(y),max(y)]
        #     plt.imshow(s,extent=extent,aspect='auto',origin='lower')
        # plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((args['exstate'][0],'_',title))))
        # plt.close()
        return {}

    if title == 'coupling_2d':
        # vv, tv, sv = data
        # plt.figure()
        # for i in range(np.shape(s_z)[1]):
        #     x, y, s = vv[:,i], tv[0,:,i], np.abs(sv[:,:,i]).T
        #     extent = [min(x),max(x),min(y),max(y)]
        #     plt.imshow(s,extent=extent,aspect='auto',origin='lower')
        # plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((args['exstate'][0],'_',title))))
        # plt.close()
        return {}

    if title == 'T1_2d':
        q_target = args['exstate'][0]
        # print(q_target,data)
        readnum = qname.index(q_target)
        vv, tv, sv = data
        x = tv[0,:,readnum]
        T1 = []
        # for i in range(len(vv[:,0])):
        #     y = np.abs(sv[i,:,readnum])
        #     res, func = T1_Fit().fitT1(x,y)
        #     T1.append(res.x[1])
        plt.figure()
        extent = [np.min(vv),np.max(vv),np.min(x),np.max(x)]
        plt.imshow(np.abs(sv[:,:,readnum]).T,extent=extent,aspect='auto',origin='lower',cmap='jet')
        # plt.plot(vv[:,0],T1,'ro',markersize=2)
        plt.ylim(0,40e3)
        # plt.hlines(np.mean(T1),np.min(vv),np.max(vv))
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((q_target,'_',title))))
        plt.close()
        return {}

    if title == 'spec2d_awg1':
        q_target = args['exstate'][0]
        # print(q_target,data)
        readnum = qname.index(q_target)
        vv, tv, sv = data

        x = sy.Symbol('x',real=True)

        v, f, s = vv[:,0], tv[0,:,readnum]/1e9, np.abs(sv[:,:,readnum])
        peak = (np.max(np.abs(s))+np.min(np.abs(s))) / 4

        f, v, res, func = Spec2d_Fit(peak=peak).fitSpec2d(v,f,np.abs(s),classify=False)
        voffset, vperiod, ejs, ec, d = res.x
        v1 = np.linspace((min(v)-np.abs((max(v)-min(v))/2)),(max(v)+np.abs((max(v)-min(v))/2)),1001)
        tmp = np.pi*(v1-voffset)/vperiod
        z = np.sqrt(8*ejs*ec*np.abs(np.cos(tmp))*np.sqrt(1+d**2*np.tan(tmp)**2))-ec
        tmp_s = np.pi*(x-voffset)/vperiod
        y = sy.sqrt(8*ejs*ec*sy.Abs(sy.cos(tmp_s))*sy.sqrt(1+d**2*sy.tan(tmp_s)**2))-ec
        specfuncz = [y,voffset, vperiod, ejs, ec, d]

        plt.figure()
        extent = [np.min(vv),np.max(vv),np.min(tv/1e9),np.max(tv/1e9)]
        plt.imshow(np.abs(sv[:,:,readnum]).T,extent=extent,aspect='auto',origin='lower',cmap='jet')
        plt.scatter(v,f,marker='.',c='',edgecolors='m')
        plt.plot(v1,z,'y--')
        plt.hlines(np.max(z),np.max(v),np.min(v),'w',label=f'w_max={round(np.max(z),3)}GHz')
        plt.legend(loc='best')
        plt.title(q_target+':%s'%(round(voffset,4)))

        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((q_target,'_',title))))
        plt.close()
        return {q_target:{'specfuncz':specfuncz}}

    if title == 'singleVrabi':
        vv, sv = data
        # qubit_z = measure.qubits[args['dcstate'][0]]
        # num = eval(qubit_z.q_name[1:])-1
        # v_big.append(vv[:,num][np.argmax(np.abs(sv[:,num]))])
        num_z = qname.index(args['dcstate'][0])
        num_ex = qname.index(args['exstate'][0])
        loc, cost = [], []
        for m in [num_ex,num_z]:
            x, y = vv[:,m], np.abs(sv[:,m])
            func = scipy.interpolate.interp1d(x,y)
            x = np.linspace(min(x),max(x),1001)
            y = func(x)
            y0 = RowToRipe().smooth(y,f0=0.2)
            res, func = Gaussian_Fit().fitGaussian(x, y0)
            paras = res.x
            loc.append((paras[-1]))
            cost.append(res.fun)
            plt.plot(x,y,'-o',markersize=3)
            plt.plot(x,func(x,paras))
        volt_op = loc[np.argmin(cost)]
        # v_mean.append(volt_op)
        plt.vlines(loc,[np.min(y)]*2,[np.max(y)]*2)
        plt.vlines(volt_op,np.min(y),np.max(y),color='r')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((args['dcstate'][0],args['exstate'][0],'_','singleVrabi'))))
        plt.close()

    if title == 'optDragalpha':
        q_target = args['exstate'][0]
        readnum = qname.index(q_target)

        x, y = data[0][:,0], data[1][:,readnum,0]
        xnew = np.linspace(min(x),max(x),1001)
        y0 = RowToRipe().smooth(y,f0=0.2)
        res, f = Cos_Fit(phi=None).fitCos(x,y0)
        drag_op = RowToRipe().firstMax(xnew,f(xnew,res.x),num=0,peakpercent=0.8,insitu=True)
        plt.figure()
        plt.plot(x,y)
        plt.plot(xnew,f(xnew,res.x))
        plt.plot(drag_op,f(drag_op,res.x),'ro')
        plt.title(f'drag={drag_op}')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((q_target,'_',title))))
        plt.close()
        return {q_target:{'DRAGScaling':drag_op/(measure.qubits[q_target].alpha*2*np.pi)}}

    if title == 'pipulseOpt' :
        q_target = args['exstate'][0]
        readnum = qname.index(q_target)

        x, y, s = data[0][:,readnum], data[1][0,:,readnum], np.abs(data[2][:,:,readnum])
        xnew = y
        volt = []
        for j,i in enumerate(range(len(x))):
            y0 = RowToRipe().smooth(s[i,:],f0=0.2)
            #     res, f = op.Cos_Fit(phi=None).fitCos(y,y0)
            if j == 0:
                res, f = Cos_Fit(phi=None).fitCos(y,y0)
                v = xnew[np.argmax(f(xnew,res.x))]
                vtarget = v
            else:
                v = RowToRipe().firstMax(xnew,y0,num=vtarget,peakpercent=0.8,insitu=False,mean=False)
                v = v if np.abs(v-vtarget)<=0.1*vtarget else vtarget
            volt.append(v)
        # volt = [amp_opt(y,s)]
        plt.figure()
        extent = [min(y),max(y),min(x),max(x)]
        plt.imshow(s,origin='lower',aspect='auto',extent=extent)
        # plt.plot(volt,x,'ro')
        plt.vlines(np.mean(volt),min(x),max(x))
        plt.title(q_target+':'+f'amp={np.mean(volt)}')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((q_target,'_',title))))
        plt.close()
        return {q_target:{args['optwhich']:np.mean(volt)}}

    
    if title == 'pipulseOpt_select' :
        q_target = args['exstate'][0]
        readnum = qname.index(q_target)

        x, y, s = data[0][:,readnum], data[1][0,:,readnum], np.abs(data[2][:,:,readnum])
        xnew = y
        volt = []
        for j,i in enumerate(range(len(x))):
            y0 = RowToRipe().smooth(s[i,:],f0=0.2)
            #     res, f = op.Cos_Fit(phi=None).fitCos(y,y0)
            if j == 0:
                res, f = Cos_Fit(phi=None).fitCos(y,y0)
                v = xnew[np.argmax(f(xnew,res.x))]
                vtarget = v
            else:
                v = RowToRipe().firstMax(xnew,y0,num=vtarget,peakpercent=0.8,insitu=False,mean=False)
                v = v if np.abs(v-vtarget)<=0.1*vtarget else vtarget
            volt.append(v)
        # volt = [amp_opt(y,s)]
        plt.figure()
        extent = [min(y),max(y),min(x),max(x)]
        plt.imshow(s,origin='lower',aspect='auto',extent=extent)
        # plt.plot(volt,x,'ro')
        plt.vlines(np.mean(volt),min(x),max(x))
        plt.title(q_target+':'+f'amp={np.mean(volt)}')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((q_target,'_',title))))
        plt.close()
        return {q_target:{args['optwhich']:np.mean(volt)}}

    if title == 'Dphase_lm' or title == 'Dphase11' :
        q_target = args['exstate'][0]
        tag = args['paras']
        nf = args['nf']
        readnum = qname.index(q_target)

        x, y, s = data[0][:,readnum], data[1][0,:,readnum], np.abs(data[2][:,:,readnum])
        s = RowToRipe().smooth(s,f0=0.25,axis=-1)
        xnew, ynew = RowToRipe().profile(x,y,s,peak=0.9)
        ynew = np.unwrap(ynew)
        z, func = RowToRipe().poly(xnew,ynew)

        plt.figure()
        extent = [min(x),max(x),min(y),max(y)]
        plt.imshow(s.T,origin='lower',aspect='auto',extent=extent)
        plt.plot(xnew,ynew,'mo')
        plt.plot(xnew,func(xnew),'k')

        plt.title(q_target+':'+f'{tag}_{nf}={round(-z[0]*1e3/2/np.pi,3)}MHz,w={round(args["w"]/1e6,3)}MHz')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((q_target,'_',title,'_',tag,'_',str(nf)))))
        plt.close()
        return {q_target:{tag:(-z[0]*1e9/2/np.pi-args['w'])}}


    if title == 'optDrag_delta_ex_2':
        q_target = args['exstate'][0]
        readnum = qname.index(q_target)

        x, y, s = data[0][:,readnum], data[1][0,:,readnum], np.abs(data[2][:,:,readnum])
        xnew = y
        volt = []
        for j,i in enumerate(range(len(x))):
            y0 = RowToRipe().smooth(s[i,:],f0=0.2)
            #     res, f = op.Cos_Fit(phi=None).fitCos(y,y0)
            if j == 0:
                res, f = Cos_Fit(phi=None).fitCos(y,y0)
                v = xnew[np.argmax(f(xnew,res.x))]
                vtarget = v
            else:
                v = RowToRipe().firstMax(xnew,y0,num=vtarget,peakpercent=0.8,insitu=False,mean=False)
                v = v if np.abs(v-vtarget)<=0.1*vtarget else vtarget
            volt.append(v)
        # volt = [amp_opt(y,s)]
        plt.figure()
        extent = [min(y),max(y),min(x),max(x)]
        plt.imshow(s,origin='lower',aspect='auto',extent=extent)
        # plt.plot(volt,x,'ro')
        plt.vlines(np.mean(volt),min(x),max(x))
        plt.title(q_target+':'+f'f_ex={qubits[q_target].f_ex+np.mean(volt)}')
        # plt.title(q_target+':'+f'detuning={np.mean(volt)}')
        plt.savefig(r'D:\skzhao\fig\f_ex%s.png'%(''.join((q_target,'_',title))))
        plt.close()
        # return {q_target:{'detuning':np.mean(volt)} }
        
        return {q_target:{'f_ex':qubits[q_target].f_ex+np.mean(volt),'delta_ex':qubits[q_target].delta_ex+np.mean(volt)} }


    if title == 'optDragalpha_2':
        q_target = args['exstate'][0]
        readnum = qname.index(q_target)

        x, y, s = data[0][:,readnum], data[1][0,:,readnum], np.abs(data[2][:,:,readnum])
        xnew = y
        volt = []
        for j,i in enumerate(range(len(x))):
            y0 = RowToRipe().smooth(s[i,:],f0=0.2)
            #     res, f = op.Cos_Fit(phi=None).fitCos(y,y0)
            if j == 0:
                res, f = Cos_Fit(phi=None).fitCos(y,y0)
                v = xnew[np.argmax(f(xnew,res.x))]
                vtarget = v
            else:
                v = RowToRipe().firstMax(xnew,y0,num=vtarget,peakpercent=0.8,insitu=False,mean=False)
                v = v if np.abs(v-vtarget)<=0.1*vtarget else vtarget
            volt.append(v)
        # volt = [amp_opt(y,s)]
        plt.figure()
        extent = [min(y),max(y),min(x),max(x)]
        plt.imshow(s,origin='lower',aspect='auto',extent=extent)
        # plt.plot(volt,x,'ro')
        plt.vlines(np.mean(volt),min(x),max(x))
        plt.title(q_target+':'+f'alpha={np.mean(volt)}')
        plt.savefig(r'D:\skzhao\fig\f_ex%s.png'%(''.join((q_target,'_',title))))
        plt.close()
        return {q_target:{'DRAGScaling':np.mean(volt)/(qubits[q_target].alpha*2*np.pi)} }


    if title == 'readpowerOpt':
        q_target = args['exstate'][0]
        readnum = qname.index(q_target)

        x, y = data[0][:,readnum], data[1][:,readnum]

        y0 = RowToRipe().smooth(y,f0=0.2)
        volt_op = x[np.argmax(y0)]
        plt.figure()
        plt.title(f'readamp={volt_op}')
        plt.plot(x,y)
        plt.plot(x,y0)
        plt.plot(volt_op,dtl.nearest(x,volt_op,y0)[1],'ro')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((q_target,'_',title))))
        plt.close()

        measure.readamp[readnum] = volt_op

        return {}

    if title == 'couplingCQ':
        qubitparas = {}
        q_target = args['exstate'][0]
        readnum = qname.index(q_target)
        st, f_op, s_op = data
        f, s_off, s_on = f_op[:,:,readnum][0], np.abs(s_op[:,:,readnum][0]), np.abs(s_op[:,:,readnum][1])
        f_off = f[np.argmin(np.abs(s_off))]
        f_on = f[np.argmin(np.abs(s_on))]
        chi = (f_off-f_on) / 2
        delta_cq = f_off - qubits[q_target].f_ex
        alpha = qubits[q_target].alpha
        g_cq = np.sqrt(chi*delta_cq*(1+delta_cq/alpha))

        plt.figure()
        plt.plot(f,s_off)
        plt.plot(f,s_on)
        plt.vlines(f_off,np.max(s_off),np.min(s_off),'r')
        plt.vlines(f_on,np.max(s_off),np.min(s_off),'g')
       
        plt.title(f'$chi={round(chi/1e6,5)}MHz,g={round(g_cq/1e6,3)}MHz$')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((q_target,'_',title))))
        plt.close()
        qubitparas[q_target] = {'g_cq':g_cq,'chi':chi}
        return qubitparas

    if title == 'photonNum':
        qubitparas = {}
        q_target = args['exstate'][0]
        readnum = qname.index(q_target)
        f, v, s = data[0][:,readnum], data[1][0,:,readnum], np.abs(data[2][:,:,readnum])
        f = f/1e9 if f[0]/1e9 >= 1 else f
        extent = [min(v), max(v), min(f), max(f)]
        peak = (np.max(s) + np.min(s)) / 2
        f,v = RowToRipe().profile(f,v,s,peak,axis=0)
        res, func = Exp_Fit().poly(v,f,2)
        f_fit = np.max(func(v))
        delta_cq = measure.f_lo - measure.delta[readnum] - qubits[q_target].f_ex
        g_cq, alpha = qubits[q_target].g_cq, qubits[q_target].alpha
        chi = g_cq**2/delta_cq/(1+delta_cq/alpha)
        delta_chi = chi-qubits[q_target].chi
        chi = qubits[q_target].chi
        acstark_shift = [res,(res[0]*xvar**2 + res[1]*xvar+res[2])*1e9,chi]
        photonnum_func = [res,res[0]*xvar**2*1e9/chi/(-2),chi]
        plt.figure()
        plt.imshow(s,extent=extent,origin='lower',aspect='auto',cmap='jet')
        plt.colorbar()
        plt.plot(v,f,'wo')
        plt.plot(v,func(v),'k-')
        plt.title(f'f_diff={round(np.abs(qubits[q_target].f_ex/1e9-f_fit),4)},chi={delta_chi}')

        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((q_target,'_',title))))
        plt.close()
        qubitparas[q_target] = {'photonnum_func':photonnum_func,'acstark_shift':acstark_shift}
        return qubitparas

    if title =='v2_swap':
        qname_ex = args['exstate'][0]   ###args 对应paras 字典
        qubit_z = args['qubit_z']
        qubit_ex = qubits[qname_ex]
        print(qubit_ex.q_name)
        qname_z = qubit_z.q_name
        print(qubit_z.q_name)
        num_z, num_ex = measure.qubitToread.index(qubit_z.q_name),measure.qubitToread.index(qubit_ex.q_name)
        v_offset,vv, sv = data
        v_mean, v_big = [], []
        volt_offset=0.3
        plt.figure()
        for n in [0,1]:
            loc, cost = [], []
            v_big.append(vv[n,:,num_z][np.argmax(np.abs(sv[n,:,num_z]))])
            v_big.append(vv[n,:,num_ex][np.argmin(np.abs(sv[n,:,num_ex]))])
            for m in [num_ex,num_z]:
                x, y = vv[n,:,m], np.abs(sv[n,:,m])
                func = scipy.interpolate.interp1d(x,y)
                x = np.linspace(min(x),max(x),201)
                y = func(x)
                y0 = RowToRipe().smooth(y,f0=0.2)
                res, func = Gaussian_Fit().fitGaussian(x, y0)
                paras = res.x
                loc.append((paras[-1]))
                cost.append(res.fun)
                plt.plot(x,y,'-o',markersize=3)
                plt.plot(x,func(x,paras))
            volt_op = loc[np.argmin(cost)]
            v_mean.append(volt_op)
            
        print(v_big,volt_op,v_mean)
        # if qubit_ex.index>qubit_z.index:
        #     qname_z = qubit_ex.q_name
        #     qname_ex = qubit_z.q_name

        # plt.vlines(loc,[np.min(y)]*2,[np.max(y)]*2)
        plt.vlines(v_mean,np.min(y),np.max(y),color='k')
        volt_op = np.mean(v_mean) if np.abs(np.mean(v_mean)-qubit_z.volt)<0.01 else np.mean(v_big)
        plt.vlines(volt_op,np.min(y),np.max(y),color='r')
        plt.title(qname_z+f'.volt={volt_op}')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((qname_ex,qname_z,str(volt_offset),'_','singleVrabi'))))
        plt.close()
        return {qname_z:{'volt':volt_op}}

    if title =='specbias_awg2d':
        qubit_ex = args['qubit']   ###args 对应paras 字典
        qname_ex = qubit_ex.q_name
        num_ex = measure.qubitToread.index(qubit_ex.q_name)
        v_offset,vv, sv = data
        v_mean, v_big = [], []
        plt.figure()
        for n in [0,1]:
            x, y = vv[n,:,num_ex], np.abs(sv[n,:,num_ex])
            # res,func, e = Lorentz_Fit().fitLorentz(x,np.abs(y))
            y0 = RowToRipe().smooth(y,f0=0.3)
            res, func = Gaussian_Fit().fitGaussian(x, y0)
            v_big.append((res.x[-1]))
            # v_big.append(vv[n,:,num_ex][np.argmax(np.abs(sv[n,:,num_ex]))])
            plt.plot(x,y,'-o',markersize=3)
            plt.plot(x,func(x,res.x))
        plt.vlines(v_big,np.min(y),np.max(y),color='k')
        volt_op = np.mean(v_big)
        plt.vlines(volt_op,np.min(y),np.max(y),color='r')
        plt.title(qname_ex+f'.volt={volt_op}')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((qname_ex,'_','specbias_awg2d'))))
        plt.close()
        return {qname_ex:{'volt':volt_op}}

    if title =='rabi_awg2d':
        return {}

    if title == 'threshHold':
        exstate, states = args['exstate'], args['states']
        st, s_st = data
        num = measure.n
        fig, axes = plt.subplots(ncols=2,nrows=num,figsize=(7,3*num))
        for i in range(measure.n):
            s_off, s_on= s_st[0,:,i], s_st[1,:,i]
            data = dtl.visibility(1,s_off,s_on)
            ax0 = axes[i][0] if num>1 else axes[i]
            ax0.plot(np.real(s_off),np.imag(s_off),'.')
            ax0.plot(np.real(s_on),np.imag(s_on),'.',alpha=1)
            if np.shape(s_st)[0] == 3:
                s_on2 = s_st[2,:,i]
                ax0.plot(np.real(s_on2),np.imag(s_on2),'.',alpha=0.6)
            ax0.plot(*(data[0][3]),'k--')
            ax0.plot(*(data[0][4]),'k--')
            ax0.axis('equal')
            ax1 = axes[i][1] if num>1 else axes[i+1]
            for j in data[0][:3]:
                ax1.plot(j)
            maxdata = np.max(data[0][2])
            ax1.hlines(maxdata,0,60,'r','--',label=f'visibility={round(maxdata*100,1)}%')
            ax1.legend(loc='upper left')
        #     ax1.vlines([0],10,-100)
        #     ax1.hlines([0],-10,100)
        plt.title(str(exstate))
        plt.savefig(r'D:\skzhao\fig\2s%s.png'%(''.join((title,*exstate))),dpi=400)
        plt.close()
    #     num = eval(q_target[0][1:])-1
        for qubit in exstate:
            num=measure.qubitToread.index(qubit)
        #     para0, para1 = await dtl.find_circle(measure,s_st,num)
            dtl.classify(measure,s_st,target=num,predictexe=True,n_cluster=len(states))
        return {}

    if title == 'AllXYdragdetune':
        q_target = args['exstate'][0]
        num = measure.qubitToread.index(q_target)
        fall, sall = data

        fig, axes = plt.subplots(ncols=2,nrows=1,figsize=(9,4))
        l = np.shape(fall)[0]//2
        f1, f2, s1, s2 = fall[:l,num], fall[l:,num], np.abs(sall[:l,num]), np.abs(sall[l:,num])
        f1_new = np.linspace(f1[0],f1[-1],4001)
        z1 = np.poly1d(np.polyfit(f1,s1,2))(f1_new)
        z2 = np.poly1d(np.polyfit(f2,s2,2))(f1_new)
        # index = np.argmin(np.abs(z1-z2))
        # z1 = scipy.interpolate.interp1d(f1,RowToRipe().smooth(s1,f0=0.2),kind="cubic")(f1_new)
        # z2 = scipy.interpolate.interp1d(f2,RowToRipe().smooth(s2,f0=0.2),kind="cubic")(f1_new)
        index1, = scipy.signal.argrelmin(np.abs(z1-z2))
        index = index1[np.argmin(np.abs(z1[index1]-0.5))]
        axes[0].plot(np.array([f1,f2]).T,np.array([s1,s2]).T,'.')
        axes[0].plot(np.array([f1_new,f1_new]).T,np.array([z1,z2]).T)
        axes[0].plot([f1_new[index],f1_new[index]],[z1[index],z2[index]],'ko')
        axes[0].set_title(q_target+f'alpha={round(f1_new[index],3)}')
        
        plt.savefig(r'D:\skzhao\fig\2s%s.png'%(''.join((title,q_target))),dpi=400)
        plt.close()
        DRAGScaling =round(f1_new[index],3)/(measure.qubits[q_target].alpha*2*np.pi)

        return {q_target:{'DRAGScaling':DRAGScaling}}

    if title == 'readpowerOpt_zsk':
        exstate = args['exstate']
        readamp_op = {}
        rdp,visb = data
        plt.figure()
        for qubit in exstate:
            num = measure.qubitToread.index(qubit)
            x,y = rdp[:,num], visb[:,num]
            y = RowToRipe().smooth(y,f0=0.2)
            measure.readamp[num] = x[np.argmax(y)]
            plt.plot(x,y)
            plt.plot(x[np.argmax(y)],y[np.argmax(y)],'o')
        plt.savefig(r'D:\skzhao\fig\2s%s.png'%(''.join((title,*exstate))),dpi=400)
        plt.close()
        return {}

    if title == 'Ramsey_repeat':
        return {}

    if title == 'Ramsey_repeat1':
        return {}

    if title == "zPulse_pop":
        return {}

    if title == 'XYZtiming_single':

        q_target = args['exstate'][0]   ###yhs
        readnum = qname.index(q_target)
        qubit = measure.qubits[qname[readnum]]    ##zsk

        # qubit = measure.qubits[qname[0]]    ##zsk
        t_shift, s_z = data
        
        plt.figure()
        for i in range(np.shape(s_z)[1]):
            if i==readnum:
                x, y = t_shift[:,i], np.abs(s_z[:,i])
                func = scipy.interpolate.interp1d(x,y)
                x = np.linspace(min(x),max(x),501)
                y = func(x)
                y0 = RowToRipe().smooth(y,f0=0.15)
                res, func = singleErf_fit().fitErf(x, y0)
                paras = res.x
                loc = paras[1]
                plt.plot(x,y,'-o',markersize=3)
                plt.plot(x,func(x,paras))
                plt.vlines(loc,np.min(y),np.max(y)) 
            
        # plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((qname[0],'_',title))))  ##zsk
        plt.title(f'Q%d:z>xy={(loc-1000*0)*1e-9}'%(qubit.index+1))
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((qname[readnum],'_',title))))  ##yhs
        plt.close()
        zbigxy = loc-1000*0
        qubit.timing['z>xy'] = (zbigxy*1e-9)
        # return {j: {'timing':qubit.timing} for i, j in enumerate(qname)}    ##zsk
        QT={j: {'timing':measure.qubits[j].timing} for i, j in enumerate(qname)}
        # print(QT)
        return QT    ##yhssigma1, center1, a, b

    if title == 'QRamsey_2d':
        q_target = args['exstate'][0]
        num = measure.qubitToread.index(q_target)
        v_2d, t_2d, s_2d = data

        x, y, s = v_2d[:,num], t_2d[0,:,num], s_2d[:,:,num]
        extent = [min(x),max(x),min(y),max(y)]
        fig, ax = plt.subplots(figsize=(8,6),ncols=1,nrows=2,sharex=True)
        im = ax[0].imshow((s/np.max(s)).T,origin='lower',aspect='auto',cmap='plasma',extent=extent)
        plt.colorbar(im,ax=ax)
        ax[1].set_xlabel('Voltage (a.u.)')
        ax[0].set_ylabel('Time (ns)')
        ax[1].set_ylabel('Frequency (MHz)')

        w = []
        for i in range(len(x)):
            y0 = s[i,:]
            res, func = Cos_Fit().fitCos(y,y0)
            w0 = res.x[2]
        #     w0 = 0 if len(x)//2 == i else res.x[2]
        #     w0 = -w0 if len(x)//2 > i else w0
            w.append(w0)
        res, func = RowToRipe().poly(x,np.array(w),1)
        ax[1].plot(x,np.array(w)*1e3,'-o', ms=8, lw=2, alpha=0.7, mfc='orange')
        ax[1].plot(x,func(x)*1e3,'r--')

        ax[0].set_title(q_target+f':res={res}')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((q_target,'_',title))))  ##yhs
        plt.close()

        return {q_target: {'diff_height':-res[0]}}

    if title == 'zShape_tomo_1':
        return {}

    if title == 'QRamsey_crosstalk':
        matrix = args['matrix']
        q_target = args['exstate'][0]
        for q in args['zstate'].keys():
            if q != q_target:
                q_bias = q 
                v_bias = args['zstate'][q_bias]
        num = measure.qubitToread.index(q_target)
        row, col = measure.qubits[q_target].index, measure.qubits[q_bias].index

        v_2d, t_2d, s_2d = data

        x, y, s = v_2d[:,num], t_2d[0,:,num], s_2d[:,:,num]
        extent = [min(x),max(x),min(y),max(y)]
        fig, ax = plt.subplots(figsize=(8,6),ncols=1,nrows=2,sharex=True)
        im = ax[0].imshow((s/np.max(s)).T,origin='lower',aspect='auto',cmap='plasma',extent=extent)
        plt.colorbar(im,ax=ax)
        ax[1].set_xlabel('Voltage (a.u.)')
        ax[0].set_ylabel('Time (ns)')
        ax[1].set_ylabel('Frequency (MHz)')

        w = []

        for i in range(len(x)):
            y0 = s[i,:]
            if np.max(y0)-np.min(y0)<0.15*(np.max(s)-np.min(s)):
                w0 = 0
            else:
                res, func = Cos_Fit().fitCos(y,y0)
                w0 = res.x[2]
            w.append(w0)
        wnew = sorted(w)
        idx00 = w.index(wnew[0])
        idx11 = w.index(wnew[1])
        idx0, idx1 = sorted([idx00,idx11])
        w = np.array(w)
        w[:idx0] *= -1
        xcut = np.concatenate([x[:idx0],x[(idx1+1):]])
        wcut = np.concatenate([w[:idx0],w[(idx1+1):]])

        xnew = np.linspace(np.min(x)-np.abs(np.max(x)-np.min(x)),np.max(x)+np.abs(np.max(x)-np.min(x)),50001)
        res, func = RowToRipe().poly(xcut,wcut,1)
        v_op = xnew[np.argmin(np.abs(func(xnew)))]
        ax[1].plot(xcut,wcut,'-o', ms=8, lw=2, alpha=0.7, mfc='orange')
        ax[1].plot(xnew,func(xnew),'g--')
        ax[1].hlines(0,np.min(xnew),np.max(xnew))
        ax[1].plot(v_op,0,'ro',markersize=10)


        ax[0].set_title(q_target+f',v_op={round(v_op,5)},v_bias={v_bias},matrixelement={round(-v_op/v_bias*100,5)}')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((q_target,'-',q_bias,'_',title))))  ##yhs
        plt.close()

        matrix[row,col] = -v_op/v_bias
        print(matrix)
        return {}

    if title == 'Rcscali_single':
        exstate = args['exstate']
        dcstate = list(args['dcstate'].keys())
        num = measure.qubitToread.index(exstate[0])
        tt_Rc, s_Rc = data
        x, y = tt_Rc[:,num], np.abs(s_Rc[:,num])
        yimag = signal.hilbert(y-y.mean())
        res_hilbert, func_hilbert = RowToRipe().poly(x[10:-10],np.unwrap(np.angle(yimag[10:-10])),1)
        w_hilbert = res_hilbert[0]/2/np.pi
        res, func = T2_Fit(T1=30000,funcname='gauss',envelopemethod='hilbert').fitT2(x,np.abs(y))
        A,B,T1,T2,w,phi = res.x
        z = func(x,res.x)
        z_env = A*np.exp(-(x/T2)**2-x/T1/2) + B
        fig, axes = plt.subplots(ncols=2,nrows=1,figsize=(9,3))
        axes[0].plot(tt_Rc,np.abs(s_Rc),'-o',markersize=3)
        axes[0].plot(x,z)
        axes[0].plot(x,z_env)
        axes[0].set_title(exstate[0]+dcstate[0]+str(round(measure.qubits[exstate[0]].detune/1e6,3)))

        axes[1].plot(x,np.unwrap(np.angle(yimag)),'-o')
        axes[1].plot(x,func_hilbert(x))
        axes[1].set_title(f'w_hilbert={w_hilbert*1e3}MHz')
        plt.savefig(r'D:\skzhao\fig\%s.png'%(''.join((exstate[0],'-',dcstate[0],'_',title))))  ##yhs
        plt.close()
        return {}