import torch
from argparse import ArgumentParser
from pytorch_lightning import Trainer
from om_simple_encoder.text_image_dm import TextImageDataModule
from om_simple_encoder import CustomCLIPWrapper
from torchvision.models import resnet50,vit_b_16
from transformers import AutoTokenizer, AutoModel
import om_simple_encoder.clip as clip
from pytorch_lightning.loggers import MLFlowLogger
import timm


mlf_logger = MLFlowLogger(
    experiment_name="CLIP_finetune_text",
    #tracking_uri="http://192.168.1.141:5007"
)


def main(model_name='vit_base_patch16_224', max_epochs=1000, data="brands.json", img_dir="img_dir", batch_size=64, gpus=1):
    parser = ArgumentParser()
    parser.add_argument('--minibatch_size', type=int, default=0)
    #parser = TextImageDataModule.add_argparse_args(parser)
    parser = TextImageDataModule.add_argparse_args(parser)
    parser = Trainer.add_argparse_args(parser)
    hparams = parser.parse_args()
    hparams.data = data
    hparams.img_dir = img_dir
    hparams.batch_size = batch_size

    img_encoder = timm.create_model(model_name,pretrained=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if hparams.minibatch_size < 1:
        hparams.minibatch_size = hparams.batch_size

    model = CustomCLIPWrapper(img_encoder, hparams.minibatch_size)
    dm = TextImageDataModule.from_argparse_args(hparams)
    trainer = Trainer.from_argparse_args(hparams, precision=16, max_epochs=max_epochs)#,logger=mlf_logger)
    trainer.logger.log_hyperparams(hparams)
    trainer.fit(model, dm)


if __name__ == '__main__':
    main()
