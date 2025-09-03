#!/bin/bash

# convert the activehostport.txt data to json data
json_array="["
while IFS= read -r line || [ -n "$line" ]; do
    line=$(echo "$line" | tr -d '\r\n')
    json_array+="\"$line\","
done < activehostport.txt

# Removes the last comma from the json
json_array="${json_array%,}"
json_array+="]"

# Run the testscript with the json array as its input
python3 testscript.py "$json_array"
