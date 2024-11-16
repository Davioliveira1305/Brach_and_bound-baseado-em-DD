from estrutura import Node
from estrutura import tj
from ordenacao import min_state
from ordenacao import cds
from mesclagens import mesclagem
import random

def dd_relaxado(no_inicial, dados, w, metodo, metodo_order):
  # Lista pra guardar o cutset exato
  cut_set_exato = []
  # Flag para indicar se o nó foi resolvido de maneira exata
  se_dd_exato = True
  # Camada de inicialização
  camada_atual = [no_inicial]
  # Domínio das variáveis
  dominio = [0, 1]
  ordenacao = no_inicial.ordenacao.copy()
  var = ordenacao[0]
  while len(ordenacao) != 0:
    ordenacao.remove(var)
    # Lista para guardar os nós da camada atual
    proxima_camada = []
    # Percorre os nós da camada atual
    for no in camada_atual:
      # Percorre o domínio das variáveis de decisão
      for d in dominio:
        # Estado, valor e vetor solução do novo nó
        estado, valor, solucao = tj(no, var, d, dados)
        # Se o estado for inviável, passa para a próxima iteração
        if estado is None:
          continue
        node = Node(estado, valor, solucao, ordenacao.copy())
        # Flag para indicar se foi achado nós com mesmos estados na camada atual
        achou = False
        # Verifica se tem nós na camada atual com estados iguais
        for comp in proxima_camada:
          if node.estado == comp.estado:
            achou = True
            if comp.valor < node.valor:
              comp.valor = node.valor
              comp.solucao = node.solucao.copy()
            else:
              node.valor = comp.valor
              node.solucao = comp.solucao
        # Se não achou, adiciona o nó na camada atual
        if not achou:
          proxima_camada.append(node)
    se_dd_exato_ant = se_dd_exato
    # Restrição do tamanho das camadas
    if len(proxima_camada) > w:
      # O nó deixará de ser resolvido de maneira exata
      se_dd_exato = False
      # Heurística de meslagem
      proxima_camada = mesclagem(proxima_camada, w, metodo)
    # Identificação do cut-set-exato
    if(se_dd_exato_ant == True) and (se_dd_exato == False):
      cut_set_exato = camada_atual
    camada_atual = proxima_camada

    # Escolhe a próxima variável de acordo com a ordenação
    if metodo_order == 1:
      if len(ordenacao) != 0:
        var = ordenacao[0]
    elif metodo_order == 2:
      if len(ordenacao) != 0:
        var = min_state(proxima_camada)
    elif metodo_order == 3:
      if len(ordenacao) != 0:
        var = cds(proxima_camada, dados)
  else: return camada_atual, cut_set_exato, se_dd_exato
