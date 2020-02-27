from pyargus import directionEstimation
import numpy as np

import logging

class DOAEstimator():
    """
    A wrapper for pyargus to simplify creation of DOA plots
    """
    VALID_ARRAY_TYPES = ["ULA", "UCA", "Other"]
    VALID_ESTIMATORS = ["Bartlett", "Capon", "MEM", "MUSIC", "MD-MUSIC"]

    def __init__(self, array_type="ULA", estimator="MUSIC", **kwargs):
        if array_type not in self.VALID_ARRAY_TYPES:
            raise ValueError("{} not a recognized array type. Must be one of ['ULA', 'UCA', 'Other']".format(array_type))

        def required_arg_check(required_args):
            for arg in required_args:
                if arg not in kwargs:
                    raise ValueError("Missing required argument: {}".format(arg))
        
        required_arg_check(['incident_angles',])
        self.__incident_angles = kwargs['incident_angles']
        
        if array_type == "ULA":
            required_args = ['array_alignment']
            required_arg_check(required_args)
            self.__scanning_vectors = \
                directionEstimation.gen_ula_scanning_vectors(
                    kwargs['array_alignment'], kwargs['incident_angles']
                )
        elif array_type == "UCA":
            required_args = ['num_elems', 'radius']
            required_arg_check(required_args)
            self.__scanning_vectors = \
                directionEstimation.gen_uca_scanning_vectors(
                    kwargs['num_elems'],
                    kwargs['radius'],
                    kwargs['incident_angles']
                )
        elif array_type == "Other":
            required_args = ['num_elems', 'x', 'y']
            required_arg_check(required_args)
            self.__scanning_vectors = \
                directionEstimation.gen_scanning_vectors(
                    kwargs['num_elems'],
                    kwargs['x'],
                    kwargs['y'],
                    kwargs['incident_angles'],
                )

        if estimator not in self.VALID_ESTIMATORS:
            raise ValueError("Unrecognized estimator: {}".format(estimator))
        self.__estimator = estimator
        

    @property
    def scanning_vectors(self):
        return self.__scanning_vectors


    def estimate_doa(self, rx_signal):
        R = directionEstimation.corr_matrix_estimate(rx_signal.T, imp="mem_eff")
        if self.__estimator == "Bartlett":
            estimate = directionEstimation.DOA_Bartlett(R, self.__scanning_vectors)
        elif self.__estimator == "Capon":
            estimate = directionEstimation.DOA_Capon(R, self.__scanning_vectors)
        elif self.__estimator == "MEM":
            estimate = directionEstimation.DOA_MEM(
                R, self.__scanning_vectors, column_select=0
            )
            logging.warning("Column select is not yet implemented. Set to default (0)")
        elif self.__estimator == "MUSIC":
            raise NotImplementedError
        elif self.__estimator == "MD-MUSIC":
            raise NotImplementedError

        return estimate


    def gen_plot_data(self, rx_signal, log_scale_min=None):
        DOA_data = self.estimate_doa(rx_signal)
        DOA_data = np.divide(np.abs(DOA_data), np.max(np.abs(DOA_data))) # normalization

        if log_scale_min is not None:
            DOA_data = 10 * np.log10(DOA_data)
            for i, theta in enumerate(self.__incident_angles):
                if DOA_data[i] < log_scale_min:
                    DOA_data[i] = log_scale_min

        return self.__incident_angles, DOA_data