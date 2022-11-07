"""Modules used for plotting.
"""
# imports
from pandas import DataFrame, concat
from numpy import concatenate
from scipy.sparse import issparse
from plotnine import ggplot, aes, stat_ecdf, ylim, ylab, xlab, labs, ggtitle, theme_minimal, theme, element_text

# modules
def ecdf(adata, gene, contrast, contrast_a, contrast_b, font_size = 14, layer = None):
    """Plot ECDF plot for two groups of cells.
    Parameters
    ----------
    adata: anndata object
        Object containing single cell RNA-seq data.
    gene: string
        Gene name.
    contrast: string
        A column in adata.obs containing group labels.
    contrast_a: string
        Name of the first group.
    contrast_b: string
        Name of the second group.
    font_size: integer
        Font size for the text on the plot.
    layer: string
        Name of the adata layer to be used for calculation. Default is None. If default adata.X will be used for calculation.

    Returns
    -------
    p: ggplot object
        p contains ECDF plot for a given gene. To plot p use print(p).
    """

    gene_list = adata.var.index.tolist()
    
    if gene in gene_list:
        if not layer:
            if issparse(adata.X):
                df1 = DataFrame({
                    "expr" : concatenate(DataFrame.sparse.from_spmatrix(adata[adata.obs[contrast] == contrast_a, gene].X).to_numpy()), 
                    "cond" : contrast_a
                })
                df2 = DataFrame({
                    "expr" : concatenate(DataFrame.sparse.from_spmatrix(adata[adata.obs[contrast] == contrast_b, gene].X).to_numpy()), 
                    "cond" : contrast_b
                })
            else:
                df1 = DataFrame({
                    "expr" : concatenate(adata[adata.obs[contrast] == contrast_a, gene].X), 
                    "cond" : contrast_a
                })
                df2 = DataFrame({
                    "expr" : concatenate(adata[adata.obs[contrast] == contrast_b, gene].X),
                    "cond" : contrast_b
            })
        else:
            if issparse(adata.layers[layer]):
                df1 = DataFrame({
                    "expr" : concatenate(DataFrame.sparse.from_spmatrix(adata[adata.obs[contrast] == contrast_a, gene].layers[layer]).to_numpy()), 
                    "cond" : contrast_a
                })
                df2 = DataFrame({
                    "expr" : concatenate(DataFrame.sparse.from_spmatrix(adata[adata.obs[contrast] == contrast_b, gene].layers[layer]).to_numpy()), 
                    "cond" : contrast_b
                })
            else:
                df1 = DataFrame({
                    "expr" : concatenate(adata[adata.obs[contrast] == contrast_a, gene].layers[layer]), 
                    "cond" : contrast_a
                })
                df2 = DataFrame({
                    "expr" : concatenate(adata[adata.obs[contrast] == contrast_b, gene].layers[layer]), 
                    "cond" : contrast_b
                })

        df = concat([df1, df2])

        p = (
            ggplot(aes(x = 'expr', colour = 'cond'), df)
            + stat_ecdf()
            + ylim((0,1))
            + ylab("ECDF")
            + xlab("Expression")
            + labs(colour = "Groups")
            + ggtitle(gene)
            + theme_minimal()
            + theme(text = element_text(size = font_size))
        )

        return(p)
        
    else:
        print("Input gene is not present in the input dataset!")
        return(None)

# run when file is directly executed
if __name__ == '__main__':
    from .utils import dummy_adata
    # create a dummy anndata object
    adata = dummy_adata()
    p = ecdf(adata, 'Gene_1', 'cell_type', 'B', 'Monocyte', layer = 'log_transformed')
    print(p)
