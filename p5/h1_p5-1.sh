#!/bin/bash

# 
T=-1     # Default value for granularty                                  (T)
t=-1     # Default value for number of seconds                           (Tp)
X=1000   #                                                               (X) 
Y=1000   #                                                               (5)
C=0      # Boolean for Clean                                             (Clean)
H=0      # Boolean for help                                              (Help)

# defining csv file names
FILE="/home/vmadm/amay/hw1/p5/h1_p5-1.csv"
ALERT_FILE="/home/vmadm/amay/hw1/p5/h1_p5-1-alert.csv"


# Use getopts to parse options
while getopts ":T:t:X:Y:C:H:" opt; do
  case $opt in
    T) T="$OPTARG" ;;
    t) t="$OPTARG" ;;
    X) X="$OPTARG" ;;
    Y) Y="$OPTARG" ;;
    C) C="$OPTARG" ;;
    H) H="$OPTARG" ;;
    \?) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
  esac
done

# Code for cleaning up the csv files (depends on the argument given)
if (( $(echo "$C == 1" | bc -l) )); then
  echo "cleaning Log files"
  echo "timestamp,1_min_load,5_min_load,15_min_load" > "$FILE"
  echo "timestamp,Alert,1_min_load,5_min_load,15_min_load" > "$ALERT_FILE"
  exit
elif (( $(echo "$C == 0" | bc -l) )); then
  ignore=""
else 
  echo "-C should be between 0 and 1"
  exit
fi

# Check if csv files exist, and create them if they don't
if ! [ -e "$FILE" ]; then
  echo "timestamp,1_min_load,5_min_load,15_min_load" > "$FILE"
fi

if ! [ -e "$ALERT_FILE" ]; then
  echo "timestamp,Alert,1_min_load,5_min_load,15_min_load" > "$ALERT_FILE"
fi

# Loops according to user specified parameters to get average CPU load
for ((i=0; i<t; i+=T)); do
  uptime_res=$(uptime)
  timestamp=$(echo $uptime_res | awk -F' ' '{print $1}')
  one_min_load=$(echo $uptime_res | awk -F', ' '{print $4}' | awk -F': ' '{print $2}' | bc )
  five_min_load=$(echo $uptime_res | awk -F', ' '{print $5}' | bc)
  five_min_load=$(echo $uptime_res | awk -F', ' '{print $5}' | bc)
  fifteen_min_load=$(echo $uptime_res | awk -F', ' '{print $6}' | bc)
  X=$(echo $X | bc)
  Y=$(echo $Y | bc)

  # appends averege cpu load to csv
  echo "$timestamp,$one_min_load,$five_min_load,$fifteen_min_load" >> "$FILE"

  # appends in case X is exceeded
  if (( $(echo "$one_min_load > $X" | bc -l) )); then
    echo "$timestamp,HIGH CPU USAGE,$one_min_load,$five_min_load,$fifteen_min_load" >> "$ALERT_FILE"
  fi

  # appends in case Y is exceeded
  if (( $(echo "$five_min_load > $Y" | bc -l) )); then
    echo "$timestamp,VERY HIGH CPU USAGE,$one_min_load,$five_min_load,$fifteen_min_load" >> "$ALERT_FILE"
  fi

  # defines granularity
  sleep "$T"
done