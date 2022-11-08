from sklearn.manifold import TSNE
def tsne(x_data, dim_reduc):
    model = TSNE(n_components = dim_reduc, init = 'random', random_state = 0, 
            learning_rate = 'auto', n_iter = 1000,
            perplexity = 50)
    return model.fit_transform(x_data)
