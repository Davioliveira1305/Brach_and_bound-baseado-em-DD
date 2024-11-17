from leitura import leitura
from estrutura import Node
from relaxado import dd_relaxado
from restrito import dd_restrito
import pandas as pd
import time

"""
      PARÂMETROS
path: caminho da instância
w_relax: tamanho máximo de camada no dd - relaxado
w_restrito: tamanho máximo de camada no dd - restrito
metodo_relax: método utilizado para a mesclagem dos nós(1 - Menor FO, 2 - Maior Estado, 3 - Aleatório)
metodo_restrito: método utilizado para ordenar os nós(1 - Maior FO, 2 - Menor FO, 3 - Ordenação normal, 4 - Ordenação por borda)
metodo_order: método utilizado para a ordenação de variáveis(1 - Ordenação normal, 2 - Min State, 3 - CDS)
"""

def branch_and_bound_dd(instancia, w_relax, w_restrito, metodo_relax, metodo_restrito, metodo_order):
  # Leitura dos dados da instância
  dados = leitura(instancia)
  # Nó inicial da árvore de branch and bound
  no_inicial = Node(set(dados[0]), 0, [0 for _ in range(len(dados[0]))], [i for i in range(0, len(dados[0]))])
  # Lista que guarda os nós que ainda não foram explorados
  abertos = [no_inicial]
  # Variável para guardar o número de nós percorridos na árvore de brach-and-bound
  num_nos = 0
  # Variável que vai guardar a melhor solução encontrada
  melhor_sol =  no_inicial
  while len(abertos) != 0:
    # Pega o primeiro nó da fila
    no = abertos[0]
    abertos.remove(no)
    num_nos += 1
    # Retorno do DD - Relaxado
    sol_relax, cut_set_exato, se_dd_exato = dd_relaxado(no, dados, w_relax, metodo_relax, metodo_order)
    # Se não teve nós corrompidos, a solução relaxada encontrada é viável
    if se_dd_exato == True:
      if sol_relax[0].valor > melhor_sol.valor:
        melhor_sol = sol_relax[0]
      continue
    # Se a solucão do relaxado for menor do que a melhor solução já encontrada, o nó é descartado
    if (sol_relax[0].valor < melhor_sol.valor): continue
    # Adiciona os nós do cut-set-exato aos nós que ainda devem ser explorados
    else:
      abertos += cut_set_exato
    # Retorno do DD - Restrito
    sol_restrita = dd_restrito(no, dados, w_restrito, metodo_restrito, metodo_order)
    # Melhor solução até o momento
    if sol_restrita[0].valor > melhor_sol.valor:
      melhor_sol = sol_restrita[0]
  return melhor_sol, num_nos

path = 'C:\\Users\\Davi\\Documents\\brach_and_bound\\instancias\\instancia29.txt'
w_relax = 100
w_restrito = 100
metodo_relax = 4
metodo_restrito = 1
metodo_order = 2
tempo_inicial = time.time()
sol, num_nos = branch_and_bound_dd(path, w_relax, w_restrito, metodo_relax, metodo_restrito, metodo_order)
tempo_final = time.time()
print(f"Tempo total = {tempo_final - tempo_inicial}s")
print(sol)
print(f'Foram percorridos {num_nos} nós')