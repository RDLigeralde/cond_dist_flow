# -*- coding: utf-8 -*-
"""Generate_Params.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GZFxijyKmTpZi4dPma2DPGjf5kKkYy3j
"""

from jax import jit, vmap
import jax.numpy as jnp
import jax.numpy.linalg as jla
import numpy as np

"""
Density calculation:
Experiment 1: average of x, y stdevs
"""

#Returns scalar
@jit
def std_density(subarray):
  trans = subarray.T
  xs = trans[0]
  ys = trans[1]
  r_stdevs = (jnp.std(xs) + jnp.std(ys)) / 2
  return r_stdevs

densities = jit(vmap(std_density))

"""
Experiment 2: average Euclidean distance around a centerpoint
Going to try scaling

Distance from:
https://www.reddit.com/r/learnpython/comments/ypumzn/calculating_euclidean_distance_between_1_point/
u/lanemik
"""

@jit
def c_dist(center, neighbors):
  c = jnp.array([center])
  ds = jnp.array(neighbors)
  d_array = jnp.linalg.norm(c - ds, axis = 1)
  d_mean = jnp.mean(d_array)
  return d_mean

c_dists = jit(vmap(c_dist, in_axes = (0, 0)))

"""
Composite function for neighborhood spread method
Takes array of sorted points A, creates array of arrays B s.t B[i] are neighbors of A[i]
Then finds the mean Euclidean distance of each A[i] from the points in their B[i]
"""

def neighbor_split(array, size):

    pad = jnp.floor(size / 2).astype(int)
    count = len(array) - size + 1

    indices = jnp.arange(0, count)
    A_center = array[indices[:, jnp.newaxis] + jnp.arange(size)]

    A_left = jnp.repeat(jnp.array([A_center[0]]), pad, axis = 0)
    A_right = jnp.repeat(jnp.array([A_center[-1]]), pad, axis = 0)

    result = jnp.concatenate([A_left, A_center, A_right], axis = 0)
    return result

#Modified sigmoid to smoothly map distance data to range of desirable lrs
@jit
def set_range(x, min, max):
  numer = 2 * (max - min)
  denom = 1 + jnp.exp(-x)
  result = (numer / denom) + (2 * min - max)
  return result

#Generalize to array of distances
set_ranges = jit(vmap(set_range, in_axes = (0, None, None)))

def dists(array, size, min, max):

  dists = c_dists(array, neighbor_split(array, size))
  return set_ranges(dists, min, max)

"""
Use nearest neighborhood approach to determine learning rate for each datapoint
"""

#Minimum distance in xbetween a target point and a comparison array
@jit
def nearest_neighbor(x, ys):
  diffs = jla.norm(ys - x, axis = 1)
  closest = jnp.min(diffs)
  return closest

#Extend to target array, comparison array
nearest_neighbors = jit(vmap(nearest_neighbor, in_axes = (0, None)))

#Use above to assign learning rates
@jit
def make_lrs(starting, target, min, max):
  diffs = nearest_neighbors(starting, target)
  lrs = set_ranges(diffs, min, max)
  return jnp.expand_dims(lrs, axis = 1)

"""
For creating triangular cost matrix
"""

def make_lambda(lam, numpar, numobs):

  aux_param = jnp.ones(numpar)
  aux_param = jnp.ones(numpar)
  aux_obs = (1/lam) * jnp.ones(numobs)

  lamMat = jnp.diag(np.hstack((aux_param,aux_obs)), 0)
  return lamMat