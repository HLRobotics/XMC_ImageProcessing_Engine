"""Engine.py"""
import cv2
import glob
import os
import numpy as np
from datetime import datetime


class Engine:
    """Rust Engine"""

    def logger(FILE, STATUS):
        """Logger functionality"""
        now = datetime.now()
        file = open("Log.txt", "a")
        if STATUS == True:
            file.write(FILE + "\n")
            file.write("Start TIme: " + str(now) + "\n")
        else:
            file.write("End TIme: " + str(now))
        file.close()

    def edge_generator(DIR_PATH):
        """Generate edge detected Images"""
        count = 0
        for filename in glob.glob(DIR_PATH + "/*.jpg"):
            count = count + 1
            print(filename)
            img = cv2.imread(filename)
            edges = cv2.Canny(img, 100, 200)
            os.path.basename(filename)
            cv2.imwrite("EDGE/" + str(os.path.basename(filename)), edges)
            print("[ ISW Engine:Writing to Edge " + filename + "]")
        return True

    def image_to_video(IMAGE_DIR, NAME):
        """Convert Image Sequence to video Format"""
        img_array = []
        for filename in glob.glob(IMAGE_DIR + "/*.jpg"):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)
        out = cv2.VideoWriter(NAME + "_OUTPUT.avi", cv2.VideoWriter_fourcc(*"DIVX"), 0.5, size)
        for i in range(len(img_array)):
            out.write(img_array[i])
            print("[ ISW ENGINE GENERATING VIDEO ..... ]")

        out.release()
        print("[ ISW ENGINE VIDEO GENERATED ]")
        return True

    def video_to_image(PATH):
        """Convert video to image format"""
        vidcap = cv2.VideoCapture(str(PATH))
        success, image = vidcap.read()
        count = 0
        print("[ ISW ENGINE VIDEO TO IMAGE CONVERTER TOOL ]")
        print("[ Getting ready ...]")

        while success:
            cv2.imwrite("FRAMES/frame%d.jpg" % count, image)
            success, image = vidcap.read()
            count += 1
            print("[ ISW ENGINE Converting Image...FRAMES/frame", str(count) + ".jpg]")
        return True

    def selection(DIR_PATH):
        """Selection process of required images"""
        for root, dirs, files in os.walk(DIR_PATH):
            total_files = len(files)
            count = 0
            file_Count = 0
            print("Total Files to process:" + str(total_files))
            rate = int(input("Enter the selction rate:"))
            for file in files:
                count = count + 1
                if count % rate != 0:
                    os.remove(DIR_PATH + "/" + file)
                    print("Removed :" + file)
                else:
                    print("Saved :" + file)
                    file_Count = file_Count + 1
        return True

    def image_to_rust_detected_image(DIR_PATH):
        """Image to rust detected images"""
        print("[ ISW ENGINE RUST DETECTION TOOL ]")
        print("[ Getting ready ...]")
        count = 0
        for root, dirs, files in os.walk(DIR_PATH):
            for file in files:
                count = count + 1
                img = cv2.imread((DIR_PATH + "/" + file), 1)
                # Set different boundaries for different shades of rust
                boundaries1 = [([58, 57, 101], [76, 95, 162])]
                boundaries2 = [([26, 61, 111], [81, 144, 202])]
                boundaries3 = [([44, 102, 167], [115, 169, 210])]

                # Highlight out the shades of rust
                for (lower1, upper1) in boundaries1:
                    lower1 = np.array(lower1, dtype="uint8")
                    upper1 = np.array(upper1, dtype="uint8")
                    mask = cv2.inRange(img, lower1, upper1)
                    output1 = cv2.bitwise_and(img, img, mask=mask)

                for (lower2, upper2) in boundaries2:
                    lower2 = np.array(lower2, dtype="uint8")
                    upper2 = np.array(upper2, dtype="uint8")
                    mask = cv2.inRange(img, lower2, upper2)
                    output2 = cv2.bitwise_and(img, img, mask=mask)

                for (lower3, upper3) in boundaries3:
                    lower3 = np.array(lower3, dtype="uint8")
                    upper3 = np.array(upper3, dtype="uint8")
                    mask = cv2.inRange(img, lower3, upper3)
                    output3 = cv2.bitwise_and(img, img, mask=mask)

                # Combine the 3 different masks with the different shades into 1 image file
                final = cv2.bitwise_or(output1, output2)
                cv2.imwrite("RUST/" + str(os.path.basename(file)), final)
                print("[ ISW ENGINE Saving Rust Detected Image... " + file + " ]")
        return True

    def tracking_and_marking(filename):
        """Tracking and marking sub function"""
        img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        _, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        xlist = []
        ylist = []
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
            n = approx.ravel()
            i = 0
            for j in n:
                if i % 2 == 0:
                    x = n[i]
                    y = n[i + 1]

                    # String containing the co-ordinates.
                    string = str(x) + " " + str(y)
                    xlist.append(x)
                    ylist.append(y)
                i = i + 1
        return xlist, ylist

    def Crack_Detection(DIR_PATH):
        """Detecting crack in an object"""
        for filename in glob.glob(DIR_PATH + "/*.jpg"):
            img = cv2.imread(filename)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Image processing ( smoothing )
            blur = cv2.blur(gray, (3, 3))
            # Apply logarithmic transform
            img_log = (np.log(blur + 1) / (np.log(1 + np.max(blur)))) * 255
            # Specify the data type
            img_log = np.array(img_log, dtype=np.uint8)
            # Image smoothing: bilateral filter
            bilateral = cv2.bilateralFilter(img_log, 5, 75, 75)
            # Canny Edge Detection
            edges = cv2.Canny(bilateral, 100, 200)
            # Morphological Closing Operator
            kernel = np.ones((5, 5), np.uint8)
            closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
            # Create feature detecting method
            # sift = cv2.xfeatures2d.SIFT_create()
            # surf = cv2.xfeatures2d.SURF_create()
            orb = cv2.ORB_create(nfeatures=1500)
            # Make featured Image
            keypoints, descriptors = orb.detectAndCompute(closing, None)
            featuredImg = cv2.drawKeypoints(closing, keypoints, None)
            cv2.imwrite("CRACK/" + str(os.path.basename(filename)), featuredImg)
            print("[ ISW ENGINE Saving Crack Detected Image... " + filename + " ]")
        return True

    def mark(DIR_PATH):
        """Mark the tracked image"""
        for filename in glob.glob(DIR_PATH + "/*.jpg"):
            Status = False
            fontScale = 1
            font = cv2.FONT_HERSHEY_SIMPLEX
            xList, yList = Tracking_and_Marking(filename)
            mapping = dict(zip(xList, yList))
            for x in mapping.keys():
                x = x
                y = mapping[x]
                if Status == False:
                    FILENAME = os.path.basename(filename)
                    path = "FRAMES/" + FILENAME
                    image = cv2.imread(path)
                    color = (0, 0, 255)
                    thickness = 1
                    # image = cv2.rectangle(image, start_point, end_point, color, thickness)
                    image = cv2.putText(image, "#", (x, y), font, fontScale, color, thickness, cv2.LINE_AA)
                    cv2.imwrite("MARKED/" + FILENAME, image)
                    print("[ ISW ENGINE Marking" + filename + "]")
                    Status = True
                else:
                    path = "MARKED/" + FILENAME
                    image = cv2.imread(path)
                    color = (0, 0, 255)
                    thickness = 1
                    # image = cv2.rectangle(image, start_point, end_point, color, thickness)
                    image = cv2.putText(image, "#", (x, y), font, fontScale, color, thickness, cv2.LINE_AA)
                    cv2.imwrite("MARKED/" + FILENAME, image)
                    print("[ ISW ENGINE Marking" + filename, (x, y), "]")
                    Status = True
        return True
