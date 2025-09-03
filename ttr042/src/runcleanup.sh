#!/bin/bash

# Iterere over activehostport.txt
# Finne ut hvordan man kan avslutte en prosess remote med bruk av ssh


while IFS= read -r line; do
    echo "$line"
done < activehostport.txt