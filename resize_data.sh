#!/usr/bin/env bash

dir=$1

mkdir $dir"_small"

for class in `ls $dir`
do
    echo "Resizing $class"
    mkdir $dir"_small/"$class
    ./resize.py -s 96 -d $dir/$class -o $dir"_small/"$class
done
