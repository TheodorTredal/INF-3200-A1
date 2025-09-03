#!/bin/bash

# if $1 > list, start på nytt
# Sjekk om en port i en host er tatt


filename="activehostport.txt"
# nodes=$( /share/ifi/available-nodes.sh | head -n "$1" )

mapfile -t nodes < <( /share/ifi/available-nodes.sh | head -n "$1" )

echo "Antall noder: ${#nodes[@]}"

check_port_availability() {
    local node="$1"
    local port    
    while :; do
        port=$(shuf -i 49631-65535 -n 1)
        if ! ssh "$USER@$node" "nc -z localhost $port" >/dev/null 2>&1; then
            echo "$port"
            return
        fi
    done
}




total_servers=$1
servers_per_node=$(( (total_servers + ${#nodes[@]} - 1) / ${#nodes[@]} ))

for node in "${nodes[@]}"; do
    for i in $(seq 1 $servers_per_node); do
        port=$(check_port_availability "$node")
        echo "$port"
        ssh "$USER@$node" "nohup python3 INF-3200-A1/ttr042/src/server.py $node $port > /dev/null 2>&1 &" &
        echo "$node:$port" >> activehostport.txt
    done
done




Print the host:port combinations
json_array="["
while IFS= read -r line; do
    json_array+="\"$line\","
done < activehostport.txt

json_array="${json_array%,}"
json_array+="]"

echo "$json_array"