import numpy as np
cimport numpy as np
from numpy.fft cimport fft  # Importa la función fft desde numpy.fft
cimport cython

cdef class Phase:
    cdef public np.ndarray[np.float64_t] V
    cdef public np.ndarray[np.float64_t] I
    cdef public np.ndarray[np.float64_t] Theta_V
    cdef public np.ndarray[np.float64_t] Theta_I

    def __init__(self, np.ndarray[np.float64_t] V, np.ndarray[np.float64_t] I,
                 np.ndarray[np.float64_t] Theta_V, np.ndarray[np.float64_t] Theta_I):
        self.V = V
        self.I = I
        self.Theta_V = Theta_V
        self.Theta_I = Theta_I
    
    cpdef str mostrar_atributos(self):
        output = "|V|: {} Volts\n|I|: {} Amperes\nTheta_V: {}°\nTheta_I: {}°".format(
            self.V, self.I, self.Theta_V, self.Theta_I)
        return output


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef np.ndarray[np.complex128_t] true_fft(np.ndarray[np.float64_t] Voltage, int N):
    cdef np.ndarray[np.complex128_t] FFT_VX = fft(Voltage)  # Usa la función fft importada
    cdef np.ndarray[np.float64_t] x
    x = FFT_VX[:int(N/2 + 1)] * 2 / N
    x[0] *= 2
    return x


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef list true_fft_phase(np.ndarray[np.float64_t] Voltages, int N):
    cdef np.ndarray[np.complex128_t] FFT_VX = fft(Voltages, axis=1)  # Usa la función fft importada
    cdef list FFT_V = []
    cdef np.ndarray[np.float64_t] x
    for i in range(len(FFT_VX)):
        x = FFT_VX[i][:int(N/2 + 1)] * 2 / N
        x[0] *= 2
        FFT_V.append(x)
    return FFT_V


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double data_mag(np.ndarray[np.complex128_t] FFT, int Z):
    return abs(FFT[1 * Z])


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double data_angle(np.ndarray[np.complex128_t] FFT1, np.ndarray[np.complex128_t] FFT2, int Z):
    return (np.angle(FFT2[1 * Z]) - np.angle(FFT1[1 * Z])) * 180 / np.pi


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef np.ndarray[np.float64_t] update(np.ndarray[np.float64_t] data, np.ndarray[np.float64_t] new_data):
    cdef int old_data = max(0, data.shape[0] - new_data.shape[0])
    cdef np.ndarray[np.float64_t] data_update = np.concatenate((data[-old_data:], new_data))
    return data_update


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double fix_data(double data, double REF):
    if data < 0:
        data = (data * REF / 0x80000000) - 2 * REF
    else:
        data = (data * REF / 0x7fffffff)
    return data


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef list predict(np.ndarray[np.float64_t] estado, Model):
    cdef np.ndarray[np.float64_t] Mean = np.array([5839.074220, 7061.736407, 4902.503453, 38.128003,
                                                    47.863958, 68.348688, 153.001569, 156.524264,
                                                    146.806856, 0.293765, 0.188813, -0.062767,
                                                    7.482766, 7.604663, 7.080138, -0.217297,
                                                    0.558062, -0.290082])
    cdef np.ndarray[np.float64_t] var = np.array([6396379824.971244, 9405516053.802622, 4360129360.965660,
                                                   349.518481, 1746351.907888, 89135.605438, 102039.080906,
                                                   133339.606473, 79522.579804, 4.072448, 3.096451,
                                                   2.802325, 337.582695, 368.279829, 375.622753,
                                                   4.080932, 2.577789, 3.128683])
    cdef np.ndarray[np.float64_t] normalized_data = (estado - Mean) / var
    return Model.predict([normalized_data])

