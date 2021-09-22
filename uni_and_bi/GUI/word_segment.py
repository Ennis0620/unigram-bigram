import re
import json
import time

#正向分割
def forward_seg(source_sentence,word_dic,max_word_length): 
    
    start = time.time()
    
    source_sentence = re.sub(r'[^\u4e00-\u9fa5]', "",source_sentence)
    #在dic中找到 切分的字串 
    seg_string=[]   
    sum_len=0   
    original = source_sentence       
    while(len(source_sentence)>0):             
        #如果不再字典中
        if(source_sentence not in word_dic):
            #從字典中最長的字，所以不用每次都要整句開始找 只要從最長的字數字開始縮小就好        
            #如果字串長度>=字典中最長的字 那麼要從字典中最長的字數開始切 
            if(len(source_sentence)>max_word_length):               
                source_sentence = source_sentence[:max_word_length]               
            #否則就一個一個慢慢切    
            else:
                #
                source_sentence = source_sentence[:len(source_sentence)-1]         
        else:
            #統計目前分割完的字總共多長
            sum_len+=len(source_sentence)
            #加入串列中
            seg_string.append(source_sentence)
            #字典出現次數+1
            word_dic[source_sentence]+=1
            #source_sentence 就 變成原本完整句子的字串 扣除 前面分割完的字句
            source_sentence =  original[sum_len:]   
    #print(seg_string)
    
    end = time.time()
    print("正向分割時間:",end-start)
    return seg_string   
        

#反向分割
def backward_seg(source_sentence,word_dic_back,max_word_length):
    
    start = time.time()
    
    source_sentence = re.sub(r'[^\u4e00-\u9fa5]', "",source_sentence)
    #在dic中找到 切分的字串 
    seg_string=[] 
    sum_len=0 
    original = source_sentence    
    while(len(source_sentence)>0):            
        #如果不再字典中
        if(source_sentence not in word_dic_back):
            #從字典中最長的字，所以不用每次都要整句開始找 只要從最長的字數字開始縮小就好
            #如果字串長度>=字典中最長的字 那麼要從字典中最長的字數開始切 
            if(len(source_sentence)>max_word_length): 
                source_sentence = source_sentence[len(source_sentence)-max_word_length:len(source_sentence)+1]     
            #否則就一個一個慢慢切    
            else:
                #
                source_sentence = source_sentence[1:]                 
        else:
            #統計目前分割完的字總共多長
            sum_len+=len(source_sentence)
            #加入串列中
            seg_string.append(source_sentence)
            #字典出現次數+1
            word_dic_back[source_sentence]+=1
            #source_sentence 就 變成原本完整句子的字串 扣除 前面分割完的字句
            source_sentence =  original[:len(original)-sum_len]
    end = time.time()
    print("反向分割時間:",end-start)
    #print(seg_string)
    return seg_string[::-1] 
           

def fully_seg(source_sentence,word_dic,bi_gram,max_key_len):
    
    s = time.time()
    
    source_sentence = re.sub(r'[^\u4e00-\u9fa5]', "",source_sentence)
    lists = []
    index_range_list = []
    word_net = [[] for i in range(len(source_sentence))] #建立詞網
    for length in range(len(source_sentence)):
        for j in range(length+1,len(source_sentence)+1):
            #如果再找切分可能的字詞長度 大於 字典中最大長度時 就結束此字的可能切分 
            if(j - length > max_key_len):
                break           
            word = source_sentence[length:j]           
            if word in word_dic:
                #分割的詞
                lists.append(word)
                #
                word_net[length].append(word)
                #找出分割所在的index
                index_range = str(length) + "," + str(j-1)               
                index_range_list.append(index_range)                               
    #print("完全切分:",lists) 
    #print("詞網:",word_net)             
    """-----找出句子組合-----"""
    pro=[]
    
    if(len(word_net)==0): #如果遇到空白 就 跳回傳空
        return ""
    
    final_pro = [] #存這個句子各個組合的 總機率   
    for i,start in enumerate(word_net[0]):
        #print(start+"|<s>",bi_gram[start+"|<s>"])
        count=0
        
        start_len = 0+len(start)#算開頭
        
        if bi_gram.get(start+"|<s>"):
            start_pro = bi_gram[start+"|<s>"]#開頭 是 start 的機率
        else:
            start_pro = 0.000000001
        
        
        per_list=[start] #存所有句子組合
        
        for j in range(1,len(word_net)):
            
            per_row_dif_DIC = {}
            
            for k in word_net[j]:
                
                 if  start_len == j :
                    
                    pp = k +"|"+ per_list[count] # 後面|前面 的 文字 例如: 的|項目 => 項目的
                    
                    #如果 pp 不在 bi_gram 內的話 代表機率=0
                    if not bi_gram.get(pp):
                        p = 0.000000001                        
                        per_row_dif_DIC.setdefault(k,p)
                        #print("文字:",pp,"機率:",p)
                    else:
                        p = bi_gram[pp]  #該 的|項目 的機率
                        
                        per_row_dif_DIC.setdefault(k,p)
                        #print("文字:",pp,"機率:",bi_gram.get(pp))
                        
            if per_row_dif_DIC:
                maxstr = max(per_row_dif_DIC, key=per_row_dif_DIC.get)
                start_pro*= per_row_dif_DIC[maxstr]
                start_len+=len(maxstr)
                count+=1
                per_list.append(maxstr)
                
        #print("---------------")    
        final_pro.append(start_pro)
        pro.append(per_list)        
    #print("可能組合:",pro)
    #print("機率:",final_pro)
    #回傳機率最大的可能組合
    lists = pro[final_pro.index(max(final_pro))]    
    print(lists)       
    
    end = time.time()
    print("機率分割時間:",end-s)
    return lists


