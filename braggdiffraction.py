import matplotlib.pyplot as plt
import numpy as np

# TODO: Bragg's law demonstration on a 2D Crystal

theta = np.deg2rad(30)
rotmatrix = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
print(rotmatrix)
