from moviepy.editor import VideoFileClip
from PIL import Image

if __name__ == "__main__":
    data_dir = "/media/alan/新增磁碟區/toshiba/ros_projects/scenarios/6/"
    input_file = f"{data_dir}video.mp4"
    video = VideoFileClip(input_file)
    # video_resized = video.resize((640, video.size[1]), Image.BICUBIC)
    video = video.set_fps(10)
    video.write_gif(f"{data_dir}video.gif",
                            program='ffmpeg',
                            opt='optimizeplus',
                            fuzz=10)


