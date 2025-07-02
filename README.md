# 🚀 Mars Climate Visualizer

This project is a visual data exploration of real Martian climate using historical data collected by NASA’s Mars rover missions from 2012 to 2018. It uses Python and Plotly to generate interactive plots that reveal how temperature, atmospheric pressure, and dust opacity on Mars vary over time and seasons.

The core script `main.py` loads a cleaned dataset (`mars-weather.csv`) and generates a series of stunning visualizations:
- **Temperature Range**: Line plot showing daily minimum and maximum temperatures on Mars.
- **Atmospheric Pressure**: Trend of surface pressure over time.
- **Atmospheric Opacity**: Distribution of dust and sky clarity (e.g., 'Sunny', 'Cloudy', 'Very Dusty').
- **Seasonal Averages**: Grouped bar charts comparing climate variables across Martian seasons.
- **Animated Temperature**: A year-wise animation of maximum temperatures for visualizing heat trends.
- **Polar Plots**: Circular charts of temperature and pressure plotted against Mars’ solar longitude (Ls), representing its orbit and seasons.

All plots are saved as interactive HTML files, ready to be opened in any browser.

### Technologies Used
- Python 3
- pandas, numpy
- plotly (offline mode)
- Real Martian data from publicly available rover logs (CSV format)

### How to Run
1. Place your `mars-weather.csv` file in the `data/` folder.
2. Install dependencies:  
   `pip install pandas numpy plotly`
3. Run the script:  
   `python main.py`

You’ll get a bunch of `.html` files like `temperature_plot.html`, `pressure_plot.html`, etc., ready to explore.

### About
Built by **Sayed Umair Ali**, a freelance technologist and space enthusiast, for learning and showcasing Martian data science in a visual and intuitive way. No AI used in data — just pure science and Python.

