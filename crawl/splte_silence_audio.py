# Import the AudioSegment class for processing audio and the
# split_on_silence function for separating out silent chunks.
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

AudioSegment.converter = "D:\\ffmpeg-20190323-5252d59-win64-static\\bin\\ffmpeg.exe"
AudioSegment.ffmpeg = "D:\\ffmpeg-20190323-5252d59-win64-static\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = "D:\\ffmpeg-20190323-5252d59-win64-static\\bin\\ffmpeg.exe"


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


# Load your audio.
song = AudioSegment.from_mp3("test.mp3")
# song = AudioSegment.from_mp3("toeic-listening-part2-0006.mp3")

print(song)
duration = len(song)
print(duration)
print(song.dBFS)
start_trim = detect_leading_silence(song)
print(start_trim)
# trimmed_sound = song[start_trim:duration]
# trimmed_sound.export("test.mp3", format="mp3")
# start_trim = detect_leading_silence(song)

# silence = detect_silence(song)
nonsilent = detect_nonsilent(song, min_silence_len=2000, silence_thresh=-32)
#
nonsilent = [((start / 1000), (stop / 1000)) for start, stop in nonsilent]  # convert to sec
# print(silence)
print(nonsilent)
# pass

# Split track where the silence is 2 seconds or more and get chunks using
# the imported function.
# https://github.com/jiaaro/pydub/issues/169
# chunks = split_on_silence(
#     # Use the loaded audio.
#     song,
#     # # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
#     min_silence_len=1000,
#     # Consider a chunk silent if it's quieter than -16 dBFS.
#     # (You may want to adjust this parameter.)
#     silence_thresh=-32
# )
#
# print(chunks)
#
# # Process each chunk with your parameters
# for i, chunk in enumerate(chunks):
#     # # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
#     # silence_chunk = AudioSegment.silent(duration=500)
#     #
#     # # Add the padding chunk to beginning and end of the entire chunk.
#     # audio_chunk = silence_chunk + chunk + silence_chunk
#
#     # Normalize the entire chunk.
#     normalized_chunk = match_target_amplitude(chunk, -20.0)
#
#     # Export the audio chunk with new bitrate.
#     print("Exporting chunk{0}.mp3.".format(i))
#     normalized_chunk.export(
#         ".//chunk{0}.mp3".format(i),
#         bitrate="192k",
#         format="mp3"
#     )
