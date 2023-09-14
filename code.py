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
config_sound_mode = 0

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

PLAY_Q_EVERY_SEC = [5, 10]

PLAY_ABC_EVERY_SEC = [5, 10]

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
            self.last_played = time.monotonic()

        if time.monotonic() - self.last_played > random.uniform(*PLAY_Q_EVERY_SEC):
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
                self.last_played = time.monotonic()
                return

            # Reason 3: Currently waiting.
            else:
                pass

        if not self.playing_word and (time.monotonic() - self.last_played > random.uniform(*PLAY_ABC_EVERY_SEC)):
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

pixels.fill((0, 0, 0))

last_update = time.monotonic()

q_sounds = PlayQ()
abc_sounds = TTAstromech()

#
#   3 2 1
#     0
#   4 5 6
#

class Blinky:
    def __init__(self):
        self.last_state_change = 0
        self.last_blink = 0
        self.step = 0
        self.state = 0
        self.from_color = (255,0,0)
        self.to_color = (0,0,255)

        self.col_disp_a = (128,0, 128)
        self.col_disp_b = (128,128,0)

    def update(self):
        global pixels

        new_state = self.state
        if self.state == 0:
            wait_time = random.uniform(3, 8)
            if time.monotonic() - self.last_state_change >= wait_time:
                new_state = 1
        elif self.state > 0:
            trans_time = random.uniform(0.02, 0.05)
            if time.monotonic() - self.last_state_change >= trans_time:
                new_state = self.state + 1
                if new_state > 3:
                    new_state = 0

        need_update = False

        blink_time = random.uniform(5, 20)
        if time.monotonic() - self.last_blink >= blink_time:
            self.col_disp_a, self.col_disp_b = self.col_disp_b, self.col_disp_a
            pixels[7] = self.col_disp_a
            pixels[8] = self.col_disp_b
            self.last_blink = time.monotonic()
            need_update = True

        if new_state != self.state:
            self.state = new_state
            self.last_state_change = time.monotonic()
            need_update = True

            if self.state == 0:
                for i in range(7):
                    pixels[i] = self.from_color

            elif self.state == 1:
                pixels[1] = self.to_color
                pixels[2] = self.to_color
                pixels[3] = self.to_color

                pixels[0] = self.from_color

                pixels[4] = self.from_color
                pixels[5] = self.from_color
                pixels[6] = self.from_color

            elif self.state == 2:
                pixels[1] = self.to_color
                pixels[2] = self.to_color
                pixels[3] = self.to_color

                pixels[0] = self.to_color

                pixels[4] = self.from_color
                pixels[5] = self.from_color
                pixels[6] = self.from_color

            elif self.state == 3:
                pixels[1] = self.to_color
                pixels[2] = self.to_color
                pixels[3] = self.to_color

                pixels[0] = self.to_color

                pixels[4] = self.to_color
                pixels[5] = self.to_color
                pixels[6] = self.to_color

                self.from_color, self.to_color = self.to_color, self.from_color

        if need_update:
            pixels.show()

blinky = Blinky()

while(True):
    button.update()
    if button.fell:
        if config_sound_mode == 0:
            config_sound_mode = 1
            config_play_audio = True
        elif config_sound_mode == 1:
            config_sound_mode = 2
            config_play_audio = True
        else:
            config_sound_mode = 0
            config_play_audio = False

        print("audio", config_play_audio, "mode", config_sound_mode)
    elif button.rose:
        pass
    #time.sleep(0.01)

    if config_sound_mode == 1:
        q_sounds.update()
    elif config_sound_mode == 2:
        abc_sounds.update()

    blinky.update()
    time.sleep(0.002)




