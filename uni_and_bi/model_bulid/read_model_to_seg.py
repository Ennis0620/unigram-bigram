# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 18:26:33 2021

@author: user
"""

import re
import json
import time


def fully_seg(source_sentence,word_dic):
    
    lists = []
    #index_range_list = []
    word_net = [[] for i in range(len(source_sentence))] #建立詞網 2維的list
    
    #做完全切分
    for length in range(len(source_sentence)):
        for j in range(length+1,len(source_sentence)+1):
            #如果再找切分可能的字詞長度 大於 字典中最大長度時 就結束此字的可能切分 
            if(j - length > max_key_len):
                break
            #例如 項目的研究  項 = [length=0:1] 項目=[length=0:2]
            word = source_sentence[length:j]
            #如果這個詞 在 uni_gram 就代表是正確的切分
            if word in word_dic:
                #切分的詞
                lists.append(word)
                #詞網
                word_net[length].append(word)
                #找出分割所在的index
                #index_range = str(length) + "," + str(j-1)                
                #index_range_list.append(index_range)                          
    #print("完全切分:",lists) 
    #print("詞網:",word_net)          
    
    """-----找出句子組合-----"""
    pro=[]   
    if(len(word_net)==0): #如果遇到空白 就 跳回傳空
        return ""  
    final_pro = [] #存這個句子各個組合的 總機率   
    for i,start in enumerate(word_net[0]):
        count=0      
        start_len = 0+len(start)#算開頭長度 index        
        if bi_gram.get(start+"|<s>"):
            start_pro = bi_gram[start+"|<s>"]#開頭 是 start 的機率
        else:
            start_pro = 0.000000001#代表不存在model中
        
        per_list=[start] #存所有句子組合
        
        for j in range(1,len(word_net)):     
            per_row_dif_DIC = {}#相同開頭的詞的機率  目、目的
            #如果 該詞有在word_net中
            for k in word_net[j]:
                 #如果 目前index 在 word_net index為 j 代表是可以組合的 
                 if  start_len == j :
                    # 後面|前面 的 文字 例如: 的|項目 => 項目的
                    pp = k +"|"+ per_list[count]         
                    #如果 pp 不在 bi_gram 內的話 代表不存在model中
                    if not bi_gram.get(pp):
                        p = 0.000000001                        
                        per_row_dif_DIC.setdefault(k,p)#將詞和機率存在字典
                    else:
                        p = bi_gram[pp]  #該 的|項目 的機率
                        per_row_dif_DIC.setdefault(k,p)         
            #如果 per_row_dif_DIC 中有東西的話 =>因為可能有1種以上 要找出最大可能       
            if per_row_dif_DIC:
                maxstr = max(per_row_dif_DIC, key=per_row_dif_DIC.get) #找最大機率的詞
                start_pro*= per_row_dif_DIC[maxstr]  #連續乘 在 該詞的機率
                start_len+=len(maxstr) #起始長度就會換到 該詞
                count+=1
                per_list.append(maxstr) #加到list代表目前的決定
                      
        final_pro.append(start_pro) #將該開頭 最大可能 字詞組合的機率 加到list
        pro.append(per_list)  # 將該開頭 最大可能 字詞組合 加到list
   
    #回傳 不同開頭中 機率最大的那個組合 
    lists = pro[final_pro.index(max(final_pro))]   
    
    #將出現的詞彙加入字典裏面
    for i in lists:
        if i not in pro_dic:
            pro_dic.setdefault(i,1)
        else:
            pro_dic[i]+=1
         
    return lists
 
#計算分詞後與正確答案重合的部分
def same_slice(max_pro_s,per_sentence,source_sentence):
    
    correct_set=[]
    seg_set=[]
    
    #迴圈取得正確答案在整段文字的index在哪裡
    i = 0
    for index,per in enumerate(per_sentence):
        #利用分割的長度 [項目,的,研究] 找到各自的index所在範圍 
        correct_set.append( str(i)+","+ str((i+len(per)-1)))
        i+=len(per)
    
    #迴圈取得正向分割在整段文字的index在哪裡
    j = 0
    
    for index,per in enumerate(max_pro_s):
        #利用分割的長度 [項目,的,研究] 找到各自的index所在範圍
        #將分割的index放到set中，方面計算分割相同的有哪些
        seg_set.append( str(j)+","+ str((j+len(per)-1)))      
        j+=len(per)
       
    #計算分割正確的數量
    score = set(seg_set) & set(correct_set)   
    return len(score)   
 
load_model_start = time.time() 
    
tf = open("bi_gram_all.json", "r")
bi_gram = json.load(tf)
tf.close()
 
tf = open("uni_gram_all.json", "r")
uni_gram = json.load(tf)
tf.close()

load_model_done = time.time()
print("讀model時間",load_model_done - load_model_start)

start = time.time()

key_len_set = set()

for i in uni_gram:
   key_len_set.add(len(i)) 
   
max_key_len = max(key_len_set)

pro_dic ={} #存入切分字詞的出現次數

correct_slice_num = 0
slice_num = 0 
score = 0
count=0
with open("GigaWord_text_lm.txt",encoding='utf-8-sig') as fp:
    
    per_line = fp.readlines()
    
    for per_sentence in per_line:
        
        correct_seg = per_sentence.strip("\n").split(" ")
        #去除不必要的符號
        origin_sentence = re.sub(r'[^\u4e00-\u9fa5]', "",per_sentence)
        #組合最大可能
        max_pro_s = fully_seg(origin_sentence, uni_gram)
        
        #換成index表示 且切分位置相同的
        score += same_slice(max_pro_s,correct_seg,origin_sentence)
        
        #表準答案總共分割幾組
        correct_slice_num += len(correct_seg)
        #分割出來的有幾組
        slice_num += len(max_pro_s)
        
        count+=1
        if count%50000==0:
            print("目前資料處理數量:",count,"筆")
        
precision_pro = (score/slice_num)*100
recall_pro = (score/correct_slice_num)*100
print("------機率計算-------")
print("score:",score)
print("correct_slice_num:",correct_slice_num)
print("pro_slice_num:",slice_num)
print("精準度:",score,"/",slice_num,"=",precision_pro,"%")
print("召回率:",score,"/",correct_slice_num,"=",recall_pro,"%")
print("F1:", (2*precision_pro*recall_pro)/(precision_pro+recall_pro))        
 
end = time.time()
print("切分時間",end- start)

