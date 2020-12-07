==============
Example of Use
==============

Let's give a simple example how to use the script.

Input and Computation
---------------------

After running the script we see the following: ::

    Type number of points for dipole evaluation:
    >> 1000

    Type number of points for integrals evaluation:
    >> 1000

    Type sense of polarisation of the first field (-1 anticlockwise, 1 clockwise):
    >> -1

    Type sense of polarisation of the second field (-1 anticlockwise, 1 clockwise):
    >> 1

    Type ellipticity of the first field between 0.0 and 1.0 (0.0 for linear polarisation):
    >> 0

    Type carrier envelope phase of the first field: 0.0 to 1.0:
    >> 0

    Type carrier envelope phase of the second field: 0.0 to 1.0:
    >> 0

    Type number of cycles in the envelope for the first field (must be greater than 0):
    >> 10

    Type second field frequency relative to the first field for multicolored fields (1, 2, 3, ...):
    >> 1

    Type relative delays between fields (between 0.0 and 1.0):
    >> 0.5

    Type deviation between pulses (0.0 to 1.0):
    >> 0

At this moment, the parameters have been accepted and the script proceeds to the most computational heavy part of the script by calling a function:

.. function:: main.sfa(parameters, result, N_points)

The function returns a numpy.array of computed values. The result is saved to the file 'result.h5'.


Plotting
--------

The result is processed using Fast Fourier Transform:

.. function:: scipy.fftpack.fft(result[i,:])

The output of this function is plotted using matplotlib library.

The resulting plots should look similiar to these:

.. image :: _build/html/images/omega.png
    :width: 400

.. image :: _build/html/images/E_fields.png
    :width: 400
