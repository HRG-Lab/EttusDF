# -*- coding: utf-8 -*-

from .context import ettusdf

import unittest
import numpy as np
from pyargus import directionEstimation
import matplotlib.pyplot as plt


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_DOAEstimator_constructor(self):
        with self.assertRaises(ValueError) as ctx:
            ettusdf.DOAEstimator(array_type='Fancy')
        
        ula_alignment = np.arange(0, 4, 1) * 0.5
        incident_angles = np.arange(0, 181, 1)
        scan_vecs = directionEstimation.gen_ula_scanning_vectors(
            ula_alignment,
            incident_angles
        )

        doa_est = ettusdf.DOAEstimator(
            array_type='ULA',
            array_alignment=ula_alignment,
            incident_angles=incident_angles
        )
        np.testing.assert_array_equal(doa_est.scanning_vectors, scan_vecs)

    def test_DOAEstimator_constructor_key_check(self):
        with self.assertRaises(ValueError) as ctx:
            ettusdf.DOAEstimator(array_type='ULA')

        with self.assertRaises(ValueError) as ctx:
            ettusdf.DOAEstimator(array_type='UCA')

    def test_doa_estimate_bartlett(self):
        M = 4
        N = 2**12
        d = 0.5
        theta = 60
        ula_alignment = np.arange(0, 4, 1) * 0.5
        incident_angles = np.arange(0, 181, 1)
        scan_vecs = directionEstimation.gen_ula_scanning_vectors(
            ula_alignment,
            incident_angles
        )

        doa_est = ettusdf.DOAEstimator(
            array_type='ULA',
            array_alignment=ula_alignment,
            incident_angles=incident_angles,
            estimator='Bartlett'
        )

        a = np.exp(np.arange(0, M, 1)*1j*2*np.pi*d*np.cos(np.deg2rad(theta)))
        soi = np.random.normal(0, 1, N)
        soi_matrix = np.outer(soi, a).T
        noise = np.random.normal(0, np.sqrt(10**-1), (M,N))
        rx_signal = soi_matrix
        R = directionEstimation.corr_matrix_estimate(rx_signal.T, imp="mem_eff")
        Bartlett = directionEstimation.DOA_Bartlett(R, scan_vecs)

        np.testing.assert_array_equal(Bartlett, doa_est.estimate_doa(rx_signal))


if __name__ == '__main__':
    unittest.main()