import 


@click.command()
@click.argument('',
                #type=click.Path(exists=True),
                type=click.File('r', encoding='utf8'),
                default=sys.stdin
               )
def dformat(data):
    values = [float(value) for value in data]
    print scipy.stats.describe(values)


