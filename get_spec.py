# -*-coding:utf-8-*-
__author__ = 'Sunny'

import psutil
import platform
from datetime import datetime
import json

# https://www.thepythoncode.com/article/get-hardware-system-information-python
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


print("=" * 40, "System Information", "=" * 40)
uname = platform.uname()
# print(f"System: {uname.system}")
# print(f"Node Name: {uname.node}")
# print(f"Release: {uname.release}")
# print(f"Version: {uname.version}")
# print(f"Machine: {uname.machine}")
# print(f"Processor: {uname.processor}")

System = {"System": f"{uname.system}",
          "Node Name": f"{uname.node}",
          # "Release": f"{uname.release}",
          "Release": f"56",
          # "Version": f"{uname.version}",
          "Version": f"10.0.5656",
          # "Machine": f"{uname.machine}",
          "Machine": f"AMD56",
          "Processor": f"{uname.processor}"}
json_System = json.dumps(System, indent=4)
print(json_System)  ##

# Boot Time
print("=" * 40, "Boot Time", "=" * 40)
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
# print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
Boot = {"Boot Time": f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"}
json_Boot = json.dumps(Boot, indent=4)
print(json_Boot)  ##

print("=" * 40, "CPU Info", "=" * 40)
# number of cores
# print("Physical cores:", psutil.cpu_count(logical=False))
# print("Total cores:", psutil.cpu_count(logical=True))
# CPU frequencies
cpufreq = psutil.cpu_freq()
# print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
# print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
# print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
# CPU usage
# print("CPU Usage Per Core:")

cpu_use_keys = []
cpu_use_values = []
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    # print(f"Core {i}: {percentage}%")
    cpu_use_keys.append(f"Core {i}")
    cpu_use_values.append(f"{percentage}%")

# print(f"Total CPU Usage: {psutil.cpu_percent()}%")

per_cpu_use = dict(zip(cpu_use_keys, cpu_use_values))
# print(per_cpu_use)
# per_cpu_use = json.dumps(per_cpu_use, indent=4)
# print(per_cpu_use)

cpu = {"Physical cores": f"{psutil.cpu_count(logical=False)}",
       "Total cores": f"{psutil.cpu_count(logical=True)}",
       "Max Frequency": f"{cpufreq.max:.2f}Mhz",
       "Min Frequency": f"{cpufreq.min:.2f}Mhz",
       "Current Frequency": f"{cpufreq.current:.2f}Mhz",
       "CPU Usage Per Core": per_cpu_use,
       "Total CPU Usage": f"{psutil.cpu_percent()}%"}
json_cpu = json.dumps(cpu, indent=4)
print(json_cpu)  ##


# Memory Information
print("=" * 40, "Memory Information", "=" * 40)
# get the memory details
svmem = psutil.virtual_memory()
# print(f"Total: {get_size(svmem.total)}")
# print(f"Available: {get_size(svmem.available)}")
# print(f"Used: {get_size(svmem.used)}")
# print(f"Percentage: {svmem.percent}%")

Memory = {"Total": f"{get_size(svmem.total)}",
          "Available": f"{get_size(svmem.available)}",
          "Used": f"{get_size(svmem.used)}",
          "Percentage": f"{svmem.percent}%"}
json_Memory = json.dumps(Memory, indent=4)
print(json_Memory)  ##

print("=" * 20, "SWAP", "=" * 20)
# get the swap memory details (if exists)
swap = psutil.swap_memory()
# print(f"Total: {get_size(swap.total)}")
# print(f"Free: {get_size(swap.free)}")
# print(f"Used: {get_size(swap.used)}")
# print(f"Percentage: {swap.percent}%")

swap_d = {"Total": f"{get_size(swap.total)}",
          "Free": f"{get_size(swap.free)}",
          "Used": f"{get_size(swap.used)}",
          "Percentage": f"{swap.percent}%"}

# print(swap_d)
json_swap_d = json.dumps(swap_d, indent=4)
print(json_swap_d)  ##

# Disk Information
print("=" * 40, "Disk Information", "=" * 40)
# print("Partitions and Usage:")
# get all disk partitions
partitions = psutil.disk_partitions()
device_l = []
device_keys = ['Mountpoint', 'File system type', 'Total Size', 'Used', 'Free', 'Percentage']
device_value_all = []

for partition in partitions:
    device_value = []
    # print(f"=== Device: {partition.device} ===")
    device_l.append(f"Device: {partition.device}")
    # print(f"  Mountpoint: {partition.mountpoint}")
    # print(f"  File system type: {partition.fstype}")
    device_value.append(f"{partition.mountpoint}")
    device_value.append(f"{partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    # print(f"  Total Size: {get_size(partition_usage.total)}")
    # print(f"  Used: {get_size(partition_usage.used)}")
    # print(f"  Free: {get_size(partition_usage.free)}")
    # print(f"  Percentage: {partition_usage.percent}%")
    device_value.append(f"{get_size(partition_usage.total)}")
    device_value.append(f"{get_size(partition_usage.used)}")
    device_value.append(f"{get_size(partition_usage.free)}")
    device_value.append(f"{partition_usage.percent}%")

    device_value_all.append(dict(zip(device_keys, device_value)))



# get IO statistics since boot
disk_io = psutil.disk_io_counters()
# print(f"Total read: {get_size(disk_io.read_bytes)}")
# print(f"Total write: {get_size(disk_io.write_bytes)}")
disk_total = {"Total read": f"{get_size(disk_io.read_bytes)}",
              "Total write": f"{get_size(disk_io.write_bytes)}"}

disk_info = dict(zip(device_l, device_value_all))
disk_info.update(disk_total)
disk_info = {'Partitions and Usage': disk_info}
json_disk_info = json.dumps(disk_info, indent=4)
print(json_disk_info)  ##





# Network information
print("=" * 40, "Network Information", "=" * 40)
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()

Interface_l = []
AF_INET_keys = ['IP Address', 'Netmask', 'Broadcast IP']
AF_PACKET_keys = ['MAC Address', 'Netmask', 'Broadcast MAC']
address_value_all = {}

for interface_name, interface_addresses in if_addrs.items():
    address_info = []
    for address in interface_addresses:
        # print(f"=== Interface: {interface_name} ===")
        # Interface.update({'Interface': f'{interface_name}'})
        Interface_l.append(f"{interface_name}")
        if str(address.family) == 'AddressFamily.AF_INET':
            # print(f"  IP Address: {address.address}")
            # print(f"  Netmask: {address.netmask}")
            # print(f"  Broadcast IP: {address.broadcast}")
            # address_info.append(f'{address.address}')
            # address_info.append(f'{address.netmask}')
            # address_info.append(f'{address.broadcast}')
            address_info.append(f'56.565.56.56')
            address_info.append(f'55.66.566.556')
            address_info.append(f'{address.broadcast}')
            address_info = dict(zip(AF_INET_keys, address_info))
            address_value_all.update({f"{interface_name}": address_info})
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            # print(f"  MAC Address: {address.address}")
            # print(f"  Netmask: {address.netmask}")
            # print(f"  Broadcast MAC: {address.broadcast}")
            # address_info.append(f'{address.address}')
            # address_info.append(f'{address.netmask}')
            # address_info.append(f'{address.broadcast}')
            address_info.append(f'{address.address}')
            address_info.append(f'{address.netmask}')
            address_info.append(f'{address.broadcast}')
            address_info = dict(zip(AF_PACKET_keys, address_info))
            address_value_all.update({f"{interface_name}": address_info})

        else:
            address_value_all.update({})

# get IO statistics since boot
net_io = psutil.net_io_counters()
# print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
# print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")
Interface_total = {"Total read": f"{get_size(net_io.bytes_sent)}",
                   "Total write": f"{get_size(net_io.bytes_recv)}"}
# Interface_info = dict(zip(Interface_l, address_value_all))
# print(Interface_info)
address_value_all.update(Interface_total)
json_Interface_info = json.dumps(address_value_all, indent=4, ensure_ascii=False)
print(json_Interface_info)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(json_System, f, ensure_ascii=False, indent=4)
    json.dump(json_Boot, f, ensure_ascii=False, indent=4)
    json.dump(json_cpu, f, ensure_ascii=False, indent=4)
    json.dump(json_Memory, f, ensure_ascii=False, indent=4)
    json.dump(json_swap_d, f, ensure_ascii=False, indent=4)
    json.dump(json_disk_info, f, ensure_ascii=False, indent=4)
    json.dump(json_Interface_info, f, ensure_ascii=False, indent=4)



