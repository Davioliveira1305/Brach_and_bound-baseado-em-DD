# Gerador de instancias do problema do conjunto independente maximo.
from ortools.linear_solver import pywraplp
import random as rnd

def instanciaConjInd(nVertices, nArestas):

    A = set() # Conjunto de arestas

    while len(A) < nArestas:

        vi = rnd.randint(0, nVertices-1)
        vj = rnd.randint(0, nVertices-1)

        if vi == vj:
            continue

        if vi > vj:
            vi, vj = vj, vi
        aresta = (vi,vj)
        A.add(aresta)

    pesos = [rnd.randint(1,2*nVertices) for _ in range(nVertices)]

    return A, pesos



def resolverConjuntoIndependente(nVertices, arestas, pesos):

    TOL = 1.0e-3             # Tolerancia para o solver
    nArestas = len(arestas)  # Numero de restricoes

    # Criar do solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None

    # Criar variaveis de decisao
    x = [solver.IntVar(0, 1, f'x{j}') for j in range(nVertices)]
    print('Numero de variaveis =', solver.NumVariables())

    # Criar restricoes
    for (vi, vj) in arestas:
        solver.Add( x[vi] + x[vj] <= 1 )
    print('Numero de restricoes =', solver.NumConstraints())

    # Criar funcao objetivo e definir o sentido de otimizacao
    solver.Maximize( sum([pesos[j]*x[j] for j in range(nVertices)]) )

    # Resolver o problema
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Valor da funcao objetivo =', solver.Objective().Value())
        print(f'Tempo de solucao: {(solver.wall_time()/1000):.4} (s)')
        print('Variaveis iguais a 1:')
        for j in range(nVertices):
            if x[j].solution_value() > 1-TOL:
                print(f' x{j}', end='')
        print('')

        return (solver.Objective().Value(), solver.wall_time()/1000)
    else:
        print('O problema nao possui solucao.')


def gerarArquivos(sequencial, n, m, semente):

    nVertices = n
    nArestas = m

    rnd.seed(semente)

    A, pesos = instanciaConjInd(nVertices, nArestas)

    arqSaida = open(f'instancias\instancia{sequencial}.txt', 'w+')

    arqSaida.write(f'{nVertices}\n')
    arqSaida.write(f'{nArestas}\n')

    for wj in pesos:
        arqSaida.write(f'{wj} ')
    arqSaida.write('\n')

    for (vi, vj) in A:
        arqSaida.write(f'{vi} {vj}\n')

    arqSaida.close()

    (z, tempo) = resolverConjuntoIndependente(nVertices, A, pesos)

    resultados = open(f'resultados.csv', 'a')
    resultados.write(f'instancia{sequencial}, {z}, {tempo:.4}\n')
    resultados.close()


if __name__ == '__main__':

    nInstancias = 31
    rnd.seed(190)
    semente = [rnd.randint(1,100000) for _ in range(nInstancias)]

    dimensao = [
        [5, 6],
        [8, 15],
        [8, 20],
        [10, 30],
        [10, 40],
        [15, 40],
        [15, 50],
        [15, 60],
        [20, 50],
        [20, 70],
        [20, 90],
        [25, 80],
        [25, 100],
        [25, 150],
        [30, 100],
        [30, 200],
        [30, 300],
        [35, 100],
        [35, 200],
        [35, 300],
        [40, 200],
        [40, 300],
        [40, 500],
        [50, 200],
        [50, 300],
        [50, 500],
        [70, 500],
        [70, 800],
        [70, 1000],
        [100, 2000],
        [150, 3000]]

    nInstancias = len(dimensao)

    for i in range(nInstancias):
        gerarArquivos(i, dimensao[i][0], dimensao[i][1], semente[i])
