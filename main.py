
import argparse
import json
import os
import time
import cv2
import numpy as np


class Tracking():
    """Class to handle tracking operations: Create,initialize and update.
    """

    def __init__(self, tracker, first_frame=True):
        self.first_frame = first_frame
        self.tracker = tracker
        # Create OpenCV MultiTracker object
        self.multiTracker = cv2.legacy.MultiTracker_create()

    def init_trackers(self, bboxes_list, frame):
        """Method to create and initialize user-defined opencv tracker over bboxes defined in first frame.

        Args:
            bboxes_list (List): Contains info about each object to track(object name,id and coordinates in format (x_topleft,t_topleft,width,height))
            frame (Numpy ndarray): First image of videofile.

        Returns:
            None
        """
        for bbox_dict in bboxes_list:
            det = bbox_dict['coordinates']
            if self.tracker == 'CSRT':
                self.multiTracker.add(
                    cv2.legacy.TrackerCSRT_create(), frame, det)
            elif self.tracker == 'KCF':
                self.multiTracker.add(
                    cv2.legacy.TrackerKCF_create(), frame, det)

    def update_trackers(self, frame):
        """Method to update tracker object based on the appeareance frame

        Args:
            frame (Numpy ndarray): Current image of videofile.

        Returns:
            current_conditions(List):Dictionary list with current coordinates of tracked objects. Same as json input file.
        """
        ok, bboxes = self.multiTracker.update(frame)
        current_conditions = []
        if ok:
            for id, bbox in enumerate(bboxes):
                current_condition_dict = {
                    'object': 'player', 'id': id, 'coordinates': list(bbox)}
                current_conditions.append(current_condition_dict)
        return current_conditions

    def draw_boxes(self, frame, bboxes_list):
        """Draw bounding boxes over each object in current frame

        Args:
            frame (_type_): Current image of videofile.
            bboxes_list (_type_):Dictionary list with current coordinates of tracked objects. Same as json input file
        """
        for bbox_dict in bboxes_list:
            x, y, w, h = int(
                bbox_dict['coordinates'][0]), int(
                bbox_dict['coordinates'][1]), int(
                bbox_dict['coordinates'][2]), int(
                bbox_dict['coordinates'][3])
            cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (225, 0, 0), 3, 1)
            if self.first_frame:
                cv2.putText(frame, "Ground truth", (75, 75),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                cv2.putText(
                    frame, "Tracking players:{}".format(
                        self.tracker), (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 225, 0), 2)

            cv2.putText(
                frame, "Player id:{}".format(
                    bbox_dict['id']), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        return frame


def main():
    """
    Main file of tracking system.
    """
    # Parsers to handle inputs
    parser = argparse.ArgumentParser(description='Epicio Tracking system')
    parser.add_argument(
        "-i",
        '--input_video',
        type=str,
        default='Inputs\\input.mkv',
        help="path to input video")
    parser.add_argument(
        "-json",
        '--json_file',
        default='Inputs\\initial_conditions.json',
        help="path to input json file")
    parser.add_argument(
        "-t",
        '--tracker',
        choices=[
            "CSRT",
            "KCF"],
        default="KCF",
        help="Choose Opencv tracker")
    args = parser.parse_args()
    print(
        "1 of 8 step: Reading inputs:",
        args.json_file,
        ",",
        args.input_video)
    print("2 of 8 step: Chose OpenCV tracker:", args.tracker)
    # Reading inputs
    input_video_extension = os.path.splitext(args.input_video)[1]
    if input_video_extension in ['.mkv', '.avi', '.mp4', '.mov']:
        cap = cv2.VideoCapture(args.input_video)
    else:
        raise Exception(
            "{} format not supported. Is video?".format(input_video_extension))

    input_jsonfile_extension = os.path.splitext(args.json_file)[1]
    if input_jsonfile_extension == ".json":
        with open(args.json_file, 'r') as f:
            initial_conditions = json.load(f)
    else:
        raise Exception(
            "{} format not supported. Is json file?".format(input_jsonfile_extension))
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out_videoname = 'output_' + args.tracker + '.mkv'
    out_videopath = os.path.join(os.getcwd(), "Output")
    if not os.path.isdir(out_videopath):
        os.mkdir(out_videopath)
        
    out = cv2.VideoWriter(os.path.join(out_videopath,out_videoname), fourcc, 24.0, (1920, 1080))
    # create object tracking
    print("3 of 8 step: Creating multitracker object.")
    multitrack = Tracking(args.tracker)
    # used to record the time when we processed last frame
    prev_frame_time = 0
    # used to record the time at which we processed current frame
    new_frame_time = 0
    # Frames per second list
    fps_list = []
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            if multitrack.first_frame:
                print("Video started")
                print("4 of 8 step: Initializing chosen tracker.")
                multitrack.init_trackers(initial_conditions, frame)
                print("5 of 8 step: Drawing bboxes as ground truth.")
                out_frame = multitrack.draw_boxes(frame, initial_conditions)
                multitrack.first_frame = False
                print("6 of 8 step: Update tracker over frames.")
            else:
                current_conditions = multitrack.update_trackers(frame)
                out_frame = multitrack.draw_boxes(frame, current_conditions)

        else:
            print("Video finished. Exiting ...")
            break

        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        fps_list.append(fps)
        prev_frame_time = new_frame_time
        out.write(out_frame)
        if cv2.waitKey(1) == ord('q'):
            break
    print(
        "7 of 8 step: Compute output video FPS:{}(Frames per second).".format(
            round(
                np.mean(fps_list))))
    print("8 of 8 step: Create output video file.")

    # Release everything if job is finished
    cap.release()
    out.release()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("Total time(seconds): {:.4f}".format((time.time() - start_time)))
