#!/usr/bin/env python3
"""
Paper 3 — S4.6 MCMC Posterior Table (FINAL)
Optimized forward model + long chains.
"""
import numpy as np
from scipy.stats import beta as betadist
import time, sys

CAL = [
    (-10000,5),(-8000,5),(-5000,5),(-3000,14),(-2000,27),(-1000,50),
    (0,170),(200,190),(400,190),(600,200),(800,250),
    (1000,275),(1200,360),(1340,443),(1400,350),
    (1500,425),(1600,545),(1700,610),
    (1800,954),(1900,1634),(1950,2527),(1970,3700),
    (1980,4440),(1990,5320),(2000,6140),(2010,6960),
    (2020,7840),(2024,8100)
]
t_obs = np.array([c[0] for c in CAL], dtype=float)
N_obs = np.array([c[1] for c in CAL], dtype=float)
log_N_obs = np.log10(N_obs)
sigma_obs = np.zeros(len(CAL))
for i, (t, _) in enumerate(CAL):
    if t >= 1800:   sigma_obs[i] = 0.02
    elif t >= 0:    sigma_obs[i] = 0.15
    else:           sigma_obs[i] = 0.30

# Pre-1800 obs indices (for which sigma is large, LL contribution is small)
# Post-1800 obs indices (sigma=0.02, dominate LL)
obs_post1800 = [i for i,(t,_) in enumerate(CAL) if t >= 1800]

# Optimized: first 3 points (-10000, -8000, -5000) are always N=5
# Integrate from t=-5000 only
obs_from_m5k = [(i,int(round(t))) for i,(t,_) in enumerate(CAL) if t >= -5000]
obs_set_m5k = set(tt for _,tt in obs_from_m5k if tt > -5000)
obs_map_m5k = {tt:i for i,tt in obs_from_m5k if tt > -5000}

R_BASE = 5e-4

def simulate_m4_fast(theta):
    a0, C, alpha, tc, x_on, x_off, L_floor, r_L = theta
    a0_eff = a0 * 1e6
    log_N_pred = np.empty(len(t_obs))
    # First 3 points: N=5 always
    log_N_pred[0] = log_N_pred[1] = log_N_pred[2] = np.log10(5.0)

    N = 5.0; in_collapse = False
    for t_int in range(-5000, 2026):
        if t_int in obs_set_m5k:
            log_N_pred[obs_map_m5k[t_int]] = np.log10(max(N, 0.01))
        t = float(t_int)
        dt_sing = max(tc - t, 0.1)
        VF = C * dt_sing**(-alpha)
        ratio = N / max(VF, 0.01)
        if not in_collapse and ratio >= x_on: in_collapse = True
        if in_collapse and ratio <= x_off: in_collapse = False
        if not in_collapse:
            L_pop = 1.0
            if t >= 1963:
                L_pop = 1.0 - (1.0 - L_floor) * (1.0 - np.exp(-r_L * (t - 1963)))
            growth = (R_BASE * N + a0_eff * N * N) * L_pop
            N = N + growth
            if N < 0.1: N = 0.1
    return log_N_pred

def log_likelihood(theta):
    try:
        pred = simulate_m4_fast(theta)
        if np.any(np.isnan(pred)): return -1e10
        return -0.5 * np.sum(((log_N_obs - pred) / sigma_obs)**2)
    except: return -1e10

def log_prior(theta):
    a0, C, alpha, tc, x_on, x_off, L_floor, r_L = theta
    if a0 <= 0 or C <= 0 or alpha <= 0 or r_L <= 0: return -1e10
    if L_floor <= 0 or L_floor >= 1: return -1e10
    if tc < 2020 or tc > 2034: return -1e10
    if x_on < 1.20 or x_on > 1.70: return -1e10
    if x_off < 0.95 or x_off > 1.10: return -1e10
    lp = 0.0
    lp += -0.5*((np.log(a0)-np.log(4.74e-12))/np.log(2))**2
    lp += -0.5*((np.log(C)-np.log(1e5))/0.25)**2
    lp += -0.5*((alpha-0.89)/0.10)**2
    lp += -0.5*((tc-2027)/4)**2
    lp += -0.5*((x_on-1.40)/0.05)**2
    lp += -0.5*((x_off-1.003)/0.02)**2
    lp += betadist.logpdf(L_floor, 1.5, 3.5)
    lp += -0.5*((r_L-0.03)/0.015)**2
    return lp

def log_posterior(theta):
    return log_prior(theta) + log_likelihood(theta)

def run_mcmc(theta0, n_warmup, n_sample, seed):
    rng = np.random.RandomState(seed)
    scales = np.array([
        4.74e-12*0.003, 1e5*0.002, 0.0008, 0.06,
        0.0005, 0.0002, 0.003, 0.0004
    ])
    n_total = n_warmup + n_sample
    chain = np.zeros((n_total, 8))
    lp_arr = np.zeros(n_total)
    chain[0] = theta0.copy()
    lp_arr[0] = log_posterior(theta0)
    acc = 0; acc_w = 0

    for i in range(1, n_total):
        prop = chain[i-1] + rng.normal(0, scales)
        lp = log_posterior(prop)
        if np.log(rng.uniform()) < (lp - lp_arr[i-1]):
            chain[i]=prop; lp_arr[i]=lp; acc+=1; acc_w+=1
        else:
            chain[i]=chain[i-1].copy(); lp_arr[i]=lp_arr[i-1]
        if i < n_warmup and i % 300 == 0:
            r = acc_w / 300
            if r < 0.20: scales *= 0.80
            elif r > 0.35: scales *= 1.20
            acc_w = 0
        if i % 5000 == 0:
            ph = "WU" if i<n_warmup else "SA"
            print(f"    [{ph}] {i}/{n_total}, acc={acc/i:.3f}", flush=True)
    rate = acc/n_total
    print(f"  Final accept: {rate:.3f}", flush=True)
    return chain[n_warmup:], rate

# ============================================================
print("="*70, flush=True)
print("M4 MCMC FINAL (optimized, 4 x 5k+20k)", flush=True)
print("="*70, flush=True)

theta_mle = np.array([4.74e-12, 95525.0, 0.898, 2027.0, 1.40, 1.003, 0.30, 0.03])
t0=time.time(); ll_mle=log_likelihood(theta_mle); dt_e=time.time()-t0
print(f"MLE LL: {ll_mle:.2f} ({dt_e:.4f}s/eval)", flush=True)

chains=[]; accept_rates=[]; t_start=time.time()
for c in range(4):
    print(f"\nChain {c+1}/4...", flush=True)
    rng=np.random.RandomState(c*111+42)
    t0=theta_mle.copy()
    t0[0]*=np.exp(rng.normal(0,0.06)); t0[1]*=np.exp(rng.normal(0,0.03))
    t0[2]+=rng.normal(0,0.012); t0[3]+=rng.normal(0,0.6)
    t0[4]+=rng.normal(0,0.006); t0[5]+=rng.normal(0,0.002)
    t0[6]=np.clip(t0[6]+rng.normal(0,0.03),0.05,0.95)
    t0[7]=max(t0[7]+rng.normal(0,0.004),0.001)
    s,ar=run_mcmc(t0, n_warmup=5000, n_sample=20000, seed=c*111+42)
    chains.append(s); accept_rates.append(ar)

elapsed=time.time()-t_start
print(f"\nTotal: {elapsed:.1f}s ({elapsed/60:.1f}min)", flush=True)

all_s=np.vstack(chains)  # 80000 total

def gelman_rubin(chs):
    m=len(chs);n=len(chs[0])
    cm=np.array([np.mean(c,0) for c in chs])
    cv=np.array([np.var(c,0,ddof=1) for c in chs])
    B=n*np.var(cm,0,ddof=1);W=np.mean(cv,0)
    return np.sqrt(((1-1/n)*W+B/n)/np.maximum(W,1e-30))

R_hat=gelman_rubin(chains)

def compute_ess(s):
    n=len(s)
    if n<10:return float(n)
    v=np.var(s)
    if v<1e-30:return float(n)
    m=np.mean(s);c=s-m
    ml=min(n//2,1000)
    ac=np.array([np.mean(c[:n-l]*c[l:])/v for l in range(ml)])
    tau=1.0
    for k in range(1,ml-1,2):
        p=ac[k]+ac[k+1]
        if p<0:break
        tau+=2*p
    return max(1.0,n/max(tau,1.0))

ess=np.array([compute_ess(all_s[:,j]) for j in range(8)])
pn=['a_0','C','alpha','t_c','x_on','x_off','L_floor','r_L']

print("\n"+"="*95, flush=True)
print(f"{'Param':<12} {'Median':>14} {'5%':>14} {'95%':>14} {'R-hat':>8} {'ESS':>8}", flush=True)
print("-"*95, flush=True)
for j in range(8):
    m=np.median(all_s[:,j]);q5=np.percentile(all_s[:,j],5);q95=np.percentile(all_s[:,j],95)
    if j==0:print(f"{pn[j]:<12} {m:>14.3e} {q5:>14.3e} {q95:>14.3e} {R_hat[j]:>8.3f} {ess[j]:>8.0f}",flush=True)
    elif j==1:print(f"{pn[j]:<12} {m:>14.0f} {q5:>14.0f} {q95:>14.0f} {R_hat[j]:>8.3f} {ess[j]:>8.0f}",flush=True)
    else:print(f"{pn[j]:<12} {m:>14.4f} {q5:>14.4f} {q95:>14.4f} {R_hat[j]:>8.3f} {ess[j]:>8.0f}",flush=True)

rhat_ok=np.all(R_hat<1.05);ess_ok=np.all(ess>400)
print(f"\nR-hat<1.05: {'PASS' if rhat_ok else 'FAIL'} (max={np.max(R_hat):.3f})", flush=True)
print(f"ESS>400: {'PASS' if ess_ok else 'FAIL'} (min={np.min(ess):.0f})", flush=True)

delta_bic=14.2;log10_BF=delta_bic/(2*np.log(10));BF=10**log10_BF

outdir='CoWork_加藤方程式/Paper3専用_4回目作業用_出力はここだけにしろ'
with open(f'{outdir}/mcmc_m4_posterior_results.txt','w',encoding='utf-8') as f:
    f.write("M4 Bayesian Posterior Summary (S4.6)\n")
    f.write("="*60+"\n")
    f.write("Model: dN/dt = (1-C(t))*(r*N + a0*N^2)*L_pop\n")
    f.write("  VF = C*(tc-t)^{-alpha}, r_base = 5e-4 (fixed)\n")
    f.write("  Collapse: frozen when N/VF >= x_on, release when <= x_off\n")
    f.write("Sampler: Metropolis-Hastings (diagonal, adaptive warmup)\n")
    f.write(f"4 chains x 5000 warmup + 20000 post-warmup\n")
    f.write(f"Forward model: dt=1yr, N0=5M at t=-5000 (=K_HG)\n")
    f.write(f"28-point calibration (-10000 BCE to 2024 CE)\n")
    f.write(f"Priors: S4.6 weakly informative\n")
    f.write(f"Total MCMC time: {elapsed:.1f}s\n")
    f.write(f"MLE log-likelihood: {ll_mle:.2f}\n\n")
    f.write(f"{'Parameter':<12} {'Median':>14} {'5%':>14} {'95%':>14} {'R-hat':>8} {'ESS':>8}\n")
    f.write("-"*80+"\n")
    for j in range(8):
        m=np.median(all_s[:,j]);q5=np.percentile(all_s[:,j],5);q95=np.percentile(all_s[:,j],95)
        if j==0:f.write(f"{pn[j]:<12} {m:>14.3e} {q5:>14.3e} {q95:>14.3e} {R_hat[j]:>8.3f} {ess[j]:>8.0f}\n")
        elif j==1:f.write(f"{pn[j]:<12} {m:>14.0f} {q5:>14.0f} {q95:>14.0f} {R_hat[j]:>8.3f} {ess[j]:>8.0f}\n")
        else:f.write(f"{pn[j]:<12} {m:>14.4f} {q5:>14.4f} {q95:>14.4f} {R_hat[j]:>8.3f} {ess[j]:>8.0f}\n")
    f.write(f"\nAccept rates: {[f'{ar:.3f}' for ar in accept_rates]}\n")
    f.write(f"R-hat<1.05: {'PASS' if rhat_ok else 'FAIL'} (max={np.max(R_hat):.3f})\n")
    f.write(f"ESS>400: {'PASS' if ess_ok else 'FAIL'} (min={np.min(ess):.0f})\n")
    f.write(f"\nBayes factor (Laplace approx from ΔBIC=14.2):\n")
    f.write(f"  log10(BF) ≈ {log10_BF:.2f}\n")
    f.write(f"  BF ≈ {BF:.0f}\n")
print(f"\nSaved to {outdir}/mcmc_m4_posterior_results.txt", flush=True)

np.savez(f'{outdir}/mcmc_m4_chains.npz',
         chain0=chains[0],chain1=chains[1],chain2=chains[2],chain3=chains[3],
         all_samples=all_s,param_names=pn,R_hat=R_hat,ESS=ess,
         accept_rates=np.array(accept_rates))
print(f"Saved chains to {outdir}/mcmc_m4_chains.npz", flush=True)
print("Done.", flush=True)
