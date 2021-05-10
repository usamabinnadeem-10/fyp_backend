import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torchvision.transforms as transforms
import numpy as np
from PIL import Image

from .networks.resnet import resnet50, resnet101

class Core:

    # intialize model using trained parameters
    def __init__(self):
        self.num_classes = 576
        self.weights = 'ai\weights\Car_epoch_90.pth'

        self.model = resnet50(num_classes=self.num_classes)

        if self.weights != '':
            try:
                self.model = torch.nn.DataParallel(self.model)
                ckpt = torch.load(self.weights, map_location=torch.device('cpu'))
                self.model.load_state_dict(ckpt['state_dict'])
                print ('!!!load weights success !!! path is ', self.weights)
            except Exception as e:
                print(e)
                print ('!!!load weights failed !!! path is ', self.weights)
        else:
            print('!!!Load Weights PATH ERROR!!!')


    # transform image for model input
    def transform(self, img):
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        scale_size = 336
        crop_size = 224

        data_transform = transforms.Compose([
                transforms.Scale((scale_size,scale_size)),
                transforms.RandomHorizontalFlip(),
                transforms.RandomCrop((crop_size,crop_size)),
                transforms.ToTensor(),
                normalize])
        
        return data_transform(img)


    # load gallery features from the database
    def load_gallery_feats(self, db_feats):
        self.gallery_feats = []

        for arr in db_feats:
            t = torch.FloatTensor(arr)
            t = t.reshape(1, 2048, 1, 1)
            self.gallery_feats.append(t)

        print('load gallery feats success!')
        

    # run function will take query image as argument and return indices of top K matches
    def run(self, query, TopK=10):
        model = self.model
        model.eval()
        
        img = self.transform(query)
        img = img.unsqueeze(0)
        _, query_feats = model(img)

        qf = query_feats
        gf = torch.cat(self.gallery_feats, dim=0)

        m, n = qf.shape[0], gf.shape[0]
        qf = qf.view(m, -1)
        gf = gf.view(n, -1)
        distmat = torch.pow(qf, 2).sum(dim=1, keepdim=True).expand(m, n) + torch.pow(gf, 2).sum(dim=1, keepdim=True).expand(n, m).t()
        distmat.addmm_(1, -2, qf, gf.t())
        distmat = distmat.cpu().detach().numpy()
        
        indices = np.argsort(distmat, axis=1)
        result = indices[:, :TopK]

        return result
