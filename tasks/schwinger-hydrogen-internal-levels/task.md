---
schema_version: '1.3'
metadata:
  author_name: AlienTu
  author_email: 149789160+AlienTu@users.noreply.github.com
  difficulty: hard
  category: natural-science
  subcategory: quantum-field-theory
  category_confidence: high
  task_type:
  - analysis
  - calculation
  - simulation
  modality:
  - scientific-data
  - json
  - csv
  interface:
  - terminal
  - python
  skill_type:
  - domain-procedure
  - mathematical-method
  - library-api-usage
  tags:
  - theoretical-physics
  - quantum-electrodynamics
  - schwinger-model
  - bound-states
  - spectral-analysis
verifier:
  type: test-script
  timeout_sec: 900.0
  service: main
  pytest_plugins:
  - ctrf
  hardening:
    cleanup_conftests: true
agent:
  timeout_sec: 7200.0
environment:
  network_mode: none
  build_timeout_sec: 1200.0
  os: linux
  cpus: 4
  memory_mb: 8192
  storage_mb: 10240
  gpus: 0
---

Determine whether a hydrogen-like atom in one-flavour massive QED in \(1+1\)
dimensions has localized internal energy levels at leading semiclassical order.
The atom consists of one infinitely heavy external charge \(+e\) fixed at the
origin and the dynamical Dirac field of charge \(-e\) and mass \(m\) that
screens it. Work at \(\theta=0\) on the infinite line.

Use \(\mu=e/\sqrt{\pi}\) as the unit of energy and \(\xi=\mu x\) as the
dimensionless coordinate. Coleman normal ordering is fixed at \(\mu\). For
avoidance of convention ambiguity, the continuum effective Hamiltonian that
defines the requested leading-semiclassical observable is

\[
\frac{\mathcal H}{\mu^2}
=\frac{1}{8\pi}\left[
  \Pi_\varphi^2+(\partial_\xi\varphi)^2+
  \bigl(\varphi+2\pi\Theta(\xi)\bigr)^2
\right]
+\frac{e^\gamma}{2\sqrt{\pi}}\frac{m}{e}
 \left(1-\cos\varphi\right),
\]

where \(\gamma\) is Euler's constant and \(\Theta(0)=1/2\). The screened
ground-state sector obeys
\(\varphi(-\infty)=0\) and \(\varphi(+\infty)=-2\pi\).
An internal level means a normalizable neutral excitation about the
lowest-energy screened static state whose positive frequency lies strictly
below the infinite-volume continuum threshold. Do not count negative modes,
zero modes, or finite-box discretizations of the continuum.

Evaluate the spectrum for

\[
m/e \in \{0.05,\;0.10,\;0.25,\;0.50,\;1.00\}.
\]

Use an infinite-volume extrapolation or a sufficiently documented convergence
study so that every reported frequency and continuum threshold is accurate to
three significant figures. You may use any valid analytical or numerical
method.

Write `/root/atom_spectrum.json` with this exact top-level structure:

```json
{
  "energy_unit": "mu=e/sqrt(pi)",
  "classification": "localized-internal-levels-present or no-localized-internal-levels",
  "levels": [
    {
      "mass_over_e": 0.05,
      "continuum_threshold_mu": 0.0,
      "bound_state_count": 0,
      "bound_frequencies_mu": [],
      "lowest_binding_gap_mu": 0.0
    }
  ]
}
```

Include exactly one `levels` entry for each requested mass ratio, in increasing
order. Frequencies must be positive and sorted. Define
`lowest_binding_gap_mu` as the continuum threshold minus the lowest bound
frequency, or `0.0` if no bound state exists. Set `classification` to
`localized-internal-levels-present` if at least one requested parameter point
has an internal level.

Also write `/root/screening_profile.csv` for \(m/e=0.25\). It must contain the
header

```text
xi,phi,electric_field_over_e
```

and exactly 601 data rows at \(\xi=-12.00,-11.96,\ldots,12.00\). Here

\[
\frac{E(\xi)}{e} =
\frac{\varphi(\xi)+2\pi\Theta(\xi)}{2\pi}.
\]

Finally, write `/root/method.md` describing the physical criterion used to
separate localized levels from the continuum and a numerical convergence
check. The scientific values, rather than the choice of method or software,
will be graded.
