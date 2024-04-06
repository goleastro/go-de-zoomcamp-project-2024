if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    print("Trips with 0 count:", data['Count'].isin([0]).sum())
    # Specify your transformation logic here

    return data[data['Count'] > 0]


@test
def test_output(output, *args) -> None:

    assert output['Count'].isin([0]).sum() == 0, 'All trips have 0 count'
