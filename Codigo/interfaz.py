from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
import os
from pandas_datareader import data as pdr     #Obtener archivos desde API Yahoo Finance
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox as mb
import os.path

import localizarPatrones
import visualizarGrafico
import velas
import difuso
import localizarPatronesDifusos

def calcularPosicionMaximo(valores):
    max=valores[0]
    pos = int(0)
    for i in len(valores):
        if valores[i]>max:
            max = valores[i]
            pos = i
    return pos

#VARIABLES GLOBALES

imagen="blanco.png"
#Obtener el directorio actual de trabajo
dir = os.getcwd()

#CLASE PRINCIPAL

class Application():
    #Por defecto, la fecha incial es 30 dias antes a la fecha de fin, que es la actual
    #Calcular fecha actual
    fechaSeleccionadaFin=datetime.date.today()
    dias = datetime.timedelta(days=30)
    #Calcular fecha inicial
    fechaSeleccionadaInicio=fechaSeleccionadaFin - dias
    #Aqui se almacena la primera imagen por defecto
    graficos = imagen
    graficospatrones = "./imagenes/blanco.png"
    suma=0
    fin=False

    def __init__(self):
        self.window = Tk()
        self.window.config(bg="white")
        #Cálculo para ocupar la pantalla completa
        self.window.geometry("{0}x{1}+0+0".format(self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.window.title("Análisis Bursatil")

        #Variables globales
        self.archivo = StringVar()
        self.intervalo = IntVar()
        self.variable = StringVar()
        self.procedencia = StringVar() #Dos opciones: csv ó menu
        self.valor = StringVar()


        #Botonotes para seleccionar intervalo de fechas
        self.createCalendario(texto="Fecha Inicio", momento="inicio")
        self.createLabelTextoFecha(momento="inicio")
        self.createCalendario(texto="Fecha Final", momento="fin")
        self.createLabelTextoFecha(momento="fin")
        #Cuadro para leer un archivo CSV
        self.seleccionaCSV()
        #Menu Desplegable para seleccionar
        self.menuDesplegable()
        #Visualización del Gráfico de Velas Japonesas
        self.grafico()
        #Boton para iniciar el algoritmo de reconocimiento de patrones
        self.encontrarPatrones()
        self.encontrarPatronesDifusos()
        #Boton para salir del programa
        self.createExit()

        self.window.mainloop()



#Mostrar Boton de salida
    def createExit(self):
        self.button = Button(self.window, text="Salir", command= self.window.quit,highlightbackground="red", foreground="black")
        self.button.grid(row=8, column=6)
#Mostrar Boton para ejecutar el algoritmo de reconocimiento de patrones
    def encontrarPatrones(self):
        self.patrones = Button(self.window, text="Hallar Patrones", command= self.reconocerPatrones,highlightbackground="green", foreground="black")
        self.patrones.grid(row=6, column=6)

    def reconocerPatrones(self):
        self.graficospatrones = "./imagenes/blanco1.png"
        self.suma=0
        self.fin=False
        def siguientePatron():
            if self.fin==False:
                if self.procedencia=="csv":
                    self.graficos, self.fin, self.suma, nombreVela= localizarPatrones.hallarPatrones(fechaInicio=self.fechaSeleccionadaInicio, fechaFin=self.fechaSeleccionadaFin, archivo=self.archivo.get(), procedencia=self.procedencia, contador=self.suma)
                else:
                    self.graficos, self.fin, self.suma, nombreVela= localizarPatrones.hallarPatrones(fechaInicio=self.fechaSeleccionadaInicio, fechaFin=self.fechaSeleccionadaFin, archivo=self.dataFrame, procedencia=self.procedencia, contador=self.suma)
                self.graficos = PhotoImage(file=self.graficos)
                self.tag.configure(image=self.graficos)
                self.graficospatrones = PhotoImage(file="./imagenes/"+nombreVela+".png")
                self.graf.configure(image=self.graficospatrones)
                self.etiqP.configure(text=velas.nombreVela(nombreVela))
                self.etiqP1.configure(text=velas.descripcionVela(nombreVela))
                #self.etiqDisufo.configure(text=difuso.pertenencia(nombreVela))

            elif self.fin==True:
                self.graficospatrones = PhotoImage(file="./imagenes/blanco1.png")
                self.graf.configure(image=self.graficospatrones)
                self.etiqP.configure(text="No se han encontrado más patrones")
                self.etiqP1.configure(text="Ha finalizado el análisis de Patrones")



                #Actualizar a la nueva imagen

        top = Toplevel(self.window)
        top.geometry("300x470")
        top.title("Reconocimiento de Patrones")

        self.etiqP = Label(top, text=" Comienza el Reconocimiento de Patrones ")
        self.etiqP.pack()
        self.graficospatrones = PhotoImage(file=self.graficospatrones)
        self.graf = Label(top, image=self.graficospatrones, padx=10, pady=10, bg="white")
        self.graf.pack()
        self.etiqP1 = Label(top, text="Pulse el Botón inferior")
        self.etiqP1.pack()
        self.etiqP2 = Label(top, text=" ")
        self.etiqP2.pack()
        self.etiqP2 = Label(top, text=" ")
        self.etiqP2.pack()
        Button(top, text="Siguiente Patrón", command=siguientePatron, width=17).pack()
        Button(top, text="Cerrar", command=top.destroy, width=10).pack()
        #top.update_idletasks()
        #top.update()

    def encontrarPatronesDifusos(self):
        self.patrones1 = Button(self.window, text="Hallar Patrones Difusos", command= self.reconocerPatronesDifusos,highlightbackground="blue", foreground="black")
        self.patrones1.grid(row=7, column=6)

    def reconocerPatronesDifusos(self):
        self.graficospatrones = "./imagenes/blanco1.png"
        self.graficospatrones1 = "./imagenes/blanco1.png"
        self.graficospatrones2 = "./imagenes/blanco1.png"
        self.suma=0
        self.fin=False
        def siguientePatron():
            if self.fin==False:
                if self.procedencia=="csv":
                    self.graficos, self.fin, self.suma, nomVelaPertenencia, pertenencia= localizarPatronesDifusos.hallarPatronesDifusos(fechaInicio=self.fechaSeleccionadaInicio, fechaFin=self.fechaSeleccionadaFin, archivo=self.archivo.get(), procedencia=self.procedencia, contador=self.suma)
                else:
                    self.graficos, self.fin, self.suma, nomVelaPertenencia, pertenencia= localizarPatronesDifusos.hallarPatronesDifusos(fechaInicio=self.fechaSeleccionadaInicio, fechaFin=self.fechaSeleccionadaFin, archivo=self.dataFrame, procedencia=self.procedencia, contador=self.suma)
                self.graficos = PhotoImage(file=self.graficos)
                self.tag.configure(image=self.graficos)
                if len(pertenencia)>=3:
                    self.graficospatrones = PhotoImage(file="./imagenes/"+nomVelaPertenencia[0]+".png")
                    self.graf.configure(image=self.graficospatrones)
                    self.etiqP.configure(text=velas.nombreVela(nomVelaPertenencia[0]))
                    self.etiqP1.configure(text="Grado de Pertenencia: "+str(round(pertenencia[0],2)))

                    self.graficospatrones1 = PhotoImage(file="./imagenes/"+nomVelaPertenencia[1]+".png")
                    self.graf1.configure(image=self.graficospatrones1)
                    self.etiqP2.configure(text=velas.nombreVela(nomVelaPertenencia[1]))
                    self.etiqP3.configure(text="Grado de Pertenencia: "+str(round(pertenencia[1],2)))

                    self.graficospatrones2 = PhotoImage(file="./imagenes/"+nomVelaPertenencia[2]+".png")
                    self.graf2.configure(image=self.graficospatrones2)
                    self.etiqP4.configure(text=velas.nombreVela(nomVelaPertenencia[2]))
                    self.etiqP5.configure(text="Grado de Pertenencia: "+str(round(pertenencia[2],2)))



                elif len(pertenencia)==2:
                    self.graficospatrones = PhotoImage(file="./imagenes/"+nomVelaPertenencia[0]+".png")
                    self.graf.configure(image=self.graficospatrones)
                    self.etiqP.configure(text=velas.nombreVela(nomVelaPertenencia[0]))
                    self.etiqP1.configure(text="Grado de Pertenencia: "+str(round(pertenencia[0],2)))

                    self.graficospatrones1 = PhotoImage(file="./imagenes/"+nomVelaPertenencia[1]+".png")
                    self.graf1.configure(image=self.graficospatrones1)
                    self.etiqP2.configure(text=velas.nombreVela(nomVelaPertenencia[1]))
                    self.etiqP3.configure(text="Grado de Pertenencia: "+str(round(pertenencia[1],2)))

                    self.graficospatrones2 = PhotoImage(file="./imagenes/blanco1.png")
                    self.graf2.configure(image=self.graficospatrones2)
                    self.etiqP4.configure(text=" ")
                    self.etiqP5.configure(text=" ")



                elif len(pertenencia)==1:
                    self.graficospatrones = PhotoImage(file="./imagenes/"+nomVelaPertenencia[0]+".png")
                    self.graf.configure(image=self.graficospatrones)
                    self.etiqP.configure(text=velas.nombreVela(nomVelaPertenencia[0]))
                    self.etiqP1.configure(text="Grado de Pertenencia: "+str(round(pertenencia[0],2)))
                    #Vaciar los otros
                    self.graficospatrones1 = PhotoImage(file="./imagenes/blanco1.png")
                    self.graf1.configure(image=self.graficospatrones1)
                    self.etiqP2.configure(text=" ")
                    self.etiqP3.configure(text=" ")

                    self.graficospatrones2 = PhotoImage(file="./imagenes/blanco1.png")
                    self.graf2.configure(image=self.graficospatrones2)
                    self.etiqP4.configure(text=" ")
                    self.etiqP5.configure(text=" ")




            elif self.fin==True:
                self.graficospatrones = PhotoImage(file="./imagenes/blanco1.png")
                self.graf.configure(image=self.graficospatrones)
                self.etiqP.configure(text="No se han encontrado más patrones")
                self.etiqP1.configure(text="Ha finalizado el análisis de Patrones")
                self.graficospatrones1 = PhotoImage(file="./imagenes/blanco1.png")
                self.graf1.configure(image=self.graficospatrones1)
                self.etiqP2.configure(text=" ")
                self.etiqP3.configure(text=" ")
                self.graficospatrones2 = PhotoImage(file="./imagenes/blanco1.png")
                self.graf2.configure(image=self.graficospatrones2)
                self.etiqP4.configure(text=" ")
                self.etiqP5.configure(text=" ")


        #Actualizar a la nueva imagen

        top = Toplevel(self.window)
        top.geometry("670x400")
        top.title("Reconocimiento de Patrones")

        self.etiqP = Label(top, text=" Comienza el Reconocimiento de Patrones ")
        self.etiqP.grid(row=1, column=1)
        self.graficospatrones = PhotoImage(file=self.graficospatrones)
        self.graf = Label(top, image=self.graficospatrones, padx=10, pady=10, bg="white")
        self.graf.grid(row=2, column=0, columnspan = 2)
        self.etiqP1 = Label(top, text="Pulse el Botón inferior ")
        self.etiqP1.grid(row=3, column=1)

        self.etiqP2 = Label(top, text=" ")
        self.etiqP2.grid(row=1, column=3)
        self.graficospatrones1 = PhotoImage(file=self.graficospatrones1)
        self.graf1 = Label(top, image=self.graficospatrones1, padx=10, pady=10, bg="white")
        self.graf1.grid(row=2, column=2, columnspan = 2)
        self.etiqP3 = Label(top, text=" ")
        self.etiqP3.grid(row=3, column=3)

        self.etiqP4 = Label(top, text=" ")
        self.etiqP4.grid(row=1, column=5)
        self.graficospatrones2 = PhotoImage(file=self.graficospatrones2)
        self.graf2 = Label(top, image=self.graficospatrones2, padx=10, pady=10)
        self.graf2.grid(row=2, column=4,columnspan=2)
        self.etiqP5 = Label(top, text=" ")
        self.etiqP5.grid(row=3, column=5)


        Button(top, text="Siguiente Patrón", command=siguientePatron, width=17).grid(row=4, column=1)
        Button(top, text="Cerrar", command=top.destroy, width=10).grid(row=5, column=1)
        #top.update_idletasks()
        #top.update()

#Mostrar boton para cambiar la fecha
    def createLabelTextoFecha(self, momento):
        if momento=="inicio":
            self.etiq7 = Label(self.window, text="Fecha Inicio:", bg="white")
            self.etiq7.grid(row=2, column=4, sticky=E)
            self.tag1 = Label(self.window, text=self.fechaSeleccionadaInicio, fg="blue", bg="white")
            self.tag1.grid(row=2, column=5, sticky=W)
        if momento=="fin" :
            self.etiq8 = Label(self.window, text="Fecha Fin:", bg="white")
            self.etiq8.grid(row=3, column=4, sticky=E)
            self.tag2 = Label(self.window, text=self.fechaSeleccionadaFin, fg="red", bg="white")
            self.tag2.grid(row=3, column=5,  sticky=W)
    def calendarioInicio(self):
        def print_sel():
            if cal.selection_get() > self.fechaSeleccionadaFin:
                mb.showinfo("Información", "La fecha de inicio no puede ser posterior a la fecha de fin")
            else:
                self.fechaSeleccionadaInicio=cal.selection_get()
                self.tag1["text"] = self.fechaSeleccionadaInicio
                mb.showinfo("Información", "Fecha Inicio Cambiada")
                #ACTUALIZACION DE LA GRAFICA
                if self.procedencia=="csv":
                    self.graficos= visualizarGrafico.mostrarGrafico(fechaInicio=self.fechaSeleccionadaInicio, fechaFin=self.fechaSeleccionadaFin, archivo=self.archivo.get())
                if self.procedencia=="menu":
                    nomArch = pdr.get_data_yahoo(self.valor, start=self.fechaSeleccionadaInicio, end=self.fechaSeleccionadaFin)
                    self.dataFrame = nomArch
                    self.graficos= visualizarGrafico.mostrarGraficoDataFrame(archivo=self.dataFrame, nombre=self.valor, fechaInicio=self.fechaSeleccionadaInicio, fechaFin=self.fechaSeleccionadaFin)
                self.graficos = PhotoImage(file=self.graficos)
                self.tag.configure(image=self.graficos)
                self.tag["image"] = self.graficos


        top = Toplevel(self.window)
        top.geometry("500x500")
        top.title("Seleccione una fecha")
        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                   cursor="hand1", year=2019, month=8, day=5)
        cal.pack(fill="both", expand=True)
        Button(top, text="Seleccionar Fecha Inicio", command=print_sel).pack()
        Button(top, text="Cerrar", command=top.destroy).pack()

    def calendarioFin(self):
        def print_sel():
            if cal.selection_get() < self.fechaSeleccionadaInicio:
                mb.showinfo("Información", "La fecha de fin no puede ser anterior a la fecha de inicio")
            else:
                self.fechaSeleccionadaFin=cal.selection_get()
                self.tag2["text"] = self.fechaSeleccionadaFin
                mb.showinfo("Información", "Fecha Fin Cambiada")
                #ACTUALIZACION DE LA GRAFICA
                if self.procedencia=="csv":
                    self.graficos= visualizarGrafico.mostrarGrafico(fechaInicio=self.fechaSeleccionadaInicio, fechaFin=self.fechaSeleccionadaFin, archivo=self.archivo.get())
                if self.procedencia=="menu":
                    nomArch = pdr.get_data_yahoo(self.valor, start=self.fechaSeleccionadaInicio, end=self.fechaSeleccionadaFin)
                    self.dataFrame = nomArch
                    self.graficos= visualizarGrafico.mostrarGraficoDataFrame(archivo=self.dataFrame, nombre=self.valor, fechaInicio=self.fechaSeleccionadaInicio, fechaFin=self.fechaSeleccionadaFin)
                self.graficos = PhotoImage(file=self.graficos)
                self.tag.configure(image=self.graficos)
                self.tag["image"] = self.graficos

        top = Toplevel(self.window)
        top.geometry("500x500")
        top.title("Seleccione una fecha")
        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                   cursor="hand1", year=2019, month=9, day=5)
        cal.pack(fill="both", expand=True)
        Button(top, text="Seleccionar Fecha Fin", command=print_sel).pack()
        Button(top, text="Cerrar", command=top.destroy).pack()

    def createCalendario(self, texto="Fecha", momento="inicio"):
        texto = "Cambiar " + texto
        if momento=="inicio":
            Button(self.window, text=texto, command=self.calendarioInicio).grid(row=2, column=6, sticky=W)
        if momento=="fin":
            Button(self.window, text=texto, command=self.calendarioFin).grid(row=3, column=6, sticky=W)

#Añadir cuandro para introducir un archivo csv
    def seleccionaCSV(self):
        #Etiqueta de Añadir CSV
        self.etiq1 = Label(self.window, text="Añadir CSV de datos:", bg="white")
        self.etiq1.grid(row=2, column=1, sticky=E)
        #Cuadro para introducir CSV
        self.ctexto1 = Entry(self.window, textvariable=self.archivo,width=30)
        self.ctexto1.grid(row=2, column=2, sticky=W)
        #Boton para cargar el CSV
        self.boton1 = Button(self.window, text="Cargar Archivo", command=self.cargarArchivo)
        self.boton1.grid(row=3, column=2)

    def cargarArchivo(self):
        print(self.archivo.get())
        permitidas = ['csv']
        extension = self.archivo.get().split('.')[-1]
        if extension in permitidas:
            print("El archivo ha sido cargado correctamente")
            mb.showinfo("Información", "El archivo ha sido cargado correctamente")
            print(self.archivo.get())
            self.graficos= visualizarGrafico.mostrarGrafico(fechaInicio=self.fechaSeleccionadaInicio, fechaFin=self.fechaSeleccionadaFin, archivo=self.archivo.get())
            self.graficos = PhotoImage(file=self.graficos)
            self.tag.configure(image=self.graficos)
            self.tag["image"] = self.graficos
            self.procedencia = "csv"
        else:
            print("El archivo no es de tipo CSV")
            mb.showinfo("Información", "El archivo no es de tipo CSV")

#Mostrar imágenes
    def grafico(self):

        self.graficos = PhotoImage(file=self.graficos)
        # Ponemos la imagen en un label dentro de la ventana
        self.tag=Label(self.window, image=self.graficos, width=1340, bg="white")
        self.tag.grid(row=0, column=1, columnspan=6, rowspan=2,
               padx=50, pady=50)



#Menú Desplegable
    def menuDesplegable(self):
        self.etiq5 = Label(self.window, text="ó", bg="white")
        self.etiq5.grid(row=4, column=2, sticky=W)
        self.etiq6 = Label(self.window, text="Seleccione una opción:", bg="white")
        self.etiq6.grid(row=5, column=1, sticky=E)
        self.combo = ttk.Combobox(self.window, textvariable=self.variable)
        self.combo.grid(row=5, column=2, sticky=W)
        self.combo["values"] = ["IBEX", "BBVA", "Santander", "Telefónica", "Iberdrola"]
        #self.combo.current(0)
        self.combo.bind('<<ComboboxSelected>>', self.callback)

    def callback(self, event=None):
        if event:
            if self.variable.get()=="Santander":
                self.valor = "SAN"
                nomArch = pdr.get_data_yahoo(self.valor, start=self.fechaSeleccionadaInicio, end=self.fechaSeleccionadaFin)
                self.graficos= visualizarGrafico.mostrarGraficoDataFrame(archivo=nomArch, nombre="SAN", fechaInicio=self.fechaSeleccionadaInicio, fechaFin=self.fechaSeleccionadaFin)
            if self.variable.get()=="BBVA":
                self.valor="BBVA"
                nomArch = pdr.get_data_yahoo(self.valor, start=self.fechaSeleccionadaInicio, end=self.fechaSeleccionadaFin)
                self.graficos= visualizarGrafico.mostrarGraficoDataFrame(archivo=nomArch, nombre="BBVA", fechaInicio=self.fechaSeleccionadaInicio, fechaFin=self.fechaSeleccionadaFin)
            if self.variable.get()=="IBEX":
                self.valor = "^IBEX"
                nomArch = pdr.get_data_yahoo(self.valor, start=self.fechaSeleccionadaInicio, end=self.fechaSeleccionadaFin)
                self.graficos= visualizarGrafico.mostrarGraficoDataFrame(archivo=nomArch, nombre="IBEX", fechaInicio=self.fechaSeleccionadaInicio, fechaFin=self.fechaSeleccionadaFin)
            if self.variable.get()=="Telefónica":
                self.valor = "TNE2.BE"
                nomArch = pdr.get_data_yahoo(self.valor, start=self.fechaSeleccionadaInicio, end=self.fechaSeleccionadaFin)
                self.graficos= visualizarGrafico.mostrarGraficoDataFrame(archivo=nomArch, nombre="Telefonica", fechaInicio=self.fechaSeleccionadaInicio, fechaFin=self.fechaSeleccionadaFin)
            if self.variable.get()=="Iberdrola":
                self.valor = "IBE.MC"
                nomArch = pdr.get_data_yahoo(self.valor, start=self.fechaSeleccionadaInicio, end=self.fechaSeleccionadaFin)
                self.graficos= visualizarGrafico.mostrarGraficoDataFrame(archivo=nomArch, nombre="Iberdrola", fechaInicio=self.fechaSeleccionadaInicio, fechaFin=self.fechaSeleccionadaFin)
            self.dataFrame = nomArch
            self.procedencia = "menu"
            self.graficos = PhotoImage(file=self.graficos)
            self.tag.configure(image=self.graficos)
            self.tag["image"] = self.graficos

#####################################################


Application()
