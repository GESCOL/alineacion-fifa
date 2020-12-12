
class Formacion():

  posiciones = {'POR': 1, 'LI': 3, 'LD': 5, 'CAD' : 7,
                'CAI' : 11, 'DFC' : 13, 'MCD' : 17,
                'MC' : 19, 'MCO' : 23, 'ED' : 29, 
                'EI' : 31, 'MP' : 37, 'SDD' : 41,
                'SDI' : 43, 'DC' : 47, 'MD' : 53,
                'MI' : 59}  

  def __init__(self, numero, matrix_falsa, matriz, valor_equilibrio):    
    self.numero = numero
    self.matriz_falsa = matrix_falsa[:][:]
    self.matriz = Formacion.generar_matriz(matriz)
    self.valor_equilibrio = valor_equilibrio        

  def get_codigo(self):    

    codigo = 1

    if(self.valor_equilibrio == -1):

      for i in self.matriz[1]:
        codigo *= i

    elif(self.valor_equilibrio == 0):
      for i in self.matriz[2]:
        codigo *= i
    else:
      for i in self.matriz[3]:
        codigo *= i

    return codigo


  @staticmethod
  def generar_matriz(matrix_falsa):
    matrix_falsa2 = matrix_falsa[:][:]
    for i in range(len(matrix_falsa2)):      
      for j in range(len(matrix_falsa2[i])):
        matrix_falsa[i][j] = Formacion.posiciones.get(matrix_falsa2[i][j])
    
    return matrix_falsa2

def get_formaciones():
    mis_formaciones = []

    mis_formaciones.append(Formacion(1,[["POR"],["DFC","DFC","DFC"],["MD","MC","MC","MI"],["ED","DC","EI"]], [["POR"],["DFC","DFC","DFC"],["MD","MC","MC","MI"],["ED","DC","EI"]],1))
    mis_formaciones.append(Formacion(2,[["POR"],["DFC","DFC","DFC"],["MD","MCD","MCO","MCD","MI"],["DC","DC"]], [["POR"],["DFC","DFC","DFC"],["MD","MCD","MCO","MCD","MI"],["DC","DC"]],0))
    mis_formaciones.append(Formacion(3,[["POR"],["LD","DFC","DFC","LI"],["MC","MC"],["ED","DC","DC","EI"]], [["POR"],["LD","DFC","DFC","LI"],["MC","MC"],["ED","DC","DC","EI"]],1))
    mis_formaciones.append(Formacion(4,[["POR"],["LD","DFC","DFC","LI"],["MD","MC","MI"],["ED","DC","EI"]], [["POR"],["LD","DFC","DFC","LI"],["MD","MC","MI"],["ED","DC","EI"]],-1))

    return mis_formaciones
