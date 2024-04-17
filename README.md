# Expense Stream

## Overview

`expenses-stream` is a Streamlit app designed to automate the categorization of monthly expenses from Excel files. It processes transaction records, including company names, dates, and amounts, and categorizes each expense based on predefined keywords. The script handles Turkish-specific case conversions for accurate categorization and includes visualization through pie charts to represent the distribution of expenses across different categories. This tool is particularly useful for individuals looking to gain insights into their spending patterns and manage their finances more effectively.

<img width="598" alt="Screenshot 2024-04-18 at 01 46 36" src="https://github.com/sedyldz/expense-stream/assets/41821819/0bd960ab-aa17-4335-9e73-a18231ae9562">


## Features

- **Turkish Case Conversion**: Custom function to accurately match Turkish characters during the categorization process.
- **Automated Categorization**: Expenses are automatically categorized based on a pre-defined list of Turkish keywords.
- **Visualization**: Generates pie charts to visually display the distribution of spending across categories.
- **Excel and CSV Support**: Processes Excel files and outputs categorized expenses into CSV files for easy analysis.
