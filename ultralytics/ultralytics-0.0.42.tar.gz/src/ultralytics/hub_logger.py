import json
import sys
from pathlib import Path
from time import time, sleep

from . import __version__
from .config import HUB_API_ROOT
from .yolov5_utils.general import LOGGER, PREFIX, emojis, threaded
from .yolov5_utils.hub_utils import smart_request

IN_COLAB = 'google.colab' in sys.modules


def get_agent():
    pip_version = __version__
    return f'python-{pip_version}-colab' if IN_COLAB else f'python-{pip_version}-local'


class HUBLogger:

    def __init__(self, model_id, auth):
        self.model_id = model_id
        self.api_url = f'{HUB_API_ROOT}/models/{model_id}'
        self.auth_header = auth.get_auth_header()
        self.rate_limits = {'metrics': 3.0, 'ckpt': 900.0, 'heartbeat': 300.0}  # rate limits (seconds)
        self.t = {}  # rate limit timers (seconds)
        self.metrics_queue = {}  # metrics queue
        self.keys = [
            'train/box_loss',
            'train/obj_loss',
            'train/cls_loss',  # train loss
            'metrics/precision',
            'metrics/recall',
            'metrics/mAP_0.5',
            'metrics/mAP_0.5:0.95',  # metrics
            'val/box_loss',
            'val/obj_loss',
            'val/cls_loss',  # val loss
            'x/lr0',
            'x/lr1',
            'x/lr2']  # metrics keys
        self.alive = True  # for heartbeats
        self._heartbeats()  # start heartbeats

    def on_pretrain_routine_start(self, *args, **kwargs):
        # YOLOv5 pretrained routine start
        pass

    def on_pretrain_routine_end(self, *args, **kwargs):
        # Start timer for upload rate limit
        LOGGER.info(emojis(f"{PREFIX}View model at https://hub.ultralytics.com/models/{self.model_id} 🚀"))
        self.t = {'metrics': time(), 'ckpt': time()}  # start timer on self.rate_limit

    def on_fit_epoch_end(self, *args, **kwargs):
        # Upload metrics after val end
        vals, epoch = args[:2]
        self.metrics_queue[epoch] = json.dumps({k: round(float(v), 5) for k, v in zip(self.keys, vals)})  # json string
        if time() - self.t['metrics'] > self.rate_limits['metrics']:
            self._upload_metrics()
            self.t['metrics'] = time()  # reset timer
            self.metrics_queue = {}  # reset queue

    def on_model_save(self, *args, **kwargs):
        # Upload checkpoints with rate limiting
        last, epoch, final_epoch, best_fitness, fi = args[:5]
        is_best = best_fitness == fi
        if time() - self.t['ckpt'] > self.rate_limits['ckpt']:
            LOGGER.info(f"{PREFIX}Uploading checkpoint {self.model_id}")
            self._upload_model(epoch, last, is_best)
            self.t['ckpt'] = time()  # reset timer

    def on_train_end(self, *args, **kwargs):
        # Upload final model and metrics with exponential standoff
        last, best, epoch, results = args[:4]
        LOGGER.info(emojis(f"{PREFIX}Training completed successfully ✅"))
        LOGGER.info(f"{PREFIX}Uploading final {self.model_id}")
        self._upload_model(epoch, best, map=results[3], final=True)  # results[3] is mAP0.5:0.95
        self.alive = False  # stop heartbeats
        LOGGER.info(emojis(f"{PREFIX}View model at https://hub.ultralytics.com/models/{self.model_id} 🚀"))

    # Internal functions ---
    def _upload_metrics(self):
        payload = {"metrics": self.metrics_queue.copy(), "type": "metrics"}
        smart_request(f'{self.api_url}', json=payload, headers=self.auth_header, code=2)

    def _upload_model(self, epoch, weights, is_best=False, map=0.0, final=False):
        # Upload a model to HUB
        file = None
        if Path(weights).is_file():
            with open(weights, "rb") as f:
                file = f.read()
        if final:
            smart_request(f'{self.api_url}/upload',
                          data={"epoch": epoch, "type": "final", "map": map},
                          files={"best.pt": file},
                          headers=self.auth_header,
                          retry=10,
                          timeout=3600,
                          code=4)
        else:
            smart_request(f'{self.api_url}/upload',
                          data={"epoch": epoch, "type": "epoch", "isBest": bool(is_best)},
                          headers=self.auth_header,
                          files={"last.pt": file},
                          code=3)

    @threaded
    def _heartbeats(self):
        while self.alive:
            smart_request(f'{HUB_API_ROOT}/agent/heartbeat/models/{self.model_id}',
                          json={"agent": get_agent()},
                          headers=self.auth_header,
                          retry=0,
                          code=5)
            sleep(self.rate_limits['heartbeat'])
