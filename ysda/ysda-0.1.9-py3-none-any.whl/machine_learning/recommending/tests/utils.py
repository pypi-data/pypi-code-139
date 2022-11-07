import numpy as np
import scipy


def random_explicit_feedback(size, density=0.05, max_rating=1):
    ratings = np.arange(max_rating + 1)
    probs = [1 - density] + [density / max_rating] * max_rating
    return scipy.sparse.csr_matrix(np.random.choice(ratings, p=probs, size=size))


def ignore_cuda_error(exception):
    exception_message = str(exception)
    if not (
        exception_message.startswith("cublas error")
        or exception_message.startswith("CURAND error")
    ):
        raise exception
