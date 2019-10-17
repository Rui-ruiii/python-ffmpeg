import os
import re
import shutil
import psutil
import time


#获取ffmpeg.exe的路径
path_to_ffmpeg = (os.getcwd() + "\\" + "ffmpeg")

#获取源流文件夹的路径
path_to_stream = []
path_to_stream.append(os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir)))

#获取当前路径的盘符
pan_code = path_to_stream[0].split(':')[0]
pan_ffmpeg = path_to_ffmpeg.split(':')[0]

# 获取本机磁盘使用率和剩余空间G信息
# 循环磁盘分区
disk_size_free = []
disk_device_name = []
for disk in psutil.disk_partitions():
    # 读写方式 光盘 or 有效磁盘类型
    if 'cdrom' in disk.opts or disk.fstype == '':
        continue
    disk_device_name.append(disk.device)
    disk_info = psutil.disk_usage(disk.device)
    # 磁盘剩余空间
    free_disk_size = disk_info.free
    disk_size_free.append(free_disk_size)
    # 当前磁盘使用率和剩余空间G信息

dic = dict(zip(disk_device_name,disk_size_free))
os.chdir(max(dic))
os.mkdir(max(dic) + '\\' + 'ResultOfProcess')
path_to_result = max(dic) + '\\' + 'ResultOfProcess'
#生成全部的文件列表
os.chdir(path_to_result)
FL = open('FileLists.txt','w',encoding='utf-8')

file_size = []
for dirname,subdirList,fileList in os.walk(path_to_stream[0]):
    for fname in fileList:
        need = dirname + "\\" + fname
        file_size.append(os.path.getsize(need))
        FL.write(need + "\n")


if sum(file_size) * 2 > max(disk_size_free):
    print("Expected more disk free space")
    time.sleep(5)
    print("The Process will exit after 10s")
    time.sleep(10)
else:
    print("totol filelist was in %s" % max(dic))
    SFL = open('StreamsFileLists.txt', 'w', encoding='utf-8')
FL.close()

os.chdir(path_to_stream[0])

#筛选流文件生成新的流文件列表
total_invaluble_suffix = ['.py','.dll','.pyd','.pyc','.rst','.css','','.txt','.ts',',trp','.exe','.xlsx','.db','.log','.ini','.rar','.js','.zip','.bat','xls','html','.doc','.docx','adif','.jpg','.png']

fname_list = []
new_fname_list =[]
stream_name_list = []
new_stream_name_list = []
suffix = []

for dirname,subdirList,fileList in os.walk(path_to_stream[0]):
    for fname in fileList:
        # 修改路径中的非法字符
        if os.path.splitext(fname)[1].lower() not in total_invaluble_suffix:
            fname_list.append(dirname)
            stream_name_list.append(fname)
            SFL.write(dirname + "\\" + fname + "\n")
            suffix.append(os.path.splitext(fname)[1])
no_repeat_fname_list = list(set(fname_list))
no_repeat_suffix = list(set(suffix))

#改路径名列表
for unin in no_repeat_fname_list:
    if '&' in unin:
        unin = unin.replace('&', '_')
    if ' ' in unin:
        unin = unin.replace(' ', '_')
    else:
        pass
    new_fname_list.append(unin)
print(new_fname_list)

#改流名列表
for name in stream_name_list:
    if '&' in name:
        name = name.replace('&','_')
    if ' ' in name:
        name = name.replace(' ','_')
    else:
        pass
    new_stream_name_list.append(name)

#改流名
os.getcwd()
error_stream_name_list_len = len(stream_name_list)
j = 0
for dirname,subdirList,fileList in os.walk(path_to_stream[0]):
    for fname in fileList:
        if os.path.splitext(fname)[1].lower() not in total_invaluble_suffix:
            if j < error_stream_name_list_len:
                os.rename(dirname + '\\' + stream_name_list[j],dirname + '\\' + new_stream_name_list[j])
                j += 1
time.sleep(2)

# 改名
list_len = len(no_repeat_fname_list)
print(list_len)
print(no_repeat_fname_list)
i = 0
while i < len(no_repeat_fname_list):
    print(no_repeat_fname_list[i])
    print(new_fname_list[i])
    if os.path.exists(new_fname_list[i]):
        pass
    else:
        os.renames(no_repeat_fname_list[i], new_fname_list[i])
    i += 1
    print(i)
time.sleep(2)
print("change path finish")
#for dirname,subdirList,fileList in os.walk(path_to_stream[0]):
 #   for fname in fileList:
  #      print(dirname + fname)


os.chdir(path_to_result)
EL = open("ErrorLog.txt",'w',encoding='utf-8')
#打印编解码表和封装解封格式列表
os.chdir(path_to_ffmpeg)
os.system("cd %s &&cd %s &&ffmpeg -codecs >>codecs_list.txt 2>&1" % (pan_ffmpeg + ':',path_to_ffmpeg))
os.system("cd %s &&cd %s &&ffmpeg -formats >>formats_list.txt 2>&1" % (pan_ffmpeg + ':',path_to_ffmpeg))
shutil.copy(path_to_ffmpeg + "\\" + "codecs_list.txt",path_to_result)
shutil.copy(path_to_ffmpeg + "\\" + "formats_list.txt",path_to_result)
os.remove(path_to_ffmpeg + "\\" + "codecs_list.txt")
os.remove(path_to_ffmpeg + "\\" + "formats_list.txt")
os.chdir(path_to_stream[0])

time.sleep(2)
#创建以后缀名为目录名的文件夹
for dirname,subdirList,fileList in os.walk(path_to_stream[0]):
    for fname in fileList:
        #防止ffmpeg对生成的音视频文件再次分析
        #if 'Stream_Video_' or 'Stream_Audio_' in str(fname):
        suffix_name = os.path.splitext(fname)[1].lower()
        Raw_name = os.path.splitext(fname)[0]
        if suffix_name not in total_invaluble_suffix:
            if not os.path.exists(path_to_result + "\\" + suffix_name):
                    os.mkdir(path_to_result + "\\" + suffix_name)
            os.chdir(path_to_result + "\\" + suffix_name)
            os.mkdir(path_to_result + "\\" + suffix_name + '\\' + Raw_name)
            Stream_size_Raw = os.path.getsize(dirname + "\\" + fname)
            shutil.copy(dirname + "\\" + fname,path_to_result + "\\" + suffix_name + "\\" + Raw_name)
            # 进入ffmpeg.exe所在目录下,生成源流ffmpeg信息的log
            os.chdir(path_to_ffmpeg)
            os.system("cd %s &&ffmpeg -i %s >>Stream_Raw_Infolog.txt 2>&1" % (path_to_ffmpeg, dirname + "\\" + fname))
            shutil.copy(path_to_ffmpeg + "\\" + "Stream_Raw_Infolog.txt",path_to_result + "\\" + suffix_name + "\\" + Raw_name)
            # Judge用来搜集信息判断源流中是否含有音/视频
            Judge_Video = []
            Judge_Audio = []
            time.sleep(2)
            # 分解视频
            with open(path_to_ffmpeg + "\\" + "Stream_Raw_Infolog.txt", 'r', encoding='ISO-8859-1') as f:
                for line in f:
                    video_add_list1 = re.findall('Video:.+\S+', line)
                    if len(video_add_list1):
                        A = str(video_add_list1)
                        Judge_Video.append(A)
                        video_add_list2 = re.findall(' \w+', video_add_list1[0])
                        # 获取后缀名
                        video_add_list3 = re.findall('\w+', video_add_list2[0])
                        video_add = video_add_list3[0]
                        print(video_add,"video add")
                        # 执行指令生成文件和文件名
                        channel_list = re.findall('\d:\d+', line)
                        channel = str(channel_list[0])
                        os.system("cd %s &&ffmpeg -i %s -map %s -c copy Stream_Video_%s.%s >>Stream_Video_Infolog.txt 2>&1" % (path_to_ffmpeg, dirname + "\\" + fname, channel, Raw_name, video_add))
                        shutil.copy(path_to_ffmpeg + "\\" + "Stream_Video_Infolog.txt",path_to_result + "\\" + suffix_name + "\\" + Raw_name)
                        with open(path_to_ffmpeg + "\\" + "Stream_Video_Infolog.txt", 'r',encoding='ISO-8859-1') as Logcheck:
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
            time.sleep(2)
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
                        os.system("cd %s &&ffmpeg -i %s -map %s -c copy Stream_Audio_%s.%s >>Stream_Audio_Infolog.txt 2>&1" % (path_to_ffmpeg, dirname + "\\" + fname, channel, Raw_name, audio_add))
                        shutil.copy(path_to_ffmpeg + "\\" + "Stream_Audio_Infolog.txt",path_to_result + "\\" + suffix_name + "\\" + Raw_name)
                        with open(path_to_ffmpeg + "\\" + "Stream_Audio_Infolog.txt", 'r',encoding='ISO-8859-1') as Logcheck:
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
                if ("Stream_Video_" + Raw_name ) in i:
                    Stream_size_Video = os.path.getsize(path_to_ffmpeg + "\\" + "Stream_Video_" + Raw_name + "." + video_add)
                    break
                else:
                    Stream_size_Video = 0
            for i in os.listdir(path_to_ffmpeg):
                if ("Stream_Audio_" + Raw_name ) in i:
                    Stream_size_Audio = os.path.getsize(path_to_ffmpeg + "\\" + "Stream_Audio_" + Raw_name + "." + audio_add)
                    break
                else:
                    Stream_size_Audio = 0

            # 计算文件差值
            total_size = Stream_size_Video + Stream_size_Audio
            size_differ = Stream_size_Raw - total_size
            if size_differ > (Stream_size_Raw / 100):
                persentage1 = size_differ / Stream_size_Raw
                persentage = (persentage1 * 100)
                EL.write("%s:\n生成音视频文件大小总和与源流大小差距为%s，损失达源流大小的百分之%.2f\n\n" % (
                Raw_name + suffix_name, size_differ, persentage))
            time.sleep(2)
            if os.path.exists(path_to_ffmpeg + "\\" + "Stream_Raw_Infolog.txt"):
                os.remove(path_to_ffmpeg + "\\" + "Stream_Raw_Infolog.txt")
            # 把在ffmpeg.exe同级目录生成的流文件复制到流名文件夹,并且删除ffmpeg中的此流
            for i in os.listdir((path_to_ffmpeg)):
                if ("Stream_Video_" + Raw_name ) in i:
                    shutil.copy(path_to_ffmpeg + "\\" + "Stream_Video_" + Raw_name + "." + video_add,path_to_result + "\\" + suffix_name + "\\" + Raw_name)
                    os.remove(i)
                else:
                    pass
                if ("Stream_Audio_" + Raw_name ) in i:
                    shutil.copy(path_to_ffmpeg + "\\" + "Stream_Audio_" + Raw_name + "." + audio_add,path_to_result + "\\" + suffix_name + "\\" + Raw_name)
                    os.remove(i)
                else:
                    pass

#如果不close，txt文件就一直呈写入状态，close不能放进循环，一旦放进循环那么下一个内容就没有权限进行写入了
EL.close()

#删除ffmpeg文件夹内分解后的流
#os.chdir(path_to_ffmpeg)
#for i in os.listdir(path_to_ffmpeg):
 #   if i == 'ffmpeg.exe':
  #      pass
   # else:
    #    os.remove(i)

#改回之前的名字(路径名，流名)
time.sleep(2)
i = 0
if i < len(no_repeat_fname_list):
    os.renames(new_fname_list[i], no_repeat_fname_list[i])
    i += 1

j = 0
for dirname,subdirList,fileList in os.walk(path_to_stream[0]):
    for fname in fileList:
        if os.path.splitext(fname)[1].lower() not in total_invaluble_suffix:
            if j < error_stream_name_list_len:
                os.rename(dirname + '\\' + new_stream_name_list[j],dirname + '\\' + stream_name_list[j])
                j += 1

SFL.close()

print("**********Finish**********")
print("Every Folder should have 6 file(3 Audio/Video && 3 text)")
print("If the number of files is incorrect, please check ErrorLog.txt,thank you.")
print("The result is set in %s" %(max(dic) + '\\' + 'ResultOfProcess'))
time.sleep(10)


