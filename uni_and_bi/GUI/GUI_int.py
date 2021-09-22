from tkinter import *
from word_segment import forward_seg,backward_seg,fully_seg
import json
import time

win = Tk() #建立視窗window
win.title('自然語言處理句子分割') #視窗的名子
win.geometry('1480x764') # 設定視窗的大小(長x寬) 
win.config(bg='#4F4F4F') #背景

"""----讀取bi_gram和uni_gram的model----"""
tf = open("bi_gram_all.json", "r")
bi_gram = json.load(tf)
tf.close()
 
tf = open("uni_gram_all.json", "r")
uni_gram = json.load(tf)
tf.close()

"""讀取前後像切分所需的字典"""
word_dic={}
max_word_length=0
with open("lexicon1_raw_nosil.txt",encoding='utf-8-sig') as fp:
    per_line = fp.readlines()
    for dic in per_line:
        dic_split = dic.split(" ")
        word_dic.setdefault(dic_split[0],0)       
        #找出常用字典中最長的字 以每次切分時從此長度進行判斷
        if max_word_length<len(dic_split[0]):            
            max_word_length = len(dic_split[0])
#反向分割的字典
word_dic_back= word_dic.copy()

def getTextInput():
    source_sentence=Text_input.get("1.0","end")#取得文字框的輸入內容 從最初到最末的所有內容
    
    s1 = time.time()
    seg = forward_seg(source_sentence,word_dic,max_word_length)
    e1 = time.time()
    
    s2 = time.time()
    seg_2 = backward_seg(source_sentence,word_dic_back,max_word_length)
    e2 = time.time()
    
    s3 = time.time()
    seg_3 = fully_seg(source_sentence,word_dic,bi_gram,max_word_length)
    e3 = time.time()
    
    
    listbox.delete("0","end")#點擊前都要先刪除原有的
    for i in seg:
        listbox.insert("end", i)#一筆一筆加進去
    
    listbox2.delete("0","end")#點擊前都要先刪除原有的
    for i in seg_2:
        listbox2.insert("end", i)#一筆一筆加進去
    
    listbox3.delete("0","end")#點擊前都要先刪除原有的
    for i in seg_3:
        listbox3.insert("end", i)#一筆一筆加進去
        
        
    stringvar.set("耗時:"+str(e1-s1))#要用stringvar才能更改顯示
    stringvar2.set("耗時:"+str(e2-s2))
    stringvar3.set("耗時:"+str(e3-s3))
    
    print(seg,len(seg),e1-s1)
    print(seg_2,len(seg_2),e2-s2)
    print(seg_2,len(seg_3),e3-s3)
    

title = Label(win,text='自然語言文句切分',bg='#02578E',fg='#FFFFFF',width=87,font=('微軟正黑體',20,'bold'))#標題


label_intput = Label(win,text='請輸入文章:',bg='#4F4F4F',fg='#FFFFFF',height=3,width=10,font=('微軟正黑體',20,'bold'))
Text_input  = Text(win, height=10) 
Text_input.grid(row=1,column=1,rowspan=2,columnspan=3,ipadx=10,ipady=10,padx=50 ,pady=50)

btn_forward = Button(win,command=getTextInput,text='文章切分', width = 10,bg='#02578E',fg='#FFFFFF',font=('微軟正黑體',16,'bold'),relief="flat")#設定搜尋詳細資訊


#前向分割
stringvar = StringVar()
frame = Frame(win) #讓滾動條和listbox結合
frame.grid(row=7,column=0)
label_forward = Label(frame,text='前向分割:',bg='#FFFFFF',fg='#000000',width=10,font=('微軟正黑體',20,'bold')).grid(row=4,column=5)      
l_forward_time = Label(frame,text='耗時:',textvariable=stringvar,bg='#FFFFFF',fg='#000000',width=25,font=('微軟正黑體',10,'bold')).grid(row=6,column=5)
listbox = Listbox(frame,width=20,height=10,font=('微軟正黑體',12,'bold'))#設定listbox
listbox.grid(row=5,column=5)#顯示listbox

scb = Scrollbar(frame ,command=listbox.yview) #設定滾動條
listbox.configure(yscroll=scb.set)
scb.grid(row=5,column=4,sticky=NS)#其中N代表北，S代表南，意思是讓這個布局能夠在此格子中及於從南到北的長度

#後向分割
stringvar2 = StringVar()
frame2 = Frame(win) #讓滾動條和listbox結合
frame2.grid(row=7,column=2)
label_backward = Label(frame2,text='後向分割:',bg='#FFFFFF',fg='#000000',width=10,font=('微軟正黑體',20,'bold')).grid(row=4,column=5)      
l_backward_time = Label(frame2,text='耗時:',textvariable=stringvar2,bg='#FFFFFF',fg='#000000',width=25,font=('微軟正黑體',10,'bold')).grid(row=6,column=5)
listbox2 = Listbox(frame2,width=20,height=10,font=('微軟正黑體',12,'bold'))#設定listbox
listbox2.grid(row=5,column=5)#顯示listbox

scb2 = Scrollbar(frame2 ,command=listbox2.yview) #設定滾動條
listbox2.configure(yscroll=scb2.set)
scb2.grid(row=5,column=4,sticky=NS)#其中N代表北，S代表南，意思是讓這個布局能夠在此格子中及於從南到北的長度

#機率分割
stringvar3 = StringVar()
frame3 = Frame(win) #讓滾動條和listbox結合
frame3.grid(row=7,column=5)
label_forward = Label(frame3,text='機率分割:',bg='#FFFFFF',fg='#000000',width=10,font=('微軟正黑體',20,'bold')).grid(row=4,column=5)      
l_pro_time = Label(frame3,text='耗時:',textvariable=stringvar3,bg='#FFFFFF',fg='#000000',width=25,font=('微軟正黑體',10,'bold')).grid(row=6,column=5)
listbox3 = Listbox(frame3,width=20,height=10,font=('微軟正黑體',12,'bold'))#設定listbox
listbox3.grid(row=5,column=5)#顯示listbox

scb3 = Scrollbar(frame3 ,command=listbox3.yview) #設定滾動條
listbox3.configure(yscroll=scb3.set)
scb3.grid(row=5,column=4,sticky=NS)#其中N代表北，S代表南，意思是讓這個布局能夠在此格子中及於從南到北的長度




title.grid(row=0,columnspan=10)
label_intput.grid(row=1,column=0,sticky=W+S,padx=50)

btn_forward.grid(row=1,column=5,sticky=S)
          
win.mainloop()