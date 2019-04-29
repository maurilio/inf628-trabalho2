############################################################ BIBLIOTECAS
import gym
import random
import copy

###################################################### VARIÁVEIS GLOBAIS
NUM_GERACOES = 10
NUM_ENTES = 10
NUM_GENES = 100
NUM_CAMPEOES = 6 #NUMERO PAR

populacao = []
env = gym.make('BipedalWalker-v2')


################################################################ FUNÇÕES
def cria_populacao(n):
	for _ in range(n):
		populacao.append(Ente())

def converte_gene_in_action(gene):
	return [gene.a, gene.t, gene.g, gene.c]	

def faz_cruzamento(ente1, ente2):
	novoEnte1 = copy.deepcopy(ente1)
	novoEnte2 = copy.deepcopy(ente2)
	for i in range(NUM_GENES):
		if(random.uniform(0, 100) > 50):
			aux = novoEnte1.dna.genes[i]
			novoEnte1.dna.genes[i] = novoEnte2.dna.genes[i]
			novoEnte2.dna.genes[i] = aux
	return novoEnte1, novoEnte2

################################################## DEFINIÇÕES DE CLASSES
class Gene:
	def __init__(self):
		self.setA(random.uniform(-1, 1))
		self.setT(random.uniform(-1, 1))
		self.setG(random.uniform(-1, 1))
		self.setC(random.uniform(-1, 1))

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

class DNA:
	num_genes = NUM_GENES

	def __init__(self):
		self.genes = []
		for _ in range(self.num_genes):
			self.addGene(Gene())
		
	def addGene(self, gene):
		self.genes.append(gene)

class Ente:

	def __init__(self):
		self.setDNA(DNA())

	def setDNA(self, dna):
		self.dna = dna

	def setFitness(self, fit):
		self.fit = fit

######################################################### LAÇO PRINCIPAL


#inicio as variáveis
cria_populacao(NUM_ENTES)

#calculo a aptidão de cada ente
for _ in range(NUM_GERACOES):
	for ente in populacao:
		env.reset()
		enteFitness = 0
		for gene in ente.dna.genes:
			env.render()
			action = converte_gene_in_action(gene)	
			observation, reward, done, info = env.step(action)
			gene.setFenotipo(reward)
			enteFitness = enteFitness + reward
		ente.setFitness(enteFitness)

	#escolho os N mais aptos
	#ordena entes por maior apitidã(o
	populacao.sort(key=lambda e: e.fit, reverse=True)

	#pega os primeiros N mais aptos
	it = iter(populacao[:NUM_CAMPEOES])
	for campeao in it:

		#faço cruzamento do DNA deles
		filho1, filho2 = faz_cruzamento(campeao.fit, next(it).fit)

		#coloco o resultado do cruzamento no lugar dos menos aptos
		populacao.append(filho1)
		populacao.append(filho2)
		
#repita o processo por N gerações

env.close()

