# Symphony

Symphony is an Automated Chart Generator Powered by MindsDB and Streamlit

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Introduction

Symphony is an open-source data visualization tool that streamlines the creation of charts and graphs from raw data. It provides intelligent chart type recommendations based on data characteristics, aiding users in crafting effective visualization.

## Features

- Line Charts: Ideal for time-series data, showcasing trends and changes.
- Bar Charts: Efficient for comparing categorical data and data distribution.
- Area Charts: Perfect for cumulative trends and accumulation patterns.
- Pie Charts: Useful for displaying percentage distribution in parts of a whole.
- Scatter Plots: Revealing relationships and correlations between numerical variables.
- Heatmaps: Effective for dense data visualization and matrix-format relationships.

## Getting Started

### Prerequisites

- Python (>=3.9)
- OpenAI API Key

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/adeyinkaezra123/symphony.git
   cd symphony
   ```

2. Install the required dependencies:

    ```bash
      pip install -r requirements.txt
    ```

### Usage

0. Create a new MindsDB Model. Example [here](https://docs.mindsdb.com/integrations/ai-engines/langchain#ai-model)
1. Run the Streamlit app:

    ```bash
      streamlit run app.py
    ```
    Or go to use the [webapp](https://symphony.streamlit.app/)

2. Enter your OpenAI API key in the provided input field.
3. Upload your dataset in CSV format.

### Configuration
To configure the output of the Chart generator, you can modify the following settings in the mindsdb.py file:
1. `temperature`: Adjust the temperature parameter for OpenAI model responses.
2. `model_name`: Choose the desired OpenAI model variant.

