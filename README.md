# Tools for analyzing Mozilla make test-perf results

## Prerequisites

pip install -r requirements.txt

If you want to use iPython to visualize, also:

pip install -r requirements-ipython.txt

This sets up iPython for use with qtconsole for inline matplotlib. You'll need
to make sure Qt is also installed via your local package manager.

Note that PySide requires pyside_postinstall.py to be executed after pip install
if you're on OS X. It'll be on your path, or in your virtualenv's bin folder.

## Usage

crunch_perf_results.py creates summary datasets by combining runs. Run `python
crunch_perf_results.py --help` for details.

Run `python make_comparison_charts.py name1 name2` to compare result sets and save
charts to png. This will process two sets of json results, name1\*.json and 
name2\*.json. You may have multiple files for each, and they will be combined prior
to charting.

Both can also be imported in iPython and used interactively.
make_comparison_charts.compare() is particularly useful with matplotlib inline.

## Notes

These are currently not polished for general use.

To see how to generate results to use with this, look in the test-perf-wrappers 
directory for example driver scripts for make test-perf.

