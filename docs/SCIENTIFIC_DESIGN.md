# Scientific Design

## Controlled contrast

For graph \(G\), density target \(\rho\), and repetition \(r\), let
\(T_P(G,\rho,r)\) and \(T_O(G,\rho,r)\) denote partitioning and overlapping
clustering runtimes.

The primary paired effect is

\[
S(G,\rho,r)=\frac{T_O(G,\rho,r)}{T_P(G,\rho,r)},
\qquad
L(G,\rho,r)=\log S(G,\rho,r).
\]

\(S>1\) indicates additional computational cost for overlap. The robust
estimand is

\[
\widehat{S}_{G,\rho}
=
\exp\!\left(\operatorname{median}_r L(G,\rho,r)\right).
\]

Dispersion is reported as the exponentiated interquartile interval

\[
\left[
\exp(Q_{0.25}(L)),
\exp(Q_{0.75}(L))
\right].
\]

## Experimental controls

- Identical graph, density target, implementation backend, and hardware
- Matched repetition index for paired effects
- Two untimed warm-up executions
- Eight measured executions, giving exact 4:4 order balance
- Alternating method order to reduce temporal and thermal bias
- Timer encloses `fit()` only
- Graph loading, serialization, and plotting excluded

## Scientific invariants

For every \((G,\rho)\):

\[
C^{(1)}_P(G,\rho)=C^{(1)}_O(G,\rho),
\]

and every later overlapping seed triangle \(\tau_k\) satisfies

\[
\tau_k \cap \bigcup_{j<k} C_j = \varnothing.
\]

Each selected cluster state must satisfy

\[
RD(C)=\frac{|E_{\mathrm{int}}(C)|}
{|E_{\mathrm{int}}(C)|+|E_{\mathrm{ext}}(C)|}.
\]

## Interpretation

The estimand isolates the runtime cost of retaining previously clustered nodes
for later expansion. It does not claim that slower runtime implies better
clustering quality. Runtime and clustering behavior are reported separately.
