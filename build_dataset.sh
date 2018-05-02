#!/usr/bin/env bash

key=$1
file=$2
out=$3


counter=0
while read name
do
  mkdir "$out/$name"
  ./image_download.py -q "$name" -o "$out/$name" -m 100 -k "$key"
done < $file

