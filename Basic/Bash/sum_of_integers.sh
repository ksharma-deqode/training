#!/bin/bash

total=0
while read -r line; do
    ((total+=line))
done < file.txt
echo "$total"

