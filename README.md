# Assessing the Practical Applicability of Neural-Based Point Clouds Registration Algorithms: A Comparative Analysis

This repository collects the results and utilities related to our work
[Assessing the Practical Applicability of Neural-Based Point Clouds Registration Algorithms: A Comparative Analysis](https://www.authorea.com/doi/full/10.22541/au.168908592.24833908/v1)

This work compares different neural network-based algorithms for point clouds registration on our [Point Clouds Registraion Benchmark](https://github.com/iralabdisco/point_clouds_registration_benchmark).
The results of the registration problems can be found in the ```results``` folder, divided by algorithm used. In each leaf folder, a file with the ```_config.json``` suffix can be found, stating the parameters used for the registration.

The full instructions to reproduce the experiments can be found in the [wiki](https://github.com/iralabdisco/neural_registration_comparison/wiki) of this repository.

## Results
These are the results of different feature extractors in conjunction with RANSAC, FastGlobal, and TEASER. Results are reported as the median, 0.75 quantile, and 0.95 quantile of the residual error (as defined in the [Point Clouds Registraion Benchmark](https://github.com/iralabdisco/point_clouds_registration_benchmark).

### 3DFeatNet features
|                                | RANSAC |        |        | FastGlobal |        |        | TEASER |        |        |
|----------------------------------|--------|-------:|-------:|------------|-------:|-------:|--------|-------:|-------:|
|                                | Median | 0.75 Q | 0.95 Q |     Median | 0.75 Q | 0.95 Q | Median | 0.75 Q | 0.95 Q |
|** Sequence**   |        |        |        |            |        |        |        |        |        |
|**plain**   |   8.40 |  12.24 |  18.73 |       4.99 |   6.17 |   7.61 |   9.57 |  13.26 |  22.57 |
|**stairs**   |   2.17 |   3.09 |   7.07 |       2.31 |   3.36 |   5.26 |   2.30 |   3.78 |   7.39 |
|**apartment**   |   1.92 |   2.78 |   4.81 |       2.03 |   2.53 |   3.73 |   2.22 |   3.27 |   5.10 |
|**hauptgebaude**   |   2.72 |   6.47 |   9.28 |       2.79 |   4.91 |   6.31 |   2.44 |   5.57 |   8.72 |
|**wood\_autumn**  |   3.20 |   4.42 |   5.92 |       2.53 |   3.62 |   5.10 |   2.87 |   4.10 |   5.95 |
|**wood\_summer**  |   2.79 |   3.73 |   5.34 |       2.21 |   3.52 |   4.17 |   2.49 |   3.83 |   5.06 |
|**gazebo\_summer**  |   3.51 |   4.81 |   8.41 |       2.33 |   3.30 |   4.17 |   3.13 |   4.98 |   7.15 |
|**gazebo\_winter**  |   3.72 |   5.47 |   9.10 |       2.15 |   3.34 |   4.51 |   3.14 |   4.92 |   8.09 |
|**box\_met**  |  10.14 |  12.76 |  19.82 |       8.30 |  10.53 |  13.98 |  13.01 |  28.65 |  81.78 |
|**p2at\_met**  |  10.43 |  17.48 |  32.84 |       6.27 |  10.27 |  15.89 |  10.22 |  18.40 |  89.83 |
|**planetary\_map**  |  41.00 |  60.25 | 100.93 |      27.08 |  42.20 |  61.59 |  40.76 |  62.61 | 103.20 |
|**pioneer\_slam**  |  10.25 |  17.67 |  35.64 |       6.74 |   8.91 |  10.64 |  13.87 |  27.94 |  43.60 |
|**pioneer\_slam3**  |   4.73 |   9.13 |  13.84 |       5.86 |   7.98 |   9.47 |   7.47 |  12.44 |  21.51 |
|**long\_office\_household** |  14.93 |  27.53 |  41.75 |       4.13 |   7.77 |  11.24 |   9.68 |  28.31 |  72.94 |
|**urban05**   |   2.27 |   3.54 |   6.79 |       1.33 |   2.03 |   3.47 |   2.17 |   3.71 |   7.09 |
|**Total**   |   4.21 |   9.96 |  37.31 |       3.53 |   6.53 |  21.15 |   4.17 |  10.55 |  50.44 |

###  FCGF features using the model trained on 3dMatch

|                                  | RANSAC |        |        | FastGlobal |        |        | TEASER |        |        |
|----------------------------------|--------|-------:|-------:|------------|-------:|-------:|--------|-------:|-------:|
|                                 | Median | 0.75 Q | 0.95 Q |     Median | 0.75 Q | 0.95 Q | Median | 0.75 Q | 0.95 Q |
|**Sequence**   |        |        |        |            |        |        |        |        |        |
|**plain**   |   7.05 |   8.90 |  13.55 |       7.22 |   9.19 |  13.95 |   7.22 |   9.34 |  13.82 |
|**stairs**   |   5.77 |   7.45 |   9.15 |       5.85 |   7.43 |   9.28 |   5.85 |   7.50 |   9.28 |
|**apartment**   |   5.93 |   7.38 |  10.94 |       6.15 |   7.62 |  10.33 |   6.15 |   7.63 |  10.33 |
|**hauptgebaude**   |   2.53 |   3.08 |   3.71 |       2.59 |   3.22 |   3.78 |   2.62 |   3.18 |   3.78 |
|**wood\_autumn**  |   3.19 |   4.21 |   5.64 |       3.92 |   5.12 |   5.79 |   3.84 |   5.12 |   5.79 |
|**wood\_summer**  |   2.96 |   3.73 |   4.98 |       2.60 |   3.44 |   4.55 |   2.54 |   3.51 |   4.63 |
|**gazebo\_summer**  |   2.84 |   4.07 |   5.06 |       3.11 |   4.35 |   5.20 |   3.14 |   4.36 |   5.44 |
|**gazebo\_winter**  |   3.50 |   4.79 |   5.85 |       3.60 |   4.77 |   5.85 |   3.61 |   4.78 |   5.68 |
|**box\_met**  |   7.61 |  10.84 |  13.79 |       8.40 |  12.07 |  17.89 |   8.92 |  11.43 |  17.93 |
|**p2at\_met**  |   9.82 |  12.75 |  17.48 |       8.43 |  13.13 |  21.25 |   8.69 |  12.97 |  19.59 |
|**planetary\_map**  |  11.33 |  15.52 |  21.16 |      31.09 |  46.49 |  67.82 |  31.92 |  47.25 |  67.94 |
|**pioneer\_slam**  |  11.74 |  18.76 |  30.26 |      11.77 |  18.76 |  30.29 |  11.77 |  18.76 |  30.30 |
|**pioneer\_slam3**  |   7.07 |  12.86 |  16.62 |       7.07 |  12.86 |  16.64 |   7.06 |  12.85 |  16.63 |
|**long\_office\_household** |   9.21 |  20.70 |  41.05 |       9.41 |  20.66 |  41.05 |   9.68 |  20.65 |  41.05 |
|**urban05**   |   2.51 |   3.76 |   5.30 |       1.41 |   1.93 |   3.16 |   2.27 |   3.68 |  11.04 |
|**Total**   |   4.85 |   8.73 |  18.11 |       4.92 |   9.53 |  30.27 |   5.08 |   9.71 |  30.35 |

###  FCGF features using the model trained on Kitti

|                                  | RANSAC |        |        | FastGlobal |        |        | TEASER |        |        |
|----------------------------------|--------|-------:|-------:|------------|-------:|-------:|--------|-------:|-------:|
|                                 | Median | 0.75 Q | 0.95 Q |     Median | 0.75 Q | 0.95 Q | Median | 0.75 Q | 0.95 Q |
|**Sequence**   |        |        |        |            |        |        |        |        |        |
|**plain**   |   7.05 |   8.90 |  13.55 |       7.22 |   9.19 |  13.95 |   7.22 |   9.34 |  13.82 |
|**stairs**   |   5.77 |   7.45 |   9.15 |       5.85 |   7.43 |   9.28 |   5.85 |   7.50 |   9.28 |
|**apartment**   |   5.93 |   7.38 |  10.94 |       6.15 |   7.62 |  10.33 |   6.15 |   7.63 |  10.33 |
|**hauptgebaude**   |   2.53 |   3.08 |   3.71 |       2.59 |   3.22 |   3.78 |   2.62 |   3.18 |   3.78 |
|**wood\_autumn**  |   3.19 |   4.21 |   5.64 |       3.92 |   5.12 |   5.79 |   3.84 |   5.12 |   5.79 |
|**wood\_summer**  |   2.96 |   3.73 |   4.98 |       2.60 |   3.44 |   4.55 |   2.54 |   3.51 |   4.63 |
|**gazebo\_summer**  |   2.84 |   4.07 |   5.06 |       3.11 |   4.35 |   5.20 |   3.14 |   4.36 |   5.44 |
|**gazebo\_winter**  |   3.50 |   4.79 |   5.85 |       3.60 |   4.77 |   5.85 |   3.61 |   4.78 |   5.68 |
|**box\_met**  |   7.61 |  10.84 |  13.79 |       8.40 |  12.07 |  17.89 |   8.92 |  11.43 |  17.93 |
|**p2at\_met**  |   9.82 |  12.75 |  17.48 |       8.43 |  13.13 |  21.25 |   8.69 |  12.97 |  19.59 |
|**planetary\_map**  |  11.33 |  15.52 |  21.16 |      31.09 |  46.49 |  67.82 |  31.92 |  47.25 |  67.94 |
|**pioneer\_slam**  |  11.74 |  18.76 |  30.26 |      11.77 |  18.76 |  30.29 |  11.77 |  18.76 |  30.30 |
|**pioneer\_slam3**  |   7.07 |  12.86 |  16.62 |       7.07 |  12.86 |  16.64 |   7.06 |  12.85 |  16.63 |
|**long\_office\_household** |   9.21 |  20.70 |  41.05 |       9.41 |  20.66 |  41.05 |   9.68 |  20.65 |  41.05 |
|**urban05**   |   2.51 |   3.76 |   5.30 |       1.41 |   1.93 |   3.16 |   2.27 |   3.68 |  11.04 |
|**Total**   |   4.85 |   8.73 |  18.11 |       4.92 |   9.53 |  30.27 |   5.08 |   9.71 |  30.35 |
