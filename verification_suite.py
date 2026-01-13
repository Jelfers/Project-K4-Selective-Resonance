import sys
import numpy as np

# ==============================================================================
# PROJECT V11.0: THE DYNAMIC STABILITY FILTER
# Filters transients to find the true "Zero Attractor" survivors.
# ==============================================================================

PRIME_MOD = 1_000_000_007
K_FACTOR = 4
BATCH_SIZE = 100_000
BURN_IN_STEPS = 2_000
TEST_CYCLES = 10      # 10 full loops (30 steps) for stability proof

def ascii_histogram(data, bins=25, width=60, title="Data"):
    # Text-only histogram visualization
    counts, bin_edges = np.histogram(data, bins=bins, density=True)
    max_count = np.max(counts) if len(counts) > 0 else 1
    print(f"\n[{title}]")
    print(f"   Spacing (s) | Density P(s)")
    print("-" * (width + 20))
    for i in range(len(counts)):
        bar_len = int((counts[i] / max_count) * width)
        bar = "#" * bar_len
        mid = (bin_edges[i] + bin_edges[i+1]) / 2
        print(f"   {mid:5.2f}       | {bar:<{width}} ({counts[i]:5.2f})")

def run_suite():
    print(f"--- INITIALIZING V11.0 DYNAMIC FILTER (N={BATCH_SIZE}) ---")
    
    # 1. SETUP
    w = (np.random.randint(0, 2**30, BATCH_SIZE) * 2 + 1).astype(np.int64)
    n = np.random.randint(1, PRIME_MOD, BATCH_SIZE).astype(np.int64)
    inv2 = pow(2, PRIME_MOD - 2, PRIME_MOD)
    
    # 2. BURN-IN
    print(">> Burning in 2000 steps...")
    for _ in range(BURN_IN_STEPS):
        is_odd = (w % 2 != 0)
        is_even = ~is_odd
        w[is_even] //= 2
        n[is_even] = (n[is_even] * inv2) % PRIME_MOD
        n_odd = n[is_odd]
        carry = (K_FACTOR * n_odd) // PRIME_MOD
        w[is_odd] = 3 * w[is_odd] + 1 + carry
        n[is_odd] = (K_FACTOR * n_odd) % PRIME_MOD

    # 3. DYNAMIC STABILITY TEST
    print(f">> Running {TEST_CYCLES * 3} steps to identify TRUE RESONANCE...")
    
    # Track who remains in the loop {1, 2, 4} for the entire duration
    stable_mask = np.isin(w, [1, 2, 4]) 
    
    # Snapshot for zero-drift verification
    n_start_test = n.copy()
    
    for step in range(TEST_CYCLES * 3):
        # Evolve
        is_odd = (w % 2 != 0)
        is_even = ~is_odd
        w[is_even] //= 2
        n[is_even] = (n[is_even] * inv2) % PRIME_MOD
        n_odd = n[is_odd]
        carry = (K_FACTOR * n_odd) // PRIME_MOD
        w[is_odd] = 3 * w[is_odd] + 1 + carry
        n[is_odd] = (K_FACTOR * n_odd) % PRIME_MOD
        
        # Filter: If you leave {1, 2, 4}, you are a transient.
        current_in_loop = np.isin(w, [1, 2, 4])
        stable_mask &= current_in_loop

    # 4. PARTITION RESULTS
    n_survivors = n[stable_mask]
    n_rejected = n[~stable_mask]
    
    print(f"\n[V11.0 RESULTS]")
    print(f"True Invariant Set (Zero Attractor): {len(n_survivors)} ({100*len(n_survivors)/BATCH_SIZE:.2f}%)")
    print(f"Transients (Infinity Repulsor):      {len(n_rejected)} ({100*len(n_rejected)/BATCH_SIZE:.2f}%)")
    
    # 5. SPECTRAL ANALYSIS
    if len(n_survivors) > 100:
        phases = np.sort(n_survivors / PRIME_MOD)
        spacings = np.diff(phases)
        norm_s = spacings / np.mean(spacings)
        
        near_zero_pct = 100 * np.sum(norm_s < 0.05) / len(norm_s)
        
        print(f"\n[SPECTRAL STATISTICS]")
        print(f"Near-Zero Spacings (<0.05): {near_zero_pct:.2f}%")
        print("Interpretation: High clustering indicates Resonance Zones.")
        
        ascii_histogram(norm_s, bins=20, title="Survivor Spectrum")
        
    # 6. VERIFYING "ZERO ATTRACTOR"
    survivor_start = n_start_test[stable_mask]
    survivor_end = n[stable_mask]
    
    deviations = np.sum(survivor_start != survivor_end)
    print(f"\n[ZERO ATTRACTOR CHECK]")
    print(f"Fiber Drifts detected in Survivors: {deviations}")
    
    if deviations == 0:
        print(">> VERDICT: ABSOLUTE ZERO. Perfect stability verified.")
    else:
        print(f">> VERDICT: {deviations} deviations detected.")

if __name__ == "__main__":
    run_suite()
