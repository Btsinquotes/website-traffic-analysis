import pandas as pd
import streamlit as st_module
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Display introductory video
def display_image():
    st_module.image("D://..project//network.jpeg", width=400)
    
# Load dataset
@st_module.cache_data
def load_dataset(file_path):
    df = pd.read_csv(file_path)
    return df

# Display data
def display_data(df):
    st_module.write(df)

# Bar graph
def bargraph(df):
    # Get unique years in the dataset
    years = sorted(df['Year'].unique())
    # Prompt the user to select a year using a combobox
    selected_year = st_module.sidebar.selectbox("Select Year", years)

    # Filter data by selected year
    df_filtered = df[df['Year'] == selected_year]

    # Check if 'Month of the year' column exists in filtered DataFrame
    if 'Month of the year' in df.columns:
        # Check if 'Month of the year' column exists in filtered DataFrame
        if 'Month of the year' in df_filtered.columns:
            # Group by Month and sum Pageviews
            monthly_pageviews = df_filtered.groupby('Month of the year')['Pageviews'].sum().reset_index()

            # Plot bar graph
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Month of the year', y='Pageviews', data=monthly_pageviews, palette="Blues_d")
            plt.title(f'Pageviews by Month in {selected_year}')
            plt.xlabel('Month of the year')
            plt.ylabel('Pageviews')
            st_module.pyplot(plt)
        else:
            st_module.warning(f"The 'Month of the year' column is not present in the dataset for the year {selected_year}.")
    else:
        st_module.warning("The 'Month of the year' column is not present in the dataset.")

# Line graph
def line_graph(df):
    # Get unique years in the dataset
    years = sorted(df['Year'].unique())
    # Prompt the user to select a year using a combobox
    selected_year = st_module.sidebar.selectbox("Select Year", years)

    # Filter data by selected year
    df_filtered = df[df['Year'] == selected_year]

    # Check if 'Month of the year' and 'Avg. Session Duration' columns exist in the filtered DataFrame
    if 'Month of the year' in df.columns and 'Avg. Session Duration' in df.columns:
        # Check if 'Month of the year' and 'Avg. Session Duration' columns exist in the filtered DataFrame
        if 'Month of the year' in df_filtered.columns and 'Avg. Session Duration' in df_filtered.columns:
            # Convert 'Avg. Session Duration' to seconds
            df_filtered['Avg. Session Duration'] = df_filtered['Avg. Session Duration'].apply(lambda x: pd.to_timedelta(x).total_seconds())
            # Group by Month and calculate average session duration
            monthly_avg_session_duration = df_filtered.groupby('Month of the year')['Avg. Session Duration'].mean().reset_index()
            # Convert average session duration back to "hour:min:sec" format for display
            monthly_avg_session_duration['Avg. Session Duration'] = pd.to_timedelta(monthly_avg_session_duration['Avg. Session Duration'], unit='s')
            
            # Plot line graph
            plt.figure(figsize=(10, 6))
            sns.lineplot(x='Month of the year', y='Avg. Session Duration', data=monthly_avg_session_duration, marker='o', color='#3498db')
            plt.title(f'Avg. Session Duration by Month in {selected_year}')
            plt.xlabel('Month of the year')
            plt.ylabel('Avg. Session Duration')
            st_module.pyplot(plt)
        else:
            st_module.warning(f"The 'Month of the year' or 'Avg. Session Duration' column is not present in the dataset for the year {selected_year}.")
    else:
        st_module.warning("The 'Month of the year' or 'Avg. Session Duration' column is not present in the dataset.")

# Correlation
def correlation(df):
    df_chart = df.copy()
    df_chart['Users'] = pd.to_numeric(df_chart['Users'], errors='coerce')
    df_chart['Pageviews'] = pd.to_numeric(df_chart['Pageviews'], errors='coerce')
    df_chart = df_chart.dropna(subset=['Users', 'Pageviews'])

    if not df_chart.empty:
        correlation = df_chart['Users'].corr(df_chart['Pageviews'])
        st_module.write(f"Correlation coefficient: {correlation:.2f}")

        plt.figure(figsize=(8, 6))
        plt.scatter(df_chart['Users'], df_chart['Pageviews'], color='#3498db', alpha=0.7)
        m, b = np.polyfit(df_chart['Users'], df_chart['Pageviews'], 1)
        plt.plot(df_chart['Users'], m*df_chart['Users'] + b, color="#e74c3c")
        plt.xlabel('Users', fontsize=12)
        plt.ylabel('Pageviews', fontsize=12)
        plt.title('Correlation and scatter plot between Users and Pageviews', fontsize=12)
        plt.grid(True, linestyle=' ', alpha=0.7)
        plt.tight_layout()
        st_module.pyplot(plt)
    else:
        st_module.warning("No valid data to display.")

# Boxplot
def display_boxplot(df):
    df['Sessions'] = pd.to_numeric(df['Sessions'], errors='coerce')
    df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')

    df_plot = df.dropna(subset=['Sessions', 'Revenue'])

    if not df_plot.empty:
        plot_data = df_plot[['Sessions', 'Revenue']].copy()

        plt.figure(figsize=(8, 6))
        sns.boxplot(data=plot_data, palette="Set2")
        plt.xlabel('Sessions', fontsize=12)
        plt.ylabel('Revenue', fontsize=12)
        plt.title('Boxplot of Sessions and Revenue', fontsize=14)
        plt.grid(True, linestyle=' ', alpha=0.7)
        plt.tight_layout()
        st_module.pyplot(plt)
    else:
        st_module.warning("No valid data to display.")

# Users Increase
def show_graph(df):
    selected_year = st_module.selectbox("Select Year", sorted(df['Year'].unique()))
    df_filtered = df[df['Year'] == int(selected_year)].copy()

    if not df_filtered.empty:
        df_filtered['Users'] = df_filtered['Users'].str.replace(',', '').astype(int)
        df_filtered['New Users'] = df_filtered['New Users'].str.replace(',', '').astype(int)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        visit_types = ['Users', 'New Users']
        visit_counts = [df_filtered['Users'].sum(), df_filtered['New Users'].sum()]
        ax1.pie(visit_counts, labels=visit_types, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Users vs New Users')

        avg_Users = df_filtered['Users'].mean()
        avg_NewUsers = df_filtered['New Users'].mean()
        ax2.bar(['Users', 'New Users'], [avg_Users, avg_NewUsers], color='#3498db')
        ax2.set_ylabel('Average Users')
        ax2.set_title('Average Users vs New Users')

        plt.tight_layout()
        st_module.pyplot(plt)
    else:
        st_module.warning("No valid data to display for the selected year.")

def main():
    st_module.title("Dataset Explorer")

    display_image()

   # Set the page title using JavaScript
    st_module.markdown("<script>window.document.title='Website traffic analysis';</script>", unsafe_allow_html=True)

    file_path = st_module.file_uploader("Upload CSV", type=["csv"])

    if file_path is not None:
        df = load_dataset(file_path)
        st_module.success("Dataset loaded successfully.")

        analysis_option = st_module.sidebar.selectbox("Select Analysis", ("Display Data", "Bar Graph", "Line Graph", "Correlation", "Boxplot", "Users Increase"))

        if analysis_option == "Display Data":
            display_data(df)
        elif analysis_option == "Bar Graph":
            bargraph(df)
        elif analysis_option == "Line Graph":
            line_graph(df)
        elif analysis_option == "Correlation":
            correlation(df)
        elif analysis_option == "Boxplot":
            display_boxplot(df)
        elif analysis_option == "Users Increase":
            # Move the combobox for selecting year below the analysis dropdown
            st_module.markdown("---")
            st_module.markdown("### Select Year")
            show_graph(df)

if __name__ == "__main__":
    main()
