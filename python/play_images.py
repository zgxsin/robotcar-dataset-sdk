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

import argparse
import os
import re
import matplotlib.pyplot as plt
from datetime import datetime as dt
from image import load_image
from camera_model import CameraModel
from PIL import Image

parser = argparse.ArgumentParser(description='Play back images from a given directory')

parser.add_argument('--images_dir', type=str, help='Directory containing images.')
parser.add_argument('--models_dir', type=str, default=None, help='(optional) Directory containing camera model. If supplied, images will be undistorted before display')
parser.add_argument('--scale', type=float, default=1.0, help='(optional) factor by which to scale images before display')

args = parser.parse_args()

camera = re.search('(stereo|mono_(left|right|rear))', args.images_dir).group(0)

timestamps_path = os.path.join(os.path.join(args.images_dir, os.pardir, camera + '.timestamps'))
if not os.path.isfile(timestamps_path):
  timestamps_path = os.path.join(args.images_dir, os.pardir, os.pardir, camera + '.timestamps')
  if not os.path.isfile(timestamps_path):
      raise IOError("Could not find timestamps file")

model = None
if args.models_dir:
    model = CameraModel(args.models_dir, args.images_dir)

current_chunk = 0
timestamps_file = open(timestamps_path)
path_to_write = os.path.join(args.images_dir, os.pardir, "recified")
if os.path.exists(path_to_write):
    pass
else:
    os.mkdir(path_to_write)
print(path_to_write)
files = os.listdir(args.images_dir)
num_files = len(files)
for id, line in enumerate(timestamps_file):
    tokens = line.split()
    datetime = dt.utcfromtimestamp(int(tokens[0])/1000000)
    chunk = int(tokens[1])

    filename = os.path.join(args.images_dir, tokens[0] + '.png')
    if not os.path.isfile(filename):
        if chunk != current_chunk:
            print("Chunk " + str(chunk) + " not found")
            current_chunk = chunk
        continue

    current_chunk = chunk

    img = load_image(filename, model)
    # print(type(img))
    img = Image.fromarray(img)
    # print(type(img))
    img.save(os.path.join(path_to_write, tokens[0] + '.png'))
    print("Processing {0}/{1} image".format(id+1, num_files))
    # plt.imshow(img)
    # plt.xlabel(datetime)
    # plt.xticks([])
    # plt.yticks([])
    # plt.pause(0.01)
