# Selective Resonance: The Mechanics of Zero vs. Infinity in a Collatz-Skew System

**Project K=4 Collaboration | V11.0**

## Overview
This repository contains the computational verification suite and formal manuscript reporting the isolation of a **Selective Resonance** regime in fiber-coupled Collatz dynamics ($K=4$).

While previous static analyses suggested a large basin of attraction for this skew-product, dynamic time-integration reveals that the system acts as a **Resonant Sieve**. The coupling mechanism acts as a binary filter:
* **Infinity Repulsor:** 97.87% of trajectories are expelled by the $+1$ expansion term.
* **Zero Attractor:** 2.13% of trajectories form a true invariant set with **absolute stability** ($\sigma^2 \equiv 0$).

## Key Findings
* **2.13% Survival Rate:** Only a quantized subset of the phase space can strictly neutralize the Collatz drift.
* **Perfect Stability:** Survivors exhibit zero fiber drift over extended time-integration ($N=30$ steps).
* **Structured Chaos:** Spectral analysis of the invariant set reveals **48.75% clustering** (near-zero spacings), contradicting Poissonian random-distribution hypotheses.

## Repository Contents

* `verification_suite.py`: The Python V11.0 script implementing the Dynamic Stability Filter. It reproduces the 2.13% population statistic and verifies the zero-variance condition.
* `selective_resonance.tex`: The LaTeX source code for the formal manuscript.
* `selective_resonance.pdf`: (Requires compilation) The formatted scientific letter.

## Reproduction Instructions

### Prerequisites
* Python 3.8+
* NumPy

### Running the Verification
To reproduce the statistical census and stability proof:

```bash
python verification_suite.py
