
# Define a estrutura de um nó DD
class Node:
  def __init__(self, estado, valor, solucao, primeira_variavel):
    self.estado = estado
    self.valor = valor
    self.solucao = solucao
    self.primeira_variavel = primeira_variavel

  def __repr__(self):
    return f'Estado = {self.estado}, Valor: {self.valor}, Solução = {self.solucao}, Primeira Variável = {self.primeira_variavel}'
  
# Função de transição
def tj(no, var, d, dados):
  pesos, vizinhanca = dados[1], dados[2]
  # Pega o vetor solução do pai
  vetor_solucao = no.solucao.copy()
  # Adiciona o domínio no vetor solução
  vetor_solucao[var] = d
  # Calcula a função objetivo daquele nó
  fo = 0
  for i in range(len(pesos)):
    fo += pesos[i]*vetor_solucao[i]

  # Domínio = 1(Se for viável, o vértice e sua vizinhança seram retirados do estado de referência)
  if d == 1:
    if var in no.estado:
      estado = no.estado.copy() - set(vizinhanca[var])
      estado = estado - {var}
      return estado, fo, vetor_solucao
    else:
      return None, None, None

  # Domínio = 0(Apenas o vértice será retirado do estado de referência)
  else:
    estado = no.estado.copy() - {var}
    return estado, fo, vetor_solucao