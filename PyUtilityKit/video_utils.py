
from moviepy.editor import *



def mp4_to_mp3(mp4, mp3):

	filetoconvert = AudioFileClip(mp4)
	filetoconvert.write_audiofile(mp3)
	filetoconvert.close()



def mp4_to_wav(mp4, wav):

	# For best results, the audio source should be captured and transmitted using a lossless encoding (FLAC or LINEAR16).
	# The accuracy of the speech recognition can be reduced if lossy codecs are used to capture or transmit audio, particularly 
	# if background noise is present. Lossy codecs include MULAW, AMR, AMR_WB, OGG_OPUS, SPEEX_WITH_HEADER_BYTE, MP3, and WEBM_OPUS.
	#
	# https://cloud.google.com/speech-to-text/docs/reference/rest/v1/RecognitionConfig

	filetoconvert = AudioFileClip(mp4)
	filetoconvert.write_audiofile(wav)
	filetoconvert.close()





def mp4_merge(): # ⚠️ Revisar código
	L =[]

	for root, dirs, files in os.walk("C:\\Users\\7490\\Desktop\\vid"):

	    #files.sort()
	    files = natsorted(files)
	    for file in files:
	        if os.path.splitext(file)[1] == '.mp4':
	            filePath = os.path.join(root, file)
	            video = VideoFileClip(filePath)
	            L.append(video)

	final_clip = concatenate_videoclips(L)
	final_clip.to_videofile("output2.mp4", fps=24, remove_temp=False)