#!/usr/bin/env python3
"""
Paper 3 — S4.6 Posterior Table via Laplace Approximation
MLE + numerical Hessian → Gaussian credible intervals.
More reliable than poorly-converged MCMC.
"""
import numpy as np
from scipy.optimize import minimize
from scipy.stats import beta as betadist

# --- Calibration data (t >= -10000) ---
CAL_FULL = [
    (-70000, 0.5), (-50000, 1.0), (-30000, 2.0), (-25000, 3.34),
    (-15000, 4.0), (-10000, 5), (-8000, 5), (-5000, 5),
    (-3000, 14), (-2000, 27), (-1000, 50),
    (0, 170), (200, 190), (400, 190), (600, 200), (800, 250),
    (1000, 275), (1200, 360), (1340, 443), (1400, 350),
    (1500, 425), (1600, 545), (1700, 610),
    (1800, 954), (1900, 1634), (1950, 2527), (1970, 3700),
    (1980, 4440), (1990, 5320), (2000, 6140), (2010, 6960),
    (2020, 7840), (2024, 8100)
]
CAL = [(t, n) for t, n in CAL_FULL if t >= -10000]
t_obs = np.array([c[0] for c in CAL], dtype=float)
N_obs = np.array([c[1] for c in CAL], dtype=float)
log_N_obs = np.log10(N_obs)

sigma_obs = np.zeros(len(CAL))
for i, (t, _) in enumerate(CAL):
    if t >= 1800: sigma_obs[i] = 0.02
    elif t >= 0:  sigma_obs[i] = 0.15
    else:         sigma_obs[i] = 0.30

# Build observation map
obs_map = {}
for i, t in enumerate(t_obs):
    obs_map[int(round(t))] = i

def simulate_m4(theta):
    """Forward model with dt=1 for all t >= 1800, adaptive before."""
    a0, C, alpha, tc, x_on, x_off, L_floor, r_L = theta
    a0_eff = a0 * 1e6
    N = 5.0
    in_collapse = False
    log_N_pred = np.full(len(t_obs), np.nan)

    t = -10500.0
    while t <= 2025.0:
        # Adaptive dt: coarse for ancient, fine for modern
        if t < -5000:    dt = 20.0
        elif t < 0:      dt = 10.0
        elif t < 1800:   dt = 5.0
        elif t < 1950:   dt = 2.0
        else:            dt = 1.0

        t_int = int(round(t))
        if t_int in obs_map:
            log_N_pred[obs_map[t_int]] = np.log10(max(N, 0.01))

        dt_sing = max(tc - t, 0.1)
        VF = C * dt_sing**alpha
        K = 5.0 if t < -5000 else 1e12
        ceil = min(K, VF)

        ratio = N / max(VF, 0.01)
        if not in_collapse and ratio >= x_on:
            in_collapse = True
        if in_collapse and ratio <= x_off:
            in_collapse = False

        L_pop = 1.0
        if t >= 1963:
            L_pop = 1.0 - (1.0 - L_floor) * (1.0 - np.exp(-r_L * (t - 1963)))

        if not in_collapse:
            growth = a0_eff * N**2 * max(0, 1.0 - N / ceil) * L_pop
            N = max(N + growth * dt, 0.1)

        t += dt

    for i in range(len(log_N_pred)):
        if np.isnan(log_N_pred[i]):
            log_N_pred[i] = np.log10(max(N, 0.01))
    return log_N_pred

def neg_log_posterior(theta_vec):
    """Negative log-posterior for minimization. theta_vec is in transformed space."""
    # Transform back: log-space for positive params
    a0 = np.exp(theta_vec[0])
    C = np.exp(theta_vec[1])
    alpha = theta_vec[2]
    tc = theta_vec[3]
    x_on = theta_vec[4]
    x_off = theta_vec[5]
    L_floor_logit = theta_vec[6]
    L_floor = 1.0 / (1.0 + np.exp(-L_floor_logit))  # logit transform for (0,1)
    r_L = np.exp(theta_vec[7])

    theta = (a0, C, alpha, tc, x_on, x_off, L_floor, r_L)

    # Bounds check
    if alpha <= 0 or tc < 2015 or tc > 2040: return 1e10
    if x_on < 1.10 or x_on > 1.80: return 1e10
    if x_off < 0.90 or x_off > 1.15: return 1e10

    # Likelihood
    try:
        pred = simulate_m4(theta)
        if np.any(np.isnan(pred)): return 1e10
        ll = -0.5 * np.sum(((log_N_obs - pred) / sigma_obs)**2)
    except:
        return 1e10

    # Prior (in original space, need Jacobian for transformed)
    lp = 0.0
    lp += -0.5 * ((np.log(a0) - np.log(4.74e-12)) / np.log(2))**2
    lp += -0.5 * ((np.log(C) - np.log(1e5)) / 0.25)**2
    lp += -0.5 * ((alpha - 0.89) / 0.10)**2
    lp += -0.5 * ((tc - 2027) / 4)**2
    lp += -0.5 * ((x_on - 1.40) / 0.05)**2
    lp += -0.5 * ((x_off - 1.003) / 0.02)**2
    lp += betadist.logpdf(L_floor, 1.5, 3.5)
    lp += -0.5 * ((r_L - 0.03) / 0.015)**2

    # Jacobian for log/logit transforms
    lp += theta_vec[0]  # log(a0) -> a0
    lp += theta_vec[1]  # log(C) -> C
    lp += np.log(L_floor * (1 - L_floor))  # logit -> L_floor
    lp += theta_vec[7]  # log(r_L) -> r_L

    return -(ll + lp)

def transform_to_vec(theta):
    a0, C, alpha, tc, x_on, x_off, L_floor, r_L = theta
    return np.array([
        np.log(a0), np.log(C), alpha, tc, x_on, x_off,
        np.log(L_floor / (1 - L_floor)),  # logit
        np.log(r_L)
    ])

def transform_from_vec(v):
    return (np.exp(v[0]), np.exp(v[1]), v[2], v[3], v[4], v[5],
            1.0/(1.0+np.exp(-v[6])), np.exp(v[7]))

# MLE starting point
theta_mle = np.array([4.74e-12, 95525.0, 0.898, 2027.0, 1.40, 1.003, 0.30, 0.03])
v0 = transform_to_vec(theta_mle)

print("Finding MAP estimate...")
print(f"  Initial neg-log-post: {neg_log_posterior(v0):.2f}")

# Nelder-Mead first (robust), then Powell for refinement
res1 = minimize(neg_log_posterior, v0, method='Nelder-Mead',
                options={'maxiter': 20000, 'xatol': 1e-8, 'fatol': 1e-8})
print(f"  Nelder-Mead: {res1.fun:.2f}, success={res1.success}")

res2 = minimize(neg_log_posterior, res1.x, method='Powell',
                options={'maxiter': 20000, 'xtol': 1e-10, 'ftol': 1e-10})
print(f"  Powell: {res2.fun:.2f}, success={res2.success}")

v_map = res2.x
theta_map = transform_from_vec(v_map)

print(f"\nMAP estimate (original space):")
pn = ['a_0', 'C', 'alpha', 't_c', 'x_on', 'x_off', 'L_floor', 'r_L']
for j, name in enumerate(pn):
    print(f"  {name}: {theta_map[j]:.6g}")

# Numerical Hessian at MAP
print("\nComputing Hessian (numerical)...")
ndim = len(v_map)
eps = 1e-5
H = np.zeros((ndim, ndim))
f0 = neg_log_posterior(v_map)

for i in range(ndim):
    for j in range(i, ndim):
        v_pp = v_map.copy(); v_pp[i] += eps; v_pp[j] += eps
        v_pm = v_map.copy(); v_pm[i] += eps; v_pm[j] -= eps
        v_mp = v_map.copy(); v_mp[i] -= eps; v_mp[j] += eps
        v_mm = v_map.copy(); v_mm[i] -= eps; v_mm[j] -= eps
        H[i,j] = (neg_log_posterior(v_pp) - neg_log_posterior(v_pm)
                 - neg_log_posterior(v_mp) + neg_log_posterior(v_mm)) / (4*eps*eps)
        H[j,i] = H[i,j]

# Covariance = inverse Hessian
try:
    cov = np.linalg.inv(H)
    se_vec = np.sqrt(np.diag(cov))
    print("  Hessian inversion successful")
    hessian_ok = True
except np.linalg.LinAlgError:
    print("  Hessian singular! Using diagonal approximation")
    se_vec = np.zeros(ndim)
    for i in range(ndim):
        vi_p = v_map.copy(); vi_p[i] += eps
        vi_m = v_map.copy(); vi_m[i] -= eps
        d2 = (neg_log_posterior(vi_p) - 2*f0 + neg_log_posterior(vi_m)) / eps**2
        se_vec[i] = 1.0/np.sqrt(max(d2, 1e-30))
    hessian_ok = False

# Convert to original-space CIs via delta method / sampling
print("\nGenerating posterior samples from Laplace approximation...")
rng = np.random.RandomState(42)
n_samples = 50000
if hessian_ok:
    samples_vec = rng.multivariate_normal(v_map, cov, size=n_samples)
else:
    samples_vec = v_map + rng.normal(0, 1, (n_samples, ndim)) * se_vec

# Transform all samples to original space
samples_orig = np.zeros((n_samples, ndim))
for s in range(n_samples):
    samples_orig[s] = transform_from_vec(samples_vec[s])

# Compute quantiles
print("\n" + "="*90)
print(f"{'Param':<12} {'MAP':>14} {'5%':>14} {'95%':>14} {'Prior_mean':>14}")
print("-"*90)

prior_means = [4.74e-12, 1e5, 0.89, 2027, 1.40, 1.003, 0.273, 0.03]  # Beta(1.5,3.5) mean=0.273

for j in range(ndim):
    m = theta_map[j]
    q5 = np.percentile(samples_orig[:,j], 5)
    q95 = np.percentile(samples_orig[:,j], 95)
    pm = prior_means[j]
    if j == 0:
        print(f"{pn[j]:<12} {m:>14.3e} {q5:>14.3e} {q95:>14.3e} {pm:>14.3e}")
    elif j == 1:
        print(f"{pn[j]:<12} {m:>14.0f} {q5:>14.0f} {q95:>14.0f} {pm:>14.0f}")
    else:
        print(f"{pn[j]:<12} {m:>14.4f} {q5:>14.4f} {q95:>14.4f} {pm:>14.4f}")

# Check prior-vs-posterior shift
print("\n--- Prior vs Posterior shift (|MAP - prior_mean| / prior_sd) ---")
prior_sds = [4.74e-12*np.log(2)/1, 1e5*0.25/1, 0.10, 4.0, 0.05, 0.02, 0.15, 0.015]
for j in range(ndim):
    if j == 0:
        shift = abs(np.log(theta_map[j]) - np.log(prior_means[j])) / np.log(2)
    elif j == 1:
        shift = abs(np.log(theta_map[j]) - np.log(prior_means[j])) / 0.25
    else:
        shift = abs(theta_map[j] - prior_means[j]) / prior_sds[j]
    label = "data-identified" if shift > 0.5 else "prior-dominated"
    print(f"  {pn[j]:<12}: shift = {shift:.2f} sigma  [{label}]")

# Likelihood at MAP
pred_map = simulate_m4(theta_map)
ll_map = -0.5 * np.sum(((log_N_obs - pred_map) / sigma_obs)**2)
print(f"\nLog-likelihood at MAP: {ll_map:.2f}")
print(f"Residual RMSE (log10 scale): {np.sqrt(np.mean((log_N_obs - pred_map)**2)):.4f}")

# Bayes factor from Laplace
bic = -2*ll_map + ndim*np.log(len(t_obs))
bic_null = -2*0 + 0  # null model: no parameters, LL=sum of log(1/sigma)... simplified
print(f"BIC (M4): {bic:.1f}")
print(f"Laplace BF from ΔBIC=14.2: log10(BF) = {14.2/(2*np.log(10)):.2f}")

# Save results
od = '/sessions/dazzling-epic-sagan/mnt/CoWork_加藤方程式/Paper3専用_4回目作業用_出力はここだけにしろ'
with open(f'{od}/laplace_m4_posterior_results.txt', 'w') as f:
    f.write("M4 Bayesian Posterior Summary (Laplace Approximation)\n")
    f.write("MAP + Hessian-based Gaussian CIs, 50000 posterior samples\n")
    f.write("Priors: S4.6 weakly informative\n\n")
    f.write(f"{'Param':<12} {'MAP':>14} {'5%':>14} {'95%':>14}\n")
    f.write("-"*60 + "\n")
    for j in range(ndim):
        m = theta_map[j]
        q5 = np.percentile(samples_orig[:,j], 5)
        q95 = np.percentile(samples_orig[:,j], 95)
        if j == 0:
            f.write(f"{pn[j]:<12} {m:>14.3e} {q5:>14.3e} {q95:>14.3e}\n")
        elif j == 1:
            f.write(f"{pn[j]:<12} {m:>14.0f} {q5:>14.0f} {q95:>14.0f}\n")
        else:
            f.write(f"{pn[j]:<12} {m:>14.4f} {q5:>14.4f} {q95:>14.4f}\n")
    f.write(f"\nLog-likelihood at MAP: {ll_map:.2f}\n")
    f.write(f"Residual RMSE: {np.sqrt(np.mean((log_N_obs - pred_map)**2)):.4f}\n")
    f.write(f"Bayes factor (Laplace from ΔBIC=14.2): log10(BF)≈{14.2/(2*np.log(10)):.2f}, BF≈{10**(14.2/(2*np.log(10))):.0f}\n")

print(f"\nSaved to {od}/laplace_m4_posterior_results.txt")
