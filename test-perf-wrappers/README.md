# make test-perf wrapper scripts

## Overview

These are wrapper scripts for make test-perf, used to create a
repeated number of result sets for comparison.

They were written for Ubuntu, and may have Linux-specific commands
in them. They are meant more for examples of how to create results than
to be directly useful.

## Pre-requisites

As written, they expect to be driving a Flame, and a specific directory 
structure is expected.

### Structure

    TOP_DIR (scripts go here)
    |
    |- BASE (a base build for flashing device)
    |
    |- BRANCH-b2g-distro-BUILD (a nightly b2g build)
    |
    |- BRANCH-b2g-distro-BUILD (a nightly b2g build)
    |
    |- gaia (a checkout of mozilla-b2g/gaia)
    |
    |- results (empty, will receive results)

### BASE 

BASE is a base build for Flame. This directory should have the img files
and flash.sh script at top level. Note that existing flash.sh scripts end 
in `adb logcat` and never exit. They must be modified to exit at the end.

This is used by prep.bash.

### BRANCH-b2g-distro-BUILD

An example of BRANCH-b2g-distro-BUILD would be:

2.0-b2g-distro-2014-10-31-00-02-01

...where 2.0 is the branch and 2014-10-31-00-02-01 designates the build.
In this case a timestamp is used, but it is arbitrary.

This directory should contain the unzipped contents of a nightly build,
including the flash.sh script and sources.xml at top level.

This is used by prep.bash.

### gaia

The gaia directory should be an up to date pull of mozilla-b2g/gaia.

This is used by prep.bash and run.bash.

### results

results is only expected by go.bash. It's given to run.bash as part of the results 
prefix, but if you execute run.bash directly any prefix can be supplied.

## Scripts

### go.bash

Hardcoded driver script for prep.bash and run.bash. Mostly useful to 
see how the other scripts are run. 

Note that the `rev1` and `rev2` variables must be modified to point at
the gaia revisions corresponding to the two builds being ran. These 
are available out of the sources.xml files in the nightly builds.

### prep.bash:

This goes through all the steps to flash a phone, update to the build
being tested, reset gaia for testing, etc.

Run like `./prep.bash BASE BRANCH BUILD REVISION`.

Ex: `./prep.bash v188-1 2.0 2014-10-31-00-02-01 7b8df994`

BASE, BRANCH, BUILD are as documented in the directory structure above.
REVISION is as documented under go.bash.

### run.bash

This runs make test-perf on the build under test repeatedly, to generate
a number of result sets.

It uses only the gaia directory, and assumes any device attached has already
been flashed and prepped with test data.

Run like `./run.bash RESULT_PREFIX ITERATIONS`

Ex: `./run.bash results/2.0-2014-10-31-00-02-01 16`

This will run make test-perf 16 times, placing all the result sets in the
results directory. They will be called 2.0-2014-10-31-00-02-01-##.json,
where ## is from 1 to 16.

