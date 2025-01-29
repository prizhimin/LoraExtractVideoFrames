import cv2
import os
import numpy as np

def extract_unique_frames(video_path, output_folder, threshold=99):
    # Проверяем, существует ли выходная папка, если нет — создаем
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Открываем видеофайл
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Ошибка: Не удалось открыть видеофайл {video_path}")
        return

    frame_count = 0
    saved_frame_count = 0
    prev_frame = None

    while True:
        # Читаем кадр из видео
        ret, frame = cap.read()

        # Если кадр не удалось прочитать, выходим из цикла
        if not ret:
            break

        # Преобразуем кадр в оттенки серого для упрощения сравнения
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Если это первый кадр или текущий кадр значительно отличается от предыдущего
        if prev_frame is None or np.abs(gray_frame - prev_frame).mean() > threshold:
            # Сохраняем кадр в файл
            frame_filename = os.path.join(output_folder, f"image_{saved_frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            print(f"Сохранено уникальное изображение {saved_frame_count} в {frame_filename}")

            # Обновляем предыдущий кадр
            prev_frame = gray_frame
            saved_frame_count += 1

        frame_count += 1

    # Освобождаем ресурсы
    cap.release()
    print(f"Всего обработано {frame_count} кадров. Сохранено {saved_frame_count} уникальных изображений.")

if __name__ == "__main__":
    # Укажите путь к видеофайлу и папку для сохранения изображений
    video_path = r"R:\input_video.mov"
    output_folder = r"R:\output_images"

    # Извлекаем уникальные изображения из видео
    extract_unique_frames(video_path, output_folder)
