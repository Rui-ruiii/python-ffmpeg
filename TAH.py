import os
path_to_stream = []
path_to_stream.append(os.getcwd())

total_invaluble_suffix = ['.py','.txt','.ts',',trp','.exe','.xlsx','.db','.log','.ini','.rar','.js','.zip','.bat','xls','html','.doc','.docx','adif','.jpg','.png']

fname_list = []
new_fname_list =[]
for dirname,subdirList,fileList in os.walk(path_to_stream[0]):
    for fname in fileList:
        #只获取音频文件的路径
        if os.path.splitext(fname)[1] not in total_invaluble_suffix:
            fname_list.append(dirname)
no_repeat_fname_list = list(set(fname_list))
print(no_repeat_fname_list)
for unin in no_repeat_fname_list:
    if '&' in unin:
        unin = unin.replace('&','_')
    if ' ' in unin:
        unin = unin.replace(' ','_')
    else:
        pass
    new_fname_list.append(unin)
print(new_fname_list)

#改名
list_len = len(no_repeat_fname_list)
i = 0
if i < len(no_repeat_fname_list):
    #f = open(no_repeat_fname_list[i])
    #f.close(no_repeat_fname_list[i])
    os.rename(no_repeat_fname_list[i],new_fname_list[i])
    i += 1

if i < len(no_repeat_fname_list):
    os.rename(new_fname_list[i],no_repeat_fname_list[i])
    i += 1