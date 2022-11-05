import dataclasses
import pathlib
import torch
import irisml.core


class Task(irisml.core.TaskBase):
    """Save the model's state_dict to the specified file."""
    VERSION = '0.1.1'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Inputs:
        model: torch.nn.Module

    @dataclasses.dataclass
    class Config:
        path: pathlib.Path

    def execute(self, inputs):
        state_dict = inputs.model.state_dict()
        self.config.path.parent.mkdir(exist_ok=True, parents=True)
        torch.save(state_dict, self.config.path)
        return self.Outputs()
