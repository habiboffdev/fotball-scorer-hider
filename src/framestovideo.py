import cv2
import glob
from pathlib import Path
import os

def play_frames_images(frames, fps, output_video_path):
    """Create a video from a list of image paths"""
    if not frames:
        print("No frames provided to create video!")
        return
    
    # Get dimensions from the first frame
    frame = cv2.imread(frames[0])
    height, width, _ = frame.shape
 
    # Set up the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4 codec
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
 
    # Add each frame to the video
    print(f"\nCreating video from {len(frames)} frames at {fps} FPS...")
    for i, frame_path in enumerate(frames):
        frame = cv2.imread(frame_path)
        video_writer.write(frame)
        
        # Progress update every 10%
        if i % max(1, len(frames) // 10) == 0:
            print(f"Processing: {i}/{len(frames)} frames")
 
    video_writer.release()
    print(f"Video saved to {output_video_path}")
 
def play_frames_from_list(frames, fps, output_video_path, frame_processor):
    """Create a video from a list of frames with optional processing"""
    if not frames:
        print("No frames provided to create video!")
        return
    
    # Get dimensions from the first frame
    frame = cv2.imread(frames[0])
    height, width, _ = frame.shape

    # Set up the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4 codec
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
 
    # Process and add each frame to the video
    for frame in frames:
        processed_frame = frame_processor(frame)
        video_writer.write(processed_frame)

    video_writer.release()
    print(f"Video saved to {output_video_path}")

if __name__ == "__main__":
    # Example usage when run as standalone script
    frames_dir = Path(os.path.dirname(os.path.abspath(__file__))) / "images"
    fps = 15
    output_video_path = 'output.mp4'
    
    # Get all JPG images
    frames = sorted(glob.glob(str(frames_dir / '*.jpg')))
    
    if frames:
        play_frames_images(frames, fps, output_video_path)
    else:
        print(f"No frames found in {frames_dir}")
