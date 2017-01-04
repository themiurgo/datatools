import numpy as np
import json

def get_pdf(data, **kwargs):
    pdf, bin_edges = np.histogram(data, density=True, **kwargs)
    return pdf, bin_edges


def get_cdf(data, **kwargs):
    pdf, bin_edges = get_pdf(data, **kwargs)
    cdf = np.cumsum(pdf * np.diff(bin_edges))
    return cdf, bin_edges

def save_ndjson(iterable, fname, json_fun=json.dumps, **dump_opts):
    with open(fname, "w+") as fw:
        for element in iterable:
            line = json_fun(element, **dump_opts)
            fw.write("{0}\n".format(line))


