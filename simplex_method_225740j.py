import numpy as np
import pandas as pd
import re

#tableauをを表示する関数
def tablueau_print(table):
    x=[row[:] for row in table]
    x[0][0]=' '
    x[0][1]='const'
    x[len(x)-1][0]='z'
    for i in range(len(x[0])-2):
        x[0][i+2]=f'-X_{x[0][i+2]}'
    for i in range(len(x)-2):
        x[i+1][0]=f'-X_{x[i+1][0]}'
    df = pd.DataFrame(x)
    #print('Simplex Tableau')
    print(df.to_string(index=False, header=False))
    print(' ')

#二つのリストから共通しない値を取り出す
def get_unique_el(list1, list2):
    if len(list1) > len(list2):
        list_l=list1
        list_s=list2
    else:
        list_l=list2
        list_s=list1
    for i in list_l:
        if i not in list_s:
            answer = i
    return answer

#式から係数とXの番号を取得する関数
def coff_x(equation):
    x_num=[]
    coeff=[]
    const=[]
    pattern = r'([+-]?\d*)x_(\d+)'
    lhs = equation.split('=')[0]
    rhs = equation.split('=')[1]
    constant= re.findall('(\d+)', rhs)
    matches = re.findall(pattern, lhs)
    for i in constant:
        const.append(i)
    for i in matches:
        coefficient,var_index=i
        x_num.append(int(var_index))
        if coefficient in ('', '+'):
            coeff.append(1)
        elif coefficient == '-':
            coeff.append(-1)
        else:
            coeff.append(int(coefficient))
    return coeff,x_num,const


#説明文
print(' ')
#式の入力を受け付ける
s=1
equation_subject=[]
equation_max=input('Maximize : ')
print('subject to  ')
while True:
    equation_i=input(f'formula{s} : ')
    if equation_i=='0' or not equation_i.strip():
        print(' ')
        break
    equation_subject.append(equation_i)
    s+=1   

# maxmize
max_coff,max_x,max_const=coff_x(equation_max)

#要素数が全て0のt1を作成
t1=[[0]*(len(max_coff)+2) for i in range(len(equation_subject)+2)]

#maxmizeの式をtableauに代入
t1[0][2:len(max_coff)+2]=max_x
t1[len(equation_subject)+1][2:len(max_coff)+2]=[n*(-1) for n in max_coff]

#subject toの式をtablesuに代入
for i in equation_subject:
    subject_coff,subject_x,subject_const=coff_x(i)
    subject_line=equation_subject.index(i)+1
    t1[subject_line][0]=get_unique_el(subject_x,max_coff)
    sub_coff_index=subject_x.index(t1[subject_line][0])
    t1[subject_line][1]=int(subject_const[0])/subject_coff[sub_coff_index]
    for j in max_x:
        if j in subject_x:
            sub_index=subject_x.index(j)
            max_line=t1[0].index(j)
            t1[subject_line][max_line]=subject_coff[sub_index]/subject_coff[sub_coff_index]


tablueau_print(t1)

#以下は作成されたtableauから最適解を求めるプロセス
while True:
    #1. Zの行で，負の値で絶対値最大のもの
    #負の値の絶対値を求め、負の値以外は0を入れる
    negative_num = [abs(i) if i<0 else 0 for i in t1[len(t1)-1] ]
    #最大値とそのインデックスを求める
    max_n = max(negative_num)
    max_index = negative_num.index(max_n)
    nega_line = [t1[i+1][max_index] for i in range(len(t1)-2)]
    #停止条件:選んだ列の値が全て0または負の場合は最適解が存在しない。
    # 全てが0の場合
    if all(x == 0 for x in nega_line):
        print("There is no optimal solution")#最適解はありません(texで日本語出力がうまくできないため英語表記)
        break
    # 全てが負の値の場合
    elif all(x < 0 for x in nega_line):
        print("There is no optimal solution")
        break
    #2. 1で選んだ列の正値で定数の列の値を割る
    constance_value = [t1[i+1][1]/t1[i+1][max_index] for i in range(len(t1)-2) if t1[i+1][max_index]>0 ]
    #3. 2で得た値のうち最小値を示す行をえらぶ
    #最小値とそのインデックスを求める
    min_n = min(constance_value)
    min_index = constance_value.index(min_n)
    #PEの値を保存する。
    PE = t1[min_index+1][max_index]
    #xの入れ替え
    t1[min_index+1][0],t1[0][max_index] = t1[0][max_index],t1[min_index+1][0]


    #新しいtableauの作成
    #PEの行の更新
    for i in range(len(t1[min_index+1])-1):
        t1[min_index + 1][i+1]=t1[min_index + 1][i+1]/PE
    #その他の行の更新
    for i in range(len(t1)-1):
        if i != min_index :
            old = t1[i+1][max_index]
            for j in range(len(t1[i])-1):
                t1[i+1][j+1]=t1[i+1][j+1]-t1[min_index+1][j+1]*old
                
    tablueau_print(t1)
    #停止条件：Zの行が全て0または正ならばすでに最適解である.
    if all(x >= 0 for x in t1[len(t1)-1]):
            print(f"optimal solution is Z={t1[len(t1)-1][1]}")
            break