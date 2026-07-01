from requests import get
from mysql.connector import connect
import pandas as pd
import csv
from sklearn import tree
import re
from decimal import Decimal
from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Car Predictor")
root.geometry("400x300")


con = connect(
  host="localhost", user="root",
  password="",port="3306", database="test",charset='utf8mb4')
cursor=con.cursor()

for n in range(0,10):
    link='https://bama.ir/cad/api/search?pageIndex=%i&pageSize=12' %n
    r=get(link)
    data = r.json()
    for i in data['data']['ads']:
        if i['type'] != 'ad':
            continue
        name=i['detail']['title']
        year=i['detail']['year']
        price=int(i['price']['price'].replace(',', ''))
        if i['detail']['mileage']=='صفر کیلومتر':
            mile=0
        else:
            mile=int(i['detail']['mileage'].replace(',', '').replace(' km', ''))
        cursor.execute('INSERT INTO cars VALUES(%s,%s,%s,%s)',(name,year,price,mile))

con.commit()
sql_query = pd.read_sql_query('select * from test.cars',con)
con.close()
df = pd.DataFrame(sql_query)
df.to_csv (r'C:/Users/ASUS/Desktop/data.csv', index = False)
x=[]
y=[]

with open('C:/Users/ASUS/Desktop/data.csv','r', encoding='utf-8') as f:
    reader=csv.reader(f)
    n=0
    for line in reader:
      if n!=0:
           x.append(line[0])
           y.append(line[1:])
      n+=1

clf=tree.DecisionTreeClassifier()
clf=clf.fit(y,x)

Label(root,text="Year").pack()
year_entry=Entry(root)
year_entry.pack()

Label(root,text="Price").pack()
price_entry=Entry(root)
price_entry.pack()

Label(root,text="Mileage").pack()
mile_entry=Entry(root)
mile_entry.pack()

def predict():
    nyear=float(year_entry.get())
    nprice=float(price_entry.get())
    nmile=float(mile_entry.get())

    new=[[nyear,nprice,nmile]]

    j=clf.predict(new)

    car = j[0]
    info = df[df['name'] == car].iloc[0]
    ryear = int(info['year'])
    rprice = int(info['price'])
    rmile = int(info['mile'])

    text = (
    f"خودروی پیشنهادی:\n{car}\n\n"
    f"سال حدودی: {ryear}\n"
    f"قیمت حدودی: {rprice:,}\n"
    f"کارکرد حدودی: {rmile:,}\n\n"
    f"پیشنهاد ما به شما طبق آگهی‌های اخیر سایت باما می‌باشد!")

    result_label.config(text=text)

Button(root,text="Predict",command=predict).pack(pady=10)

result_label=Label(root,text="")
result_label.pack()

root.mainloop()