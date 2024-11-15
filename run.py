import subprocess
import os
import time
import threading
import signal
import sys
import logging
logging.basicConfig(format='%(message)s')
logging.root.setLevel(logging.NOTSET)
handler = logging.StreamHandler(sys.stdout)
log = logging.getLogger(__name__)
log.addHandler(handler)
def print(a):
    log.info(a)
base = os.getcwd()
# List of daemon bash scripts with optional custom prefixes
scripts_with_prefixes = [
    {'script': 'arrpc_start.sh', 'prefix': 'arRPC'},
    {'script': 'discord-headless_start.sh', 'prefix': 'Discord Headless'},
    {'script': 'subsonic-rich_start.sh', 'prefix': "Subsonic Rich Presence"},
    {'script': 'api_start.sh', 'prefix': "Dashboard Api"},
    {'script': 'web_start.sh', 'prefix': "Dashboard Web"}
]
processes = []
pids = []
def run_script_as_daemon_with_log(script_name):
    global pids
    os.chdir("bin")
    """Function to start a bash script as a daemon with log output."""
    process = subprocess.Popen(
        ['/bin/bash', script_name],  # Call the bash script
        stdout=subprocess.PIPE,      # Capture stdout
        stderr=subprocess.PIPE,      # Capture stderr
        close_fds=True,              # Close file descriptors, making it independent
        preexec_fn=os.setpgrp         # Detach from the parent process, making it a daemon
    )
    os.chdir(base)
    pids.append(os.getpgid(process.pid))
    return process
def log_output(prefix, stream):
    """Function to print the log output with a prefix."""
    for line in iter(stream.readline, b''):
        print(f"[{prefix}] {line.decode().strip()}")
    stream.close()
def terminate_processes():
    """Terminate all running daemon processes."""
    print("Terminating all daemons...")
    for process in processes:
        try:
            # Send SIGTERM to terminate the process group started by
            os.setpgrp()
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except Exception as e:
            print(f"Error terminating process {process.pid}: {e}")
def signal_handler(sig, frame):
    """Handle termination signals (SIGINT/SIGTERM) to stop daemons."""
    terminate_processes()
    time.sleep(4)
    os.system("rm temp/pids.txt")
    sys.exit(0)
if __name__ == "__main__":
  if len(sys.argv) > 1 and sys.argv[1].strip() != "":
    argument = sys.argv[1].strip()  # assign to variable, with whitespace removed
  else:
    print("Error: No valid argument provided.")
    sys.exit(1)  # exit with code 1
  if argument == "start":
    # Register signal handler to handle Ctrl+C or SIGTERM
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    for script_info in scripts_with_prefixes:
        script = script_info['script']
        custom_prefix = script_info['prefix'] or script  # Use custom prefix or default to script name
        print(f"Starting {script} as a daemon in the background...")
        # Start the bash script as a daemon with log capture
        process = run_script_as_daemon_with_log(script)
        processes.append(process)
        # Start threads to read and log stdout and stderr with custom prefixes
        threading.Thread(target=log_output, args=(custom_prefix, process.stdout), daemon=True).start()
        threading.Thread(target=log_output, args=(custom_prefix + " (internal, error)", process.stderr), daemon=True).start()
        # Delay to ensure scripts are started in sequence (2 seconds)        time.sleep(2)
    print("All scripts have been started as daemons with customizable log prefixes.")
    pdfile = open("temp/pids.txt", "w")
    pdfile.write(str(pids))
    pdfile.close()
    # Keep the main script running until interrupted
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        os.system("rm temp/pids.txt")
        time.sleep(1)
        terminate_processes()
  elif argument == "kill":
    os.system("cd entrypoint/ && python3 emergkill.py")
  elif argument == "auth":
    os.system("cd entrypoint && python3 auth.py")
  elif argument == "install_chrome":
   os.system("cd bin && bash chrome_download.sh")
  else:
    print("Invalid Argument")
    sys.exit(1)
    
