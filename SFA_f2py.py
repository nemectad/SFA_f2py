###########################################################
# Script: SFA_f2py                                        #
# Author: Tadeas Nemec, 2020                              #
# Email: nemectad@cvut.fjfi.cz                            #
# ******************************************************* #
# This Python script takes input field parameters for     #
# High harmonic frequency generation. It calls precom-    #
# piled Fortran code for corresponding computations.      #
#                                                         #
# The output is saved to file and can be further process- #
# ed and plotted in Python using matplotlib library       #
###########################################################

# Libraries import
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import h5py

# Importing code
import Fortran.main as main

###########################################################
# User input:

errFlag = 1

# Computation parameters (Higher numbers, slower computation):
try:
    print("Type number of points for dipole evaluation: ")
    N_pts = int(input())        
except:
    print("Invalid input, input must be integer!")
    errFlag = -1
    
if (errFlag != -1):
    try:
        print("Type number of points for integrals evaluation: ")
        N_int = int(input())
    except:
        print("Invalid input, input must be integer!")
        errFlag = -1

# Field parameters:

# sense of polarisation
if (errFlag != -1):
    try:
        print("Type sense of polarization of the first field (-1 anticlockwise, 1 clockwise): ")
        p1 = int(input())
    except:
        print("Invalid input, input must be integer!")
        errFlag = -1 

if (errFlag != -1):
    try:
        print("Type sense of polarization of the second field (-1 anticlockwise, 1 clockwise): ")
        p2 = int(input())
    except:
        print("Invalid input, input must be integer!")
        errFlag = -1 

# fields ellipticity
if (errFlag != -1):
    try:
        print("Type ellipticity of the first field between 0.0 and 1.0 (0.0 for linear polarisation):")
        eps = float(input())
        if (eps < 0.0 or eps > 1.0):
            print("Invalid input, input must be between 0.0 and 1.0!")
            errFlag = -1
    except:
        print("Invalid input, input must be float!")
        errFlag = -1 

# carrier envelope phases
if (errFlag != -1):
    try:
        print("Type carrier envelope phase of the first field: 0.0 to 1.0: ")
        phi1 = float(input())
        if (phi1 < 0.0 or phi1 > 1.0):
            print("Invalid input, input must be between 0.0 and 1.0!")
            errFlag = -1
    except:
        print("Invalid input, input must be float!")
        errFlag = -1 

if (errFlag != -1):
    try:
        print("Type carrier envelope phase of the second field: 0.0 to 1.0: ")
        phi2 = float(input())
        if (phi2 < 0.0 or phi2 > 1.0):
            print("Invalid input, input must be between 0.0 and 1.0!")
            errFlag = -1
    except:
        print("Invalid input, input must be float!")
        errFlag = -1 

# number of cycles in the first field:
if (errFlag != -1):
    try:
        print("Type number of cycles in the envelope for the first field (must be greater than 0): ")
        N_cycl = float(input())
        if (N_cycl < 0):
            print("Invalid input, input must be between greater greater than 0!")
            errFlag = -1
    except:
        print("Invalid input, input must be float!")
        errFlag = -1 

# field frequencies
if (errFlag != -1):
    try:
        print("Type second field frequency relative to the first field for multicolored fields (1, 2, 3, ...):")
        relOmega = int(input())
        if (relOmega < 1):
            print("Invalid input, input must be between greater or equal to 1!")
            errFlag = -1
    except:
        print("Invalid input, input must be integer!")
        errFlag = -1 

# relative delays
if (errFlag != -1):
    try:
        print("Type relative delays between fields (between 0.0 and 1.0): ")
        relDelay = float(input())
        if (relDelay < 0.0 or relDelay > 1.0):
            print("Invalid input, input must be between 0.0 and 1.0!")
            errFlag = -1
    except:
        print("Invalid input, input must be float!")
        errFlag = -1 
        
# deviation between pulses
if (errFlag != -1):
    try:
        print("Type deviation between pulses (0.0 to 1.0): ")
        theta = float(input())
        if (theta < 0.0 or theta > 1.0):
            print("Invalid input, input must be between 0.0 and 1.0!")
            errFlag = -1
    except:
        print("Invalid input, input must be float!")
        errFlag = -1 

if (errFlag != -1):
    parametersI = np.zeros((4), dtype=int)
    parametersR = np.zeros((5), dtype=float)
    parametersS = np.zeros((7), dtype=float)

    # polarization mode (p1), polarization mode (p2) (i.e. clockwise 
    # p = 1, anticlockwise p = -1)
    # num. of pts. for integral (N_int), num. of pts. for dipole(N_pts)
    parametersI = [p1, p2, N_int, N_pts]

    # Ionization potential in a.u. (Ip), Carrier envelope phase (phi1)
    # photon energy (\omega_01), Carrier envelope phase (phi2)
    # photon energy (\omega_02)
    parametersR = [0.5, phi1, 5.68000E-2, phi2, relOmega*5.68000E-2]

    # Electric field aplitude (E0), s default 1 (symmetrical fields)
    # (ineq default 0), El. field ellipticity (eps), Deviation (theta)
    # Rel. delay between pulses (Rel_delay), No. of cycles in envelope (N_cycl)
    parametersS = [0.750000E-01, 1.0, 0.0, eps, theta, relDelay, N_cycl]

    dim = int(2.0*parametersS[6]*parametersI[3])

    result = np.zeros((9,dim), dtype=float)


    # Main task
    try:
        result = main.sfa(parametersR, parametersI, parametersS, result, dim)
        print("Computation completed!")
    except:
        errFlag=-1
        print("Computation failed!")
        
    
    # Save to .h5 file
    try:
        with h5py.File("result.h5", "w") as hdf5_file:
            hdf5_file.create_dataset("dipole", data=[result[1,:],result[2,:]], dtype='float')
            hdf5_file.create_dataset("Afield", data=[result[3,:],result[4,:]], dtype='float')
            hdf5_file.create_dataset("Efield", data=[result[6,:],result[7,:]], dtype='float')
            hdf5_file.create_dataset("tgrid", data=result[0,:], dtype='float')
        print("File saved successfully!")
    except:
        errFlag=-2
        print("Unable to save .h5 file! Data will be plotted but will not be saved!")


    if (errFlag != -1):
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
        ax.legend(loc=1)
        ax.set_xlim(0, 0.5)
        ax.set_ylim(bottom = 10e-7)
        ax.set_title("Dipole radiation spectrum")
        plt.yscale('log')
        plt.show()

        # Time domain for fields
        tf2 = np.linspace(0.0, T_step, N)

        # Plot fields
        fig2, ax2 = plt.subplots()
        ax2.plot(tf2, result[6,:])
        ax2.plot(tf2, result[7,:])
        ax2.set_title("Electric fields")
        plt.show()

        errFlag = 0
    

print("Script returned with exit code {}".format(errFlag))
