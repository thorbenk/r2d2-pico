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
import audiomp3

config_play_audio = False

Q_SOUNDS = [
    "QSCANING.mp3",
    "QSNTNC10.mp3",
    "QSNTNC13.mp3",
    "QSNTNC16.mp3",
    "QSNTNC18.mp3",
    "QSNTNC20.mp3",
    "QSNTNC4.mp3",
    "QWORD16.mp3",
    "QWORD1.mp3",
    "QWORD22.mp3",
    "QWORD4.mp3",
    "QWORD8.mp3",
    "QWORD9.mp3"
]

PLAY_Q_EVERY_SEC = 5

PLAY_ABC_EVERY_SEC = 5

class PlayQ:
    def __init__(self):
        self.last_played = 0
        self.playing = False

    def update(self):
        global config_play_audio

        if not config_play_audio:
            return

        if mixer.voice[0].playing:
            return
        elif self.playing:
            self.playing = False
            self.last_played = time.time()

        if time.time() - self.last_played > PLAY_Q_EVERY_SEC:
            self.playing = True
            r = random.randint(0, len(Q_SOUNDS)-1)
            rnd_sound = Q_SOUNDS[r]
            print(rnd_sound)
            f = open(rnd_sound, "rb")
            snd = audiomp3.MP3Decoder(f)
            #audio.play(wav)
            mixer.voice[0].play(snd)



def play_character(char):
    wave_file = open(char + ".mp3", "rb")
    wav = audiomp3.MP3Decoder(wave_file)
    #audio.play(wav)
    mixer.voice[0].play(wav)
    #while audio.playing:
    #while mixer.voice[0].playing:
    #    pass

class TTAstromech(object):
    def __init__(self):
        self.letters = [
            "a", "b", "c", "c1", "d", "e", "f", "g", "g1", "h", "i", "j", "k",
            "l", "m", "n", "o", "o1", "p", "q", "r", "s", "s1", "t", "u", "u1",
            "v", "w", "x", "y", "z"
        ]
        self.playing_word = False
        self.last_played = 0

        self.current_word = None
        self.current_char = 0

    def update(self):
        global config_play_audio

        if not config_play_audio:
            return

        if mixer.voice[0].playing:
            return
        else:
            # currently not playing

            # Reason 1: Stopped in the middle of speaking a word. Speak next letter
            if self.playing_word and self.current_char < len(self.current_word) - 1:
                # still some letters to go
                self.current_char += 1

            # Reason 2: Stopped at the end of the word
            elif self.playing_word:
                # done with this word
                self.playing_word = False
                self.current_char = 0
                self.current_word = None
                self.last_played = time.time()
                return

            # Reason 3: Currently waiting.
            else:
                pass

        if not self.playing_word and (time.time() - self.last_played > PLAY_ABC_EVERY_SEC):
            self.playing_word = True
            self.current_char = 0
            self.current_word = self.getnrandom()

        if self.playing_word:
            play_character(self.current_word[self.current_char])

    def getnrandom(self, n=6):
        s = []
        for i in range(n):
            i = random.randint(0, len(self.letters)-1)
            s.append(self.letters[i])
        return s

button_pin = digitalio.DigitalInOut(board.GP22)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP

button = Debouncer(button_pin)

audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)

mixer = audiomixer.Mixer(voice_count=1, sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
audio.play(mixer) # attach mixer to audio playback

mixer.voice[0].level = 0.8


# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 9
pixels = neopixel.NeoPixel(board.GP10, num_pixels, pixel_order=neopixel.GRB)
pixels.brightness = 0.5

tt = TTAstromech()
pixels.fill((255, 0, 0))
i = 0

last_update = time.time()

#q_sounds = PlayQ()
abc_sounds = TTAstromech()

while(True):
    button.update()
    if button.fell:
        print("button pressed")
        config_play_audio = not config_play_audio
        print("audio", config_play_audio)
    elif button.rose:
        print("button released")
    #time.sleep(0.01)

    #q_sounds.update()
    abc_sounds.update()

    if time.time() - last_update < 2:
        continue
    else:
        # x = tt.getnrandom(8)
        #if config_play_audio:
        #    tt.play(x)
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
    if i >= 2:
        i = 0





