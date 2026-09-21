import os

#输入文件的目录
folder = r'C:/Users/forfe/Desktop/project/Python.project/all name'
#输入前缀的名字
add_front = 'qqq'
#输入后缀的名字
add_suffix = ''   
#默认为先打印预览，确认修改时将True改为False
run = True 

if not os.path.isdir(folder):
    print('不是一个有效目录!')
    exit()
    
for file in os.listdir(folder):
    full_path = os.path.join(folder,file)
    if os.path.isfile(full_path):
        name,ext = os.path.splitext(file)
        add = f'{add_front}{name}{add_suffix}{ext}'
        new_file = os.path.join(folder,add)
                
        if run:
            print(f'打印成功 {file} --> {add}')
        else:
            try:
                os.replace(full_path,new_file)                
                print(f'重命名成功 {file} --> {add}')
            except Exception as e:
                print('重命名失败!')

    else:
        print('不是一个有效文件或是一个文件夹!')

if run:
    print('\n该模式为打印模式,确认无误后将run改为False执行重命名模式')
else:
    print('\n🎉重命名已完成')


       


            
    
    




