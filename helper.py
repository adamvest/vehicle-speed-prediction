import torch
from torch import nn
from params import par


#calculate MSE of model predictions on GT speed data
def evaluate_predictions(preds, split_name):
    gt_speeds_file = open("./data/%s.txt" % split_name, "r")
    gt_speeds = gt_speeds_file.readlines()
    gt_speeds = [float(pred) for pred in gt_speeds]
    gt_speeds = torch.FloatTensor(gt_speeds)
    gt_speeds_file.close()
    return torch.mean((preds - gt_speeds) ** 2)


#store evaluation predictions in text file
def write_predictions(preds, split_name):
    with open("./data/%s.txt" % split_name, "w") as preds_file:
        for pred in preds.data:
            preds_file.write("%f\n" % float(pred))


#weight initialization for 3D Resnet model
def initialize_weights(resnet):
    for m in resnet.modules():
        if isinstance(m, nn.Conv3d) or isinstance(m, nn.Linear):
            nn.init.kaiming_normal_(m.weight.data)

            if m.bias is not None:
                m.bias.data.zero_()

        elif isinstance(m, nn.BatchNorm3d) or isinstance(m, nn.BatchNorm1d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()


#load pretrained weights, excluding necessary layers for finetuning
def load_weights(model):
    pretrained_dict = torch.load(par.load_model_path)

    if par.model == "deepvo" and par.load_base_deepvo:
        if par.use_optical_flow or par.use_both:
            raise ValueError("Pretrained DeepVO cannot handle optical flow!")

        model_dict = model.base_model.state_dict()
        exclude, strict = [], True

        if par.load_conv_only:
            exclude.append("rnn")
            strict = False
        elif par.img_w != 608 or par.img_h != 184:
            exclude.append("rnn.weight_ih_l0")
            strict = False

        if par.num_channels != 6:
            exclude.append("conv1")
            strict = False

        if strict == True:
            filtered_dict = {k: v for k, v in pretrained_dict.items()
                if k in model_dict}
        else:
            filtered_dict = {}

            for k, v in pretrained_dict.items():
                excluded = False

                if k in model_dict:
                    for name in exclude:
                        if k.startswith(name):
                            excluded = True
                            break

                if not excluded:
                    filtered_dict[k] = v

        model.base_model.load_state_dict(filtered_dict, strict=strict)
    else:
        model.load_state_dict(pretrained_dict)
