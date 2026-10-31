# Empirical Performance Analysis of Hybrid Post-Quantum Cryptography

This repository contains the simulation scripts, benchmark datasets, and LaTeX source code for my undergraduate thesis. This research evaluates the performance and network behavior of hybrid cryptographic key exchange mechanisms under various constrained network profiles.

## Proposed Thesis Titles

1. Empirical Evaluation of Hybrid Classical and Post-Quantum Key Exchange Under Network Constraints
2. Performance Trade-offs of X25519 and ML-KEM-768 in Latency-Sensitive Network Environments
3. Benchmarking Post-Quantum Cryptographic Handshakes: Impact of ML-KEM-768 Ciphertext Overhead on Transport Latency

## Repository Structure

* `main.tex`: The primary LaTeX document for my thesis.
* `thesis_table.tex`: The generated LaTeX table containing performance metrics.
* `hybrid_performance_evaluation.pdf`: Generated visualization plotting mean latency against success rates.
* `simulate_network_transmission.py`: The simulation script I used to run network benchmarks.
* `thesis_benchmark_results.csv`: Raw experimental data exported from my simulations.

## Experimental Setup

My benchmark framework evaluates the hybrid cryptographic stack combining classical **X25519** and post-quantum **ML-KEM-768** across three distinct network profiles:
1. **Local Wi-Fi**: Low latency, minimal packet loss baseline.
2. **Standard 4G**: Moderate latency representing typical mobile network conditions.
3. **High-Latency / Lossy**: Elevated round-trip time and packet loss to observe fragmentation and failure behavior.

## Execution

To run the simulation and generate updated benchmark results locally:

```bash
python3 simulate_network_transmission.py