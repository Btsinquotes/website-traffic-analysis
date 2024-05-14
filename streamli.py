import pandas as pd
import streamlit as st_module
import plotly.express as px
import plotly.graph_objects as go
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
def bargraph(df, x_column, y_column):
    st_module.subheader("Bar Graph")
    fig = px.bar(df, x=x_column, y=y_column)
    st_module.plotly_chart(fig)

# Line graph
def line_graph(df, x_column, y_column):
    st_module.subheader("Line Graph")
    fig = px.line(df, x=x_column, y=y_column)
    st_module.plotly_chart(fig)

# Scatter plot
def scatter_plot(df, x_column, y_column):
    st_module.subheader("Scatter Plot")
    fig = px.scatter(df, x=x_column, y=y_column)
    st_module.plotly_chart(fig)

# Correlation
def correlation(df, columns):
    st_module.subheader("Correlation Plot")
    numeric_df = df[columns].replace(['%', ',', '<0.01'], '', regex=True).replace('', float('nan')).astype(float)  # Remove '%' and ',' and convert to float
    corr = numeric_df.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.index.values,
        y=corr.columns.values,
        colorscale='RdBu',  # Red for negative correlation, Blue for positive correlation
        colorbar=dict(title='Correlation'),
        hovertemplate='Correlation: %{z:.2f}<extra></extra>',  # Add hover text for correlation values
        text=corr.values.round(2),  # Display correlation values in the cells
        zmin=-1, zmax=1  # Set color scale limits to -1 and 1
    ))
    
    fig.update_layout(
        title='Correlation Heatmap',
        xaxis=dict(title=columns[0]),  # Add axis labels
        yaxis=dict(title=columns[1]),
        annotations=[dict(x=x, y=y, text=str(corr.iloc[x, y].round(2)),
                          font=dict(color='white' if abs(corr.iloc[x, y]) > 0.5 else 'black'),  # Adjust text color based on correlation strength
                          showarrow=False) 
                     for x in range(corr.shape[0]) for y in range(corr.shape[1])],  # Add annotations
        height=500, width=700  # Adjust plot size
    )
    
    st_module.plotly_chart(fig)


# Boxplot
def boxplot(df, x_column, y_column):
    st_module.subheader("Box Plot")
    
    fig = go.Figure()
    fig.add_trace(go.Box(y=df[x_column], name=x_column))
    fig.add_trace(go.Box(y=df[y_column], name=y_column))
    
    fig.update_layout(xaxis_title='Parameter', yaxis_title='Value', title="Box Plots")
    st_module.plotly_chart(fig)

def main():
    st_module.set_page_config(page_title='Website traffic analysis')
    st_module.title("Dataset Explorer")

    display_image()

    file_path = st_module.file_uploader("Upload CSV", type=["csv"])

    if file_path is not None:
        df = load_dataset(file_path)
        st_module.success("Dataset loaded successfully.")
        
        # Select columns for analysis
        columns = st_module.multiselect("Select Parameters", df.columns)

        if len(columns) == 2:
            analysis_option = st_module.selectbox("Select Analysis", ["Display Data", "Bar Graph", "Line Graph", "Scatter Plot", "Correlation", "Boxplot"])

            if analysis_option == "Display Data":
                display_data(df[columns])
            elif analysis_option == "Bar Graph":
                bargraph(df, columns[0], columns[1])
            elif analysis_option == "Line Graph":
                line_graph(df, columns[0], columns[1])
            elif analysis_option == "Scatter Plot":
                scatter_plot(df, columns[0], columns[1])
            elif analysis_option == "Correlation":
                correlation(df, columns)
            elif analysis_option == "Boxplot":
                boxplot(df, columns[0], columns[1])
        else:
            st_module.warning("Please select exactly two parameters for analysis.")

if __name__ == "__main__":
    main()
