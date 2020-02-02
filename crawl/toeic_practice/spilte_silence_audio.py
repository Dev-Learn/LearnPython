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


class SplitAudio:

    @staticmethod
    def splitAudioCrawl(indexQuestion, filePath, min_silence_len=2000, indexTempQuestion=-1, indexAnswer=-1, maxError=0,
                        isHasQuestion=True):
        splitAudio(indexQuestion, filePath, min_silence_len, indexTempQuestion, indexAnswer, maxError,
                   isHasQuestion)


def splitAudio(indexQuestion, filePath, min_silence_len=2000, indexTempQuestion=-1, indexAnswer=-1, maxError=0,
               isHasQuestion=True):
    chunks = split(filePath, min_silence_len)
    if min_silence_len >= 2000:
        if chunks.__len__() == 3:
            for i, chunk in enumerate(chunks):
                splitAudio(indexQuestion + i, saveFile(chunk, "question Split %s" % i), 1000, i)
        else:
            print("len split Question= %s" % chunks.__len__())
            retry(indexQuestion, filePath, min_silence_len, indexTempQuestion, indexAnswer, maxError)
    elif 1000 <= min_silence_len:
        if chunks.__len__() == 4:
            for i, chunk in enumerate(chunks):
                if isHasQuestion:
                    if i == 0:
                        if validAudio(chunk, indexTempQuestion, ""):
                            saveFile(chunk, "Question %s" % indexQuestion)
                        else:
                            print("Not Valid Audio")
                    else:
                        splitAudio(indexQuestion, saveFile(chunk, "Answer Split %s_%s" % (indexTempQuestion, i)), 500,
                                   indexTempQuestion, i)
                else:
                    splitAudio(indexQuestion, saveFile(chunk, "Answer Split %s_%s" % (indexTempQuestion, i)), 150,
                               indexTempQuestion, i, isHasQuestion=isHasQuestion)
            os.remove(filePath)
        else:
            print("len split Answer = %s" % chunks.__len__())
            retry(indexQuestion, filePath, min_silence_len, indexTempQuestion, indexAnswer, maxError, isHasQuestion)
    else:
        print(" Split Answer Child %s" % chunks.__len__())
        print(" indexAnswer %s" % indexAnswer)
        name = "Answer A"
        if isHasQuestion:
            if indexAnswer == 2:
                name = "Answer B"
            elif indexAnswer == 3:
                name = "Answer C"
        else:
            if indexAnswer == 1:
                name = "Answer B"
            elif indexAnswer == 2:
                name = "Answer C"
            elif indexAnswer == 3:
                name = "Answer D"

        if chunks.__len__() == 1:
            retry(indexQuestion, filePath, min_silence_len, indexTempQuestion, indexAnswer, maxError, isHasQuestion,
                  True)
        else:
            maxSize = 0
            audioFile = chunks[0]
            for index, chuck in enumerate(chunks):
                if maxSize < len(chuck):
                    audioFile = chuck
                    maxSize = len(chuck)

            saveFile(audioFile, "Question %s __ %s" % (indexQuestion, name))
            os.remove(filePath)


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


def validAudio(chunk, indexQuestion, text):
    print("validAudio")
    isValid = False
    dir = 'audios'
    # if not os.path.isdir(dir):
    #     os.mkdir(dir)
    pathFile = dir + "/Question %s.wav" % indexQuestion
    # pathFile = "/Question %s.wav" % indexQuestion
    normalized_chunk = match_target_amplitude(chunk, -20.0)

    normalized_chunk.export(
        pathFile,
        bitrate="192k",
        format="wav"
    )
    try:
        with sr.AudioFile(pathFile) as source:
            audio = r.record(source)
        textRecognize = r.recognize_google(audio, show_all=True)
        textRecognize = textRecognize['alternative']
        if textRecognize.__len__() > 0:
            textRecognize = textRecognize[0]['transcript']
            print(textRecognize)
            isValid = True
    except Exception as e:
        print(e)
    os.remove(pathFile)
    return isValid


def retry(indexQuestion, filePath, min_silence_len, indexTempQuestion, indexAnswer, maxError, isHasQuestion=True,
          isAnswer=False):
    if maxError == 7:
        # print("Error")
        if isHasQuestion or isAnswer:
            os.remove(filePath)
    else:
        maxError += 1
        if isAnswer and not isHasQuestion:
            min_silence_len -= 10
        elif isAnswer and isHasQuestion:
            min_silence_len -= 50
        else:
            min_silence_len += 100
        # print("maxError %s" % maxError)
        # print("min_silence_len %s" % min_silence_len)
        splitAudio(indexQuestion, filePath, min_silence_len, indexTempQuestion, indexAnswer, maxError, isHasQuestion)


def split(filePath, min_silence_len):
    audio = AudioSegment.from_mp3(filePath)
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
    return chunks


def saveFile(chunk, name):
    dir = 'audios'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    file = dir + "/%s.mp3" % name
    # file = "%s.mp3" % name
    normalized_chunk = match_target_amplitude(chunk, -20.0)
    normalized_chunk.export(
        file,
        bitrate="192k",
        format="mp3"
    )
    print(file)
    return file


# Load your audio.
# splitAudio("toeic-listening-part2-0006.mp3")
# SplitAudio.splitAudioCrawl(1, "toeic-listening-part2-0047.mp3")
# SplitAudio.splitAudioCrawl(1, "toeic-part1-85-1.mp3", 1000, isHasQuestion=False)
