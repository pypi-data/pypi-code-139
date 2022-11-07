"""Modules used for differential expression analysis.
"""
# imports
from pandas import DataFrame, concat
from pyranges.statistics import fisher_exact
from scipy.sparse import issparse
from scipy.stats import ks_2samp

def scvi(model, contrast, contrast_a, contrast_b, iterations = 50, filter = True, lfc = 1, bayes_factor = 2.5, pval = 0.01, non_zeros_proportion_b = 0.3, layer = 'scvi_normalized'):
    """Calculate differentially expressed genes from two groups of cells using scvi model, calculate Fisher statistics to identify significant change between proportions of expressing cells and select only significant genes using calculated parameters. As scVI model is stochastic, analysis is run multiple times (see iterations parameter) and then averaged over all iterations.

    Parameters
    ----------
    model: scVI model
        scVI model trained on an annData object.
    contrast: string
        A column in adata.obs containing group labels.
    contrast_a: string
        Name of the first group.
    contrast_b: string
        Name of the second group.
    iterations: integer
        Number of iteration for differential expression
    filter: boolean
        Parameter to switch on/off filtering. Default is on.
    lfc: float
        Min log fold change for a gene to be considered as differentially expressed. Default is 1.
    bayes_factor: float
        Min bayes factor for a gene to be considered as differentially expressed. Default is 3.
    pval: float
        Max p-value for a gene to be considered as differentially expressed. Default is 0.01.
    non_zeros_proportion_b: float
        Min proportion of non zero cells for a gene in contrast_b (usually mutant) to be considered as differentially expressed. Default is 0.3

    Returns
    -------
    scvi_de: pandas DataFrame
        A DataFrame containing results of scVI DE analysis averaged over multiple runs (see iterations parameter).
    """

    scvi_de = DataFrame()

    for i in range(iterations):
        # https://discourse.scverse.org/t/de-analysis-between-two-batch-specific-clusters/393
        # 'batch_correction = True' should only be used when group1 and group2 populations have members from multiple batches.
        # batch should be defined via batch_key in scvi.model.SCVI.setup_anndata
        df = model.differential_expression(
            groupby=contrast,
            group1=contrast_b,
            group2=contrast_a,
            batch_correction = True
        )
        scvi_de = concat([scvi_de, df])

    scvi_de.index.name = None
    scvi_de['genes'] = scvi_de.index
    comparison = list(set(scvi_de['comparison']))[0]

    # average DE results over multiple runs
    scvi_de = scvi_de.groupby('genes').mean()
    scvi_de['comparison'] = comparison

    # perform Fisher test to check whether number of non-zeros has significantly changed
    a = (1 - scvi_de['non_zeros_proportion1'])*model.adata[model.adata.obs[contrast] == contrast_b].obs.shape[0]
    b = (1 - scvi_de['non_zeros_proportion2'])*model.adata[model.adata.obs[contrast] == contrast_a].obs.shape[0]
    c = scvi_de['non_zeros_proportion1']*model.adata[model.adata.obs[contrast] == contrast_b].obs.shape[0]
    d = scvi_de['non_zeros_proportion2']*model.adata[model.adata.obs[contrast] == contrast_a].obs.shape[0]

    fish = fisher_exact(a, b, c, d, pseudocount=0)

    fish.index = scvi_de.index
    scvi_de['fisher'] = fish['P']

    # filter based on alethiomics criteria
    if filter:
        scvi_de = scvi_de[
            (scvi_de["lfc_mean"] > lfc) & 
            (scvi_de["bayes_factor"] > bayes_factor) & 
            (scvi_de['fisher'] <= pval) &
            (scvi_de["non_zeros_proportion1"] > scvi_de["non_zeros_proportion2"]) &
            (scvi_de["non_zeros_proportion1"] >= non_zeros_proportion_b)
        ]

    # perform Kolmogorov-Smirnov test
    ks_table = DataFrame(index = scvi_de.index)
    ks_table['ks-stat'] = 0
    ks_table['ks-pval'] = 1

    if layer is not None:
        d1 = model.get_normalized_expression(library_size = 10e4)[model.adata.obs[contrast] == contrast_b][scvi_de.index]
        d2 = model.get_normalized_expression(library_size = 10e4)[model.adata.obs[contrast] == contrast_a][scvi_de.index]
    else:
        d1 = model.get_normalized_expression(library_size = 10e4)[model.adata.obs[contrast] == contrast_b][scvi_de.index]
        d2 = model.get_normalized_expression(library_size = 10e4)[model.adata.obs[contrast] == contrast_a][scvi_de.index]

    for gene in scvi_de.index:
        ks = ks_2samp(d1[gene], d2[gene])
        ks_table.loc[gene, 'ks-stat'] = ks[0]
        ks_table.loc[gene, 'ks-pval'] = ks[1]
    
    scvi_de = concat([scvi_de, ks_table], axis = 1)
    scvi_de.sort_values('lfc_mean', ascending = False, inplace = True)

    return(scvi_de)

# run when file is directly executed
if __name__ == '__main__':
    from .utils import dummy_adata, scvi_model
    # create a dummy anndata object
    adata = dummy_adata()
    model = scvi_model(adata)
    df = scvi(
        model, 
        contrast = "cell_type", 
        contrast_a = "B", 
        contrast_b = "Monocyte", 
        iterations = 5,
        lfc = 0.1,
        bayes_factor = 1,
        pval = 0.5,
        non_zeros_proportion_b = 0.1
    )
    print(df)
