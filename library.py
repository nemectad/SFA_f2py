# Libraries import
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import h5py
import universal_input
# Importing Fortran code
import Fortran.main as main


###########################################################
# User input:
def user_input():
    # Computation parameters (Higher numbers, slower computation):
    N_pts = universal_input.u_input(
        "Type number of points for dipole evaluation: ",
        int, 1)

    N_int = universal_input.u_input(
        "Type number of points for integrals evaluation: ",
        int, 1)

    # Field parameters:
    # sense of polarisation
    p1 = universal_input.u_input(
        "Type sense of polarization of the first field "
        "(-1 anticlockwise, 1 clockwise): ",
        int, -1, 1, None, [-1,1])

    p2 = universal_input.u_input(
        "Type sense of polarization of the second field "
        "(-1 anticlockwise, 1 clockwise): ",
        int, -1, 1, None, [-1,1])

    # fields ellipticity
    eps = universal_input.u_input(
        "Type ellipticity of the first field between 0.0"
        "and 1.0 (0.0 for linear polarisation):",
        float, 0, 1)

    # carrier envelope phases
    phi1 = universal_input.u_input(
        "Type carrier envelope phase of the first field from "
        "0.0 to 1.0: ",
        float, 0, 1)

    phi2 = universal_input.u_input(
        "Type carrier envelope phase of the second field from "
        "0.0 to 1.0: ",
        float, 0, 1)

    # number of cycles in the first field:
    N_cycl = universal_input.u_input(
        "Type number of cycles in the envelope for the first field "
        "(must be greater than 0): ",
        float, 0)

    # field frequencies
    rel_omega = universal_input.u_input(
        "Type second field frequency relative to the first field "
        "for multicolored fields (1, 2, 3, ...):",
        int, 1)

    # relative delays
    rel_delay = universal_input.u_input(
        "Type relative delays between fields (between 0.0 and 1.0): ",
        float, 0, 1)

    # deviation between pulses
    theta = universal_input.u_input(
        "Type deviation between pulses (0.0 to 1.0): ",
        float, 0, 1)

    # polarization mode (p1), polarization mode (p2) (i.e. clockwise
    # p = 1, anticlockwise p = -1)
    # num. of pts. for integral (N_int), num. of pts. for dipole(N_pts)
    int_parameters = np.array([p1, p2, N_int, N_pts], dtype = int)
    # Ionization potential in a.u. (Ip), Carrier envelope phase (phi1)
    # photon energy (\omega_01), Carrier envelope phase (phi2)
    # photon energy (\omega_02)
    float_parameters = np.array([0.5, phi1, 5.68000E-2, phi2,
                               rel_omega*5.68000E-2], dtype = float)
    # Electric field aplitude (E0), s default 1 (symmetrical fields)
    # (ineq default 0), El. field ellipticity (eps), Deviation (theta)
    # Rel. delay between pulses (Rel_delay), No. of cycles in envelope (N_cycl)
    s_parameters = np.array([0.750000E-01, 1.0, 0.0, eps, theta, rel_delay,
                            N_cycl], dtype = float)

    dim = int(2.0*s_parameters[6]*int_parameters[3])

    return [float_parameters, int_parameters, s_parameters, dim]


###########################################################
# Compute result:
def compute(parameters):
    # Testing input
    assert np.shape(parameters[0])[0] == 5
    assert np.shape(parameters[1])[0] == 4
    assert np.shape(parameters[2])[0] == 7
    assert isinstance(parameters[3], int)

    # Result array
    result = np.zeros((9,parameters[3]), dtype = float)

    print("\n"
          "Hold on, it will take a while...")

    # Main task
    result = main.sfa(
        parameters[0], parameters[1], parameters[2],
        result, parameters[3])
    print("Computation completed!")

    return result


###########################################################
# Save to file:
def save_to_H5file(result):
    # Save to .h5 file
    with h5py.File("result.h5", "w") as hdf5_file:
        hdf5_file.create_dataset("dipole", data = [result[1,:],result[2,:]],
                                 dtype = 'float')
        hdf5_file.create_dataset("Afield", data = [result[3,:],result[4,:]],
                                 dtype = 'float')
        hdf5_file.create_dataset("Efield", data = [result[6,:],result[7,:]],
                                 dtype = 'float')
        hdf5_file.create_dataset("tgrid", data = result[0,:], dtype = 'float')
        print("File saved successfully!")


###########################################################
# Plot result:
def plot_result(result):
    # Number of samplepoints
    N = np.shape(result)[1]

    # Time step
    T_step = result[0,1]-result[0,0]

    # Do Fast Fourier Transform
    yf1 = scipy.fftpack.fft(result[1,:])
    yf2 = scipy.fftpack.fft(result[2,:])

    # Time domain for FFT
    tf = np.linspace(0.0, 1.0/(2.0*T_step), N//2)

    T = tf[1]-tf[0]

    # Plot solution
    fig, ax = plt.subplots()
    ax.plot(tf, 2.0/N * np.abs(yf1[0:N//2]), label = r"$E_{dip1}$")
    ax.plot(tf, 2.0/N * np.abs(yf2[0:N//2]), label = r"$E_{dip2}$")

    # Setting ticks for dipole radiation
    omega_0 = 5.68000E-2/(2*np.pi)
    omegas = np.linspace(0, tf[-1], int(round(tf[-1]/omega_0)))
    ax.set_xticks(omegas)
    #ax.set_xticklabels([r"{}$\omega$".format(x) for x in range(0, omegas.shape[0])], fontsize=9)
    ax.set_xticklabels([x for x in range(0, omegas.shape[0])], fontsize = 9)
    plt.setp(ax.get_xticklabels()[0], visible = False)
    # shows odd harmonics:
    for i, odd_omeg in enumerate(omegas):
        if (i % 2) != 0:
            plt.axvline(x = odd_omeg, color = 'r', linestyle = ':',
                        linewidth = 0.5)

    # Setting legend and size
    ax.legend(loc = 1)
    ax.set_xlim(0, 0.5)
    ax.set_ylim(bottom = 10e-7)
    ax.set_ylabel(r"$E$", fontsize = 14)
    ax.set_xlabel(r"$\omega_0$", fontsize = 14)
    ax.set_title("Dipole radiation spectrum")
    plt.yscale('log')
    fig.set_size_inches(18.5, 5)
    plt.show()

    # Time domain for fields
    tf2 = np.linspace(0.0, T_step, N)

    # Plot fields
    fig2, ax2 = plt.subplots()
    ax2.plot(tf2, result[6,:])
    ax2.plot(tf2, result[7,:])
    ax2.set_title("Electric fields")
    plt.show()
