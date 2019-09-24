import os
import re
import shutil

#获取ffmpeg.exe的路径
path_to_ffmpeg = input("**********Please enter the folder path of ffmpeg: ")
#path_to_ffmpeg = r"C:\Users\Julie\Desktop\ffmpeg"
#获取源流文件夹的路径
path_to_stream = input("**********Please enter the folder path of stream: ")
#path_to_stream = r"C:\Users\Julie\Desktop\H265"

#获取生成文件夹的路径
path_to_result = input("**********Please enter the folder path of result: ")
#path_to_result = r"C:\Users\Julie\Desktop\Process_Result"

#处理路径中如果带有&和空格的情况
if '&' or " " in str(path_to_stream):
    path_to_streams = path_to_stream.replace('&','_').replace(' ','_')
else:
    path_to_streams = path_to_stream
os.rename(path_to_stream,path_to_streams)

#处理流名,把文件中的流名和后缀名分开
dirs = os.listdir((path_to_streams))
list_of_streamsuffixs = []

#before是为了记录修改之前的流名，在还原流名的时候用
before = []
for i in dirs:
    before.append(i)
    #处理流名，把流名中含有空格的字符用下划线代替
    Raw_name = os.path.splitext(i)[0]
    suffix = os.path.splitext(i)[1]
    input_name = Raw_name + suffix
    if ' ' in os.path.splitext(i)[0]:
        Raw_name = os.path.splitext(i)[0].replace(' ', '_')
        input_name = Raw_name + suffix
    else:
        pass
    os.rename(path_to_streams + "\\" + i, path_to_streams + "\\" + input_name)
    list_of_streamsuffixs.append(os.path.splitext(input_name)[1])

#这里需要重新获取地址是因为需要刷新，不然流名修改的结果可能不能立即同步
dirs = os.listdir((path_to_streams))

#建立以后缀名为名的文件夹
Current = os.getcwd()
os.chdir(path_to_result)
EL = open("ErrorLog.txt",'w',encoding='utf-8')
#打印编解码表和封装解封格式列表
os.system("cd %s && ffmpeg -codecs >>codecs_list.txt 2>&1" % (path_to_ffmpeg))
os.system("cd %s && ffmpeg -formats >>formats_list.txt 2>&1" % (path_to_ffmpeg))
shutil.copy(path_to_ffmpeg + "\\" + "codecs_list.txt",path_to_result)
shutil.copy(path_to_ffmpeg + "\\" + "formats_list.txt",path_to_result)
os.remove(path_to_ffmpeg + "\\" + "codecs_list.txt")
os.remove(path_to_ffmpeg + "\\" + "formats_list.txt")
os.chdir(Current)

for suffix_name in list_of_streamsuffixs:
    if not os.path.exists(path_to_result + "\\" + suffix_name):
        os.mkdir(path_to_result + "\\" + suffix_name)
        #把streams文件夹中后缀名相同的文件放入同后缀名的文件夹
        for i in dirs:
            Raw_name = os.path.splitext(i)[0]
            if os.path.splitext(i)[1] == suffix_name:
                #以流名创建文件夹
                os.mkdir(path_to_result + "\\" + suffix_name + "\\" + os.path.splitext(i)[0])
                #把源流放到以源流名命名的文件夹
                Stream_size_Raw = os.path.getsize(path_to_streams + "\\" + i)
                shutil.copy(path_to_streams + "\\" + i,path_to_result + "\\" + suffix_name + "\\" + os.path.splitext(i)[0])
                # 进入ffmpeg.exe所在目录下,生成源流ffmpeg信息的log
                os.system("cd %s && ffmpeg -i %s >>Stream_Raw_Infolog.txt 2>&1" % (path_to_ffmpeg, path_to_streams + "\\" + i))
                shutil.copy(path_to_ffmpeg + "\\" + "Stream_Raw_Infolog.txt",path_to_result + "\\" + suffix_name + "\\" + Raw_name)

                TS_suffix = ['.tp', '.ts', '.TP', '.TS','.db']
                if os.path.splitext(i)[1] in TS_suffix:
                    print("%s 是一个 %s 文件，暂不处理" % (Raw_name, os.path.splitext(i)[1]))
                    pass
                else:
                    #Judge用来搜集信息判断源流中是否含有音/视频
                    Judge_Video = []
                    Judge_Audio = []
                    #分解视频
                    with open(path_to_ffmpeg + "\\" + "Stream_Raw_Infolog.txt",'r',encoding='ISO-8859-1') as f:
                        for line in f:
                            video_add_list1 = re.findall('Video:.+\S+', line)
                            if len(video_add_list1):
                                A = str(video_add_list1)
                                Judge_Video.append(A)
                                video_add_list2 = re.findall(' \w+', video_add_list1[0])
                                # 获取后缀名
                                video_add_list3 = re.findall('\w+', video_add_list2[0])
                                video_add = video_add_list3[0]
                                # 执行指令生成文件和文件名
                                channel_list = re.findall('\d:\d+', line)
                                channel = str(channel_list[0])
                                os.system("cd %s &&ffmpeg -i %s -map %s -c copy Stream_Video_%s.%s >>Stream_Video_Infolog.txt 2>&1" % (path_to_ffmpeg,path_to_streams + "\\" + i, channel, Raw_name, video_add))
                                shutil.copy(path_to_ffmpeg + "\\" + "Stream_Video_Infolog.txt",path_to_result + "\\" + suffix_name + "\\" + Raw_name)
                                with open(path_to_ffmpeg + "\\" + "Stream_Video_Infolog.txt",'r',encoding='ISO-8859-1') as Logcheck:
                                    for line in Logcheck:
                                        if 'NULL' in line:
                                            Now_path = os.getcwd()
                                            os.chdir(path_to_result)
                                            EL.write(Raw_name + suffix_name)
                                            EL.write(":\n")
                                            EL.write(line)
                                            os.chdir(Now_path)
                                        else:
                                            pass
                                os.remove(path_to_ffmpeg + "\\" + "Stream_Video_Infolog.txt")
                            else:
                                pass
                        if len(Judge_Video):
                            pass
                        else:
                            Now_path = os.getcwd()
                            os.chdir(path_to_result)
                            EL.write("The file %s%s have not video\n" % (Raw_name, suffix_name))
                            os.chdir(Now_path)
                    # 抽取音频
                    with open(path_to_ffmpeg + "\\" + 'Stream_Raw_Infolog.txt', 'r', encoding='ISO-8859-1') as f:
                        for line in f:
                            audio_add_list1 = re.findall('Audio:.+\S+', line)
                            if len(audio_add_list1):
                                B = str(audio_add_list1)
                                Judge_Audio.append(B)
                                audio_add_list2 = re.findall(' \w+', audio_add_list1[0])
                                # 获取后缀名
                                audio_add_list3 = re.findall('\w+', audio_add_list2[0])
                                audio_add_str = audio_add_list3[0]
                                audio_add = audio_add_str
                                # 执行指令生成文件和文件名
                                channel_list = re.findall('\d:\d+', line)
                                channel = str(channel_list[0])
                                os.system("cd %s &&ffmpeg -i %s -map %s -c copy Stream_Audio_%s.%s >>Stream_Audio_Infolog.txt 2>&1" % (path_to_ffmpeg, path_to_streams + "\\" + i, channel, Raw_name, audio_add))
                                shutil.copy(path_to_ffmpeg + "\\" + "Stream_Audio_Infolog.txt",path_to_result + "\\" + suffix_name + "\\" + Raw_name)
                                with open(path_to_ffmpeg + "\\" + "Stream_Audio_Infolog.txt",'r',encoding='ISO-8859-1') as Logcheck:
                                    for line in Logcheck:
                                        if 'NULL' in line:
                                            Now_path = os.getcwd()
                                            os.chdir(path_to_result)
                                            EL.write(Raw_name + suffix_name)
                                            EL.write(":\n")
                                            EL.write(line)
                                            os.chdir(Now_path)
                                        else:
                                            pass
                                os.remove(path_to_ffmpeg + "\\" + "Stream_Audio_Infolog.txt")
                            else:
                                pass
                        if len(Judge_Audio):
                            pass
                        else:
                            Now_path = os.getcwd()
                            os.chdir(path_to_result)
                            EL.write("The file %s%s have not audio\n" % (Raw_name, suffix_name))
                            EL.write("\n\n")
                            os.chdir(Now_path)
                    for i in os.listdir((path_to_ffmpeg)):
                        if ("Stream_Video_" + Raw_name + "." + video_add) == i:
                            Stream_size_Video = os.path.getsize(path_to_ffmpeg + "\\" + "Stream_Video_" + Raw_name + "." + video_add)
                            break
                        else:
                            Stream_size_Video = 0
                    for i in os.listdir(path_to_ffmpeg):
                        if ("Stream_Audio_" + Raw_name + "." + audio_add) == i:
                            Stream_size_Audio = os.path.getsize(path_to_ffmpeg + "\\" + "Stream_Audio_" + Raw_name + "." + audio_add)
                            break
                        else:
                            Stream_size_Audio = 0

                    #计算文件差值
                    total_size = Stream_size_Video + Stream_size_Audio
                    size_differ = Stream_size_Raw - total_size
                    if size_differ > (Stream_size_Raw / 100):
                        persentage1 = size_differ / Stream_size_Raw
                        persentage = (persentage1 * 100)
                        EL.write("%s:\n生成音视频文件大小总和与源流大小差距为%s，损失达源流大小的百分之%.2f\n\n" % (Raw_name + suffix_name, size_differ,persentage))

                os.remove(path_to_ffmpeg + "\\" + "Stream_Raw_Infolog.txt")
                # 把在ffmpeg.exe同级目录生成的流文件复制到流名文件夹

                for i in os.listdir((path_to_ffmpeg)):
                    if ("Stream_Video_" + Raw_name + "." + video_add) == i:
                        shutil.copy(path_to_ffmpeg + "\\" + "Stream_Video_" + Raw_name + "." + video_add,path_to_result + "\\" + suffix_name + "\\" + Raw_name)
                    else:
                         pass
                    if ("Stream_Audio_" + Raw_name + "." + audio_add) == i:
                        shutil.copy(path_to_ffmpeg + "\\" + "Stream_Audio_" + Raw_name + "." + audio_add,path_to_result + "\\" + suffix_name + "\\" + Raw_name)
                    else:
                        pass


#如果不close，txt文件就一直呈写入状态，close不能放进循环，一旦放进循环那么下一个内容就没有权限进行写入了
EL.close()

#删除ffmpeg文件夹内分解后的流
os.chdir(path_to_ffmpeg)
for i in os.listdir(path_to_ffmpeg):
    if i == 'ffmpeg.exe':
        pass
    else:
        os.remove(i)

#这段是用来还原流名的
a = 0
for i in dirs:
    os.rename(path_to_streams + "\\" + i,path_to_streams + "\\" + before[a])
    a += 1
os.rename(path_to_streams,path_to_stream)


print("**********Finish**********")
print("Every Folder should have 6 file(3 Audio/Video && 3 text)")
print("If the number of files is incorrect, please check ErrorLog.txt,thank you.")