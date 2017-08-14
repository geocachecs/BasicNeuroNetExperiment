import random


class Neuron:
	def __init__(self,weight=0):
		self._activationWeight = weight
		self.raw_input = 0
		self.activation = 0
		self.connectionsBack = []
		##self.connectionsForward = []
		#following are for backpropogation
		self._weightAdjustment = 0
		self._goalActivation = 0.5
		self._error = 0
	def calculateActivation(self):
		input = 0
		for conn in self.connectionsBack:
			input += conn.getOutput()
		weightedInput = input+self._activationWeight
		if(weightedInput>709): # numbers larger than 709 will cause OverflowError
			self.activation =  0
		else:
			self.activation =  1/float(1 + pow(2.718281828459,-weightedInput))
	
	def setConnections(self,allConnections):
		self.connectionsBack = allConnections
	def getActivation(self):
		return self.activation
		
	def _applyActivationWeightAdjustment(self,multiplier=1):
		self._activationWeight += self._weightAdjustment*multiplier
	def _calculateNewGoalActivation(self):
		if(self._weightAdjustment>=0):
			self._goalActivation = 1
		else:
			self._goalActivation = 0
	def _sortConnections(self):
		if(len(self.connectionsBack)>0):
			self.connectionsBack.sort(key=lambda n:n.output,reverse=True)
	def _calculateNewError():
		self._error = self._goalActivation - self.getActivation()
	
	
	def backPropogate(self):
		self._applyActivationWeightAdjustment()
		self._calculateNewGoalActivation()
		self._sortConnections()
		
		for conn in self.connectionsBack:
			self.calculateActivation()
			self._calculateNewError()
			conn.adjustWeight(self._error)
		


		
			
class Connection:
	def __init__(selfn1,n2):
		self.connectionWeight  = (random.random() - 0.5) * 6
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
	def adjustBackNueronActivationWeight(self,percentage):
		self.lastNueron._weightAdjustment






