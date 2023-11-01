import os
import pandas as pd

# Функция для загрузки всех файлов из указанной директории
def load_files_from_directory(directory):
    data_frames = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.csv', '.xlsx')):
                file_path = os.path.join(root, file)
                if file.endswith('.csv'):
                    data_frames.append(pd.read_csv(file_path))
                else:
                    data_frames.append(pd.read_excel(file_path))
    return data_frames

# Функция для объединения всех данных в один DataFrame
def combine_dataframes(data_frames):
    print(pd.concat(data_frames, ignore_index=True))
    if data_frames:
        return pd.concat(data_frames, ignore_index=True)
    else:
        return None

# Функция для выполнения нечеткого поиска по номеру телефона
def fuzzy_search_by_phone(data_frame, phone):
    if data_frame is not None:
        return data_frame[data_frame['phone'].str.contains(phone, na=False, case=False, regex=False)]
    return None

# Загрузка данных из указанной директории
data_directory = '/db/sliv/'
data_frames = load_files_from_directory(data_directory)

# Проверка, есть ли данные для объединения
if data_frames:
    # Объединение данных в один DataFrame
    combined_data = combine_dataframes(data_frames)
    
    # Выполнение нечеткого поиска по номеру телефона
    query = '9643426406'  # Здесь укажите ваш запрос
    result = fuzzy_search_by_phone(combined_data, query)

    # Вывод результата
    if result is not None:
        print(result)
    else:
        print("Нет данных, удовлетворяющих запросу.")
else:
    print("Нет данных для обработки.")
