#!/bin/bash

mapfile -t nodes < <( /share/ifi/available-nodes.sh | head -n "$1" )

echo "Antall noder: ${#nodes[@]}"

# checks if a port on a node is in use
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


# Calculate how many server instances should run on each node
total_servers=$1
servers_per_node=$(( (total_servers + ${#nodes[@]} - 1) / ${#nodes[@]} ))

# iterating over all the available nodes
for node in "${nodes[@]}"; do
    for i in $(seq 1 $servers_per_node); do
        port=$(check_port_availability "$node")

        # Copy the file over to the other nodes
        # Start the server on the host:port
        {
        scp server.py "$USER@$node:~/server.py"> /dev/null 2>&1
        ssh "$USER@$node" "nohup python3 ~/server.py $node $port > /dev/null 2>&1"
        } &
        echo "$node:$port" >> activehostport.txt
    done
done



# Print the host:port combinations
json_array="["
while IFS= read -r line; do
    json_array+="\"$line\","
done < activehostport.txt

json_array="${json_array%,}"
json_array+="]"

echo "$json_array"