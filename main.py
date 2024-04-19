import pyaudio
import wave
import numpy as np
import struct
import time
from collections import deque

# Pre-defining audio constants
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
THRESHOLD = 2000
WAVE_OUTPUT_FILENAME = "clap.wav"
WINDOW_SIZE = int(RATE * 2)  # Size of the sliding window
RECORD_DURATION = 5  # Duration to save after clap detection

audio = pyaudio.PyAudio()

def SetMicrophone():
    global CHANNELS
    index = audio.get_default_input_device_info()['index']
    info = audio.get_device_info_by_index(index)
    print(info["name"])
    CHANNELS = info["maxInputChannels"]

def SaveRecording(frames):
    wavefile = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    wavefile.setnchannels(CHANNELS)
    wavefile.setsampwidth(audio.get_sample_size(FORMAT))
    wavefile.setframerate(RATE)
    wavefile.writeframes(b''.join(struct.pack('<h', s) for s in frames)) # SHOUTOUT TO
    wavefile.close()

def SplitRecording(frames):
    frames_to_save = list(frames)[-int(RATE * RECORD_DURATION):]
    SaveRecording(frames_to_save)
    print(f"Saved audio input to {WAVE_OUTPUT_FILENAME}")

def ReceiveStream():
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True, # Enable microphone recording
                        frames_per_buffer=CHUNK,
                        )

    print("Recording stream opened")

    frames = deque(maxlen=WINDOW_SIZE) # SHOUTOUT TO STACKOVEFLOW $$$
    clap_detected = False

    while True:
        data = stream.read(CHUNK)
        frames.extend(data)
        np_data = np.frombuffer(data, dtype=np.int16)
        max_amplitude = np.max(np_data)
        if max_amplitude > THRESHOLD:
            print("Clap detected!")
            clap_detected = True

        # Logic for saving the last few seconds of the audio clip, defined by the constants above
        if clap_detected:
            SplitRecording(frames)
            stream.stop_stream()
            stream.close()
            audio.terminate()
            break

try:
    SetMicrophone()
except Exception as error:
    print(error)
    exit()

ReceiveStream()
