from moviepy.editor import VideoFileClip

if __name__ == "__main__":
    data_dir = "/home/alan/Videos/"
    file_name = "Screencast 2023-11-29 17:01:22"
    input_file = f"{data_dir}{file_name}.mp4"
    start_time = 15 * 60 + 13
    end_time = 15 * 60 + 48
    video = VideoFileClip(input_file)
    video = video.subclip(start_time, end_time)

    video.write_videofile(f"{data_dir}{file_name}_{start_time}_{end_time}.mp4")