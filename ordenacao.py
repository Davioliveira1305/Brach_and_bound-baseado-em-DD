# Escolhe o vértice que participa do menor número de estados na camada 
from collections import defaultdict
def min_state(camada):
  lista_estados = []
  for no in camada:
    lista_estados.append(list(no.estado))
  # Dicionário para contar a ocorrência de cada vertice nos estados
  contagem = defaultdict(int)

  # Contar em quantas sublistas cada vertice aparece
  for sublista in lista_estados:
      # Usamos o set para evitar contagens duplicadas na mesma sublista
      for numero in set(sublista):
          contagem[numero] += 1

  # Encontrar o número com a menor contagem de ocorrências nas sublistas
  if len(contagem) != 0:
    min_vertice = min(contagem, key=contagem.get)
  else:
    min_vertice = camada[0].ordenacao[0]
  return min_vertice

import itertools
def cds(camada, dados):
  lista_estados = []
  for no in camada:
    lista_estados.append(list(no.estado))
  contagem = defaultdict(int)
  for sublista in lista_estados:
    pares = list(itertools.combinations(sublista, 2))
    for v_1, v_2 in pares:
      vizinhanca_v1 = dados[2][v_1]
      if v_2 in vizinhanca_v1:
        contagem[v_1] += 1
        contagem[v_2] += 1
  # Encontrar o número com a menor contagem de ocorrências nas sublistas
  if len(contagem) != 0:
    min_vertice = min(contagem, key=contagem.get)
  else:
    min_vertice = camada[0].ordenacao[0]
  return min_vertice