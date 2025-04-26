def inner_product(vector1, vector2):
    return sum(a * b for a, b in zip(vector1, vector2))


# TODO verify the below norm is calculated correctly
def K_norm(p, K):
    return max(inner_product(p, v) for v in K.normal_vectors)


def K_length(pi, pi_plus1, K):
    return K_norm(pi_plus1 - pi, K)
