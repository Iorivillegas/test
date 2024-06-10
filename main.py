from datetime import datetime
import serial, time, requests
puertoSerial = serial.Serial('COM4', 9600)
time.sleep(2)   #Espera 2 segundos para conectar puerto serial

def calibracion():
    condicion = 0
    distancia_anterior = 0
    data = 0
    contador = 0
    while condicion == 0:
        try:
            raw_data = puertoSerial.readline()
            data = str(raw_data).replace("b'", "").replace("\\r\\n'", "")
            
            try:
                data = data.split("|")
                distancia = int(data[0].replace("cm", ""))
                if abs(distancia-distancia_anterior) == 0:
                    contador += 1
                elif contador > 0:
                    contador -= 1
                if contador == 5:
                    condicion = 1
                distancia_anterior = distancia
            except:
                pass
        except:
            break
    puertoSerial.close()
    return distancia

def deteccion(rango, ruta):
    contador_pasadas = 0
    data = 0
    bandera_entrada = 0
    distancia = 0
    contador_h_t = 0
    suma_humedad = 0
    suma_temperatura = 0
    contador = 0
    while 1:
        try:
            contador_h_t += 1
            raw_data = puertoSerial.readline()
            data = str(raw_data).replace("b'", "").replace("\\r\\n'", "").split("|")
            distancia = int(data[0].replace("cm", ""))
            suma_humedad += float(data[1].replace("%", ""))
            suma_temperatura += float(data[2].replace("C", ""))
            if contador_h_t == 10:
                humedad = str(round(suma_humedad/10, 2)) + "%"
                temperatura = str(round(suma_temperatura/10, 2)) + "C"
                print("humedad: " + humedad)
                print("temperatura: " + temperatura)
                suma_humedad = 0
                suma_temperatura = 0
                contador_h_t = 0
                time = str(datetime.now())
                enviar_data(ruta, str(contador), time, contador_pasadas, temperatura, humedad)
                contador += 1
            if abs(distancia - rango) > 3:
                bandera_entrada = 1
            if bandera_entrada == 1:
                if abs(distancia - rango) < 3:
                    bandera_entrada = 0
                    contador_pasadas += 1
                    print("cantidad de veces pasadas :" + str(contador_pasadas))
            
        except Exception as e:
            print(e)
            break
    puertoSerial.close()
    return contador_pasadas

def enviar_data(ruta, index,tiempo,pasadas,temperatura,humedad):
    api = "https://proyecto-adatos-default-rtdb.firebaseio.com/"+ruta+"/"+str(index)+".json"
    dataline = '{"tiempo":"'+str(tiempo)+'", "conteo":"'+str(pasadas)+'", "temperatura": "'+str(temperatura)+'", "humedad": "'+str(humedad)+'"}'
    x = requests.put(api, data = dataline)
    print(x.text)


api = "https://proyecto-adatos-default-rtdb.firebaseio.com/"
fecha = datetime.now()
dataline = '{ "fecha" : "'+str(fecha) + '"}'
titulo = "p"+str(fecha)[0:-7].replace(" ", "")+"p"
nueva_api = api + titulo + ".json"
nueva_api = nueva_api.replace(" ", "")
print(nueva_api)
x = requests.put(nueva_api, data=dataline)
print(x.text)

rango = calibracion()
print("rango es " + str(rango))
puertoSerial = serial.Serial('COM4', 9600)
print(titulo)
deteccion(rango, titulo)



