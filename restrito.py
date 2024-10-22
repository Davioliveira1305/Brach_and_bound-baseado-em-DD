from estrutura import Node
from estrutura import tj

def dd_restrito(no_inicial, dados, w, metodo):
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
        estado, valor, solucao = tj(no, var, d, dados)
        # Estado inviável
        if estado is None:
          continue
        node = Node(estado, valor, solucao, var + 1)
        # Flag
        achou = False
        # Verifica se tem algum nó com estado igual na camada atual
        for comp in proxima_camada:
          if node.estado == comp.estado:
            achou = True
            if comp.valor < node.valor:
              comp.valor = node.valor
              comp.solucao = node.solucao.copy()
            else:
              node.valor = comp.valor
              node.solucao = comp.solucao
        # Se não achou adiciona na camada atual
        if not achou:
          proxima_camada.append(node)
        # Restrição do tamanho das camadas
    if len(proxima_camada) > w:
      # Ordena a camada atual em ordem decrescente por valor de função objetivo dos nós
      if metodo == 1:
        proxima_camada = sorted(proxima_camada, key=lambda x: x.valor, reverse=True)
      # Ordena a camada atual em ordem crescente por valor de função objetivo dos nós
      elif metodo == 2:
        proxima_camada = sorted(proxima_camada, key=lambda x: x.valor, reverse=False)
      # Ordenação normal
      elif metodo == 3:
        proxima_camada = proxima_camada
    camada_atual = proxima_camada[:w]
  return camada_atual