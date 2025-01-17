import getpass
import platform
import time
import psutil
import GPUtil
import speedtest
import random
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

def display_menu():
    ascii_art = r"""
 _____             _____ _           _           
|  _  |___ ___ ___|     | |_ ___ ___| |_ ___ ___ 
|   __| -_|  _|___|   --|   | -_|  _| '_| -_|  _|
|__|  |___|_|     |_____|_|_|___|___|_,_|___|_|  
                                                  """
    
    # Random color for ASCII art
    random_color = random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])
    
    print(random_color + ascii_art)
    
    # Description of the tool
    print(Fore.WHITE + "This tool measures the performance of your system components, including CPU, GPU, memory, and network speed.")
    print(Fore.WHITE + "It is part of the project available at: https://github.com/syntax-15")
    
    menu_options = [
        "1. Show performance metrics",
        "2. Show discipline ratings",
        "3. Overall evaluation",
        "4. Exit"
    ]
    
    # Create a border
    border_symbol = "*"
    border_length = 50
    border = border_symbol * border_length
    
    print(border)
    print(Fore.GREEN + "Select an option:")
    for option in menu_options:
        print(Fore.GREEN + option)
    
    print(border)

def get_performance_metrics():
    # Measure CPU, RAM, and disk
    print(Fore.YELLOW + "Measuring CPU...")
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq().current  # Get current CPU frequency
    
    print(Fore.YELLOW + "Measuring memory...")
    memory_info = psutil.virtual_memory()
    
    print(Fore.YELLOW + "Measuring disk...")
    try:
        disk_usage = psutil.disk_usage('C:\\')  # Use 'C:\\' for Windows
    except Exception as e:
        print(Fore.RED + "Error measuring disk usage:", e)
        disk_usage = None

    # Get CPU temperature (if supported)
    try:
        print(Fore.YELLOW + "Getting CPU temperature...")
        temperatures = psutil.sensors_temperatures()
        cpu_temp = temperatures['coretemp'][0].current if 'coretemp' in temperatures else None
    except Exception as e:
        cpu_temp = None

    # Get GPU information
    gpus = GPUtil.getGPUs()
    if gpus:
        print(Fore.YELLOW + "Measuring GPU...")
        gpu_usage = gpus[0].load * 100
        gpu_temp = gpus[0].temperature
        gpu_freq = gpus[0].gpu_clock  # Get current GPU frequency
    else:
        gpu_usage = None
        gpu_temp = None
        gpu_freq = None

    # Measure network speed
    print(Fore.YELLOW + "Measuring network speed...")
    try:
        st = speedtest.Speedtest()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000      # Convert to Mbps
    except Exception as e:
        print(Fore.RED + "Error measuring network speed:", e)
        download_speed = None
        upload_speed = None

    metrics = {
        'CPU Usage (%)': cpu_usage,
        'CPU Frequency (MHz)': cpu_freq,
        'Memory Usage (%)': memory_info.percent,
        'Disk Usage (%)': disk_usage.percent if disk_usage else None,
        'CPU Temperature (°C)': cpu_temp,
        'GPU Usage (%)': gpu_usage,
        'GPU Frequency (MHz)': gpu_freq,
        'GPU Temperature (°C)': gpu_temp,
        'Download Speed (Mbps)': download_speed,
        'Upload Speed (Mbps)': upload_speed
    }
    
    return metrics

def evaluate_scores(metrics):
    # Evaluate discipline ratings based on performance metrics
    scores = {}

    # Example scoring logic based on CPU usage
    if metrics['CPU Usage (%)'] < 50:
        scores['Gaming Performance'] = 95
    elif metrics['CPU Usage (%)'] < 75:
        scores['Gaming Performance'] = 80
    else:
        scores['Gaming Performance'] = 60

    # Example scoring logic based on memory usage
    if metrics['Memory Usage (%)'] < 50:
        scores['Productivity'] = 90
    elif metrics['Memory Usage (%)'] < 75:
        scores['Productivity'] = 75
    else:
        scores['Productivity'] = 50

    # Example scoring logic based on GPU usage
    if metrics['GPU Usage (%)'] is not None:
        if metrics['GPU Usage (%)'] < 50:
            scores['Multimedia'] = 90
        elif metrics['GPU Usage (%)'] < 75:
            scores['Multimedia'] = 70
        else:
            scores['Multimedia'] = 40
    else:
        scores['Multimedia'] = 0  # No GPU available

    return scores

def overall_evaluation(metrics):
    # Calculate total score and detailed scores
    total_score = 0
    detailed_scores = {}

    # Calculate total score based on individual metrics
    detailed_scores['Gaming Performance'] = evaluate_scores(metrics)['Gaming Performance']
    detailed_scores['Productivity'] = evaluate_scores(metrics)['Productivity']
    detailed_scores['Multimedia'] = evaluate_scores(metrics)['Multimedia']

    # Calculate total score as the average of the detailed scores
    total_score = (detailed_scores['Gaming Performance'] + 
                   detailed_scores['Productivity'] + 
                   detailed_scores['Multimedia']) / 3

    # Add detailed scores for CPU, GPU, and Disk
    detailed_scores['CPU Score'] = max(0, 100 - metrics['CPU Usage (%)'])  # Lower usage = higher score
    detailed_scores['Disk Score'] = max(0, 100 - metrics['Disk Usage (%)']) if metrics['Disk Usage (%)'] is not None else 0
    detailed_scores['Memory Score'] = max(0, 100 - metrics['Memory Usage (%)'])  # Lower usage = higher score

    return total_score, detailed_scores

def main():
    username = getpass.getuser()
    os_name = platform.system()
    
    while True:
        display_menu()
        user_input = input(f"{username}@{os_name}➤ ")
        
        if user_input == '1':
            metrics = get_performance_metrics()
            for key, value in metrics.items():
                print(Fore.WHITE + f"{key}: {value}")
        elif user_input == '2':
            metrics = get_performance_metrics()
            scores = evaluate_scores(metrics)
            for key, value in scores.items():
                print(Fore.WHITE + f"{key}: {value}")
        elif user_input == '3':
            metrics = get_performance_metrics()
            total_score, detailed_scores = overall_evaluation(metrics)
            print(Fore.WHITE + "Overall Evaluation:")
            print(Fore.WHITE + f"Total Score: {total_score}")
            for key, value in detailed_scores.items():
                print(Fore.WHITE + f"{key}: {value}")  # Display detailed scores
        elif user_input == '4':
            print(Fore.GREEN + "Exiting the program. Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid option. Please try again.")

if __name__ == "__main__":
    main()
