#!/bin/bash

path="$1"
if [[ -z "$path" ]]; then
	echo "Usage : ./detector.sh <path>"
elif [[ -d "$path" ]]; then
	echo "directory"
elif [[ -f "$path" ]]; then
	echo "regular file"
else
	echo "other"
fi
