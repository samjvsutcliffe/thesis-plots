#!/bin/bash
set -e
for n in 0 0.25 0.5 0.75 1
do
    export NOTCH=$n
    sbcl --dynamic-space-size 16GB --disable-debugger --load "example.lisp" --quit > ./logs/log_$n.txt &
done
