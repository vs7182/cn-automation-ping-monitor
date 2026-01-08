import subprocess
import platform
import os
import time, datetime


def load_hosts(file_name):
    hosts = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                host = line.strip()
                if host:
                    hosts.append(host)
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return hosts


def ping_host(host):
    start = time.time()
    
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result.returncode
    end = time.time()
    
    if result:
        calculated_time = (end - start) * 1000 # for converting into milliseconds
        return True, calculated_time
        
    else:
        return False, None
    
    
def log_result(host,status,response_time):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("logs/results.log", 'a') as file:
        if response_time is not None:
            file.write(f"{timestamp} - {host} is {status} - Response Time: {response_time:.2f} ms\n")
        else:
            file.write(f"{timestamp} - {host} is {status} - Response Time: N/A\n")
    






if __name__ == "__main__":
    hosts = load_hosts("data/host.txt")

    for host in hosts:
        status = ping_host(host)
        if status[0]:
            print(f"{host} is UP - Response Time: {status[1]:.2f} ms")
            log_result(host, "UP", status[1])
        else:
            print(f"{host} is DOWN - Response Time: N/A")
            log_result(host, "DOWN", None)