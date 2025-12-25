from ortools.sat.python import cp_model

def solve_rocket_power():
    model = cp_model.CpModel()

    # 1. DATA: Supply, Demand, and "Cost" (Weight)
    sources = {'Battery': 100, 'Solar': 150}
    systems = {'Thrusters': 80, 'LifeSupport': 50, 'Nav': 40}
    
    # Weight per unit of power (Battery is heavy, Solar is light)
    weights = {('Battery', 'Thrusters'): 10, ('Solar', 'Thrusters'): 2}

    # 2. VARIABLES: How much power flows from source to system
    flow = {}
    for s in sources:
        for sys in systems:
            flow[(s, sys)] = model.NewIntVar(0, 200, f'flow_{s}_{sys}')

    # 3. CONSTRAINTS
    # Supply: Don't exceed source capacity
    for s, capacity in sources.items():
        model.Add(sum(flow[(s, sys)] for sys in systems) <= capacity)

    # Demand: Systems must get exactly what they need
    for sys, demand in systems.items():
        model.Add(sum(flow[(s, sys)] for s in sources) == demand)

    # 4. OBJECTIVE: Minimize "Launch Weight"
    total_weight = sum(flow[(s, sys)] * 5 for s, sys in flow) # Simplified weight multiplier
    model.Minimize(total_weight)

    # 5. SOLVER
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print(f"Mission Success! Total Weight: {solver.ObjectiveValue()}")
        for (s, sys), var in flow.items():
            if solver.Value(var) > 0:
                print(f" -> {s} providing {solver.Value(var)}W to {sys}")

solve_rocket_power()
