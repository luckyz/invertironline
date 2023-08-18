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
    def login(self):
        if len(sys.argv) == 3:
            _user = sys.argv[1]
            _pass = sys.argv[2]
            _data = {
                'username':_user,
                'password':_pass,
                'grant_type':'password'
                }
            r = requests.post('https://api.invertironline.com/token', data=_data)
            c = 'Bearer ' + str(json.loads(r.text)['access_token'])
            borrarPant()

        else:
            _user = os.environ.get('IOL_USER')
            _pass = os.environ.get('IOL_PASSWORD')
            _data = {
                'username':_user,
                'password':_pass,
                'grant_type':'password'
                }
            r = requests.post('https://api.invertironline.com/token', data=_data)
            self.borrarPant()
            return 'Bearer ' + str(json.loads(r.text)['access_token'])

    def borrarPant(self):
        if os.name == 'posix':
            os.system('clear')
        elif os.name == 'ce' or os.name == 'nt' or os.name == 'dos':
            os.system('cls')

    def variacion(self, token, show=False):
        data = {'Authorization': token}
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
    token = iol.login()
    data = iol.variacion(token)

    gh = Github()
    #gh.download_from_github()
    
    db = Database()
    db.add_dict_data(data)
    
    #gh.upload_to_github()


if __name__ == '__main__':
    main()
