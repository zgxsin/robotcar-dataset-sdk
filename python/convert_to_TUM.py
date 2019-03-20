import os
import sys
import re
import numpy as np
from transform import build_se3_transform

from interpolate_poses import interpolate_vo_poses, interpolate_ins_poses, convert_ins_poses_to_TUM_Format


if __name__ == "__main__":
    import argparse
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    parser = argparse.ArgumentParser(description='Build and display a pointcloud')
    parser.add_argument('--poses_file', type=str, default=None, help='File containing relative or absolute poses')

    args = parser.parse_args()

    #================================================================================================
    #convertion_GX
    convert_ins_poses_to_TUM_Format(args.poses_file)
    # sys.exit() # quitthe program here
    #=============================================================================================