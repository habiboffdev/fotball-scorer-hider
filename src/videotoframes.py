from datetime import timedelta
import cv2
import numpy as np
import os

class Framer:
    """Extracts frames from a video at specified intervals"""
    
    def __init__(self, video_path, output_path, fps):
        # Save the paths and target framerate
        self.video_path = video_path
        self.output_path = output_path
        self.fps = fps
        
        # Open up the video file
        self.cap = cv2.VideoCapture(self.video_path)
        
        # Make sure we have somewhere to save the frames
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
    
    def format_timedelta(self, td):
        """Format a timedelta into a filename-friendly string"""
        result = str(td)
        try:
            result, ms = result.split(".")
        except ValueError:
            # Handle case with no milliseconds
            return (result + ".00").replace(":", "-")
            
        # Format milliseconds nicely
        ms = int(ms)
        ms = round(ms / 1e4)
        return f"{result}.{ms:02}".replace(":", "-")
    
    def frame_lengths(self):
        """Calculate the timestamps for frames to be extracted"""
        frames = []
        duration = self.cap.get(cv2.CAP_PROP_FRAME_COUNT) / self.cap.get(cv2.CAP_PROP_FPS)
        for i in np.arange(0, duration, 1 / self.fps):
            frames.append(i)
        return frames
    
    def get_frames(self):
        """Extract frames from the video"""
        fps_of_video = self.cap.get(cv2.CAP_PROP_FPS)
        print(f"Video FPS: {fps_of_video}")
        self.fps = min(self.fps, fps_of_video)
        frames = self.frame_lengths()
        
        cnt = 0
        result = []
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            duration = cnt / fps_of_video
            try:
                closest_dur = frames[0]
            except IndexError:
                break
            if duration >= closest_dur:
                file, _ = os.path.splitext(os.path.basename(self.video_path))
                duration_ = self.format_timedelta(timedelta(seconds=duration))
                cv2.imwrite(os.path.join(self.output_path, file) + f"-{duration_}.jpg", frame)
                result.append(frame)
                try:
                    frames.pop(0)
                except IndexError:
                    break
            cnt += 1
        self.cap.release()
        print(f"Extracted {len(result)} frames")
        return result

if __name__ == "__main__":
    video_path = input("Video Path: ")
    output_path = input("Output Path: ")
    fps = int(input("Frames Per Second: "))
    framer = Framer(video_path, output_path, fps)
    framer.get_frames()
