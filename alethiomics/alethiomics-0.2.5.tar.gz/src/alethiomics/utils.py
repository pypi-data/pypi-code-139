"""Utils modules used in other modules.
"""
# imports
from scipy.sparse import csr_matrix
from anndata import AnnData
from pandas import Categorical
from numpy.random import poisson, choice, normal, seed, rand
from numpy import float32, log1p
from scipy.sparse import issparse
from scvi import settings, model

def dummy_adata(ncells = 100, ngenes = 2000):
    """Create a dummy AnnData object. This module follows this online tutorial: https://anndata-tutorials.readthedocs.io/en/latest/getting-started.html

    Parameters
    ----------
    ncells: Integer
        Number of cells in the output AnnData object.
    ngenes: Integer
        Number of genes in the output AnnData object.

    Returns
    -------
    adata: AnnData object
        AnnData object with the following fields filled with random values:
            - adata.X
            - adata.obs_names
            - adata.var_names
            - adata.obs["cell_type"]
            - adata.obsm["X_umap"]
            - adata.varm["gene_stuff"]
            - adata.uns["random"]
            - adata.layers["log_transformed"]
    """

    seed(1); rand(1)
    counts = csr_matrix(poisson(1, size=(ncells, ngenes)), dtype=float32)
    adata = AnnData(counts)
    adata.obs_names = [f"Cell_{i:d}" for i in range(adata.n_obs)]
    adata.var_names = [f"Gene_{i:d}" for i in range(adata.n_vars)]
    ct = choice(["B", "T", "Monocyte"], size=(adata.n_obs,))
    adata.obs["cell_type"] = Categorical(ct)  # Categoricals are preferred for efficiency
    adata.obsm["X_umap"] = normal(0, 1, size=(adata.n_obs, 2))
    adata.varm["gene_stuff"] = normal(0, 1, size=(adata.n_vars, 5))
    adata.uns["random"] = [1, 2, 3]
    adata.layers["log_transformed"] = log1p(adata.X)
    return(adata)

def scvi_model(adata, max_epochs = 50):
    """Train a dummy scVI model on an AnnData object. This module follows this online tutorial: https://docs.scvi-tools.org/en/latest/tutorials/notebooks/api_overview.html#Creating-and-training-a-model 

    Parameters
    ----------
    adata: anndata object
        Object containing single cell RNA-seq data.
    max_epochs: Integer
        Number of epochs to perform model trainin with.

    Returns
    -------
    m: scVI model object
        scVI model object which has been trained.
    """

    settings.seed = 1
    model.SCVI.setup_anndata(adata)
    m = model.SCVI(adata, gene_likelihood = 'nb')
    m.train(max_epochs = max_epochs)
    return(m)

# run when file is directly executed
if __name__ == '__main__':
    # create a dummy anndata object
    adata = dummy_adata()
    print("Dummy Data:")
    print(adata)
    print("\nObs:")
    print(adata.obs)
    print("\nVars:")
    print(adata.var)
    print("\nIs adata.X sparse?")
    print(issparse(adata.X))
    model = scvi_model(adata)
    print("\nscVI model:")
    print(model)