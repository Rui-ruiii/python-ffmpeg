import os
import re
import shutil

#获取ffmpeg.exe的路径
path_to_ffmpeg = r"C:\Users\Julie\Desktop\ffmpeg"
#获取源流文件夹的路径
#path_to_streams = input("**********Please enter the folder path of stream: ")
path_to_streams = r"C:\Users\Julie\Desktop\streams"
#获取生成文件夹的路径
path_to_resule = r"C:\Users\Julie\Desktop\Process_Result"



#处理流名,把文件中的流名和后缀名分开
dirs = os.listdir((path_to_streams))
list_of_stream = []
list_of_streamname = []
list_of_streamsuffixs = []

for i in dirs:
    # 处理流名，把流名中含有空格的字符用下划线代替
    Raw_name = os.path.splitext(i)[0]
    suffix = os.path.splitext(i)[1]
    input_name = Raw_name + suffix
    if ' ' in os.path.splitext(i)[0]:
        Raw_name = os.path.splitext(i)[0].replace(' ', '_')
        input_name = Raw_name + suffix

    else:
        pass

    os.rename(path_to_streams + "\\" + i, path_to_streams + "\\" + input_name)
    list_of_stream.append(os.path.basename(input_name))
    list_of_streamname.append(os.path.splitext(input_name)[0])
    list_of_streamsuffixs.append(os.path.splitext(input_name)[1])
print(list_of_stream)
print(list_of_streamname)
print(list_of_streamsuffixs)

#建立以后缀名为名的文件夹
for suffix_name in list_of_streamsuffixs:
    if not os.path.exists(path_to_resule + "\\" + suffix_name):
        os.mkdir(path_to_resule + "\\" + suffix_name)
        #把streams文件夹中后缀名相同的文件放入同后缀名的文件夹
        for i in dirs:
            Raw_name = os.path.splitext(i)[0]
            if os.path.splitext(i)[1] == suffix_name:
                #以流名创建文件夹
                os.mkdir(path_to_resule + "\\" + suffix_name + "\\" + os.path.splitext(i)[0])
                #把源流放到以源流名命名的文件夹
                shutil.copy(path_to_streams + "\\" + i,path_to_resule + "\\" + suffix_name + "\\" + os.path.splitext(i)[0])
                # 进入ffmpeg.exe所在目录下,生成源流ffmpeg信息的log
                os.system("cd %s && ffmpeg -i %s >>Stream_Raw_Infolog.txt 2>&1" % (path_to_ffmpeg, path_to_streams + "\\" + i))
                shutil.copy(path_to_ffmpeg + "\\" + "Stream_Raw_Infolog.txt",path_to_resule + "\\" + suffix_name + "\\" + Raw_name)
                #os.remove(path_to_ffmpeg + "\\" + "Stream_Raw_Infolog.txt")
                #打印编解码表
                os.system("cd %s && ffmpeg -codecs >>codecs_list.txt 2>&1" % (path_to_ffmpeg))
                shutil.copy(path_to_ffmpeg + "\\" + "codecs_list.txt",path_to_resule + "\\" + suffix_name + "\\" + Raw_name)
                os.remove(path_to_ffmpeg + "\\" + "codecs_list.txt")
                #分解视频
                with open(path_to_ffmpeg + "\\" + "Stream_Raw_Infolog.txt",'r',encoding='ISO-8859-1') as f:
                    for line in f:
                        video_add_list1 = re.findall('Video:.+\S+', line)
                        if len(video_add_list1):
                            video_add_list2 = re.findall(' \w+', video_add_list1[0])
                            # 获取后缀名
                            video_add_list3 = re.findall('\w+', video_add_list2[0])
                            video_add = video_add_list3[0]
                            # 获取video信息
                            #videoinfo_str1 = video_add_list1[0].replace(' ', '')
                            #videoinfo_str2 = videoinfo_str1.replace(',', '')
                            #videoinfo_str3 = videoinfo_str2.replace(':', '_')
                            #videoinfo_str4 = videoinfo_str3.replace('/', '_')
                            # 执行指令生成文件和文件名
                            channel_list = re.findall('\d:\d+', line)
                            channel = str(channel_list[0])
                            #channel_name = channel.replace(':', '_')
                            os.system("cd %s &&ffmpeg -i %s -map %s -c copy Stream_Video_%s.%s >>Stream_Video_Infolog.txt 2>&1" % (path_to_ffmpeg,path_to_streams + "\\" + i, channel, Raw_name, video_add))
                            shutil.copy(path_to_ffmpeg + "\\" + "Stream_Video_Infolog.txt",path_to_resule + "\\" + suffix_name + "\\" + Raw_name)
                            os.remove(path_to_ffmpeg + "\\" + "Stream_Video_Infolog.txt")
                        else:
                            pass
                # 抽取音频
                with open(path_to_ffmpeg + "\\" + 'Stream_Raw_Infolog.txt', 'r', encoding='ISO-8859-1') as f:
                    for line in f:
                        audio_add_list1 = re.findall('Audio:.+\S+', line)
                        if len(audio_add_list1):
                            audio_add_list2 = re.findall(' \w+', audio_add_list1[0])
                            # 获取后缀名
                            audio_add_list3 = re.findall('\w+', audio_add_list2[0])
                            audio_add_str = audio_add_list3[0]
                            #audio_add_1 = audio_add_str.replace('_', ' ')
                            #audio_add_2 = re.findall('\S+', audio_add_1)
                            #audio_add = audio_add_2[0]
                            audio_add = audio_add_str
                            # 获取audio信息
                            #audioinfo_str1 = audio_add_list1[0].replace(' ', '')
                            #audioinfo_str2 = audioinfo_str1.replace(',', '')
                            #audioinfo_str3 = audioinfo_str2.replace(':', '_')
                            #audioinfo_str4 = audioinfo_str3.replace('/', '_')
                            # 执行指令生成文件和文件名
                            channel_list = re.findall('\d:\d+', line)
                            channel = str(channel_list[0])
                            #channel_name = channel.replace(':', '_')
                            os.system("cd %s &&ffmpeg -i %s -map %s -c copy Stream_Audio_%s.%s >>Stream_Audio_Infolog.txt 2>&1" % (path_to_ffmpeg, path_to_streams + "\\" + i, channel, Raw_name, audio_add))
                            shutil.copy(path_to_ffmpeg + "\\" + "Stream_Audio_Infolog.txt",path_to_resule + "\\" + suffix_name + "\\" + Raw_name)
                            os.remove(path_to_ffmpeg + "\\" + "Stream_Audio_Infolog.txt")
                        else:
                            pass
                os.remove(path_to_ffmpeg + "\\" + "Stream_Raw_Infolog.txt")
                # 把在ffmpeg.exe同级目录生成的流文件复制到流名文件夹
                #流文件
                for i in os.listdir((path_to_ffmpeg)):
                    if  ("Stream_Video_" + Raw_name + "." + video_add) == i:
                        shutil.copy(path_to_ffmpeg + "\\" + "Stream_Video_" + Raw_name + "." + video_add,path_to_resule + "\\" + suffix_name + "\\" + Raw_name)
                    else:
                        pass
                    if ("Stream_Audio_" + Raw_name + "." + audio_add) == i:
                        shutil.copy(path_to_ffmpeg + "\\" + "Stream_Audio_" + Raw_name + "." + audio_add,path_to_resule + "\\" + suffix_name + "\\" + Raw_name)
                    else:
                        pass



