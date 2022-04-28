import numpy as np

def parse_benchmark_row(row):
    problem_id = row['id']

    source_pcd_filename = row['source']
    
    target_pcd_filename = row['target']

    source_transform = np.eye(4)
    source_transform[0][0] = row['t1']
    source_transform[0][1] = row['t2']
    source_transform[0][2] = row['t3']
    source_transform[0][3] = row['t4']
    source_transform[1][0] = row['t5']
    source_transform[1][1] = row['t6']
    source_transform[1][2] = row['t7']
    source_transform[1][3] = row['t8']
    source_transform[2][0] = row['t9']
    source_transform[2][1] = row['t10']
    source_transform[2][2] = row['t11']
    source_transform[2][3] = row['t12']

    return problem_id, source_pcd_filename, target_pcd_filename, source_transform