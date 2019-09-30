import os
path_to_stream = []
path_to_stream.append(os.getcwd())


total_invaluble_suffix = ['.py','.txt','.ts',',trp','.exe','.xlsx','.db','.log','.ini','.rar','.js','.zip','.bat','xls','html','.doc','.docx','adif','.jpg','.png']

for dirname,subdirList,fileList in os.walk(path_to_stream[0]):
    for fname in fileList:
        # 修改路径中的非法字符
        dirname_arr = dirname.split(':')
        print(dirname)
        print(dirname_arr[1])
        if '&' or " " in str(dirname):
            print('dirname wrong')
        else:
            print("pass")
        for i in dirname:
            print(i.isspace())