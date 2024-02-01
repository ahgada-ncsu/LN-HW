#!/bin/bash

# loop thrice
for i in $(seq 1 3)
do
	# print top 11 lines of the output of top. The top output will be sorted by memory usage in descending order
	top_output=$(top -b -n 1 -o="%MEM" | head -n 11)
	
	#output the  top result on screen
	echo -e "$top_output"
	echo ""
	
	#sleep for 2 seconds
	sleep 2
done
