# Internet Performance Dashboard

This project is a Python-based web dashboard that continuously runs internet speed tests and visualizes the results over time. It helps you monitor your internet connection's performance, including bandwidth, responsiveness (ping/jitter), and reliability (packet loss).

![Dashboard Screenshot](<dashboard_screenshot_placeholder.png>)
*(Note: You can replace the placeholder above with a real screenshot of your dashboard after you get it running.)*

## Features

- **Continuous Monitoring:** Automatically runs a speed test every minute using the official Ookla Speedtest CLI.
- **Data Logging:** Saves all test results to a local `speedtest_log.csv` file.
- **Interactive Dashboard:** Visualizes the data with a web-based dashboard built with Plotly Dash.
- **Dynamic Filtering:** Filter the results by ISP to compare performance if you have multiple providers.
- **Performance Summary:** Get a quick, text-based summary of your connection's performance.
- **Detailed Charts:**
    - **Bandwidth:** See your Download and Upload speeds (in Mbps).
    - **Responsiveness:** Track your connection's latency (Ping) and stability (Jitter).
    - **Reliability:** Monitor your connection's packet loss percentage.
- **Data Export:** Download the currently filtered data as a CSV file directly from the dashboard.

## How to Use

### 1. Prerequisites

- **Python 3:** Make sure Python 3.6 or newer is installed.
- **Ookla Speedtest CLI:** This project uses the official CLI from Ookla, not the `speedtest-cli` Python package.
    1. Download the CLI for your OS from [speedtest.net/apps/cli](https://www.speedtest.net/apps/cli).
    2. Unzip the downloaded file and place the `speedtest.exe` (or `speedtest` on Linux/macOS) inside the `ookla-speedtest-1.2.0-win64` folder in the project directory.

### 2. Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd <repository-name>
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   # Create the environment
   python -m venv venv
   
   # Activate it
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   # source venv/bin/activate
   ```

### 3. Running the Application

You need to run two scripts, preferably in two separate terminals.

**Terminal 1: Start the Data Logger**
This script will run in the background, performing a speed test every minute and saving the results.
```bash
.\venv\Scripts\python.exe run.py
```

**Terminal 2: Start the Dashboard**
This script will launch the web dashboard. The required Python packages (`dash`, `pandas`) will be installed automatically the first time you run it.
```bash
.\venv\Scripts\python.exe dashboard.py
```
After running this command, open your web browser and go to the URL shown in the terminal (usually `http://127.0.0.1:8051/`).

## Contributing
Contributions are welcome! Please read the `CONTRIBUTING.md` file for guidelines on how to get involved.
