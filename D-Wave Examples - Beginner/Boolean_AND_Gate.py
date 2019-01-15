# Boolean AND Gate - D-Wave Beginner Example

# This example solves a simple problem of a Boolean AND gate on a D-Wave system to 
# demonstrate programming the underlying hardware more directly; in particular, 
# minor-embedding a chain.

# Set the QUBO coefficients for this AND gate
Q = {('x1', 'x2'): 1, ('x1', 'z'): -2, ('x2', 'z'): -2, ('z', 'z'): 3}

# Automated Minor-Embedding
# Set up a D-Wave system as the sampler
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
sampler = DWaveSampler()
sampler_embedded = EmbeddingComposite(sampler)

# Ask for 5000 samples
response = sampler_embedded.sample_qubo(Q, num_reads=5000)
for datum in response.data(['sample', 'energy', 'num_occurrences']):   
	print(datum.sample, "Energy: ", datum.energy, "Occurrences: ", datum.num_occurrences)

# Non-automated Minor-Embedding
# The Boolean NOT Gate example found that a NOT gate can be represented by a BQM in 
# QUBO form with the following coefficients:
Q_not = {('x', 'x'): -1, ('x', 'z'): 2, ('z', 'x'): 0, ('z', 'z'): -1}

# Look at properties of the sampler. We select the first node, which on a QPU is a qubit, 
# and print its adjacent nodes, i.e., coupled qubits
print(sampler.adjacency[sampler.nodelist[0]])  

# Use the FixedEmbeddingComposite composite to manually minor-embed the problem. Its last 
# line prints a confirmation that indeed the two selected qubits are adjacent (coupled)
from dwave.system.composites import FixedEmbeddingComposite
sampler_embedded = FixedEmbeddingComposite(sampler, {'x': [0], 'z': [4]})
print(sampler_embedded.adjacency)

# Ask for 5000 samples
response = sampler_embedded.sample_qubo(Q_not, num_reads=5000)
for datum in response.data(['sample', 'energy', 'num_occurrences']):   
	print(datum.sample, "Energy: ", datum.energy, "Occurrences: ", datum.num_occurrences)

# Use Ocean’s dwave-system FixedEmbeddingComposite() composite for manual minor-embedding. 
# Its last line prints a confirmation that indeed all three variables are connected (coupled).
from dwave.system.composites import FixedEmbeddingComposite
embedding = {'x1': {1}, 'x2': {5}, 'z': {0, 4}}
sampler_embedded = FixedEmbeddingComposite(sampler, embedding)
print(sampler_embedded.adjacency)     

# Ask for 5000 samples
Q = {('x1', 'x2'): 1, ('x1', 'z'): -2, ('x2', 'z'): -2, ('z', 'z'): 3}
response = sampler_embedded.sample_qubo(Q, num_reads=5000)
for datum in response.data(['sample', 'energy', 'num_occurrences']):   
	print(datum.sample, "Energy: ", datum.energy, "Occurrences: ", datum.num_occurrences)

# For comparison, the following code purposely weakens the chain strength (strength of the
# coupler between qubits 0 and 4, which represents variable z). The first line prints the 
# range of values available for the D-Wave system this code is executed on. By default, 
# FixedEmbeddingComposite() used the maximum chain strength, which is 2. By setting it to 
# a low value of 0.25, the two qubits are not strongly correlated and the result is that 
# many returned samples represent invalid states for an AND gate.
print(sampler.properties['extended_j_range'])
sampler_embedded = FixedEmbeddingComposite(sampler, embedding)
response = sampler_embedded.sample_qubo(Q, num_reads=5000, chain_strength=0.25)
for datum in response.data(['sample', 'energy', 'num_occurrences']):   
	print(datum.sample, "Energy: ", datum.energy, "Occurrences: ", datum.num_occurrences)
