# -*- coding: utf-8 -*-
"""AIML_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X9dNLuJNexKtoAh5xMGoZmJ-wUcFg-Qj
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import plotly.express as px

path ="/content/AmazonProducts.csv"
df = pd.read_csv(path, low_memory=False)
df.head()

# Knowing the number of rows and columns
df.shape

# Checking the missing values
df.isnull().sum()

# Droping the columns with 70% or more missing data
perc = 70.0
min_count =  int(((100 - perc)/100) * df.shape[1] + 1)
mod_df = df.dropna(axis = 1, thresh = min_count)

# Number of columns are reduced significantly from 895 to 14
mod_df.shape

# Checking the column name
mod_df.columns

# Checking the data type, missing values in remaining columns
mod_df.info()

"""## **📂 Clean numeric columns and set data types**
The columns actual_price, discount_price, no_of_ratings and ratings have wrong datatype. The datatype given is object but we want them to be int or float. Let us correct it.
The column amazon_category_and_sub_category has multiple values. In order to clean the data we will seperate them to individual columns.
"""

# Removing the ₹ sign
mod_df["discount_price"] = mod_df["discount_price"].str.split(" ", expand = True).get(0).str.split("₹", expand = True).get(1)
mod_df["actual_price"] = mod_df["actual_price"].str.split(" ", expand = True).get(0).str.split("₹", expand = True).get(1)

# Change commas to dots and change the type to float
mod_df['discount_price'] = mod_df["discount_price"].str.replace(',', '').astype(float)
mod_df["actual_price"] = mod_df["actual_price"].str.replace(',', '').astype(float)

"""There are values in the 'ratings' column that cannot be represented as a number. We replace them with '0.0'"""

# Modify ratings values
mod_df['ratings'].unique()

# Extract the digits and change the type to float
mod_df['ratings'] = mod_df['ratings'].replace(['Get','FREE'], '0.0')
mod_df['ratings'] = mod_df["ratings"].astype(float)
mod_df['ratings'].unique()

"""### **➡️ Preprocess Rating column**
The 'no_of_ratings' column is converted to the float type in two steps: first, a new boolean column is formed, where the True value corresponds to the numeric value in the original column. Then the values ​​in the 'no_of_ratings' column are recalculated for values ​​matching the True of the 'correct_no_of_ratings' column
"""

# Add column 'correct_no_of_ratings' which value is 'True' if 'no_of_ratings' begins from digit
mod_df['no_of_ratings'] = mod_df['no_of_ratings'].astype(str)
mod_df['correct_no_of_ratings'] = pd.Series([mod_df['no_of_ratings'][x][0].isdigit() for x in range(len(mod_df['no_of_ratings']))])
# Drop columns with incorrect 'no_of_ratings'
mod_df = mod_df[mod_df['correct_no_of_ratings'] == True]
mod_df['correct_no_of_ratings'].value_counts()

# Change the type to float
mod_df["no_of_ratings"] = mod_df["no_of_ratings"].str.replace(',', '').astype(float)

# Dataframe after first phase of cleaning
mod_df.head()

mod_df.info()

# Plot the total missing values
x = mod_df.isnull().sum()

fig = px.bar(x, orientation = "h",  text_auto='.2s',
            color_discrete_sequence= ["#ff6b00"] * len(x))
fig.update_layout(
    title="<b>Missing Value Count</b>",
    xaxis_title="Total missing values",
    yaxis_title="Column Names",
    plot_bgcolor = "#ECECEC",
    showlegend=False
)
fig.show()

"""### **🗄️ EDA**
Now let us imagine we are browsing the Amazon website. What are the things that you see when you click on a product. For me the priority order is as follows:

1. Price
2. Rating
3. Manufacturer
4. Description
5. Customer reviews

Let us see analyze the given dataframe on following points.
"""

# Let us check and create a dataframe of missing ratings
missing_no_of_ratings = mod_df[mod_df['actual_price'].isnull()]

missing_no_of_ratings.head(2)

# Since our further analysis is based on the price column so let us drop it.
df = mod_df.dropna(subset=['actual_price','discount_price'])
df.head()

"""### **➡️ Extract the manufacturer from the 'name' column**
Extract the manufacturer from the 'name' column and insert the 'manufacturer' column after the 'name' column. To do this, we convert the 'name' column (type 'Series') into a string, split by spaces and select the first substring. We will have some incorrect names (such as 'The', 'Van', etc.) for brands which names consists of more than one word. But for many others it is okay. And I think this is enought to obtain general understanding for our purposes
"""

df['manufacturer'] = df['name'].str.split(' ').str[0]
cols = df.columns.tolist()
cols

cols = ['name',
 'manufacturer',
 'main_category',
 'sub_category',
 'image',
 'link',
 'ratings',
 'no_of_ratings',
 'discount_price',
 'actual_price']

df = df[cols]
df.head()

df.info()

# Make column with discount net value and discounting percent
df['discount_value'] = df['actual_price'] - df['discount_price']
df['discounting_percent'] = (1 - df['discount_price']/df['actual_price'])

df.head()

# Let us check the manufactures according to their prices
df[["actual_price", 'manufacturer']].groupby("manufacturer").mean().round(2).sort_values(by = "actual_price",
                                                                    ascending = False)

# Detail of the maximum price row
df[df["actual_price"] == df["actual_price"].max()]

# Detail of the minimum price row
df[df["discount_value"] == df["discount_value"].min()]

# Let us check the common manufacture
values = df["manufacturer"].value_counts().keys().tolist()[:10]
counts = df["manufacturer"].value_counts().tolist()[:10]

fig = px.bar(df, y = counts, x = values,
            color_discrete_sequence = ["#EC2781"] * len(df))


fig.update_layout(
                 plot_bgcolor = "#ECECEC",
                  yaxis_title = "Count",
                xaxis_title = "Name of Manufacturers",
                  title = "<b>Popular Manufacturers Category</b>"
                 )
fig.show()

"""### **✔️ Insight 1**
From above graph we see that the Havells is most popular. Let us check the main category for the above top 10 brands
"""

# Creating the dataframe of top 10 manufacturer
df_list = []
for i in values:
    x = df[df["manufacturer"] == i]
    df_list.append(x)
frame = pd.concat(df_list)
frame.head(2)

# Average rating of the manufactures
frame[["manufacturer", "ratings"]].groupby("manufacturer").mean().sort_values(by = "ratings",
                                                ascending = False)

"""### **✔️ Insight 2**
Even though the most popular brand is Havells but the highest rated is Panasonic.
Also the manufacturer Samsung is second most favourite in the popular manufacturer category. On the other hand AGARO is second in terms of average rating
Let us now check the popular main category items present.
"""

# Different main categories present
frame["main_category"].unique()

fig = px.bar(frame, "main_category",
             color_discrete_sequence = ["#2377a4"] * len(frame))
fig.update_layout(
                 plot_bgcolor = "#ECECEC",
                  yaxis_title = "Count",
                  xaxis_title = "Main Categories",
                  title = "<b>Count of Main Categories of Products</b>"
                 )
fig.show()

"""### **✔️ Insight 3**
From the graph we see that 'Man's cloothing' is the popular main category. Let us select the top 10 popular main category. We are narrowing our selction to reach the goal
"""

# Let us select the 5 popular main categories

value_main = frame["main_category"].value_counts().keys().tolist()[:5]
count_main = frame["main_category"].value_counts().tolist()[:5]
value_main

"""Let us create a new dataframe having top 10 popular manufcturers and 5 most popular main category"""

df_list = []
for i in value_main:
    x = frame[frame["main_category"] == i]
    df_list.append(x)
    #print(df)
frame = pd.concat(df_list)
frame.head(2)

# Let us check the popular subcategory
import seaborn as sns
cm = sns.light_palette("green", as_cmap=True)
frame_sub = frame[["main_category", "sub_category"]].groupby("main_category").count()
frame_sub.style.background_gradient(cmap=cm)

value_sub = frame["sub_category"].value_counts().keys().tolist()[:10]
count_sub = frame["sub_category"].value_counts().tolist()[:10]

# New dataframe with selected sub_category
df_list = []
for i in value_sub:
    x = frame[frame["sub_category"] == i]
    df_list.append(x)
frame = pd.concat(df_list)
frame.head(2)

"""Now we have completed the second phase of data preprocessing. After this we have achieved a dataframe with following characterstics:

1. No null price.
2. Top 10 manufacturers with respect to count
3. Popular top 5 main categories, 10 sub_category

Let us now check the average rating and price for this selected dataframe.
"""

# Rating of the products
print("The average rating: ",frame["ratings"].unique())

# After processing our data we have significantly reduced the size of the dataframe.
# Also the rating are now 4 or greater.
# Let us now check new average price ### check above before processing to compare.
print("The average price: ", frame["actual_price"].mean())

import plotly.figure_factory as ff
x = frame["actual_price"]
hist_data = [x]
group_labels = ['actual_price']

fig = ff.create_distplot(hist_data, group_labels, show_rug = False,
                        colors=["#ffd514"])
fig.update_layout(
                 plot_bgcolor = "#ECECEC",
                  title = "<b>Price Distribution of Data</b>"
                 )

fig.show()

"""### **✔️ Insight 4**
We see that the plot is right skew plot with the presence of outliers. Let us see these outliers
"""

# Check the statistics of the price_new column
frame.actual_price.describe()

# plot the quartiles and check for outliers
fig = px.box(frame, "actual_price")
fig.update_layout(
                 plot_bgcolor = "#ECECEC",
                  title = "<b>Price Data Distribution</b>",
                 xaxis_title = "Price of Products"
                 )
fig.show()

# Let us find the outliers
Q1 = 1399
Q2 = 2199
Q3 = 3599
IQR = Q3 - Q1
outlier1 = (Q1 - 1.5 * IQR)
outlier2 = (Q3 + 1.5 * IQR)
print("outlier1: ", outlier1)
print("outlier2: ", outlier2)

outlier_price = []

for i in frame.actual_price:
    if i < outlier1 or i > outlier2:
        outlier_price.append("outlier")
    elif i > outlier1 or i < outlier2:
        outlier_price.append("normal")

frame["outlier_price"] = outlier_price

fig = px.pie(frame, names = frame["outlier_price"], color = frame["outlier_price"],
             color_discrete_map={'normal': '#2377a4', 'outlier': '#ffd514'})

fig.update_layout(title = "<b>Distribution of Outlier</b>")

fig.show()

# Let us see the outlier value
frame_outlier = frame.loc[frame["outlier_price"] == "outlier"].head()
frame_outlier

print("Manufacturers with outlier price: ", frame_outlier.manufacturer.value_counts())

# Top category
print("Main category with outliers: ", frame_outlier.main_category.value_counts())

print("Sub_category with outliers: ",frame_outlier.sub_category.value_counts())

# Let us check the rating of the products
fig = px.violin(frame, "ratings",
               color_discrete_sequence = ["#FFBF00"] * len(frame))
fig.update_layout(
                 plot_bgcolor = "#ECECEC",
                  xaxis_title = "Rating",
                  title = "<b>Rating Distribution of the Popular Products</b>"
                 )
fig.show()

"""### **✔️ Insight 5**
As expected our selected category of products have the most common rating as 4 and 5. It also seems that our selection of top manufacturer, categories have resulted in dataframe having a very few 1, 2 and 3 ratings. Now let us check the customer reviews
"""

fig = px.histogram(frame, "no_of_ratings",
                  color_discrete_sequence = ["#8B4000"] * len(frame))
fig.update_xaxes(range=[10, 5000])
fig.update_yaxes(range=[0, 2000])
fig.update_layout(
                 plot_bgcolor = "#ECECEC",
                  xaxis_title = "Number of Reviews",
                  title = "<b>Number of Reviews Distribution</b>"
                 )
fig.show()

"""### **✔️ Insight 6**
We see that 10k+ products has less than 49 reviews, 1.5k products has less than 99 reviews. After 1k reviews we see outliers, possibly with fake reviews.
"""

# Let us check if there are any null review
print("Number of null values: ",frame['no_of_ratings'].isnull().sum())
# It seems that with high end products people love to leave a review

frame.head(2)

frame['no_of_ratings']

fig = px.scatter(frame, x="discounting_percent", y="no_of_ratings",
                 trendline="ols")
fig.update_yaxes(range=[0, 1000])
fig.update_layout(title = "<b>Relationship between the number of reviews and discount percent</b>",
                 plot_bgcolor = "#ECECEC",
                 yaxis_title = "Number of reviews",
                 xaxis_title = "Discount percent")

fig.show()

"""### **✔️ Insight 7**
We see slightly decreasing number of reviews with increasing of discount percent.
"""

fig = px.histogram(frame, "discounting_percent",
                  color_discrete_sequence = ["#C04000"] * len(frame))
fig.update_layout(
                 plot_bgcolor = "#ECECEC",
                  xaxis_title = "Discounting Percent",
                  title = "<b>Number of products with different discount percent</b>"
                 )
fig.show()

"""### **💡 Conclusion**
From above analysis of the selected frame of popular categories we arrive at following conclusions:

1. The products with price less than ₹3600 are popular.
2. The outlier in price data are around 5.32%
3. Havells and V-Guard are the most popular manufactures with outlier price
4. Character and brand is the subcatogory with outlier price
5. The maximum number rating of popular brands is in range of 4 star
6. Mostly 0-49 review were given on the products
7. Every product has a review in selected dataframe
8. Distribution of products by discount percent shows distribution similar to normal with slight rigth skew and spikes at each value multiple of ten We can analyse at other relationship as well but for now the above is the conclusion.
"""