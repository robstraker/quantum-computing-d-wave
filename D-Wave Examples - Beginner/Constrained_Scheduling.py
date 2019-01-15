# Constrained Scheduling - D-Wave Beginner Example

# This example solves a binary constraint satisfaction problem (CSP). CSPs require that
# all a problem’s variables be assigned values that result in the satisfying of all
# constraints. Here, the constraints are a company’s policy for scheduling meetings:
# - Constraint 1: During business hours, all meetings must be attended in person at the office.
# - Constraint 2: During business hours, participation in meetings is mandatory.
# - Constraint 3: Outside business hours, meetings must be teleconferenced.
# - Constraint 4: Outside business hours, meetings must not exceed 30 minutes.
# Solving such a CSP means finding meetings that meet all the constraints.

# Define a function that returns True when all constraints are met
def scheduling(time, location, length, mandatory):
	if time:                                 # Business hours
		return (location and mandatory)      # In office and mandatory participation
	else:                                    # Outside business hours
		return ((not location) and length)   # Teleconference for a short duration
    
# Create a constraint from this function and adds it to CSP instance, csp, 
# instantiated with binary variables.    
import dwavebinarycsp
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
csp.add_constraint(scheduling, ['time', 'location', 'length', 'mandatory'])

# Display the BQM’s linear and quadratic coefficients, qi and qi,j respectively in
# ∑Niqixi+∑Ni<jqi,jxixj, which are the inputs for programming the quantum computer.
bqm = dwavebinarycsp.stitch(csp)
bqm.linear
bqm.quadratic  

# Solving classically on a CPU
from dimod.reference.samplers import ExactSolver
sampler = ExactSolver()
solution = sampler.sample(bqm)

# Sets variable min_energy to the BQM’s lowest value, which is in the first record of 
# the returned result
min_energy = next(solution.data(['energy']))[0]
print(min_energy)

# Print all solutions (assignments of variables) for which the BQM has its minimum value.
for sample, energy in solution.data(['sample', 'energy']):
	if energy == min_energy:
		time = 'business hours' if sample['time'] else 'evenings'
		location = 'office' if sample['location'] else 'home'
		length = 'short' if sample['length'] else 'long'
		mandatory = 'mandatory' if sample['mandatory'] else 'optional'
		print("During {} at {}, you can schedule a {} meeting that is {}".format(time, location, length, mandatory))
		
# Set up a D-Wave system as the sampler
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
sampler = EmbeddingComposite(DWaveSampler())

# Ask for 5000 answers
response = sampler.sample(bqm, num_reads=5000)

# Print all those solutions (assignments of variables) for which the BQM has its 
# minimum value and the number of times it was found.
total = 0
for sample, energy, occurrences in response.data(['sample', 'energy', 'num_occurrences']):
	total = total + occurrences
	if energy == min_energy:
		time = 'business hours' if sample['time'] else 'evenings'
		location = 'office' if sample['location'] else 'home'
		length = 'short' if sample['length'] else 'long'
		mandatory = 'mandatory' if sample['mandatory'] else 'optional'
		print("{}: During {} at {}, you can schedule a {} meeting that is {}".format(occurrences, time, location, length, mandatory))
print("Total occurrences: ", total)