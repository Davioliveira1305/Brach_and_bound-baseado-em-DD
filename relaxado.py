from estrutura import Node
from estrutura import tj
import random
def dd_relaxado(no_inicial, dados, w, metodo):
  # Lista pra guardar o cutset exato
  cut_set_exato = []
  # Flag para indicar se o nó foi resolvido de maneira exata
  se_dd_exato = True
  # Camada de inicialização
  camada_atual = [no_inicial]
  # Domínio das variáveis
  dominio = [0, 1]
  for var in range(no_inicial.primeira_variavel, len(dados[0])):
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
        node = Node(estado, valor, solucao, var + 1)
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
    # lista sentinela(para não modificar a lista de nós atuais)
    lista_sentinela = proxima_camada.copy()
    # Restrição do tamanho das camadas
    if len(proxima_camada) > w:
      # O nó deixará de ser resolvido de maneira exata
      se_dd_exato = False
      if metodo == 1:
        # Ordenando a camada de referência em ordem crescente pelo valor de função objetivo
        lista_sentinela = sorted(lista_sentinela, key=lambda x: x.valor, reverse=False)
      elif metodo == 2:
        # Ordenando a camada de referência em ordem decrescente pelo tamanho de estado
        lista_sentinela = sorted(lista_sentinela, key=lambda x: len(x.estado), reverse=True)
      elif metodo == 3:
        # Ordenando a camada de referência aleatoriamente
        random.shuffle(lista_sentinela)
      # Número de nós selecionados para a mesclagem
      num_nodes_merge = len(proxima_camada) - w + 1
      selecao = []
      for node in lista_sentinela:
        selecao.append(node)
        # remove os nós escolhidos para a mesclagem na camada de referência
        proxima_camada.remove(node)
        if len(selecao) == num_nodes_merge: break
      # Lista para guardar os estados dos nós que serão unidos
      lista_estados = []
      # Lista para guardar os valores de fo dos nós que serão unidos
      lista_valores = []
      melhor_no = selecao[0]
      # Escolher o nó que possui o maior valor de função objetivo
      for node_select in selecao:
        lista_estados.append(node_select.estado)
        lista_valores = [node_select.valor]
        if node.valor > melhor_no.valor: melhor_no = node
      # União de todos os estados
      estado = set().union(*lista_estados)
      # Maior valor de FO dentre os nós escolhidos para a mesclagem
      valor = max(lista_valores)
      solucao = melhor_no.solucao
      primeira_variavel = melhor_no.primeira_variavel
      # Adiciona o nó mesclado na proxima camada
      merge = Node(estado, valor, solucao, primeira_variavel)
      proxima_camada.append(merge)
    # Identificação do cut-set-exato
    if(se_dd_exato_ant == True) and (se_dd_exato == False): 
      cut_set_exato = camada_atual
    camada_atual = proxima_camada
  if len(cut_set_exato) != 0: return camada_atual, cut_set_exato, se_dd_exato
  else: return camada_atual, [], se_dd_exato
