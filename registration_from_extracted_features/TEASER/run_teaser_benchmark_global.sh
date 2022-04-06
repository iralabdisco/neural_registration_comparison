PY3="python3"
GPU=0
BENCHMARK_DIR="/neural_comparison/point_clouds_registration_benchmark/"
FEATURES_DIR="/neural_comparison/experiments/3DFeatNet/feature_extraction_voxelgrid_0.1/"
RESULTS_DIR="/neural_comparison/experiments/3DFeatNet/results_teaser_voxelgrid_0.1/"
CBAR2="1"
NOISE_BOUND="0.1" #voxel size
ESTIMATE_SCALING="False"
ROTATION_ESTIMATION_ALGORITHM='GNC_TLS'
ROTATION_GNC_FACTOR='1.4'
ROTATION_MAX_ITERATIONS="100"
ROTATION_COST_THRESHOLD="1e-12"
ROTATION_TIM_GRAPH='CHAIN'
INLIER_SELECTION_MODE='PMC_EXACT'
KCORE_HEURISTIC_THRESHOLD="0.5"
DISTANCE_METRIC="euclidean" #for valid metrics see https://github.com/scikit-learn/scikit-learn/issues/4520#issuecomment-89837739

## KAIST
# uban05_global
${PY3} teaser_benchmark.py --gpu ${GPU} \
        --input_txt=${BENCHMARK_DIR}'kaist/urban05_global.txt' \
        --input_pcd_dir=${BENCHMARK_DIR}'kaist/urban05/' \
        --input_features_dir=${FEATURES_DIR}'kaist/urban05/'  \
        --output_dir=${RESULTS_DIR} \
        --cbar2=${CBAR2} \
        --noise_bound=${NOISE_BOUND} \
        --estimate_scaling=${ESTIMATE_SCALING} \
        --rotation_estimation_algorithm=${ROTATION_ESTIMATION_ALGORITHM} \
        --rotation_gnc_factor=${ROTATION_GNC_FACTOR} \
        --rotation_max_iterations=${ROTATION_MAX_ITERATIONS} \
        --rotation_cost_threshold=${ROTATION_COST_THRESHOLD} \
        --rotation_tim_graph=${ROTATION_TIM_GRAPH} \
        --inlier_selection_mode=${INLIER_SELECTION_MODE} \
        --kcore_heuristic_threshold=${KCORE_HEURISTIC_THRESHOLD} \
        --distance_metric=${DISTANCE_METRIC}

## ETH

# apartment global
${PY3} teaser_benchmark.py --gpu ${GPU} \
        --input_txt=${BENCHMARK_DIR}'eth/apartment_global.txt' \
        --input_pcd_dir=${BENCHMARK_DIR}'eth/apartment/' \
        --input_features_dir=${FEATURES_DIR}'eth/apartment/'  \
        --output_dir=${RESULTS_DIR} \
        --cbar2=${CBAR2} \
        --noise_bound=${NOISE_BOUND} \
        --estimate_scaling=${ESTIMATE_SCALING} \
        --rotation_estimation_algorithm=${ROTATION_ESTIMATION_ALGORITHM} \
        --rotation_gnc_factor=${ROTATION_GNC_FACTOR} \
        --rotation_max_iterations=${ROTATION_MAX_ITERATIONS} \
        --rotation_cost_threshold=${ROTATION_COST_THRESHOLD} \
        --rotation_tim_graph=${ROTATION_TIM_GRAPH} \
        --inlier_selection_mode=${INLIER_SELECTION_MODE} \
        --kcore_heuristic_threshold=${KCORE_HEURISTIC_THRESHOLD} \
        --distance_metric=${DISTANCE_METRIC}

# gazebo_summer global
${PY3} teaser_benchmark.py --gpu ${GPU} \
        --input_txt=${BENCHMARK_DIR}'eth/gazebo_summer_global.txt' \
        --input_pcd_dir=${BENCHMARK_DIR}'eth/gazebo_summer/' \
        --input_features_dir=${FEATURES_DIR}'eth/gazebo_summer/'  \
        --output_dir=${RESULTS_DIR} \
        --cbar2=${CBAR2} \
        --noise_bound=${NOISE_BOUND} \
        --estimate_scaling=${ESTIMATE_SCALING} \
        --rotation_estimation_algorithm=${ROTATION_ESTIMATION_ALGORITHM} \
        --rotation_gnc_factor=${ROTATION_GNC_FACTOR} \
        --rotation_max_iterations=${ROTATION_MAX_ITERATIONS} \
        --rotation_cost_threshold=${ROTATION_COST_THRESHOLD} \
        --rotation_tim_graph=${ROTATION_TIM_GRAPH} \
        --inlier_selection_mode=${INLIER_SELECTION_MODE} \
        --kcore_heuristic_threshold=${KCORE_HEURISTIC_THRESHOLD} \
        --distance_metric=${DISTANCE_METRIC} 

# gazebo_winter global
${PY3} teaser_benchmark.py --gpu ${GPU} \
        --input_txt=${BENCHMARK_DIR}'eth/gazebo_winter_global.txt' \
        --input_pcd_dir=${BENCHMARK_DIR}'eth/gazebo_winter/' \
        --input_features_dir=${FEATURES_DIR}'eth/gazebo_winter/'  \
        --output_dir=${RESULTS_DIR} \
        --cbar2=${CBAR2} \
        --noise_bound=${NOISE_BOUND} \
        --estimate_scaling=${ESTIMATE_SCALING} \
        --rotation_estimation_algorithm=${ROTATION_ESTIMATION_ALGORITHM} \
        --rotation_gnc_factor=${ROTATION_GNC_FACTOR} \
        --rotation_max_iterations=${ROTATION_MAX_ITERATIONS} \
        --rotation_cost_threshold=${ROTATION_COST_THRESHOLD} \
        --rotation_tim_graph=${ROTATION_TIM_GRAPH} \
        --inlier_selection_mode=${INLIER_SELECTION_MODE} \
        --kcore_heuristic_threshold=${KCORE_HEURISTIC_THRESHOLD} \
        --distance_metric=${DISTANCE_METRIC}

# hauptgebaude global
${PY3} teaser_benchmark.py --gpu ${GPU} \
        --input_txt=${BENCHMARK_DIR}'eth/hauptgebaude_global.txt' \
        --input_pcd_dir=${BENCHMARK_DIR}'eth/hauptgebaude/' \
        --input_features_dir=${FEATURES_DIR}'eth/hauptgebaude/'  \
        --output_dir=${RESULTS_DIR} \
        --cbar2=${CBAR2} \
        --noise_bound=${NOISE_BOUND} \
        --estimate_scaling=${ESTIMATE_SCALING} \
        --rotation_estimation_algorithm=${ROTATION_ESTIMATION_ALGORITHM} \
        --rotation_gnc_factor=${ROTATION_GNC_FACTOR} \
        --rotation_max_iterations=${ROTATION_MAX_ITERATIONS} \
        --rotation_cost_threshold=${ROTATION_COST_THRESHOLD} \
        --rotation_tim_graph=${ROTATION_TIM_GRAPH} \
        --inlier_selection_mode=${INLIER_SELECTION_MODE} \
        --kcore_heuristic_threshold=${KCORE_HEURISTIC_THRESHOLD} \
        --distance_metric=${DISTANCE_METRIC}

# plain global
${PY3} teaser_benchmark.py --gpu ${GPU} \
        --input_txt=${BENCHMARK_DIR}'eth/plain_global.txt' \
        --input_pcd_dir=${BENCHMARK_DIR}'eth/plain/' \
        --input_features_dir=${FEATURES_DIR}'eth/plain/'  \
        --output_dir=${RESULTS_DIR} \
        --cbar2=${CBAR2} \
        --noise_bound=${NOISE_BOUND} \
        --estimate_scaling=${ESTIMATE_SCALING} \
        --rotation_estimation_algorithm=${ROTATION_ESTIMATION_ALGORITHM} \
        --rotation_gnc_factor=${ROTATION_GNC_FACTOR} \
        --rotation_max_iterations=${ROTATION_MAX_ITERATIONS} \
        --rotation_cost_threshold=${ROTATION_COST_THRESHOLD} \
        --rotation_tim_graph=${ROTATION_TIM_GRAPH} \
        --inlier_selection_mode=${INLIER_SELECTION_MODE} \
        --kcore_heuristic_threshold=${KCORE_HEURISTIC_THRESHOLD} \
        --distance_metric=${DISTANCE_METRIC}

# stairs global
${PY3} teaser_benchmark.py --gpu ${GPU} \
        --input_txt=${BENCHMARK_DIR}'eth/stairs_global.txt' \
        --input_pcd_dir=${BENCHMARK_DIR}'eth/stairs/' \
        --input_features_dir=${FEATURES_DIR}'eth/stairs/'  \
        --output_dir=${RESULTS_DIR} \
        --cbar2=${CBAR2} \
        --noise_bound=${NOISE_BOUND} \
        --estimate_scaling=${ESTIMATE_SCALING} \
        --rotation_estimation_algorithm=${ROTATION_ESTIMATION_ALGORITHM} \
        --rotation_gnc_factor=${ROTATION_GNC_FACTOR} \
        --rotation_max_iterations=${ROTATION_MAX_ITERATIONS} \
        --rotation_cost_threshold=${ROTATION_COST_THRESHOLD} \
        --rotation_tim_graph=${ROTATION_TIM_GRAPH} \
        --inlier_selection_mode=${INLIER_SELECTION_MODE} \
        --kcore_heuristic_threshold=${KCORE_HEURISTIC_THRESHOLD} \
        --distance_metric=${DISTANCE_METRIC}

# wood_autumn global
${PY3} teaser_benchmark.py --gpu ${GPU} \
        --input_txt=${BENCHMARK_DIR}'eth/wood_autumn_global.txt' \
        --input_pcd_dir=${BENCHMARK_DIR}'eth/wood_autumn/' \
        --input_features_dir=${FEATURES_DIR}'eth/wood_autumn/'  \
        --output_dir=${RESULTS_DIR} \
        --cbar2=${CBAR2} \
        --noise_bound=${NOISE_BOUND} \
        --estimate_scaling=${ESTIMATE_SCALING} \
        --rotation_estimation_algorithm=${ROTATION_ESTIMATION_ALGORITHM} \
        --rotation_gnc_factor=${ROTATION_GNC_FACTOR} \
        --rotation_max_iterations=${ROTATION_MAX_ITERATIONS} \
        --rotation_cost_threshold=${ROTATION_COST_THRESHOLD} \
        --rotation_tim_graph=${ROTATION_TIM_GRAPH} \
        --inlier_selection_mode=${INLIER_SELECTION_MODE} \
        --kcore_heuristic_threshold=${KCORE_HEURISTIC_THRESHOLD} \
        --distance_metric=${DISTANCE_METRIC}

# wood_summer global
${PY3} teaser_benchmark.py --gpu ${GPU} \
        --input_txt=${BENCHMARK_DIR}'eth/wood_summer_global.txt' \
        --input_pcd_dir=${BENCHMARK_DIR}'eth/wood_summer/' \
        --input_features_dir=${FEATURES_DIR}'eth/wood_summer/'  \
        --output_dir=${RESULTS_DIR} \
        --cbar2=${CBAR2} \
        --noise_bound=${NOISE_BOUND} \
        --estimate_scaling=${ESTIMATE_SCALING} \
        --rotation_estimation_algorithm=${ROTATION_ESTIMATION_ALGORITHM} \
        --rotation_gnc_factor=${ROTATION_GNC_FACTOR} \
        --rotation_max_iterations=${ROTATION_MAX_ITERATIONS} \
        --rotation_cost_threshold=${ROTATION_COST_THRESHOLD} \
        --rotation_tim_graph=${ROTATION_TIM_GRAPH} \
        --inlier_selection_mode=${INLIER_SELECTION_MODE} \
        --kcore_heuristic_threshold=${KCORE_HEURISTIC_THRESHOLD} \
        --distance_metric=${DISTANCE_METRIC}

## TUM

# long_office_household global
${PY3} teaser_benchmark.py --gpu ${GPU} \
        --input_txt=${BENCHMARK_DIR}'tum/long_office_household_global.txt' \
        --input_pcd_dir=${BENCHMARK_DIR}'tum/long_office_household/' \
        --input_features_dir=${FEATURES_DIR}'tum/long_office_household/'  \
        --output_dir=${RESULTS_DIR} \
        --cbar2=${CBAR2} \
        --noise_bound=${NOISE_BOUND} \
        --estimate_scaling=${ESTIMATE_SCALING} \
        --rotation_estimation_algorithm=${ROTATION_ESTIMATION_ALGORITHM} \
        --rotation_gnc_factor=${ROTATION_GNC_FACTOR} \
        --rotation_max_iterations=${ROTATION_MAX_ITERATIONS} \
        --rotation_cost_threshold=${ROTATION_COST_THRESHOLD} \
        --rotation_tim_graph=${ROTATION_TIM_GRAPH} \
        --inlier_selection_mode=${INLIER_SELECTION_MODE} \
        --kcore_heuristic_threshold=${KCORE_HEURISTIC_THRESHOLD} \
        --distance_metric=${DISTANCE_METRIC}


# pioneer_slam global
${PY3} teaser_benchmark.py --gpu ${GPU} \
        --input_txt=${BENCHMARK_DIR}'tum/pioneer_slam_global.txt' \
        --input_pcd_dir=${BENCHMARK_DIR}'tum/pioneer_slam/' \
        --input_features_dir=${FEATURES_DIR}'tum/pioneer_slam/'  \
        --output_dir=${RESULTS_DIR} \
        --cbar2=${CBAR2} \
        --noise_bound=${NOISE_BOUND} \
        --estimate_scaling=${ESTIMATE_SCALING} \
        --rotation_estimation_algorithm=${ROTATION_ESTIMATION_ALGORITHM} \
        --rotation_gnc_factor=${ROTATION_GNC_FACTOR} \
        --rotation_max_iterations=${ROTATION_MAX_ITERATIONS} \
        --rotation_cost_threshold=${ROTATION_COST_THRESHOLD} \
        --rotation_tim_graph=${ROTATION_TIM_GRAPH} \
        --inlier_selection_mode=${INLIER_SELECTION_MODE} \
        --kcore_heuristic_threshold=${KCORE_HEURISTIC_THRESHOLD} \
        --distance_metric=${DISTANCE_METRIC}

# pioneer_slam3 global
${PY3} teaser_benchmark.py --gpu ${GPU} \
        --input_txt=${BENCHMARK_DIR}'tum/pioneer_slam3_global.txt' \
        --input_pcd_dir=${BENCHMARK_DIR}'tum/pioneer_slam3/' \
        --input_features_dir=${FEATURES_DIR}'tum/pioneer_slam3/'  \
        --output_dir=${RESULTS_DIR} \
        --cbar2=${CBAR2} \
        --noise_bound=${NOISE_BOUND} \
        --estimate_scaling=${ESTIMATE_SCALING} \
        --rotation_estimation_algorithm=${ROTATION_ESTIMATION_ALGORITHM} \
        --rotation_gnc_factor=${ROTATION_GNC_FACTOR} \
        --rotation_max_iterations=${ROTATION_MAX_ITERATIONS} \
        --rotation_cost_threshold=${ROTATION_COST_THRESHOLD} \
        --rotation_tim_graph=${ROTATION_TIM_GRAPH} \
        --inlier_selection_mode=${INLIER_SELECTION_MODE} \
        --kcore_heuristic_threshold=${KCORE_HEURISTIC_THRESHOLD} \
        --distance_metric=${DISTANCE_METRIC}

## PLANETARY

# box_met global
${PY3} teaser_benchmark.py --gpu ${GPU} \
        --input_txt=${BENCHMARK_DIR}'planetary/box_met_global.txt' \
        --input_pcd_dir=${BENCHMARK_DIR}'planetary/box_met/' \
        --input_features_dir=${FEATURES_DIR}'planetary/box_met/'  \
        --output_dir=${RESULTS_DIR} \
        --cbar2=${CBAR2} \
        --noise_bound=${NOISE_BOUND} \
        --estimate_scaling=${ESTIMATE_SCALING} \
        --rotation_estimation_algorithm=${ROTATION_ESTIMATION_ALGORITHM} \
        --rotation_gnc_factor=${ROTATION_GNC_FACTOR} \
        --rotation_max_iterations=${ROTATION_MAX_ITERATIONS} \
        --rotation_cost_threshold=${ROTATION_COST_THRESHOLD} \
        --rotation_tim_graph=${ROTATION_TIM_GRAPH} \
        --inlier_selection_mode=${INLIER_SELECTION_MODE} \
        --kcore_heuristic_threshold=${KCORE_HEURISTIC_THRESHOLD} \
        --distance_metric=${DISTANCE_METRIC}

# p2at_met global
${PY3} teaser_benchmark.py --gpu ${GPU} \
        --input_txt=${BENCHMARK_DIR}'planetary/p2at_met_global.txt' \
        --input_pcd_dir=${BENCHMARK_DIR}'planetary/p2at_met/' \
        --input_features_dir=${FEATURES_DIR}'planetary/p2at_met/'  \
        --output_dir=${RESULTS_DIR} \
        --cbar2=${CBAR2} \
        --noise_bound=${NOISE_BOUND} \
        --estimate_scaling=${ESTIMATE_SCALING} \
        --rotation_estimation_algorithm=${ROTATION_ESTIMATION_ALGORITHM} \
        --rotation_gnc_factor=${ROTATION_GNC_FACTOR} \
        --rotation_max_iterations=${ROTATION_MAX_ITERATIONS} \
        --rotation_cost_threshold=${ROTATION_COST_THRESHOLD} \
        --rotation_tim_graph=${ROTATION_TIM_GRAPH} \
        --inlier_selection_mode=${INLIER_SELECTION_MODE} \
        --kcore_heuristic_threshold=${KCORE_HEURISTIC_THRESHOLD} \
        --distance_metric=${DISTANCE_METRIC}

# planetary_map global
${PY3} teaser_benchmark.py --gpu ${GPU} \
        --input_txt=${BENCHMARK_DIR}'planetary/planetary_map_global.txt' \
        --input_pcd_dir=${BENCHMARK_DIR}'planetary/p2at_met/' \
        --input_features_dir=${FEATURES_DIR}'planetary/planetary_map/'  \
        --output_dir=${RESULTS_DIR} \
        --cbar2=${CBAR2} \
        --noise_bound=${NOISE_BOUND} \
        --estimate_scaling=${ESTIMATE_SCALING} \
        --rotation_estimation_algorithm=${ROTATION_ESTIMATION_ALGORITHM} \
        --rotation_gnc_factor=${ROTATION_GNC_FACTOR} \
        --rotation_max_iterations=${ROTATION_MAX_ITERATIONS} \
        --rotation_cost_threshold=${ROTATION_COST_THRESHOLD} \
        --rotation_tim_graph=${ROTATION_TIM_GRAPH} \
        --inlier_selection_mode=${INLIER_SELECTION_MODE} \
        --kcore_heuristic_threshold=${KCORE_HEURISTIC_THRESHOLD} \
        --distance_metric=${DISTANCE_METRIC}