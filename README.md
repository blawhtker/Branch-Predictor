The objective of this project was to design a simulator for a Gshare Global Branch Predictor.
Branch prediction allows processors to speculatively execute instructions before the outcome
of a conditional branch is known. The simulator models a predictor using a Pattern History
Table (PHT) of 2-bit saturating counters, indexed by an XOR combination of the Program
Counter (PC) and a Global History Register (GHR). The simulator accepts configurable
parameters for the number of PC index bits (M) and the Global History bits (N). The goal of this
simulation was to analyze the trade-offs between table size and history length. While also
observing how aliasing and capacity affect misprediction rates.
