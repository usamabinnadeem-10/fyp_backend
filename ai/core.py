import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn

from networks.resnet import resnet50, resnet101

class Core:
    def __init__(self):
        self.num_classes = 576
        self.weights = './weights/Car_epoch_90.pth'

        self.model = resnet50(num_classes=self.num_classes)

        if weights != '':
            try:
                model = torch.nn.DataParallel(model)
                ckpt = torch.load(weights, map_location=torch.device('cpu'))
                model.load_state_dict(ckpt['state_dict'])
                print ('!!!load weights success !!! path is ', weights)
            except Exception as e:
                print(e)
                print ('!!!load weights failed !!! path is ', weights)
        else:
            print('!!!Load Weights PATH ERROR!!!')

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

    def backend_api(self, query, model, gallery_feats, TopK=20):
        model.eval()
        
        img = Image.open(query).convert('RGB')
        img = self.transform(img)
        img = img.unsqueeze(0)
        _, query_feats = model(img)

        qf = query_feats
        gf = torch.cat(gallery_feats, dim=0)

        m, n = qf.shape[0], gf.shape[0]
        qf = qf.view(m, -1)
        gf = gf.view(n, -1)
        distmat = torch.pow(qf, 2).sum(dim=1, keepdim=True).expand(m, n) + torch.pow(gf, 2).sum(dim=1, keepdim=True).expand(n, m).t()
        distmat.addmm_(1, -2, qf, gf.t())
        distmat = distmat.cpu().detach().numpy()
        
        indices = np.argsort(distmat, axis=1)
        result = indices[:, :TopK]

        return result


print('success')
