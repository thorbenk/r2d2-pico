# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import random
import audiocore
import board
import audiobusio
import audiomixer
import time
import neopixel
from adafruit_debouncer import Debouncer
import digitalio

config_play_audio = False

def play_character(char):
    wave_file = open(char + ".wav", "rb")
    wav = audiocore.WaveFile(wave_file)
    #audio.play(wav)
    mixer.voice[0].play(wav)
    #while audio.playing:
    while mixer.voice[0].playing:
        pass

class TTAstromech(object):
    def __init__(self):
        self.letters = [
            "a", "b", "c", "c1", "d", "e", "f", "g", "g1", "h", "i", "j", "k",
            "l", "m", "n", "o", "o1", "p", "q", "r", "s", "s1", "t", "u", "u1",
            "v", "w", "x", "y", "z"
        ]

    def play(self, word):
        data = b""

        for letter in word:
            letter = letter.lower()  # need this?
            if not letter.isalpha():
                continue

            play_character(letter)
        return data

    def run(self):
        while True:
            word = self.getnrandom()
            self.speak(word)

    def getnrandom(self, n=6):
        s = ""
        for i in range(n):
            i = random.randint(0, len(self.letters)-1)
            s += self.letters[i]
        return s

button_pin = digitalio.DigitalInOut(board.GP22)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP

button = Debouncer(button_pin)

audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)

mixer = audiomixer.Mixer(voice_count=1, sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
audio.play(mixer) # attach mixer to audio playback

mixer.voice[0].level = 0.2


# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 9
pixels = neopixel.NeoPixel(board.GP10, num_pixels, pixel_order=neopixel.GRB)
pixels.brightness = 0.5

tt = TTAstromech()
pixels.fill((255, 0, 0))
i = 0

last_update = time.time()

while(True):
    button.update()
    if button.fell:
        print("button pressed")
        config_play_audio = not config_play_audio
        print("audio", config_play_audio)
    elif button.rose:
        print("button released")
    time.sleep(0.01)
    if time.time() - last_update < 2:
        continue
    else:
        x = tt.getnrandom(8)
        if config_play_audio:
            tt.play(x)
        if i % 2 == 0:
            for j in range(7):
                pixels[j] = (0, 0, 255)
            pixels[7] = (0,128,128)
            pixels[8] = (128,128,0)
        else:
            for j in range(7):
                pixels[j] = (255, 0, 0)
            pixels[8] = (0,128,128)
            pixels[7] = (128,128,0)
        last_update = time.time()
    # time.sleep(2)
    i += 1




