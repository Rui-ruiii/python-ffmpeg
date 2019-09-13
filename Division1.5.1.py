import os
import subprocess
import re
import winpexpect


current = os.getcwd()
dirs = os.listdir(current)

suffix = input("please enter the suffix which you need oprate:")

for i in dirs:
    if os.path.splitext(i)[1] == suffix:
        #统一名称
        name = 'example'+ suffix
        os.rename(i,name)

        #打印视频信息
        itislog = 'ffmpeg -i ' + name +' >>itislog.txt 2>&1'
        printlog = subprocess.call(itislog,shell=True)

        #抽取视频
        with open('itislog.txt', 'r', encoding='ISO-8859-1') as f:
            for line in f:
                video_add_list1 = re.findall('Video:.+\S+', line)
                if len(video_add_list1):
                    video_add_list2 = re.findall(' \w+', video_add_list1[0])
                    #获取后缀名
                    video_add_list3 = re.findall('\w+', video_add_list2[0])
                    video_add = video_add_list3[0]
                    #获取video信息
                    videoinfo_str1 = video_add_list1[0].replace(' ','')
                    videoinfo_str2 = videoinfo_str1.replace(',','')
                    videoinfo_str3 = videoinfo_str2.replace(':','_')
                    videoinfo_str4 = videoinfo_str3.replace('/','_')
                    #执行指令生成文件和文件名
                    get_video = 'ffmpeg -i '+ name +' -map 0:0 -c copy ' + videoinfo_str4 + '.' + video_add
                    returntrans_video = subprocess.run(get_video, shell=True)

                    #异常处理
                    process = subprocess.check_output(get_video, shell=False)
                    out_process = process.decode()
                    if out_process.find("Unable to find suitable format"):
                        print("ffmpeg can handle the format of %s" % video_add)
                    else:
                        print("can not find the reason of error")


                else:
                    continue
        # 抽取音频
        with open('itislog.txt', 'r', encoding='ISO-8859-1') as f:
            for line in f:
                audio_add_list1 = re.findall('Audio:.+\S+', line)
                if len(audio_add_list1):
                    audio_add_list2 = re.findall(' \w+', audio_add_list1[0])
                    #获取后缀名
                    audio_add_list3 = re.findall('\w+', audio_add_list2[0])
                    audio_add = audio_add_list3[0]
                    #获取audio信息
                    audioinfo_str1 = audio_add_list1[0].replace(' ', '')
                    audioinfo_str2 = audioinfo_str1.replace(',', '_')
                    audioinfo_str3 = audioinfo_str2.replace(':','_')
                    audioinfo_str4 = audioinfo_str3.replace('/','_')
                    # 执行指令生成文件和文件名
                    get_audio = 'ffmpeg -i '+ name +' -map 0:1 -c copy ' + audioinfo_str4 + '.' + audio_add
                    returntrans_audio = subprocess.run(get_audio, shell=True)

                    #异常处理

                    process = subprocess.check_output(get_audio,shell=False)
                    out_process = process.decode()
                    if out_process.find("Unable to find suitable format"):
                        print("ffmpeg can handle the format of %s" % audio_add)
                    else:
                        print("can not find the reason of error")



                else:
                    continue

                #还原源流的名称
                os.rename(name, i)

                break



        print(printlog,returntrans_audio,returntrans_video)


