import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Define the file path
DATA_FILENAME = Path(__file__).parent / 'data/synthetic_data.csv'
st.write(f"Looking for file at: {DATA_FILENAME}")
st.write(f"File exists: {DATA_FILENAME.exists()}")

# Load and cache the data
@st.cache_data
def load_data():
    """Load the synthetic data."""
    if DATA_FILENAME.exists():
        synthetic_df = pd.read_csv(DATA_FILENAME)
        return synthetic_df
    else:
        st.error("The data file was not found. Please check the path and ensure the file exists.")
        return None

# Load the data
synthetic_df = load_data()

# Streamlit App
st.title("Data Visualization and Analysis")
st.subheader("Caveat: the visuals are based on synthetic data and for exploratory purposes only. Not meant for circulation or as a basis for conclusion.")

# Continue only if data loaded successfully
if synthetic_df is not None:
    # Filter options based on unique values in the DataFrame
    measure_options = synthetic_df['Measure'].unique()
    group_options = synthetic_df['Group'].unique()
    day_options = synthetic_df['Day'].unique()

    # Sidebar filters
    selected_measure = st.selectbox("Select Measure", measure_options)
    selected_group = st.multiselect("Select Group(s)", group_options, default=group_options)
    selected_day = st.multiselect("Select Day(s)", day_options, default=day_options)

    # Apply the filters to the DataFrame
    filtered_data = synthetic_df[
        (synthetic_df['Measure'] == selected_measure) &
        (synthetic_df['Group'].isin(selected_group)) &
        (synthetic_df['Day'].isin(selected_day))
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