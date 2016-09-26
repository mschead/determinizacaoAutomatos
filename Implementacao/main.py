from maquina import Maquina
import sys

if len(sys.argv) == 2:
	maquina = Maquina(sys.argv[1])
	print "Determinizando ..."
	maquina.gerar_automato()
	print "Determinizado com sucesso"
else:
	print "Formato invalido!\nDigite dessa forma: python main.py <nome_arquivo_automato.json>"

