from skimage.transform import resize
from skimage.segmentation import slic
from skimage.color import label2rgb

def image_to_draw(image):
    image_segments = slic(image, n_segments = 100, compactness = 10)
    return label2rgb(image_segments, image, kind = 'avg')

def resize_image(image, proportion):
    # Limitation
    assert 0 <= proportion <= 1, "Specify a valid proportion between 0 and 1"

    height = round(image.shape[0] * proportion)
    width = round(image.shape[1] * proportion)
    image_resized = resize(image, (height, width), anti_aliasing = True)

    return image_resized