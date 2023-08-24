<!-- Copyright 2023 Kieran W Harvie. All rights reserved. -->

# Quantum Teleportation
As revised in the revision directory there is no way to clone an independent, arbitrary, unknown state.
But work has continued in the area of communicating quantum states by compromising on one of the conditions.

Quantum Teleportation is foremost result which clones an arbitrary and unknown state between two parties at the cost of changing the original by entangling it with a shared bell state.

The most enlightening form of the algorithm transports the information between parties in a classical channel.
But for practical reasons a method with deferred measurement also exits and will be presented.

# Classical Transmission
<p align="center">
	<img src="circuit_classical_transmission.png" alt="A circuit diagram" width=80%>
	<br>
		A circuit diagram for quantum teleportation with classical transmission.
	<br>
</p>
We will trace this algorithm by checking the state of the registers at each barrier.
Examples on writing the matrices in full can found in the bell directory.

Let the message state be given by:
```math
|\text{Message}\rangle = m_0|0\rangle+m_1|1\rangle
```
Then the state at the first barrier is:
```math
|\text{Message}\rangle\otimes|\Phi^+\rangle = \frac{1}{\sqrt{2}}\bigg(m_0|000\rangle+m_0|011\rangle+m_1|100\rangle + m_1|111\rangle\bigg)
```
Observe that message and bell state are separable,
now check the second barrier: 
```math
\frac{m_0}{2}\bigg(|000\rangle+|100\rangle+|011\rangle+|111\rangle\bigg)+\frac{m_1}{2}\bigg(|010\rangle-|110\rangle+|001\rangle-|101\rangle\bigg)
```
The message and bell state are now entangled and the state looks messy but can be written as a sum over the first two labels as:
```math
\frac{|00\rangle}{2}\otimes(m_0|0\rangle+m_1|1\rangle)+
\frac{|01\rangle}{2}\otimes(m_1|0\rangle+m_0|1\rangle)+
\frac{|10\rangle}{2}\otimes(m_0|0\rangle-m_1|1\rangle)+
\frac{|11\rangle}{2}\otimes(-m_1|0\rangle+m_0|1\rangle)
```

This seperatbility lets us know what Bob's state will be after measuring the X and Z bits:
| Z bit | X bit | Bob's State |
| --- | --- | --- |
| 0 | 0 | $m_0\|0\rangle+m_1\|1\rangle$ |
| 0 | 1 | $m_1\|0\rangle+m_0\|1\rangle$ |
| 1 | 0 | $m_0\|0\rangle-m_1\|1\rangle$ |
| 1 | 1 | $-m_1\|0\rangle+m_0\|1\rangle$ |

The goal is to get back to $m_0|0\rangle+m_1|1\rangle$.
First notice that every state with the coefficients switch has a X bit set, and vise-versa.
After swapping the coefficients we notice that every state with a Z bit set has a negative $|1\rangle$ and vise-versa.
These operations correspond to the X and Z gates,
as implied by the bit names,
and after completing these operations Bob's state has returned to the message state.

The final gate isn't part of the teleportation and is the initiating gate's disentangler.
If the initial state is present then the disentangler outputs $|0\rangle$,
basically it makes measurement easier.

With everything set up we can simulate the circuit,
giving the following results:
| State | Count |
| --- | --- |
| 010 | 254 |
| 000 | 262 |
| 011 | 256 |
| 001 | 252 |

This isn't the expected results.
What's happening is that measuring and then preforming other quantum operations is very buggy.
This isn't a problem with the simulation,
or more accurately it's a problem with quantum computers that is correctly being simulated.

So what should be done?
While it is possible to tweak the simulator setting to avoid this behaviour now this is also a good opportunity to practice deferred measurement.

# Deferred Measurement
<p align="center">
	<img src="circuit_deferred_measurement.png" alt="A circuit diagram" width = 80%>
	<br>
		A circuit diagram for quantum teleportation with deferred measurement.
	<br>
</p>

Despite not as demonstrative as moving the Z and X bits classically,
since the goal of teleportation is to communicate information about the quantum state over some distance and not just within the same quantum computer,
we can preform $CZ$ and $CX$ as quantum operations and then measure.
Doing so gave the above circuit.

Although not as practically useful it does work as a proof of concept as it outputs $0$ all 1024 times.

# Appendix
In the Classical Transmission section the state of circuit after the second barrier was given by:
```math
\frac{|00\rangle}{2}\otimes(m_0|0\rangle+m_1|1\rangle)+
\frac{|01\rangle}{2}\otimes(m_1|0\rangle+m_0|1\rangle)+
\frac{|10\rangle}{2}\otimes(m_0|0\rangle-m_1|1\rangle)+
\frac{|11\rangle}{2}\otimes(-m_1|0\rangle+m_0|1\rangle)
```
This form looks a bit verbose and unmotivated.
These problems can be fixed by swapping the use of $m_0$ and $m_1$ with their average $\mu = \frac{m_0+m_1}{2}$ and split difference $\delta = \frac{m_0-m_1}{2}$.
The change is summarised in the following table:
| Z bit | X bit | Bob's $\|0\rangle$ | Bob's $\|1\rangle$ |
| --- | --- | --- | --- |
| 0 | 0 | $\mu+\delta$ | $\mu-\delta$ | 
| 0 | 1 | $\mu-\delta$ | $\mu+\delta$ |
| 1 | 0 | $\mu+\delta$ | $-\mu+\delta$ |
| 1 | 1 | $-\mu+\delta$ | $\mu+\delta$ |

Bob's coefficients are the sum of $\mu$ and $\delta$ with one $-$ thrown in depending on the bits.
This suggests we use the classic $(-1)^{XZ}$ trick to embed the table in a single function:
```math
	\left((-1)^{XZ}\mu+(-1)^{X(1-Z)}\delta\right)|0\rangle+\left((-1)^{(1-X)Z}\mu+(-1)^{(1-X)(1-Z)}\delta\right)|0\rangle
```
A bit more algebra gives:
```math
\sum_{(X,Z)\in\{0,1\}^2}\frac{(-1)^{XZ}|ZX\rangle}{2}\otimes\bigg(\big(\mu+(-1)^X\delta\big)|0\rangle+(-1)^Z\big(\mu-(-1)^X\delta\big)|1\rangle\bigg)
```
The $(-1)^{XZ}$ phase will be consumed by measurement so the remaining term right term of the $\otimes$ is what's important.
This term directly shows what operations we need,
remembering that the goal is to get back to:
```math
|\text{Message}\rangle = (\mu+\delta)|0\rangle + (\mu-\delta)|1\rangle
```
Hence if the X bit is set we need to swap the two coefficients,
the same as changing the sign in $\mu\pm\delta$,
and if the Z bit is set we need to swap the sign of $|1\rangle$.

These are the expected bits and operations from the previous sections but the state is more clearly motivated by these conditions and condense.

It can be argued which form is better,
as the new form is arguably more complex,
but I think this form is at least cool.
I think the key insight is that using $\mu\pm\delta$ lets us swap coefficients with a sign change,
something more directly related to manipulation with gates.
