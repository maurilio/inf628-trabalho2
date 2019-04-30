############################################################ BIBLIOTECAS
import gym
import random
import copy

###################################################### VARIÁVEIS GLOBAIS
NUM_GERACOES = 50
NUM_ENTES = 40
NUM_GENES = 1000
NUM_CAMPEOES = 20 #NUMERO PAR, não pode ser maior que a metade da populacao (NUM_ENTES)
PROB_MUTACAO = 10

populacao = []
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
	novoEnte1 = ente1.copy()
	novoEnte2 = ente2.copy()
	crossoverPoint = round(random.uniform(0, 1) * NUM_GENES)
	for i in range(NUM_GENES):
		if i > crossoverPoint:
			aux = novoEnte1.dna.genes[i]
			novoEnte1.dna.genes[i] = novoEnte2.dna.genes[i]
			novoEnte2.dna.genes[i] = aux
		if random.uniform(0, 100) < PROB_MUTACAO:
			novoEnte1.dna.genes[i] = Gene(random_action(), random_action(), random_action(), random_action())
			novoEnte2.dna.genes[i] = Gene(random_action(), random_action(), random_action(), random_action())

	return novoEnte1, novoEnte2

def calc_fitness(totalReward):
	return totalReward

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
	num_genes = NUM_GENES

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

	def __init__(self, dna = None):
		if dna is None:
			self.setDNA(DNA())
			self.fit = 0
		else:
			self.setDNA(dna)
			self.fit = 0

	def setDNA(self, dna):
		self.dna = dna

	def setFitness(self, fit):
		self.fit = fit

	def copy(self):
		return Ente(self.dna.copy())
		

######################################################### LAÇO PRINCIPAL


#inicio as variáveis
cria_populacao(NUM_ENTES)

#calculo a aptidão de cada ente
for g in range(NUM_GERACOES):

	print('GERAÇÃO ', g)

	i = 0
	for ente in populacao:

		i = i + 1
		print('\tENTE:', i, 'APITIDÃO:', ente.fit)

		if ente.fit == 0:

			env.reset()
			totalReward = 0
			for gene in ente.dna.genes:
				#env.render()
				action = converte_gene_in_action(gene)	
				observation, reward, done, info = env.step(action)
				gene.setFenotipo(reward)
				if reward > 0:
					totalReward = totalReward + 1
			ente.setFitness(calc_fitness(totalReward))
			#print('\t   NOVA APITIDÃO:', ente.fit)

		else:
			#print('\t   JÁ FOI EXPERIMENTADO.')
			continue

	#escolho os N mais aptos
	#ordena entes por maior apitidã(o
	populacao.sort(key=lambda e: e.fit, reverse=True)

	#elimina os mais fracos, abrindo espaço para os novos entes
	del populacao[-NUM_CAMPEOES:]

	#pega os primeiros N mais aptos
	it = iter(populacao[:NUM_CAMPEOES])
	for campeao in it:

		#faço cruzamento do DNA deles
		filho1, filho2 = faz_cruzamento(campeao, next(it))

		#coloco o resultado do cruzamento no lugar dos menos aptos
		populacao.append(filho1)
		populacao.append(filho2)
		
#repita o processo por N gerações

#exibe o comportamento do ganhador
populacao.sort(key=lambda e: e.fit, reverse=True)
input("PREPARADO PARA VER O GANHADOR?\nPressione qualquer tecla para continuar ...")
env.reset()
ente = populacao[0]
for gene in ente.dna.genes:
	env.render()
	action = converte_gene_in_action(gene)	
	observation, reward, done, info = env.step(action)

env.close()

