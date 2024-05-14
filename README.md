# website-traffic-analysis
checking the traffic of different means of data from different parameters from the dataset

you can run in command prompt as
streamlit run D://..project//streamli.py [ARGUMENTS]

With these modifications:

We adjusted the colorscale to use red for negative correlation, blue for positive correlation, which is more intuitive.
Text annotations directly indicate the correlation values in each cell of the heatmap.
The color of the text adjusts based on the strength of the correlation: white for strong correlations (|r| > 0.5) and black for weaker correlations.
These changes should provide a more user-friendly and informative correlation plot.
