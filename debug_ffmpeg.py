import subprocess
import os

try:
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"IMAGEIO_FFMPEG: {ffmpeg_exe}")
    print(f"EXISTS: {os.path.exists(ffmpeg_exe)}")
except Exception as e:
    print(f"IMAGEIO_FFMPEG ERROR: {e}")

try:
    res = subprocess.run(["ffmpeg", "-version"], capture_output=True)
    print(f"SYSTEM FFMPEG: {res.returncode}")
except Exception as e:
    print(f"SYSTEM FFMPEG ERROR: {e}")
