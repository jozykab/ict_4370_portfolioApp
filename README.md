# ICT 4370 (Python Programming): Portfolio Assignment

    Author: Joseph Kabuika
    Course: ICT 4370: Python Programming
    Term: Summer 2022
    Date: August 21, 2022
    
Project Setup:
    - Python version: This project is compatible with Python 3 version. It was developed and tested with Python 3.9.
    - Project Dependencies: All the project dependencies are maintained in the requirements.txt file. All the dependencies, move to the project root directory and execute the command:
`pip3 install -r requirements.txt` or `pip install -r requirements.txt` depending on how pip is configured.


## Notes:
    - This code requires the Data_Bonds.csv  and Data_Stocks.csv files (
    provided in the assignment instructions) to be in the same repository in order to run
    successfully.
    - Requires AllStocks.json file to run.
    - After running successfully, the code will generate a report file named
    {investor_name}_investment_report.txt
    - The Code will generate the data char file named line_chart.svg

## Troubleshooting Tips:
    If ModuleNotFoundError: No module named '_tkinter': Make sure you install the python-tk or
    python3-tk package

    # Make sure to specify correct Python version.
    # For example, if you run Python v3.9 run adjust command to
    `brew install python-tk@3.9`

    If you are on Windows, you have to make sure to check the optiontcl/tk and IDLE when installing Python.
    If you already installed Python, download the installer, run it and click Modify. Then check the `tcl/tk` and `IDLE` checkbox to install tkinter for your Python version.

