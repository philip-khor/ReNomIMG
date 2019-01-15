import os
import numpy as np
import inspect
import pytest
import types

from renom.cuda import set_cuda_active, release_mem_pool

from renom_img.api.detection.yolo_v1 import Yolov1
from renom_img.api.detection.yolo_v2 import Yolov2, AnchorYolov2
from renom_img.api.detection.ssd import SSD

from renom_img.api.classification.vgg import VGG16, VGG19
from renom_img.api.classification.resnet import ResNet18, ResNet34, ResNet50, ResNet101, ResNet152
from renom_img.api.classification.inception import InceptionV1, InceptionV2, InceptionV3, InceptionV4
from renom_img.api.classification.densenet import DenseNet121, DenseNet169, DenseNet201

from renom_img.api.segmentation.unet import UNet

from renom_img.api.utility.augmentation import Augmentation
from renom_img.api.utility.load import parse_xml_detection


set_cuda_active(True)


@pytest.mark.parametrize("algo", [
    Yolov1,
    Yolov2,
    SSD,
    VGG16,
    VGG19,
    ResNet18,
    ResNet34,
    ResNet50,
    ResNet101,
    ResNet152,
])
def test_weight_download(algo):
    path = algo.__name__ + ".h5"
    model = algo(load_pretrained_weight=True)
    model.save(path)
    model.load(path)
    os.remove(path)
