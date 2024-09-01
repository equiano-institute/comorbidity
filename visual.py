import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Read JSON data from a local file
with open('main_data.json', 'r') as file:
    data = json.load(file)

# Flatten the dataset and create a DataFrame
flat_data = []
for entry in data:
    conditions = entry.pop('conditions')
    entry.update(conditions)
    flat_data.append(entry)

df = pd.DataFrame(flat_data)

# Set up the visualizations
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Age distribution
sns.histplot(df['age'], bins=10, kde=True, ax=axs[0, 0])
axs[0, 0].set_title('Age Distribution')
axs[0, 0].set_xlabel('Age')
axs[0, 0].set_ylabel('Count')

# Gender distribution
sns.countplot(x='gender', data=df, ax=axs[0, 1])
axs[0, 1].set_title('Gender Distribution')
axs[0, 1].set_xlabel('Gender')
axs[0, 1].set_ylabel('Count')

# Race distribution
sns.countplot(x='race', data=df, ax=axs[1, 0])
axs[1, 0].set_title('Race Distribution')
axs[1, 0].set_xlabel('Race')
axs[1, 0].set_ylabel('Count')

# Medical conditions frequency
conditions = df[['diabetes', 'hypertension', 'COPD', 'heart_disease', 'arthritis']]
conditions_sum = conditions.sum().reset_index()
conditions_sum.columns = ['condition', 'count']
sns.barplot(x='condition', y='count', data=conditions_sum, ax=axs[1, 1])
axs[1, 1].set_title('Medical Conditions Frequency')
axs[1, 1].set_xlabel('Condition')
axs[1, 1].set_ylabel('Count')

plt.tight_layout()
plt.show()
