import simpleaudio
import asyncio
import os
from time import time, sleep
import shutil


class MOTVOY_III:
    def __init__(self):
        print("ЗАГРУЗКА")
        print("ЗАГРУЗКА ЗАВЕРШЕНА")


    def say(self, output_path, wait=False):
        wav_path = output_path

        wave_obj = simpleaudio.WaveObject.from_wave_file(wav_path)
        play_obj = wave_obj.play()

        if wait:
            play_obj.wait_done()


    def close(self):
        self.say("assets/shutting_down.wav", wait=True)
        shutil.rmtree(f"./temp", ignore_errors=False)
        os.mkdir("temp")