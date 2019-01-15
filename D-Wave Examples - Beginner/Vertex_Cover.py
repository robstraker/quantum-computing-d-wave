# Vertex Cover - D-Wave Beginner Example

# This example solves a few small examples of a known graph problem, 
# minimum vertex cover. A vertex cover is a set of vertices such that 
# each edge of the graph is incident with at least one vertex in the set. 
# A minimum vertex cover is the vertex cover of smallest size.

import networkx as nx
s5 = nx.star_graph(4)

# Solving classically on a CPU
from dimod.reference.samplers import ExactSolver
sampler = ExactSolver()
import dwave_networkx as dnx
print(dnx.min_vertex_cover(s5, sampler))

# Solving on a D-Wave System
# A five-node star graph
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
sampler = EmbeddingComposite(DWaveSampler())
print(dnx.min_vertex_cover(s5, sampler))

# Additional problem graphs
# A five-node (wheel) graph
w5 = nx.wheel_graph(5)
print(dnx.min_vertex_cover(w5, sampler))
print(dnx.min_vertex_cover(w5, sampler))

# A ten-node (circular-ladder) graph
c5 = nx.circular_ladder_graph(5)
print(dnx.min_vertex_cover(c5, sampler))
print(dnx.min_vertex_cover(c5, sampler))