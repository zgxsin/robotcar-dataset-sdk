################################################################################
#
# Copyright (c) 2017 University of Oxford
# Authors:
#  Geoff Pascoe (gmp@robots.ox.ac.uk)
#
# This work is licensed under the Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc-sa/4.0/ or send a letter to
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
#
################################################################################

import os
import sys
import re
import numpy as np
from transform import *

from interpolate_poses import interpolate_vo_poses, interpolate_ins_poses

if __name__ == "__main__":
    import argparse
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser(description='Build and display a pointcloud')
    parser.add_argument('--poses_file_folder', type=str, default=None, help='Folder containing relative or absolute poses')
    parser.add_argument('--pose_timestamps', type=str, default=None,
                        help='Directory containing frame timestampes')

    args = parser.parse_args()

    ins_path = os.path.join(args.poses_file_folder, "ins.csv")
    path_to_write = os.path.join(args.poses_file_folder, "groundtruth.txt")


    timestamps_path = args.pose_timestamps
    with open(timestamps_path) as timestamps_file:
        start_time = int(next(timestamps_file).split(' ')[0])

    timestamps = []
    with open(timestamps_path) as timestamps_file:
        for line in timestamps_file:
            timestamp = int(line.split(' ')[0])
            timestamps.append(timestamp)

    if len(timestamps) == 0:
        raise ValueError("No LIDAR data in the given time bracket.")

    origin_timestamps = timestamps[:]
    poses_out = interpolate_ins_poses(ins_path, timestamps, start_time)
    # abs_quaternions = np.zeros((4, len(poses_out)))
    # abs_positions = np.zeros((3, len(poses_out)))
    abs_poses_TumForamt = []

    for i, pose in enumerate(poses_out):
        # abs_positions[:, i] = np.ravel(poses_out[i][0:3, 3])
        # abs_quaternions[:, i] = so3_to_quaternion_GX(poses_out[i][0:3, 0:3])
        abs_poses_TumForamt.append([int(origin_timestamps[i])] + poses_out[i][0:3, 3].transpose().tolist()[0] + so3_to_quaternion_GX(poses_out[i][0:3, 0:3]))


    with open(path_to_write, 'w') as file:
        for id, item in enumerate(abs_poses_TumForamt):
            for entry in item:
                file.write("%s "%entry)
            file.write('\n')


