def download_data(url, filename):
    from pathlib import Path
    import owncloud

    client = owncloud.Client.from_public_link(url)
    client.get_file('/', filename)

    if Path(filename).exists():
        print('Download Succeeded.')

    return None

def load_data(filename):
        import xarray as xr
        dset = xr.load_dataset(filename)
        return dset

def extract_trials(filename):
    dset = load_data(filename)
    trials = dset[['contrast_left', 'contrast_right', 'stim_onset']].to_dataframe()
    return trials

def self_merge(cells, spikes, trials):
    import pandas as pd
    merged = pd.merge(left=cells, right=spikes, left_index=True, right_on='spike_cell')
    merged = pd.merge(left=trials, right=merged, left_index=True, right_on='spike_trial').reset_index(drop=True)
    merged.columns
    return (merged
        .rename(columns=dict(
            brain_groups="brain_area",
            spike_trial="trial_id",
            spike_cell="cell_id",
            spike_time="time"
        ))
        [[
            'trial_id',
            'contrast_left',
            'contrast_right',
            'stim_onset',
            'cell_id',
            'brain_area',
            'time'
        ]]
        .astype(dict(   
            brain_area = 'category',
        ))
        # 
    )

def plot_psths(psth):
    import seaborn as sns
    g = sns.FacetGrid(data=psth, col='brain_area', col_wrap=2)
    g.map_dataframe(sns.lineplot, x='time', y='avg_spike_count', hue='contrast_left')
    g.add_legend()
    g.savefig('PSTHs.png')