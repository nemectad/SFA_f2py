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

import library


parameters = library.user_input()

result = library.compute(parameters)

library.save_to_H5file(result)

library.plot_result(result)
