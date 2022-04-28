import teaserpp_python
import numpy as np

def run_TEASER_registration(config, source, target, corrs_S, corrs_T):

    # Populate teaser parameters
    solver_params = teaserpp_python.RobustRegistrationSolver.Params()
    solver_params.cbar2 = config["cbar2"]
    solver_params.noise_bound = config["noise_bound"]
    solver_params.estimate_scaling = config["estimate_scaling"]
    solver_params.rotation_estimation_algorithm = eval(config["rotation_estimation_algorithm"])
    solver_params.rotation_gnc_factor = config["rotation_gnc_factor"]
    solver_params.rotation_max_iterations = config["rotation_max_iterations"]
    solver_params.rotation_cost_threshold = config["rotation_cost_threshold"]
    solver_params.rotation_tim_graph = eval(config["rotation_tim_graph"])
    solver_params.inlier_selection_mode = eval(config["inlier_selection_mode"])
    solver_params.kcore_heuristic_threshold = config["kcore_heuristic_threshold"]

    # Get correspondences
    S_corr = source[:, corrs_S]
    T_corr = target[:, corrs_T]

    if (len(S_corr.transpose()) > 1):
        # solve with TEASER++
        teaserpp_solver = teaserpp_python.RobustRegistrationSolver(solver_params)
        teaserpp_solver.solve(S_corr,T_corr)
        solution = teaserpp_solver.getSolution()

        registration_solution = np.eye(4)
        registration_solution[0:3, 0:3] = solution.rotation
        registration_solution[:3, 3] = solution.translation
    else:
        registration_solution = np.eye(4)

    return registration_solution