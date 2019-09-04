import pandas as pd
import numpy as np
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator
from matplotlib import pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.patches import Patch
import datetime
import os.path

import patrones

dir = os.getcwd()

def hallarPatrones(fechaInicio, fechaFin, archivo, procedencia, contador):
    terminado = False
    suma = contador
    vela = False
    nombreVela="no-vela"

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
    #Leyenda
    l1 = Patch(facecolor='maroon', label='Formación con Gap Bajista', alpha = 0.8)
    l2 = Patch(facecolor='brown', label='Formación con Gap Alcista', alpha = 0.8)
    l3 = Patch(facecolor='sienna', label='MatHold', alpha = 0.8)
    l4 = Patch(facecolor='chocolate', label='Triple Formación Alcista', alpha = 0.8)
    l5 = Patch(facecolor='sandybrown', label='Triple Formación Bajista', alpha = 0.8)

    l6 = Patch(facecolor='navy', label='Pequeña Golondrina Oculta', alpha = 0.75)

    l7 = Patch(facecolor='mediumseagreen', label='Dos Cuervos en Gap Alcista', alpha = 0.7)
    l8 = Patch(facecolor='olive', label='Tres Soldados Blancos', alpha = 0.7)
    l9 = Patch(facecolor='springgreen', label='Tres Cuervos Negros', alpha = 0.7)
    l10 = Patch(facecolor='green', label='Bebe Abandonado Alcista', alpha = 0.7)
    l11 = Patch(facecolor='forestgreen', label='Bebe Abandonado Bajista', alpha = 0.7)
    l12 = Patch(facecolor='lime', label='Estrella Vespertina Doji', alpha = 0.7)
    l13 = Patch(facecolor='darkseagreen', label='Estrella de la Mañana Doji', alpha = 0.7)
    l14 = Patch(facecolor='greenyellow', label='Estrella de la Mañana', alpha = 0.7)
    l15 = Patch(facecolor='darkcyan', label='Estrella Vespertina', alpha = 0.7)

    l16 = Patch(facecolor='pink', label='Coz Alcista', alpha = 0.6)
    l17 = Patch(facecolor='hotpink', label='Coz Bajista', alpha = 0.6)
    l18 = Patch(facecolor='magenta', label='Ventana Bajista', alpha = 0.6)
    l19 = Patch(facecolor='purple', label='Ventana Alcista', alpha = 0.6)
    l20 = Patch(facecolor='indigo', label='Envolvente Alcista', alpha = 0.6)
    l21 = Patch(facecolor='plum', label='Envolvente Bajista', alpha = 0.6)

    l22 = Patch(facecolor='g', label='Vela Alcista Grande', alpha = 0.5)
    l23 = Patch(facecolor='r', label='Vela Bajista Grande', alpha = 0.5)
    l24 = Patch(facecolor='yellow', label='Hombre Colgado', alpha = 0.5)
    l25 = Patch(facecolor='orange', label='Doji Sombrilla', alpha = 0.5)
    l26 = Patch(facecolor='gray', label='Doji Sombrilla Invertida', alpha = 0.5)

    #Situar la leyenda
    plt.legend(loc='upper center', ncol=8, handles=[l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,l13,l14,l15,l16,l17,l18,l19,l20,l21,l22,l23,l24,l25,l26], borderaxespad=-6.0, shadow=True, fontsize='x-small')


    #Analisis de Patrones
    i=0
    delta = float(0.0)
    while i<len(quotes['Open']) and vela==False and terminado==False :

        encontrado=False
        if i>3:
            if patrones.formacionConGapBajista(aper1=quotes['Open'][i-4], cierre1=quotes['Close'][i-4], aper2=quotes['Open'][i-3], cierre2=quotes['Close'][i-3], aper3=quotes['Open'][i-2], cierre3=quotes['Close'][i-2], aper4=quotes['Open'][i-1], cierre4=quotes['Close'][i-1], aper5=quotes['Open'][i], cierre5=quotes['Close'][i],
            fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Formación con Gap Bajista")
                print("Tendencia Bajista (Continuación)")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="fgb"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0 or quotes.index[i-2].weekday()==0 or quotes.index[i-3].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=4.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='maroon', alpha = 0.8)

            if patrones.formacionConGapAlcista(aper1=quotes['Open'][i-4], cierre1=quotes['Close'][i-4], aper2=quotes['Open'][i-3], cierre2=quotes['Close'][i-3], aper3=quotes['Open'][i-2], cierre3=quotes['Close'][i-2], aper4=quotes['Open'][i-1], cierre4=quotes['Close'][i-1], aper5=quotes['Open'][i], cierre5=quotes['Close'][i],
            fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Formación con Gap Alcista")
                print("Tendencia Alcista (Continuación)")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="fga"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0 or quotes.index[i-2].weekday()==0 or quotes.index[i-3].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=4.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='brown', alpha = 0.8)

            if patrones.matHold(aper1=quotes['Open'][i-4], cierre1=quotes['Close'][i-4], aper2=quotes['Open'][i-3], cierre2=quotes['Close'][i-3], aper3=quotes['Open'][i-2], cierre3=quotes['Close'][i-2], aper4=quotes['Open'][i-1], cierre4=quotes['Close'][i-1], aper5=quotes['Open'][i], cierre5=quotes['Close'][i],
            fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Mat Hold")
                print("Tendencia Alcista (Continuación)")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="mh"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0 or quotes.index[i-2].weekday()==0 or quotes.index[i-3].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=4.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='sienna', alpha = 0.8)

            if patrones.tripleFormacionAlcista(aper1=quotes['Open'][i-4], cierre1=quotes['Close'][i-4], aper2=quotes['Open'][i-3], cierre2=quotes['Close'][i-3], aper3=quotes['Open'][i-2], cierre3=quotes['Close'][i-2], aper4=quotes['Open'][i-1], cierre4=quotes['Close'][i-1], aper5=quotes['Open'][i], cierre5=quotes['Close'][i],
            fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia) == True:
                '''
                print("Detectada Triple Formacion Alcista")
                print("Tendencia Alcista (Continuación)")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="tfa"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0 or quotes.index[i-2].weekday()==0 or quotes.index[i-3].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=4.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='chocolate', alpha = 0.8)

            if patrones.tripleFormacionBajista(aper1=quotes['Open'][i-4], cierre1=quotes['Close'][i-4], aper2=quotes['Open'][i-3], cierre2=quotes['Close'][i-3], aper3=quotes['Open'][i-2], cierre3=quotes['Close'][i-2], aper4=quotes['Open'][i-1], cierre4=quotes['Close'][i-1], aper5=quotes['Open'][i], cierre5=quotes['Close'][i],
            fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia) == True:
                '''
                print("Detectada Triple Formacion Alcista")
                print("Tendencia Alcista (Continuación)")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="tfb"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0 or quotes.index[i-2].weekday()==0 or quotes.index[i-3].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=4.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='sandybrown', alpha = 0.8)

        if i>2 and encontrado==False:
            if patrones.pequeniaGolondrinaOcultada(aper1=quotes['Open'][i-3], cierre1=quotes['Close'][i-3], alto1=quotes['High'][i-3], bajo1=quotes['Low'][i-3], aper2=quotes['Open'][i-2], cierre2=quotes['Close'][i-2], alto2=quotes['High'][i-2], bajo2=quotes['Low'][i-2], aper3=quotes['Open'][i-1], cierre3=quotes['Close'][i-1],
             alto3=quotes['High'][i-1], bajo3=quotes['Low'][i-1], aper4=quotes['Open'][i], cierre4=quotes['Close'][i], alto4=quotes['High'][i], bajo4=quotes['Low'][i],fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia )==True:
                '''
                print("Detectada Pequeña Golondrina Oculta: ")
                print("Tendencia Alcista ")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="pgo"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0 or quotes.index[i-2].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=3.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='navy', alpha = 0.75)

        if i>1 and encontrado==False:
            if patrones.dosCuervosEnGapAlcista(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], aper3=quotes['Open'][i], cierre3=quotes['Close'][i],  fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Dos Cuervos en Gap Alcista: ")
                print("Tendencia Bajista ")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="dcga"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=2.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='mediumseagreen', alpha = 0.7)

            if patrones.tresSoldadosBlancos(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1], aper3=quotes['Open'][i], cierre3=quotes['Close'][i],
            alto3=quotes['High'][i], bajo3=quotes['Low'][i],fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia )==True:
                '''
                print("Detectada Tres Soldados Blancos: ")
                print("Tendencia Alcista ")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="tsb"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=2.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='olive', alpha = 0.7)

            if patrones.tresCuervosNegros(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1], aper3=quotes['Open'][i], cierre3=quotes['Close'][i],
            alto3=quotes['High'][i], bajo3=quotes['Low'][i],fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Tres Cuervos Negros: ")
                print("Tendencia Alcista ")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="tcn"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=2.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='springgreen', alpha = 0.7)

            if patrones.bebeAbandonadoAlcista(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], aper3=quotes['Open'][i], cierre3=quotes['Close'][i],  fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Bebe Abandonado Alcista: ")
                print("Tendencia Alcista ")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="baa"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=2.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='green', alpha = 0.7)

            if patrones.bebeAbandonadoBajista(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], aper3=quotes['Open'][i], cierre3=quotes['Close'][i],  fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Bebe Abandonado Bajista: ")
                print("Tendencia Bajista ")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="bab"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=2.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='forestgreen', alpha = 0.7)

            #Cambiar color de la sombra
            if patrones.estrellaVespertinaDoji(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1],
            aper3=quotes['Open'][i],cierre3=quotes['Close'][i], alto3=quotes['High'][i], bajo3=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Estrella Vespertina Doji: ")
                print("Tendencia Bajista ")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="evd"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=2.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='lime', alpha = 0.7)

            #Cambiar color de la sombra
            if patrones.estrellaDeLaManianaDoji(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1],
            aper3=quotes['Open'][i],cierre3=quotes['Close'][i], alto3=quotes['High'][i], bajo3=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Estrella de la Mañana Doji: ")
                print("Tendencia Alcista ")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="emd"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=2.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='darkseagreen', alpha = 0.7)

            #Cambiar color de la sombra
            if patrones.estrellaDeLaManiana(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1],
            aper3=quotes['Open'][i],cierre3=quotes['Close'][i], alto3=quotes['High'][i], bajo3=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Estrella de la Mañana: ")
                print("Tendencia Alcista ")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="em"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=2.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='greenyellow', alpha = 0.7)

            #Cambiar color de la sombra
            if patrones.estrellaVespertina(aper1=quotes['Open'][i-2], cierre1=quotes['Close'][i-2], alto1=quotes['High'][i-2], bajo1=quotes['Low'][i-2], aper2=quotes['Open'][i-1], cierre2=quotes['Close'][i-1], alto2=quotes['High'][i-1], bajo2=quotes['Low'][i-1],
            aper3=quotes['Open'][i],cierre3=quotes['Close'][i], alto3=quotes['High'][i], bajo3=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Estrella Vespertina: ")
                print("Tendencia Bajista ")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="ev"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0 or quotes.index[i-1].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=2.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='darkcyan', alpha = 0.7)



        if i>0 and encontrado==False:
            if patrones.cozAlcista(aperturaAct=quotes['Open'][i], cierreAct=quotes['Close'][i], aperturaAnt=quotes['Open'][i-1], cierreAnt=quotes['Close'][i-1], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Coz Alcista el día:")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="ca"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=1.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='pink', alpha = 0.6)


            if patrones.cozBajista(aperturaAct=quotes['Open'][i], cierreAct=quotes['Close'][i], aperturaAnt=quotes['Open'][i-1], cierreAnt=quotes['Close'][i-1], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Coz Bajista el día:")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="cb"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=1.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='hotpink', alpha = 0.6)

            if patrones.ventanaBajista(aper1=quotes['Open'][i-1], cierre1=quotes['Close'][i-1], alto1=quotes['High'][i-1], bajo1=quotes['Low'][i-1], aper2=quotes['Open'][i], cierre2=quotes['Close'][i], alto2=quotes['High'][i], bajo2=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Ventana Bajista: ")
                print("Tendencia Bajista")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="vb"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=1.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='magenta', alpha = 0.6)


            if patrones.ventanaAlcita(aper1=quotes['Open'][i-1], cierre1=quotes['Close'][i-1], alto1=quotes['High'][i-1], bajo1=quotes['Low'][i-1], aper2=quotes['Open'][i], cierre2=quotes['Close'][i], alto2=quotes['High'][i], bajo2=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Ventana Alcista: ")
                print("Tendencia Alcista")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="va"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=1.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='purple', alpha = 0.6)

            if patrones.envolventeAlcista(aper1=quotes['Open'][i-1], cierre1=quotes['Close'][i-1], alto1=quotes['High'][i-1], bajo1=quotes['Low'][i-1], aper2=quotes['Open'][i], cierre2=quotes['Close'][i], alto2=quotes['High'][i],
             bajo2=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Envolvente Alcista: ")
                print("Tendencia Alcista")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="ea"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=1.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='indigo', alpha = 0.6)

            #Cambiar color de la sombra
            if patrones.envolventeBajista(aper1=quotes['Open'][i-1], cierre1=quotes['Close'][i-1], alto1=quotes['High'][i-1], bajo1=quotes['Low'][i-1], aper2=quotes['Open'][i], cierre2=quotes['Close'][i], alto2=quotes['High'][i],
             bajo2=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True:
                '''
                print("Detectada Envolvente Bajista: ")
                print("Tendencia Bajista")
                print(quotes.index[i])
                '''
                encontrado=True
                vela=True
                nombreVela="eb"
                if i<=contador:
                    vela=False

                fechaInt=quotes.index[i]
                if quotes.index[i].weekday()==0:
                    delta = float(2.0)
                inter = datetime.timedelta(days=0.4)
                interNeg = datetime.timedelta(days=1.4+delta)
                plt.axvspan(fechaInt-interNeg, fechaInt+inter, facecolor='plum', alpha = 0.6)



        if patrones.velaAlcistaGrande(apertura=quotes['Open'][i], cierre=quotes['Close'][i], alto=quotes['High'][i], bajo=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True and encontrado==False:
            '''
            print("Detectada Vela Alcista Grande el día: ")
            print(quotes.index[i])
            '''
            fechaInt=quotes.index[i]
            encontrado=True
            vela=True
            nombreVela="vag"
            if i<=contador:
                vela=False
            inter = datetime.timedelta(days=0.4)
            plt.axvspan(fechaInt-inter, fechaInt+inter, facecolor='g', alpha = 0.5)
        if patrones.velaBajistaGrande(apertura=quotes['Open'][i], cierre=quotes['Close'][i], alto=quotes['High'][i], bajo=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True and encontrado==False:
            '''
            print("Detectada Vela Bajista Grande el día: ")
            print(quotes.index[i])
            '''
            encontrado=True
            vela=True
            nombreVela="vbg"
            if i<=contador:
                vela=False
            fechaInt=quotes.index[i]
            inter = datetime.timedelta(days=0.4)
            plt.axvspan(fechaInt-inter, fechaInt+inter, facecolor='r', alpha = 0.5)

        if patrones.hombreColgado(aper1=quotes['Open'][i], cierre1=quotes['Close'][i], alto1=quotes['High'][i], bajo1=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True and encontrado==False:
            '''
            print("Detectada Vela Hombre Colgado: ")
            print("Tendencia Bajista")
            print(quotes.index[i])
            '''
            encontrado=True
            vela=True
            nombreVela="hc"
            if i<=contador:
                vela=False
            fechaInt=quotes.index[i]
            inter = datetime.timedelta(days=0.4)
            plt.axvspan(fechaInt-inter, fechaInt+inter, facecolor='yellow', alpha = 0.5)

        #Cambiar color de la sombra
        if patrones.dojiSombrilla(aper1=quotes['Open'][i], cierre1=quotes['Close'][i], alto1=quotes['High'][i], bajo1=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True and encontrado==False:
            '''
            print("Detectada Vela Doji Sombrilla: ")
            print("Tendencia Alcista")
            print(quotes.index[i])
            '''
            encontrado=True
            vela=True
            nombreVela="ds"
            if i<=contador:
                vela=False
            fechaInt=quotes.index[i]
            inter = datetime.timedelta(days=0.4)
            plt.axvspan(fechaInt-inter, fechaInt+inter, facecolor='orange', alpha = 0.5)


        #Cambiar color de la sombra
        if patrones.dojiSombrillaInvertida(aper1=quotes['Open'][i], cierre1=quotes['Close'][i], alto1=quotes['High'][i], bajo1=quotes['Low'][i], fechaInicio=fechaInicio, fechaFin=fechaFin, archivo=archivo, procedencia=procedencia)==True and encontrado==False:
            '''
            print("Detectada Vela Doji Sombrilla Invertida: ")
            print("Tendencia Bajista")
            print(quotes.index[i])
            '''
            encontrado=True
            vela=True
            nombreVela="dsi"
            if i<=contador:
                vela=False
            fechaInt=quotes.index[i]
            inter = datetime.timedelta(days=0.4)
            plt.axvspan(fechaInt-inter, fechaInt+inter, facecolor='gray', alpha = 0.5)

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
    return imagen, terminado, contador, nombreVela
