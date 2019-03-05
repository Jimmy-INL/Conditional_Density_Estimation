import warnings
warnings.filterwarnings("ignore")

from cde.density_simulation import SkewNormal
from cde.density_estimator import KernelMixtureNetwork
import numpy as np


""" simulate some data """
seed = 22
density_simulator = SkewNormal(random_seed=seed)
X, Y = density_simulator.simulate(n_samples=3000)

""" fit density model """
model = KernelMixtureNetwork("KDE_demo", ndim_x=1, ndim_y=1, n_centers=50,
                             x_noise_std=0.2, y_noise_std=0.1, random_seed=22)
model.fit(X, Y)

""" query the conditional pdf and cdf"""
x_cond = np.zeros((1, 1))
y_query = np.ones((1, 1)) * 0.1
prob = model.pdf(x_cond, y_query)
cum_prob = model.cdf(x_cond, y_query)

""" compute conditional moments & VaR  """
x_cond = np.zeros((1, 1))

mean = model.mean_(x_cond)[0][0]
std = model.std_(x_cond)[0][0]
skewness = model.skewness(x_cond)[0]
VaR = model.value_at_risk(x_cond, alpha=0.01)[0]

print("Mean:", mean)
print("Std:", std)
print("Skewness:", skewness)
print("Value-at-Risk", VaR)

""" plot the fitted distribution """
x_cond_plot = np.array([-0.5, 0, 0.5])
model.plot2d(x_cond_plot, ylim=(-0.25, 0.15), show=True)



