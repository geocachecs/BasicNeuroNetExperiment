import random


class Neuron:
	def __init__(self,weight=0):
		self.weight = weight
		self.raw_input = 0
		self.output = 0
		self.connectionsBack = []
		##self.connectionsForward = []
		#following are fore backpropogation
		self._weightAdjustment = 0
		self._goalActivation = 0.5
	def newInput(self,input):
		weightedInput = input+self.weight
		if(weightedInput>709): # numbers larger than 709 will cause OverflowError
			self.output =  0
		else:
			self.output =  1/float(1 + pow(2.718281828459,-weightedInput))
	def adjustWeight(self,percentage):
		self.weight += percentage # atm I think this may be the best way to adjust
	def setConnections(self,allConnections):
		self.connectionsBack = allConnections
	def getOutput(self):
		return self.output
	def backPropogate(self):
		if(self._weightAdjustment>=0):
			self._goalActivation = 1
		else:
			self._goalActivation = 0
		self.weight += self._weightAdjustment
		if(len(self.connectionsBack)>0):
			self.connectionsBack.sort(key=lambda n:n.output,reverse=True)
			
	
			
class Connection:
	def __init__(selfn1,n2):
		self.connectionWeight  = (random.random() - 0.5) * 10
		self.lastNueron = n1
		self.nextNueron = n2
		self.output = 0
	def newInput(self):
		self.output = self.lastNueron.getOutput() * self.connectionWeight
	def getOutput(self):
		return self.output
	def setNextNueron(self):
		self.nextNueron.setInput(self.getOutput)
	def adjustWeight(self,percentage):
		self.connectionWeight += percentage # atm I think this may be the best way to adjust







