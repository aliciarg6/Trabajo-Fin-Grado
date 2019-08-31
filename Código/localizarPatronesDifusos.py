import pandas as pd
import numpy as np
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator
from matplotlib import pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.patches import Patch
import datetime
import os.path

import difuso

dir = os.getcwd()

def hallarPatronesDifusos(fechaInicio, fechaFin, archivo, procedencia, contador):
    terminado = False
    suma = contador
    vela = False
    nombreVela="no-vela"
    pertenencia = []
    nomVelaPertenencia = []

    fechaInicio = str(fechaInicio)
    fechaFin = str(fechaFin)

    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
    alldays = DayLocator()              # minor ticks on the days
    weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
    dayFormatter = DateFormatter('%d')      # e.g., 12

    if procedencia=="csv":
        quotes = pd.read_csv(archivo,index_col = "Date", parse_dates = True)
    if procedencia=="menu":
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
    #ax.xaxis.set_minor_locator(alldays)
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

    #Analisis de Patrones
    i=0
    delta = float(0.0)
    while i<len(quotes['Open']) and vela==False and terminado==False :

        encontrado=False
        if i>3:
            if round(difuso.formacionConGapBajistaDifusa(aper1=quotes['Open'][i-4], cierre1=quotes['Close'][i-4], aper2=quotes['Open'][i-3], cierre2=quotes['Close'][i-3], aper3=quotes['Open'][i-2], cierre3=quotes['Close'][i-2], aper4=quotes['Open'][i-1], cierre4=quotes['Close'][i-1], aper5=quotes['Open'][i], cierre5=quotes['Close'][i],
            fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Formación con Gap Bajista Difusa")
                print("Tendencia Bajista (Continuación)")
                print(quotes.index[i])

                vela=True
                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.formacionConGapBajistaDifusa(aper1=quotes['Open'][i-4], cierre1=quotes['Close'][i-4], aper2=quotes['Open'][i-3], cierre2=quotes['Close'][i-3], aper3=quotes['Open'][i-2], cierre3=quotes['Close'][i-2], aper4=quotes['Open'][i-1], cierre4=quotes['Close'][i-1], aper5=quotes['Open'][i], cierre5=quotes['Close'][i],
                    fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("fgb")
                    if encontrado==False:
                        if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0 or quotes.index[i-2].weekday()==0 or quotes.index[i-3].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=4.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

            if round(difuso.formacionConGapAlcistaDifusa(aper1=quotes['Open'][i-4], cierre1=quotes['Close'][i-4], aper2=quotes['Open'][i-3], cierre2=quotes['Close'][i-3], aper3=quotes['Open'][i-2], cierre3=quotes['Close'][i-2], aper4=quotes['Open'][i-1], cierre4=quotes['Close'][i-1], aper5=quotes['Open'][i], cierre5=quotes['Close'][i],
            fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Formación con Gap Alcista Difusa")
                print("Tendencia Alcista (Continuación)")
                print(quotes.index[i])

                vela=True
                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.formacionConGapAlcistaDifusa(aper1=quotes['Open'][i-4], cierre1=quotes['Close'][i-4], aper2=quotes['Open'][i-3], cierre2=quotes['Close'][i-3], aper3=quotes['Open'][i-2], cierre3=quotes['Close'][i-2], aper4=quotes['Open'][i-1], cierre4=quotes['Close'][i-1], aper5=quotes['Open'][i], cierre5=quotes['Close'][i],
                    fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("fga")
                    if encontrado==False:
                        if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0 or quotes.index[i-2].weekday()==0 or quotes.index[i-3].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=4.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

            if round(difuso.matHoldDifusa(aper1=quotes['Open'][i-4], cierre1=quotes['Close'][i-4], aper2=quotes['Open'][i-3], cierre2=quotes['Close'][i-3], aper3=quotes['Open'][i-2], cierre3=quotes['Close'][i-2], aper4=quotes['Open'][i-1], cierre4=quotes['Close'][i-1], aper5=quotes['Open'][i], cierre5=quotes['Close'][i],
            fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Mat Hold Difusa")
                print("Tendencia Alcista (Continuación)")
                print(quotes.index[i])
                vela=True
                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.matHoldDifusa(aper1=quotes['Open'][i-4], cierre1=quotes['Close'][i-4], aper2=quotes['Open'][i-3], cierre2=quotes['Close'][i-3], aper3=quotes['Open'][i-2], cierre3=quotes['Close'][i-2], aper4=quotes['Open'][i-1], cierre4=quotes['Close'][i-1], aper5=quotes['Open'][i], cierre5=quotes['Close'][i],
                    fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("mh")
                    if encontrado==False:
                        if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0 or quotes.index[i-2].weekday()==0 or quotes.index[i-3].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=4.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

            if round(difuso.tripleFormacionAlcistaDifusa(aper1=quotes['Open'][i-4], cierre1=quotes['Close'][i-4], aper2=quotes['Open'][i-3], cierre2=quotes['Close'][i-3], aper3=quotes['Open'][i-2], cierre3=quotes['Close'][i-2], aper4=quotes['Open'][i-1], cierre4=quotes['Close'][i-1], aper5=quotes['Open'][i], cierre5=quotes['Close'][i],
            fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Triple Formacion Alcista Difusa")
                print("Tendencia Alcista (Continuación)")
                print(quotes.index[i])

                vela=True
                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.tripleFormacionAlcistaDifusa(aper1=quotes['Open'][i-4], cierre1=quotes['Close'][i-4], aper2=quotes['Open'][i-3], cierre2=quotes['Close'][i-3], aper3=quotes['Open'][i-2], cierre3=quotes['Close'][i-2], aper4=quotes['Open'][i-1], cierre4=quotes['Close'][i-1], aper5=quotes['Open'][i], cierre5=quotes['Close'][i],
                    fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("tfa")
                    if encontrado==False:
                        if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0 or quotes.index[i-2].weekday()==0 or quotes.index[i-3].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=4.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

            if round(difuso.tripleFormacionBajistaDifusa(aper1=quotes['Open'][i-4], cierre1=quotes['Close'][i-4], aper2=quotes['Open'][i-3], cierre2=quotes['Close'][i-3], aper3=quotes['Open'][i-2], cierre3=quotes['Close'][i-2], aper4=quotes['Open'][i-1], cierre4=quotes['Close'][i-1], aper5=quotes['Open'][i], cierre5=quotes['Close'][i],
            fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Triple Formacion Alcista Difusa")
                print("Tendencia Alcista (Continuación)")
                print(quotes.index[i])
                vela=True
                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.tripleFormacionBajistaDifusa(aper1=quotes['Open'][i-4], cierre1=quotes['Close'][i-4], aper2=quotes['Open'][i-3], cierre2=quotes['Close'][i-3], aper3=quotes['Open'][i-2], cierre3=quotes['Close'][i-2], aper4=quotes['Open'][i-1], cierre4=quotes['Close'][i-1], aper5=quotes['Open'][i], cierre5=quotes['Close'][i],
                    fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("tfb")
                    if encontrado==False:
                        if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0 or quotes.index[i-2].weekday()==0 or quotes.index[i-3].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=4.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True
        if i>2:
            if round(difuso.pequeniaGolondrinaOcultadaDifusa(aper1=quotes['Open'][i-3], cierre1=quotes['Close'][i-3], alto1=quotes['High'][i-3], bajo1=quotes['Low'][i-3], aper2=quotes['Open'][i-2], cierre2=quotes['Close'][i-2], alto2=quotes['High'][i-2], bajo2=quotes['Low'][i-2], aper3=quotes['Open'][i-1], cierre3=quotes['Close'][i-1],
             alto3=quotes['High'][i-1], bajo3=quotes['Low'][i-1], aper4=quotes['Open'][i], cierre4=quotes['Close'][i], alto4=quotes['High'][i], bajo4=quotes['Low'][i],fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Pequeña Golondrina Oculta: ")
                print("Tendencia Alcista ")
                print(quotes.index[i])

                vela=True
                nombreVela="pgo"
                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.pequeniaGolondrinaOcultadaDifusa(aper1=quotes['Open'][i-3], cierre1=quotes['Close'][i-3], alto1=quotes['High'][i-3], bajo1=quotes['Low'][i-3], aper2=quotes['Open'][i-2], cierre2=quotes['Close'][i-2], alto2=quotes['High'][i-2], bajo2=quotes['Low'][i-2], aper3=quotes['Open'][i-1], cierre3=quotes['Close'][i-1],
                     alto3=quotes['High'][i-1], bajo3=quotes['Low'][i-1], aper4=quotes['Open'][i], cierre4=quotes['Close'][i], alto4=quotes['High'][i], bajo4=quotes['Low'][i],fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia ))
                    nomVelaPertenencia.append("pgo")
                    if encontrado==False:
                        if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0 or quotes.index[i-2].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=3.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

        if i>1:
            if round(difuso.dosCuervosEnGapAlcistaDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], aper3=quotes['Open'][i], cierre3=quotes['Close'][i],  fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Dos Cuervos en Gap Alcista Difusa: ")
                print("Tendencia Bajista ")
                print(quotes.index[i])

                vela=True
                nombreVela="dcga"
                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.dosCuervosEnGapAlcistaDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], aper3=quotes['Open'][i], cierre3=quotes['Close'][i],  fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("dcga")
                    if encontrado==False:
                        if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=2.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

            if round(difuso.tresSoldadosBlancosDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1], aper3=quotes['Open'][i], cierre3=quotes['Close'][i],
            alto3=quotes['High'][i], bajo3=quotes['Low'][i],fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Tres Soldados Blancos Difusa: ")
                print("Tendencia Alcista ")
                print(quotes.index[i])

                vela=True

                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.tresSoldadosBlancosDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1], aper3=quotes['Open'][i], cierre3=quotes['Close'][i],
                    alto3=quotes['High'][i], bajo3=quotes['Low'][i],fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia ))
                    nomVelaPertenencia.append("tsb")
                    if encontrado==False:
                        if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=2.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

            if round(difuso.tresCuervosNegrosDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1], aper3=quotes['Open'][i], cierre3=quotes['Close'][i],
            alto3=quotes['High'][i], bajo3=quotes['Low'][i],fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Tres Cuervos Negros Difusa: ")
                print("Tendencia Alcista ")
                print(quotes.index[i])

                vela=True

                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.tresCuervosNegrosDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1], aper3=quotes['Open'][i], cierre3=quotes['Close'][i],
                    alto3=quotes['High'][i], bajo3=quotes['Low'][i],fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("tcn")
                    if encontrado==False:
                        if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=2.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

            if round(difuso.bebeAbandonadoAlcistaDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], aper3=quotes['Open'][i], cierre3=quotes['Close'][i],  fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Bebe Abandonado Alcista Difusa: ")
                print("Tendencia Alcista ")
                print(quotes.index[i])

                vela=True

                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.bebeAbandonadoAlcistaDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], aper3=quotes['Open'][i], cierre3=quotes['Close'][i],  fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("baa")
                    if encontrado==False:
                        if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=2.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

            if round(difuso.bebeAbandonadoBajistaDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], aper3=quotes['Open'][i], cierre3=quotes['Close'][i],  fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Bebe Abandonado Bajista Difusa: ")
                print("Tendencia Bajista ")
                print(quotes.index[i])

                vela=True

                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.bebeAbandonadoBajistaDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], aper3=quotes['Open'][i], cierre3=quotes['Close'][i],  fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("bab")
                    if encontrado==False:
                        if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=2.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

            #Cambiar color de la sombra
            if round(difuso.estrellaVespertinaDojiDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1],
            aper3=quotes['Open'][i],cierre3=quotes['Close'][i], alto3=quotes['High'][i], bajo3=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Estrella Vespertina Doji Difusa: ")
                print("Tendencia Bajista ")
                print(quotes.index[i])

                vela=True

                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.estrellaVespertinaDojiDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1],
                    aper3=quotes['Open'][i],cierre3=quotes['Close'][i], alto3=quotes['High'][i], bajo3=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("evd")
                    if encontrado==False:
                        if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=2.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

            #Cambiar color de la sombra
            if round(difuso.estrellaDeLaManianaDojiDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1],
            aper3=quotes['Open'][i],cierre3=quotes['Close'][i], alto3=quotes['High'][i], bajo3=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Estrella de la Mañana Doji Difusa: ")
                print("Tendencia Alcista ")
                print(quotes.index[i])

                vela=True

                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.estrellaDeLaManianaDojiDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1],
                    aper3=quotes['Open'][i],cierre3=quotes['Close'][i], alto3=quotes['High'][i], bajo3=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("emd")

                    if encontrado==False:
                        if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=2.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True


            if round(difuso.estrellaDeLaManianaDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1],
            aper3=quotes['Open'][i],cierre3=quotes['Close'][i], alto3=quotes['High'][i], bajo3=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Estrella de la Mañana Difusa: ")
                print("Tendencia Alcista ")
                print(quotes.index[i])

                vela=True

                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.estrellaDeLaManianaDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1],
                    aper3=quotes['Open'][i],cierre3=quotes['Close'][i], alto3=quotes['High'][i], bajo3=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("em")

                    if encontrado==False:
                        if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=2.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

            #Cambiar color de la sombra
            if round(difuso.estrellaVespertinaDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1],
            aper3=quotes['Open'][i],cierre3=quotes['Close'][i], alto3=quotes['High'][i], bajo3=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Estrella Vespertina Difusa: ")
                print("Tendencia Bajista ")
                print(quotes.index[i])

                vela=True

                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.estrellaVespertinaDifusa(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1],
                    aper3=quotes['Open'][i],cierre3=quotes['Close'][i], alto3=quotes['High'][i], bajo3=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("ev")

                    if encontrado==False:
                        if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=2.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

        if i>0:
            if round(difuso.cozAlcistaDifusa(aperturaAct=quotes['Open'][i], cierreAct=quotes['Close'][i], aperturaAnt=quotes['Open'][i-1], cierreAnt=quotes['Close'][i-1], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Coz Alcista Difusa el día:")
                print(quotes.index[i])

                vela=True

                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.cozAlcistaDifusa(aperturaAct=quotes['Open'][i], cierreAct=quotes['Close'][i], aperturaAnt=quotes['Open'][i-1], cierreAnt=quotes['Close'][i-1], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("ca")

                    if encontrado==False:
                        if quotes.index[i].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=1.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

            if round(difuso.cozBajistaDifusa(aperturaAct=quotes['Open'][i], cierreAct=quotes['Close'][i], aperturaAnt=quotes['Open'][i-1], cierreAnt=quotes['Close'][i-1], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Coz Bajista Difusa el día:")
                print(quotes.index[i])

                vela=True

                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.cozBajistaDifusa(aperturaAct=quotes['Open'][i], cierreAct=quotes['Close'][i], aperturaAnt=quotes['Open'][i-1], cierreAnt=quotes['Close'][i-1], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("cb")

                    if encontrado==False:
                        if quotes.index[i].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=1.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

            if round(difuso.ventanaBajistaDifusa(aper1=quotes['Open'][i-1], cierre1=quotes['Close'][i-1], alto1=quotes['High'][i-1], bajo1=quotes['Low'][i-1], aper2=quotes['Open'][i], cierre2=quotes['Close'][i], alto2=quotes['High'][i], bajo2=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Ventana Bajista Difusa: ")
                print("Tendencia Bajista")
                print(quotes.index[i])

                vela=True

                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.ventanaBajistaDifusa(aper1=quotes['Open'][i-1], cierre1=quotes['Close'][i-1], alto1=quotes['High'][i-1], bajo1=quotes['Low'][i-1], aper2=quotes['Open'][i], cierre2=quotes['Close'][i], alto2=quotes['High'][i], bajo2=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("vb")

                    if encontrado==False:
                        if quotes.index[i].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=1.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

            if round(difuso.ventanaAlcistaDifusa(aper1=quotes['Open'][i-1], cierre1=quotes['Close'][i-1], alto1=quotes['High'][i-1], bajo1=quotes['Low'][i-1], aper2=quotes['Open'][i], cierre2=quotes['Close'][i], alto2=quotes['High'][i], bajo2=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Ventana Alcista Difusa: ")
                print("Tendencia Alcista")
                print(quotes.index[i])

                vela=True

                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.ventanaAlcistaDifusa(aper1=quotes['Open'][i-1], cierre1=quotes['Close'][i-1], alto1=quotes['High'][i-1], bajo1=quotes['Low'][i-1], aper2=quotes['Open'][i], cierre2=quotes['Close'][i], alto2=quotes['High'][i], bajo2=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("va")

                    if encontrado==False:
                        if quotes.index[i].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=1.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

            if round(difuso.envolventeAlcistaDifusa(aper1=quotes['Open'][i-1], cierre1=quotes['Close'][i-1], alto1=quotes['High'][i-1], bajo1=quotes['Low'][i-1], aper2=quotes['Open'][i], cierre2=quotes['Close'][i], alto2=quotes['High'][i],
             bajo2=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Envolvente Alcista Difusa: ")
                print("Tendencia Alcista")
                print(quotes.index[i])

                vela=True

                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.envolventeAlcistaDifusa(aper1=quotes['Open'][i-1], cierre1=quotes['Close'][i-1], alto1=quotes['High'][i-1], bajo1=quotes['Low'][i-1], aper2=quotes['Open'][i], cierre2=quotes['Close'][i], alto2=quotes['High'][i],
                     bajo2=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("ea")

                    if encontrado==False:
                        if quotes.index[i].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=1.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

            if round(difuso.envolventeBajistaDifusa(aper1=quotes['Open'][i-1], cierre1=quotes['Close'][i-1], alto1=quotes['High'][i-1], bajo1=quotes['Low'][i-1], aper2=quotes['Open'][i], cierre2=quotes['Close'][i], alto2=quotes['High'][i],
             bajo2=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0):
                print("Detectada Envolvente Bajista Difusa: ")
                print("Tendencia Bajista")
                print(quotes.index[i])

                vela=True

                if i<=contador:
                    vela=False
                else:
                    pertenencia.append(difuso.envolventeBajistaDifusa(aper1=quotes['Open'][i-1], cierre1=quotes['Close'][i-1], alto1=quotes['High'][i-1], bajo1=quotes['Low'][i-1], aper2=quotes['Open'][i], cierre2=quotes['Close'][i], alto2=quotes['High'][i],
                     bajo2=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                    nomVelaPertenencia.append("eb")

                    if encontrado==False:
                        if quotes.index[i].weekday()==0:
                            delta = float(2.0)
                        fechaInt=quotes.index[i]
                        inter = datetime.timedelta(days=0.4)
                        interNeg = datetime.timedelta(days=1.4+delta)
                        plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='yellow', alpha = 0.6)
                    encontrado=True

        #Patrones con una única vela

        if round(difuso.velaAlcistaGrandeDifusa(apertura=quotes['Open'][i], cierre=quotes['Close'][i], alto=quotes['High'][i], bajo=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0) and vela==False:
            print("Detectada Vela Alcista Grande Difusa el día: ")
            print(quotes.index[i])
            fechaInt=quotes.index[i]

            vela=True
            if i<=contador:
                vela=False
            else:
                pertenencia.append(difuso.velaAlcistaGrandeDifusa(apertura=quotes['Open'][i], cierre=quotes['Close'][i], alto=quotes['High'][i], bajo=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                nomVelaPertenencia.append("vag")
                if encontrado==False:
                    inter = datetime.timedelta(days=0.4)
                    plt.axvspan(fechaInt-inter, fechaInt+inter, facecolor='yellow', alpha = 0.5)
                encontrado=True


        if round(difuso.velaBajistaGrandeDifusa(apertura=quotes['Open'][i], cierre=quotes['Close'][i], alto=quotes['High'][i], bajo=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0) and vela==False:
            print("Detectada Vela Bajista Grande Difusa el día: ")
            print(quotes.index[i])

            vela=True
            if i<=contador:
                vela=False
            else:
                pertenencia.append(difuso.velaBajistaGrandeDifusa(apertura=quotes['Open'][i], cierre=quotes['Close'][i], alto=quotes['High'][i], bajo=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                nomVelaPertenencia.append("vbg")
                if encontrado==False:
                    fechaInt=quotes.index[i]
                    inter = datetime.timedelta(days=0.4)
                    plt.axvspan(fechaInt-inter, fechaInt+inter, facecolor='yellow', alpha = 0.5)
                encontrado=True


        if round(difuso.dojiSombrillaDifusa(aper1=quotes['Open'][i], cierre1=quotes['Close'][i], alto1=quotes['High'][i], bajo1=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0) and vela==False:
            print("Detectada Vela Doji Sombrilla Difusa: ")
            print("Tendencia Alcista")
            print(quotes.index[i])

            vela=True
            if i<=contador:
                vela=False
            else:
                pertenencia.append(difuso.dojiSombrillaDifusa(aper1=quotes['Open'][i], cierre1=quotes['Close'][i], alto1=quotes['High'][i], bajo1=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                nomVelaPertenencia.append("ds")
                if encontrado==False:
                    fechaInt=quotes.index[i]
                    inter = datetime.timedelta(days=0.4)
                    plt.axvspan(fechaInt-inter, fechaInt+inter, facecolor='yellow', alpha = 0.5)
                encontrado=True


        #Cambiar color de la sombra
        if round(difuso.dojiSombrillaInvertidaDifusa(aper1=quotes['Open'][i], cierre1=quotes['Close'][i], alto1=quotes['High'][i], bajo1=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0) and vela==False:
            print("Detectada Vela Doji Sombrilla Invertida Difusa: ")
            print("Tendencia Bajista")
            print(quotes.index[i])

            vela=True
            if i<=contador:
                vela=False
            else:
                pertenencia.append(difuso.dojiSombrillaInvertidaDifusa(aper1=quotes['Open'][i], cierre1=quotes['Close'][i], alto1=quotes['High'][i], bajo1=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                nomVelaPertenencia.append("dsi")
                if encontrado==False:
                    fechaInt=quotes.index[i]
                    inter = datetime.timedelta(days=0.4)
                    plt.axvspan(fechaInt-inter, fechaInt+inter, facecolor='yellow', alpha = 0.5)
                encontrado=True

        if round(difuso.hombreColgadoDifusa(aper1=quotes['Open'][i], cierre1=quotes['Close'][i], alto1=quotes['High'][i], bajo1=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia),2)>float(0.0) and vela==False:
            print("Detectada Vela Hombre Colgado Difusa: ")
            print("Tendencia Bajista")
            print(quotes.index[i])

            vela=True
            if i<=contador:
                vela=False
            else:
                pertenencia.append(difuso.hombreColgadoDifusa(aper1=quotes['Open'][i], cierre1=quotes['Close'][i], alto1=quotes['High'][i], bajo1=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia))
                nomVelaPertenencia.append("hc")
                if encontrado==False:
                    fechaInt=quotes.index[i]
                    inter = datetime.timedelta(days=0.4)
                    plt.axvspan(fechaInt-inter, fechaInt+inter, facecolor='yellow', alpha = 0.5)
                encontrado=True

        suma=i
        i=i+1

        if i== len(quotes['Open']):
            terminado = True



    contador=suma
    if len(quotes['Open']) == suma:
        terminado = True


    if procedencia=="csv":
        archivo=archivo.replace(".csv", "")
        archivo=archivo.replace(dir, "")
        archivo=archivo.replace("/", "")
        imagen = "grafica"
        imagen+=archivo
        imagen+="analisis"
        imagen+=".png"
    else:
        imagen = "grafica"
        imagen+="analisis"
        imagen+=".png"

    plt.savefig(imagen)
    return imagen, terminado, contador, nomVelaPertenencia, pertenencia
