# -*- coding: utf-8 -*-
"""Plot_Tools.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VGd0De1_GMCRhJa7AJH2Pa0ZPdxqARTx
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.stats import gaussian_kde

"""
Check Main Loop Progress
"""
def make_plot(info, save, Zinitial, Zcurrent, Zjoint):
  plt.figure(figsize=(10,8))
  plt.plot(Zinitial[:,0], Zinitial[:,1], '.b', label='Initial', alpha=0.2)
  plt.plot(Zcurrent[:,0], Zcurrent[:,1], '.g', label='Current', alpha=1)
  plt.plot(Zjoint[:,0], Zjoint[:,1], '.r', label='Target', alpha=1)
  plt.legend()

  if save:
    file_name_parts = ["Kernel = ", info[0], ", Iters = ", info[1], ", BW Range = ", info[2], ", LR Range = ", info[3], ", Neighbors = ", info[4], ", Refresh Rate = ", info[5], ", Execution Time = ", info[6], ".png"]
    filename = "".join(file_name_parts)
    plt.savefig(filename)
    files.download(filename)

"""
Check for extent of y movementr
"""
def y_mvmt(Zcurrent, Zinitial):
  mm = np.abs(Zcurrent[:,1]-Zinitial[:,1])
  plt.plot(mm)
  print('Mean movement in the y direction',np.mean(mm))

"""
Check LM Progress
Probably will be obsolete soon
"""

def LM_est(Zlm, ystr):
  dy = 0.05
  xgrid = np.linspace(-3,3,500)

  def pycx(x,ystr):
    s = 0.5; s2 = s**2;
    m = ystr-(x**2-1)
    return np.exp(-(m**2)/(2*s2))/np.sqrt(2*np.pi*s2)

  def px(x):
    return np.exp(-(x**2)/(2))/np.sqrt(2*np.pi)

  def pxcy(x,ystr):
    return pycx(x,ystr)*px(x)

  nfact = scipy.integrate.quad(pxcy,-np.inf,+np.inf,args=ystr)

  truthcd=pxcy(xgrid,ystr)/nfact[0]

  kernel_lm=scipy.stats.gaussian_kde(Zlm[:,0])

  fig, axs = plt.subplots(1,2,figsize=(16,9))

  axs[0].plot(xgrid,truthcd,'.b')
  axs[0].plot(xgrid,kernel_lm(xgrid),'.r')
  axs[0].title.set_text('Estimated cond densities lm')

  axs[1].plot(xgrid,np.abs(kernel_lm(xgrid)-truthcd),'.b')

  axs[1].title.set_text('Errors')

"""
Do LM based off slices
"""

def check_ystr(Zcurrent, ystr):

  bs = Zcurrent.shape[0]
  Z_approx = Zcurrent.at[:, 1].set(np.round(Zcurrent[:, 1]))
  Zlm = Z_approx[Z_approx[:, 1] == ystr]

  Zlm = Zlm.at[:, 0].set(np.round(Zlm[:, 0], 2))

  samples = Zlm[:,0]

  plt.hist(samples, bins = int(np.round(np.sqrt(bs))), density=True, alpha=0.5, color='b', label='Histogram')

  kde = gaussian_kde(samples)
  x = np.linspace(min(samples), max(samples), 1000)
  plt.plot(x, kde(x), color='r', label='KDE')

  plt.xlabel('Value')
  plt.ylabel('Density')
  plt.title('Distribution of Samples')
  plt.legend()

  plt.show()

