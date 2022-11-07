import numpy as np
from skimage.color import rgb2gray
# Converte uma imagem RGB de 3 canais em uma imagem monocromática de um canal.
# É como se fosse um filtro de 'branco e preto'
from skimage.exposure import match_histograms
# Manipula os pixels de uma imagem de entrada (input) com os pixels de uma imagem de referência.
# Se tiver múltiplos canais (RGB), a manipulação é feita  independente para cada canal, desde que exista o mesmo número de canais.
# É uma manipulação de imagem como se fosse uma normalização, basicamente normalizando a iluminação de cada imagem.
from skimage.metrics import structural_similarity
# Mede o MSE, a difenreça entre as imagens.
def difference(image1, image2, show_score = True, return_score = False):
    '''
    Finding differences between two images, returning a score of similarity.
    '''
    # Limitation:
    gray_image1 = rgb2gray(image1)
    gray_image2 = rgb2gray(image2)
    (score, difference_image) = structural_similarity(gray_image1, gray_image2, full = True)
    if show_score:
        print(f"Similarity of the images: {score}")

    if return_score:
        normalized_difference_image = ((difference_image - 
                                        np.min(difference_image)/(np.max(difference_image) - np.min(difference_image))))
        return normalized_difference_image, score
    
    normalized_difference_image = ((difference_image - 
                                        np.min(difference_image)/(np.max(difference_image) - np.min(difference_image))))
    return normalized_difference_image


def transfer_histogram(image1, image2):
    matched_image = match_histograms(image1, image2, multichannel = True)
    return matched_image

