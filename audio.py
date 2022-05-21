from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
import sys
class Audio(object):

        def __init__(self):

            self.effect = QSoundEffect()
            self.sound_file = 'zap_2.wav'
            self.effect.setSource(QUrl.fromLocalFile(self.sound_file))
            # effect.setLoopCount(QSoundEffect.Infinite)
            self.effect.setVolume(0.25);


        def play_sound(self):

            self.effect.play()
