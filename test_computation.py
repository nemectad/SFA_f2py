import numpy as np
import library

def test_computation():
    int_parameters = np.array([1, 1, 1, 1], dtype = int)
    float_parameters = np.array([0.5, 1, 5.68000E-2, 1, 5.68000E-2], dtype = float)
    s_parameters = np.array([0.750000E-01, 1.0, 0.0, 1, 1, 1,
                            10], dtype = float)

    parameters = np.array([float_parameters, int_parameters, s_parameters, 20])
    result = library.compute(parameters)

    assert np.allclose(result[1,0], -0.00033394)
