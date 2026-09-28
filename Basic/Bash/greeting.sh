#!/bin/bash

read -p "Enter you Name : " name
if [ -z "$name" ]; then
    echo "Hello World !"
else 
    echo "Hello $name !"
fi