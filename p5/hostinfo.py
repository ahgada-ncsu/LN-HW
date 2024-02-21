import libvirt

conn = libvirt.open('qemu:///system')
if conn is None:
    print("Failed to open connection")

print()

# Get host object
print()
host = conn.getHostname()
print("hostname: ", host)

print()
# Get the number of active domains
num_domains = conn.numOfDomains()
print("Number of domains in the host:", num_domains)

# host details
host_details = conn.getInfo()
print()
print("CPU Model: ", host_details[0])
print("Memory size in Megabytes: ", host_details[1])
print("Number of active CPUs: ", host_details[2])
print("Expected CPU frequency: ", host_details[3])

# Hypervisor type 
print()
print("Hypervisor type:", conn.getType())

# free memory of the host
print()
print("Free Memory in Host: ", conn.getFreeMemory())
conn.close()