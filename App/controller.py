"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import time
import csv
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {
        'model': None
    }
    control['model'] = model.new_data_structs()
    return control



# Funciones para la carga de datos

def load_data(control):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    catalog = control['model']
    
    
    bogota_vertices = cf.data_dir + 'bogota_vertices.txt'
    
    bogota_edges = cf.data_dir + 'bogota_arcos.txt'
    
    infraction_file = cf.data_dir + 'comparendos_2019_bogota_vertices.csv'
    
    police_station_file = cf.data_dir + 'estacionpolicia_bogota_vertices.csv'

    with open(bogota_vertices, mode='r') as verts:
        
        line = verts.readline()
        
        while line:
            
            vert, long, lat = line.split(',')
            
            model.vertex(catalog, int(vert), float(lat), float(long))
            line = verts.readline()

    infractions_input = csv.DictReader(open(infraction_file, encoding='utf-8'))
    
    police_stations_input = csv.DictReader(open(police_station_file, encoding='utf-8'))
    
    for infraccion in infractions_input:
        
        model.add_infraction(catalog, int(infraccion['VERTICES']), infraccion)
        
        model.add_data_to_ind_set(catalog["infractions_by_type_service"], infraccion["TIPO_SERVICIO"], infraccion["INFRACCION"])
        
        model.add_data_to_ind_list(catalog["infractions_by_code_ticket"], infraccion["INFRACCION"], infraccion["VERTICES"])

    for estacion in police_stations_input:
        
        
        
        
        model.add_police_station(catalog, int(estacion['VERTICES']), estacion)

    with open(bogota_edges, mode='r') as verts:
        line = verts.readline()
        while line:
            line_info = line.split()
            for each_node in range(1, len(line_info)):
                
                model.add_edge(catalog, int(line_info[0]), int(line_info[each_node]))
                
            line = verts.readline()



# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control,latitud1, longitud1, latitud2, longitud2):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    
    
    return model.req_1(control['model'], latitud1, longitud1, latitud2, longitud2)




def req_2(control,latitud1, longitud1, latitud2, longitud2):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    model.req_2(control['model'], latitud1, longitud1, latitud2, longitud2)



def req_3(control,cams,lugar):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    lugar="CHAPINERO"
    
    cams=15
    model.req_3(control['model'], cams, lugar)


def req_4(control,cams):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    model.req_4(control, cams)


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(control):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(control):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
