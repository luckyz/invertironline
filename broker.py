#!/usr/bin/env python3
import requests
import json
import sys
import os
import time
from dotenv import load_dotenv
from database import Database
from github import Github

load_dotenv()

database = os.environ.get('DATABASE')


class InvertirOnline:
    
    token = None
    
    def __init__(self):
        self.login()
    
    def login(self):
        if len(sys.argv) == 3:
            _user = sys.argv[1]
            _pass = sys.argv[2]
            _data = {
                'username':_user,
                'password':_pass,
                'grant_type':'password'
                }

            self.borrarPant()

            r = requests.post('https://api.invertironline.com/token', data=_data)
            self.token = 'Bearer ' + str(json.loads(r.text)['access_token'])

        else:
            _user = os.environ.get('IOL_USER')
            _pass = os.environ.get('IOL_PASSWORD')
            _data = {
                'username':_user,
                'password':_pass,
                'grant_type':'password'
                }

            self.borrarPant()

            r = requests.post('https://api.invertironline.com/token', data=_data)
            self.token = 'Bearer ' + str(json.loads(r.text)['access_token'])

    def borrarPant(self):
        if os.name == 'posix':
            os.system('clear')
        elif os.name == 'ce' or os.name == 'nt' or os.name == 'dos':
            os.system('cls')

    def portafolio(self, show=False):
        data = {'Authorization': self.token}
        r = requests.get('https://api.invertironline.com/api/portafolio', headers=data)
        port = json.loads(r.text)
        lista = []
        
        n = 0
        while n < len(port['activos']):
            descripcion = port['activos'][n]['titulo']['descripcion']
            ultimo_precio = port['activos'][n]['ultimoPrecio']
            cantidad = port['activos'][n]['cantidad']
            moneda = port['activos'][n]['titulo']['moneda']
            ganancia_porcentaje = port['activos'][n]['gananciaPorcentaje']
            valorizado = port['activos'][n]['valorizado']
            simbolo = port['activos'][n]['titulo']['simbolo']
            variacion_diaria = port['activos'][n]['variacionDiaria']
            ganancia = port['activos'][n]['gananciaDinero']
            
            variacion_diaria = f'+{variacion_diaria}' if float(variacion_diaria) > 0.0 else variacion_diaria
            
            if show:
                print(f'{simbolo: <10}', variacion_diaria)
            
            datos = {}
            
            datos['descripcion'] = descripcion
            datos['ultimo_precio'] = ultimo_precio
            datos['cantidad'] = cantidad
            datos['moneda'] = moneda
            datos['ganancia_porcentaje'] = ganancia_porcentaje
            datos['valorizado'] = valorizado
            datos['simbolo'] = simbolo
            datos['variacion_diaria'] = variacion_diaria
            datos['ganancia'] = ganancia
            
            lista.append(datos)
            
            n += 1
            
        return lista

def main():
    iol = InvertirOnline()

    db = Database()
    db.add_dict_data(iol.portafolio())
    
    # db.upload()


if __name__ == '__main__':
    main()
