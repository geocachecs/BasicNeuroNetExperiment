import random


class Neuron:
	def __init__(self,weight=0):
		self._activationWeight = weight
		self._input = 0
		self._activation = 0
		self.connectionsBack = []
		self.connectionsForward = []
		self.e = 2.718281828459
		
		#following are for backpropogation
		self._weightAdjustmentTemp = 0
		self._weightAdjustment = 0
		self._goalActivation = 0.5
		self._error = 0
		self._backAcvitationAdjustVariable = 0
	def calculateActivation(self):
		input = 0
		for conn in self.connectionsBack:
			input += conn.getOutput()
		weightedInput = input+self._activationWeight
		if(weightedInput>709): # numbers larger than 709 will cause OverflowError
			self._activation =  0
		else:
			self._activation =  1/float(1 + pow(self.e,-weightedInput))
	def setConnections(self,allConnections):
		self.connectionsBack = allConnections
	def getActivation(self):
		return self._activation
	def contributeWeightAdjustment(self,input):
		self._weightAdjustmentTemp += input
	def getError(self):
		return self._error
	## 
	def _calculateActivationWeightAdjustment(self): ## used in conjunction with _backActivationWeightAdjust() in a forward neuron thru Connection.backActivationWeightAdjust()
		averageConnWeight = 0
		for conn in self.connectionsForward:
			averageConnWeight += conn.getWeight()
		averageConnWeight /= len(self.connectionsForward)
		self._weightAdjustment = (self._weightAdjustmentTemp/averageConnWeight)/len(self.connectionsForward)
		self._weightAdjustmentTemp = 0
	def _applyActivationWeightAdjustment(self):
		self._activationWeight += self._weightAdjustment
	def _calculateGoalActivation(self): ##_calculateActivationWeightAdjustment() must be run first
 		if(self._weightAdjustment>=0):
			self._goalActivation = 1
		else:
			self._goalActivation = 0
	def _sortConnections(self):
		if(len(self.connectionsBack)>0):
			self.connectionsBack.sort(key=lambda n:n.output,reverse=True)
	def _calculateError(): ## _calculateGoalActivation() and _calculateActivationWeightAdjustment() must be run first
		self._error = self._goalActivation - self.getActivation()
	def _calculateBackActivationAdjustVariable(self,multiplier=4)
		self._backAcvitationAdjustVariable = pow(self.e,self._input)/pow((pow(self.e,self._input)+1),2) * self.getError() * multiplier
	def _backActivationWeightAdjust(self,conn): ## used in conjunction with _calculateActivationWeightAdjustment() in a back neuron thru Connection.backActivationWeightAdjust()
		conn.backActivationWeightAdjust(self._backAcvitationAdjustVariable*conn.getWeight)
		
	def backPropogate(self):
		self._calculateActivationWeightAdjustment()
		self._applyActivationWeightAdjustment()
		self._calculateGoalActivation()
		
		self._sortConnections()
		self.calculateActivation()
		
		self._calculateBackActivationAdjustVariable()
		
		for conn in self.connectionsBack:
			self._calculateError()
			differenceFromCurrentInput = conn.adjustWeight(self._error) #adjusts weight on connection
			self._input += differenceFromCurrentInput #updates input for purposes of backpropogation
			self._backActivationWeightAdjust(conn) #contribute to back nueron's activation weight adjustment and goal activation

		
			
class Connection:
	def __init__(self,n1,n2):
		self.connectionWeight  = (random.random() - 0.5) * 6
		self.backNueron = n1
		self.forwardNueron = n2
		self.output = 0
	def newInput(self):
		self.output = self.backNueron.getOutput() * self.connectionWeight
	def getOutput(self):
		return self.output
	def setNextNueron(self):
		self.forwardNueron.setInput(self.getOutput)
	def adjustWeight(self,percentage):
		oldOutput = self.getOutput()
		self.connectionWeight += percentage # atm I think this may be the best way to adjust
		newOutput = self.getOutput()
		return oldOutput-newOutput
	def getWeight(self): #used by Nueron._backActivationWeightAdjust()
		return self.connectionWeight
	def adjustBackNueronActivationWeight(self,percentage):
		self.backNueron._weightAdjustment
	def backActivationWeightAdjust(self,input): ## used by Neuron._backActivationWeightAdjust()
		self.backNueron.contributeWeightAdjustment(input)






