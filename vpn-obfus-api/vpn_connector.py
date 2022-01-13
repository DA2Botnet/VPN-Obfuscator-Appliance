import os
import json
import subprocess
import time
import requests

os.chdir("/etc/openvpn")

# Command to kill any running instances of OpenVPN
kill_command = "sudo killall openvpn"

# URL to the NordVPN server connection tool obtained from the browser
url = "" # Insert URL here

def start_openvpn_connection():
    response = requests.get(url)

    if len(response.text) != 2:
        nvpn_response = json.loads(response.text)
        vpn_info = nvpn_response[0]
        vpn_info_hostname = vpn_info["hostname"]
        vpn_file = vpn_info_hostname + ".udp1194.ovpn"

        # Command to start Openvpn
        ov_command = "sudo openvpn --config " + vpn_file

        # Start the NordVPN connection
        subprocess.Popen(ov_command.split())

if __name__ == "__main__":
    subprocess.Popen(kill_command.split())
    time.sleep(2)
    start_openvpn_connection()
