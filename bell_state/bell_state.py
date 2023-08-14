# Copyright 2023 Kieran W Harvie. All rights reserved.

# Import qiskit and the AER Simulator
from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator

#create quantum circuit with 4 qubits and 4 classical bits
qc = QuantumCircuit(4, 4)

# All quibits start in 0 for variety invert the 2nd and 3rd qubits
qc.x([2,3])

# Construct the Bell state creators 
qc.h([0,2])
qc.cx(0,1) 
qc.cx(2,3)

# A barrier to stop the optimizer combining the Bell creators and upcoming measurers
# And for visual clarity.
qc.barrier()

# Construct Bell state measurers
qc.cx(2,3)
qc.h(2)
qc.barrier()

# Measure the states
qc.measure([0,1,2,3], [0,1,2,3])

# Export the circuit diagram
fig = qc.draw(output='mpl')
fig.savefig("circuit.png")

# Simulate the circuit
sim = AerSimulator()  # make new simulator object
job = sim.run(qc)      # run the experiment
result = job.result()  # get the results

# Output the simulation results
# Remember, most significant bits first
print("Result: ", result.get_counts())
