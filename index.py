# Shaheer Ahmed (k190233) - 4F - ToA A3 - Q5

from statemachine import StateMachine, State, Transition
import json
from PySimpleAutomata import automata_IO
from tabulate import tabulate

class FiniteAutomata:
	def __init__(self):
		self.states = {}
		self.transitions = {}
		self.initialState = None
		self.jsonDump = {
			"alphabet": [],
			"states": [],
			"initial_states": [],
			"accepting_states": [],
			"transitions": [],
		}

	def transition(self, fromState = None, token = None):
		# TODO: null checks

		if ((fromState not in self.transitions) or (token not in self.transitions[fromState])):
			# failed to transition
			return False

		self.transitions[fromState][token]["transitioner"] # should be func
		return self.transitions[fromState][token]["nextState"]

	def addState(self, stateName = None, state = None):
		# TODO: null checks

		if (not self.states):
			self.initialState = stateName

		if (stateName not in self.states):
			self.states[stateName] = state
		
	def addTransition(self, fromState = None, toState = None, token = None):
		# TODO: null checks

		if (fromState not in self.states or toState not in self.states):
			# undefined states
			return False

		if (fromState not in self.transitions):
			self.transitions[fromState] = {}

		if (token in self.transitions[fromState]):
			# token transition already defined
			return False

		self.transitions[fromState][token] = {
			"nextState": toState,
			"transitioner": (self.getState(fromState)).to((self.getState(toState))),
		}

	def getState(self, stateName = None):
		# TODO: null checks

		if (stateName in self.states):
			return self.states[stateName]

		return None

	def buildFA(self):
		if len(self.states.keys()) <= 0 or len(self.transitions.keys()) <= 0:
			return

		alphabets = set()
		
		self.jsonDump["states"] = list(self.states.keys())

		for state in self.states:
			if self.states[state].initial == True:
				self.jsonDump["initial_states"].append(state)

			if self.states[state].value == True:
				self.jsonDump["accepting_states"].append(state)

		self.jsonDump["initial_state"] = self.jsonDump["initial_states"][0]

		for fromState in self.transitions:
			for token in self.transitions[fromState]:
				alphabets.add(token)
				self.jsonDump["transitions"].append([fromState, token, self.transitions[fromState][token]["nextState"]])

		self.jsonDump["alphabet"] = list(alphabets)

	def dumpJson(self, dumpPath = None):
		if len(self.jsonDump.keys()) <= 0 or dumpPath is None:
			return

		with open(dumpPath, 'w') as f:
			json.dump(self.jsonDump, f)

	def getFormattedDFA(self, dfaPath = None):
		if dfaPath is None:
			return
		
		return automata_IO.dfa_json_importer(dfaPath)

	def saveSVG(self, dfaPath = None, dfaName = None, svgPath = None):
		if dfaPath is None or dfaName is None or svgPath is None:
			return

		dfa = self.getFormattedDFA(dfaPath)

		automata_IO.dfa_to_dot(dfa, dfaName, svgPath)

	def visualize(self, dfaPath = None, dfaName = None, svgPath = None):
		if dfaPath is None or dfaName is None or svgPath is None:
			return

		self.buildFA()
		self.dumpJson(dfaPath)
		self.getFormattedDFA(dfaPath)
		self.saveSVG(dfaPath, dfaName, svgPath)

	def reset(self):
		self.states = {}
		self.transitions = {}

	# Tests a string on our FA
	def test(self, string = None, verbose = False, silent = False):
		state = FA.initialState
		oldState = state

		if not silent:
			print(f"Testing [string = \"{string}\"]")
		if (verbose and not silent):
			print(f"Starting from [state = {state}]...")

		for char in string:
			state = FA.transition(fromState=state, token=char)
			if (verbose and not silent):
				print(f"Transitioned from [state = {oldState}] to [state = {state}] with [token = {char}]...")
			oldState = state
		
		if not silent:
			print(f"Ended at [state = {state}] [value = \"{self.getState(state).value}\"]...")

		return self.getState(state).value

FA = FiniteAutomata()

# Simulating An FA

# Adding States | Initialization
FA.addState("q0", State("q0", value=False, initial=True))
FA.addState("q1", State("q1", value=False, initial=False))
FA.addState("q2", State("q2", value=False, initial=False))
FA.addState("q3", State("q3", value=True, initial=False))
FA.addState("q4", State("q4", value=True, initial=False))
FA.addState("q5", State("q5", value=False, initial=False))
FA.addState("q6", State("q6", value=False, initial=False))
FA.addState("q7", State("q7", value=False, initial=False))
FA.addState("q8", State("q8", value=True, initial=False))
FA.addState("q9", State("q9", value=True, initial=False))

# Adding Transitions
FA.addTransition("q0", "q1", "a")
FA.addTransition("q0", "q9", "b")

FA.addTransition("q1", "q8", "a")
FA.addTransition("q1", "q2", "b")

FA.addTransition("q2", "q3", "a")
FA.addTransition("q2", "q2", "b")

FA.addTransition("q3", "q2", "a")
FA.addTransition("q3", "q4", "b")

FA.addTransition("q4", "q5", "a")
FA.addTransition("q4", "q8", "b")

FA.addTransition("q5", "q4", "a")
FA.addTransition("q5", "q5", "b")


FA.addTransition("q6", "q7", "a")
FA.addTransition("q6", "q5", "b")


FA.addTransition("q7", "q6", "a")
FA.addTransition("q7", "q5", "b")


FA.addTransition("q8", "q1", "a")
FA.addTransition("q8", "q3", "b")


FA.addTransition("q9", "q7", "a")
FA.addTransition("q9", "q8", "b")

# visualizes the DFA constructed
FA.visualize("./dfa.json", "DFA", "./")

acceptedStrings = []
rejectedStrings = []

# Generates All Possible Strings Of our FA, of specified len
def getCombos(str = "", i = 0, len = 10):
	if (i > len):
		return

	# print(f"{str}")

	if (FA.test(str, verbose=False, silent = True)):
		# print(str)
		acceptedStrings.append(str)
		# print("\n")
	else:
		rejectedStrings.append(str)

	getCombos(str + "a", i + 1, len)
	getCombos(str + "b", i + 1, len)

getCombos(len=5)

print(tabulate([list(item) for item in zip(acceptedStrings, rejectedStrings)], headers=["Accepted Strings", "Rejected Strings"], tablefmt="pretty"))
