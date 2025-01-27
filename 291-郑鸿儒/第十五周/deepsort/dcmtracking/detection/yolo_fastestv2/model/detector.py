import torch
import torch.nn as nn

from dcmtracking.detection.yolo_fastestv2.model.fpn import *
from dcmtracking.detection.yolo_fastestv2.model.backbone.shufflenetv2 import *

class Detector(nn.Module):
    def __init__(self, classes, anchor_num, load_param, export_onnx = False):
        super(Detector, self).__init__()
        out_depth = 72
        stage_out_channels = [-1, 24, 48, 96, 192]

        self.export_onnx = export_onnx
        self.backbone = ShuffleNetV2(stage_out_channels, load_param)
        self.fpn = LightFPN(stage_out_channels[-2] + stage_out_channels[-1], stage_out_channels[-1], out_depth)

        self.output_reg_layers = nn.Conv2d(out_depth, 4 * anchor_num, 1, 1, 0, bias=True)
        self.output_obj_layers = nn.Conv2d(out_depth, anchor_num, 1, 1, 0, bias=True)
        self.output_cls_layers = nn.Conv2d(out_depth, classes, 1, 1, 0, bias=True)

    def forward(self, x):
        C2, C3 = self.backbone(x)
        cls_2, obj_2, reg_2, cls_3, obj_3, reg_3 = self.fpn(C2, C3)
        
        out_reg_2 = self.output_reg_layers(reg_2)
        out_obj_2 = self.output_obj_layers(obj_2)
        out_cls_2 = self.output_cls_layers(cls_2)

        out_reg_3 = self.output_reg_layers(reg_3)
        out_obj_3 = self.output_obj_layers(obj_3)
        out_cls_3 = self.output_cls_layers(cls_3)
        
        if self.export_onnx:
            out_reg_2 = out_reg_2.sigmoid()
            out_obj_2 = out_obj_2.sigmoid()
            out_cls_2 = F.softmax(out_cls_2, dim = 1)

            out_reg_3 = out_reg_3.sigmoid()
            out_obj_3 = out_obj_3.sigmoid()
            out_cls_3 = F.softmax(out_cls_3, dim = 1)

            print("export onnx ...")
            return torch.cat((out_reg_2, out_obj_2, out_cls_2), 1).permute(0, 2, 3, 1), \
                   torch.cat((out_reg_3, out_obj_3, out_cls_3), 1).permute(0, 2, 3, 1)  

        else:
            return out_reg_2, out_obj_2, out_cls_2, out_reg_3, out_obj_3, out_cls_3

if __name__ == "__main__":
    model = Detector(80, 3, False)
    test_data = torch.rand(1, 3, 352, 352)
    torch.onnx.export(model,
                     test_data,
                     "test.onnx",
                     export_params=True,
                     opset_version=11,
                     do_constant_folding=True)
    


