from tkinter import *
import matplotlib.pyplot as plt
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import requests
import json

root = Tk()

root.geometry("1080x720")
root.resizable(0,0)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

container = Frame(root, bg='green')
container.grid(row=0, column=0, sticky="nswe")

container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# frame izquierda
container1 = Frame(container, bg='red')
container1.grid(row=0, column=0, sticky='nsew')

container1.grid_rowconfigure(0, weight=30)
#container1.grid_rowconfigure(1, weight=1, minsize=15)
container1.grid_columnconfigure(0, weight=1)

container1_1 = Frame(container1, bg ='#002060')
container1_1.grid(row=0, column=0, sticky='nsew')
container1_1.grid_rowconfigure(0, weight=1)
container1_1.grid_rowconfigure(1, weight=1)
container1_1.grid_rowconfigure(2, weight=1)
container1_1.grid_columnconfigure(0, weight=1)

container1_1_1 = Frame(container1_1)
container1_1_1.grid(row=0,column=0,sticky='nsew', padx = 10, pady = 10)

container1_1_2 = Frame(container1_1)
container1_1_2.grid(row=1,column=0,sticky='nsew', padx = 10, pady = 10)

container1_1_3 = Frame(container1_1)
container1_1_3.grid(row=2,column=0,sticky='nsew', padx = 10, pady = 10)


plt.style.use('ggplot')

indice = []
conteo = []
humedad = []
temperatura = []

contador = 0

def recibir_data(index):
    response = requests.get('https://38c6-2800-200-e250-d43-c463-a616-e444-1564.ngrok.io/data')
    cadenas = response.text[2:-3].split("},{")

    new_cadena = "{"+cadenas[index]+"}"
    json_object = json.loads(new_cadena)
    contador_pasadas = json_object["contador_pasadas"]
    humedad = json_object["humedad"]
    temperatura = json_object["temperatura"]
    tiempo = json_object["tiempo"]
    id = json_object["id"]
    return id, contador_pasadas, humedad, temperatura, tiempo

def Creacion_Grafica_Real_Time_2(num):
    dic2 = {1:humedad, 2:conteo, 3:temperatura}
    dic3 = {1:"humedad", 2:"cantidad entradas/salidas", 3:"temperatura"}
    figure = pyplot.figure()
    line, = pyplot.plot(indice, dic2[num] , '-')
    figure.suptitle(str(dic3[num]))
    def grafico(frame):
        line.set_data(indice, dic2[num])
        figure.gca().relim()
        figure.gca().autoscale_view()
        return line,

    dic = {1:container1_1_1, 2:container1_1_2, 3:container1_1_3}
    canvas = FigureCanvasTkAgg(figure, master=dic[num])
    canvas.get_tk_widget().pack(side=TOP)
    
    canvas._tkcanvas.pack(side=BOTTOM,fill=BOTH, expand=True)
    animation = FuncAnimation(figure, grafico, interval=1000)
    return animation

def Creacion_Grafica_Real_Time(num):
    dic2 = {1:humedad, 2:conteo, 3:temperatura}
    dic3 = {1:"humedad", 2:"cantidad entradas/salidas", 3:"temperatura"}
    figure = pyplot.figure()
    figure.suptitle(str(dic3[num]))
    line, = pyplot.plot(indice, dic2[num] , '-')
    def grafico(frame):
        global contador
        contador += 1
        id, contador_pasadas_v, humedad_v, temperatura_v, tiempo_v = recibir_data(contador)
        indice.append(int(id))
        conteo.append(int(contador_pasadas_v))
        humedad.append(int(float(humedad_v)*100))
        temperatura.append(int(float(temperatura_v)*100))
        line.set_data(indice, dic2[num])
        figure.gca().relim()
        figure.gca().autoscale_view()
        return line,

    dic = {1:container1_1_1, 2:container1_1_2, 3:container1_1_3}
    canvas = FigureCanvasTkAgg(figure, master=dic[num])
    canvas.get_tk_widget().pack(side=TOP)
    
    canvas._tkcanvas.pack(side=BOTTOM,fill=BOTH, expand=True)
    animation = FuncAnimation(figure, grafico, interval=1000)
    return animation
try:
    animation1 = Creacion_Grafica_Real_Time(1)
    animation2 = Creacion_Grafica_Real_Time_2(2)
    animation3 = Creacion_Grafica_Real_Time_2(3)
except Exception as e:
    print(e)
    pass
root.mainloop()
