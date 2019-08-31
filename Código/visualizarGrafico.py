import pandas as pd
import numpy as np
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator
from matplotlib import pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.patches import Patch
import datetime
import os.path

dir = os.getcwd()

#FUNCIONES
def mostrarGrafico(fechaInicio, fechaFin, archivo):
    fechaInicio = str(fechaInicio)
    fechaFin = str(fechaFin)
    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
    alldays = DayLocator()              # minor ticks on the days
    weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
    dayFormatter = DateFormatter('%d')      # e.g., 12

    quotes = pd.read_csv(archivo,index_col = "Date", parse_dates = True)

    quotes = quotes[(quotes.index >= fechaInicio) & (quotes.index <= fechaFin)]

    quotes_numpy = {
        'Open': np.array(quotes['Open'], dtype='float'),
        'High': np.array(quotes['High'], dtype='float'),
        'Low': np.array(quotes['Low'], dtype='float'),
        'Close': np.array(quotes['Close'], dtype='float'),
        'Volume': np.array(quotes['Volume'], dtype='int')
        }

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(weekFormatter)
    ax.xaxis.set_minor_formatter(dayFormatter)

    candlestick_ohlc(ax, zip(mdates.date2num(quotes.index.to_pydatetime()),
                         quotes['Open'], quotes['High'],
                         quotes['Low'], quotes['Close']),
                 width=0.9, colorup='g', colordown='r')

    ax.xaxis_date()
    ax.autoscale_view()
    plt.rcParams["figure.figsize"] = [16.0,4.8]

    plt.setp(plt.gca().get_xticklabels(), rotation=90, horizontalalignment='right')
    archivo=archivo.replace(".csv", "")
    archivo=archivo.replace(dir, "")
    archivo=archivo.replace("/", "")

    imagen = "grafica"
    imagen+=archivo
    imagen+=".png"
    plt.savefig(imagen)
    #plt.show()

    return imagen

def mostrarGraficoDataFrame(archivo, nombre, fechaInicio, fechaFin):
    fechaInicio = str(fechaInicio)
    fechaFin = str(fechaFin)
    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
    alldays = DayLocator()              # minor ticks on the days
    weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
    dayFormatter = DateFormatter('%d')      # e.g., 12

    quotes = archivo

    quotes = quotes[(quotes.index >= fechaInicio) & (quotes.index <= fechaFin)]

    quotes_numpy = {
        'Open': np.array(quotes['Open'], dtype='float'),
        'High': np.array(quotes['High'], dtype='float'),
        'Low': np.array(quotes['Low'], dtype='float'),
        'Close': np.array(quotes['Close'], dtype='float'),
        'Volume': np.array(quotes['Volume'], dtype='int')
        }

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(weekFormatter)
    ax.xaxis.set_minor_formatter(dayFormatter)

    candlestick_ohlc(ax, zip(mdates.date2num(quotes.index.to_pydatetime()),
                         quotes['Open'], quotes['High'],
                         quotes['Low'], quotes['Close']),
                 width=0.9, colorup='g', colordown='r')

    ax.xaxis_date()
    ax.autoscale_view()
    plt.rcParams["figure.figsize"] = [16.0,4.8]

    plt.setp(plt.gca().get_xticklabels(), rotation=90, horizontalalignment='right')


    imagen = "grafica"
    imagen+=nombre
    imagen+=".png"
    plt.savefig(imagen)
    #plt.show()

    return imagen
