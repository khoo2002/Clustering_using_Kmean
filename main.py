import sys
import subprocess

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install','sklearn'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install','numpy'])

import tkinter as tk
from tkinter import filedialog as fd 
import tkinter.messagebox
import os
p_file = ""
n_cluster = 0
def KMEAN(absolute_path,number_cluster):
    import os, codecs
    from PIL import Image
    import numpy as np
    from sklearn.cluster import KMeans
    def get_file_name(path): #获得文件名
        filenames = os.listdir(path) #  os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表。
        path_filenames = []
        filename_list = [] #创建两个列表
        for file in filenames: #便利文件夹里面的文件
            if not file.startswith('.'):
                path_filenames.append(os.path.join(path, file))#路径拼接
                filename_list.append(file) #使用append 增加文件
        return path_filenames #返回：带文件名的路径
    def kmeans_detect(file_list, cluster_nums, randomState=None): # KNN 线性分类器
        features = []
        files = file_list #特征检测
        for file in files:
            img = Image.open(file)
            img = img.resize((1000,1000))
            img = img.convert('L')
            tmp = np.array(img)
            vec = tmp.ravel()
            features.append(vec)
        input_x = np.array(features) #计算关键点
        kmeans = KMeans(n_clusters=cluster_nums, random_state=randomState).fit(input_x) #关键点聚类
        return kmeans.labels_, kmeans.cluster_centers_
    def res_fit(filenames, labels):
        files = [file.split('/')[-1] for file in filenames]
        return dict(zip(files, labels)) #打上标签
    def save(path, filename, data):
        file = os.path.join(path, filename) #路径拼接
        with codecs.open(file, 'wb', encoding='utf-8') as fw: #编码
            for f, l in data.items():
                fw.write("{}\t{}\r\n".format(f,l)) # 控制换行
    path_filenames = sorted(get_file_name(absolute_path)) # 从picture 文件夹里面获取图片名字
    labels, cluster_centers = kmeans_detect(path_filenames, number_cluster) # 识别n组数字类
    imgs = os.listdir(absolute_path)
    imgnum = len(imgs)  # 文件夹中图片的数量
    res_dict = res_fit(path_filenames, labels) #带上标签
    grade=[n for n in range(number_cluster)]
    with open('result.txt','w') as f:
        for key,value in res_dict.items():
            f.write('{0} : {1}\n'.format(key,grade[value]))
        f.close()
    return imgnum,res_dict,grade

def result_window(text):
     win= tk.Tk()
     win.title('Result of Clustering')
     win.geometry('800x600')
     ti = tk.Label(win, text='Result of Clustering', font=('Arial', 22), width=30, height=2)
     re = tk.Label(win, text=text, font=('Arial', 12))
     fo = tk.Label(win, text="By ZW", font=('Arial', 20), width=30, height=2)
     ti.pack(side="top")
     re.pack()
     fo.pack(side="bottom")
     win.mainloop()


def folder_ex():
    global p_file
    folder = fd.askdirectory(initialdir=os.path.normpath("C://"), title="Select Folder")
    p_file = folder
    
def submit():
    n_cluster = int(e_n_cluster.get())
    x = p_file
    fp_file = "\/".join(x.split("/"))
    n_img,r_d,g = KMEAN(fp_file,n_cluster)
    result='文件夹里面图片数量:{0}\n分类结果为:\n'.format(n_img)
    for key,value in r_d.items():
        result += "{0}:{1}\n".format(key,g[value])
    result_window(result)

window = tk.Tk()
window.title('Clustering')
window.geometry('800x600')
frame = tk.Frame(window)
frame_l = tk.Frame(frame)
frame_r = tk.Frame(frame)
space = tk.Label(window, width=30, height=1)
f_r_space = tk.Label(frame_r, width=30, height=2)
f_l_space = tk.Label(frame_l, width=30, height=2)
title = tk.Label(window, text='Clustering', font=('Arial', 22), width=30, height=2)
l_btn_cluster = tk.Label(frame_l, text='Number of Cluster(0-100):', font=('Arial', 12), height=2)
l_btn_folder = tk.Label(frame_l, text='Source (Folder):', font=('Arial', 12), height=2)
btn_folder = tk.Button(frame_r, text='Select Folder', font=('Arial', 12), width=18, height=2, command=folder_ex)
btn_submit = tk.Button(window, text='Submit', font=('Arial', 12), width=12, height=1, command=submit)
e_n_cluster = tk.Entry(frame_r, show = None,  font=('Arial', 12))
footer = tk.Label(window, text="By ZW", font=('Arial', 20), width=30, height=2)
title.pack(side='top')
frame.pack()
frame_l.pack(side='left')
frame_r.pack(side='right')
l_btn_cluster.pack()
e_n_cluster.pack()
f_r_space.pack()
f_l_space.pack()
l_btn_folder.pack()
btn_folder.pack()
space.pack()
btn_submit.pack()
footer.pack(side='bottom')
window.mainloop()
