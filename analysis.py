
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

# Load the .joblib model
model = joblib.load('work.joblib')

# Load the preprocessed data
data = pd.read_csv('finaldata.csv')

# Drop the 'Unnamed' column if it exists
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

# Remove 'Mumbai' from the location names
data['loc'] = data['loc'].str.replace('Mumbai', '').str.strip()

#Factor affecting house price: Correlation heatmap
corr_matrix = data.corr()
plt.figure(figsize=(6,6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap of Features')
plt.show()
#
#Comparison of house prices across locations: Bar plot
plt.figure(figsize=(6,6))
avg_prices = data.groupby('loc')['price'].mean().sort_values(ascending=False)
sns.barplot(x=avg_prices.index, y=avg_prices.values)
plt.xticks(rotation=90)
plt.ylabel('Average Price')
plt.title('Average House Prices Across Locations')
plt.show()

#Size vs Price
plt.figure(figsize=(6, 6))
avg_price_by_size = data.groupby('size')['price'].mean().sort_values(ascending=False)
sns.barplot(x=avg_price_by_size.index, y=avg_price_by_size.values, palette='viridis')
plt.title('Average House Price by Size')
plt.xlabel('Size')
plt.ylabel('Average Price')
plt.xticks(rotation=0)
plt.show()


avg_price_by_size_loc = data.groupby(['loc', 'size'])['price'].mean().reset_index()


#Hue Plot Size vs Price for All Loc
plt.figure(figsize=(16, 8))
palette = sns.color_palette("tab10")
sns.barplot(x='size', y='price', hue='loc', data=avg_price_by_size_loc, palette=palette)
plt.title('Average House Price by Size and Location')
plt.xlabel('Size')
plt.ylabel('Average Price')
plt.xticks(rotation=0)
plt.legend(title='Location', bbox_to_anchor=(1.05, 1), loc='upper left')  # Adjust legend position to the right
plt.tight_layout()  # Adjust layout to fit everything
plt.show()