import click
import toolz
import toolz.curried
import fileinput
import sys
import json

# Fix for pipe handling https://stevereads.com/2015/09/25/python-sigpipe/
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)


@click.command()
@click.argument('input_file',
                type=click.File('r', encoding='utf8'),
                default=sys.stdin
               )
def json2geojson(input_file):
    """Convert a json file into geojson format"""
    data = json.load(input_file)

    geojson = {
        "type": "FeatureCollection",
        "features": [
        {
            "type": "Feature",
            "geometry" : {
                "type": "Point",
                "coordinates": [d["lon"], d["lat"]],
                },
            "properties" : d,
         } for d in data]
    }


    output = open(out_file, 'w')
    json.dump(geojson, output)

    print geojson
