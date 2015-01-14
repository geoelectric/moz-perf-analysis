#!/bin/bash

my_dir=`pwd`
prefix=${1:-perf}
iterations=${2:-16}
settle=30s

export MARIONETTE_RUNNER_HOST=marionette-device-host
export RUNS=31

cd gaia

for i in `seq $iterations`; do
    echo "Starting iteration $i of $iterations"
    export MOZPERFOUT="$my_dir/$prefix-results-$i.json"
    echo "Rebooting..."
    adb reboot
    echo "Waiting for device..."
    adb wait-for-device
    echo "Settling for $settle..."
    sleep 30s
    echo "Running tests..."
    make test-perf
    echo "Iteration $i finished."
done

echo "All Done!"

