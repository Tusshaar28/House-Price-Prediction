
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.compose import  make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score,mean_absolute_percentage_error

# loading the file
data = pd.read_csv('mumbaiproject.csv')

# dropping the columns which are not needed
data=data.drop(['zaroni','status','society','transaction'],axis=1)

# extracting size from location
data = data[data['location'].str.contains("Studio|Plot") == False]
data['size'] = data['location'].str[0:2]
data = data[data['size'].str.contains("Ap|>|Ho|Vi") == False]
data['size'] = data['size'].astype(int)

# extracting just the location from column
new = data["location"].str.split("in ", n = 1, expand = True)
data['loc'] = new[1]

data= data.drop(['location'],axis=1)

# converting parking to int
data['parking'] = data['parking'].str[0:2]
data['parking']=data['parking'].fillna(1)
data['parking'] = data['parking'].astype(int)

# converting bath to int
data['bath'] = data['bath'].str[0:2]
data['bath']=data['bath'].fillna(1)
data = data[data['bath'].str.contains(">") == False]
data['bath'] = data['bath'].astype(int)



def convert_price(price):
    try:
        amount, unit = price.split()
        amount = float(amount)
        if unit == 'Cr':
            amount *= 10 ** 7
        elif unit == 'Lac':
            amount *= 10 ** 5
        return int(round(amount))
    except ValueError:
        return None


data['price'] = data['price'].apply(convert_price)
data['price'] = data['price'].fillna(data['price'].mean())
data['price'] = data['price'].astype(int)

new1 = data["total_sqft"].str.split("sq",n=1,expand=True)
data['sqft'] = new1[0]
data['sqft'] = data['sqft'].fillna(data['sqft'].median())
data['sqft'] = data['sqft'].astype(int)

data= data.drop(['total_sqft'],axis=1)

data['furnishing'] = data['furnishing'].fillna('Furnished')



# removing outliers from sqft
sqhigh = data['sqft'].quantile(0.98)
sqlow = data['sqft'].quantile(0.02)
data= data[(data['sqft']>sqlow) & (data['sqft']<sqhigh)]

# removing outliers from parking
parkhigh = data['parking'].quantile(0.99)
data= data[data['parking']<parkhigh]

# removing outliers from bathroom
bathhigh = data['bath'].quantile(0.99)
data= data[data['bath']<bathhigh]

# removing outliers from size
sizehigh = data['size'].quantile(0.999)
data= data[data['size']<sizehigh]

#removing outliers from price
pricehigh = data['price'].quantile(0.98)
pricelow = data['price'].quantile(0.006)
data= data[(data['price']<pricehigh)&(data['price']>pricelow)]

#fitting
X = data.drop(['price'],axis=1)
Y= data['price']

X_train, X_test, y_train,y_test = train_test_split(X,Y,test_size=0.2,random_state=22)
column_transform = make_column_transformer((OneHotEncoder(sparse_output=False),['loc','furnishing']),remainder='passthrough')
scal = StandardScaler()
l = LinearRegression()

# pipelining
pipe = make_pipeline(column_transform,scal,l)
pipe.fit(X_train,y_train)
y_pred = pipe.predict(X_test)

# accuracy
print(r2_score(y_test,y_pred))
print(mean_absolute_percentage_error(y_test,y_pred))


