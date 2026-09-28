#!/bin/bash

read -p "Enter the String : " line
if [ -z "$line" ]; then
    echo "Empty String"
else 
    wc -w <<<"$line"
fi