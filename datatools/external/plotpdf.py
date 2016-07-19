#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""Plot PDF.

Prints the probability density function of input values. It accepts one value
per line.

Usage:
  plotpdf [DATAFILE ...] [options]

Options:
  -t STR --title=STR       title
  -x STR --xlabel=STR      x axis label [default: Values]
  -y STR --ylabel=STR      y axis label [default: PDF]
  -b INT --nbins=INT       number of bins
  --logbin                 logarithmic binning
  --linestyle=STR          linestyle (matplotlib) [default: -]
  --plotstyle=STR          plotstyle
  -o FILE --output=FILE    save to file (do not show)
  --xlog                   x logarithmic scale
  --ylog                   y logarithmic scale
  -r --rasterized          rasterize data points (to speed up rendering of many data points).
  --dpi=INT                resolution (only has sense when using rasterize) [default: 300]

"""

import fileinput
import sys

from docopt import docopt
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import settings
from utils import common_settings

if __name__ == "__main__":
    args = docopt(__doc__, version='Plot 0.1')
    sys.argv = [sys.argv[0]] + args['DATAFILE']
    #if args['--plotstyle']:
    #    settings.apply_settings(mpl, args['--plotstyle'])
    finput = fileinput.FileInput(openhook=fileinput.hook_compressed)
    data = [np.abs(float(i)+1) for i in finput]

    common_settings(args, plt)
    plt.plot(bin_edges[1:], n, args['--linestyle'], rasterized=args['--rasterized'])
    if args['--output']:
        plt.savefig(args['--output'], dpi=int(args['--dpi']))
    else:
        plt.show()
