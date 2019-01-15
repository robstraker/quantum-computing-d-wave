# Multiple-Gate Circuit - D-Wave Intermediate Example

# Formulate the Problem as a CSP
# 1. Single comprehensive constraint:
import dwavebinarycsp

def logic_circuit(a, b, c, d, z):
    not1 = not b
    or2 = b or c
    and3 = a and not1
    or4 = or2 or d
    and5 = and3 and or4
    not6 = not or4
    or7 = and5 or not6
    return (z == or7)

csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
csp.add_constraint(logic_circuit, ['a', 'b', 'c', 'd', 'z'])

# 2. Multiple small constraints:
import dwavebinarycsp
import dwavebinarycsp.factories.constraint.gates as gates
import operator

csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
csp.add_constraint(operator.ne, ['b', 'not1'])  # add NOT 1 gate
csp.add_constraint(gates.or_gate(['b', 'c', 'or2']))  # add OR 2 gate
csp.add_constraint(gates.and_gate(['a', 'not1', 'and3']))  # add AND 3 gate
csp.add_constraint(gates.or_gate(['d', 'or2', 'or4']))  # add OR 4 gate
csp.add_constraint(gates.and_gate(['and3', 'or4', 'and5']))  # add AND 5 gate
csp.add_constraint(operator.ne, ['or4', 'not6'])  # add NOT 6 gate
csp.add_constraint(gates.or_gate(['and5', 'not6', 'z']))  # add OR 7 gate

# Convert the binary constraint satisfaction problem to a binary quadratic model
bqm = dwavebinarycsp.stitch(csp)

# Minor-Embedding and Sampling
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

# Set up a D-Wave system as the sampler
sampler = EmbeddingComposite(DWaveSampler())

# Ask for 1000 samples and separate those that satisfy the CSP from those that fail to do so.
response = sampler.sample(bqm, num_reads=1000)

# Check how many solutions meet the constraints (are valid)
valid, invalid, data = 0, 0, []
for datum in response.data(['sample', 'energy', 'num_occurrences']):
    if (csp.check(datum.sample)):
        valid = valid+datum.num_occurrences
        for i in range(datum.num_occurrences):
            data.append((datum.sample, datum.energy, '1'))
    else:
        invalid = invalid+datum.num_occurrences
        for i in range(datum.num_occurrences):
            data.append((datum.sample, datum.energy, '0'))
print(valid, invalid)

# Looking at the Results
# Verify the solution to the circuit problem by checking an arbitrary valid or invalid sample:
print(next(response.samples())) 

# Plot the energies for valid and invalid samples
import matplotlib.pyplot as plt
plt.ion()
plt.scatter(range(len(data)), [x[1] for x in data], c=['y' if (x[2] == '1') else 'r' for x in data],marker='.')
plt.xlabel('Sample')
plt.ylabel('Energy')

for datum in response.data(['sample', 'energy', 'num_occurrences', 'chain_break_fraction']):
	print(datum)
