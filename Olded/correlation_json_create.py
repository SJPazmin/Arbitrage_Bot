import pandas as pd
import json
import ast

# Load the CSV data
data = pd.read_csv('correlation_results.csv')

# Display the first few rows of the dataframe
print(data.head())

# Calculate the percentage of highly correlated windows
data['Correlation Percentage'] = data['Highly Correlated Windows'] / \
    data['Total Windows']

# Sort the dataframe by the 'Correlation Percentage' in descending order
data_sorted = data.sort_values('Correlation Percentage', ascending=False)

# Display the sorted dataframe
print(data_sorted)

# Extract the pairs with correlation percentage greater than 0.5
pairs = data_sorted[data_sorted['Correlation Percentage']
                    > 0.5]['Pair'].tolist()

# Convert strings to lists
pairs = [ast.literal_eval(pair) for pair in pairs]

print(pairs)

# Save the pairs to a json file named 'pairs_corr.json'
with open('pairs_corr.json', 'w') as file:
    # Convert the list of pairs to a json string and write it to the file
    json.dump(pairs, file)
