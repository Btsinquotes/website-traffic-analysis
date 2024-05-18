import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Display introductory image
def display_image():
    st.image("D:\..project\ppg.jpeg", width=400)

# Load dataset
@st.cache_data
def load_dataset(file_path):
    df = pd.read_csv(file_path)
    return df

# Display data
def display_data(df):
    st.write(df)

# Refined Pie Chart based on Years
def pie_chart(df, labels_column, values_column):
    st.subheader("Refined Pie Chart based on Years")
    
    # Get unique years from the DataFrame
    years = sorted(df['Year'].unique())

    # Dropdown for selecting year
    selected_year = st.selectbox("Select Year", years)

    # Filter data based on selected year
    filtered_df = df[df['Year'] == selected_year]

    # Plot pie chart
    fig = px.pie(filtered_df, names=labels_column, values=values_column, title=f"Pie Chart of {labels_column} vs {values_column} for {selected_year}")
    st.plotly_chart(fig)

# Updated Line Graph Function with Year Selection
def line_graph(df, x_column, y_column):
    st.subheader("Line Graph")

    # Get unique years from the DataFrame
    years = sorted(df['Year'].unique())

    # Dropdown for selecting year
    selected_year = st.selectbox("Select Year", years)

    # Filter data based on selected year
    filtered_df = df[df['Year'] == selected_year]

    # Try converting non-numeric data to integers
    try:
        filtered_df[y_column] = pd.to_numeric(filtered_df[y_column], errors='coerce', downcast='integer')
    except ValueError:
        st.warning(f"Unable to convert non-numeric data in column '{y_column}' to integers for the selected year.")
        return

    fig = px.line(filtered_df, x=x_column, y=y_column, title=f"Line Graph of {x_column} vs {y_column} for {selected_year}")

    fig.update_layout(
        xaxis_title=x_column,
        yaxis_title=y_column,
        hovermode="x unified",
        dragmode="zoom",
        xaxis=dict(
            rangeslider=dict(
                visible=True
            )
        )
    )

    st.plotly_chart(fig)

# Scatter plot
def scatter_plot(df, x_column, y_column):
    st.subheader("Scatter Plot")
    fig = px.scatter(df, x=x_column, y=y_column)
    st.plotly_chart(fig)

# Correlation
def correlation(df, columns):
    st.subheader("Correlation Plot")
    numeric_df = df[columns].replace(['%', ',', '<0.01'], '', regex=True).replace('', float('nan')).astype(float)
    corr = numeric_df.corr()

    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.index.values,
        y=corr.columns.values,
        colorscale='RdBu',
        colorbar=dict(title='Correlation'),
        hovertemplate='Correlation: %{z:.2f}<extra></extra>',
        text=corr.values.round(2),
        zmin=-1, zmax=1
    ))

    fig.update_layout(
        title='Correlation Heatmap',
        xaxis=dict(title=columns[0]),
        yaxis=dict(title=columns[1]),
        annotations=[dict(x=x, y=y, text=str(corr.iloc[x, y].round(2)),
                          font=dict(color='white' if abs(corr.iloc[x, y]) > 0.5 else 'black'),
                          showarrow=False)
                     for x in range(corr.shape[0]) for y in range(corr.shape[1])],
        height=500, width=700
    )

    st.plotly_chart(fig)

# Boxplot without messages
def boxplot(df, x_column, y_columns):
    st.subheader("Box Plots")

    num_columns = len(y_columns)
    for idx, y_column in enumerate(y_columns):
        st.subheader(f"Box Plot for {y_column}")
        fig = go.Figure()
        fig.add_trace(go.Box(y=df[y_column], name=y_column))
        fig.update_layout(xaxis_title=x_column, yaxis_title=y_column, title=f"Box Plot for {y_column}")
        st.plotly_chart(fig, use_container_width=True)

        if idx < num_columns - 1:
            st.write('<hr style="border:2px solid gray"> ', unsafe_allow_html=True)

def main():
    st.set_page_config(page_title='Website Traffic Analysis')
    st.title("Dataset Explorer")

    display_image()

    file_path = st.file_uploader("Upload CSV", type=["csv"])

    if file_path is not None:
        df = load_dataset(file_path)
        st.success("Dataset loaded successfully.")

        columns = st.multiselect("Select Parameters", df.columns)

        if len(columns) == 2:
            analysis_option = st.selectbox("Select Analysis", ["Display Data", "Pie Chart", "Line Graph", "Scatter Plot", "Correlation", "Boxplot"])

            if analysis_option == "Display Data":
                display_data(df[columns])
            elif analysis_option == "Pie Chart":
                pie_chart(df, columns[0], columns[1])
            elif analysis_option == "Line Graph":
                line_graph(df, columns[0], columns[1])
            elif analysis_option == "Scatter Plot":
                scatter_plot(df, columns[0], columns[1])
            elif analysis_option == "Correlation":
                correlation(df, columns)
            elif analysis_option == "Boxplot":
                boxplot(df, columns[0], columns)
        else:
            st.warning("Please select exactly two parameters for analysis.")

if __name__ == "__main__":
    main()
