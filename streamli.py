import pandas as pd
import streamlit as st_module
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Display introductory image
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
    st_module.subheader("Bar Graph")

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
            fig = px.bar(monthly_pageviews, x='Month of the year', y='Pageviews', 
                         title=f'Pageviews by Month in {selected_year}',
                         labels={'Pageviews': 'Pageviews Count'},
                         hover_name='Month of the year',
                         hover_data={'Pageviews': True, 'Month of the year': False},
                         color_discrete_sequence=['#1f77b4'])  # Blue color scheme
            fig.update_layout(xaxis_title='Month of the Year', yaxis_title='Pageviews Count')
            fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.8)  # Marker styling
            fig.update_layout(plot_bgcolor='white', bargap=0.1)  # Background color and bar gap
            fig.update_xaxes(tickangle=-45, tickfont=dict(size=10))  # Rotate x-axis labels for better readability
            fig.update_yaxes(gridcolor='lightgray')  # Gridlines
            st_module.plotly_chart(fig)
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
            fig = px.line(monthly_avg_session_duration, x='Month of the year', y='Avg. Session Duration', title=f'Avg. Session Duration by Month in {selected_year}', markers=True)
            st_module.plotly_chart(fig)
        else:
            st_module.warning(f"The 'Month of the year' or 'Avg. Session Duration' column is not present in the dataset for the year {selected_year}.")
    else:
        st_module.warning("The 'Month of the year' or 'Avg. Session Duration' column is not present in the dataset.")

# Correlation
def display_correlation(df):
    st_module.write("### Correlation Between Parameters")
    # Filter numeric columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    corr_matrix = df[numeric_columns].corr()
    
    fig, ax = plt.subplots()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    st_module.pyplot(fig)


# Boxplot
def display_boxplot(df):
    df['Sessions'] = pd.to_numeric(df['Sessions'], errors='coerce')
    df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')

    df_plot = df.dropna(subset=['Sessions', 'Revenue'])

    if not df_plot.empty:
        fig = px.box(df_plot, y=['Sessions', 'Revenue'], title='Boxplot of Sessions and Revenue')
        st_module.plotly_chart(fig)
    else:
        st_module.warning("No valid data to display.")

# Users Increase
def show_graph(df):
    selected_year = st_module.selectbox("Select Year", sorted(df['Year'].unique()))
    df_filtered = df[df['Year'] == int(selected_year)].copy()

    if not df_filtered.empty:
        df_filtered['Users'] = df_filtered['Users'].str.replace(',', '').astype(int)
        df_filtered['New Users'] = df_filtered['New Users'].str.replace(',', '').astype(int)

        visit_types = ['Users', 'New Users']
        visit_counts = [df_filtered['Users'].sum(), df_filtered['New Users'].sum()]
        fig = go.Figure(data=[go.Pie(labels=visit_types, values=visit_counts, hole=.3)])
        fig.update_layout(title='Users vs New Users')
        
        avg_Users = df_filtered['Users'].mean()
        avg_NewUsers = df_filtered['New Users'].mean()
        fig.add_trace(go.Bar(x=['Users', 'New Users'], y=[avg_Users, avg_NewUsers], name='Average Users'))
        fig.update_layout(title='Average Users vs New Users')
        
        st_module.plotly_chart(fig)
    else:
        st_module.warning("No valid data to display for the selected year.")

def conversion(df):
    st_module.subheader("Conversion Rate Over Time")

    # Get unique years in the dataset
    years = sorted(df['Year'].unique())
    # Prompt the user to select a year using a combobox
    selected_year = st_module.sidebar.selectbox("Select Year", years)

    # Filter data by selected year
    df_filtered = df[df['Year'] == selected_year]

    # Check if 'Month of the year' column exists in the DataFrame
    if 'Month of the year' in df.columns:
        # Calculate conversion rate
        df_filtered["Transactions"] = pd.to_numeric(df_filtered["Transactions"], errors="coerce")
        df_filtered["Sessions"] = pd.to_numeric(df_filtered["Sessions"], errors="coerce")
        df_filtered["Conversion Rate (%)"] = (df_filtered["Transactions"] / df_filtered["Sessions"]) * 100

        # Sort DataFrame by month
        df_filtered = df_filtered.sort_values(by="Month of the year")

        # Plot conversion rate over time
        fig = px.line(df_filtered, x="Month of the year", y="Conversion Rate (%)", 
                      title=f"Conversion Rate Over Time for Year {selected_year}")
        fig.update_layout(xaxis_title='Month of the Year', yaxis_title='Conversion Rate (%)')
        st_module.plotly_chart(fig)
    else:
        st_module.warning("The 'Month of the year' column is not present in the dataset.")

def main():
    st_module.title("Dataset Explorer")

    display_image()

   # Set the page title using JavaScript
    st_module.markdown("<script>window.document.title='Website traffic analysis';</script>", unsafe_allow_html=True)

    file_path = st_module.file_uploader("Upload CSV", type=["csv"])

    if file_path is not None:
        df = load_dataset(file_path)
        site_parameter = st_module.selectbox("Select Site Parameter", df.columns)
        # Ensure that 'site_parameter' is a valid column in the DataFrame
        if site_parameter in df.columns:
            st_module.success("Dataset loaded successfully.")
            analysis_option = st_module.sidebar.selectbox("Select Analysis", ("Display Data", "Bar Graph", "Line Graph", "Correlation", "Boxplot", "Users Increase","Conversion"))
            
            if analysis_option == "Display Data":
                display_data(df)
            elif analysis_option == "Bar Graph":
                bargraph(df)
            elif analysis_option == "Line Graph":
                line_graph(df)
            elif analysis_option == "Correlation":
                display_correlation(df)  # Call the function without any arguments
            elif analysis_option == "Boxplot":
                display_boxplot(df)
            elif analysis_option == "Users Increase":
                # Move the combobox for selecting year below the analysis dropdown
                st_module.markdown("---")
                st_module.markdown("### Select Year")
                show_graph(df)
            elif analysis_option == "Conversion":
                conversion(df)
        else:
            st_module.error(f"Selected site parameter '{site_parameter}' is not present in the dataset.")

if __name__ == "__main__":
    main()
