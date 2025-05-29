from src.videotoframes import Framer
from src.framestovideo import play_frames_images
from src.imagestocartoon import Cartoonizer
import os, shutil
import glob
import cv2
import re
from pathlib import Path

def natural_sort(file_list):
    """Fix Windows-style sorting of numbered files"""
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(file_list, key=alphanum_key)

def process_video(video_path, output_path, fps):
    """Main process to convert video to cartoon style"""
    # Step 1: Extract frames from video
    print(f"Extracting frames from {video_path}...")
    framer = Framer(video_path, output_path, fps)
    framer.get_frames()
    
    # Step 2: Find extracted frames
    base_dir = os.path.dirname(os.path.abspath(__file__))
    frames_dir = Path(base_dir) / output_path
    jpg_frames = sorted(glob.glob(str(frames_dir / '*.jpg')))
    
    if not jpg_frames:
        print("No frames found! Check your input paths.")
        return
    
    # Step 3: Set up cartoonizer and output folder
    print(f"Found {len(jpg_frames)} frames. Starting cartoon conversion...")
    canvas = Cartoonizer()
    cartoon_dir = Path(base_dir) / f"{output_path}_cartoon"
    if not os.path.exists(cartoon_dir):
        os.makedirs(cartoon_dir)
    
    # Step 4: Convert frames to cartoon style
    for i, frame in enumerate(jpg_frames):
        # Show progress indication
        progress = (i / len(jpg_frames)) * 100
        print(f"\rConverting frames to cartoon: {progress:.1f}% complete", end="")
        cartoon = canvas.render(frame)
        # Pad with zeros for proper sorting (adjust padding based on expected max frames)
        cv2.imwrite(os.path.join(cartoon_dir, f"cartoon_{i:04d}.png"), cartoon)
    
    # Step 5: Create video from cartoon frames
    cartoon_frames = natural_sort(glob.glob(str(cartoon_dir / '*.png')))
    play_frames_images(cartoon_frames, fps, f'output.mp4')

if __name__ == "__main__":
    video_path = input("Video Path: ")
    output_path = input("Output Path of frames: ")
    fps = int(input("Frames Per Second: "))
    delete_frames = int(input("Should I delete frames after creating video(1 - YES, 2 - NO): "))
    process_video(video_path, output_path, fps)
    
    # Deleting folders created
    if delete_frames:
        shutil.rmtree(output_path)
        shutil.rmtree(f"{output_path}_cartoon")