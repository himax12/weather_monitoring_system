"""
charts.py

Module for visualizing weather data using matplotlib.
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional


def plot_temperature_over_time(
    df: pd.DataFrame,
    city: Optional[str] = None,
    show: bool = False,
    save_path: Optional[str] = None,
    return_fig: bool = False
) -> Optional[plt.Figure]:
    """
    Plot temperature over time for a given city (or all data if city not provided).

    :param df: A Pandas DataFrame containing weather data.
               Expects columns ['timestamp', 'city', 'temperature'] at minimum.
    :param city: The name of the city to filter by. If None, uses all data.
    :param show: If True, displays the plot.
    :param save_path: If provided, saves the plot to the specified file path.
    :param return_fig: If True, returns the Matplotlib Figure object.
    :return: A Matplotlib Figure if return_fig is True; otherwise, None.
    """

    # If a city is specified, filter the DataFrame
    if city:
        df = df[df["city"] == city]

    # Ensure timestamp is a datetime if not already
    if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Sort by timestamp to ensure a proper time series
    df = df.sort_values(by="timestamp")

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot the data
    ax.plot(df["timestamp"], df["temperature"], marker="o", linestyle="-", label="Temperature")

    # Title and labels
    if city:
        ax.set_title(f"Temperature Over Time - {city}")
    else:
        ax.set_title("Temperature Over Time (All Cities)")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    ax.grid(True)

    # Save if a path is provided
    if save_path:
        fig.savefig(save_path, bbox_inches="tight")

    # Show if requested
    if show:
        plt.show()

    if return_fig:
        return fig
    else:
        plt.close(fig)
        return None


def plot_humidity_over_time(
    df: pd.DataFrame,
    city: Optional[str] = None,
    show: bool = False,
    save_path: Optional[str] = None,
    return_fig: bool = False
) -> Optional[plt.Figure]:
    """
    Plot humidity over time for a given city (or all data if city not provided).

    :param df: A Pandas DataFrame containing weather data.
               Expects columns ['timestamp', 'city', 'humidity'] at minimum.
    :param city: The name of the city to filter by. If None, uses all data.
    :param show: If True, displays the plot.
    :param save_path: If provided, saves the plot to the specified file path.
    :param return_fig: If True, returns the Matplotlib Figure object.
    :return: A Matplotlib Figure if return_fig is True; otherwise, None.
    """

    if city:
        df = df[df["city"] == city]

    if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    df = df.sort_values(by="timestamp")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["timestamp"], df["humidity"], marker="o", linestyle="-", label="Humidity", color="orange")

    if city:
        ax.set_title(f"Humidity Over Time - {city}")
    else:
        ax.set_title("Humidity Over Time (All Cities)")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Humidity (%)")
    ax.legend()
    ax.grid(True)

    if save_path:
        fig.savefig(save_path, bbox_inches="tight")

    if show:
        plt.show()

    if return_fig:
        return fig
    else:
        plt.close(fig)
        return None


def plot_temperature_comparison(
    df: pd.DataFrame,
    cities: list,
    show: bool = False,
    save_path: Optional[str] = None,
    return_fig: bool = False
) -> Optional[plt.Figure]:
    """
    Compare temperature over time for multiple cities.

    :param df: A Pandas DataFrame containing weather data.
               Expects columns ['timestamp', 'city', 'temperature'].
    :param cities: A list of city names to compare.
    :param show: If True, displays the plot.
    :param save_path: If provided, saves the plot to the specified file path.
    :param return_fig: If True, returns the Matplotlib Figure object.
    :return: A Matplotlib Figure if return_fig is True; otherwise, None.
    """

    if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    fig, ax = plt.subplots(figsize=(10, 5))

    for city in cities:
        city_df = df[df["city"] == city].sort_values(by="timestamp")
        ax.plot(city_df["timestamp"], city_df["temperature"], marker="o", linestyle="-", label=f"{city} Temp")

    ax.set_title(f"Temperature Comparison: {', '.join(cities)}")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    ax.grid(True)

    if save_path:
        fig.savefig(save_path, bbox_inches="tight")

    if show:
        plt.show()

    if return_fig:
        return fig
    else:
        plt.close(fig)
        return None
