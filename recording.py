import wave
import pyaudio as py
import keyboard
from array import array

print('Введи название файла')
file_name = f"C:\\Users\\mishu\\Downloads\\Лаба 2 АА\\Лаба 2 АА\\Lab_2\\voise_recording\\{input().strip()}.wav"

CHUNK = 1024
CHANNELS = 1
RATE = 22050
FORMAT = py.paInt16

p = py.PyAudio()
data_all = array('h')
trigger = False


def callback(in_data, frame_count, time_info, status):
    data_chunk = array('h', in_data)
    data_all.extend(data_chunk)
    return in_data, py.paContinue


def key_press(e):
    global trigger
    if e.name == 's' and not trigger:
        stream.stop_stream()
        stream.close()
        keyboard.unhook_all()
        wav = wave.open(file_name, "wb")
        wav.setnchannels(CHANNELS)
        wav.setframerate(RATE)
        wav.setsampwidth(p.get_sample_size(FORMAT))
        wav.writeframes(data_all)
        wav.close()
        p.terminate()
        print('Stop recording')
        trigger = True

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                start=False,
                stream_callback=callback)
stream.start_stream()
print('Recording')


while not keyboard.is_pressed('esc'):
    keyboard.hook(key_press)

if not trigger:
    stream.stop_stream()
    stream.close()
    p.terminate()
    print('Recording not saved')
else:
    print('Recording saved')
