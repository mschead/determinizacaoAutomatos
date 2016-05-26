import json

fechoGlobal = {}
deterministico = False


def algoritmoSemEpsilon(estados):
	#obtem os estados novos e suas respectivas transicoes
	
	lista = estados.values()

	while len(lista) != 0: 
		transicoes = lista.pop(0)
		for simbolo, estadoDestino in transicoes.items():
			estadoNovo = transformToString(estadoDestino)
			if (not estadoNovo in estados) and (not estadoNovo == ""):
				estados[estadoNovo] = obterHashFinal(estadoDestino, estados)
				lista.append(obterHashFinal(estadoDestino, estados))

	return estados


def algoritmoComEpsilon(estados):
	estadoInicial = fechoGlobal["q1"]
	hashFinal = {}
	hashFinal[transformToString(estadoInicial)] = obterHashFinal(estadoInicial, estados)


	lista = hashFinal.values()

	while len(lista) != 0: 
		transicoes = lista.pop(0)
		for simbolo, estadoDestino in transicoes.items():
			estadoNovo = transformToString(estadoDestino)
			if (not estadoNovo in hashFinal) and (not estadoNovo == ""):
				hashFinal[estadoNovo] = obterHashFinal(estadoDestino, estados)
				lista.append(obterHashFinal(estadoDestino, estados))

	return hashFinal



def transformToString(listaEstados):
	string = ""
	
	for estado in listaEstados:
		string += estado

	return string


def obterHashFinal(estadoDestino, estados):
	hashFinal = {}
	transicoes = []
	alfabeto = ["a", "b"]

	for estado in estadoDestino:
		transicoes.append(estados[estado])

	estadosResultantes = []
	for letra in alfabeto:
		for transicao in transicoes:
			if not transicao[letra] == []:
				if deterministico == False:
					estadosResultantes += obterFechoResultanteEstados(transicao[letra])
				else:
					estadosResultantes += transicao[letra]

		hashFinal[letra] = list(set(estadosResultantes))
		estadosResultantes = []

	return hashFinal


def obterFechoResultanteEstados(estado):
	fecho = []
	for e in estado:
		fecho += fechoGlobal[e]

	return list(set(fecho))


def obterFechoEstado(estado, estados):
	transicao = estados[estado] #hash
	fecho = []
	fecho.append(estado)

	index = 0
	while index < len(fecho):
		estadoCorrente = fecho[index]
		fechoEstadoCorrente = estados[estadoCorrente]["e"]

		for estadoFechoCorrente in fechoEstadoCorrente:
			if not estadoFechoCorrente in fecho:
				fecho.append(estadoFechoCorrente)

		index = index + 1

	return fecho


def rotinaPrincipal():

	global deterministico
	global fechoGlobal

	#obtem os estados e transicoes da maquina descritos em formato JSON
	with open("afnd.json") as json_file:
		estados = json.load(json_file)

	#verifica se eh deterministico
	deterministico = estados['deterministico']
	del estados['deterministico']

	#obtem os fechos, caso possua transicoes epsilon
	if deterministico == False:
		for estado, transicao in estados.items():
			fechoGlobal[estado] = obterFechoEstado(estado, estados)

	if deterministico:
		estados = algoritmoSemEpsilon(estados)
	else:
		estados = algoritmoComEpsilon(estados)

	#salva a maquina resultante em formato JSON
	with open('resultado.json', 'w') as output:
		json.dump(estados, output, indent=1)


rotinaPrincipal()







