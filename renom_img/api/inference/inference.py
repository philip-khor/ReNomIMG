import asyncio
import requests
import urllib.request

import numpy as np
from renom_img.server import ALG_YOLOV1, ALG_YOLOV2, ALG_SSD
from renom_img.api.utility.misc.download import download
from renom_img.api.detection.yolo_v1 import Yolov1
from renom_img.api.detection.yolo_v2 import Yolov2


class Detector(object):

    def __init__(self, url="http://localhost", port='8080'):
        self._pj_id = 1
        self._url = url
        self._port = port
        self._model = None
        self._alg_name = None
        self._model_info = {}

    def pull(self):
        url = self._url + ':' + self._port
        download_weight_api = "/api/renom_img/v1/projects/{}/deployed_model".format(self._pj_id)
        download_param_api = "/api/renom_img/v1/projects/{}/deployed_model_info".format(self._pj_id)
        download_weight_api = url + download_weight_api
        download_param_api = url + download_param_api

        ret = requests.get(download_param_api).json()
        model_name = ret["filename"]

        # TODO: Check algorithm.
        if ret["algorithm"] == ALG_YOLOV1:
            self._alg_name = "Yolov1"
            img_w = ret["hyper_parameters"]["image_width"]
            img_h = ret["hyper_parameters"]["image_height"]
            self._model = Yolov1(imsize=(img_h, img_w))

        elif ret["algorithm"] == ALG_YOLOV2:
            self._alg_name = "Yolov2"
            img_w = ret["hyper_parameters"]["image_width"]
            img_h = ret["hyper_parameters"]["image_height"]
            self._model = Yolov2(imsize=(img_h, img_w))

        if not os.path.exists(filename):
            download(download_weight_api, filename)
        self._model.load(filename)

        self._model_info = {
            "Algorithm": self._alg_name,
            "Image size": "{}x{}".format(img_w, img_h),
            "Num class": "{}".format(self._model._num_class)
        }

    def predict(self, img):
        assert self._model
        return self._model.predict(img)

    @property
    def model_info(self):
        return self._model_info
