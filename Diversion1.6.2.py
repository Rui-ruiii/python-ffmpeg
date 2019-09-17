import os
import subprocess
import re

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
        print(printlog)
        #打印编解码表
        codecs_list = 'ffmpeg -codecs >>codecs_list.txt 2>&1'
        print_codecs_list = subprocess.call(codecs_list,shell=True)
        print(print_codecs_list)

        #抽取视频
        with open('itislog.txt', 'r', encoding='ISO-8859-1') as f:
            for line in f:
                video_add_list1 = re.findall('Video:.+\S+', line)
                if len(video_add_list1):
                    video_add_list2 = re.findall(' \w+', video_add_list1[0])
                    # 获取后缀名
                    video_add_list3 = re.findall('\w+', video_add_list2[0])
                    video_add = video_add_list3[0]
                    # 获取video信息
                    videoinfo_str1 = video_add_list1[0].replace(' ', '')
                    videoinfo_str2 = videoinfo_str1.replace(',', '')
                    videoinfo_str3 = videoinfo_str2.replace(':', '_')
                    videoinfo_str4 = videoinfo_str3.replace('/', '_')
                    # 执行指令生成文件和文件名
                    channel_list = re.findall('\d:\d+', line)
                    channel = str(channel_list[0])
                    channel_name = channel.replace(':', '_')
                    get_video = 'ffmpeg -i ' + name + ' -map ' + channel +' -c copy Channel' + channel_name +videoinfo_str4 + '.' + video_add
                    returntrans_video = subprocess.run(get_video, shell=True)
                    print(returntrans_video)

                else:
                    continue
        #抽取视频
        with open('itislog.txt', 'r', encoding='ISO-8859-1') as f:
            for line in f:
                audio_add_list1 = re.findall('Audio:.+\S+', line)
                if len(audio_add_list1):
                    audio_add_list2 = re.findall(' \w+', audio_add_list1[0])
                    # 获取后缀名
                    audio_add_list3 = re.findall('\w+', audio_add_list2[0])
                    audio_add_str = audio_add_list3[0]
                    audio_add_1 = audio_add_str.replace('_',' ')
                    audio_add_2 = re.findall('\S+',audio_add_1)
                    audio_add = audio_add_2[0]
                    # 获取audio信息
                    audioinfo_str1 = audio_add_list1[0].replace(' ', '')
                    audioinfo_str2 = audioinfo_str1.replace(',', '')
                    audioinfo_str3 = audioinfo_str2.replace(':', '_')
                    audioinfo_str4 = audioinfo_str3.replace('/', '_')
                    # 执行指令生成文件和文件名
                    channel_list = re.findall('\d:\d+', line)
                    channel = str(channel_list[0])
                    channel_name = channel.replace(':', '_')
                    get_audio = 'ffmpeg -i ' + name + ' -map ' + channel + ' -c copy Channel' + channel_name + audioinfo_str4 + '.' + audio_add
                    returntrans_audio = subprocess.run(get_audio, shell=True)
                    print(returntrans_audio)

                else:
                    continue
        # 还原源流的名称
        os.rename(name, i)

#更新同步一下文件夹的内容
current = os.getcwd()
dirs = os.listdir(current)

#删除文件大小为0的文件
for file in dirs:
    if os.path.getsize(file) == 0:
        os.remove(file)
        print(file + "is deleted")
    else:
        continue

#输出结果显示
new_suffixs = []
for i in dirs:
    new_suffixs.append(os.path.splitext(i)[1])
if "." + video_add in new_suffixs:
    print("---video file of %s has successfully generated ! ~ " % (videoinfo_str4 + '.' + video_add))
else:
    print("---%s video format file has failed to generated,cause unable to find a suitable format for it ! "% video_add)
if "." + audio_add in new_suffixs:
    print("---audio file of %s has successfully generated ! ~"% (audioinfo_str4 + '.' + audio_add))
else:
    print("---%s audio format file has failed to generated,cause unable to find a suitable format for it! "% audio_add)
if "." + video_add and "." + audio_add not in new_suffixs:
    print("---%s video format can not be decode" %suffix)


#分析error原因
with open('codecs_list.txt', 'r', encoding='ISO-8859-1') as f:
    for line in f:
        video_codec_list1 = re.findall(' \S+',line)
        if len(video_codec_list1) >= 2:
            video_codec_list2 = re.findall('\w+', video_codec_list1[1])
            if video_add in str(video_codec_list2):
               video_codec_list3 = re.findall('\w', video_codec_list1[0])
               if 'D' and 'E' in video_codec_list3:
                   break
               else:
                   print("%s can not be decode or encode" %video_add)
        else:
            continue

with open('codecs_list.txt', 'r', encoding='ISO-8859-1') as f:
    for line in f:
        audio_codec_list1 = re.findall(' \S+', line)
        if len(audio_codec_list1) >= 2:
            audio_codec_list2 = re.findall('\w+', audio_codec_list1[1])
            if audio_add in str(audio_codec_list2):
                audio_codec_list3 = re.findall('\w', audio_codec_list1[0])
                if 'D' and 'E' in audio_codec_list3:
                    break
                else:
                    print("%s can not be decode or encode" % audio_add)
        else:
            continue


