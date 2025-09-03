#!/bin/bash

json_array="["
while IFS= read -r line || [ -n "$line" ]; do
    line=$(echo "$line" | tr -d '\r\n')
    json_array+="\"$line\","
done < activehostport.txt

# Fjern siste komma
json_array="${json_array%,}"
json_array+="]"

# Kjør Python-skriptet
python3 testscript.py "$json_array"
