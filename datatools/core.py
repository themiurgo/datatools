import numpy as np

def get_pdf(data, **kwargs):
    pdf, bin_edges = np.histogram(data, density=True, **kwargs)
    return pdf, bin_edges


def get_cdf(data, **kwargs):
    pdf, bin_edges = get_pdf(data, **kwargs)
    cdf = np.cumsum(pdf * np.diff(bin_edges))
    return cdf, bin_edges


