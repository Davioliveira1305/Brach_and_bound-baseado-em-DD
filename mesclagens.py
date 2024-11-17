from estrutura import Node
import random

def mesclagem(camada, w, metodo):
  if metodo != 4:
    if metodo == 1:
      # Ordenando a camada de referência em ordem crescente pelo valor de função objetivo
      camada = sorted(camada, key=lambda x: x.valor)
    elif metodo == 2:
      # Ordenando a camada de referência em ordem decrescente pelo tamanho de estado
      camada = sorted(camada, key=lambda x: len(x.estado), reverse=True)
    elif metodo == 3:
      # Ordenando a camada de referência aleatoriamente
      random.shuffle(camada)
    # Número de nós selecionados para a mesclagem
    num_nodes_merge = len(camada) - w + 1
    # Lista para guardar os estados dos nós que serão unidos
    lista_estados = []
    cont = 0
    melhor_no = camada[0]
    selecao = camada.copy()
    for node in selecao:
      cont += 1
      lista_estados.append(node.estado)
      # remove os nós escolhidos para a mesclagem na camada de referência
      camada.remove(node)
      if node.valor > melhor_no.valor: melhor_no = node
      if cont == num_nodes_merge: break
    # União de todos os estados
    estado = set().union(*lista_estados)
    # Maior valor de FO dentre os nós escolhidos para a mesclagem
    valor = melhor_no.valor
    solucao = melhor_no.solucao
    ordenacao_merge = melhor_no.ordenacao
    # Adiciona o nó mesclado na proxima camada
    merge = Node(estado, valor, solucao, ordenacao_merge)
    camada.append(merge)
    return camada
  else:
    # Ordenando em ordem decrescente
    camada = sorted(camada, key=lambda x: x.valor, reverse=True)
    # Se os nós da borda tiverem valores de FO diferentes, a função é chamada de maneira recursiva para o método 1
    if (camada[w - 2].valor != camada[w - 1].valor):
      return mesclagem(camada, w, 1)
    # Se os nós são iguais a heurística é aplicada
    else:
      iguais = [camada[w - 2], camada[w - 1]]
      diferentes = []
      i = 3
      # Guardando os nós com valores de FO iguais em uma lista(movendo-se à esquerda)
      while True:
        if camada[w - 2].valor == camada[w - i].valor: iguais.append(camada[w - i])
        else: break
        i += 1
      j = 0
      # Guardando os nós com valores de FO iguais em uma lista(movendo-se à direita)
      while True:
        if camada[w - 1].valor == camada[w + j].valor:
          iguais.append(camada[w + j])
          j += 1
        else: break
        if (len(camada) == w + j): break
      # Guardando os nós com valores de FO dieferentes em uma lista
      for k in range(w + j, len(camada)):
        diferentes.append(camada[k])
      # Removendo os nós selecionados para a mesclagem
      for no in (diferentes + iguais):
        camada.remove(no)
      # Mesclagem dos nós
      estado_1 = set().union(*[no.estado for no in iguais])
      valor_1 = iguais[0].valor
      solucao_1 = iguais[0].solucao
      ordenacao_merge_1 = iguais[0].ordenacao
      merge_1 = Node(estado_1, valor_1, solucao_1, ordenacao_merge_1)
      camada.append(merge_1)
      if len(diferentes) != 0:
        estado_2 = set().union(*[no.estado for no in diferentes])
        valor_2 = diferentes[0].valor
        solucao_2 = diferentes[0].solucao
        ordenacao_merge_2 = diferentes[0].ordenacao
        merge_2 = Node(estado_2, valor_2, solucao_2, ordenacao_merge_2)
        camada.append(merge_2)
      return camada