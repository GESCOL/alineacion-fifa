import queue
import math
from formaciones import *

class Archivador():

  mejor_alineacion = 0
  @staticmethod
  def read_formaciones():
    pass

  @staticmethod
  def read_jugadores():
    with open('jugadores.txt') as f:
      lines = f.readlines()    

    jugadores = []
    for line in lines:
      jugadores.append(Archivador.create_jugador(line))

    return jugadores

  
  @staticmethod
  def create_jugador(line):
    values = line.split(',')

    num = values[0]
    med = values[1]
    pos = values[2]
    lin = int(values[3])

    jugador = Jugador(num, pos, med, lin)
    return jugador


class Jugador():
  
  def __init__(self, numero, posicion, media, linea_jugador):
      self.numero = numero
      self.posicion = posicion
      self.media = media
      self.linea_jugador = linea_jugador


  
    
  

class Generador():

  @staticmethod
  def get_cola_ordenada(jugadores):

    cola_ordenada = queue.Queue()
    jugadores.sort(key = lambda x: x.media, reverse=True)

    for j in jugadores:
      cola_ordenada.put(j)

    return cola_ordenada

  @staticmethod
  def potenciar_jugador(posicion, jugador, val_ten, formacion):

    n = val_ten

    if(jugador.posicion != posicion):
      n -= 2
    if((jugador.linea_jugador - formacion.valor_equilibrio) == 2):
      n += 1	
    elif((jugador.linea_jugador + formacion.valor_equilibrio) == 2):
      n -= 1
    
    return n   

  @staticmethod
  def puntuar_jugador(jugador, formacion):

    n = jugador.media

    in_val = False

    for i in formacion:
      for j in i:
        if(jugador.posicion == j):
          in_val = True

    if(not in_val):
      n -= 2
    else:
      pass

          

    if((jugador.posicion_linea - formacion.val_equilibrio) == 2):
      n += 1	
    elif((jugador.posicion_linea + formacion.val_equilibrio) == 2):
      n -= 1
    
    return n   

  @staticmethod
  def get_mejor_formacion(formaciones, jugadores):

    formaciones_aux = formaciones[:][:]
    val = 0

    jugador = jugadores.get()

    pos_jugador = Formacion.posiciones.get(jugador.posicion)
    cont = 0

    if(jugador.posicion == 'POR'):
      val = -1
    #else:
     # val = jugador.linea_jugador - 2

    len_formaciones = len(formaciones)

    for i in range(len_formaciones):
      
      formacion = formaciones[i]

      if(formaciones[i] == 0):
        continue
      
      if(val == formacion.valor_equilibrio):        
        var_pos = math.gcd(formacion.get_codigo(), pos_jugador)
        if(var_pos == pos_jugador):
          cont+=1
        else:
          formaciones[i] = 0
      else:
        formaciones[i] = 0

    if (cont==1):
      for formacion in formaciones:
        if (formacion!=0):
          return formacion
    elif(cont>1):
      return Generador.get_mejor_formacion(formaciones, jugadores)
    else:
      if(jugadores.qsize() < 10):
        
        my_list = []
        jugador_formacion = {}
        
        for f in formaciones_aux:
          if(f != 0):
            jugador_formacion[f] = Generador.puntuar_jugador(jugador, f)

        items_jugador_formacion = jugador_formacion.items()

        sorted_items = sorted(items_jugador_formacion, key=lambda tup: tup[1])

        final_items = []        
        max_val = sorted_items[0][1]
        i = 0
        while(sorted_items[i][1] == max_val):
          final_items.append(sorted_items[i])
          i += 1
        
        formaciones_final = []
        for i in final_items:
          formaciones_final.append(i[0])

        if(len(formaciones_final) > 1):
          Generador.get_mejor_formacion(formaciones_final, jugadores)
        else:
          return formaciones_final[0]    

  @staticmethod
  def check_alineacion(alineacion, suplentes):

    for i in range(len(alineacion)):
      for j in range(len(alineacion[i])):
        pos = alineacion[i][j]
        if(isinstance(pos, str)):
          suplentes_copy = queue.Queue()
          suplentes_copy = suplentes
          while(not suplentes_copy.empty()):
            suplente = suplentes_copy.get()
            if(suplente.linea_jugador == i):
              alineacion[i][j] = suplente
              break
            else:
              pass
        else:
          pass

    return alineacion

  @staticmethod
  def get_formacion_definitiva(alineacion, formacion, suplentes):
    alineacion_aux = alineacion[:][:]

    while(not suplentes.empty()):
      
      alineacion_aux2 = alineacion_aux[:][:]

      jugador = suplentes.get()      
      linea_aux = alineacion_aux[jugador.linea_jugador]   

      min = linea_aux[0].media
      min_jugador = 0

      for i in range(len(linea_aux)):
        aux_min = linea_aux[i].media

        if(aux_min <= min):
          min = aux_min
          min_jugador = i

      linea_aux[min_jugador] = jugador

      alineacion_aux[jugador.linea_jugador] = linea_aux

      alineacion_aux = Generador.compare_alineacion(alineacion_aux, alineacion_aux2, formacion)

    return alineacion_aux  




  @staticmethod
  def compare_alineacion(al1, al2, formacion):
    puntaje1 = Generador.get_puntaje_alineacion(al1, formacion)
    puntaje2 = Generador.get_puntaje_alineacion(al2, formacion)

    if(puntaje2 > puntaje1):
      return al2
    else:
      return al1


  @staticmethod
  def get_puntaje_alineacion(al, formacion):

    matriz_formacion = formacion.matriz_falsa

    lista_puntajes = []
    for i in range(len(al)):
      for j in range(len(al[i])):
        
        posicion = matriz_formacion[i][j]
        jugador = al[i][j]
        #Congruencia        
        val_ten = int(jugador.media) % 10
        val_ten = (int(jugador.media) - val_ten)/10


        val_ten = Generador.potenciar_jugador(posicion, jugador, val_ten, formacion)

        lista_puntajes.append(90 + val_ten)
       
    puntaje_aux = sum(lista_puntajes) % 100

    if(puntaje_aux == 0):
      return 100
    else:
      return puntaje_aux





  @staticmethod
  def get_mejor_alineacion(formacion, jugadores_originales):

    formacion_aux = formacion.matriz_falsa    
    #Copia de la cola original
    jugadores = queue.Queue()
    #Cola con los jugadores que sobran
    jugadores_aux = queue.Queue()


    jugadores = jugadores_originales
              
    while(not jugadores.empty()):
      #var
      jugador = jugadores.get()      
      formacion_aux = formacion_aux[:][:]
      linea_aux = formacion_aux[jugador.linea_jugador]    

      for i in range(len(linea_aux)):
        pos = linea_aux[i]
        if(isinstance(pos, str)):
          if(jugador.posicion == pos):
            formacion_aux[jugador.linea_jugador][i] = jugador
            break
          elif(i == len(linea_aux) - 1):
            jugadores_aux.put(jugador)
        else:
          continue
      

    formacion_aux = Generador.check_alineacion(formacion_aux, jugadores_aux)

    return Generador.get_formacion_definitiva(formacion_aux, formacion, jugadores_aux)

















      










if __name__ == "__main__":
  jugadores = Archivador.read_jugadores()
  formaciones = get_formaciones()
  
  jugadores_ordenados = Generador.get_cola_ordenada(jugadores)
  
  formacion = Generador.get_mejor_formacion(formaciones, jugadores_ordenados)

  lista_formacion = Generador.get_mejor_alineacion(formacion, Generador.get_cola_ordenada(jugadores))
  
  
  for i in lista_formacion:
    for j in i:
      print(j.numero)
    print()
