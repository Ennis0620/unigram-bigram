import re
import time

word_dic = {} #建立常用字詞的字典        

#30萬單字數量
with open("lexicon1_raw_nosil.txt",encoding='utf-8-sig') as fp:
    per_line = fp.readlines()
    for dic in per_line:
        dic_split = dic.split(" ")
        word_dic.setdefault(dic_split[0],0)
        


uni_gram = {}
bi_gram = {}

start = time.time()



count=0

#建立Uni gram 和 bi gram   
with open("GigaWord_text_lm.txt",encoding='utf-8-sig') as fp:
    
    key_len_set = set()#找字詞的長度 為了完全切分的加速
    per_line = fp.readlines() 
    for per_sentence in per_line:     
        count+=1  
        per_sentence_split = per_sentence.strip("\n").split(" ")
        
        #uni_gram 計算出現次數
        for word in per_sentence_split:         
            key_len_set.add(len(word))#加入unigram的字詞長度到set          
            if(word in uni_gram):
                uni_gram[word]+=1              
            else:
                uni_gram.setdefault(word,1)
           
        #加入句子的 始 和 末
        len_sentence_split = len(per_sentence_split)
        per_sentence_b_e = per_sentence_split
        per_sentence_b_e.insert(0,"<s>")
        per_sentence_b_e.insert(len_sentence_split,"</s>")
        
        
        #bi_gram 前後出現可能次數  計算
        for index in range(1,len_sentence_split):         
            # 目前的詞 後面接 另外一個詞 ex: 商品 前面是 <s> 的次數 記錄成 => 商品|<s>
            key = per_sentence_b_e[index]+"|"+per_sentence_b_e[index-1]     
            if key in bi_gram: 
                bi_gram[key]+=1
            else:
                bi_gram.setdefault(key,1) 
        
        if(count%100000==0):
            print(count)
            


#計算 該字詞接在某字詞後出現次數/總出現次數 的 bi gram
for key in bi_gram:
    
    key_split = key.split("|") #分割字典中的key 去計算 <s>後接 商品 / 商品總出現次數的bi gram
    
    if key_split[0] == "</s>":        
        bi_gram[key] = bi_gram[key]/uni_gram[key_split[1]]        
    elif key_split[1] == "<s>":
        bi_gram[key] = bi_gram[key]/uni_gram[key_split[0]]
    else:       
        bi_gram[key] = bi_gram[key]/uni_gram[key_split[0]]        
    
#找到uni gram字典中最長的key 加速分割
max_key_len =max(key_len_set)
      
end = time.time()
print(end - start)


#要先算Uni gram   ex: 項目 在全部總共出現的次數
#接著算Bi gram   ex: P(項目|的) = (項目 後面接 的 的全部次數)/(的 全部出現的次數)           
      
'''
#存檔
import json
tf = open("bi_gram_all.json", "w")
json.dump(bi_gram,tf)
tf.close()

tf = open("uni_gram_all.json", "w")
json.dump(uni_gram,tf)
tf.close()
'''  