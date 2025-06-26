import gurobipy as gp
from gurobipy import GRB
import numpy as np

# Maybe I can make this a class, but for now, I'm just going to use it as a function.

def gurobi_solver_simple(A,b,c):

    # Convert np.matrix to np.array to avoid indexing issues
    A = np.asarray(A)
    b = np.asarray(b).flatten()
    c = np.asarray(c).flatten()

    num_vars = len(c)
    num_constraints = len(b)

    # Create a new model
    model = gp.Model("simple_lp")

    # Suppress output
    model.setParam("OutputFlag", 0)

    # Create variables
    x_vars = model.addVars(num_vars, lb=-GRB.INFINITY, name="x")

    # Set up constraints: A*x <= b
    for i in range(num_constraints):
        model.addConstr(gp.quicksum(A[i, j] * x_vars[j] for j in range(num_vars)) <= b[i], name=f"c{i}")

    # Set objective function: minimize c*x
    objective = gp.quicksum(c[j] * x_vars[j] for j in range(num_vars))
    model.setObjective(objective, GRB.MINIMIZE)

    # Optimize model
    model.optimize()

    # Check for solution
    if model.status == GRB.OPTIMAL:
        solution = np.array([x_vars[j].X for j in range(num_vars)])
        return model.ObjVal, "optimal", solution
    elif model.status == GRB.INFEASIBLE:
        return float("inf"), "infeasible", None
    elif model.status == GRB.UNBOUNDED:
        return float("inf"), "unbounded", None
    else:
        return float("inf"), "error", None

def gurobi_solver(As, b, c, dim, stop_num=0):
    # This function was completely written by ChatGPT.
    
    # Convert np.matrix to np.array to avoid indexing issues
    As = [np.asarray(A) for A in As]
    b = np.asarray(b).flatten()
    c = np.asarray(c).flatten()

    num_vars = len(c)
    num_constraints = len(b)

    # Step 1: Set up base model
    model = gp.Model("batched_lps")
    model.setParam("OutputFlag", 0)  # silence output

    # Step 2: Add variables
    x_vars = model.addVars(num_vars, lb=-GRB.INFINITY, name="x")

    # Step 3: Add constraints A x <= b, initially with 0.0 coefficients
    constrs = []
    for i in range(num_constraints):
        expr = gp.LinExpr([(0.0, x_vars[j]) for j in range(num_vars)])
        constr = model.addConstr(expr <= b[i], name=f"constr_{i}")
        constrs.append(constr)

    # Step 4: Set fixed objective: minimize c^T x
    obj_expr = gp.quicksum(c[j] * x_vars[j] for j in range(num_vars))
    model.setObjective(obj_expr, GRB.MINIMIZE)
    model.update()

    # Step 5: Loop through each A_i
    results = []
    for idx, A_i in enumerate(As):
        for i in range(num_constraints):
            for j in range(num_vars):
                model.chgCoeff(constrs[i], x_vars[j], A_i[i, j])
        model.update()

        model.optimize()

        if model.Status == GRB.OPTIMAL:
            solution = np.array([x_vars[j].X for j in range(num_vars)])
            objective_value = model.ObjVal
            results.append((idx, "feasible", solution, objective_value))
            if stop_num > objective_value**dim:
                return idx, objective_value
        elif model.Status == 4 or model.Status == GRB.INFEASIBLE:
            results.append((idx, "infeasible", None, float("inf")))
        else:
            print("ERROR!")
            print(model.Status)
            # print(f"Status: {model.Status}")
            results.append((idx, "error", None, float("inf")))
    min_result = min(results, key=lambda x: x[3])

    return min_result[2], min_result[3]

def gurobi_feasability(A, b):
    # Create a Gurobi model
    model = gp.Model()
    model.setParam('OutputFlag', 0)  # Suppress solver output

    # Add variables (unbounded in this example)
    n = A.shape[1]
    x = model.addMVar(shape=n, name="x", lb=-GRB.INFINITY, ub=GRB.INFINITY)

    # Add constraints: Ax <= b
    model.addConstr(A @ x <= b)

    # No need to set an objective; Gurobi defaults to minimizing 0

    # Optimize the model
    model.optimize()

    return model.Status == GRB.OPTIMAL
