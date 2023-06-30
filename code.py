# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import random
import audiocore
import board
import audiobusio
import audiomixer
import time

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

audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)

mixer = audiomixer.Mixer(voice_count=1, sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
audio.play(mixer) # attach mixer to audio playback

mixer.voice[0].level = 0.2

tt = TTAstromech()
while(True):
    x = tt.getnrandom(8)
    tt.play(x)
    time.sleep(2)



