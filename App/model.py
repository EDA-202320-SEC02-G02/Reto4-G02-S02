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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf

import math as mat

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    catalogo = {
        "streets_graph": None,
        "vertices_by_lat&long": None,
        "streets_intersections_data": None,
        "infractions_by_district": None,
        "infractions_by_severity": None,
        "infractions_by_type_service": None,
        "infractions_by_code_ticket": None,
        "mst": None
    }

    catalogo["streets_graph"] = gr.newGraph(datastructure='ADJ_LIST', directed=False)
    
    catalogo["streets_intersections_data"] = mp.newMap(maptype='CHAINING', loadfactor=0.5)
    
    catalogo["infractions_by_district"] = mp.newMap(maptype='CHAINING', loadfactor=0.5)
    
    catalogo["infractions_by_severity"] = mp.newMap(maptype='CHAINING', loadfactor=0.5)
    
    catalogo["infractions_by_type_service"] = mp.newMap(maptype='CHAINING', loadfactor=0.5)
    
    catalogo["infractions_by_code_ticket"] = mp.newMap(maptype='CHAINING', loadfactor=0.5)
    
    catalogo["vertices_by_lat&long"] = mp.newMap(maptype='CHAINING', loadfactor=0.5)

    catalogo["mst"] = None

    return catalogo


# Funciones para agregar informacion al modelo

def add_data_to_ind_set(data_structs, llave,dato):
    """
    Función para agregar nuevos elementos a un mapa que contiene listas
    """
    if not mp.contains(data_structs, llave):
        empty = set()
        mp.put(data_structs, llave, empty)

    lst = me.getValue(mp.get(data_structs, llave))
    lst.add(dato)


def add_data_to_ind_list(data_structs, llave,dato):
    """
    Función para agregar nuevos elementos a un mapa que contiene listas
    """
    if not mp.contains(data_structs, llave):
        mp.put(data_structs, llave, lt.newList('ARRAY_LIST'))

    lst = me.getValue(mp.get(data_structs, llave))
    lt.addLast(lst, dato )

# Funciones para creacion de datos
def vertex(data_structs, vertice, latitud, longintud):
    
    
    gr.insertVertex(data_structs["streets_graph"], vertex)

    mp.put(data_structs["vertices_by_lat&long"], (latitud, longintud), vertice)


    mp.put(data_structs["streets_intersections_data"], vertice, {
        "intersection": {
            "lat": latitud,
            "long": longintud,
        },
        "police_stations": lt.newList("ARRAY_LIST"),
        "infractions": lt.newList("ARRAY_LIST"),
    })

def estacionespolicia(data_structs, vertice, estacion ):
    
    
    lista = me.getValue(mp.get(data_structs["streets_intersections_data"], vertice))["police_stations"]
    lt.addLast(lista, estacion)

def infracciones(data_structs, vertice, infraction  ):
    mapa = data_structs["infractions_by_district"]
    
    entry = mp.get(data_structs["streets_intersections_data"], vertice)
    
    lista = me.getValue(entry)["infractions"]
    

    if not mp.contains(mapa, infraction["LOCALIDAD"]):
        
        mp.put(mapa, infraction["LOCALIDAD"], mp.newMap(maptype='CHAINING', loadfactor=0.5))


    verticesmp = me.getValue(mp.get(mapa , infraction["LOCALIDAD" ] ))

    if not mp.contains(verticesmp , vertex):
        
        
        mp.put(verticesmp, vertice, 0)

    numeroinfractions = me.getValue(mp.get(verticesmp, vertice))

    mp.put(verticesmp, vertice,numeroinfractions + 1)
    
    
    lt.addLast(lista, infraction)

def edge(data_structs, verticeuno, verticedos):
    verticeunodato = me.getValue(mp.get(data_structs["streets_intersections_data"], verticeuno))
    
    
    verticedosdato = me.getValue(mp.get(data_structs["streets_intersections_data"], verticedos))
    
    latitud1 = verticeunodato["intersection"]["lat"]
    latitud2 = verticedosdato["intersection"]["lat"]
    longitud1 = verticeunodato["intersection"]["long"]
    
    longitud2 = verticedosdato["intersection"]["long"]

    distancia = distanciaa(latitud1 , longitud1, latitud2, longitud2  )

    gr.addEdge(data_structs["streets_graph"], verticeuno, verticedos, distancia )



def primeroultimo(lt, filter_data=None, size=3):
    """
    Retorna los n primeros y últimos elemento de la lista
    """
    primero = []
    ultimo = []

    if lt.size(lt) < size * 2:
        
        for i in range(1, lt.size(lt) + 1):
            
            el = datafiltrado(lt.getElement(lt, i), filter_data)
            
            primero.append(el)
            
    else:
        for i in range(1, size + 1):
            
            primeroo = datafiltrado(
                
                lt.getElement(lt, i), filter_data)
            
            primero.append(primeroo)
            
            ultimoo = datafiltrado(lt.getElement(
                lt, lt.size(lt) - i + 1), filter_data)
            
            ultimo.insert(0, ultimoo)
            

    return primero + ultimo



def datafiltrado(data , atributos):
    """
    Retorna un diccionario con los atributos de un dato
    """
    if not atributos:
        return data



    filtered_data = {}
    
    for llave in atributos:
        
        filtered_data[llave] = data[llave]
    return filtered_data


def distanciaa(latitud1, longitud1, latitud2, longitud2):
    """
    Retorna la distancia entre dos puntos en la tierra
    """
    latitud1 = mat.radians(latitud1)
    latitud2 = mat.radians(latitud2)
    
    longitud1 = mat.radians(longitud1)
    
    longitud2 = mat.radians(longitud2)

    return 2 * mat.asin(mat.sqrt(mat.sin((latitud2 - latitud1) / 2) ** 2 + mat.cos(latitud1) * mat.cos(latitud2) * mat.sin((longitud2 - longitud1) / 2) ** 2)) * 6371


def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass




def req_1(data_structs,latitud1,latitud2,longitud1,longitud2):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    
    vertice1 = me.getValue(mp.get(data_structs["vertices_by_lat&long"], (latitud1, longitud1)))
    
    
    vertice2 = me.getValue(mp.get(data_structs["vertices_by_lat&long"], (latitud2, longitud2)))
   
    busqueda = dfs.DepthFirstSearch(data_structs["streets_graph"], vertice1)



    caminoo = dfs.pathTo(busqueda, vertice2)

    if caminoo is None:
        return None
    
    verticeslst = []

    for verticee in lt.iterator(caminoo):
        
        
        datav = me.getValue(mp.get(data_structs["streets_intersections_data"], verticee))
        
        verticeslst.append({
            "intersection_id": verticee,
            
            "lat": datav["intersection"]["lat"],
            
            "long": datav["intersection"]["long"],
            
            "police_stations": len(datav["police_stations"]),
            
            "infractions": len(datav["infractions"]),
            
            
        })

    return verticeslst



def req_2(data_structs,latitud1,latitud2,longitud1,longitud2):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    vertice1 = me.getValue(mp.get(data_structs["vertices_by_lat&long"], (latitud1, longitud1)))
    
    
    vertice2 = me.getValue(mp.get(data_structs["vertices_by_lat&long"], (latitud2, longitud2)))
    
    busqueda = bfs.BreadhtFisrtSearch(data_structs["streets_graph"], vertice1)

    caminoo = bfs.BreadhtFisrtSearch(busqueda, vertice2)

    if caminoo is None:
        return None
    
    
    verticeslst = []

    for verticee in lt.iterator(caminoo):
        datav = me.getValue(mp.get(data_structs["streets_intersections_data"], verticee))
        verticeslst.append({
            
            "intersection_id": verticee,
            "lat": datav["intersection"]["lat"],
            
            "long": datav["intersection"]["long"],
            
            
            "police_stations": len(datav["police_stations"]),
            
            "infractions": len(datav["infractions"]),
        })



def req_3(data_structs,  cams,  lugar):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    verticeslugar = me.getValue(mp.get(data_structs["infractions_by_district"], lugar  ) ) 
    
    lugarvertices = mp.keySet(verticeslugar)
    
    
    verticeslist = lt.newList("ARRAY_LIST")
    
    for verticee in lt.iterator(lugarvertices):
        
        
        lt.addLast(verticeslist, (verticee, me.getValue(mp.get(verticeslugar, verticee))))

    verticeslist = sort(verticeslist , composed_sort([comparavertices]))
    
    
    print("Los Vertices:", lt.subList(verticeslist, 1, cams))
    



def req_4(data_structs,cams):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    tipo = data_structs['model']["infractions_by_type_service"]
    
    
    cod = data_structs['model']["infractions_by_code_ticket"]
    
    
    entry = mp.get(tipo, "Diplomatico")
    
    
    valoresentry = me.getValue(entry)
    
    orden= sorted(valoresentry, reverse=True)
    cams =10
    severoo = lt.newList('ARRAY_LIST')
    
    
    while (cams > 0):
        for cada in orden:
            
            
            if (cams == 0):
                break
            
            
                #cams=7
            codentry = mp.get(cod, cada)
            
            codvalues = me.getValue(codentry )
            
            for cadaa in lt.iterator(codvalues):
                
                
                if ( not lt.isPresent( severoo ,cadaa )):
                    
                    
                    lt.addLast(severoo, cadaa )
                    cams -= 1
                    
                if (cams == 0):
                    break
             
             
             
    print( "Nodos severos/graves: ", severoo )



def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que solucionsa el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass

def composed_sort(cmp_list):
    
    def cmp(data1, data2):
        for cmp_function in cmp_list:
            result = cmp_function(data1, data2)
            if result != 0:
                return result > 0
        return False
    return cmp

def comparavertices(v1, v2):
    
    
    if v1[1] == v2[1]:
        
        return 0
    
    elif v1[1] > v2[1]:
        
        
        return 1
    
    else:
        return -1


def sort(data_structs, criteria):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    
    return merg.sort(data_structs, criteria)


def mst(data_structs):
    """
    Función que retorna el arbol de expansión mínima del grafo
    """
    
    
    if data_structs["mst"] is None:
        
        
        data_structs["mst"] = prim.PrimMST(data_structs["streets_graph"] )
    return data_structs ["mst"] 
