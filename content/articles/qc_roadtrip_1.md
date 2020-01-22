Title: Quantum Computing Roadtrip
Date: 2020-01-22 09:00
Modified: 2020-01-22 09:00
Category: misc
Tags: quantum computing, quantum mechanics, qubits, misc
Slug: quantumcomputing1
Authors: Ernek
Summary: Basics of Quantum Computing I. Tunneling through the learning curve

My intent with this post is to present some fundamental concepts related to Quantum Computing and document my learning experience. You can find several web reasources at the end of this post that I used to get accuanted with the field terminology and to understand the motivation behind the current funding resurgence towards this field. 
I am mostly covering elements of the first chapter of **'Quantum Computation and Quantum Information'** by Michael A. Nielsen and Isaac L. Chuang (know as the basic textbook for Quantum Computing)    

# Quantum Computing Conceptual Framework. 
# Basics I
## Quantum computation

*Quantum computation* refers to the implementation (or study) of computations --calculations, algorithms, programs-- employing quantum mechanical systems and their properties. 

## Qubits 

Let's start by giving a definition of a **qubit** (_**qu**antum **bit**_). You can get familiarized with the concept of a **qubit** entity using the following comparative statement:

> A **qubit** is the fundamental unit of _quantum computation_ (in the same way a **bit** is the fundamental unit of _classical computation_)

This means that **qubits** are the <ins>representation of the possible states</ins> a _quantum computer_ can use to perform computations.  

In classical computers, a **bit** represents two possibilities: either **0** or **1**. All classical computations are based on this binary representation and are excecuted by combining **bits** in very specific ways (i.e computer gates). Calculations and programming decisions (i.e True is 1 and False is 0) are ultimately a combination of **0**s and **1**s.  

In terms of hardware you can think of a **qubit** as the single physical entity able to generate _quantum states_ available for quantum computation.

However, if we separate ourselves from the hardware perspective, and think about the generation of _quantum states_, we can define a **qubit** more rigorously as:

> An _abstract mathematical object_ used to represent a given set of _quantum computing states_ with properties that comply with the rules of quantum mechanics.

The quantum analogy of the classical states **0** and **1**  would be the states **|0>** and **|1>** (ket notation).

