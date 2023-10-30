# Registration from extracted features

Execute `run_registration_global.py` to execute the registration for all the benchmark problems.

Modify the parameters inside the scipt as follows:

ALGORITHM: specify "RANSAC", "FastGlobal" or "TEASER"
VOXEL_SIZE: specify the voxel size used for the downsampling
USE_STATUS_TXT: specify True if you also generated a .txt file that contains for each problem the feature extraction result, else specify False

BENCHMARK_DIR= path to the benchmark folder
FEATURES_DIR= path to the folder that contains the features
RESULTS_DIR= path to the folder where the results will be saved