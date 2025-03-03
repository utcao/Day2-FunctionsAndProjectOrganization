
# %% Script Parameters
import psth

url = 'https://uni-bonn.sciebo.de/s/oTfGigwXQ4g0raW'
filename = 'data/data.nc'

# %% Download Data
# Exercise (Example): Make a download_data(url, filename) function:

# from scripts.utils import download_data   

psth.download_data(url=url, filename=filename)

# %% Load Data
# Exercise: Make a `load_data(filename)` function, returning the `dset` variable.
# from scripts.psth import load_data
dset = psth.load_data(filename)
print(dset)
# %% Extract Experiment-Level Data
# Exercise: Make an `extract_trials(filename)` function, returning the `trials` variable.
# from scripts.psth import extract_trials
trials = psth.extract_trials(filename)
print(trials)
# %% Extract Spike-Time Data
# Exercise: Make an `extract_spikes(filename)` function, returning the `spikes` variable.
dset = psth.load_data(filename)
spikes = dset[['spike_trial', 'spike_cell', 'spike_time']].to_dataframe()
spikes


# %% Extract Cell-Level Data
# Exercise: Make an `extract_cells(filename)` function, returning the `cells` variable.

import xarray as xr

dset = psth.load_data(filename)
cells = dset['brain_groups'].to_dataframe()
cells

# %% Merge and Compress Extracted Data
# Exercise: Make a `merge_data(trials, cells, spikes)` function, returning the `merged` variable.
# from scripts.psth import self_merge
merged = psth.self_merge(cells, spikes, trials)
merged.info()



# %% Calculate Time Bins for psth
# Exercise: Make a `compute_time_bins(time, bin_interval)` function, returning the `time_bins` variable.

import numpy as np
time = merged['time']
time = np.round(time, decimals=6)  # Round time to the nearest microsecond, to reduce floating point errors.
bin_interval = 0.05
time_bins = np.floor(time /bin_interval) * bin_interval  # Round down to the nearest time bin start
time_bins


# %% filter out stimuli with contrast on the right.
# No function needed here for this exercise.

filtered = merged[merged['contrast_right'] == 0]
print(f"Filtered out {len(merged) - len(filtered)} ({len(filtered) / len(merged):.2%}) of spikes in dataset.")
filtered

# %% Make psths
# Exercise: Make a `compute_psths(data, time_bins)` function here, returning the `psth` variable.

psth_df = (
    filtered
    .groupby([time_bins, 'trial_id', 'contrast_left', 'cell_id', 'brain_area'], observed=True, )
    .size()
    .rename('spike_count')
    .reset_index()
)
psth_df
psth_df = (
    psth_df
    .groupby(['time', 'contrast_left', 'brain_area'], observed=True)
    .spike_count
    .mean()
    .rename('avg_spike_count')
    .reset_index()
)
psth_df
psth_df['avg_spike_rate'] = psth_df['avg_spike_count'] * bin_interval
psth_df


# %% Plot psths
# Make a `plot_psths(psth)` function here, returning the `g` variable.
# from scripts.psth import plot_psths
psth.plot_psths(psth_df, path='results/utilss.png')

