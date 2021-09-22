import json
import matplotlib.pyplot as plt

def draw_most_word(word,fre,b): 
    plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta'] #用來正常顯示中文標籤
    
    parameters = {'xtick.labelsize': 25,'ytick.labelsize': 35}#修改坐標軸的文字大小
    plt.rcParams.update(parameters)
    
    plt.figure(figsize=(60, 40))
    plt.style.use("ggplot")
    
    plt.xticks(rotation=90)
      
    plt.plot(word,fre,linewidth=5)
    
    plt.title("機率切分單字出現頻率表", fontsize = 50)
    plt.xlabel("字詞", fontsize = 40)
    plt.ylabel("出現頻率", fontsize = 40)
    
    plt.savefig(b+"_test_word_fre.png")


tf = open("pro_dic.json", "r")
dic_sort = json.load(tf)
tf.close()

#畫圖X，Y軸        
list_forward_x = []
list_forward_y = []           

dic_sort = sorted(dic_sort.items(),key=lambda item:item[1],reverse=True)

for index,i in enumerate(dic_sort): 
    if index < 100:   
        
        list_forward_x.append(i[0])
        list_forward_y.append(i[1])
    else:
        break

draw_most_word(list_forward_x,list_forward_y,"pro_")