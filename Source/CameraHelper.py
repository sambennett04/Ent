from picamera import PiCamera
from time import sleep
from json import dumps, load
from datetime import datetime

import os.path

CONFIGURATION_PATH = os.path.join("Configuration", "CameraConfiguration.json")

class CameraHelper(object):

    def __init__(self):

        jsonObj = self.__get_config()

        self.camera = PiCamera()
        self.camera.rotation = self.__get_camera_rotation(jsonObj)
        self.photoPath = self.__get_photo_path(jsonObj)
        self.videoPath = self.__get_video_path(jsonObj)
        self.videoDuration = self.__get_video_duration(jsonObj)

    def __str__(self):

        return dumps(str(self.__dict__))
    
    def __get_config(self):

        jsonFile = open(CONFIGURATION_PATH, "r")
        jsonObj = load(jsonFile)
        jsonFile.close()

        return jsonObj

    def __get_camera_rotation(self, jsonObj):

        cameraRotation = jsonObj["camera_rotation"]

        return cameraRotation

    def __get_photo_path(self, jsonObj):

        photoPath = jsonObj["picture_storage"]

        return photoPath

    def __get_video_path(self, jsonObj):

        videoPath = jsonObj["video_storage"]

        return videoPath

    def __get_video_duration(self, jsonObj):

        videoDuration = jsonObj["video_duration"]

        return videoDuration

    def take_default_picture(self):

        path = self.photoPath
        path = path + "/" + self.get_date_string()
        realPath = self.take_picture(path)

        return realPath
    
    def take_default_video(self):

        self.camera.start_preview()

        path = self.videoPath
        path = path + "-" + self.get_date_string()
        duration = self.videoDuration
        realPath = self.take_video(path, duration)

        return realPath

    def get_date_string(self):

        now = datetime.now()
        dateString = now.strftime("%Y-%m-%d-%H:%M:%S")

        return dateString

    def take_picture(self, filePath):

        # check if path is null
        # check if path is writable

        if not filePath:

            raise Exception("the value of filepath must be well-formed and not null.")
        
        self.camera.annotate_text = self.get_date_string()
        filePathWithExtension = filePath + ".jpg"

        sleep(2)

        try:

            self.camera.capture(filePathWithExtension)

        except Exception as e:

            print("WARNING: Failed to take picture. Go to CameraHelper.take_picture.")
            print("ERROR: {}".format(str(e)))

        return filePathWithExtension
    
    def take_video(self, filePath, duration):

        # check if path is null
        # check if path is writable

        if not filePath:

            raise Exception("the value of filepath must be well-formed and not null.")

        self.camera.annotate_text = self.get_date_string()
        filePathWithExtension = filePath + ".h264"

        try:
            self.camera.start_recording(filePathWithExtension)
            sleep(duration)
            self.camera.stop_recording()

        except Exception as e:

            print("WARNING: Failed to take video. Go to CameraHelper.take_video.")
            print("ERROR: {}".format(str(e)))

        return filePathWithExtension

if __name__ == "__main__":

    ch = CameraHelper()
    print(str(ch))

    print("taking video for {} seconds".format(str(ch.videoDuration)))
    videoPath = ch.take_default_video()
    print("video available at {}".format(videoPath))
    
    print("taking picture")
    picturePath = ch.take_default_picture()
    print("picture available at {}".format(picturePath))