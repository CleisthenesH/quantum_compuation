# Copyright 2023 Kieran W Harvie. All rights reserved.

# Import qiskit and the AER Simulator
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.providers.aer import AerSimulator
from qiskit.extensions import Initialize
from qiskit.quantum_info import random_statevector
from qiskit import IBMQ, Aer, transpile

#create quantum circuit with 3 qubits and 1 classical bit
qm = QuantumRegister(1, name="Message")
qa = QuantumRegister(1, name="Alice")
qb = QuantumRegister(1, name="Bob")

co = ClassicalRegister(1, name="Output")

qc = QuantumCircuit(qm, qa, qb,  co)

# Set-up message
message = Initialize(random_statevector(2))
message.label = "Message"
qc.append(message,[0])

# Contstruct a bell state
qc.h(1)
qc.cx(1,2)

# Alice operations
qc.cx(0,1)
qc.h(0)

# Bob operations
qc.cx(1,2)
qc.cz(0,2)

# Invert the message for easy reading
inv_message = message.gates_to_uncompute()
qc.append(inv_message,[2])
qc.measure(2,0)

# Export the circuit diagram
fig = qc.draw(output='mpl')
fig.savefig("circuit_deferred_measurement.png")

# Simulate the circuit
sim = Aer.get_backend('aer_simulator')
t_qc = transpile(qc, sim)
t_qc.save_statevector()
result = sim.run(t_qc).result()

# Output the simulation results
# Remember, most significant bits first
print("Result: ", result.get_counts())
