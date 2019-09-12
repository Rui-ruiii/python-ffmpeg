import os
import subprocess
import re

current = os.getcwd()
dirs = os.listdir(current)

suffix = input("please enter the suffix which you need oprate:")

for i in dirs:
    if os.path.splitext(i)[1] == suffix:
        #统一名称
        os.rename(i,'example.flv')

        #打印视频信息
        log = 'ffmpeg -i example.flv >>itislog.txt 2>&1'
        printlog = subprocess.call(log,shell=True)

        #抽取视频
        with open('itislog.txt', 'r', encoding='ISO-8859-1') as f:
            for line in f:
                video_add_list1 = re.findall('Video:.+\S+', line)
                if len(video_add_list1):
                    video_add_list2 = re.findall(' \w+', video_add_list1[0])
                    video_add_list3 = re.findall('\w+', video_add_list2[0])
                    video_add = video_add_list3[0]
                    getflv_video = 'ffmpeg -i example.flv -map 0:0 -c copy video' + '.' + video_add
                    returntrans_video = subprocess.run(getflv_video, shell=True)

                else:
                    continue
        # 抽取音频
        with open('itislog.txt', 'r', encoding='ISO-8859-1') as f:
            for line in f:
                audio_add_list1 = re.findall('Audio:.+\S+', line)
                if len(audio_add_list1):
                    audio_add_list2 = re.findall(' \w+', audio_add_list1[0])
                    audio_add_list3 = re.findall('\w+', audio_add_list2[0])
                    audio_add = audio_add_list3[0]
                    getflv_audio = 'ffmpeg -i example.flv -map 0:1 -c copy audio' + '.' + audio_add
                    returntrans_audio = subprocess.run(getflv_audio, shell=True)

                else:
                    continue

                #还原源流的名称
                os.rename('example.flv', i)

                break

        print(printlog,returntrans_audio,returntrans_video)
        print("Successful Diversion!~")









