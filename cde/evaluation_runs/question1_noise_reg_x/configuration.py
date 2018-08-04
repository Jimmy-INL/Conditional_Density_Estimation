import pickle
import numpy as np
import glob
import os

from cde.evaluation.ConfigRunner import ConfigRunner
from ml_logger import logger

EXP_PREFIX = 'question1_noise_reg_x'

def question1(): #noise
  estimator_params = {
  'KernelMixtureNetwork':

    {'center_sampling_method': ["k_means"],
     'n_centers': [20, 50],
     'keep_edges': [True],
     'init_scales': [[0.1, 0.5, 1.]],
     'train_scales': [True],
     'hidden_sizes': [(16, 16)],
     'n_training_epochs': [500],
     'x_noise_std': [0.01, 0.05, 0.1, None],
     'y_noise_std': [None],
     'random_seed': [22]
     },
  'MixtureDensityNetwork':
    {
      'n_centers': [10, 20],
      'n_training_epochs': [1000],
      'hidden_sizes': [(16, 16)],
      'x_noise_std': [0.01, 0.05, 0.1, None],
      'y_noise_std': [None],
      'random_seed': [22]
    }
  }

  simulators_params = {
  'EconDensity': {'std': [1],
                  'heteroscedastic': [True],
                  },

  'GaussianMixture': {'n_kernels' : [20],
                      'ndim_x': [2],
                      'ndim_y': [2],
                      'means_std': [1.5]
                      },
  'ArmaJump': {'c': [0.1],
               'arma_a1': [0.9],
               'std': [0.05],
               'jump_prob': [0.05],
              }
  }


  return estimator_params, simulators_params


if __name__ == '__main__':

  run = True
  load = not run

  keys_of_interest = ['task_name', 'estimator', 'simulator', 'n_observations', 'center_sampling_method', 'x_noise_std',
                      'y_noise_std', 'ndim_x', 'ndim_y', 'n_centers', "n_mc_samples", "n_x_cond", 'mean_est',
                      'cov_est', 'mean_sim', 'cov_sim', 'kl_divergence', 'hellinger_distance', 'js_divergence',
                      'x_cond', 'random_seed', "mean_sim", "cov_sim", "mean_abs_diff", "cov_abs_diff",
                      "VaR_sim", "VaR_est", "VaR_abs_diff", "CVaR_sim", "CVaR_est", "CVaR_abs_diff",
                      "time_to_fit"
                      ]


  if run:
      observations = 100 * np.logspace(0, 4, num=5, base=2.0,
                                       dtype=np.int32)  # creates a list with log scale: 100, 200, 400, 800, 1600

      conf_est, conf_sim = question1()
      conf_runner = ConfigRunner(EXP_PREFIX, conf_est, conf_sim, observations=observations, keys_of_interest=keys_of_interest,
                                 n_mc_samples=2*10**4, n_x_cond=5, n_seeds=5) #TODO set back n_mc_samples to 2*10**6

      results_list, full_df = conf_runner.run_configurations(dump_models=True)

  # if load:
  #   with open(results_pickle, 'rb') as pickle_file:
  #     gof_result = pickle.load(pickle_file)
  #     results_df = gof_result.generate_results_dataframe(keys_of_interest)
  #
  #
  #     graph_dicts = [
  #       {"estimator": "KernelMixtureNetwork", "x_noise_std": 0.1, "y_noise_std": None, "n_centers": 20},
  #       {"estimator": "KernelMixtureNetwork", "x_noise_std": 0.01, "y_noise_std": None, "n_centers": 20},
  #       {"estimator": "KernelMixtureNetwork", "x_noise_std": None, "y_noise_std": None, "n_centers": 20},
  #       {"estimator": "MixtureDensityNetwork", "x_noise_std": 0.1, "y_noise_std": None, "n_centers": 10},
  #       { "estimator": "MixtureDensityNetwork", "x_noise_std": 0.01, "y_noise_std": None, "n_centers": 10},
  #       {"estimator": "MixtureDensityNetwork", "x_noise_std": None, "y_noise_std": None, "n_centers": 10}
  #     ]
  #
  #     gof_result.plot_metric(graph_dicts, metric="kl_divergence", simulator="EconDensity")
  #     print(gof_result)