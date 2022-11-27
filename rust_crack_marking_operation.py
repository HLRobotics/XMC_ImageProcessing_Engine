"""rust_crack_marking_operation.py"""
from XMC_IMG_PRO_Engine import *


class RustCrackDection:
    """Main Operation Class"""

    VIDEO_PATH = "footage.mp4"
    FRAME = "FRAMES"
    RUST = "RUST"
    MARKED = "MARKED"
    EDGE = "EDGE"
    CRACK = "CRACK"

    def __init__(self):
        self.engine = Engine()
        self.engine.logger(self.VIDEO_PATH, True)
        self.engine.video_to_image(self.VIDEO_PATH)
        self.engine.selection(self.FRAME)
        self.engine.image_to_rust_detected_image(self.FRAME)
        self.engine.edge_generator(self.RUST)
        self.engine.mark(self.EDGE)
        self.engine.image_to_video(self.MARKED, self.RUST)
        self.engine.Crack_Detection(self.FRAME)
        self.engine.edge_generator(self.CRACK)
        self.engine.mark(self.EDGE)
        self.engine.image_to_video(self.MARKED, self.CRACK)
        self.engine.logger(self.VIDEO_PATH, False)
        print("[********COMPLETED********]")


task = RustCrackDection()
