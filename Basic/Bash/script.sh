#!/bin/bash

CURRENT_DIR=$(pwd)
if [[ "$CURRENT_DIR" == "/home/deq/Training/Day 1" ]]; then
	echo "Working as Trainee"
else
	echo "Working as Admin"
fi
echo "$CURRENT_DIR"
echo "--------------------------------------------------"
for file in /var/log/*.log; do
	echo "Processing File : $file"
done
echo "---------------------------------------------------"
while read -r line; do
	echo "Line Read $line"
done < test.txt
