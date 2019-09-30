import os
path_to_stream = []
path_to_stream.append(os.getcwd())


total_invaluble_suffix = ['.py','.txt','.ts',',trp','.exe','.xlsx','.db','.log','.ini','.rar','.js','.zip','.bat','xls','html','.doc','.docx','adif','.jpg','.png']

for dirname,subdirList,fileList in os.walk(path_to_stream[0]):
    for fname in fileList:
        # 修改路径中的非法字符
        #fname_arr = fname.split(':')
        #print(fname)
        #print(str(fname[1]))
        if '&' or " " in str(dirname):
            print('dirname wrong')
            dir_name = dirname.replace('&', '_').replace(' ', '_')
            print(dir_name)
            os.chdir(path_to_stream[0])
            os.renames(dirname, dir_name)
        else:
            print('dirname is ok')
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
            #SFL.write(need + "\n")