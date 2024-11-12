import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv('/workspaces/synthetic_data_tab3_4/data/synthetic_data.csv')

# Streamlit App
st.title("Data Visualization and Analysis")
st.subheader("Caveat: the visuals are based on synthetic data and for exploratory purpose. Not meant for circulation or as a basis for conclusion.")

# Filter options based on unique values in the DataFrame
measure_options = data['Measure'].unique()
group_options = data['Group'].unique()
day_options = data['Day'].unique()

# Sidebar filters
selected_measure = st.selectbox("Select Measure", measure_options)
selected_group = st.multiselect("Select Group(s)", group_options, default=group_options)
selected_day = st.multiselect("Select Day(s)", day_options, default=day_options)

# Apply the filters to the DataFrame
filtered_data = data[
    (data['Measure'] == selected_measure) &
    (data['Group'].isin(selected_group)) &
    (data['Day'].isin(selected_day))
]

# Check if there's data to display after filtering
if not filtered_data.empty:
    # Create a violin plot showing the distribution by day and group
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Only use split=True if exactly two groups are selected
    if len(selected_group) == 2:
        sns.violinplot(data=filtered_data, x='Day', y='Value', hue='Group', split=True, ax=ax)
    else:
        sns.violinplot(data=filtered_data, x='Day', y='Value', hue='Group', ax=ax)

    # Add titles and labels
    ax.set_title(f'Distribution of {selected_measure} Values by Day and Group')
    ax.set_xlabel('Day')
    ax.set_ylabel(f'{selected_measure} Value')

    # Show the plot in Streamlit
    st.pyplot(fig)
else:
    st.write("No data available for the selected filters.")