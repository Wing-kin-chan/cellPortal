import h5py

def check_metadata(handle: str):
    experiment = h5py.File(handle, 'r')
    assert all([attribute in experiment for attribute in ['X', 'obs', 'var', 'uns', 'obsm']]), 'Missing data.'

    response = {
        'Observations': list(experiment['obs'].keys()),
        'Variables': list(experiment['var'].keys()),
        'Embeddings': list(experiment['obsm'].keys()),
        'Metadata': list(experiment['uns'].keys())
    }    
    
    return response

