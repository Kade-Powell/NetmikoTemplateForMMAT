import asyncio
from netmiko import Netmiko, ConnectHandler
import concurrent.futures
import time

##this is the function that does the work - takes hosts as an arguement##
def sendCommand(host):
    users = ["tacacsUser", "backupUser"]
    passwords = ["tacacsPass", "backupPass"]
    for user, password in zip(users, passwords):
        try:
            nokia7210 = {
                "host": host,
                "username": user,
                "password": password,
                "device_type": "alcatel_sros",
            }
            net_connect = ConnectHandler(**nokia7210)

            commands = [
                "show chassis | match Location",
                "show version",
                "show port",
            ]

            tid = net_connect.find_prompt()
            output = net_connect.send_config_set(commands)
            net_connect.disconnect()
            # print(output)
            outputList.append(output)
            return tid

        except Exception as e:
            print(e)


def main():
    # Runs in a custom thread pool:
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        # set some hosts will need to be a csv file later
        hosts = [
            "172.17.239.154",
            "172.17.239.182",
            "172.17.238.249",
            "172.24.36.231",
            "172.24.36.241",
            "172.17.251.58",
            "172.24.36.220",
            "172.17.238.231",
            "172.17.238.220",
            "172.17.238.241",
        ]
        results = [pool.submit(sendCommand, host) for host in hosts]

        for f in concurrent.futures.as_completed(results):
            print(f.result())


if __name__ == "__main__":
    start_time = time.time()
    outputList = []
    main()
    outputList.sort()
    for s in outputList:
        print(s)

    print("--- %s seconds ---" % (time.time() - start_time))
