from pytube import YouTube
import urllib.request
import re
import urllib.parse
import os
import sys
from pydub import AudioSegment


def mash(singer,n,y):
    delete_after_use = True
# Download N videos of X singer from Youtube (N>=10 && X is any singer) using pypi.org

    # if len(sys.argv) != 5:
    #     print("No. Of Arguments Needed = 5")
    #     exit(1)


    #taking inputs
    # singer = sys.argv[1]
    singer = singer.replace(' ','+') + "+songs"
    # outputfile = sys.argv[4]
    outputfile='out.mp3'

    try:
        # n=int(sys.argv[2])
        # y=int(sys.argv[3])
        n = int(n)
        y = int(y)
    except:
        print("You have not entered valid input, pls add the value correctly")
        exit(1)

    if n<=10:
        print("Pls enter value of #videos more than 10 for best user experience of listening to our Mashup")
        exit(1)

    if y<=20:
        print("Pls enter value of duration more than 20 for best user experience of listening to our Mashup")



    request = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(singer))
    number = re.findall(r"watch\?v=(\S{11})", request.read().decode())

    # for i in range(n):
    #     yt = YouTube("https://www.youtube.com/watch?v=" + number[i]) 
    #     stream = yt.streams.filter(only_audio=True, mime_type='audio/mp4; codecs="mp4a.40.2"').first() or \
    #              yt.streams.filter(only_audio=True).last()
    #     stream.download(filename='file-' + str(i) + '.mp3')
    #     print("File " + str(i+1) + "Download Successful")
    for i in range(n):
        try:
            yt = YouTube("https://www.youtube.com/watch?v=" + number[i]) 
            stream = yt.streams.filter(only_audio=True, mime_type='audio/mp4; codecs="mp4a.40.2"').first() or \
                    yt.streams.filter(only_audio=True).last()
            stream.download(filename='file-' + str(i) + '.mp3')
            print("File " + str(i+1) + " Download Successful")
        except Exception as e:
            print("Error in downloading file " + str(i+1) + ": " + str(e))


    from pydub import AudioSegment

    # for i in range(n):
    #     yt = YouTube("https://www.youtube.com/watch?v=" + number[i])
    #     length = yt.length
    #     if length is not None and length > 300:
    #         stream = yt.streams.filter(only_audio=True, mime_type='audio/mp4; codecs="mp4a.40.2"',
    #                                   progressive=True).first() or \
    #                  yt.streams.filter(only_audio=True).last()
    #         stream.download(filename='file-' + str(i) + '.mp3')
    #         audio = AudioSegment.from_file('file-' + str(i) + '.mp3', format='mp3')
    #         audio = audio[:300000]
    #         audio.export('file-' + str(i) + '.mp3', format='mp3')
    #     else:
    #         stream = yt.streams.filter(only_audio=True, mime_type='audio/mp4; codecs="mp4a.40.2"').first() or \
    #                  yt.streams.filter(only_audio=True).last()
    #         stream.download(filename='file-' + str(i) + '.mp3')
    #     print("File " + str(i+1) + " Download Successful")



    # print("Initiating Mashup Creation...")
    # if not os.path.exists('file-0.mp3'):
    #     print("Error: file file-0.mp3 does not exist")
    #     exit(1)
    # else:
    #     first_audio = AudioSegment.from_file('file-0.mp3')[:y*1000]

    # for i in range(1, n):
    #     filename = 'file-' + str(i) + '.mp3'
    #     if not os.path.exists(filename):
    #         print(f"Error: file {filename} does not exist")
    #         exit(1)
    #     else:
    #         audio = AudioSegment.from_file(filename)[30:y*1000]
    #         first_audio = first_audio.append(audio, crossfade=1000)


    print("Initiating Mashup Creation...")
    if not os.path.exists('file-0.mp3'):
        print("Error: file file-0.mp3 does not exist")
        exit(1)
    else:
        first_audio=AudioSegment.from_file("start.mp3")
        audio=AudioSegment.from_file('file-0.mp3')[:y*1000]
        first_audio=first_audio.append(audio,crossfade=1000)

    for i in range(1, n):
        filename = 'file-' + str(i) + '.mp3'
        if not os.path.exists(filename):
            print(f"Error: file {filename} does not exist")
            exit(1)
        else:
            audio = AudioSegment.from_file(filename)[30:y*1000]
            first_audio = first_audio.append(audio, crossfade=1000)

    try:
        first_audio.export(outputfile, format="mp3")
        print("Mashup successfully created.")
    except Exception as e:
        print("Error:", str(e))
        exit(1)

    for i in range(n):
        filename = "file-" + str(i) + ".mp3"
        try:
            os.remove(filename)
        except Exception as e:
            print("Error removing file", filename, ":", str(e))
