#from torchsummary import summary
from ptflops import get_model_complexity_info
from torchinfo import summary
from torchstat import stat
import utility
import data
import model
import loss
from option import args
from trainer import Trainer
import torch
from thop import profile

torch.manual_seed(args.seed)
checkpoint = utility.checkpoint(args)

# 导入模型，输入一张输入图片的尺寸
#summary(cnn.cuda(), input_size=(1, 28, 28), batch_size=-1)
batch_size = 1
_model = model.Model(args, checkpoint)

macs, params = get_model_complexity_info(_model.model, (1, 48,48), as_strings=True, print_per_layer_stat=False, verbose=True)
print('{:<30}  {:<8}'.format('Computational complexity: ', macs))
print('{:<30}  {:<8}'.format('Number of parameters: ', params))


# summary(_model.model, input_size=(batch_size, 3, 96, 96)) # x2-96, x3-64,x4-48
input = torch.randn(1, 1, 48, 48).cuda()
flops, params = profile(_model.model, inputs=(input, ))
print('flops: ', flops, 'params: ', params)
print('flops: %.2f M, params: %.2f M' % (flops / 1000000.0, params / 1000000.0))