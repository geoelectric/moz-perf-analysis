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

crunch_perf_results.py creates summary datasets by combining runs. Run 'python
crunch_perf_results.py --help' for details.

Run 'python compare_results.py' to save graphs to png.

Both can also be imported in iPython and used interactively.
compare_results.compare() is particularly useful with matplotlib inline.

## Notes

These are currently not polished for general use, particularly compare_results,
and require things like editing the scripts to change the logs parsed.

They are being generalized and will be updated.

