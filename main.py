# main.py

import os
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as pyo

# Ensure offline rendering opens in browser
pyo.init_notebook_mode(connected=True)


def load_and_clean_data(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"❌ Data file not found at: {csv_path}")

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={'atmo_opacity': 'atmospheric_opacity'})
    df['terrestrial_date'] = pd.to_datetime(df['terrestrial_date'], errors='coerce')
    df = df.dropna(subset=['terrestrial_date', 'min_temp', 'max_temp', 'pressure', 'ls'])

    df['season'] = df['ls'].apply(assign_mars_season)
    df['year'] = df['terrestrial_date'].dt.year
    df['day'] = df['terrestrial_date'].dt.strftime('%Y-%m-%d')

    return df


def assign_mars_season(ls):
    if 0 <= ls < 90:
        return 'Spring'
    elif 90 <= ls < 180:
        return 'Summer'
    elif 180 <= ls < 270:
        return 'Autumn'
    elif 270 <= ls < 360:
        return 'Winter'
    else:
        return 'Unknown'


def plot_temperature(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['terrestrial_date'], y=df['min_temp'],
        mode='lines', name='Min Temp (°C)', line=dict(color='skyblue')
    ))
    fig.add_trace(go.Scatter(
        x=df['terrestrial_date'], y=df['max_temp'],
        mode='lines', name='Max Temp (°C)', line=dict(color='orangered')
    ))
    fig.update_layout(
        title='Martian Temperature Range (2012–2018)',
        xaxis_title='Earth Date',
        yaxis_title='Temperature (°C)',
        hovermode='x unified',
        template='plotly_dark'
    )
    pyo.plot(fig, filename='temperature_plot.html')


def plot_pressure(df):
    fig = px.line(
        df, x='terrestrial_date', y='pressure',
        title='Martian Atmospheric Pressure (2012–2018)',
        labels={'pressure': 'Pressure (Pa)', 'terrestrial_date': 'Earth Date'},
        template='plotly_dark'
    )
    fig.update_traces(line=dict(color='limegreen'))
    fig.update_layout(hovermode='x unified')
    pyo.plot(fig, filename='pressure_plot.html')


def plot_opacity(df):
    if 'atmospheric_opacity' in df.columns:
        opacity_counts = df['atmospheric_opacity'].value_counts().reset_index()
        opacity_counts.columns = ['Opacity Type', 'Count']
        fig = px.bar(
            opacity_counts, x='Opacity Type', y='Count',
            title='Atmospheric Opacity Observations on Mars',
            template='plotly_dark',
            color='Opacity Type'
        )
        fig.update_layout(showlegend=False)
        pyo.plot(fig, filename='opacity_plot.html')
    else:
        print("⚠️ No atmospheric_opacity column found.")


def plot_season_comparison(df):
    avg_by_season = df.groupby('season')[['min_temp', 'max_temp', 'pressure']].mean().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Min Temp', x=avg_by_season['season'], y=avg_by_season['min_temp'], marker_color='skyblue'))
    fig.add_trace(go.Bar(name='Max Temp', x=avg_by_season['season'], y=avg_by_season['max_temp'], marker_color='orangered'))
    fig.add_trace(go.Bar(name='Pressure', x=avg_by_season['season'], y=avg_by_season['pressure'], marker_color='limegreen'))

    fig.update_layout(
        title='Average Mars Climate by Season (Based on Solar Longitude)',
        barmode='group',
        xaxis_title='Season',
        yaxis_title='Average Value',
        template='plotly_dark'
    )
    pyo.plot(fig, filename='season_comparison.html')


def plot_animated_temperature(df):
    fig = px.line(
        df, x='day', y='max_temp', animation_frame='year',
        title='Animated Max Temperature on Mars (Yearly)',
        labels={'day': 'Earth Day', 'max_temp': 'Max Temp (°C)'},
        template='plotly_dark'
    )
    fig.update_traces(line=dict(color='tomato'))
    fig.update_layout(xaxis_tickformat='%b %d', xaxis_title='Earth Date', yaxis_title='Max Temp (°C)')
    pyo.plot(fig, filename='animated_temperature.html')


def plot_polar_climate(df):
    df_sorted = df.sort_values('ls')

    # === Polar Plot: Min/Max Temp vs Ls ===
    fig1 = go.Figure()
    fig1.add_trace(go.Scatterpolar(
        r=df_sorted['min_temp'],
        theta=df_sorted['ls'],
        mode='lines',
        name='Min Temp (°C)',
        line=dict(color='skyblue')
    ))
    fig1.add_trace(go.Scatterpolar(
        r=df_sorted['max_temp'],
        theta=df_sorted['ls'],
        mode='lines',
        name='Max Temp (°C)',
        line=dict(color='orangered')
    ))
    fig1.update_layout(
        title='Martian Temperature vs Solar Longitude (Ls)',
        polar=dict(
            angularaxis=dict(direction='clockwise', rotation=90),
            radialaxis=dict(title='Temperature (°C)')
        ),
        template='plotly_dark'
    )
    pyo.plot(fig1, filename='polar_temperature.html')

    # === Polar Plot: Pressure vs Ls ===
    fig2 = go.Figure()
    fig2.add_trace(go.Scatterpolar(
        r=df_sorted['pressure'],
        theta=df_sorted['ls'],
        mode='lines',
        name='Pressure',
        line=dict(color='limegreen')
    ))
    fig2.update_layout(
        title='Martian Pressure vs Solar Longitude (Ls)',
        polar=dict(
            angularaxis=dict(direction='clockwise', rotation=90),
            radialaxis=dict(title='Pressure (Pa)')
        ),
        template='plotly_dark'
    )
    pyo.plot(fig2, filename='polar_pressure.html')


def main():
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "../data/mars-weather.csv")

    try:
        df = load_and_clean_data(csv_path)
        plot_temperature(df)
        plot_pressure(df)
        plot_opacity(df)
        plot_season_comparison(df)
        plot_animated_temperature(df)
        plot_polar_climate(df)
        print("✅ All plots generated including polar plots. Check your HTML files.")
    except Exception as e:
        print(f"🚨 Error: {e}")


if __name__ == "__main__":
    main()
