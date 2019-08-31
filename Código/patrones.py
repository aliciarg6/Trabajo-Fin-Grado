import pandas as pd
import numpy as np



#################################### ANALISIS ##################################

def detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia):
    fechaInicio = str(fechaInicio)
    fechaFin = str(fechaFin)

    if procedencia=="csv":
        quotes = pd.read_csv(archivo,index_col = "Date", parse_dates = True)
    else:
        quotes=archivo
    quotes = quotes[(quotes.index >= fechaInicio) & (quotes.index <= fechaFin)]

    open= np.array(quotes['Open'], dtype='float')
    close = np.array(quotes['Close'], dtype='float')
    #Se almacenan las diferencias entre el precio de apertura y el de cierre
    dif = []
    for i in range(len(open)):
        if open[i]<close[i]:
            dif.append(close[i]-open[i])
        else:
            dif.append(open[i]-close[i])

    #ORDENADO
    dif.sort()
    #Cantidad de datos
    num = len(dif)
    #Porcentaje de Datos Perteneciente a cada conjunto: alto(30%), medio(40%), bajo(30%)
    numAltoBajo = (30*num)/100
    numMedio = (40*num)/100
    #Evitar que no se tengan valores decimales
    if numAltoBajo%1>0.5:
        numAltoBajo=int(numAltoBajo)+1
    else:
        numAltoBajo=int(numAltoBajo)
    if numMedio%1>0.5:
        numMedio=int(numMedio)+1
    else:
        numMedio=int(numMedio)

    #Diferenciación por tamaño
    #El porcentaje mayor
    alto =[]
    for i in range(numAltoBajo):
        alto.append(dif[numMedio+numAltoBajo+i-1])
    #El porcentaje medio
    medio =[]
    for i in range(numMedio):
        medio.append(dif[numAltoBajo+i])
    #El porcentaje menor
    bajo =[]
    for i in range(numAltoBajo):
        bajo.append(dif[i])

    return alto, medio, bajo


def detectarTamVelasSegunSombra(fechaInicio, fechaFin, archivo, procedencia):
    fechaInicio = str(fechaInicio)
    fechaFin = str(fechaFin)

    if procedencia=="csv":
        quotes = pd.read_csv(archivo,index_col = "Date", parse_dates = True)
    else:
        quotes = archivo
    quotes = quotes[(quotes.index >= fechaInicio) & (quotes.index <= fechaFin)]

    open= np.array(quotes['Open'], dtype='float')
    close = np.array(quotes['Close'], dtype='float')
    high= np.array(quotes['High'], dtype='float')
    low = np.array(quotes['Low'], dtype='float')
    #Se almacenan las diferencias entre el precio de apertura y el de cierre
    dif = []
    for i in range(len(high)):

        if open[i]<close[i]:
            dif.append(open[i]-low[i])
            dif.append(high[i]-close[i])
        else:
            dif.append(high[i]-open[i])
            dif.append(close[i]-low[i])

        #ORDENADO
        dif.sort()
        #Cantidad de datos
        num = len(dif)
        #Porcentaje de Datos Perteneciente a cada conjunto: alto(30%), medio(40%), bajo(30%)
        numAltoBajo = (30*num)/100
        numMedio = (40*num)/100
        #Evitar que no se tengan valores decimales
        if numAltoBajo%1>0.5:
            numAltoBajo=int(numAltoBajo)+1
        else:
            numAltoBajo=int(numAltoBajo)
        if numMedio%1>0.5:
            numMedio=int(numMedio)+1
        else:
            numMedio=int(numMedio)

        #Diferenciación por tamaño
        #El porcentaje mayor
        alto =[]
        for i in range(numAltoBajo):
            alto.append(dif[numMedio+numAltoBajo+i-1])
        #El porcentaje medio
        medio =[]
        for i in range(numMedio):
            medio.append(dif[numAltoBajo+i])
        #El porcentaje menor
        bajo =[]
        for i in range(numAltoBajo):
            bajo.append(dif[i])

        return alto, medio, bajo

def tamVela(fechaInicio, fechaFin, archivo, valor1=0, valor2=0, criterio="cuerpo" , procedencia=""):
    tipo = "ninguno"
    if criterio=="cuerpo":
        a, m, b=detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        diferencia = 0
        if valor1 < valor2 :
            diferencia = valor2 - valor1
        else:
            diferencia = valor1 - valor2

        if diferencia<=b[len(b)-1]:
            tipo = "bajo"
        if diferencia>=m[0] and diferencia<=m[len(m)-1]:
            tipo = "medio"
        if diferencia>=a[0] :
            tipo = "alto"

    elif criterio=="sombra":
         a, m, b=detectarTamVelasSegunSombra(fechaInicio, fechaFin, archivo, procedencia)
         diferencia = 0
         if valor1 < valor2 :
             diferencia = valor2 - valor1
         else:
             diferencia = valor1 - valor2
         if diferencia<=b[len(b)-1]:
             tipo = "bajo"
         if diferencia>=m[0] and diferencia<=m[len(m)-1]:
             tipo = "medio"
         if diferencia>=a[0] :
             tipo = "alto"
    else:
        print("El criterio elegido no es correcto, elegir entre: cuerpo o sombra")

    return tipo



#PATRONES ANALIZADOS
def velaAlcistaGrande(apertura, cierre, alto, bajo, fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    if apertura < cierre:
        res = tamVela(fechaInicio, fechaFin, archivo, valor1=apertura, valor2=cierre, procedencia=procedencia)
        if res=="alto":
            patron = True

    return patron

def velaBajistaGrande(apertura, cierre, alto, bajo, fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    if apertura > cierre:
        res = tamVela(fechaInicio, fechaFin, archivo, valor1=apertura, valor2=cierre, procedencia=procedencia)
        if res=="alto":
            patron = True
    return patron

def cozAlcista(aperturaAct, cierreAct, aperturaAnt, cierreAnt, fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    if aperturaAnt>cierreAnt and aperturaAct<cierreAct:
        if aperturaAnt==aperturaAct:
            resAct = tamVela(fechaInicio, fechaFin, archivo, valor1=aperturaAct, valor2=cierreAct, procedencia=procedencia)
            resAnt = tamVela(fechaInicio, fechaFin, archivo, valor1=aperturaAnt, valor2=cierreAnt, procedencia=procedencia)
            if resAnt=="alto" and resAct=="alto":
                patron=True
    return patron

def cozBajista(aperturaAct, cierreAct, aperturaAnt, cierreAnt, fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    if aperturaAnt<cierreAnt and aperturaAct>cierreAct:
        if aperturaAnt==aperturaAct:
            resAct = tamVela(fechaInicio, fechaFin, archivo, valor1=aperturaAct, valor2=cierreAct, procedencia=procedencia)
            resAnt = tamVela(fechaInicio, fechaFin, archivo, valor1=aperturaAnt, valor2=cierreAnt, procedencia=procedencia)
            if resAnt=="alto" and resAct=="alto":
                patron=True
    return patron

#Mejorado!
def dosCuervosEnGapAlcista(aper1, cierre1, aper2, cierre2, aper3, cierre3, fechaInicio, fechaFin, archivo , procedencia):
    patron = False
    if aper1 < cierre1 and aper2>cierre2 and aper3>cierre3 and cierre1<cierre2 and cierre1<cierre3:
        res1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
        res2 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper2, valor2=cierre2, procedencia=procedencia)
        res3 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper3, valor2=cierre3, procedencia=procedencia)
        if res1=="alto" and res2=="bajo" and res3=="bajo":
            if cierre2>cierre3 and aper2<aper3:
                patron = True
    return patron

#Mejorado!
def ventanaBajista(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    #Comprobamos que ocurren dos velas bajistas separadas por un gap
    if aper1>cierre1 and aper2>cierre2 and bajo1>alto2:
        res1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
        res2 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper2, valor2=cierre2, procedencia=procedencia)
        if res1=="alto" and res2=="alto":
            patron=True
    return patron

#Mejorado!
def ventanaAlcita(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, fechaInicio, fechaFin, archivo , procedencia):
    patron= False
    #Comprobamos que ocurren dos velas alcistas separadas por un gap
    if aper1<cierre1 and aper2<cierre2 and alto1<bajo2:
        res1=tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
        res2=tamVela(fechaInicio, fechaFin, archivo, valor1=aper2, valor2=cierre2, procedencia=procedencia)
        if res1=="alto" and res2=="alto":
            patron = True
    return patron

#Mejorado!
def pequeniaGolondrinaOcultada(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, aper3, cierre3, alto3, bajo3, aper4, cierre4, alto4, bajo4,fechaInicio, fechaFin, archivo, procedencia):
    patron=False
    #Comprobamos que las cuatro velas son bajistas
    if aper1>cierre1 and aper2>cierre2 and aper3>cierre3 and aper4>cierre4:
        res1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
        res2 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper2, valor2=cierre2, procedencia=procedencia)
        res3 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper3, valor2=cierre3, procedencia=procedencia)
        res4 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper4, valor2=cierre4, procedencia=procedencia)
        #Comprobamos que las primera, segunda y cuarta vela son de gran tamaño, la tercera de tamaño pequeño
        if res1=="alto" and res2=="alto" and res4=="alto" and  res3=="bajo":
            som3 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper3, valor2=alto3, criterio="sombra" , procedencia=procedencia)
            if som3 == "alto":
                if aper1>aper2 and aper2>alto3 and alto3>aper4 and cierre1>cierre2 and cierre2>cierre3 and cierre3>cierre4 and cierre3==bajo3:
                    patron = True
    return patron

#Mejorado!
def formacionConGapBajista(aper1, cierre1, aper2, cierre2, aper3, cierre3, aper4, cierre4, aper5, cierre5,fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    tam1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
    tam5 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper5, valor2=cierre5, procedencia=procedencia)
    #Comprobamos que las dos velas de los extremos son grandes y son bajistas
    if tam1=="alto" and tam5=="alto" and cierre1<aper1 and cierre5<aper5:
        tam2 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper2, valor2=cierre2, procedencia=procedencia)
        tam3 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper3, valor2=cierre3, procedencia=procedencia)
        tam4 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper4, valor2=cierre4, procedencia=procedencia)
        #Comprobamos que las tres velas de en medio son de cuerpo pequeño
        if tam2=="bajo" and tam3=="bajo" and tam4=="bajo" :
            #Comprobamos que las tres velas de en medio son alcistas
            if aper2<cierre2 and aper3<cierre3 and aper4<cierre4:
                if  aper2<aper3 and aper3<aper4 and cierre1<aper2 and cierre4<aper1:
                    #Comprobamos el gap con el que comienza la ultima gran vela
                    if aper5<aper4:
                        patron = True
    return patron

#Mejorado!
def formacionConGapAlcista(aper1, cierre1, aper2, cierre2, aper3, cierre3, aper4, cierre4, aper5, cierre5,fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    tam1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
    tam5 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper5, valor2=cierre5, procedencia=procedencia)
    #Comprobamos que las dos velas de los extremos son grandes y son alcistas
    if tam1=="alto" and tam5=="alto" and cierre1>aper1 and cierre5>aper5:
        tam2 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper2, valor2=cierre2, procedencia=procedencia)
        tam3 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper3, valor2=cierre3, procedencia=procedencia)
        tam4 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper4, valor2=cierre4, procedencia=procedencia)
        #Comprobamos que las tres velas de en medio son de cuerpo pequeño
        if tam2=="bajo"  and tam3=="bajo" and tam4=="bajo":
            #Comprobamos que las tres velas de en medio son bajistas
            if aper2>cierre2 and aper3>cierre3 and aper4>cierre4:
                if cierre3<cierre2 and cierre4<cierre3 and cierre1>aper2 and aper1<cierre4:
                    #Comprobamos el gap con el que comienza la ultima gran vela
                    if aper4<aper5:
                        patron = True
    return patron

#Mejorado!
def matHold(aper1, cierre1, aper2, cierre2, aper3, cierre3, aper4, cierre4, aper5, cierre5,fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    tam1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
    tam5 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper5, valor2=cierre5, procedencia=procedencia)
    #Comprobamos que las dos velas de los extremos son grandes y son alcistas
    if tam1=="alto" and tam5=="alto" and cierre1>aper1 and cierre5>aper5:
        tam2 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper2, valor2=cierre2, procedencia=procedencia)
        tam3 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper3, valor2=cierre3, procedencia=procedencia)
        tam4 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper4, valor2=cierre4, procedencia=procedencia)
        #Comprobamos que las tres velas de en medio son de cuerpo pequeño
        if tam2=="bajo" and tam3=="bajo" and tam4=="bajo":
            #Comprobamos que las tres velas de en medio son bajistas
            if aper2>cierre2 and aper3>cierre3 and aper4>cierre4:
                #Comprombamos que las tres velas hacen nuevos minimos y que quedan contenidas dentro del cuerpo de la primera vela
                if cierre3<cierre2 and cierre4<cierre3 and cierre1>cierre2:
                    #La ultima vela cubre con su cuerpo los tres anteriores
                    if cierre5>aper2 and aper5<cierre4:
                        patron = True
    return patron

#Mejorado!
def tresSoldadosBlancos(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, aper3, cierre3, alto3, bajo3, fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    tam1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
    tam2 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper2, valor2=cierre2, procedencia=procedencia)
    tam3 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper3, valor2=cierre3, procedencia=procedencia)
    #Comprobamos que las tres velas alcistas son de gran tamaño
    if tam1=="alto" and tam2=="alto" and tam3=="alto" and aper1<cierre1 and aper2<cierre2 and aper3<cierre3:
        #La segunda y la tercera abren dentro del cuerpo de la vela anterior y cierran por encima de ella
        if aper1<aper2 and aper2<aper3 and cierre1<cierre2 and cierre2<cierre3:
            patron=True
    return patron

#Mejorado!
def tresCuervosNegros(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, aper3, cierre3, alto3, bajo3, fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    tam1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
    tam2 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper2, valor2=cierre2, procedencia=procedencia)
    tam3 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper3, valor2=cierre3, procedencia=procedencia)
    #Comprobamos que las tres velas son bajistas y de gran tamaño
    if tam1=="alto" and tam2=="alto" and tam3=="alto" and aper1>cierre1 and aper2>cierre2 and aper3>cierre3:
        #La segunda y la tercera abren dentro del cuerpo de la vela anterior y cierran por encima de ella
        if aper1>aper2 and aper2>aper3 and cierre1>cierre2 and cierre2>cierre3:
            patron=True
    return patron

#Mejorado!
def tripleFormacionBajista(aper1, cierre1, aper2, cierre2, aper3, cierre3, aper4, cierre4, aper5, cierre5,fechaInicio, fechaFin, archivo, procedencia):
    patron= False
    tam1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
    tam5 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper5, valor2=cierre5, procedencia=procedencia)
    #Comprobamos si las dos velas de los extremos son bajista y con gran cuerpo
    if tam1=="alto" and tam5=="alto" and aper1>cierre1 and aper5>cierre5:
        tam2 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper2, valor2=cierre2, procedencia=procedencia)
        tam3 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper3, valor2=cierre3, procedencia=procedencia)
        tam4 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper4, valor2=cierre4, procedencia=procedencia)
        #Comprobamos si las tres velas intermedias son alcistas y con cuerpo peqeño
        if tam2=="bajo" and tam3=="bajo" and tam4=="bajo" and cierre2>aper2 and cierre3>aper3 and cierre4>aper4:
            if aper2<aper3 and aper3<aper4 and cierre1<aper2 and cierre4<aper1 and cierre5<aper2 and cierre4<aper5:
                patron=True
    return patron

#Mejorado!
def tripleFormacionAlcista(aper1, cierre1, aper2, cierre2, aper3, cierre3, aper4, cierre4, aper5, cierre5,fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    tam1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
    tam5 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper5, valor2=cierre5, procedencia=procedencia)
    #Comprobamos si las dos velas de los extremos son alcistas y con gran cuerpo
    if tam1=="alto" and tam5=="alto" and aper1<cierre1 and aper5<cierre5:
        tam2 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper2, valor2=cierre2, procedencia=procedencia)
        tam3 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper3, valor2=cierre3, procedencia=procedencia)
        tam4 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper4, valor2=cierre4, procedencia=procedencia)
        #Comprobamos si las tres velas intermedias son bajistas y con cuerpo peqeño
        if tam2=="bajo" and tam3=="bajo" and tam4=="bajo" and cierre2<aper2 and cierre3<aper3 and cierre4<aper4:
            if cierre1>aper2 and aper1<cierre4 and cierre2>cierre3 and cierre3>cierre4 and cierre5>aper2 and aper5<cierre4:
                patron=True
    return patron

#Mejorado!
def bebeAbandonadoAlcista(aper1, cierre1, aper2, cierre2, aper3,cierre3 ,fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    tam1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
    tam3 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper3, valor2=cierre3, procedencia=procedencia)
    #Comprobamos que la primera vela es bajista de gran tamaño y la tercera es alcista de gran tamaño
    if tam1=="alto" and tam3=="alto" and aper1>cierre1 and cierre3>aper3 and cierre1>cierre2 and cierre1>aper2  and aper3>cierre2  and aper3>aper2:
        #Comprobamos que la segunda vela es un doji
        if aper2==cierre2:
            if aper3<cierre1 and aper1>cierre3:
                patron = True
    return patron

#Mejorado!
def bebeAbandonadoBajista(aper1, cierre1, aper2, cierre2, aper3,cierre3 ,fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    tam1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
    tam3 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper3, valor2=cierre3, procedencia=procedencia)
    #Comprobamos que la primera vela es alcista de gran tamaño y la tercera es bajista de gran tamaño
    if tam1=="alto" and tam3=="alto" and aper1<cierre1 and cierre3<aper3 and cierre1>cierre2 and cierre1>aper2  and aper3>cierre2  and aper3>aper2:
        #Comprobamos que la segunda vela es un doji
        if aper2==cierre2:
            if aper3<cierre1 and aper1>cierre3:
                patron = True
    return patron

#Mejorado!
def estrellaVespertina(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, aper3,cierre3, alto3, bajo3, fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    tam1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
    tam3 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper3, valor2=cierre3, procedencia=procedencia)
    #Comprobamos que la primera vela es alcista de gran tamaño y la tercera es bajista de gran tamaño
    if tam1=="alto" and tam3=="alto" and aper1<cierre1 and cierre3<aper3 and cierre1<cierre2 and cierre1<aper2  and aper3<cierre2  and aper3<aper2:
        #Comprobamos que la segunda vela es de tamaño pequeño
        tam2 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper2, valor2=cierre2, procedencia=procedencia)
        if tam2=="bajo" and (aper2-cierre2)!=0:
            if aper3>cierre1 and aper1<cierre3:
                patron = True
    return patron

#Mejorado!
def estrellaVespertinaDoji(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, aper3,cierre3, alto3, bajo3, fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    tam1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
    tam3 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper3, valor2=cierre3, procedencia=procedencia)
    #Comprobamos que la primera vela es alcista de gran tamaño y la tercera es bajista de gran tamaño
    if tam1=="alto" and tam3=="alto" and aper1<cierre1 and cierre3<aper3  and cierre1<cierre2 and cierre1<aper2  and aper3<cierre2  and aper3<aper2:
        #Comprobamos que la segunda vela es un doji
        if aper2==cierre2:
            #Comprobamos que la segunda tiene un gap al alza
            if aper3>cierre1 and aper1<cierre3:
                patron = True
    return patron

#Mejorado!
def estrellaDeLaManianaDoji(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, aper3,cierre3, alto3, bajo3, fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    tam1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
    tam3 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper3, valor2=cierre3, procedencia=procedencia)
    #Comprobamos que la primera vela es bajista de gran tamaño y la tercera es alcista de gran tamaño
    if tam1=="alto" and tam3=="alto" and aper1>cierre1 and aper3<cierre3 and cierre1>cierre2 and cierre1>aper2  and aper3>cierre2  and aper3>aper2:
        #Comprobamos que la segunda vela es un doji y que tiene un gap con la primera y la tercera vela
        if aper2==cierre2 and aper3<cierre1 and aper1>cierre3:
            patron = True
    return patron

#Mejorado!
def estrellaDeLaManiana(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, aper3,cierre3, alto3, bajo3, fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    tam1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
    tam3 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper3, valor2=cierre3, procedencia=procedencia)
    #Comprobamos que la primera vela es bajista de gran tamaño y la tercera es alcista de gran tamaño
    if tam1=="alto" and tam3=="alto" and aper1>cierre1 and aper3<cierre3 and  cierre1>cierre2 and cierre1>aper2  and aper3>cierre2  and aper3>aper2:
        #Comprobamos que la segunda vela es de tamaño pequeño
        tam2 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper2, valor2=cierre2, procedencia=procedencia)
        if tam2=="bajo":

            if aper3<cierre1 and aper1>cierre3:
                patron = True
    return patron

def envolventeAlcista(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    tam1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
    tam2 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper2, valor2=cierre2, procedencia=procedencia)
    #Comprobamos que la primera vela es bajista pequeña y la segunda es alcista grande
    if tam1=="bajo":
        if tam2=="alto":
            if aper1>cierre1 and aper2<cierre2:
                #La segunda vela cubre el cuerpo de la anterior
                if cierre2>aper1 and cierre1>aper2:
                    #La sombras de las velas marcan máximos crecientes
                    if alto2>alto1:
                        patron = True
    return patron

def envolventeBajista(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    tam1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
    tam2 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper2, valor2=cierre2, procedencia=procedencia)
    #Comprobamos que la primera vela es alcista pequeña y la segunda es bajista grande
    if tam1=="bajo":
        if tam2=="alto":
            if aper1<cierre1 and aper2>cierre2:
                #La segunda vela cubre el cuerpo de la anterior
                if aper2>cierre1 and aper1>cierre2:
                    #La sombras de las velas marcan máximos decrecientes
                    if alto2>alto1:
                        patron = True
    return patron

def hombreColgado(aper1, cierre1, alto1, bajo1, fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    tam1 = tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=cierre1, procedencia=procedencia)
    #Comprobamos que es una vale de tamaño pequeño
    if tam1=="bajo":
        #Si la vela es de tipo bajista
        if aper1>cierre1:
            #Comprobamos que no tenga sombra superior
            if alto1==aper1:
                #Comprobamos que la sombra inferior es al menos dos veces el tamaño del cuerpo
                rest = aper1-cierre1
                rest1 = cierre1-bajo1
                if rest1> 2*rest:
                    patron = True
        #Si la vela es de tipo alcista
        if aper1<cierre1:
            #Comprobamos que no tenga sombra superior
            if alto1==cierre1:
                #Comprobamos que la sombra inferior es al menos dos veces el tamaño del cuerpo
                rest = cierre1-aper1
                rest1 = aper1-bajo1
                if rest1> 2*rest:
                    patron = True
    return patron

#CAMBIO DE TENDENCIA
def dojiSombrilla(aper1, cierre1, alto1, bajo1, fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    #Comprobamos que es una vela de tipo doji
    if aper1==cierre1:
        #Comprobamos que la sombra superior sea nula o muy pequña
        tam1=tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=alto1, criterio="sombra", procedencia=procedencia)
        if alto1==aper1 or tam1=="bajo":
            #Comprobamos vela inferior muy larga
            tam2=tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=bajo1, criterio="sombra" , procedencia=procedencia)
            if tam2=="alto":
                patron = True
    return patron

#CAMBIO DE TENDENCIA
def dojiSombrillaInvertida(aper1, cierre1, alto1, bajo1, fechaInicio, fechaFin, archivo, procedencia):
    patron = False
    #Comprobamos que es una vela de tipo doji
    if aper1==cierre1:
        #Comprobamos que la sombra inferior sea nula o muy pequña
        tam1=tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=bajo1, criterio="sombra", procedencia=procedencia)
        if bajo1==aper1 or tam1=="bajo":
            #Comprobamos vela superior muy larga
            tam2=tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=alto1, criterio="sombra" , procedencia=procedencia)
            if tam2=="alto":
                patron = True
    return patron



################################################################################
