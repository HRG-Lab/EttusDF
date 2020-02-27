# -*- coding: utf-8 -*-

from .context import ettusdf

import unittest
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""
    def test_rx_signal_live_update(self):
        fig, ax = plt.subplots()
        d = 0.5
        M = 4
        N = 2**12
        ula_alignment = np.arange(0, 4, 1) * d
        thetas = np.arange(0, 181, 1)
        test_theta = 60

        doa_est = ettusdf.DOAEstimator(
            array_type='ULA',
            array_alignment=ula_alignment,
            incident_angles=thetas,
            estimator='Bartlett'
        )

        a = np.exp(np.arange(0, M, 1)*1j*2*np.pi*d*np.cos(np.deg2rad(test_theta)))
        soi = np.random.normal(0, 1, N)
        soi_matrix = np.outer(soi, a).T
        rx_signal = soi_matrix
        ln, = plt.plot([], [])

        def init():
            xdata, ydata = doa_est.gen_plot_data(rx_signal, log_scale_min=-50)
            ln.set_data(xdata, ydata)
            return ln,

        def update(i):
            noise = np.random.normal(0, np.sqrt(10**-1), (M,N))
            rx_signal = soi_matrix + noise
            xdata, ydata = doa_est.gen_plot_data(rx_signal, log_scale_min=-50)
            ln.set_data(xdata, ydata)
            return ln,

        ani = FuncAnimation(fig, update, init_func=init, blit=True)
        plt.show()


if __name__ == '__main__':
    unittest.main()
