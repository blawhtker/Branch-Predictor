import matplotlib.pyplot as plt
import sys
import os

# --- Import Logic ---
try:
    from sim import run_simulation
    print("Successfully imported simulator from sim.py")
except ImportError:
    print("Error: Could not find 'sim.py'.")
    print("Make sure this script is in the SAME FOLDER as your simulator code.")
    sys.exit(1)

def generate_graphs():
    # Make sure these trace files exist in your folder!
    traces = ["gobmk_trace.txt", "mcf_trace.txt"]
    
    print("--- Starting Simulations for Graphs ---")
    
    results_a = {t: [] for t in traces}
    results_b = {t: [] for t in traces}
    results_c = {t: [] for t in traces}
    
    # --- TASK A: Vary N (Fixed M=4) [cite: 93] ---
    print("Collecting Task A data...")
    x_axis_n = [1, 2, 3, 4]
    for trace in traces:
        for n in x_axis_n:
            rate = run_simulation(trace, 4, n)
            results_a[trace].append(rate)

    # --- TASK B: Vary M (Fixed N=4) [cite: 94] ---
    print("Collecting Task B data...")
    x_axis_m = [4, 5, 6, 7]
    for trace in traces:
        for m in x_axis_m:
            rate = run_simulation(trace, m, 4)
            results_b[trace].append(rate)

    # --- TASK C: Bimodal (N=0), Vary M [cite: 95] ---
    print("Collecting Task C data...")
    for trace in traces:
        for m in x_axis_m:
            rate = run_simulation(trace, m, 0)
            results_c[trace].append(rate)

    print("Simulations complete. Drawing plots...")

    # --- Plotting Task A ---
    plt.figure(figsize=(10, 6))
    for trace in traces:
        plt.plot(x_axis_n, results_a[trace], marker='o', label=trace)
    
    plt.title("Task A: Misprediction Rate vs. History Bits (N)\n(Fixed M=4)")
    plt.xlabel("N (Global History Bits)")
    plt.ylabel("Misprediction Rate")
    plt.xticks(x_axis_n)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.savefig("Task_A_Plot.png")
    print("Saved Task_A_Plot.png")
    plt.close()

    # --- Plotting Task B ---
    plt.figure(figsize=(10, 6))
    for trace in traces:
        plt.plot(x_axis_m, results_b[trace], marker='o', label=trace)

    plt.title("Task B: Misprediction Rate vs. Table Size (M)\n(Fixed N=4)")
    plt.xlabel("M (Table Index Bits)")
    plt.ylabel("Misprediction Rate")
    plt.xticks(x_axis_m)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.savefig("Task_B_Plot.png")
    print("Saved Task_B_Plot.png")
    plt.close()

    # --- Plotting Task C (Comparison) ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Subplot 1: gobmk
    if "gobmk_trace.txt" in traces:
        trace = "gobmk_trace.txt"
        ax1.plot(x_axis_m, results_b[trace], marker='o', label="Task B: Gshare (N=4)")
        ax1.plot(x_axis_m, results_c[trace], marker='x', linestyle='--', label="Task C: Bimodal (N=0)")
        ax1.set_title(f"Task C Comparison: {trace}")
        ax1.set_xlabel("M (Table Index Bits)")
        ax1.set_ylabel("Misprediction Rate")
        ax1.set_xticks(x_axis_m)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend()

    # Subplot 2: mcf
    if "mcf_trace.txt" in traces:
        trace = "mcf_trace.txt"
        ax2.plot(x_axis_m, results_b[trace], marker='o', label="Task B: Gshare (N=4)")
        ax2.plot(x_axis_m, results_c[trace], marker='x', linestyle='--', label="Task C: Bimodal (N=0)")
        ax2.set_title(f"Task C Comparison: {trace}")
        ax2.set_xlabel("M (Table Index Bits)")
        ax2.set_ylabel("Misprediction Rate")
        ax2.set_xticks(x_axis_m)
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()

    plt.tight_layout()
    plt.savefig("Task_C_Comparison.png")
    print("Saved Task_C_Comparison.png")
    plt.close()

if __name__ == "__main__":
    generate_graphs()
