import abc
from algorithms.algorithm import IAlgorithm


class IClustering(IAlgorithm):

	@abc.abstractmethod
	def get_clusters(self, points):
		"""
		Agrupar elementos en clústeres.
		:param points: elementos/puntos/objetos a agrupar
		:return:
		"""
		raise NotImplementedError


if __name__ == '__main__':
	import cv2 as cv
	import imutils.paths
	import numpy as np
	from algorithms.clustering.cw2 import ClusteringCW2
	from algorithms.descriptors.tatt_mobilenetv1.mobilenetv1 import DescriptorMobileNetV1
	"""
	probar el clustering
	"""
	print('started')
	d = DescriptorMobileNetV1()
	c = ClusteringCW2()
	imgs_dir = "C:\_cosas\Desarrollo\Trabajo\Aplicado\HDL18\datasets\TattooBlood_and_Ink_Tattu_&_Valhalla_Tattoos/resized/"
	imgs_paths = imutils.paths.list_images(imgs_dir)
	feats = []
	for i, img_path in enumerate(imgs_paths):
		img = cv.imread(img_path)
		feat = d.features(img)
		feats.append(feat)
		if i % 10 == 0: print(f'{i}')
	afeats = np.array(feats)
	clusters = c.get_clusters(afeats)
	print(len(feats), len(clusters))

	print('end')
