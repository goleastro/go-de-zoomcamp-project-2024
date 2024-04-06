import io
from io import StringIO
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    url = 'https://cycling.data.tfl.gov.uk/ActiveTravelCountsProgramme/2019%20Q1%20(Jan-Mar)-Central.csv'
    response = requests.get(url)
    s=requests.get(url, headers= headers).text
    
    cycle_dtypes = {
                'Year': str,
                'UnqID': str,
                'Weather': str,
                'Day': str,
                'Round': str,
                'Dir': str,
                'Path': str,
                'Mode': str,
                'Count': pd.Int64Dtype()
            }
    
    parse_dates=[['Date', 'Time']]


    return pd.read_csv(StringIO(s),sep=",",dtype=cycle_dtypes,parse_dates=parse_dates)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
