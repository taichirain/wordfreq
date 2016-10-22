#打开文件
def openfile(): 
    filename_tup=QFileDialog.getOpenFileName(self,'选择文件')
    if filename_tup==('', ''): #点击打开文件按钮但未选择文件，为防止闪退，设置pass
        pass           
    elif filename_tup :
        self.sword_dic={} #初始化字典
        self.progressBar.show() #显示进度条
        while self.completed<50: #设置进度条速度，先加载50%，然后读入文件，最后再加载%50
            self.completed+=0.0001
            self.progressBar.setValue(self.completed)

#读取文件，存入字典
def readfile():
    doctype = re.findall(r'\..+', filename_tup[0]) #使用正则表达式找出文件类型名
    start = time.clock() #设置开始时间点
    if doctype==['.txt']:
        with open(filename_tup[0],'r',encoding='utf-8') as f:
            for line in f: #如果是txt文档打开后逐行读入
                words_list=[]
                words_list = re.findall(r'\d+\.\d+|[a-z0-9A-Z]+', str(line).lower()) #使用正则表达式找出每一行的单词和数字，存入列表
                for i in words_list: 
                    if (i not in self.sword_dic):  #如果列表中的单词不存在于字典中，将单词存入字典，初始value置1
                        self.sword_dic[i] = 1
                    else:  #如果列表中的单词存在于字典中，将单词存入字典，value加1
                        self.sword_dic[i] = self.sword_dic[i] + 1
    elif doctype==['.docx'] or doctype==['.wps']: #如果是docx文件，使用docx模块读取
        doc = docx.Document(filename_tup[0])
        pc = doc.paragraphs
        for each in pc:
            words_list = []
            words_list = re.findall(r'\d+\.\d+|[a-z0-9A-Z]+', str(each.text).lower())
            for i in words_list:
                if (i not in self.sword_dic):
                    self.sword_dic[i] = 1
                else:
                    self.sword_dic[i] = self.sword_dic[i] + 1
        doc.save(filename_tup[0])
        end=time.clock()  #结束时间
    while self.completed<100:  #加载剩余%50进度条
        self.completed=self.completed+0.0001
        self.progressBar.setValue(self.completed)
    time.sleep(0.3) 
    self.progressBar.hide() #0.3秒后隐藏进度条
    self.label.setText('导入成功  耗时:'+str(end-start))  #在下方的label中显示消耗时间

#统计词频
def word_freq_count():
    dict=sorted(self.sword_dic.items(), key=lambda d: d[0], reverse=False)

    for k, v in dict: #将key和value分别存入两个列表
        k_list.append(k)
        v_list.append(v)
    dict.clear()
    i = 0
    k_len = len(k_list) #len出列表长度
    houzhui = ['s', 'es', 'ed', 'd', 'ing']
    while i < (k_len - 1): #从第一个单词开始进行词形还原
        if len(k_list[i]) > 2: #还原的都是长度大于2的单词
            for each in houzhui: #对于后缀列表中的每个后缀，如果单词加上后缀后等于后一个单词，则将后一个单词变为前一个单词，
                                #如第三个单词'egg'+'s'==第四个单词'eggs'，将第四个'eggs'变为'egg'
                if k_list[i + 1] == k_list[i] + each:
                    k_list[i + 1] = k_list[i]
        i = i + 1
    for num in k_list: #变换完成后，再次统计词频，存在key，value两个列表中
        i = k_list.index(num)
        while i < k_len - 1 and num == k_list[i + 1]:
            v_list[i] = v_list[i] + v_list[i + 1]
            k_list.pop(i + 1)
            v_list.pop(i + 1)
            k_len = k_len - 1
    i=0
    k_len=len(k_list)
    self.dic={}
    while i<k_len:  #key、value列表转为字典
        self.dic[k_list[i]]=v_list[i]
        i=i+1
    self.sword_dic={}
    self.sword_dic = sorted(self.dic.items(), key=lambda d: d[1], reverse=True)
    for k, v in self.sword_dic: #在'textBrowser'中插入统计结果
        self.textBrowser_2.insertPlainText((str(k) + ' 出现 ' + str(v) + ' 次\n'))


#查询单词频率
def word_freq():
    temp=self.lineEdit.text().lower()  #获取linEdit中输入的单词
    if temp in self.dic:
        self.lineEdit_2.setText(temp+' 出现 '+str(self.dic[temp])+' 次')
    else:
        self.lineEdit_2.setText('未查找到')

#批量查询
def batch_query():
    filename_tup = QFileDialog.getOpenFileName(self, '选择文件')
    if filename_tup==('', ''):
        pass
    elif filename_tup :
        with open(filename_tup[0], 'r', encoding='utf-8') as f:
            for line in f:  #将要查询的单词统一放在txt文档中，读取稳定将单词写入查询列表
                words_list = []
                words_list = re.findall(r'\d+\.\d+|[a-z0-9A-Z]+', str(line).lower())
                for each in words_list:
                    query_word.append(each)
    for k in query_word:  #对列表中的每个单词进行查询并输出结果
        if k in self.dic:
            self.textBrowser_2.insertPlainText((str(k) + ' 出现 ' + str(self.dic[k]) + ' 次\n'))
        else:
            self.textBrowser_2.insertPlainText((str(k) + '不存在\n'))

#保存查询结果
def save_result():
    filename=QFileDialog.getSaveFileName(self,'文件保存','D:/','Text Files (*.txt)')  #PyQt5中保存文件的语句
    if filename==('', ''):
        pass
    elif filename:
        fn=open(filename[0],'w')
        for k, v in self.sword_dic:
            fn.writelines((str(k) + ' occur ' + str(v) + ' times\n'))
        fn.close()
 
 #主函数
def main():
    app=QApplication(sys.argv)
    win=ExampleApp()
    win.show()
    app.exec_()

#程序入口
if __name__ == '__main__':
    main()