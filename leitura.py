def leitura(path):
  with open(path, 'r') as f:
    for idx,linha in enumerate(f):
      elementos = linha.split()
      if idx == 0:
        # Cria os vértices do grafo
        vertices = [i for i in range(int(linha))]
        # dicionário para armazenar os pesos dos vértices
        pesos = dict.fromkeys(vertices, 0)
        # vizinhança de cada vértice
        vizinhanca = {vertice: [] for vertice in vertices}

      # Adciona o peso referente a cada vértice
      if idx == 2:
        for ind, peso in enumerate(elementos):
          pesos[ind] = int(peso)

      # Define a vizinhança de cada vértice
      if idx > 2:
        chave_1 = int(elementos[0])
        chave_2 = int(elementos[1])
        vizinhanca[chave_1].append(chave_2)
        vizinhanca[chave_2].append(chave_1)

  return (vertices, pesos, vizinhanca)