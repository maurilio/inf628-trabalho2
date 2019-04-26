############################################################ BIBLIOTECAS
import gym
import random


###################################################### VARIÁVEIS GLOBAIS
populacao = []
env = gym.make('BipedalWalker-v2')


################################################################ FUNÇÕES
def cria_populacao(n):
	for _ in range(n):
		populacao.append(Ente())

def converte_gene_in_action(gene):
	return [gene.a, gene.t, gene.g, gene.c]	

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

class DNA:
	num_genes = 1000

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
cria_populacao(4)

for ente in populacao:
	env.reset()

	print("NOVO ENTE ###############")	

	for gene in ente.dna.genes:
		env.render()
		action = converte_gene_in_action(gene)
		print("Acao: ")
		print(action)
		observation, reward, done, info = env.step(action)
		ente.setFitness(reward)

env.close()

