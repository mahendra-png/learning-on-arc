import os
import subprocess

def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return str(e)
    
def write_file(path, content):
    try:
        with open(path, "w") as f:
            f.write(content)
        return "file return successfully"
    except Exception as e:
        return str(e)
    
def run_Shell(command):
    blocked = ["rm", "shutdown", "reboot"]
    if any(word in command for word in blocked):
        return "Command blocked for safety"
    
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True
        )
        return result.stdout or result.stderr
    except Exception as e:
        return str(e)
    