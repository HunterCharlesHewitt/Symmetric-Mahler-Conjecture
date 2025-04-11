
title: Conjecture (Mahler):
If $K \subset \mathbb{R}^{n}$ is convex, centrally symmetric ($k=-k$) then $$\text{vol}(k)\text{vol}(k^{0}) \geq \frac{4^{n}}{n!}$$

The below implies the above


title: Billiard Conjecture (Mahler):
Let $T,K \subset \mathbb{R}^{n}$ with $K=-K$. Let $C_K(T) = \text{min}\{\text{length}_k(\Gamma) : \Gamma \subset T \text{ is a closed }k-\text{billiard orbit}\}$ Then $$\frac{C_k(T)^{2}}{\text{vol}_k(T)} \leq \frac{C_{Q^{n}}(Q^{n})^{2n}}{\text{vol}_{Q^{n}}(Q^{n})}$$


- $vol_k(T) = vol(T)\cdot vol(k^{0})$ - (where $k^{0}$ is $k$-dual)
- $\text{length}_k(\Gamma) = \int_{0}^1 \Vert {\frac{d\Gamma}{dt}}\Vert_kdt$ - (where $\Vert {-}\Vert_k$ is the unique norm w/unit ball $k$, the unique 1-homogenous positive function $F_k$ such that $F^{-1}_k([0,1])=k$, $\Gamma(\lambda x) = \lambda F(x)$ with $\lambda \geq 0$). 


title: Theorem (Arseniy V. Akopyan, Alexey M. Balitskiy, Roman N. Karasev, Anastasia Sharipova)
$C_K(T) = \text{min}_{k \leq n+1}\left( \text{min}\left\{ \sum_{i=1}^k \Vert {p_{i+1}-p_i}\Vert : p =\left\{ p_{1},\dots,p_k \right\} \text{ is a set of points in } T \text{ such that } p+v \not\in T \text{ for any } v \neq 0 \in \mathbb{R}^{n} \right\}  \right)$

$C_K(T) = \text{min}_{k \leq n+1}\left( \text{min}\left\{ \sum_{i=1}^k \Vert {p_{i+1}-p_i}\Vert : p =\left\{ p_{1},\dots,p_k \right\} \text{ is a set of points in } T \text{ such that } p+v \not\in T \text{ for any } v \neq 0 \in \mathbb{R}^{n} \right\}  \right)$
If I translate them all simultaneously then one of them leaves the body

The goal is to find an example which breaks the conjecture, ideally a 2d planar polygon

If $T \neq -T, K = - K$ then there is a counterexample by Haim-Kislev, Ostrover. 

![[Pasted image 20250309155427.png]]

We want to make a program and start with the Haim-Kislev-Ostrover counterxample and then use the following pseudo code 

$\text{Length}_k, C_k(T), \text{Vol}_k(T)$

Fix $K, T \subset \mathbb{R}^{n}$ convex <u>polytopes</u>. Assume wlog $0 \in \text{int } x, \text{int }k$ $$\displaylines{T = \left\{ \vec{p} : \vec{p} \cdot\vec{v}_i \leq 1 \text{ for } i =1\dots M\right\} \quad \text{for some } \vec{v}_1\dots\vec{v}_m \in \mathbb{R}^{n} \setminus 0 \\ = \cap_i H(\vec{v_i}), \quad H(v) = \left\{ \vec{p}: \vec{p} \cdot \vec{v} \leq 1 \right\} }$$
$K$ is defined similarly for $\omega_i$

<u>lemma:</u> $\Vert {\vec{x}}\Vert_k = max_i \vec{v}_i \cdot \vec{x}$