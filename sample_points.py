# -*- coding: utf-8 -*-
"""Sample_Points.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Grsoh2PqsthokinK31Umpq7BPFDQ9koU
"""

import jax.numpy as jnp
import numpy as np

def sample_moon(N, M, LM, ystr):

  data = np.zeros([N,2])
  for i in range(N):
      data[i,0] = np.random.randn()
      data[i,1]= 0.5 * np.random.randn() + data[i,0] ** 2 - 1

  data_product = np.transpose([np.tile(data[:,0], N), np.repeat(data[:,1], N)])

  data_product_get = data_product[np.random.choice(N**2, M, replace=False),:]

  Zcurrent = jnp.array(sorted(data_product_get, key = lambda x: x[0]))
  Zinitial = Zcurrent.copy()

  Zjoint = jnp.array(sorted(data, key = lambda x: x[0]))

  if LM:
    #to estimate rho(x|ystr_lm)
    Zlm = np.zeros((M,2))
    Zlm[:,0] = np.random.randn(M)
    Zlm[:,1] = np.ones(M) * ystr
    Zlm = jnp.array(sorted(Zlm, key = lambda x: x[0]))
    return [Zinitial, Zcurrent, Zjoint, Zlm]

  else:
    return [Zinitial, Zcurrent, Zjoint]