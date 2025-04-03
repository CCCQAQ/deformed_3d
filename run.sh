# python train.py -s /public/home/xiandaifuwuye/601182/4d_reconstruction/our4d/stable-virtual-camera/work_dirs/demo/img2trajvid_s-prob/car2 -m output/car2 --is_blender 

# python train.py -s /public/home/xiandaifuwuye/601182/4d_reconstruction/4DGaussians/datasets/dnerf/bouncingballs -m output/bouncingballs --eval --is_blender


# python train.py -s ./stable-virtual-camera/work_dirs/demo/img2trajvid_s-prob/car2 -m output/car2s --is_blender

python train.py -s ./stable-virtual-camera/work_dirs/demo/img2trajvid_s-prob/car_spiral -m output/car_spiral2 --is_blender
# python train.py -s ./stable-virtual-camera/work_dirs/demo/img2trajvid_s-prob/car2 -m output/car2_add_depth_aj_lr2 --is_blender

# python render.py -m output/car2 --mode render --skip_test