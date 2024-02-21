import libvirt

def get_state(state):
    if state == libvirt.VIR_DOMAIN_NOSTATE:
        return 'The state is VIR_DOMAIN_NOSTATE'
    elif state == libvirt.VIR_DOMAIN_RUNNING:
        return 'The state is VIR_DOMAIN_RUNNING'
    elif state == libvirt.VIR_DOMAIN_BLOCKED:
        return 'The state is VIR_DOMAIN_BLOCKED'
    elif state == libvirt.VIR_DOMAIN_PAUSED:
        return 'The state is VIR_DOMAIN_PAUSED'
    elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
        return 'The state is VIR_DOMAIN_SHUTDOWN'
    elif state == libvirt.VIR_DOMAIN_SHUTOFF:
        return 'The state is VIR_DOMAIN_SHUTOFF'
    elif state == libvirt.VIR_DOMAIN_CRASHED:
        return 'The state is VIR_DOMAIN_CRASHED'
    elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
        return 'The state is VIR_DOMAIN_PMSUSPENDED'
    elif state == libvirt.VIR_DOMAIN_RUNNING:
        return 'The state is Running'

conn = libvirt.open("qemu:///system")
if conn==None:
    print("Error in connection")

# Domain Names in the host
domains = conn.listAllDomains()
print("Guest Domains in the host")
for domain in domains:
    print("    UUID: ", domain.UUIDString())
    print("    Name: ", domain.name())
    print("    State: ", get_state(domain.state()[0]))
    if domain.state()[0] == libvirt.VIR_DOMAIN_RUNNING:
        print("    Num CPUs: ", domain.maxVcpus())
    else:
        print("    Num CPUs: None [Not running]")
    print("    Max Memory (Bytes): ", domain.maxMemory())
    print()

conn.close()
