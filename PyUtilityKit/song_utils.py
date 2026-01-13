from pydub import AudioSegment
from moviepy.editor import *
import os
from natsort import natsorted
  

def mp3_cut(): # ⚠️ Revisar código

	# Open an mp3 file
	song = AudioSegment.from_file("/home/eduardo/Desktop/tomp3.cc - The Sound of Inner Peace 5  Relaxing Music for Meditation Zen Yoga  Stress Relief.mp3", format="mp3")
	  
	inicio = 0 * 60 * 1000
	fim = 15 * 60 * 1000

	fracao = song[ inicio : fim ]
	  
	# save file
	# Cada minuto consome em média 1 MB

	fracao.export("fracao.mp3", format="mp3")
	print("New Audio file is created and saved")