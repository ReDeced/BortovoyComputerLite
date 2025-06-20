import os
from tkinter import Tk, filedialog

import speech_recognition as sr
import win32com.client
import win32gui
import win32con

from MOTVOY_III import MOTVOY_III

root = Tk()
root.withdraw()

def listen_for_activation(recognizer, microphone):
    with microphone as source:
        print("Ожидание активационной фразы 'Ало, компьютер'...")
        recognizer.adjust_for_ambient_noise(source)  # Уменьшение фонового шума
        audio = recognizer.listen(source)

    try:
        # Распознаем речь с помощью Google Web Speech API (русский язык)
        phrase = recognizer.recognize_google(audio, language="ru-RU").lower()
        print(f"Распознано: {phrase}")

        if ("алло компьютер" in phrase or "компьютер алло" in phrase or
                "computer алло" in phrase or "алло computer" in phrase):
            print("Слушаю...")
            return True, False
    except sr.UnknownValueError:
        pass  # Речь не распознана
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания: {e}")
        return False, True

    return False, False


def listen_command(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    command = ""
    try:
        command = recognizer.recognize_google(audio, language="ru-RU")
        print(f"Вы сказали: {command}")
    except sr.UnknownValueError:
        print("Не удалось распознать команду")
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания: {e}")

    return command


def main():
    motvoy = MOTVOY_III()

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    running = True
    while running:
        try:
            activated, error = listen_for_activation(recognizer, microphone)
            if activated and not error:
                motvoy.say("assets/listening.wav")
                command = listen_command(recognizer, microphone).lower()
                if command != "":
                    if command.split()[0] == "запусти" or command.split()[0] == "открой":
                        try:
                            os.startfile(os.path.join("shortcuts", f"{' '.join(command.split()[1:])}.lnk"))
                            motvoy.say("assets/opening.wav")
                        except FileNotFoundError:
                            motvoy.say("assets/chose_file_for_shortcut.wav")
                            file_path = filedialog.askopenfilename(title="Выберите файл")

                            if file_path:
                                os.makedirs(f"./shortcuts", exist_ok=True)
                                shortcut_path = os.path.join("shortcuts", f"{' '.join(command.split()[1:])}.lnk")

                                shell = win32com.client.Dispatch("WScript.Shell")
                                shortcut = shell.CreateShortCut(shortcut_path)
                                shortcut.TargetPath = file_path
                                shortcut.WorkingDirectory = os.path.dirname(file_path)
                                shortcut.Save()

                                os.startfile(os.path.join("shortcuts", f"{' '.join(command.split()[1:])}.lnk"))
                                motvoy.say("assets/opening.wav")

                    elif command == "сверни окно":
                        hwnd = win32gui.GetForegroundWindow()
                        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

                    elif command == "работа завершена":
                        running = False

                    elif command == "выключи windows":
                        os.system("shutdown /s /f /t 1")
                        running = False

                    else:
                        motvoy.say(output_path="assets/cannot_do.wav")

            elif error:
                motvoy.say(output_path="assets/no_internet.wav")

        except KeyboardInterrupt:
            running = False

    motvoy.close()

if __name__ == "__main__":
    main()