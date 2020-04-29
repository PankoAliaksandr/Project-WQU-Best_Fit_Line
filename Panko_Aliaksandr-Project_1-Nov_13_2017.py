# Python 2.7.14
# Windows 7 x64

# Task Description:
# 1) Write a python program that prompts the user to enter any valid stock
#    symbol available in the sources for NYSE & NASDAQ.
#    Ensure proper error handling for wrong user inputs.
# 2) Download data for last 1 month for user entered ticker from the source.
# 3) Using Interpolation techniques, fit a quadratic line through the
#    data points and plot the same
# 4) Choose a quadratic equation of your choice and using SciPy leastsq()
#    optimization method calculate the best fit line with respect to
#    the downloaded data 
# 5) Plot the best fit line and the actual data points together with error bars.

# Importing Libraries
# $ pip install pandas-datareader

import datetime
import pandas as pd
from pandas_datareader import data as pdr
from pandas_datareader._utils import RemoteDataError
import numpy as np
import pylab
import scipy as sp


class Model:
        
    # Constructor
    def __init__(self):
        
        # Private attributes
        self.__df = pd.DataFrame() # store stock data
        self.__quadratic_func_values =  list() # interpolation function values 
        self.__leastsq_results = [] # optimal parameters
        self.__n = 0 # number of rows in data frame
        
    # User Input and Donwload Data
    def DownloadData(self):
        # Determine the first and the last days of the period
        end_date = datetime.date.today()
        start_date = datetime.date(end_date.year, end_date.month - 1, end_date.day)
        
        # User Input
        self.__df = pd.DataFrame()
        while(self.__df.empty):       
            ticker = raw_input("Enter a valid stock symbol: ")
            try:
                self.__df = pdr.get_data_yahoo(ticker, start = start_date, end = end_date)
            except RemoteDataError:
                # handle error
                print 'Stock symbol "{}" is not valid'.format(ticker)
        
        self.__n = len(self.__df.Close)
    
    # Fit a quadratic line (using a polynom degree 2) through the data points
    def Interpolate(self):
        
        # Find coefficients of polinom degree 2 which approximates data
        coefficients = np.polyfit(x = range(self.__n), y = self.__df.Close, deg = 2)
        # create a polynomial function of one argument
        fit_fun = np.poly1d (coefficients) 
        
        # Calculate approximational function values
        func_value = lambda x: fit_fun(x)
        # Allocate space
        self.__quadratic_func_values = np.empty(self.__n)
        
        for i in range(self.__n):
            self.__quadratic_func_values[i] = func_value(i)
            
    def PlotQuadraticLine(self):
    
        pylab.plot(range(self.__n), self.__quadratic_func_values,
                   label = "Interpolation Quadratic Line", color='blue' )
        pylab.plot(range(self.__n) ,self.__df.Close ,'d',
                   label='Original Data', color='red')
        pylab.ylabel('Stock Price')
        pylab.xlabel('Day number')
        pylab.legend()
        pylab.show()  
        
    def CalculateBestFitLine(self):
    
        # Based on coefficients array 'p' approximation function is created
        # and using argument 'x', approximation value is determined
        approx_function = lambda p, x: np.poly1d(p)(x)
        
        # Resudual function (difference between real value and approximation)
        residual = lambda p, x, y: (y - approx_function(p, x))
        
        # initial polinom degree 2 coefficients
        initial_coeff = np.array([1,2,3])
        
        optim_result = sp.optimize.leastsq( residual, initial_coeff,
                                    args=(range(self.__n), self.__df.Close))
        
        self.__leastsq_results = approx_function(optim_result[0], range(self.__n))
    
    def PlotBestFitLine(self):
        original = 'Original Data Points'
        
        pylab.errorbar( range(self.__n), self.__df.Close, yerr = 0.01 * self.__df.Close,
                       fmt = 'ko', label = original)
        
        best_fit = 'Best Fit'
        
        pylab.plot(range(self.__n), self.__leastsq_results, 'b--', lw = 2, 
                   label = best_fit )
        
        pylab.legend()
        pylab.show ()  
              
        
    # 
    def Main(self):
        self.DownloadData()
        self.Interpolate()
        self.PlotQuadraticLine()
        self.CalculateBestFitLine()
        self.PlotBestFitLine()

#-------------End of Class---------------------------------------------

# Create the instance of a class
model = Model()
# Call Main function of a class
model.Main()        
        
        