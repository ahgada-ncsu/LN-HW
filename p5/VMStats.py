import libvirt
import time
from datetime import datetime

#percentage memory usage
def get_memory_usage(memstat):
    return (memstat["actual"] - memstat["available"])/memstat["actual"]

#percentage system and user cpu usage
def get_cpu_usage(cpustat):
    total_cpu_time = 0
    for c in cpustat:
        total_cpu_time += c["cpu_time"]
    return total_cpu_time

def add_to_file(file_name, data):
    with open(file_name, 'a') as file:
        file.write(data)
        file.write("\n")

def get_cpu_change(cpu_list):
    return abs(cpu_list[-2] - cpu_list[-1])/cpu_list[-2]

srt = input("Input 'CPU' to get a sorted list by CPU or 'MEM' to get a sorted list by Memory: ")
ct = input("Enter cpu percentage threshold for alert: ")
mt = input("Enter mem percentage threshold for alert: ")

monitor_interval = 1 # in seconds
conn = libvirt.open("qemu:///system")
if conn==None:
    print("Error in connection")

# stores the tupple (domain_name, %cpu usage (user), %cpu usage(kernel), %memory usage)
stat_dict = {}

while(True):
    res = []
    domains = conn.listAllDomains()
    for domain in domains:
        domain_name = domain.name()
        if domain.state()[0] == libvirt.VIR_DOMAIN_RUNNING:
            if domain_name not in stat_dict:
                stat_dict[domain_name] = {"cpu": [], "mem": 0}
            cpustat = domain.getCPUStats(libvirt.VIR_NODE_CPU_STATS_ALL_CPUS)
            cpustat = get_cpu_usage(cpustat)
            stat_dict[domain_name]["cpu"].append(cpustat)
            if len(stat_dict[domain_name]["cpu"])>1: 
                cpustat = get_cpu_change(stat_dict[domain_name]["cpu"])                
            memstat = domain.memoryStats()
            memstat = get_memory_usage(memstat)
            stat_dict[domain_name]["mem"] = memstat
            if len(stat_dict[domain_name]["cpu"])>1:
                data = (datetime.now(), domain_name, cpustat*100, memstat*100)
                res.append(data)
                if cpustat*100 > float(ct):
                    add_to_file("cpu_alert.txt", str(data[0])+"  ALERT CPU LIMIT EXCEEDED FOR: " + str(data[1]) + " -> "+ str(cpustat*100) + "%")
                if memstat*100 > float(mt):
                    add_to_file("mem_alert.txt", str(data[0])+"  ALERT MEM LIMIT EXCEEDED FOR: " + str(data[1]) + " -> "+ str(memstat*100) + "%")
                    
    if len(res) > 0:
        if srt == "CPU":
            res.sort(key = lambda x: x[2])
        elif srt == "MEM":
            res.sort(key = lambda x: x[3])
        else:
            print("Wrong Input")
            exit()
        for i in res:
            print("TIMESTAMP: ", i[0], "      NAME: ", i[1], "    CPU USAGE:", i[2], "%", "     MEMORY USAGE:", i[3], "%")
    time.sleep(1)
    print()