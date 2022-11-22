import Engine
VIDEO_PATH="Coke inspection2021_08_19_12_52_5.mp4"
FRAME="FRAMES"
RUST="RUST"
MARKED="MARKED"
EDGE="EDGE"
CRACK="CRACK"

Engine.logger(VIDEO_PATH,True)
Engine.VIdeo_to_Image(VIDEO_PATH)
Engine.Removing_Unwanted(FRAME)
Engine.Image_to_Rust(FRAME)
Engine.Edge_Generator(RUST)
Engine.Mark(EDGE)
Engine.Image_to_Video(MARKED,RUST)
Engine.Crack_Detection(FRAME)
Engine.Edge_Generator(CRACK)
Engine.Mark(EDGE)
Engine.Image_to_Video(MARKED,CRACK)
Engine.logger(VIDEO_PATH,False)
print("[********COMPLETED********]")
