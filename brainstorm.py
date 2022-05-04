# Join with weather data
# Average sleep per day of the week?
# If less sleep lead to more spending
# If weather effected food or coffee spending
# If sunny weather effected buying clothes
# If Weather effected sleep
"""
https://stackoverflow.com/questions/48231758/merge-pandas-dataframes-based-on-date#:~:tex
t=A%20generalised%20solution%20where%20there%20can%20be%20any,fix%20the%20column%20names%
20using%20rename%20and%20add_prefix
"""
import pandas as pd
import numpy as np
import scipy.stats as stats

#read sleep into pandas DF
sleep_df=pd.read_csv("sleep.csv")

#read  checking into DF
checking_df=pd.read_csv("checking-cleaned.csv")
#Drop name, memmo
del checking_df["Name"]
del checking_df["Memo"]

#print(checking_df)
#make copies of checking for merging:
checking_1_df=checking_df.copy()
checking_2_df=checking_df.copy()

#read weather into DF
weather_df=pd.read_csv("spokane_daily_weather_cleaned.csv")
# combine checking with sleep
merged_sleep_df=sleep_df.merge(checking_1_df,on=["Date"])

# combine checking with weather
merged_weather_df=weather_df.merge(checking_2_df,on=["Date"])


#Compute basic stats on checking:
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
#compute_stats("Amount",checking_df)
grouped_by_category_checking=checking_1_df.groupby("Category")
group_keys=grouped_by_category_checking.groups.keys()
#print(group_keys)
#print(grouped_by_category_checking.get_group("Gas"))

for key in group_keys:
  
    print("Stats for Category:",key)
    compute_stats("Amount",grouped_by_category_checking.get_group(key))

#Hypothesis testing:
# On days I bought coffee did I sleep less than 6 hourss?

coffee=grouped_by_category_checking.get_group("Coffee")

coffee_dates=coffee["Date"]
merged_coffee_sleep=sleep_df.merge(coffee_dates,on="Date")
#print(merged_coffee_sleep)
merged_coffee_sleep_mean=merged_coffee_sleep["Hours Sleep"].mean()
coffee_sleep_ser=merged_coffee_sleep["Hours Sleep"]


print("Average sleep on days with coffee:",merged_coffee_sleep_mean)
average_sleep=merged_sleep_df["Hours Sleep"].mean()
sleep_ser=merged_sleep_df["Hours Sleep"]

print("Average total sleep",average_sleep)

#non_coffee_keys=['Amazon', 'Pandora', 'Income', 'Hair', 'Misc', 'Phone', 'Piercing', 'Travel', 'Gym', 'Vending Machine', 'Clothes', 'Gas', 'Food', 'Groceries', 'Vet Bill']
#print(non_coffee_keys)

merged_sleep_grouped=merged_sleep_df.groupby("Category")
"""
total=0
n=0
for key in non_coffee_keys:
    print(key)
    grouped=merged_sleep_grouped.get_group(key)
    sum=grouped["Hours Sleep"].sum()
    #print(sum)
    count=grouped["Hours Sleep"].count()
    total=total+sum
    n=n+count
non_coffee_avg_sleep=total/n
print("Average on non doffee days:",non_coffee_avg_sleep)
"""
#Do a t test for 1 sample:
#1. Identify null and alternative hypothesis:
# On days I bought coffee did I sleep less than 7 hourss?
# Null Hypothesis: Average sleep (on dates that I bought coffee)>= 7
# Alternative Hypothesis: Average sleep(on dates that I bought coffee)< 7
#2 Select alpha: Level of significance 0.01
#3. Choose test statistic:
#Ours will be a 1 sample test statistic
#4. Formulate decision rule:
# For a one tailed test, alpha =0.01, if t_computed is negative, and p<0.05, we can reject our null hypothesis
t_computed,p=stats.ttest_1samp(coffee_sleep_ser,7)
print(t_computed,p)
print("Since p/2>alpha, we cannot reject our null hypothesis")

import matplotlib.pyplot as plt

#Visualize transaction frequency"
y_list=[]
x_list=[]
for group in grouped_by_category_checking:
    group_name=group[0]  
    print(group_name)
    group_total=len(group[1]["Category"])
    print(group_total)
    if group_name not in x_list:
        x_list+=[group_name]
    y_list+=[group_total]
y_ser=pd.Series(y_list)
x_ser=pd.Series(x_list)
print(y_ser)
print(x_ser)

plt.figure() # to create a new "current" figure
plt.pie(y_ser, labels=x_ser, autopct="%.2f%%")
plt.title("Frequency of transaction by type")
plt.show()