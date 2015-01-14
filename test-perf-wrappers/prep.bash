#!/bin/bash

if [ -z $1 ]; then
    echo "prep.sh base branch build revision"
    exit
fi

my_dir=`pwd`
base=$1
branch=$2
build=$3
revision=$4
settle=30s

echo "Flashing with $base..."
cd "$base"
bash ./flash.sh
cd ..

echo "Waiting for device..."
adb wait-for-device

echo "Flashing with $branch-b2g-distro-$build..."
cd "$branch"-b2g-distro-"$build"
bash ./flash.sh -f
cd ..

echo "Checking out revision $revision..."
cd gaia
git checkout master
git pull
git checkout "$revision"

echo "Setting memory to 319M..."
adb reboot bootloader
fastboot oem mem 319
fastboot reboot

echo "Waiting for device and settling..."
adb wait-for-device
sleep $settle

echo "Resetting Gaia..."
GAIA_OPTIMIZE=1 NOFTU=1 make reset-gaia

echo "Waiting for device and settling..."
adb wait-for-device
sleep $settle

echo "Injecting workload..."
make reference-workload-light

echo "Waiting for device and settling..."
adb wait-for-device
sleep $settle

echo "Done with prep!"

