import patrones

def velaAlcistaGrandeDifusa(apertura, cierre, alto, bajo, fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if cierre > apertura:
        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = float(bajo[l])
        m = float(medio[0])
        b =float(medio[len(medio)-1])

        x = float(abs(apertura-cierre))

        if x<=a:
            p = float(0.0)
        elif a<x and x<=m:
            p = 2*((x-a)/(b-a))**2
        elif m<x and x<b:
            p = 1 - (2*((x-b)/(b-a))**2)
        elif x>=b:
            p = float(1.0)

    return p

def velaBajistaGrandeDifusa(apertura, cierre, alto, bajo, fechaInicio, fechaFin, archivo, procedencia):
    p= float(0.0)

    if apertura > cierre:
        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]

        x = abs(apertura-cierre)

        if x<=a:
            p = float(0.0)
        elif a<x and x<=m:
            p = 2*((x-a)/(b-a))**2
        elif m<x and x<b:
            p = 1 - 2*((x-b)/(b-a))**2
        elif x>=b:
            p = float(1.0)

    return p

def dojiSombrillaDifusa(aper1, cierre1, alto1, bajo1, fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)

    if aper1==cierre1:
        tam = patrones.tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=alto1, criterio="sombra", procedencia=procedencia)
        if aper1==alto1 or tam=="bajo":
            alto, medio, bajo = patrones.detectarTamVelasSegunSombra(fechaInicio, fechaFin, archivo, procedencia)
            l = len(bajo)
            l = l/2
            l = int(l)
            a = bajo[l]
            m = medio[0]
            b = medio[len(medio)-1]
            x = abs(aper1-bajo1)
            if x<=a:
                p = float(0.0)
            elif a<x and x<=m:
                p = 2*((x-a)/(b-a))**2
            elif m<x and x<b:
                p = 1 - 2*((x-b)/(b-a))**2
            elif x>=b:
                p = float(1.0)

            if p>float(1.0):
                p = float(1.0)

    return p

def dojiSombrillaInvertidaDifusa(aper1, cierre1, alto1, bajo1, fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)

    if aper1==cierre1:
        tam = patrones.tamVela(fechaInicio, fechaFin, archivo, valor1=aper1, valor2=bajo1, criterio="sombra", procedencia=procedencia)
        if aper1==bajo1 or tam=="bajo":
            alto, medio, bajo = patrones.detectarTamVelasSegunSombra(fechaInicio, fechaFin, archivo, procedencia)
            l = len(bajo)
            l = l/2
            l = int(l)
            a = bajo[l]
            m = medio[0]
            b = medio[len(medio)-1]
            x = abs(aper1-alto1)
            if x<=a:
                p = float(0.0)
            elif a<x and x<=m:
                p = 2*((x-a)/(b-a))**2
            elif m<x and x<b:
                p = 1 - 2*((x-b)/(b-a))**2
            elif x>=b:
                p = float(1.0)

    return p

def hombreColgadoDifusa(aper1, cierre1, alto1, bajo1, fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)

    #CASO VELA ALCISTA
    if aper1 < cierre1:
        if cierre1==alto1:
            rest = cierre1-aper1
            rest1 = aper1-bajo1
            if rest1> 2*rest:
                alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)

                l = len(bajo)
                l = l/2
                l = int(l)
                a = bajo[l]
                m = medio[0]
                b = medio[len(medio)-1]

                x = abs(aper1-cierre1)

                if x<=a:
                    p = float(1.0)
                elif a<x and x<=m:
                    p = 1 - 2*((x-a)/(b-a))**2
                elif m<x and x<b:
                    p = 2*((x-b)/(b-a))**2
                elif x>=b:
                    p = float(0.0)

    #CASO VELA BAJISTA
    elif cierre1 < aper1:
        if aper1==alto1:
            rest = aper1-cierre1
            rest1 = cierre1-bajo1
            if rest1> 2*rest:
                alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)

                l = len(bajo)
                l = l/2
                l = int(l)
                a = bajo[l]
                m = medio[0]
                b = medio[len(medio)-1]

                x = abs(aper1-cierre1)

                if x<=a:
                    p = float(1.0)
                elif a<x and x<=m:
                    p = 1 - 2*((x-a)/(b-a))**2
                elif m<x and x<b:
                    p = 2*((x-b)/(b-a))**2
                elif x>=b:
                    p = float(0.0)
    return p


def pertenenciaVelaGrandeDifusa(apertura, cierre, a, m, b):
    p = float(0.0)
    x = abs(apertura-cierre)
    if x<=a:
        p = float(0.0)
    elif a<x and x<=m:
        p = 2*((x-a)/(b-a))**2
    elif m<x and x<b:
        p = 1 - 2*((x-b)/(b-a))**2
    elif x>=b:
        p = float(1.0)
    return abs(p)


def pertenenciaVelaPequeniaDifusa(apertura, cierre, a, m, b):
    p = float(0.0)
    x = abs(apertura-cierre)
    if x<=a:
        p = float(1.0)
    elif a<x and x<=m:
        p = 1 - 2*((x-a)/(b-a))**2
    elif m<x and x<b:
        p = 2*((x-b)/(b-a))**2
    elif x>=b:
        p = float(0.0)
    return abs(p)


def cozBajistaDifusa(aperturaAct, cierreAct, aperturaAnt, cierreAnt, fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)

    if aperturaAnt<cierreAnt and aperturaAct>cierreAct and aperturaAnt >= aperturaAct:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aperturaAnt, cierreAnt, a, m, b)
        p2 = pertenenciaVelaGrandeDifusa(aperturaAct, cierreAct, a, m, b)

        p1 = 0.3 * p1
        p2 = 0.3 * p2
        p = p + p1 + p2

        if aperturaAnt==aperturaAct:
            p = p + float(0.2)
    return p


def cozAlcistaDifusa(aperturaAct, cierreAct, aperturaAnt, cierreAnt, fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aperturaAnt>cierreAnt and aperturaAct<cierreAct and aperturaAnt <= aperturaAct:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aperturaAnt, cierreAnt, a, m, b)
        p2 = pertenenciaVelaGrandeDifusa(aperturaAct, cierreAct, a, m, b)

        p1 = 0.3 * p1
        p2 = 0.3 * p2
        p = p + p1 + p2

        if aperturaAnt==aperturaAct:
            p = p + float(0.2)
    return p

def ventanaBajistaDifusa(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1>cierre1 and aper2>cierre2:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p2 = pertenenciaVelaGrandeDifusa(aper2, cierre2, a, m, b)

        p1 = 0.3 * p1
        p2 = 0.3 * p2
        p = p + p1 + p2

        if bajo1>alto2:
            p = p + float(0.2)
    return p


def ventanaAlcistaDifusa(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, fechaInicio, fechaFin, archivo , procedencia):
    p = float(0.0)
    if aper1<cierre1 and aper2<cierre2:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p2 = pertenenciaVelaGrandeDifusa(aper2, cierre2, a, m, b)

        p1 = 0.3 * p1
        p2 = 0.3 * p2
        p = p + p1 + p2

        if alto1<bajo2:
            p = p + float(0.2)
    return p


def envolventeBajistaDifusa(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1<cierre1 and aper2>cierre2:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaPequeniaDifusa(aper1, cierre1, a, m, b)
        p2 = pertenenciaVelaGrandeDifusa(aper2, cierre2, a, m, b)

        p1 = 0.3 * p1
        p2 = 0.3 * p2
        p = p + p1 + p2

        if aper2>cierre1 and aper1>cierre2:             #La segunda vela cubre el cuerpo de la anterior
            p = p + float(0.1)
        if alto2>alto1:                                 #La sombras de las velas marcan máximos decrecientes
            p = p + float(0.1)

    return p

def envolventeAlcistaDifusa(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1>cierre1 and aper2<cierre2:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaPequeniaDifusa(aper1, cierre1, a, m, b)
        p2 = pertenenciaVelaGrandeDifusa(aper2, cierre2, a, m, b)

        p1 = 0.3 * p1
        p2 = 0.3 * p2
        p = p + p1 + p2

        if cierre2>aper1 and cierre1>aper2:             #La segunda vela cubre el cuerpo de la anterior
            p = p + float(0.1)
        if alto2>alto1:                                 #La sombras de las velas marcan máximos decrecientes
            p = p + float(0.1)

    return p



def tresSoldadosBlancosDifusa(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, aper3, cierre3, alto3, bajo3, fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1<cierre1 and aper2<cierre2 and aper3<cierre3:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p2 = pertenenciaVelaGrandeDifusa(aper2, cierre2, a, m, b)
        p3 = pertenenciaVelaGrandeDifusa(aper3, cierre3, a, m, b)

        p1 = 0.2 * p1
        p2 = 0.2 * p2
        p3 = 0.2 * p3
        p = p + p1 + p2 + p3

        if aper1<aper2 and aper2<aper3:
            p = p + float(0.1)
        if cierre1<cierre2 and cierre2<cierre3:
            p = p + float(0.1)

    return p


def tresCuervosNegrosDifusa(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, aper3, cierre3, alto3, bajo3, fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1>cierre1 and aper2>cierre2 and aper3>cierre3:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p2 = pertenenciaVelaGrandeDifusa(aper2, cierre2, a, m, b)
        p3 = pertenenciaVelaGrandeDifusa(aper3, cierre3, a, m, b)

        p1 = 0.2 * p1
        p2 = 0.2 * p2
        p3 = 0.2 * p3
        p = p + p1 + p2 + p3

        if aper1>aper2 and aper2>aper3:
            p = p + float(0.1)
        if cierre1>cierre2 and cierre2>cierre3:
            p = p + float(0.1)

    return p


def dosCuervosEnGapAlcistaDifusa(aper1, cierre1, aper2, cierre2, aper3, cierre3, fechaInicio, fechaFin, archivo , procedencia):
    p = float(0.0)
    if aper1<cierre1 and aper2>cierre2 and aper3>cierre3 and cierre1<cierre2 and cierre1<cierre3:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p2 = pertenenciaVelaPequeniaDifusa(aper2, cierre2, a, m, b)
        p3 = pertenenciaVelaPequeniaDifusa(aper3, cierre3, a, m, b)

        p1 = 0.2 * p1
        p2 = 0.2 * p2
        p3 = 0.2 * p3
        p = p + p1 + p2 + p3

        if cierre2>cierre3 and aper2<aper3:
            p = p + float(0.2)

    return p

def estrellaVespertinaDifusa(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, aper3,cierre3, alto3, bajo3, fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1<cierre1 and aper3>cierre3 and cierre1<cierre2 and cierre1<aper2  and aper3<cierre2  and aper3<aper2:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p2 = pertenenciaVelaPequeniaDifusa(aper2, cierre2, a, m, b)
        p3 = pertenenciaVelaGrandeDifusa(aper3, cierre3, a, m, b)

        p1 = 0.2 * p1
        p2 = 0.2 * p2
        p3 = 0.2 * p3
        p = p + p1 + p2 + p3

        if aper3>cierre1:
            p = p + float(0.1)
        if aper1<cierre3:
            p = p + float(0.1)

    return p


def estrellaVespertinaDojiDifusa(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, aper3,cierre3, alto3, bajo3, fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1<cierre1 and aper3>cierre3 and cierre1<cierre2 and cierre1<aper2  and aper3<cierre2  and aper3<aper2:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p3 = pertenenciaVelaGrandeDifusa(aper3, cierre3, a, m, b)

        p1 = 0.2 * p1
        p3 = 0.2 * p3
        p = p + p1 + p3

        if aper2==cierre2:              #Segunda vela es un doji
            p = p + float(0.2)
        if aper3>cierre1:
            p = p + float(0.1)
        if aper1<cierre3:
            p = p + float(0.1)

    return p


def bebeAbandonadoBajistaDifusa(aper1, cierre1, aper2, cierre2, aper3,cierre3 ,fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1<cierre1 and aper3>cierre3 and cierre1<cierre2 and cierre1<aper2  and aper3<cierre2  and aper3<aper2:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p3 = pertenenciaVelaGrandeDifusa(aper3, cierre3, a, m, b)

        p1 = 0.2 * p1
        p3 = 0.2 * p3
        p = p + p1 + p3

        if aper2==cierre2:              #Segunda vela es un doji
            p = p + float(0.2)
        if aper3<cierre1:
            p = p + float(0.1)
        if aper1<cierre3:
            p = p + float(0.1)

    return p

def estrellaDeLaManianaDifusa(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, aper3,cierre3, alto3, bajo3, fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1>cierre1 and aper3<cierre3 and  cierre1>cierre2 and cierre1>aper2  and aper3>cierre2  and aper3>aper2:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p2 = pertenenciaVelaPequeniaDifusa(aper2, cierre2, a, m, b)
        p3 = pertenenciaVelaGrandeDifusa(aper3, cierre3, a, m, b)

        p1 = 0.2 * p1
        p2 = 0.2 * p2
        p3 = 0.2 * p3
        p = p + p1 + p2 + p3

        if aper3<cierre1:
            p = p + float(0.1)
        if aper1>cierre3:
            p = p + float(0.1)

    return p

def estrellaDeLaManianaDojiDifusa(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, aper3,cierre3, alto3, bajo3, fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1>cierre1 and aper3<cierre3 and cierre1>cierre2 and cierre1>aper2  and aper3>cierre2  and aper3>aper2:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p3 = pertenenciaVelaGrandeDifusa(aper3, cierre3, a, m, b)

        p1 = 0.2 * p1
        p3 = 0.2 * p3
        p = p + p1 + p3

        if aper2==cierre2:              #Segunda vela es un doji
            p = p + float(0.2)
        if aper3<cierre1:
            p = p + float(0.1)
        if aper1>cierre3:
            p = p + float(0.1)

    return p

def bebeAbandonadoAlcistaDifusa(aper1, cierre1, aper2, cierre2, aper3,cierre3 ,fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1>cierre1 and aper3<cierre3 and cierre1>cierre2 and cierre1>aper2  and aper3>cierre2  and aper3>aper2:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p3 = pertenenciaVelaGrandeDifusa(aper3, cierre3, a, m, b)

        p1 = 0.2 * p1
        p3 = 0.2 * p3
        p = p + p1 + p3

        if aper2==cierre2:              #Segunda vela es un doji
            p = p + float(0.2)
        if aper3<cierre1:
            p = p + float(0.1)
        if aper1>cierre3:
            p = p + float(0.1)

    return p


def pequeniaGolondrinaOcultadaDifusa(aper1, cierre1, alto1, bajo1, aper2, cierre2, alto2, bajo2, aper3, cierre3, alto3, bajo3, aper4, cierre4, alto4, bajo4,fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1>cierre1 and aper2>cierre2 and aper3>cierre3 and aper4>cierre4:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p2 = pertenenciaVelaGrandeDifusa(aper2, cierre2, a, m, b)
        p3 = pertenenciaVelaPequeniaDifusa(aper3, cierre3, a, m, b)
        p4 = pertenenciaVelaGrandeDifusa(aper4, cierre4, a, m, b)

        p1 = 0.1 * p1
        p2 = 0.1 * p2
        p3 = 0.1 * p3
        p4 = 0.1 * p4
        p = p + p1 + p2 + p3 + p4

        #Sobre la sombra de la tercera vela

        altoSombra, medioSombra, bajoSombra = patrones.detectarTamVelasSegunSombra(fechaInicio, fechaFin, archivo, procedencia)
        ls = len(bajoSombra)
        ls = ls/2
        ls = int(ls)
        asombra = bajoSombra[ls]
        ms = medioSombra[0]
        bs = medioSombra[len(medioSombra)-1]

        ps = pertenenciaVelaGrandeDifusa(aper3, alto3, asombra, ms, bs)
        ps = 0.1 * ps
        p= p + ps


        if aper1>aper2 and aper2>alto3 and alto3>aper4:
            p = p + float(0.15)
        if cierre1>cierre2 and cierre2>cierre3 and cierre3>cierre4:
            p = p + float(0.1)
        if cierre3==bajo3:          #La tercera vela no tiene sombra inferior
            p = p + float(0.05)

    return p

def tripleFormacionAlcistaDifusa(aper1, cierre1, aper2, cierre2, aper3, cierre3, aper4, cierre4, aper5, cierre5,fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1<cierre1 and aper2>cierre2 and aper3>cierre3 and aper4>cierre4 and aper5<cierre5:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p2 = pertenenciaVelaPequeniaDifusa(aper2, cierre2, a, m, b)
        p3 = pertenenciaVelaPequeniaDifusa(aper3, cierre3, a, m, b)
        p4 = pertenenciaVelaPequeniaDifusa(aper4, cierre4, a, m, b)
        p5 = pertenenciaVelaGrandeDifusa(aper5, cierre5, a, m, b)

        p1 = 0.1 * p1
        p2 = 0.1 * p2
        p3 = 0.1 * p3
        p4 = 0.1 * p4
        p5 = 0.1 * p5
        p = p + p1 + p2 + p3 + p4 + p5

        if cierre1>aper2 and aper1<cierre4:
            p = p + float(0.1)
        if cierre2>cierre3 and cierre3>cierre4:
            p = p + float(0.1)
        if cierre5>aper2 and aper5<cierre4:
            p = p + float(0.1)

    return p

def tripleFormacionBajistaDifusa(aper1, cierre1, aper2, cierre2, aper3, cierre3, aper4, cierre4, aper5, cierre5,fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1>cierre1 and aper2<cierre2 and aper3<cierre3 and aper4<cierre4 and aper5>cierre5:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p2 = pertenenciaVelaPequeniaDifusa(aper2, cierre2, a, m, b)
        p3 = pertenenciaVelaPequeniaDifusa(aper3, cierre3, a, m, b)
        p4 = pertenenciaVelaPequeniaDifusa(aper4, cierre4, a, m, b)
        p5 = pertenenciaVelaGrandeDifusa(aper5, cierre5, a, m, b)

        p1 = 0.1 * p1
        p2 = 0.1 * p2
        p3 = 0.1 * p3
        p4 = 0.1 * p4
        p5 = 0.1 * p5
        p = p + p1 + p2 + p3 + p4 + p5

        if aper2<aper3 and aper3<aper4:
            p = p + float(0.1)
        if cierre1<aper2 and cierre4<aper1:
            p = p + float(0.1)
        if cierre5<aper2 and cierre4<aper5:
            p = p + float(0.1)

    return p

def matHoldDifusa(aper1, cierre1, aper2, cierre2, aper3, cierre3, aper4, cierre4, aper5, cierre5,fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1<cierre1 and aper2>cierre2 and aper3>cierre3 and aper4>cierre4 and aper5<cierre5:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p2 = pertenenciaVelaPequeniaDifusa(aper2, cierre2, a, m, b)
        p3 = pertenenciaVelaPequeniaDifusa(aper3, cierre3, a, m, b)
        p4 = pertenenciaVelaPequeniaDifusa(aper4, cierre4, a, m, b)
        p5 = pertenenciaVelaGrandeDifusa(aper5, cierre5, a, m, b)

        p1 = 0.1 * p1
        p2 = 0.1 * p2
        p3 = 0.1 * p3
        p4 = 0.1 * p4
        p5 = 0.1 * p5
        p = p + p1 + p2 + p3 + p4 + p5

        if cierre1>cierre2:
            p = p + float(0.1)
        if cierre2>cierre3 and cierre3>cierre4:
            p = p + float(0.1)
        if cierre5>aper2 and aper5<cierre4:
            p = p + float(0.1)

    return p

def formacionConGapAlcistaDifusa(aper1, cierre1, aper2, cierre2, aper3, cierre3, aper4, cierre4, aper5, cierre5,fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1<cierre1 and aper2>cierre2 and aper3>cierre3 and aper4>cierre4 and aper5<cierre5:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p2 = pertenenciaVelaPequeniaDifusa(aper2, cierre2, a, m, b)
        p3 = pertenenciaVelaPequeniaDifusa(aper3, cierre3, a, m, b)
        p4 = pertenenciaVelaPequeniaDifusa(aper4, cierre4, a, m, b)
        p5 = pertenenciaVelaGrandeDifusa(aper5, cierre5, a, m, b)

        p1 = 0.1 * p1
        p2 = 0.1 * p2
        p3 = 0.1 * p3
        p4 = 0.1 * p4
        p5 = 0.1 * p5
        p = p + p1 + p2 + p3 + p4 + p5

        if cierre1>aper2 and aper1<cierre4:
            p = p + float(0.1)
        if cierre2>cierre3 and cierre3>cierre4:
            p = p + float(0.1)
        if aper4<aper5:
            p = p + float(0.1)

    return p

def formacionConGapBajistaDifusa(aper1, cierre1, aper2, cierre2, aper3, cierre3, aper4, cierre4, aper5, cierre5,fechaInicio, fechaFin, archivo, procedencia):
    p = float(0.0)
    if aper1>cierre1 and aper2<cierre2 and aper3<cierre3 and aper4<cierre4 and aper5>cierre5:
        p = float(0.2)

        alto, medio, bajo = patrones.detectarTamVelasSegunCuerpo(fechaInicio, fechaFin, archivo, procedencia)
        l = len(bajo)
        l = l/2
        l = int(l)
        a = bajo[l]
        m = medio[0]
        b = medio[len(medio)-1]
        p1 = pertenenciaVelaGrandeDifusa(aper1, cierre1, a, m, b)
        p2 = pertenenciaVelaPequeniaDifusa(aper2, cierre2, a, m, b)
        p3 = pertenenciaVelaPequeniaDifusa(aper3, cierre3, a, m, b)
        p4 = pertenenciaVelaPequeniaDifusa(aper4, cierre4, a, m, b)
        p5 = pertenenciaVelaGrandeDifusa(aper5, cierre5, a, m, b)

        p1 = 0.1 * p1
        p2 = 0.1 * p2
        p3 = 0.1 * p3
        p4 = 0.1 * p4
        p5 = 0.1 * p5
        p = p + p1 + p2 + p3 + p4 + p5

        if aper2<aper3 and aper3<aper4:
            p = p + float(0.1)
        if cierre1<aper2 and cierre4<aper1:
            p = p + float(0.1)
        if aper4>aper5:
            p = p + float(0.1)

    return p
