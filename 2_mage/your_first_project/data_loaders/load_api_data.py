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
    
    # change the date to a keyword argument then have triggers for 2018, 2019, Central, Inner
    year = kwargs['year']
    programme = kwargs['programme']
    #year = "2019"
    #programme = 'Outer'

    urls = [f'https://cycling.data.tfl.gov.uk/ActiveTravelCountsProgramme/{year}%20Q1%20(Jan-Mar)-{programme}.csv',
    f'https://cycling.data.tfl.gov.uk/ActiveTravelCountsProgramme/{year}%20Q2%20spring%20(Apr-Jun)-{programme}.csv',
    f'https://cycling.data.tfl.gov.uk/ActiveTravelCountsProgramme/{year}%20Q3%20(Jul-Sep)-{programme}.csv',
    f'https://cycling.data.tfl.gov.uk/ActiveTravelCountsProgramme/{year}%20Q4%20autumn%20(Oct-Dec)-{programme}.csv'
    ]

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    #url = 'https://cycling.data.tfl.gov.uk/ActiveTravelCountsProgramme/2019%20Q1%20(Jan-Mar)-Central.csv'
    #url = f'https://cycling.data.tfl.gov.uk/ActiveTravelCountsProgramme/{year}%20{quarter}%20(Jan-Mar)-Central.csv'

    dfs = []

    for url in urls:
        response = requests.get(url)
        if response.ok:
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

            df = pd.read_csv(StringIO(s),sep=",",dtype=cycle_dtypes,parse_dates=parse_dates)

            df['Programme'] = programme

            dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)
    
    return combined_df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
