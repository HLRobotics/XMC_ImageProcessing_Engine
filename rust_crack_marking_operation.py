"""rust_crack_marking_operation.py"""
from XMC_IMG_PRO_Engine import *


class RustCrackDection:
    """Main Operation Class"""

    def __init__(self):

        VIDEO_PATH = ""
        FRAME = "FRAMES"
        RUST = "RUST"
        MARKED = "MARKED"
        EDGE = "EDGE"
        CRACK = "CRACK"
        self.engine = Engine()
        self.engine.logger(VIDEO_PATH, True)
        self.engine.video_to_image(VIDEO_PATH)
        self.engine.selection(FRAME)
        self.engine.image_to_rust_detected_image(FRAME)
        self.engine.edge_generator(RUST)
        self.engine.mark(EDGE)
        self.engine.image_to_video(MARKED, RUST)
        self.engine.Crack_Detection(FRAME)
        self.engine.edge_generator(CRACK)
        self.engine.mark(EDGE)
        self.engine.image_to_video(MARKED, CRACK)
        self.engine.logger(VIDEO_PATH, False)
        print("[********COMPLETED********]")
