"""Modules used for statistical analysis.
"""
# imports
from pandas import DataFrame
from scipy.sparse import issparse
from pyranges.statistics import fisher_exact
from scipy.stats import ks_2samp
from numpy import array

def fisher(adata, contrast, contrast_a, contrast_b):
    """Calculate Fisher's Statistics on two groups of cells, testing whether the number of expressed cells (not zero expression) has significantly changed between two groups.

    Parameters
    ----------
    adata: anndata object
        Object containing single cell RNA-seq data.
    contrast: string
        A column in adata.obs containing group labels.
    contrast_a: string
        Name of the first group.
    contrast_b: string
        Name of the second group.

    Returns
    -------
    adata: anndata object
        Original anndata object with six new added columns in adata.var. Columns correspond to 1) fraction of non-zero cells in contrast_a, 2) fraction of non-zero cells in contrast_b, and 3) Fisher p-value. If Fisher p-value was calculated before it will be overwritten with new values.
    """
    
    x = adata[adata.obs[contrast] == contrast_a].X
    y = adata[adata.obs[contrast] == contrast_b].X
    
    if not issparse(adata.X):
        x = DataFrame(x == 0)
        y = DataFrame(y == 0)
        a = x.sum(axis = 0)
        b = y.sum(axis = 0)
    else:
        x = DataFrame.sparse.from_spmatrix(x != 0)
        y = DataFrame.sparse.from_spmatrix(y != 0)
        a = (x == 0).sum(axis = 0)
        b = (y == 0).sum(axis = 0)
    
    c = x.shape[0] - a
    d = y.shape[0] - b

    fish = fisher_exact(a, b, c, d, pseudocount=0)

    fish.index = adata.var.index
    
    adata.var['non_zeros_proportion_a'] = (c / x.shape[0]).tolist()
    adata.var['non_zeros_proportion_b'] = (d / y.shape[0]).tolist()

    adata.var['fisher'] = fish['P']

    return(adata)

def ks(adata, contrast, contrast_a, contrast_b, gene, layer = None):
    """Calculate Kolmogorov-Smirnov's Statistics on two groups of cells, testing whether their expression distributions for a given gene are significantly different.

    Parameters
    ----------
    adata: anndata object
        Object containing single cell RNA-seq data.
    contrast: string
        A column in adata.obs containing group labels.
    contrast_a: string
        Name of the first group.
    contrast_b: string
        Name of the second group.
    gene: string
        Gene name to perform statistical analysis on.
    layer: string
        Name of the adata layer to be used for calculation. Default is None. If default adata.X will be used for calculation.

    Returns
    -------
    ks: KstestResult object
        The object contains KS statistic and pvalue for a given gene.
    """

    d1 = adata[adata.obs[contrast] == contrast_a, gene]
    d2 = adata[adata.obs[contrast] == contrast_b, gene]

    if layer is not None:
        d1 = d1.layers[layer]
        d2 = d2.layers[layer]
    else:
        d1 = d1.X
        d2 = d2.X

    if issparse(d1):
        d1 = d1.toarray()
        d2 = d2.toarray()

    d1 = array(d1).flatten()
    d2 = array(d2).flatten()

    ks = ks_2samp(d1, d2)

    return(ks)

# run when file is directly executed
if __name__ == '__main__':
    from .utils import dummy_adata
    # create a dummy anndata object
    adata = dummy_adata()
    adata = fisher(adata, 'cell_type', 'B', 'Monocyte')
    print(adata.var)
    ks = ks(adata, 'cell_type', 'Monocyte', 'B', gene = adata.var.index[0], layer = 'log_transformed')
    print(ks)