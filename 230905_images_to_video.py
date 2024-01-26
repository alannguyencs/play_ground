import cv2
import os
import glob

height, width = 1080, 1920
data_dir = '/media/alan/新增磁碟區/toshiba/ros_projects/scenarios/8/'
video_fps = 5
image_dir = f"{data_dir}obstacle_velocity/"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(f'{data_dir}video.mp4', fourcc, video_fps, (width, height))
image_paths = sorted(glob.glob(os.path.join(image_dir, '*.png')))
for image_path in image_paths:
    cv_rgb = cv2.imread(image_path)
    # cv_depth = cv2.imread(image_path.replace('rgb', 'depth'))
    # cv_image = cv2.hconcat([cv_rgb, cv_depth])
    video_writer.write(cv_rgb)
video_writer.release()