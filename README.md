# Data Analysis Toolkit

Welcome to the Data Analysis Toolkit repository! This toolkit provides a set of Python scripts for data analysis, preprocessing, visualization, and reporting.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
  - [Programmatic Usage](#programmatic-usage)
  - [Command-Line Interface (CLI)](#command-line-interface-cli)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This toolkit contains various scripts for performing data analysis tasks. It includes functions for downloading datasets, preprocessing data, analyzing statistics, generating exploratory data analysis (EDA) visualizations, creating summary PDF reports, and more. Whether you're a data analyst or a data scientist, this toolkit can help streamline your data analysis workflow.

## Installation
1. Clone this repository to your local machine:

2. Install the required dependencies. You can use a virtual environment to manage dependencies:
## Requirements
To ensure that you have the necessary dependencies for this project, you can use the provided `environment.yml` file. This file contains a list of packages and their versions required to run the toolkit. You can install them using the following command within your activated virtual environment:

`conda env create -f environment.yml`

## Usage
The toolkit offers both programmatic usage and a Command-Line Interface (CLI) for generating reports and visualizations.
- [data_downloader.py](data_downloader.py): Contains functions for downloading datasets using Kaggle API.
- [data_analyzer.py](data_analyzer.py): Provides data analysis and preprocessing methods.
- [report_generator.py](report_generator.py): Generates PDF reports summarizing analysis results.
- [helper.py](helper.py): Helper functions for various tasks.
- [example_test.ipynb](example_test.ipynb): notebook for demonstration on example.



### Programmatic Usage
The toolkit provides various Python scripts for data analysis, preprocessing, visualization, and reporting. You can import these scripts and utilize their functions in your own data analysis projects.

### Command-Line Interface (CLI)
The CLI allows you to interactively generate reports and visualizations based on user input. Here's how you can use it:

1. Navigate to the `data-analysis-toolkit` directory.
2. Run the CLI script using the following command:
3. Follow the prompts to:
- Choose a custom dataset or use the example dataset.
- Select the type of report to generate (PDF visualization, PDF summary, or both).

The toolkit will generate the selected reports and visualizations and provide feedback about the process.

## Features
- Download datasets from Kaggle using the Kaggle API.
- Analyze data statistics, duplicates, null values, and outliers.
- Generate exploratory data analysis (EDA) visualizations.
- Generate detailed PDF reports summarizing analysis results.
- Encapsulate data analysis functionalities into easy-to-use classes.
- Interact with the toolkit using the Command-Line Interface (CLI).

## Contributing
Contributions are welcome! If you find a bug or have an idea for an enhancement, feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Create a pull request.

