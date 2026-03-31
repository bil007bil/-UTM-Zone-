import pandas as pd
from pyproj import Transformer
import os

# 1. Прямой путь к вашему файлу
input_file = r'E:\Рабочий стол\ГПНИ\скважины градусы.dat'

# 2. Путь для сохранения результата
base_path = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(base_path, 'belarus_utm35n.csv')

if not os.path.exists(input_file):
    print(f"Ошибка: Файл не найден по пути {input_file}")
else:
    try:
        # Читаем данные (запятая как разделитель в исходном файле)
        df = pd.read_csv(input_file, sep=',', names=['X_lon', 'Y_lat', 'Z'], header=None)

        # Настройка трансформации (WGS84 -> UTM 35N)
        transformer = Transformer.from_crs("epsg:4326", "epsg:32635", always_xy=True)

        print(f"Начинаю пересчет {len(df)} точек...")

        # Пересчет
        x_utm, y_utm = transformer.transform(df['X_lon'].values, df['Y_lat'].values)
        df['X_utm'] = x_utm
        df['Y_utm'] = y_utm

        # Оставляем только нужные колонки
        df_final = df[['X_utm', 'Y_utm', 'Z']]

        # ИЗМЕНЕНИЕ ЗДЕСЬ: используем sep=';' для Excel и decimal='.'
        # Это заставит Excel сразу разнести данные по столбцам
        df_final.to_csv(output_file, index=False, sep=';', decimal='.')

        print(f"Успешно! Файл создан: {output_file}")
        print("Теперь Excel откроет его по столбцам.")

    except Exception as e:
        print(f"Произошла ошибка при обработке: {e}")