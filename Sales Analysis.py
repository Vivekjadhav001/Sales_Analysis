import pandas as pd

##[TASK 1]
### Merging all month sales data into one file(CSV)
 import os
 files = [file for file in os.listdir("G:/Datasets/Sales_Data")]

all_month_data=pd.DataFrame()
for file in files:
     df=pd.read_csv("G:/Datasets/Sales_Data/"+file)
     all_month_data=pd.concat([all_month_data,df])

 all_month_data.to_csv("final output.csv",index=False)

 all_data=pd.read_csv("final output.csv")
 print(all_data.head())

##[TASK 2]
##Deleteing missing values rows

all_data=all_data.dropna()
print("Empty  rows deleted succesfully")
print(all_data)

##[TASK 3]
##Finding an error of "Or" 
all_data=all_data[all_data["Order Date"].str[0:2]!="Or"]

##[TASK 4]
##Adding month column to  the dataset for easy understanding
all_data['Month']=all_data["Order Date"].str[0:2]
all_data['Month']=all_data['Month'].astype(dtype='int64')
print(all_data.head())

##[TASK 5]
##Convert quantity orderd and price of each to numerical type
all_data["Quantity Ordered"]=pd.to_numeric(all_data["Quantity Ordered"])
all_data["Price Each"]=pd.to_numeric(all_data["Price Each"])
print("Numerical Conversion Successful")

##[TASK 6]
##Adding a sales coloumn to  calculate total sales from Quantity Ordered * Price Each
all_data["Total Sales"]=all_data["Quantity Ordered"] * all_data["Price Each"]
print("Sales Calculated successfully")
print(all_data.head(10))

##Question 1:What was the best month for sales?How much we earned in that month?
 results=all_data.groupby('Month').sum()
 print(results)

##Ploting a graph for Question 1
import matplotlib.pyplot as plt
 month=range(1,13)
 plt.bar(month,results['Total Sales'])
 plt.title("Best Month For Sale")
 plt.xticks(month)
 plt.xlabel("Months")
 plt.ylabel("Sales")
 plt.show()

##Additional Funtion to get city from adress
def get_city(adress):
    return adress.split(",")[1].strip()


##QUESTION 2:Which City has the highest sale.
##Adding city Column to data after retriving it from address
all_data["City"]=all_data["Purchase Address"].apply(lambda x:x.split(",")[1]+" "+x.split(",")[2].split(" ")[1])
print(all_data.head())

# high_city=all_data.groupby(all_data["City"]).sum()
# print(high_city)

##Ploting a graph for Question 2
city=[city for city,df in all_data.groupby('City')]
plt.bar(city,high_city["Total Sales"])
plt.title("Highest City in Sales")
plt.xticks(city,rotation='vertical',size=8)
plt.xlabel("City")
plt.ylabel("Sales")
plt.show()

##[TASK 7]
##Question No 3:What time is good to show advtisment ? 
## coloumn to data as hours and minutes extracting from order date
all_data["Order Date"]=pd.to_datetime(all_data["Order Date"])
all_data["Hours"]=all_data["Order Date"].dt.hour
all_data["Minutes"]=all_data["Order Date"].dt.minute
print(all_data.head())

##Ploting a graph for Question 3
hours=[hours for hours,df in all_data.groupby('Hours')]
plt.plot(hours,all_data.groupby("Hours").count())
plt.title("GOOD TIME TO DISPLAY ADVITISMENT")
plt.xticks(hours)
plt.xlabel("Hours")
plt.ylabel("Viewers Count")
plt.grid()
plt.show()

##Question No 4:What products are often sold togeather?
##Grouping all same order id and  joining the products baught
df=all_data[all_data["Order ID"].duplicated(keep=False)]
df["Grouped"]=df.groupby("Order ID")["Product"].transform(lambda x:",".join(x))
print(df.head(10))

##Deleting the duplicates now
df=df[["Order ID","Grouped"]].drop_duplicates()
print(df)

##Checking the most  common product with its count

from itertools import combinations
from collections import Counter

count=Counter()

for row in df["Grouped"]:
     row_list=row.split(",")
    count.update(combinations(row_list,2))

 for key,value in count.most_common(10):
     print(f"{key}: {value}")


##Question 5:Which product sold the most ? why do you think it sold the most?

product_group=all_data.groupby("Product")
quantity_orderd=product_group["Quantity Ordered"].sum()

products=[product for product,df in product_group]

plt.bar(products,quantity_orderd)
plt.title("MOST SOLD PRODUCTS")
plt.xticks(products,rotation="vertical",size=8)


prices = all_data.groupby('Product')['Price Each'].mean()

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_orderd, color='g')
ax2.plot(products, prices, color='b')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(products, rotation='vertical', size=8)

fig.show()
