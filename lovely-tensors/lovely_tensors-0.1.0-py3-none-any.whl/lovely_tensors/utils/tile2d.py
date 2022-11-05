# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/03c_utils.tile2d.ipynb.

# %% auto 0
__all__ = ['tile_images']

# %% ../../nbs/03c_utils.tile2d.ipynb 4
from math import floor, ceil, log2

from matplotlib import colormaps
from matplotlib.colors import to_rgba, ListedColormap
import torch
from torch.nn.functional import embedding, pad

from ..repr_rgb import RGBProxy

# %% ../../nbs/03c_utils.tile2d.ipynb 9
def fit_columns(t: torch.Tensor, # Tensor with images. 4-dim, ch-last: batch,y,x,ch
                view_width=966):
    """Find out how many colums and rows to use to display the images"""
    
    assert t.dim() == 4
    # Let's figure out how many images can we put in a row without the need for
    # re-scaling. Let's try to keep the number as power or 2 if we have to have
    # multiple rows.
    
    n_img = t.shape[0]
    width = t.shape[-2]
    
    n_cols = 2**floor(log2((view_width / width)))

    # At least 1 image per row, even if it does not fit the view without rescaling.
    n_cols = max(1, n_cols)

    # But if we actually don't have enough images to fill a single
    # power-of-two row, just display as many as we got.
    n_cols = min(n_img, n_cols)
    
    n_rows = ceil(n_img / n_cols) # Last row might have free space.
    
    return (n_rows, n_cols)

# %% ../../nbs/03c_utils.tile2d.ipynb 11
def tile_images(t:torch.Tensor, # Tensor containing images, shape=[n,h,w,c]
                view_width=966):  # Try to protuce an images at most this wide
    """
    Tile images in a grid.
    """
    assert t.dim() == 4
    assert t.shape[-1] in (3, 4) # Either RGB or RGBA.

    
    n_images = t.shape[0]
    n_channels = t.shape[-1]
    xy_shape = t.shape[1:3]

    n_rows, n_cols = fit_columns(t, view_width=view_width)

    
    # We need to form the images inro a rectangular area. For this, we might
    # need to add some dummy images to the last row, whoch might be not full.
    n_extra_images = n_rows*n_cols - t.shape[0]
    if n_extra_images:
        extra_images = torch.ones((n_extra_images, *t.shape[1:]))
        t = torch.cat([ t, extra_images ])
    
    # This is where the fun begins! Imagine 't' is tensor[20, 128, 128, 3].
    # and we want 5 rows, 4 columns each.
    
    t = t.reshape(n_rows, n_cols, *t.shape[-3:])
    # Now t is tensor[5, 4, 128, 128, 3]

    t = t.permute(0, 2, 1, 3, 4)
    # now t is tensor[5, 128, 4, 128, 3]
    # If we just squick dimensions 0,1 and 2,3 togerther, we get the image we want.
    t = t.reshape(n_rows*xy_shape[0], n_cols*xy_shape[1], n_channels)
    
    # Now t is tensor[640, 512, 3], channel-last.
    
    return t
