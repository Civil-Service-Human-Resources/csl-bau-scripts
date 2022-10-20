# CSL BAU scripts

This project contains various scripts/programs that are used in CSL to aid in BAU/automation tasks.

## Scripts

Scripts can be found in the `scripts` directory. A `README.md` is provided alongside each script with more details on how to run/what it does. General configurations (`config.py`) are found in the parent category directories (i.e mongo), whilst specific configurations should be stored next to the script itself.

## Running scripts

Due to the way that Python handles imports, the base directory must be explicitly set using the PYTHONPATH environment variable. This tells Python that wherever this project is in the overall directory structure should be used as the import root. This then allows absolute imports to be used.

The `run.sh` file facilitates this requirement. To run a script, simply run `run.sh` followed by the `script.py` that you want to run, followed by any args for that specific script.

