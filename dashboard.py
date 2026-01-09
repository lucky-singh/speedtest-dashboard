import subprocess
import sys
import os
import io

def install(package):
    """Installs a package using pip."""
    python_executable = sys.executable
    subprocess.check_call([python_executable, "-m", "pip", "install", package],
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)

def check_and_install_packages():
    """Checks for required packages and installs them if missing."""
    required_packages = ['dash', 'pandas']
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"'{package}' not found. Installing...")
            install(package)
            print(f"'{package}' installed successfully.")

# Run the check and installation first
check_and_install_packages()

import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
from datetime import datetime

# Path to the log file
CSV_FILE = 'speedtest_log.csv'

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Define the layout of the dashboard
app.layout = html.Div([
    dcc.Store(id='data-store'),
    html.H1("Internet Performance Dashboard", style={'textAlign': 'center'}),

    # ISP Filter Dropdown
    html.Div([
        html.Label("Filter by ISP:"),
        dcc.Dropdown(id='isp-dropdown', value='All', clearable=False),
    ], style={'width': '40%', 'margin': 'auto', 'padding': '10px'}),
    
    # Dynamic Summary Section
    html.Div(id='dynamic-summary', style={'width': '80%', 'margin': '20px auto', 'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '5px'}),

    # Graphs
    html.Div([
        dcc.Graph(id='speed-graph'),
        html.P("This chart shows your download and upload speeds. Higher values are better, indicating you can transfer more data, faster.", style={'textAlign': 'center', 'fontSize': '14px', 'color': '#666'})
    ], className="six columns"),

    html.Div([
        dcc.Graph(id='ping-jitter-graph'),
        html.P("This chart shows latency (ping) and its consistency (jitter). Lower values are better, indicating a more responsive and stable connection.", style={'textAlign': 'center', 'fontSize': '14px', 'color': '#666'})
    ], className="six columns"),
    
    html.Div([
        dcc.Graph(id='packet-loss-graph'),
        html.P("This chart shows the percentage of data 'packets' lost during transmission. This should always be 0% for a reliable connection.", style={'textAlign': 'center', 'fontSize': '14px', 'color': '#666'})
    ], className="twelve columns", style={'clear': 'both'}),


    dcc.Interval(id='interval-component', interval=5 * 1000, n_intervals=0),
    
    html.Div([
        html.Button("Download Filtered Data", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
    ], style={'textAlign': 'center', 'padding': '20px'})

], style={'fontFamily': 'sans-serif'})


# Callback to periodically read data from CSV and store it
@app.callback(Output('data-store', 'data'), Input('interval-component', 'n_intervals'))
def update_data_store(n):
    try:
        df = pd.read_csv(CSV_FILE)
        return df.to_json(date_format='iso', orient='split')
    except FileNotFoundError:
        return None

# Callback to update ISP dropdown options from stored data
@app.callback(Output('isp-dropdown', 'options'), Input('data-store', 'data'))
def update_dropdown_options(jsonified_data):
    if jsonified_data is None: return [{'label': 'All', 'value': 'All'}]
    df = pd.read_json(io.StringIO(jsonified_data), orient='split')
    isps = df['ISP'].unique()
    options = [{'label': isp, 'value': isp} for isp in isps]
    options.insert(0, {'label': 'All', 'value': 'All'})
    return options

# Callback to update all graphs and summary based on stored data and dropdown
@app.callback(
    Output('speed-graph', 'figure'),
    Output('ping-jitter-graph', 'figure'),
    Output('packet-loss-graph', 'figure'),
    Output('dynamic-summary', 'children'),
    Input('data-store', 'data'),
    Input('isp-dropdown', 'value')
)
def update_all_outputs(jsonified_data, selected_isp):
    if jsonified_data is None:
        empty_figure = {'data': [], 'layout': {'title': 'Waiting for data...'}}
        summary = html.P("No data found. Ensure 'run.py' is running and has generated a 'speedtest_log.csv' file.")
        return empty_figure, empty_figure, empty_figure, summary

    df = pd.read_json(io.StringIO(jsonified_data), orient='split')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    if selected_isp == 'All' or selected_isp is None:
        filtered_df = df
        title_isp = 'All ISPs'
    else:
        filtered_df = df[df['ISP'] == selected_isp]
        title_isp = selected_isp

    # --- Generate Dynamic Summary ---
    if not filtered_df.empty:
        avg_dl = filtered_df['Download (Mbps)'].mean()
        avg_ul = filtered_df['Upload (Mbps)'].mean()
        avg_ping = filtered_df['Ping (ms)'].mean()
        avg_jitter = filtered_df['Jitter (ms)'].mean()
        max_loss = filtered_df['Packet Loss'].max()

        summary_header = html.H4(f"Performance Summary for {title_isp}", style={'textAlign': 'center'})
        summary_lines = [
            f"Average Speed: {avg_dl:.2f} Mbps Download / {avg_ul:.2f} Mbps Upload.",
            f"Average Responsiveness: {avg_ping:.2f} ms Ping with {avg_jitter:.2f} ms Jitter.",
        ]
        if avg_ping > 100:
            summary_lines.append("Note: The average ping is high, which may cause noticeable lag in gaming and video calls.")
        if max_loss > 0:
            summary_lines.append(f"Warning: Packet loss was detected (max {max_loss}%), indicating potential connection instability.")
        
        summary = [summary_header] + [html.P(line) for line in summary_lines]
    else:
        summary = html.P(f"No data available for {title_isp}.")


    # --- Create Figures ---
    speed_figure = {'data': [{'x': filtered_df['Timestamp'], 'y': filtered_df['Download (Mbps)'], 'name': 'Download'}, {'x': filtered_df['Timestamp'], 'y': filtered_df['Upload (Mbps)'], 'name': 'Upload'}], 'layout': {'title': f'Bandwidth (Mbps)', 'yaxis': {'title': 'Speed (Mbps)'}, 'hovermode': 'x unified'}}
    ping_figure = {'data': [{'x': filtered_df['Timestamp'], 'y': filtered_df['Ping (ms)'], 'name': 'Ping'}, {'x': filtered_df['Timestamp'], 'y': filtered_df['Jitter (ms)'], 'name': 'Jitter'}], 'layout': {'title': f'Responsiveness (ms)', 'yaxis': {'title': 'Latency (ms)'}, 'hovermode': 'x unified'}}
    loss_figure = {'data': [{'x': filtered_df['Timestamp'], 'y': filtered_df['Packet Loss'], 'name': 'Packet Loss'}], 'layout': {'title': f'Reliability (% Packet Loss)', 'yaxis': {'title': 'Loss (%)'}, 'hovermode': 'x unified'}}
        
    return speed_figure, ping_figure, loss_figure, summary

# Callback for the download button
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    State('data-store', 'data'),
    State('isp-dropdown', 'value'),
    prevent_initial_call=True,
)
def download_csv(n_clicks, jsonified_data, selected_isp):
    if jsonified_data is None: return None
    df = pd.read_json(io.StringIO(jsonified_data), orient='split')
    if selected_isp != 'All' and selected_isp is not None:
        df = df[df['ISP'] == selected_isp]
    return dcc.send_data_frame(df.to_csv, f"speedtest_data_{selected_isp.replace(' ', '_')}.csv", index=False)


if __name__ == '__main__':
    app.run(debug=True, port=8051)