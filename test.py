from optimizer import *

# print(check_if_line_in_cone(np.array([[1, 0], [0, 1], [-1, -1]]))) # True
# print("__")
# print(check_if_line_in_cone(np.array([[1, 0], [0, 1]]))) # False
# print("__")
# print(check_if_line_in_cone(np.array([[1, 0], [-1, 0]]))) # True
# print("__")
# print(check_if_line_in_cone(np.array([[1, 0], [0, 1], [0, -1]]))) # True
# print("__")
# print(check_if_line_in_cone(np.array([[1, 0], [0, 1], [1,1], [2,4]]))) # False

# # square example
# dim = 2
# # T is the square
# T = np.array([[1,0], [0,1], [-1,0], [0,-1]])
# # K is the polar duel of T 
# K = np.array([[1,1], [1,-1], [-1,1], [-1,-1]])
# # here m = 2. # in this case 2d array with only one item.
# orbit = [np.array([[0,1]]), np.array([[0,-1]])]
# cones = [np.array([1,1]), np.array([-1,-1])]

# # # Viterbo counter example
dim=2
sides = 9
T_vertecies = np.array([[math.cos(2*math.pi*i/sides), math.sin(2*math.pi*i/sides)] for i in range(sides)])
# Hiam and Ostrover could have been more clear about this, but it seems like the normal vectors that define K lie on the unit sphere (standard norm)
# This is odd since the dual of the the vectrors defining T lie on the unit sphere. I belive this because they inner producted these unit vectors
# with vectors in the boundary of the polytope T.
K = np.array([[math.sin(2*math.pi*i/sides), -math.cos(2*math.pi*i/sides)] for i in range((-sides)//2, sides//2)])
# K = find_polar_dual(dim, np.array([[math.sin(2*math.pi*i/sides), -math.cos(2*math.pi*i/sides)] for i in range((-sides)//2, sides//2)]))
T = find_polar_dual(2, T_vertecies)

crit_ratio = cube_capacilty_ratio(dim)
print("actually starting")
val = c_K_T_(T, K, stop_num=crit_ratio)
vol = volume_k_metric(dim, K, T)

print(val)

print(math.pow(val,2)/vol)

# # case 1
# # orbit = [np.array([T[1]]), np.array([T[4]]), np.array([T[3]])]
# # cones = np.array([K[0], K[3], K[2]])
# # cones = np.array([K[1], K[4], K[3]])
# # case 2
# orbit = [np.array([T[0]]), np.array([T[2]]), np.array([T[4]])]
# # cones = np.array([K[0], K[2], K[4]])
# # cones = np.array([K[1], K[3], K[4]])

# vol = volume_k_metric(dim, K, T)
# val, cones = optimize_over_cones(orbit, T, K, lazyness=0)
# # val, xs = optimize_k_length(orbit, cones, T, K, verbose=True)

# val, xs = optimize_k_length(orbit, cones, T, K, verbose=True)

# print(vol)
# print(val)
# print(cones)

# print(xs)

# for k in K:
#     print("_____________________")
#     print(k)
#     print(inner_product(np.array([xs[2][i]-xs[1][i] for i in [0,1]]), k))

# print(sum([K_length(xs[(i-1)%3], xs[i], K) for i in range(3)]))

# ys = [np.array([-0.22252093, 0.97492791]), np.array([-0.22252093, -0.97492791]), np.array([-0.22252093, -0.97492791])]
# print(sum([K_length(ys[i], ys[(i-1)%3], K) for i in range(3)]))
# print(2*math.cos(math.pi/10)*(1+math.cos(math.pi/5)))

# print(math.pow(4,2)/8)
# print(math.pow(val,2)/vol)