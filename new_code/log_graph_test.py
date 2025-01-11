import numpy as np
import matplotlib.pyplot as plt

key_val = 10
npoints = 100
x = key_val * np.arange(npoints)

y = key_val * np.logspace(0.1,2,npoints)

plt.plot(x, y,'o')
plt.show()