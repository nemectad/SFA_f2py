# Libraries import
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import h5py
# Importing Fortran code
import Fortran.main as main


###########################################################
# User input:
def userInput():
    # Computation parameters (Higher numbers, slower computation):
    try:
        print("Type number of points for dipole evaluation: ")
        N_pts = int(input())
    except TypeError:
        print("Invalid input!")

    try:
        print("Type number of points for integrals evaluation: ")
        N_int = int(input())
    except TypeError:
        print("Invalid input!")

    # Field parameters:

    # sense of polarisation
    try:
        print("Type sense of polarization of the first field "
              "(-1 anticlockwise, 1 clockwise): ")
        p1 = int(input())
        if (not(p1 == -1 or p1 == 1)):
            raise ValueError("Invalid input, input must be either 1 or -1!")
    except TypeError:
        print("Invalid input!")

    try:
        print("Type sense of polarization of the second field "
              "(-1 anticlockwise, 1 clockwise): ")
        p2 = int(input())
        if (not(p2 == -1 or p2 == 1)):
            raise ValueError("Invalid input, input must be either 1 or -1!")
    except TypeError:
        print("Invalid input!")

    # fields ellipticity
    try:
        print("Type ellipticity of the first field between 0.0"
              "and 1.0 (0.0 for linear polarisation):")
        eps = float(input())
        if (eps < 0.0 or eps > 1.0):
            raise ValueError("Invalid input, input must be between 0.0 and 1.0!")
    except TypeError:
        print("Invalid input!")

    # carrier envelope phases
    try:
        print("Type carrier envelope phase of the first field: "
              "0.0 to 1.0: ")
        phi1 = float(input())
        if (phi1 < 0.0 or phi1 > 1.0):
            raise ValueError("Invalid input, input must be between 0.0 and 1.0!")
    except TypeError:
        print("Invalid input!")

    try:
        print("Type carrier envelope phase of the second field: "
              "0.0 to 1.0: ")
        phi2 = float(input())
        if (phi2 < 0.0 or phi2 > 1.0):
            raise ValueError("Invalid input, input must be between 0.0 and 1.0!")
    except TypeError:
        print("Invalid input!")

    # number of cycles in the first field:
    try:
        print("Type number of cycles in the envelope for the first field "
              "(must be greater than 0): ")
        N_cycl = float(input())
        if (N_cycl < 0):
            raise ValueError("Invalid input, input must be greater than 0!")
    except TypeError:
        print("Invalid input!")

    # field frequencies
    try:
        print("Type second field frequency relative to the first field "
              "for multicolored fields (1, 2, 3, ...):")
        relOmega = int(input())
        if (relOmega < 1):
            raise ValueError("Invalid input, input must be between greater or "
                             "equal to 1!")
    except TypeError:
        print("Invalid input!")

    # relative delays
    try:
        print("Type relative delays between fields (between 0.0 and 1.0): ")
        relDelay = float(input())
        if (relDelay < 0.0 or relDelay > 1.0):
            raise ValueError("Invalid input, input must be between 0.0 and 1.0!")
    except TypeError:
        print("Invalid input!")

    # deviation between pulses
    try:
        print("Type deviation between pulses (0.0 to 1.0): ")
        theta = float(input())
        if (theta < 0.0 or theta > 1.0):
            raise ValueError("Invalid input, input must be between 0.0 and 1.0!")
    except TypeError:
        print("Invalid input!")


    # polarization mode (p1), polarization mode (p2) (i.e. clockwise
    # p = 1, anticlockwise p = -1)
    # num. of pts. for integral (N_int), num. of pts. for dipole(N_pts)
    integerParameters = np.array([p1, p2, N_int, N_pts], dtype=int)
    # Ionization potential in a.u. (Ip), Carrier envelope phase (phi1)
    # photon energy (\omega_01), Carrier envelope phase (phi2)
    # photon energy (\omega_02)
    realParameters = np.array([0.5, phi1, 5.68000E-2, phi2,
                               relOmega*5.68000E-2], dtype=float)
    # Electric field aplitude (E0), s default 1 (symmetrical fields)
    # (ineq default 0), El. field ellipticity (eps), Deviation (theta)
    # Rel. delay between pulses (Rel_delay), No. of cycles in envelope (N_cycl)
    sParameters = np.array([0.750000E-01, 1.0, 0.0, eps, theta, relDelay,
                            N_cycl], dtype=float)

    dim = int(2.0*sParameters[6]*integerParameters[3])

    return [realParameters, integerParameters, sParameters, dim]


###########################################################
# Compute result:
def compute(parameters):
    # Testing input
    assert np.shape(parameters[0])[0] == 5
    assert np.shape(parameters[1])[0] == 4
    assert np.shape(parameters[2])[0] == 7
    assert isinstance(parameters[3], int)


    # Result array
    result = np.zeros((9,parameters[3]), dtype=float)

    print("\n"
          "Hold on, it will take a while...")

    # Main task
    result = main.sfa(parameters[0], parameters[1], parameters[2],
                      result, parameters[3])
    print("Computation completed!")

    return result


###########################################################
# Save to file:
def saveToH5File(result):
    # Save to .h5 file
    with h5py.File("result.h5", "w") as hdf5_file:
        hdf5_file.create_dataset("dipole", data=[result[1,:],result[2,:]],
                                 dtype='float')
        hdf5_file.create_dataset("Afield", data=[result[3,:],result[4,:]],
                                 dtype='float')
        hdf5_file.create_dataset("Efield", data=[result[6,:],result[7,:]],
                                 dtype='float')
        hdf5_file.create_dataset("tgrid", data=result[0,:], dtype='float')
        print("File saved successfully!")


###########################################################
# Plot result:
def plotResult(result):
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
    ax.plot(tf, 2.0/N * np.abs(yf1[0:N//2]), label=r"$E_{dip1}$")
    ax.plot(tf, 2.0/N * np.abs(yf2[0:N//2]), label=r"$E_{dip2}$")

    # Setting ticks for dipole radiation
    omega_0 = 5.68000E-2/(2*np.pi)
    omegas = np.linspace(0, tf[-1], int(round(tf[-1]/omega_0)))
    ax.set_xticks(omegas)
    #ax.set_xticklabels([r"{}$\omega$".format(x) for x in range(0, omegas.shape[0])], fontsize=9)
    ax.set_xticklabels([x for x in range(0, omegas.shape[0])], fontsize=9)
    plt.setp(ax.get_xticklabels()[0], visible=False)
    # shows odd harmonics:
    for i, oddOmeg in enumerate(omegas):
        if (i % 2) != 0:
            plt.axvline(x=oddOmeg, color='r', linestyle=':', linewidth=0.5)


    # Setting legend and size
    ax.legend(loc=1)
    ax.set_xlim(0, 0.5)
    ax.set_ylim(bottom = 10e-7)
    ax.set_ylabel(r"$E$", fontsize=14)
    ax.set_xlabel(r"$\omega_0$", fontsize=14)
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
