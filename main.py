


# %% Download Data
from pathlib import Path
import owncloud
# url = 'https://uni-bonn.sciebo.de/s/OHGmJVdmMS8TITV'
# url = 'https://uni-bonn.sciebo.de/s/3ladn8YIQclZjHg'
url = 'https://uni-bonn.sciebo.de/s/oTfGigwXQ4g0raW'
client = owncloud.Client.from_public_link(url)
client.get_file('/', 'data.nc')

if Path('data.nc').exists():
    print('Download Succeeded.')

# %% Load Data
import xarray as xr

dset = xr.load_dataset('data.nc')
dset

# %% Extract Experiment-Level Data
trials = dset[['contrast_left', 'contrast_right', 'stim_onset']].to_dataframe()
trials

# %% Extract Spike-Time Data
spikes = dset[['spike_trial', 'spike_cell', 'spike_time']].to_dataframe()
spikes


# %% Extract Cell-Level Data
cells = dset['brain_groups'].to_dataframe()
cells

# %% Merge and Compress Extracted Data
import pandas as pd
merged = pd.merge(left=cells, left_index=True, right=spikes, right_on='spike_cell')
merged = pd.merge(left=trials, right=merged, left_index=True, right_on='spike_trial').reset_index(drop=True)
merged.columns
merged = (merged
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
merged.info()
# .rename(columns={'spike_trial': 'trial'})

# %% Calculate Time Bins for PSTH
import numpy as np
time = merged['time']
time = np.round(time, decimals=6)  # Round time to the nearest microsecond, to reduce floating point errors.
bin_interval = 0.05
time_bins = np.floor(time /bin_interval) * bin_interval  # Round down to the nearest time bin start
time_bins


# %% filter out stimuli with contrast on the right.
filtered = merged[merged['contrast_right'] == 0]
print(f"Filtered out {len(merged) - len(filtered)} ({len(filtered) / len(merged):.2%}) of spikes in dataset.")
filtered

# %% Make PSTHs
psth = (
    filtered
    .groupby([time_bins, 'trial_id', 'contrast_left', 'cell_id', 'brain_area'], observed=True, )
    .size()
    .rename('spike_count')
    .reset_index()
)
psth
psth = (
    psth
    .groupby(['time', 'contrast_left', 'brain_area'], observed=True)
    .spike_count
    .mean()
    .rename('avg_spike_count')
    .reset_index()
)
psth
psth['avg_spike_rate'] = psth['avg_spike_count'] * bin_interval
psth

# %% Plot PSTHs
import seaborn as sns
g = sns.FacetGrid(data=psth, col='brain_area', col_wrap=2)
# sns.lineplot(data=)
g.map_dataframe(sns.lineplot, x='time', y='avg_spike_count', hue='contrast_left')
g.add_legend()
# psth_data = spike_counts.unstack().unstack()
# avg_spike_counts.index
g.savefig('PSTHs.png')



# %%
