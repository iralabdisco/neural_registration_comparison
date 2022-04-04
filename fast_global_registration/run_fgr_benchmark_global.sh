PY3="python3"
BENCHMARK_DIR="/neural_comparison/point_clouds_registration_benchmark/"
FEATURES_DIR="/neural_comparison/experiments/3DFeatNet/feature_extraction_voxelgrid_0.1/"
RESULTS_DIR="/neural_comparison/experiments/3DFeatNet/results_fgr_voxelgrid_0.1/"
DISTANCE_METRIC="euclidean" #for valid metrics see https://github.com/scikit-learn/scikit-learn/issues/4520#issuecomment-89837739

## KAIST
# uban05_global
${PY3} fast_global_benchmark.py \
        --input_txt=${BENCHMARK_DIR}'kaist/urban05_global.txt' \
        --input_pcd_dir=${BENCHMARK_DIR}'kaist/urban05/' \
        --input_features_dir=${FEATURES_DIR}'kaist/urban05/'  \
        --output_dir=${RESULTS_DIR}'kaist/urban05/' \
        --distance_metric=${DISTANCE_METRIC}