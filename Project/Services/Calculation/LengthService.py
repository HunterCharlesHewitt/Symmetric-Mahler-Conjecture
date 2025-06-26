def inner_product(vector1, vector2):
    return sum(a * b for a, b in zip(vector1, vector2))


# TODO verify the below norm is calculated correctly
def K_norm(p, K):
    return max(inner_product(p, v) for v in K.normal_vectors)


def K_length(pi, pi_plus1, K):
    return K_norm(pi_plus1 - pi, K)

def max_K_vector(vect, K):
    # Should return the vector v in K.normal_vectors which maximizes the dot product with vect
    # Should NOT return inner_product(vect, v)
    max_vect = K.normal_vectors[0]
    max_dot = -1
    for v in K.normal_vectors:
        inner_prod = inner_product(vect, v)
        if inner_prod > max_dot:
            max_dot = inner_prod
            max_vect = v
    return max_vect
