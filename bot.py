import subprocess
import time
import os

def run_bot(script_path, restart_interval):
    while True:
        try:
            if not os.path.exists(script_path):
                print(f"Error: {script_path} does not exist!")
                break

            print(f"Starting {script_path}...")

            # Start the bot and redirect output to log files
            with open("bot_output.log", "a") as out_file, \
                 open("bot_error.log", "a") as err_file:
                process = subprocess.Popen(
                    ["python", script_path],  # Using just "python"
                    stdout=out_file,
                    stderr=err_file
                )

            # Monitor the bot process
            start_time = time.time()
            while time.time() - start_time < restart_interval:
                if process.poll() is not None:
                    print(f"Bot exited with status {process.returncode}. Restarting...")
                    break
                time.sleep(5)  # Sleep for a short period to avoid busy-waiting

            # If the bot is still running after the interval, terminate it
            if process.poll() is None:
                print(f"Bot is still running after {restart_interval} seconds. Terminating...")
                process.terminate()
                process.wait()

            print(f"Restarting {script_path} in 15 seconds...")
            time.sleep(15)  # Wait before restarting

        except subprocess.CalledProcessError as e:
            print(f"Bot exited with error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

# Assuming the script is in the same directory as this file inside the container
script_path = "wcalculateit.py"  # Adjust based on your script's actual name
run_bot(script_path, restart_interval=3600)

