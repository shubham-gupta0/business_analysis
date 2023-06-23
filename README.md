# business_analysis
The code sample given depicts a data analysis project that focuses on cleaning and prepping a dataset including Amazon product information. Based on the code provided, here is a project description:

The project starts by importing the essential libraries, such as 'numpy', 'pandas', and 'plotly.express'. These libraries are frequently used in Python for numerical computations, data processing, and visualisation.

The code then reads a CSV file named "Amazon-Products.csv" from the 'pandas' library using 'pd.read_csv()'. The dataset is loaded into a DataFrame called 'df'.

To get a sense of the dataset, the code uses 'df.head()' to display the top few rows of the DataFrame. 'df.shape' is also used to get the number of rows and columns in the dataset, giving an idea of its size.

The code then uses 'df.isnull().sum()' to verify the DataFrame for missing values. This aids in the identification of columns with missing data. Columns with 70% or more missing data are decided to be dropped. These columns are removed using the 'df.dropna()' method, and the modified DataFrame is saved in'mod_df'.

The number of columns in the modified DataFrame,'mod_df,' is decreased from 895 to 14, demonstrating a considerable reduction in the dataset's dimensionality.

The code then examines the column names in'mod_df' with'mod_df.columns' and prints the data types and missing values in the remaining columns with'mod_df.info()'.

Following that, the code cleans the data in two columns: "discount_price" and "actual_price." It strips the currency symbol "" and any commas from the values in these columns before converting them to floating-point numbers. This is accomplished by utilising 'pandas' string manipulation techniques such as'str.split()' and'str.replace()'.

The "ratings" column in'mod_df' contains non-numeric data such as text and currency symbols. The code updates these values by replacing certain characters with the value 0.0 and then converts the column to the float data type by calling'mod_df["ratings"].astype(float)'.

The project intends to run additional analysis or modelling activities on the cleaned and preprocessed dataset, which now has fewer missing values, cleaned numeric columns, and changed ratings.

It should be noted that the offered code snippet is only a fraction of the full project. The code does not explicitly state the particular objectives, subsequent analysis, or modelling procedures. To prepare the dataset for subsequent analysis, the code primarily focuses on data preprocessing, cleaning, and handling missing values.
