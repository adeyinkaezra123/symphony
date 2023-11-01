import pandas as pd
import numpy as np


def generate_sample_data():
    # Generating sample data
    num_points = 100  # Number of data points
    # Time values from 0 to 10 seconds
    time_values = np.linspace(0, 10, num_points)
    amplitude = 5  # Maximum voltage amplitude in volts
    frequency = 1  # Frequency of the sinusoidal function in Hz
    phase = 0      # Phase shift of the sinusoidal function in radians

    # Generating voltage values using a sinusoidal function
    voltage_values = amplitude * \
        np.sin(2 * np.pi * frequency * time_values + phase)

    # Creating the dataframe
    data_continuous_voltage = {
        'Time': time_values,
        'Voltage': voltage_values
    }

    df_continuous_voltage = pd.DataFrame(data_continuous_voltage)
    df_continuous_voltage.to_csv('continuous_voltage_data.csv', index=False)

    data_regional_sales = {
        'Region': ['North', 'South', 'East', 'West', 'Center', 'Oversea', 'Others'],
        'Products Sold': [300, 250, 200, 350, 490, 220, 120]
    }

    df_regional_sales = pd.DataFrame(data_regional_sales)
    df_regional_sales.to_csv('regional_sales_data.csv', index=False)

    data_monthly_status = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Visits': [500, 600, 800, 700, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600],
        'Page Views': [1200, 1500, 1800, 1700, 2100, 2400, 2500, 2800, 3000, 3200, 3500, 3700],
        'Unique Visitors': [300, 350, 400, 380, 420, 460, 480, 500, 550, 580, 600, 620]
    }

    df_monthly_status = pd.DataFrame(data_monthly_status)
    df_monthly_status.to_csv('monthly_status_data.csv', index=False)


generate_sample_data()