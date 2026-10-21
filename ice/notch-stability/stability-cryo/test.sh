#!/bin/bash
#sbcl --dynamic-space-size 16GB --load "build.lisp" --disable-debugger
for h in 0 0.25 0.5 0.75 1.0
do
    export NOTCH=$h
    ./worker-notch --dynamic-space-size 4GB > ./logs/log_$h.txt &
done
