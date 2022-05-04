import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def compute_stats(col_name,df):
    total=df[col_name].count()
    sum=df[col_name].sum()
    mean=df[col_name].mean()
    std=df[col_name].std()
    median=df[col_name].median()
    min=df[col_name].min()
    max=df[col_name].max()
    stats_dict={"Count":total,"Sum":sum,"Mean":mean,"Standard Deviation":std,"Median":median,"Min":min,"Max":max}
    print (stats_dict)


def lineplot(len,x_ser,xlabel,ylabel,title):
    plt.plot(len,x_ser,lw=5)
    #lets beautify the plot
    #first to fix overlapping x tick labels:
    plt.xticks(rotation=25,ha="right")#ha=horizontal alignment
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid()#gives gridlines

def printcats():
    print("cats")

def find_frequency_and_amount(grouped_df,attribute):
    y_list=[]
    x_list=[]
    z_list=[]
    w_list=[]
    group_total=0
    group_amount=0
    for group in grouped_df:
        group_name=group[0]
        for item in group[1][attribute]:
            group_total+=1
            group_amount+=group[1][attribute].sum()
        if group_name not in x_list:
            x_list+=[group_name]
        y_list+=[group_total]
        w_list+=[group_amount]
        group_amount=abs(group_amount)
        z_list+=[group_amount]
        group_total=0
        group_amount=0
    y_ser=pd.Series(y_list)#frequency of transaction labelss
    x_ser=pd.Series(x_list)#labels
    z_ser=pd.Series(z_list)#abs value of transactions
    w_ser=pd.Series(w_list)#actual value of transactions
    return(x_ser,y_ser,z_ser,w_ser)

def get_category_labels(ser):
    category_labels=[]
    for value in ser:
        if value not in category_labels:
            category_labels.append(value)
    return(category_labels)