# Import the AudioSegment class for processing audio and the
# split_on_silence function for separating out silent chunks.
import os

import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

AudioSegment.converter = "D:\\ffmpeg-20190323-5252d59-win64-static\\bin\\ffmpeg.exe"
AudioSegment.ffmpeg = "D:\\ffmpeg-20190323-5252d59-win64-static\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = "D:\\ffmpeg-20190323-5252d59-win64-static\\bin\\ffmpeg.exe"

r = sr.Recognizer()


# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    # Normalize given audio chunk
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    #     sound is a pydub.AudioSegment
    #     silence_threshold in dB
    #     chunk_size in ms
    #     iterate over chunks until you find the first one with sound
    trim_ms = 0  # ms
    while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold:
        trim_ms += chunk_size

    return trim_ms


def splitAudio(file, min_silence_len=2000, indexQuestion=-1, indexAnswer=-1, maxError=0):
    audio = AudioSegment.from_mp3(file)
    # Split track where the silence is 2 seconds or more and get chunks using
    # the imported function.
    # https://github.com/jiaaro/pydub/issues/169
    chunks = split_on_silence(
        # Use the loaded audio.
        audio,
        # # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
        min_silence_len=min_silence_len,
        # Consider a chunk silent if it's quieter than -16 dBFS.
        # (You may want to adjust this parameter.)
        silence_thresh=audio.dBFS - 14
    )

    if min_silence_len >= 2000:
        if chunks.__len__() == 3:
            for i, chunk in enumerate(chunks):
                splitAudio(saveFile(chunk, "question Split %s" % i), 1000, i)
        else:
            if maxError == 5:
                print("Error")
            else:
                print("len split question = %s" % chunks.__len__())
                maxError += 1
                min_silence_len += 100
                print("maxError %s" % maxError)
                print("min_silence_len %s" % min_silence_len)
                splitAudio(file, min_silence_len, maxError=maxError)
    elif 1000 <= min_silence_len:
        if chunks.__len__() == 4:
            for i, chunk in enumerate(chunks):
                if i == 0:
                    normalized_chunk = match_target_amplitude(chunk, -20.0)
                    path = "Question %s.wav" % indexQuestion
                    normalized_chunk.export(
                        path,
                        bitrate="192k",
                        format="wav"
                    )
                    try:
                        with sr.AudioFile(path) as source:
                            path = r.record(source)
                            print('Done!')
                        text = r.recognize_google(path, show_all=True)
                        print(text)
                    except Exception as e:
                        print(e)
                    # saveFile(chunk, "Question %s" % indexQuestion)
                # else:
                #     splitAudio(saveFile(chunk, "Answer Split %s_%s" % (indexQuestion, i)), 500, indexQuestion, i)
            os.remove(file)
        else:
            if maxError == 5:
                print("Next Question")
                os.remove(file)
            else:
                print("len split answer= %s" % chunks.__len__())
                maxError += 1
                min_silence_len += 100
                print("maxError %s" % maxError)
                print("min_silence_len %s" % min_silence_len)
                splitAudio(file, min_silence_len, indexQuestion, maxError=maxError)
    else:
        name = "Answer A"
        if indexAnswer == 2:
            name = "Answer B"
        elif indexAnswer == 3:
            name = "Answer C"

        maxSize = 0
        audioFile = chunks[0]
        for index, chuck in enumerate(chunks):
            if maxSize < len(chuck):
                audioFile = chuck
                maxSize = len(chuck)

        saveFile(audioFile, "Question %s __ %s" % (indexQuestion, name))
        os.remove(file)


def saveFile(chunk, name):
    normalized_chunk = match_target_amplitude(chunk, -20.0)
    file = "%s.mp3" % name
    normalized_chunk.export(
        file,
        bitrate="192k",
        format="mp3"
    )
    return file


# Load your audio.
# splitAudio("toeic-listening-part2-0006.mp3")
# splitAudio("toeic-listening-part2-0047.mp3")
splitAudio("toeic-listening-part2-0115.mp3")
