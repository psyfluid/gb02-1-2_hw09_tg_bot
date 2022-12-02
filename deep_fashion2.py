import cv2
# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.data.datasets import register_coco_instances
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import ColorMode, Visualizer


class DeepFashion(object):
    def __init__(self):
        # setup_logger()
        register_coco_instances("deepfashion2_train", {}, "./DeepFashion2/deepfashion2_train.json", "./DeepFashion2")
        register_coco_instances("deepfashion2_val", {}, "./DeepFashion2/deepfashion2_val.json", "./DeepFashion2")

        MetadataCatalog.get("deepfashion2_val").thing_classes = [
            'short_sleeved_shirt', 'long_sleeved_shirt', 'short_sleeved_outwear',
            'long_sleeved_outwear', 'vest', 'sling', 'shorts', 'trousers', 'skirt',
            'short_sleeved_dress', 'long_sleeved_dress', 'vest_dress', 'sling_dress'
        ]

        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        cfg.MODEL.WEIGHTS = "./model/model_0021999.pth"

        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 13

        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.69  # set threshold for this model
        cfg.MODEL.ROI_HEADS.NMS_THRESH_TEST = 0.3
        cfg.MODEL.DEVICE = 'cpu'
        self.predictor = DefaultPredictor(cfg)

    def predict(self, image_file):
        im = cv2.imread(image_file)
        outputs = self.predictor(im)
        v = Visualizer(im[:, :, ::-1],
                       MetadataCatalog.get("deepfashion2_val"),
                       scale=1,
                       instance_mode=ColorMode.IMAGE)
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        new_image_file = image_file.replace('.jpg', '_pred.jpg')
        cv2.imwrite(new_image_file, out.get_image()[:, :, ::-1])
        return new_image_file
