import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def make_plot(data_filename):
    #takes csv and plots graph of Power/dBm versus wavelength
    #takes in csv filename
    #does the plot
    data_to_plot=pd.read_csv(data_filename)
    fig1,axs1=plt.subplots()
    data_plot_array=data_to_plot.to_numpy(copy=True)
    xs=data_plot_array[:,0]
    ys=data_plot_array[:,1]
    axs1.plot(xs,ys)
    axs1.set_xlabel("Wavelength/dBm")
    axs1.set_ylabel("Power/dBm")
    plt.show()
    return

def make_plot_scatter(data_filename):
    #takes csv and plots graph of Power/dBm versus wavelength
    #takes in csv filename
    #does the plot
    data_to_plot=pd.read_csv(data_filename)
    fig1,axs1=plt.subplots()
    data_plot_array=data_to_plot.to_numpy(copy=True)
    xs=data_plot_array[:,0]
    ys=data_plot_array[:,1]
    axs1.scatter(xs,ys)
    axs1.set_xlabel("Wavelength/dBm")
    axs1.set_ylabel("Power/dBm")
    plt.show()
    return