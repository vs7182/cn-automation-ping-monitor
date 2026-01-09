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

    result = subprocess.run(command,timeout=2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result.returncode == 0
    end = time.time()
    
    if result.returncode == 0:
        calculated_time = (end - start) * 1000 # for converting into milliseconds
        return True, calculated_time
        
    else:
        return False, None
    
    
def log_result(host,status,response_time):

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("logs/results.log", 'a') as file:
        if response_time is not None:            
            if(response_time > 50):
                file.write(f"{timestamp} - {host} is {status} - Fast - Response Time: {response_time:.2f} ms \n")
            elif((response_time > 50) and (response_time <= 150)):

                file.write(f"{timestamp} - {host} is {status} - Moderate - Response Time: {response_time:.2f} ms \n")
            elif(response_time > 150):
                file.write(f"{timestamp} - {host} is {status} - Slow - Response Time: {response_time:.2f} ms \n")
                
        else:
            file.write(f"{timestamp} - {host} is {status} - Response Time: N/A\n")
           
        


            
        file.close()
        
        
    






if __name__ == "__main__":
    hosts = load_hosts("data/host.txt")
    total = len(hosts)
    up_count = 0
    down_count = 0

    for host in hosts:
        status = ping_host(host)
        if status[0]:
            print(f"{host} is UP - Response Time: {status[1]:.2f} ms")
            log_result(host, "UP", status[1])
            up_count += 1
            
     
        else:
            print(f"{host} is DOWN - Response Time: N/A")
            log_result(host, "DOWN", None)
            down_count += 1
            print ("-----------------------------------------------")
           
            
    with open("logs/results.log", 'a') as file:
        file.write("\n-------------------- SUMMARY --------------------\n")
        file.write(f"Total Hosts Checked: {total}\n")
        file.write(f"Hosts UP: {up_count}\n")
        file.write(f"Hosts DOWN: {down_count}\n")
        file.write("-------------------------------------------------\n")
        
    print("\n----------------------------------------")
    if total > 0:
        up_percent = (up_count / total) * 100
        down_percent = (down_count / total) * 100
    else:
        up_percent = down_percent = 0
    
    print(f"UP Percentage: {up_percent:.2f}%")
    print(f"DOWN Percentage: {down_percent:.2f}%")



    










