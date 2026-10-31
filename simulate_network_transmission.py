import pandas as pd
import numpy as np
# Import the function from your existing file
from hybrid_exchange import run_hybrid_handshake_simulation

# Now you can run it without a NameError!
profile = "Standard 4G"
res = run_hybrid_handshake_simulation(network_profile=profile)
print("Simulation Result:", res)
# Define the network profiles you want to test for your thesis evaluation
profiles = ["Local Wi-Fi", "Standard 4G", "High-Latency / Lossy"]
iterations = 100  # Number of test runs per profile

benchmark_results = []

print("Running empirical performance benchmarks across network profiles...")

for profile in profiles:
    success_count = 0
    failure_count = 0
    latencies = []
    
    for _ in range(iterations):
        res = run_hybrid_handshake_simulation(network_profile=profile)
        if res["status"] == "Success":
            success_count += 1
            latencies.append(res["total_time_ms"])
        else:
            failure_count += 1
            
    # Calculate statistical metrics for the thesis table
    avg_latency = np.mean(latencies) if latencies else 0
    std_latency = np.std(latencies) if latencies else 0
    p95_latency = np.percentile(latencies, 95) if latencies else 0
    
    benchmark_results.append({
        "Network Profile": profile,
        "Iterations": iterations,
        "Success Rate (%)": (success_count / iterations) * 100,
        "Mean Latency (ms)": round(avg_latency, 2),
        "Std Dev (ms)": round(std_latency, 2),
        "95th Percentile (ms)": round(p95_latency, 2),
        "Msg2 Size (bytes)": 1120
    })

# Convert results into a clean Pandas DataFrame (ideal for thesis tables and plotting)
df_results = pd.DataFrame(benchmark_results)
print(df_results)

import matplotlib.pyplot as plt

# 1. Save raw data to CSV for record keeping
df_results.to_csv('thesis_benchmark_results.csv', index=False)

# 2. Automatically generate LaTeX table code and save it to a file
latex_table_code = df_results.to_latex(
    index=False, 
    caption="Empirical performance metrics of hybrid X25519 and ML-KEM-768 handshakes across varied network profiles.", 
    label="tab:hybrid_benchmarks"
)
with open('thesis_table.tex', 'w') as f:
    f.write(latex_table_code)

print("Exported: thesis_benchmark_results.csv, thesis_table.tex")

# 3. Re-generate and save your graph as a vector PDF (ideal for LaTeX clarity)
fig, ax1 = plt.subplots(figsize=(9, 5))

profiles = df_results["Network Profile"]
mean_latencies = df_results["Mean Latency (ms)"]
success_rates = df_results["Success Rate (%)"]

color = '#2b5c8f'
ax1.set_xlabel('Network Profile', fontweight='bold', fontsize=11)
ax1.set_ylabel('Mean Latency (ms)', color=color, fontweight='bold', fontsize=11)
ax1.bar(profiles, mean_latencies, color=color, alpha=0.85, width=0.4)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim(0, max(mean_latencies) * 1.3)

ax2 = ax1.twinx()
color_line = '#d95f02'
ax2.set_ylabel('Success Rate (%)', color=color_line, fontweight='bold', fontsize=11)
ax2.plot(profiles, success_rates, color=color_line, marker='o', linewidth=2.5, markersize=8)
ax2.tick_params(axis='y', labelcolor=color_line)
ax2.set_ylim(50, 105)

plt.title('Hybrid Key Exchange Performance (X25519 + ML-KEM-768)', fontsize=13, fontweight='bold', pad=15)
fig.tight_layout()

# Save as PDF for your LaTeX thesis project
plt.savefig('hybrid_performance_evaluation.pdf', bbox_inches='tight')
plt.show()
print("Exported: hybrid_performance_evaluation.pdf")