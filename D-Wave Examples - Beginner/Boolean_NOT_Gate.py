# Boolean NOT Gate - D-Wave Beginner Example

# This example solves a simple problem of a Boolean NOT gate to demonstrate the 
# mathematical formulation of a problem as a binary quadratic model (BQM) and using 
# Ocean tools to solve such problems on a D-Wave system.

# Set up a D-Wave system as the sampler
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
sampler = EmbeddingComposite(DWaveSampler())

# Ask for 5000 samples
Q = {('x', 'x'): -1, ('x', 'z'): 2, ('z', 'x'): 0, ('z', 'z'): -1}
response = sampler.sample_qubo(Q, num_reads=5000)
for datum in response.data(['sample', 'energy', 'num_occurrences']):   
	print(datum.sample, "Energy: ", datum.energy, "Occurrences: ", datum.num_occurrences)

