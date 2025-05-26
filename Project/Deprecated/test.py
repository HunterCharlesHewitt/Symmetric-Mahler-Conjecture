# # from Project.Deprecated.optimizer import *
# # from visualizer import *
#
# # print(check_if_line_in_cone(np.array([[1, 0], [0, 1], [-1, -1]]))) # True
# # print("__")
# # print(check_if_line_in_cone(np.array([[1, 0], [0, 1]]))) # False
# # print("__")
# # print(check_if_line_in_cone(np.array([[1, 0], [-1, 0]]))) # True
# # print("__")
# # print(check_if_line_in_cone(np.array([[1, 0], [0, 1], [0, -1]]))) # True
# # print("__")
# # print(check_if_line_in_cone(np.array([[1, 0], [0, 1], [1,1], [2,4]]))) # False
#
# # # cube example
# # def generate_octahedron(dim):
# #     if dim == 1:
# #         return np.array([[1], [-1]])
# #     tail = generate_octahedron(dim-1)
# #     rv = np.empty((0, dim))
# #     for vector in tail:
# #         v_plus = np.append(vector, 1)
# #         v_minus = np.append(vector, -1)
# #         rv = np.concatenate((rv, np.array([v_plus]), np.array([v_minus])))
# #     return rv
# # # T is the square
# # zeroes = np.zeros(dim)
# # T  = np.empty((0, dim))
# # for i in range(dim):
# #     cur_plus = zeroes.copy()
# #     cur_plus[i] = 1
# #     cur_minus = zeroes.copy()
# #     cur_minus[i] = -1
# #     T = np.concatenate((T, np.array([cur_plus]), np.array([cur_minus])))
# # # K is the polar dual of T
# # K = generate_octahedron(dim)
#
# #  Hiam Ostrover Viterbo counter example
# dim=2
# sides = 5
# T_vertecies = np.array([[math.cos(2*math.pi*i/sides), math.sin(2*math.pi*i/sides)] for i in range(sides)])
# # Hiam and Ostrover could have been more clear about this, but it seems like the normal vectors that define K lie on the unit sphere (standard norm)
# # This is odd since the dual of the the vectrors defining T lie on the unit sphere. I belive this because they inner producted these unit vectors
# # with vectors in the boundary of the polytope T.
# K = np.array([[math.sin(2*math.pi*i/sides), -math.cos(2*math.pi*i/sides)] for i in range((-sides)//2, sides//2)])
# # # K = find_polar_dual(dim, np.array([[math.sin(2*math.pi*i/sides), -math.cos(2*math.pi*i/sides)] for i in range((-sides)//2, sides//2)]))
# T = find_polar_dual(dim, T_vertecies)
#
# # # Tetrahedron example
# # dim = 3
# # T = find_polar_dual(dim,np.array([[math.sqrt(6),-math.sqrt(3),-2], [-math.sqrt(6), -math.sqrt(3), -2], [0, math.sqrt(8), -2], [0,0,2]]))
# # K = find_polar_dual(dim, T)
#
# # # Random shapes
# # dim = 3
# # def get_random_shape(t_sides,k_sides):
# #     T = None
# #     K = None
# #     # This is the K from the n=2.84 example (second best example we had before using this)
# #     # K = np.array([[-0.70880303,  0.64350865], [ 0.31667143, -0.20694839], [-0.41566717, -0.62539306]])
# #     while T is None or not check_if_line_in_cone(T):
# #         T = np.array([[random.random()*2-1 for _ in range(dim)] for _ in range(t_sides)])
# #     while K is None or not check_if_line_in_cone(K):
# #         K = np.array([[random.random()*2-1 for _ in range(dim)] for _ in range(k_sides)])
# #     return T,K
# # max_num = 0
# # times = 10000000
# # dim = 2  # or whatever your `dim` is
# # import sys
# # # open the file once, in write‐mode
# # with open("results.txt", "a") as f:
# #     for i in range(times):
# #         sys.stdout.write(f"\rTry #:{i} ---- Current_Max: {max_num}")
# #         sys.stdout.flush()
# #         sides = random.randint(4,7)
# #         T, K = get_random_shape(sides, sides)
# #         try:
# #             val, orbit, cones = c_K_T_(T, K, stop_num=3, return_lots=True)
# #         except Exception as e:
# #             continue
# #         vol = volume_k_metric(dim, K, T)
# #
# #         num = math.pow(val, dim) / vol
# #
# #         # write the basic 'num' line
# #         f.write(f"{num}\n")
# #
# #         if num > max_num:
# #             max_num = num
# #             f.write(f"WE FOUND A NEW MAX: {max_num}\n")
# #             f.write(f"T = {T}\n")
# #             f.write(f"K = {K}\n")
# #             f.write("val then num:\n")
# #             f.write(f"{val}\n")
# #             f.write(f"{num}\n")
# #             f.write("orbit and cones:\n")
# #             f.write(f"{orbit}\n")
# #             f.write(f"{cones}\n")
# #
# #             # if you still want to run the optimizer & include its output:
# #             _, xs = optimize_k_length(orbit, cones, T, K, verbose=False)
# #             f.write("xs:\n")
# #             f.write(f"{xs}\n")
# #             f.write("______________________________\n")
# #             f.flush()
#
#             # if dim != 2:
#             #     Q = np.array([[0,1], [1,0], [0,-1], [-1,0]])
#             #     visualize_polytope(Q)
#             # else:
#             #     visualize_polytope(T, xs, K)
# # val = c_K_T_(T, K)
#
# # vol = volume_k_metric(dim, K, T)
# # print(val)
# # print(math.pow(val,dim)/vol)
#
# # print(sum([K_length(xs[(i-1)%3], xs[i], K) for i in range(3)]))
#
# # BEST SO FAR:
# # # ratio = 3.57
# # T = np.array([[-0.39275834, -0.21369186], [ 0.97887142, -0.7326133 ],[-0.2209859 ,  0.91339311]])
# # K = np.array([[-0.70880303,  0.64350865], [ 0.31667143, -0.20694839], [-0.41566717, -0.62539306]])
#
# # # ratio = 2.19
# # T = np.array([[0.62366956, -0.42674541], [-0.31253492, -0.61563267], [-0.36879486,  0.64786535], [ 0.0944798, 0.97336157]])
# # K = np.array([[ 0.13697769, -0.64448017], [ 0.07409263,  0.94443078], [-0.68079398, -0.10756287]])
#
# # # ratio = 2.5
# # T = np.array([[-0.5772615,  -0.99512385],[ 0.82656771,  0.71664457],[-0.54702504,  0.9874792 ]])
# # K = np.array([[-0.44507611, -0.09002565], [ 0.98124427,  0.94186558], [ 0.15813048, -0.60685998]])
#
# # # ratio = 2.6
# # T = np.array([[ 0.00394174,  0.45952429], [-0.81275191, -0.07295926], [ 0.50559184,  0.66769837], [ 0.71270722, -0.98338669]])
# # K = np.array([[ 0.47869793,  0.2935875 ], [-0.89527149,  0.39683043], [-0.42797739, -0.91928039]])
#
# # # ratio = 2.84
# # T = np.array([[ 0.92387521, -0.99173718], [-0.06878107,  0.4981903 ], [-0.95326733, -0.53435621]])
# # K = np.array([[-0.70880303,  0.64350865], [ 0.31667143, -0.20694839], [-0.41566717, -0.62539306]])
#
# # # ratio = 2.977
# # T = np.array([[ 0.10149025,  0.3122396 ], [-0.81288258, -0.05756627], [ 0.60665305, -0.68233359]])
# # K = np.array([[ 0.65576552, -0.27721999], [-0.38566591, -0.4849761 ], [ 0.00558822,  0.63888191]])
#
# # # ratio  2.98 (T is very big)
# # T = np.array([[-0.02450467,  0.06779781], [-0.39926916, -0.2503332 ], [ 0.68818616, -0.5137174 ]])
# # K = np.array([[-0.70880303,  0.64350865], [ 0.31667143, -0.20694839], [-0.41566717, -0.62539306]])
#
# # # ratio 3.12466
# # T = np.array([[ 0.64882863,  0.21130389], [ 0.09144596, -0.41452909], [-0.99667541,  0.93736374]])
# # K = np.array([[-0.70880303,  0.64350865], [ 0.31667143, -0.20694839], [-0.41566717, -0.62539306]])
#
# # # ratio 3.25 (second best)
# # T = np.array([[-0.88538681,  0.16564993], [ 0.15918032,  0.91929798], [ 0.78453111, -0.89113456]])
# # K = np.array([[-0.82753897,  0.64060135], [ 0.54545526, -0.83767349], [ 0.99944807,  0.3057224 ]])
#
# # # ratio 3.3 (new second best)
# # T = np.array([[ 0.59017817,  0.5542213 ], [-0.28508066, -0.74528511], [-0.68637222,  0.80348173]])
# # K = np.array([[ 0.71242983,  0.31702145],[ 0.19720467,  0.77965144],[-0.29178176, -0.66381123]])
#
# #### ___________________________________________________
# #### 3D case ratio needs to beat 6
#
# # # ratio 6.65
# # T = np.array([[-0.40194532,  0.16983462, -0.56022014], [-0.87120207, -0.97969581,  0.7977686 ], [ 0.83904777,  0.14480077, -0.20240849], [ 0.814427,    0.30484695, 0.59935952]])
# # K = np.array([[ 0.00832644,  0.62359217,  0.0120101 ], [ 0.28067259, -0.79645379,  0.71853707], [ 0.8897662,   0.11409895, -0.19667404], [-0.5365675,  -0.33801618, -0.61810512]])
#
# # # # ratio 7.2
# # T = np.array([[ 0.71652441,  0.68271534,  0.0157473 ], [ 0.32863243, -0.64573113,  0.57771234], [-0.97883107,  0.13959444,  0.26231337], [-0.11557885, -0.4785974,  -0.85218172]])
# # K = np.array([[-0.95462867, -0.46968908, -0.90322578], [-0.56556438, -0.60328048, -0.04336644], [ 0.31941768, -0.18980349, -0.87870316], [ 0.53539649,  0.53852404,  0.5290557 ]])
#
#
# # dim = 3
#
# # print(find_polar_dual(dim, T))
# # print(find_polar_dual(dim, K))
#
# val, orbit, cones = c_K_T_(T, K, return_lots = True, stop_num=0)
# vol = volume_k_metric(dim, K, T)
# num = math.pow(val,dim)/vol
# print(num)
# print(T)
# print(K)
# print("val then num:")
# print(val)
# print(num)
# print("orbit and cones:")
# print(orbit)
# print(cones)
# _, xs = optimize_k_length(orbit, cones, T, K, verbose = False)
# print("xs:")
# print(xs)
# print("______________________________")
# if dim == 2:
#     # visualize_polytope(T, xs)
#     visualize_polytope(T, xs, K)
