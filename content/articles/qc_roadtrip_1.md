Title: Quantum Computing Roadtrip
Date: 2020-01-22 09:00
Modified: 2020-01-22 09:00
Category: misc
Tags: quantum computing, quantum mechanics, qubits, misc
Slug: quantumcomputing1
Authors: Ernek
Summary: Basics of Quantum Computing I. Tunneling through the learning curve

My intent with this post is to present some fundamental concepts related to Quantum Computing and document my learning experience. You can find several web resources —which I used to get acquainted with the field terminology and to understand the motivation behind the current funding resurgence towards this field— at the end of this post. 
I am mostly covering elements of the first chapter of **'Quantum Computation and Quantum Information'** by Michael A. Nielsen and Isaac L. Chuang (known as the basic textbook for Quantum Computing) 

$E = mc^2$

# Quantum Computing Conceptual Framework. 
# Basics I
## Quantum computation

*Quantum computation* refers to the implementation (or study) of computations --calculations, algorithms, programs-- employing quantum mechanical systems and their properties. 

## Qubits 

Let's start by giving a definition of a **qubit** (**_qu_**_antum_ **_bit_**). You can get familiarized with the concept of a **qubit** entity using the following comparative statement:

> A **qubit** is the fundamental unit of _quantum computation_ (in the same way a **bit** is the fundamental unit of _classical computation_)

This means that **qubits** are the <ins>representation of the possible states</ins> a _quantum computer_ can use to perform computations.  

In classical computers, a **bit** represents two possibilities: either **0** or **1**. All classical computations are based on this binary representation and are excecuted by combining **bits** in very specific ways (i.e computer gates). Calculations and programming decisions (i.e 1 is True and 0 equals False) are ultimately a combination of **0**s and **1**s.  

In terms of hardware you can think of a **qubit** as the single physical entity able to generate _quantum states_ available for quantum computation.

However, if we separate ourselves from the hardware perspective, and think about the generation of _quantum states_, we can define a **qubit** more rigorously as:

> An _abstract mathematical object_ used to represent a given set of _quantum computing states_ with properties that comply with the rules of quantum mechanics.

The quantum analogy of the classical states **0** and **1**  would be the states **|0>** and **|1>** respectively (ket notation).
The difference between **bits** and **qubits** is that 
> **qubits** can be in a _state_ other than |0> and |1>. They can also be in any possible _linear combination_ of these two states:
>
> <p style="text-align: center;"> ![superposition state]({static}/images/superposition.png),</p> 
>
> with ![alpha]({static}/images/alpha.png) and ![beta]({static}/images/beta.png) interrelated by the normalization relationship: ![normalization relationship]({static}/images/norm_coefficients.png)        

In other words, the _state_ of a qubit is a vector in a two-dimensional complex vector space. 

The special states **0** and **1** are known as _computational basis states_, and form a orthonormal basis for this vector space. 

To adquire information about the qubit state we need to measure it. When we measure a qubit we obtain one of the two fundamental states |0> or |1>. We get either 0, with probability ![alpha_squared]({static}/images/alpha_2.png), or the result 1, with probability ![beta_squared]({static}/images/beta_2.png).

A **Bloch Sphere** is nice visual representation of the possible states and allowed transformations of single qubits:

<p style="text-align: center;"> <img src="{static}/images/blochsphere.png" width="400"> </p>