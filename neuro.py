import random


class Neuron:
	def __init__(self):
		self._activationWeight = (random.random() - 0.5) * 6 ## will set activation weight between -3 and 3
		self._weightedInput = 0
		self._activation = 0
		self.connectionsBack = []
		self.connectionsForward = []
		self.id = random.random()
		self.e = 2.718281828459
		
		#following are for backpropogation
		self._goalActivationManuallySet=False
		self._weightAdjustmentTemp = 0
		self._weightAdjustment = 0
		self._goalActivation = 0.5
		self._error = 0

	## private functions
	def _calculateActivationWeightAdjustment(self): ## used in conjunction with _backActivationWeightAdjust() in a forward neuron thru Connection.backActivationWeightAdjust()
		averageConnWeight = 0
		totalConnWeight = 0
		if(len(self.connectionsForward)>0):
			for conn in self.connectionsForward:
				totalConnWeight += conn.getWeight()
			averageConnWeight = totalConnWeight/len(self.connectionsForward)
			self._weightAdjustment = (self._weightAdjustmentTemp/averageConnWeight)/len(self.connectionsForward)
		self._weightAdjustmentTemp = 0
	def _applyActivationWeightAdjustment(self):
		self._activationWeight += self._weightAdjustment
	def _calculateGoalActivation(self): ##_calculateActivationWeightAdjustment() must be run first
		if(self._goalActivationManuallySet==False):
			if(self._weightAdjustment>=0):
				self._goalActivation = 1
			else:
				self._goalActivation = 0
	def _sortConnections(self):
		if(len(self.connectionsBack)>0):
			if(self._goalActivation >0.5):
				self.connectionsBack.sort(key=lambda n:n.output,reverse=True)
			else:
				self.connectionsBack.sort(key=lambda n:n.output,reverse=False)
	def _calculateError(self): ## _calculateGoalActivation() and _calculateActivationWeightAdjustment() must be run first
		self._error = self._goalActivation - self.getActivation()
	def _backActivationWeightAdjust(self,conn,multiplier=4): ## used in conjunction with _calculateActivationWeightAdjustment() in a back neuron thru Connection.backActivationWeightAdjust()
		if(self._weightedInput > 354):
			backAcvitationAdjustVariable = 0
		else:
			backAcvitationAdjustVariable = pow(self.e,self._weightedInput)/pow((pow(self.e,self._weightedInput)+1),2) * self.getError() * multiplier
		conn.backActivationWeightAdjust(backAcvitationAdjustVariable*conn.getWeight())
	## public functions
	def getId(self):
		return self.id
	def printNeuron(self):
		print "    Neuron # " + str(self.getId())
		print "    Activation Weight: " + str(self._activationWeight)
		print "    Forward Connections: "
		for conn in self.connectionsForward:
			print "       Connects to neuron # " + str(conn.getForwardNeuronId())
			print "          Connection weight: " + str(conn.getWeight())
	def calculateActivation(self): # input should always be zero
		input=0
		for conn in self.connectionsBack:
			conn.calculateOutput()
			input += conn.getOutput()
		self._weightedInput = input+self._activationWeight
		if(self._weightedInput<-709): # numbers larger than 709 will cause OverflowError
			self._activation =  0
		else:
			self._activation =  1/float(1 + pow(self.e,-self._weightedInput))
	def getActivation(self):
		return self._activation
	def receiveWeightAdjustmentContribution(self,input): ##used by Connection class during backpropogation
		self._weightAdjustmentTemp += input
	def getError(self):
		return self._error
	def backConnect(self,conn):
		self.connectionsBack.append(conn)
	def forwardConnect(self,conn):
		self.connectionsForward.append(conn)
	def manuallySetGoalActivation(self,goal):
		self._goalActivationManuallySet = True
		self._goalActivation = goal
	def backPropogate(self):
		self._calculateActivationWeightAdjustment()
		self._calculateGoalActivation()
		self._applyActivationWeightAdjustment()
		
		self._sortConnections()
		
		for conn in self.connectionsBack:
			self.calculateActivation()
			self._calculateError()
			differenceFromCurrentInput = conn.adjustConnectionWeight(self.getError()) #adjusts weight on connection
			self._weightedInput += differenceFromCurrentInput #updates input for purposes of backpropogation
			self._backActivationWeightAdjust(conn) #contribute to back nueron's activation weight adjustment and goal activation
		
			
class Connection:
	def __init__(self,forwardNeuron,backNueron):
		self.connectionWeight  = (random.random() - 0.5) * 6 ## will set weight between -3 and 3
		self.forwardNeuron = forwardNeuron
		self.backNueron = backNueron
		self.output = 0
	def newInput(self):
		self.output = self.backNueron.getOutput() * self.connectionWeight
	def calculateOutput(self):
		self.output = self.backNueron.getActivation()*self.connectionWeight
	def getOutput(self): ## used by Neuron.calculateActivation()
		return self.output
	def adjustConnectionWeight(self,percentage): # percentage is error
		oldOutput = self.getOutput()
		self.connectionWeight += percentage # atm I think this may be the best way to adjust
		newOutput = self.getOutput()
		return oldOutput-newOutput
	def getWeight(self): #used by Nueron._backActivationWeightAdjust()
		return self.connectionWeight
	def backActivationWeightAdjust(self,input): ## used by Neuron._backActivationWeightAdjust()
		self.backNueron.receiveWeightAdjustmentContribution(input)
	def getForwardNeuronId(self):
		return self.forwardNeuron.getId()

class InputNeuron(Neuron,object):
		def __init__(self):
			super(InputNeuron,self).__init__()
			self._activationWeight = 0
		def _calculateActivationWeightAdjustment(self): ## used in conjunction with _backActivationWeightAdjust() in a forward neuron thru Connection.backActivationWeightAdjust()
			pass
		def _applyActivationWeightAdjustment(self):
			pass
		def _calculateGoalActivation(self): ##_calculateActivationWeightAdjustment() must be run first
			pass
		def _sortConnections(self):
			pass
		def _calculateError(): ## _calculateGoalActivation() and _calculateActivationWeightAdjustment() must be run first
			pass
		def _calculateBackActivationAdjustVariable(self,multiplier=4):
			pass
		def _backActivationWeightAdjust(self,conn): ## used in conjunction with _calculateActivationWeightAdjustment() in a back neuron thru Connection.backActivationWeightAdjust()
			pass
		## public functions
		def calculateActivation(self,input=0):
				self._activation =  input
				self._weightedInput = input + self._activationWeight #activation weight should be 0 anyway
		def getActivation(self):
			return self._activation
		def receiveWeightAdjustmentContribution(self,input):
			pass
		def getError(self):
			return None	
		def backPropogate(self):
			pass

		
class Brain:
	def __init__(self,neurons): ##nodes should be a tuple describing the number of neurons in each layer, starting with the inputs and ending with outputs
		if(len(neurons)<1):
			raise ValueError("Must be more than one element in nodes")
		self.neuronLayers = []
		self.neuronLayers.append([])
		for j in range(0,neurons[0]):
			self.neuronLayers[0].append(InputNeuron())
		for i in range(1,len(neurons)):
			self.neuronLayers.append([])
			for j in range(0,neurons[i]):
				self.neuronLayers[i].append(Neuron())
		
		for i in range(1,len(self.neuronLayers)): ## connect all the neurons
			for forwardNeuron in self.neuronLayers[i]:
				for backNueron in self.neuronLayers[i-1]:
					tempConn = Connection(forwardNeuron,backNueron)
					backNueron.forwardConnect(tempConn)
					forwardNeuron.backConnect(tempConn)
	
	def getSolution(self,inputs):
		self.forwardPropogate(inputs)
		return self.getOutput()
	
	def forwardPropogate(self,inputs):
		if(len(inputs)!=len(self.neuronLayers[0])):
			raise ValueError("Number of inputs must equal number of input neurons")
		else:
			for i in range(0,len(inputs)):
				self.neuronLayers[0][i].calculateActivation(inputs[i])
			for i in range(1,len(self.neuronLayers)):
				for neuron in self.neuronLayers[i]:
					neuron.calculateActivation()
					
	def getOutput(self):
		output = []
		for neuron in self.neuronLayers[len(self.neuronLayers)-1]:
			output.append(neuron.getActivation())
		return output
					
	def backPropogate(self,inputs,goalActivations):
		for i in range(0,len(self.neuronLayers[len(self.neuronLayers)-1])):
			self.neuronLayers[len(self.neuronLayers)-1][i].manuallySetGoalActivation(goalActivations[i])
		for i in range(len(self.neuronLayers)-1,-1,-1):
			for j in range(0,len(self.neuronLayers[i])):
				self.neuronLayers[i][j].backPropogate()
	def train(self,inputs,goalActivations):
		self.forwardPropogate(inputs)
		self.backPropogate(inputs,goalActivations)
	
	def printBrain(self):
		print "################ BRAIN ####################"
		for i in range(0,len(self.neuronLayers)):
			print 
			print "########### Layer " + str(i)
			for neuron in self.neuronLayers[i]:
				print
				neuron.printNeuron()
				
				
				
#########################################################################################################################
###################################### TESTS ############################################################################

cat = Brain((2,5,5,5,5,1))

def test(num):
	for _ in range(num):
		rand = random.randrange(0,3)
		if(rand == 1):
			cat.train([0,0],[0])
		elif(rand == 2):
			cat.train([0,1],[1])
		elif(rand == 3):
			cat.train([1,0],[1])
		elif(rand == 4):
			cat.train([1,1],[0])


def test2(num):
	lastOutput = -1
	for _ in range(num):
		cat.train([1],[1])
		cat.printBrain()
		print
		solution = cat.getSolution([1])
		print 
		print solution
		if(solution <= lastOutput):
			break
		else:
			lastOutput = solution
	
	