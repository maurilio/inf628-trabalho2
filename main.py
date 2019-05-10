############################################################ BIBLIOTECAS
import os
import gym
import random
import copy
import matplotlib
import matplotlib.pyplot as plt



###################################################### VARIÁVEIS GLOBAIS
NUM_GERACOES = 50
NUM_ENTES = 500
MAX_NUM_GENES = 35
MIN_NUM_GENES = 15
NUM_PASSOS = 300
NUM_CAMPEOES = 10
NUM_FILHOS = 10
PROB_MUTACAO = 60

populacao = []
serieAptxGer = []

max_aptidao = 0

matplotlib.use('Agg')
env = gym.make('BipedalWalker-v2')


################################################################ FUNÇÕES
def random_action():
	return round(random.uniform(-1, 1), 2)

def cria_populacao(n):
	for _ in range(n):
		populacao.append(Ente())

def converte_gene_in_action(gene):
	return [gene.a, gene.t, gene.g, gene.c]	

def faz_cruzamento(ente1, ente2):
	novoEnte = ente1.copy()
	novoEnte.dna.genes = []

	novo_comprimento = round(random.uniform(MIN_NUM_GENES, MAX_NUM_GENES))
	
	crossoverPoint = round(random.uniform(0, 1) * novo_comprimento)
	
	for i in range(novo_comprimento):
		if i < crossoverPoint and i < len(ente1.dna.genes) and i < len(ente2.dna.genes):
			novoEnte.dna.genes.append(copy.deepcopy(ente1.dna.genes[i]))
		elif i >= crossoverPoint and i < len(ente1.dna.genes) and i < len(ente2.dna.genes):
			novoEnte.dna.genes.append(copy.deepcopy(ente2.dna.genes[i]))
		elif i < len(ente1.dna.genes):
			novoEnte.dna.genes.append(copy.deepcopy(ente1.dna.genes[i]))
		elif i < len(ente2.dna.genes):
			novoEnte.dna.genes.append(copy.deepcopy(ente2.dna.genes[i]))
		else:	
			novoEnte.dna.genes.append(Gene(random_action(), random_action(), random_action(), random_action()))

		if random.uniform(0, 100) < PROB_MUTACAO:
			novoEnte.dna.genes[i] = Gene(random_action(), random_action(), random_action(), random_action())

		novoEnte.fit = 0

	return novoEnte

def selecao(populacao):
	somaTotal = 0
	delta = abs(populacao[NUM_CAMPEOES-1].fit)
	
	for ente in populacao[:NUM_CAMPEOES]:
		somaTotal += ente.fit + delta

	candidato = random.uniform(0, somaTotal)

	somaTotal = 0
	for ente in populacao[:NUM_CAMPEOES]:
		somaTotal += ente.fit + delta
		if somaTotal >= candidato:
			return ente


################################################## DEFINIÇÕES DE CLASSES
class Gene:
	def __init__(self, a = None, t = None, g = None, c = None, f = None):
		if a is None:
			self.setA(random_action())
			self.setT(random_action())
			self.setG(random_action())
			self.setC(random_action())
			self.setFenotipo(0)
		else:
			self.setA(a)
			self.setT(t)
			self.setG(g)
			self.setC(c)
			self.setFenotipo(f)

	def setA(self, a):
		self.a = a
	def setT(self, t):
		self.t = t
	def setG(self, g):
		self.g = g
	def setC(self, c):
		self.c = c
	def setFenotipo(self, f):
		self.f = f;
	def copy(self):
		return Gene(self.a, self.t, self.g, self.c, self.f)

class DNA:
	num_genes = round(random.uniform(MIN_NUM_GENES, MAX_NUM_GENES))

	def __init__(self, genes = None):
		if genes is None:
			self.genes = []
			for _ in range(self.num_genes):
				self.addGene(Gene())
		else:
			self.genes = genes
		
	def addGene(self, gene):
		self.genes.append(gene)

	def copy(self):
		aux = []
		for gene in self.genes:
			aux.append(gene.copy())
		return DNA(aux)

class Ente:

	def __init__(self, dna = None, fit = None):
		if dna is None:
			self.setDNA(DNA())
			self.fit = 0
		else:
			self.setDNA(dna)
			self.fit = fit

	def setDNA(self, dna):
		self.dna = dna

	def setFitness(self, fit):
		self.fit = fit

	def copy(self):
		return Ente(self.dna.copy(), self.fit.copy())
		

######################################################### LAÇO PRINCIPAL


#inicio as variáveis
cria_populacao(NUM_ENTES)

superCampeao = None

#calcula a aptidão de cada ente
for g in range(NUM_GERACOES):

	i = 0
	for ente in populacao:

		i+=1

		env.reset()

		totalReward = 0
		for passo in range(NUM_PASSOS):
			#env.render()
			gene = ente.dna.genes[passo % len(ente.dna.genes)]
			action = converte_gene_in_action(gene)	
			observation, reward, done, info = env.step(action)
			totalReward += reward
			if done:
				break
		ente.setFitness(totalReward)

		#imprime os resultados parciais
		os.system('clear')
		print("%11s %11s %20s %16s" % ('| GERAÇÃO |', 'INDIVÍDUO |', 'APTIDÃO INDIVIDUAL |', 'MELHOR APTIDÃO |'))
		print("| %3d/%3d | %4d/%4d | %18f | %14f |" % ((g+1), NUM_GERACOES, i, NUM_ENTES, totalReward, max_aptidao))


	#escolho os N mais aptos
	#ordena entes por maior apitidã(o
	populacao.sort(key=lambda e: e.fit, reverse=True)

	if superCampeao == None:
		superCampeao = populacao[0].copy()
	elif superCampeao.fit < populacao[0].fit:
		superCampeao = populacao[0].copy()

	#adiciona um valor à série Aptidão x Geração para gerar o gráfico no final
	max_aptidao = superCampeao.fit
	serieAptxGer.append(max_aptidao)

	#nova geracao
	nova_geracao = []

	#seleciona os candidatos a transmitir seus genes
	for _ in range(NUM_FILHOS):
		candidato1 = selecao(populacao)
		candidato2 = selecao(populacao)

		filho = faz_cruzamento(candidato1, candidato2)

		nova_geracao.append(filho)


	#elimina os mais fracos, abrindo espaço para os novos entes
	del populacao[-len(nova_geracao):]
	populacao.extend(nova_geracao)

	
#repita o processo por N gerações


#imprime o gráfico de evolução
plt.plot(serieAptxGer)
plt.ylabel('Aptidão')
plt.xlabel('Geração')
plt.savefig('aptxger')

#exibe o comportamento do ganhador
populacao.sort(key=lambda e: e.fit, reverse=True)
key = None 
env.reset()
ente = superCampeao
passo = 0
key = input("\n\nPREPARADO PARA VER O GANHADOR? [S/N] \n\n USE CTRL+C PARA CANCELAR")
while key != 'N':		
	gene = ente.dna.genes[passo % len(ente.dna.genes)]
	env.render()
	action = converte_gene_in_action(gene)	
	observation, reward, done, info = env.step(action)
	passo += 1

env.close()

