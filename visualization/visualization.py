import os
import re
import matplotlib.pyplot as plt
# from matplotlib.ticker import FormatStrFormatter, MultipleLocator
import numpy as np

def parse_folder_name(folder_name):
    """
    Klasör adını çözümleyerek test periyodu ve cihaz numarasını döndürür.
    
    Args:
        folder_name (str): Klasör adı, örneğin "Test_30_193".
        
    Returns:
        tuple: (periyot, cihaz) şeklinde iki adet integer değer.
        
    Raises:
        ValueError: Klasör adı formatı geçersizse hata fırlatır.
    """
    match = re.match(r"Test_(\d+)_(\d+)", folder_name)
    if match:
        period = int(match.group(1))
        device = int(match.group(2))
        return period, device
    else:
        raise ValueError("Folder name format is invalid.")


def read_logs(base_folder):
    """
    Verilen ana klasördeki tüm log dosyalarını okur ve içeriklerini analiz eder.
    
    Args:
        base_folder (str): Log dosyalarının bulunduğu ana klasör yolu.
        
    Returns:
        tuple: (log_contents, average_percentages, average_delay)
            - log_contents (dict): Her test için log dosyalarının içeriği.
            - average_percentages (dict): Her test için ortalama yüzdelikler.
            - average_delay (dict): Her test için ortalama gecikme süreleri.
    """
    log_contents = {}
    average_percentages = {}
    average_delay = {}
    
    for test_folder in os.listdir(base_folder):
        test_folder_path = os.path.join(base_folder, test_folder)
        
        if os.path.isdir(test_folder_path):
            test_dict = {}
            
            for run_num in range(1, 31):
                run_folder_name = f"run{run_num}"
                run_folder_path = os.path.join(test_folder_path, run_folder_name)
                
                log_file_path = os.path.join(run_folder_path, "log.txt")
                
                if os.path.isfile(log_file_path):
                    with open(log_file_path, 'r') as file:
                        last_line = file.readlines()[-1]
                        last_line = last_line.split(" ")
                        test_dict[run_folder_name] = last_line
            
            log_contents[test_folder] = test_dict
            
            percentages = [round(float(run_data[3][:-1]), 4) for run_data in test_dict.values()]
            average_percentages[test_folder] = np.mean(percentages)

            delays = [round(float(run_data[4][:-2]), 4) for run_data in test_dict.values()]
            average_delay[test_folder] = np.mean(delays)
    
    return log_contents, average_percentages, average_delay


def plot_performance(log_contents, device, period, metric='percentage'):
    """
    Belirli bir cihaz ve periyot için performans grafiği çizer.
    
    Args:
        log_contents (dict): Test loglarının içeriği.
        device (int): Cihaz numarası.
        period (int): Test periyodu (saniye).
        metric (str): Çizilecek metrik, 'percentage' veya 'delay' olabilir.
    """
    test_key = f"Test_{period}_{device}"
    data_index = 3 if metric == 'percentage' else 4
    unit = '%' if metric == 'percentage' else 's'
    
    data = [float(run_data[data_index][:-1]) for run_data in log_contents[test_key].values()] if metric == 'percentage' else [float(run_data[data_index][:-2]) for run_data in log_contents[test_key].values()]
    average_value = round(sum(data) / len(data), 4)
    performance_data = [float(run_data[1]) for run_data in log_contents[test_key].values()]
    test_numbers = np.arange(1, len(performance_data) + 1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(test_numbers, data, marker='o', linestyle='-')
    plt.axhline(y=average_value, color='r', linestyle='--', label=f'Ortalama: {average_value:.4f}{unit}')
    plt.xlabel('Test Sayısı')
    plt.ylabel(f'{metric.capitalize()} ({unit})')
    plt.title(f'End Device: {device}, Periyot: {period} s')
    plt.grid(False)
    plt.legend()
    
    ax = plt.gca()  # Mevcut ekseni al
    
    if metric == 'percentage':
        plt.ylim(0, 100)

    else:
        pass
        # ax.yaxis.set_minor_locator(MultipleLocator(0.01))
        # ax.yaxis.set_major_formatter(FormatStrFormatter('%.4f'))  # Ondalık basamak sayısını ayarlama
    
    plt.show()


def plot_summary_performance(average_dict, title, xlabel, ylabel, sort_key_index, unit='%', xtick_rotation=45):
    """
    Ortalama performans değerlerini özetleyen bir grafik çizer.
    
    Args:
        average_dict (dict): Ortalama değerlerin bulunduğu sözlük.
        title (str): Grafiğin başlığı.
        xlabel (str): X ekseni etiketi.
        ylabel (str): Y ekseni etiketi.
        sort_key_index (int): Sıralama yapılacak anahtarın indeks numarası.
        unit (str): Y ekseni birimi, varsayılan '%'.
        xtick_rotation (int): X ekseni etiketlerinin dönüş açısı, varsayılan 45 derece.
    """
    sorted_items = sorted(list(average_dict.items()), key=lambda x: int(x[0].split('_')[sort_key_index]))
    x_values = [int(test.split('_')[sort_key_index]) for test, _ in sorted_items]
    y_values = [value for _, value in sorted_items]
    average_value = round(sum(y_values) / len(y_values), 4)

    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, marker='o', linestyle='-', label='Test Yüzdelikleri')
    plt.axhline(y=average_value, color='r', linestyle='--', label=f'Ortalama: {average_value:.4f}{unit}')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xlim(min(x_values) - 10, max(x_values) + 10)
    plt.xticks(x_values, rotation=xtick_rotation)
    plt.legend()
    plt.grid(False)
    plt.show()


script_dir = os.path.dirname(os.path.abspath(__file__))
experiments_dir = os.path.join(script_dir, "experiments")

base_folders = [
    os.path.join(experiments_dir, "deviceSabit"),
    os.path.join(experiments_dir, "periodSabit")
]

average_percentage_dict = {}
average_delay_dict = {}

for base_folder in base_folders:
    print(f"Reading logs from: {base_folder}")
    log_contents, average_percentages, average_delay = read_logs(base_folder)
    average_percentage_dict.update(average_percentages)
    average_delay_dict.update(average_delay)
    for folder_name in log_contents.keys():
        period, device = parse_folder_name(folder_name)
        plot_performance(log_contents, device, period, metric='percentage')
        plot_performance(log_contents, device, period, metric='delay')

print("Average Percentage Dictionary:")
print(average_percentage_dict)
print("Average Delay Dictionary:")
print(average_delay_dict)

plot_summary_performance(dict(sorted(list(average_percentage_dict.items())[6:])), 'Periyot Sabit(25s), End Device Değişken', 'End Device', 'Packet Delivery Ratio (%)', -1)
plot_summary_performance(dict(sorted(list(average_percentage_dict.items())[:6])), 'End Device Sabit(193), Periyot Değişken', 'Period (s)', 'Packet Delivery Ratio (%)', 1)
plot_summary_performance(dict(sorted(list(average_delay_dict.items())[6:])), 'Periyot Sabit(25s), End Device Değişken', 'End Device', 'Delay (s)', -1, unit='s')
plot_summary_performance(dict(sorted(list(average_delay_dict.items())[:6])), 'End Device Sabit(193), Periyot Değişken', 'Period (s)', 'Delay (s)', 1, unit='s')
