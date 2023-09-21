import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['overweight'] = 0
for index, row in df.iterrows():
    weight_kg = row['weight']
    height_m = row['height'] / 100
    bmi = weight_kg / (height_m ** 2)
    if bmi > 25:
        df.at[index, 'overweight'] = 1

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
glu_chl_map = {1:0, 2:1, 3:1}
df['gluc'] = df['gluc'].replace(glu_chl_map)
df['cholesterol'] = df['cholesterol'].replace(glu_chl_map)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, 
                     id_vars=['cardio'],
                     value_vars=['cholesterol','gluc','smoke','alco','active','overweight'])
    
  
    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = pd.melt(df, id_vars=['cardio'],
                     value_vars=['active', 'alco', 'cholesterol','gluc','overweight', 'smoke'], 
                     value_name='total')
    

    # Draw the catplot with 'sns.catplot()'



    # Get the figure for the output
    fig = sns.catplot(data = df_cat,
                      kind='count',
                      x='variable',
                      hue='total', 
                      col='cardio')

    fig.set_xlabels('variable')
    fig.set_ylabels('total')
    fig = fig.fig
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df["ap_lo"] <= df["ap_hi"])
                 & (df["height"] >= df["height"].quantile(0.025))
                 & (df["height"] <= df["height"].quantile(0.975))
                 & (df["weight"] >= df["weight"].quantile(0.025))
                 & (df["weight"] <= df["weight"].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)



    # Set up the matplotlib figure
    fig = plt.figure()
    fig.set_size_inches(9, 9)
    sns.heatmap(corr,
              mask=mask,
              fmt=".1f",
              annot=True,
              square=True)


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
