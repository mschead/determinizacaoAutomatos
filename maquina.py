import json

class Maquina:

	def __init__(self):	
		self.preparar_maquina()

	def automato_sem_epsilon(self):
		lista = self.automato.values()

		while len(lista) != 0: 
			transicoes = lista.pop(0)
			for simbolo, estado_destino in transicoes.items():
				estado_novo = self.to_string(estado_destino)
				if (not estado_novo in self.automato) and (not estado_novo == ""):
					estado_com_transicoes = self.estado_com_transicoes(estado_destino)
					self.automato[estado_novo] = estado_com_transicoes
					lista.append(estado_com_transicoes)


	def estado_com_transicoes(self, estado_destino):
		estado_com_transicoes = {}
		transicoes_estado_destino = []

		for estado in estado_destino:
			transicoes_estado_destino.append(self.automato[estado])

		estados_resultantes = []
		for letra in self.alfabeto:
			for transicao in transicoes_estado_destino:
				if not transicao[letra] == []:
					if self.usa_epsilon == True:
						estados_resultantes += self.fecho_estados(transicao[letra])
					else:
						estados_resultantes += transicao[letra]

			estado_com_transicoes[letra] = list(set(estados_resultantes))
			estados_resultantes = []

		return estado_com_transicoes



	def automato_com_epsilon(self):
		automato_novo = {}
		automato_novo[self.to_string(self.estado_inicial)] = self.estado_com_transicoes(self.estado_inicial)

		lista = automato_novo.values()

		while len(lista) != 0: 
			transicoes = lista.pop(0)
			for simbolo, estado_destino in transicoes.items():
				estado_novo = self.to_string(estado_destino)
				if (not estado_novo in automato_novo) and (not estado_novo == ""):
					estado_com_transicoes = self.estado_com_transicoes(estado_destino)
					automato_novo[estado_novo] = estado_com_transicoes
					lista.append(estado_com_transicoes)

		self.automato = automato_novo


	#obtem o fecho de um conjunto de estados
	def fecho_estados(self, estado):
		fecho = []
		for e in estado:
			fecho += self.fecho_global[e]

		return list(set(fecho))


	#obtem o fecho de um estado especifico
	def fecho_estado(self, estado):
		transicao = self.automato[estado]
		fecho = []
		fecho.append(estado)

		index = 0
		while index < len(fecho):
			estado_corrente = fecho[index]
			fecho_estado_corrente = self.automato[estado_corrente]["e"]

			for estado_fecho_corrente in fecho_estado_corrente:
				if not estado_fecho_corrente in fecho:
					fecho.append(estado_fecho_corrente)

			index = index + 1

		return fecho



	#METODOS AUXILIARES PARA PREPARAR E GERAR O AUTOMATO


	#Abre o arquivo JSON com a maquina e guarda atributos importantes para determinizar
	def preparar_maquina(self):

		with open("afnd.json") as json_file:
			self.automato = json.load(json_file)

		self.usa_epsilon = self.automato['usa_epsilon']
		del self.automato['usa_epsilon']

		self.alfabeto = self.automato['alfabeto']
		del self.automato['alfabeto']

		self.estado_inicial = self.automato['estado_inicial']
		del self.automato['estado_inicial']

		self.estados_finais = self.automato['estados_finais']
		del self.automato['estados_finais']

		if self.usa_epsilon == True:
			self.fecho_global = {}
			for estado, transicao in self.automato.items():
				self.fecho_global[estado] = self.fecho_estado(estado)
			self.estado_inicial = self.fecho_global[self.estado_inicial]


	#Salva num arquivo JSON a maquina com os estados e suas transicoes finais
	def gerar_arquivo_maquina(self):
		with open('resultado.json', 'w') as output:
			json.dump(self.automato, output, indent=1)


	#Obter o estado em formato de string, usado como chave no JSON
	def to_string(self, listaEstados):
		string = ""
	
		for estado in listaEstados:
			string += estado

		return string
