from typing import TypeVar, Callable

import torch

from machine_learning.recommending.interface import SparseTensor

Distance = TypeVar(
    "Distance", bound=Callable[[torch.Tensor, torch.Tensor], torch.Tensor]
)


def cosine_distance(
    left: torch.Tensor or SparseTensor, right: torch.Tensor or SparseTensor
) -> torch.Tensor:
    """
    Given two matrices: left of shape [n, d] and right of shape [m, d],
    containing in rows vectors from d-dimensional space, returns matrix S
    of shape [n, m], where S[i, j] = cosine distance between left[i] and right[j].
    """

    def safe_norm(tensor):
        if tensor.is_sparse:
            norm = torch.sqrt(torch.sparse.sum(tensor**2, dim=1)).to_dense()
        else:
            norm = torch.sqrt(torch.sum(tensor**2, dim=1))
        return torch.maximum(torch.tensor(torch.finfo().eps), norm)

    similarity = (left @ right.transpose(0, 1)).to_dense()
    similarity /=safe_norm(left).reshape(-1, 1)
    similarity /=safe_norm(right).reshape(1, -1)
    return 1 - similarity
