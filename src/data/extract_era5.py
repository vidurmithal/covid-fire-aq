from pathlib import Path
PATH = Path(__file__).parents[2]
    
def _get_time_from_config(start, end):
    '''Convert `start`, `end` and `freq` specified in config.yml to CDS API-readable values.'''
    
    from pandas import to_datetime
    from numpy import arange
    
    start = to_datetime(start)
    end   = to_datetime(end)

    if start.year == end.year:
        years = ['%s'%start.year]
    else:
        years = [str(x) for x in arange(start.year,end.year+1).tolist()]
         
    if start.month == end.month:
        months = ['%s'%start.month]
    else:
        months = [str(x) for x in arange(start.month,end.month+1).tolist()]

    days = [str(x) for x in arange(1,32).tolist()]

    times = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', 
             '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', 
             '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', 
             '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']

    return years, months, days, times


def extract_era5(variables, region=[74,28.5,78,32], start='2018-0path=PATH.joinpath('data/raw/')):
    '''Using CDS API to request ERA5 data for variables specified. Variable names can be found at 
    https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview . 
    Time period and area will be inferred from the `config.yml` file. 
    ''' 
    
    from src.utils import config
    from src.data.extract_era5 import _get_time_from_config
    import cdsapi
    from urllib3 import disable_warnings, exceptions

    disable_warnings(exceptions.InsecureRequestWarning)
    
    config = config()
    
    years, months, days, times = _get_time_from_config()
    xmin, ymin, xmax, ymax = list(config['region'].values())
    
    uri, key = config['COPERNICUS']['uri'], config['COPERNICUS']['key']
    
    c = cdsapi.Client(url='https://cds.climate.copernicus.eu/api/v2', key='%s:%s'%(uri, key))
#     print('Connecting to client.')
    
    res = c.retrieve("reanalysis-era5-single-levels",  {'product_type': 'reanalysis',
                                                        'variable': variables,
                                                        'year': years,
                                                        'month': months,
                                                        'day':  days,
                                                        'time': times,
                                                        'format': 'netcdf',
                                                        'area': [xmin, ymin, xmax, ymax],
                                                        'grid': [0.25, 0.25]
                                                       }
                    )
#     print('Retrieving data.')
    
    res.download(path.joinpath(res.location.split('/')[-1]))
#     print('Downloading...')
    
    return 'Completed.'