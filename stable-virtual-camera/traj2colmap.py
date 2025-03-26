import json
import numpy as np
from pathlib import Path
import shutil
import os
import subprocess
from scipy.spatial.transform import Rotation
import argparse

def c2w_to_tumpose(c2w):
    """
    Convert a camera-to-world matrix to a tuple of translation and rotation
    
    input: c2w: 4x4 matrix
    output: tuple of translation and rotation (x y z qw qx qy qz)
    """
    # convert input to numpy
    xyz = c2w[:3, -1]
    rot = Rotation.from_matrix(c2w[:3, :3])
    qx, qy, qz, qw = rot.as_quat()
    return xyz, [qw, qx, qy, qz]

def convert_transforms(workdir):
    transforms_path = os.path.join(workdir, "transforms.json")
    with open(transforms_path) as f:
        data = json.load(f)
    
    sparse_custom_dir = os.path.join(workdir, "colmap", "sparse_custom")

    os.makedirs(sparse_custom_dir, exist_ok=True)

    # 创建COLMAP cameras.txt
    with open(os.path.join(sparse_custom_dir, "cameras.txt"), "w") as f:
        f.write("# Camera list\n")
        f.write("# Format: CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]\n")
        camera_id = 1
        for frame in data["frames"]:
            f.write(f"{camera_id} PINHOLE {frame['w']} {frame['h']} "
                    f"{frame['fl_x']} {frame['fl_y']} {frame['cx']} {frame['cy']}\n")
            camera_id += 1

    # 创建COLMAP images.txt
    with open(os.path.join(sparse_custom_dir, "images.txt"), "w") as f:
        for idx, frame in enumerate(data["frames"], 1):
            image_name = os.path.basename(frame["file_path"])
            c2w = np.array(frame["transform_matrix"])
            c2w = np.vstack([c2w, [0, 0, 0, 1]])
            xyz, [qw, qx, qy, qz] = c2w_to_tumpose(c2w)
            # IMAGE_ID QW QX QY QZ TX TY TZ CAMERA_ID NAME
            f.write(f"{idx} {qw} {qx} {qy} {qz} {xyz[0]} {xyz[1]} {xyz[2]} {idx} {image_name}\n\n")
    
    # 创建COLMAP points3D.txt(空的)
    with open(os.path.join(sparse_custom_dir, "points3D.txt"), "w") as f:
        pass
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", type=str, default="./work_dirs/demo/img2trajvid_s-prob/00000/")
    args = parser.parse_args()
    convert_transforms(args.workdir)
