import dowel
from dowel import logger, tabular

logger.add_output(dowel.StdOutput())
logger.add_output(dowel.CsvOutput('out.csv'))

logger.log('Starting up...')
for i in range(4):
    logger.push_prefix('itr {} '.format(i))
    logger.log('Running training step')

    tabular.record('itr', i)
    tabular.record('loss', 100.0 / (2 + i))

    # the addition of new data to tabular breaks logging to CSV
    if i > 0:
        tabular.record('new_data', i)
    if i > 1:
        tabular.record('brand_new_data', i+i)
        tabular.record('brand_brand_new_data', i+1)


    logger.log(tabular)

    logger.pop_prefix()
    logger.dump_all()

logger.remove_all() 