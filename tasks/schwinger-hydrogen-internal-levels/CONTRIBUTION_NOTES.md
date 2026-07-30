# Contribution notes — author review required

This package is a technical draft for a FrontierPhysics contribution. The
scientific task was developed from the contributor's research question about
the weak-mass internal spectrum of a screened external charge in the massive
Schwinger model. Before opening the upstream pull request, the contributor
must personally review the prompt and oracle as needed to satisfy
FrontierPhysics's human-authorship policy.

## Scientific provenance

The task asks whether a screened heavy-light bound state in
\(1+1\)-dimensional QED supports a localized neutral excitation and determines
the first two nonzero terms of its weak-\(m/e\) binding curve. The continuum
convention is the Coleman-normal-ordered massive Schwinger model at
normal-ordering mass \(g=e/\sqrt{\pi}\), with
\(\kappa^2=e^\gamma m g/\pi\). No external dataset is used.

Relevant primary sources to cite in the pull request:

- S. Coleman, “More About the Massive Schwinger Model,” *Annals of Physics*
  **101**, 239–267 (1976), DOI: 10.1016/0003-4916(76)90280-3.
- J. Schwinger, “Gauge Invariance and Mass. II,” *Physical Review* **128**,
  2425–2429 (1962), DOI: 10.1103/PhysRev.128.2425.

## Pull-request history table

Replace every bracketed item with truthful first-person information.

| Report | Contributor statement |
|---|---|
| Project time scale — start and end date | [YYYY-MM-DD to YYYY-MM-DD] |
| Actual working hours spent exploring the task | [honest total; minimum 40 hours] |
| Estimated hours for a first-year PhD to reproduce the results | [honest estimate; minimum 10 hours] |
| LLM involvement | Codex helped scaffold the Docker environment, verifier, documentation, and this draft. [Describe all additional use.] |

## Test report

Record the exact commit and actual completed runs:

| Agent | Model | Skill mode | Trials | Passes |
|---|---|---:|---:|---:|
| oracle | n/a | n/a | [ ] | [ ] |
| [agent] | [model] | no-skill | [ ] | [ ] |
| [agent] | [model] | with-skill | [ ] | [ ] |

Include failure analysis and do not invent or extrapolate unrun trials.
