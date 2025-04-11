The function that we're trying to minimize is a piecewise affine function (some may call it piecewise linear but it is not necessarily linear).

The affine function changes from region to region.

We have 2 polytopes: $T$, and $K$

Take the points $x_i$ on $T$, then define $$v_i = x_{i+1}-x_i$$with $$\mathscr{L}(x_{1},\dots,x_k) = \sum_{i=1} \Vert {x_{i+1}-x_i}\Vert_k = \sum F_K(x_{i+1}-x_i)$$Where $$F_k(\vec{x}) = \text{max}_i (\vec{v}_i \cdot \vec{x}_i)$$
Let $E \subset K$ be a codimension $1$ facet (actual face / side) and consider $\text{cone}(E)$

```
title: Claim
$F_K$ is linear on the cones $\text{cone}(E)$ for each codimension $1$ facet
```

If the vector stays in the cone, then doesn't change. For each set of sides there should be $x_{1} \in E_1,\dots, x_k \in E_k$ and $$E_{1} \times E_{2} \times \dots \times E_k \subset \mathbb{R}^{kn-1} \overset{\mathscr{L}}{\rightarrow} \mathbb{R}$$Weird linear algebra problem to compute domains: decompose into $$\displaylines{\bigcup_{j=1}^{M} \Delta_j \text{ in each } S|_{\Delta_j} \text{ is affine} \\
x_{i},\dots,x_k \in \Delta_j \\
x_{i+1} - x_{i} \in \text{cone}(E_{ij}) \quad \text{where } E_{ij} \text{ is a specific facet of }K}$$
Our goal is to calculate the domains $E_1 \times E_2 \times \dots \times E_k$ algorithmically with python. 