#!/bin/bash

pattern="$1"
if [[ -z "$pattern" ]]; then
	echo "Usage: ./filter.sh <pattern>"
	exit 1
fi

while read -r line ;do
	if [[ -z "$line" ]]; then
		break;


	elif [[ "$line" =~ $pattern ]]; then
		echo "Pattern found : $line"
	fi
done
