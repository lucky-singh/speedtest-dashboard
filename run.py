import subprocess
import json
import csv
import time
import os
from datetime import datetime

def run_speedtest():
    # Check for the official CLI in the specific folder 'ookla-speedtest-1.2.0-win64'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_exe = os.path.join(script_dir, 'ookla-speedtest-1.2.0-win64', 'speedtest.exe')

    if os.path.exists(local_exe):
        cmd = [local_exe, '--accept-license', '--accept-gdpr', '--format=json']
    else:
        cmd = ['speedtest', '--accept-license', '--accept-gdpr', '--format=json']

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error running speedtest (Exit Code {result.returncode}):")
            print(result.stderr)
            if "license" in result.stderr.lower():
                print("\nTIP: It looks like the license isn't accepted. Try running this command manually once in your terminal:")
                print(f'"{cmd[0]}"')
            return None

        if not result.stdout.strip():
            print("ERROR: Speedtest returned nothing.")
            print(f"STDERR: {result.stderr}")
            print("Hint: Ensure you have the official Ookla Speedtest CLI installed (https://www.speedtest.net/apps/cli), not the python 'speedtest-cli' package.")
            return None

        data = json.loads(result.stdout)
        
        # Convert bytes/sec to Mbps (Bytes * 8 / 1,000,000)
        return {
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Download (Mbps)': round(data['download']['bandwidth'] / 125000, 2),
            'Upload (Mbps)': round(data['upload']['bandwidth'] / 125000, 2),
            'Ping (ms)': round(data['ping']['latency'], 2),
            'Jitter (ms)': round(data['ping']['jitter'], 2),
            'Packet Loss': data.get('packetLoss', 0),
            'ISP': data['isp'],
            'Result URL': data['result']['url']
        }

    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    csv_file = 'speedtest_log.csv'
    file_exists = os.path.isfile(csv_file)
    
    print(f"Starting continuous speedtest. Saving to {csv_file}...")
    print("Press Ctrl+C to stop.")

    with open(csv_file, mode='a', newline='') as f:
        fieldnames = ['Timestamp', 'Download (Mbps)', 'Upload (Mbps)', 'Ping (ms)', 'Jitter (ms)', 'Packet Loss', 'ISP', 'Result URL']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        while True:
            print(f"Running test at {datetime.now().strftime('%H:%M:%S')}...")
            result = run_speedtest()
            if result:
                writer.writerow(result)
                f.flush()
                print(f"  -> Down: {result['Download (Mbps)']} Mbps | Up: {result['Upload (Mbps)']} Mbps | Ping: {result['Ping (ms)']} ms")
            
            # Wait 60 seconds before next test
            time.sleep(60)

if __name__ == "__main__":
    main()
