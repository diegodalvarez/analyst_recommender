import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets, decomposition, preprocessing

#setting randomness
seed = 42
np.random(seed)
tf.random_seed(seed)

