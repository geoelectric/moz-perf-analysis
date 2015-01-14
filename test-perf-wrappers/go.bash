#!/bin/bash

stamp21=2014-11-21-00-12-02
rev21=6c739275

stamp20=2014-10-31-00-02-01
rev20=7b8df994

echo "Testing 2.1 $stamp21..."
./prep.bash Flame_2.0_v188_1 2.1 $stamp21 $rev21
./run.bash results/2.1-$stamp21 16

echo "Testing 2.0 $stamp20..."
./prep.bash 2.0 $stamp20 $rev20
./run.bash results/2.0-$stamp20 16

echo "Go done!"

