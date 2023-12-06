﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    return controller.new_controller()



def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")

def tabulate_data(elements, headers='', len=0, col=[]):
    """
    Dependiendo si es lista o diccionario la función 
    llamará a los métodos de tabulate para imprimir elements 
    """

    columnass = []
    
    
    if len > 0:
        columnas = [8 for _ in range(len)]
    if col:
        columnas = col
        
        
    if type(elements) is list:
        
        print(tabulate(elements, headers=(headers or 'keys'),
                       
              tablefmt='grid', maxcolwidths=columnas or None))
        
    if type(elements) is dict:
        print(tabulate([[i, j] for i, j in elements.items()], headers=(
            headers or elements.keys()), tablefmt="grid", maxcolwidths=columnas or None))

def printSubTable(dct):
    
    return tabulate([dct.keys(), dct.values()], tablefmt='grid')


def getSubTabulates(elems):
    
    respuesta = ""
    for elemento in elems:
        
        
        respuesta += printSubTable(elemento) + "\n"
        
    return respuesta


def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    controller.load_data(control)


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    latitud1 = float(input("Digite la latitud del vértice (origen): "))
    
    latitud2 = float(input("Ingrese la latitud del vértice (destino): "))
    
    
    longitud1 = float(input("Ingrese la longitud del vertice (origen): "))
           
    
    
    longitud2 = float(input("Ingrese la longitud del vertice (destino): "))


    vertices = controller.req_1(control, latitud1, longitud1, latitud2, longitud2)
    if vertices is None:
        
        print("No hay ruta")
        return

    tabulate_data(vertices[::-1])



def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    latitud1 = float(input("Digite la latitud del vértice (origen): "))
    
    latitud2 = float(input("Ingrese la latitud del vértice (destino): "))
    
    
    longitud1 = float(input("Ingrese la longitud del vertice (origen): "))
           
    
    
    longitud2 = float(input("Ingrese la longitud del vertice (destino): "))


    vertices = controller.req_2(control, latitud1, longitud1, latitud2, longitud2)
    if vertices is None:
        
        print("No hay ruta")
        return

    tabulate_data(vertices[::-1])


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    controller.req_3(control)


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    controller.req_4(control, 23)


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
