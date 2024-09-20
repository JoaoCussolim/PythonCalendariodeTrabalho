funcionarios = ['João', 'Pedro', 'Rafael', 'Ana Julia', 'Ana Anaconda', 'Biel Anaconda', 'Andando Anacando', 'Ana Ana']
calendario = [0] * 20

def trim(string : str):
    vetorSemEspacos = string.split(' ')
    stringSemEspacos = ''
    for i in range(len(vetorSemEspacos)):
        stringSemEspacos += vetorSemEspacos[i]
    return stringSemEspacos

def ordenarEmOrdemAlfabetica(vetor : list):
    tamanhoDoVetor = len(vetor)
    vetorOrdenado = vetor
    for i in range(tamanhoDoVetor):
        for j in range(tamanhoDoVetor):
            ind = 0
            if(i != j):
                while(vetorOrdenado[i][ind:ind+1] == vetorOrdenado[j][ind:ind+1]):
                    ind += 1
                if(vetorOrdenado[i][ind:ind+1] < vetorOrdenado[j][ind:ind+1]):
                    aux = vetorOrdenado[j]
                    vetorOrdenado[j] = vetorOrdenado[i]
                    vetorOrdenado[i] = aux        
    return vetorOrdenado


def preencherCalendario(vetor : list):
    indiceUsuario = 0
    funcionariosOrdenados = ordenarEmOrdemAlfabetica(vetor)
    for i in range(len(calendario)):
        calendario[i] = funcionariosOrdenados[indiceUsuario]
        indiceUsuario += 1
        if(indiceUsuario > (len(funcionariosOrdenados) - 1)):
            indiceUsuario = 0
    print(calendario)

def adicionarFuncionario(vetor : list, nomeFunc : str):
    vetorAntigo = vetor
    tamanhoVetor = len(vetorAntigo)
    tamanhoNovoVetor = tamanhoVetor + 1
    novoVetor = [0] * tamanhoNovoVetor
    if not(vetorAntigo.__contains__(nomeFunc)):
        for i in range(tamanhoVetor):
            novoVetor[i] = vetorAntigo[i]
        novoVetor[tamanhoNovoVetor-1] = nomeFunc
        preencherCalendario(novoVetor)
    else:
        print("Já está adicionado")

def retirarFuncionario(vetor : list, nomeFunc : str):
    vetorAntigo = vetor
    tamanhoVetor = len(vetorAntigo)
    tamanhoNovoVetor = tamanhoVetor - 1
    novoVetor = [0] * tamanhoNovoVetor
    if(vetorAntigo.__contains__(nomeFunc)):
        indiceAntigo = 0
        for i in range(tamanhoVetor):
            if(vetorAntigo[i] == nomeFunc):
                pass
            else:
                novoVetor[indiceAntigo] = vetorAntigo[i]
                indiceAntigo += 1
        preencherCalendario(novoVetor)
    else:
        print("Tem esse nao")

def append(vetor : list, oqvcquercolocarnovetor):
    tamanhoDoVetor = len(vetor) - 1
    novoVetor = [0] * tamanhoDoVetor + 1
    for i in range(tamanhoDoVetor):
        novoVetor[i] = vetor[i]
    vetor[tamanhoDoVetor] = oqvcquercolocarnovetor


adicionarFuncionario(funcionarios, 'Rafael Brasil Ulbrich')