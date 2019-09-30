import os
import re
import shutil
import psutil


#获取ffmpeg.exe的路径
path_to_ffmpeg = (os.getcwd() + "\\" + "ffmpeg")

#获取源流文件夹的路径
#path_to_stream = input("**********Please enter the folder path of stream: ")
path_to_stream = []
path_to_stream.append(os.getcwd())



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
#生成全部的文件列表
FL = open('FileLists.txt','w',encoding='utf-8')

file_size = []
for dirname,subdirList,fileList in os.walk(path_to_stream[0]):
    for fname in fileList:
        need = dirname + "\\" + fname
        file_size.append(os.path.getsize(need))
        FL.write(need + "\n")


if sum(file_size) * 2 > max(disk_size_free):
    print("Expected more disk free space")
else:
    print("totol filelist was in %s" % max(dic))
    SFL = open('StreamsFileLists.txt', 'w', encoding='utf-8')
FL.close()

os.chdir(path_to_stream[0])

#筛选流文件生成新的流文件列表
total_invaluble_suffix = ['.py','.txt','.ts',',trp','.exe','.xlsx','.db','.log','.ini','.rar','.js','.zip','.bat','xls','html','.doc','.docx','adif','.jpg','.png']
for dirname,subdirList,fileList in os.walk(path_to_stream[0]):
    for fname in fileList:
        # 修改路径中的非法字符
        if '&' or " " in str(dirname):
            dir_name = dirname.replace('&', '_').replace(' ', '_')
        else:
            dir_name = dirname
        os.chdir(dir_name)
        os.listdir(dir_name)
        print(dir_name)
        os.renames(dirname, dir_name)
        os.chdir(path_to_stream[0])
        need = dir_name + "\\" + fname
        if os.path.splitext(fname)[1].lower() not in total_invaluble_suffix:

            #修改流名中的非法字符
            suffix = os.path.splitext(fname)[1]
            Rawname = os.path.splitext(fname)[0]
            if ' ' in os.path.splitext(fname)[0]:
                Raw_name = os.path.splitext(fname)[0].replace(' ', '_')
                input_name = Raw_name + suffix
            else:
                Raw_name = Rawname
            os.rename(Rawname + suffix,Raw_name + suffix)
            print(Raw_name + suffix)
            SFL.write(need + "\n")

SFL.close()






