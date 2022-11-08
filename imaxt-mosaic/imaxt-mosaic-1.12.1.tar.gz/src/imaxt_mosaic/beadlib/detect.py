import cv2
import numpy as np
import scipy.ndimage as ndi

from dask import delayed
from scipy.stats import median_abs_deviation


@delayed
def detect_beads(
    img,
    return_type="circles",
    min_separation=60,
    min_radius=60,
    max_radius=150,
    max_area=100_000,
):
    """Detect beads in image using HoughCircles"""

    img = ndi.gaussian_filter(img, 3)

    img = (img - img.min()) / img.max() * 255

    median = np.median(img)
    mad = median_abs_deviation(img.flatten(), scale="normal")
    threshold = median + 5 * mad
    mask = (
        ndi.binary_dilation(img > threshold, iterations=3) * 1
        - ndi.binary_erosion(img > threshold, iterations=3) * 1
    )
    img = ndi.binary_fill_holes(mask)
    img = ndi.binary_opening(img, iterations=10)
    img = ndi.binary_closing(img, iterations=10)

    img = img * 255
    img = ndi.gaussian_filter(img, 3)
    img = img / img.max() * 255

    img = img.astype("uint8")

    if return_type == "image":
        return img

    analysis = cv2.connectedComponentsWithStats(img, 4, cv2.CV_16U)
    (totalLabels, label_ids, values, centroid) = analysis

    output = np.zeros(img.shape, dtype="uint8")
    for i in range(1, totalLabels):
        area = values[i, cv2.CC_STAT_AREA]
        if area < max_area:
            componentMask = (label_ids == i).astype("uint8") * 255
            output = cv2.bitwise_or(output, componentMask)

    if return_type == "mask":
        return output

    circles = cv2.HoughCircles(
        output,
        cv2.HOUGH_GRADIENT,
        1,
        min_separation,
        param1=150,
        param2=15,
        minRadius=min_radius,
        maxRadius=max_radius,
    )
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")

    return circles
