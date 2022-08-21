"""
    Name: Joseph Kabuika
    Course: ICT 4370: Python Programming
    Term: Summer 2022
    Date: August 21, 2022
    Assignment: WEEK 10 Portfolio Assignment

    Notes:
    - This code requires the Data_Bonds.csv  and Data_Stocks.csv files (
    provided in the assignment instructions) to be in the same repository in order to run
    successfully.
    - Requires AllStocks.json file to run.
    - After running successfully, the code will generate a report file named
    {investor_name}_investment_report.txt
    - The Code will generate the data char file named line_chart.svg

    🚨 🚨 🚨
    If ModuleNotFoundError: No module named '_tkinter' => Make sure you install the python-tk or
    python3-tk package

    # Make sure to specify correct Python version.
    # For example, if you run Python v3.9 run adjust command to
    brew install python-tk@3.9

    If you are on Windows, you have to make sure to check the optiontcl/tk and IDLE when installing Python.
    If you already installed Python, download the installer, run it and click Modify. Then check the tcl/tk and IDLE checkbox to install tkinter for your Python version.

"""
import datetime
import json
import uuid
import csv
from tkinter.ttk import Treeview

import pygal
from tabulate import tabulate

from tkinter import *

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

from PIL import ImageTk, Image as PIL_image
from io import BytesIO

date_format = '%m/%d/%Y'
bond_data = []
stock_data = []
root = Tk()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))
root.title("Welcome to the Portfolio Visualization App!")


def show_graph():
    print('Displaying graph...')
    file = open_file("line_chart.svg")
    svg_content = file.read()
    file.close()

    drawing = svg2rlg(path=BytesIO(bytes(svg_content, 'utf-8')))
    out = BytesIO()
    renderPM.drawToFile(drawing, out, fmt="PNG")

    img = PIL_image.open(out)
    pimg = ImageTk.PhotoImage(img)
    size = img.size

    frame = Canvas(root, width=size[0], height=size[1])

    frame.grid(column=0, row=3, sticky=W, padx=5, pady=5)
    frame.create_image(0, 0, anchor='nw', image=pimg)


def show_report():
    print('Displaying report data...')
    text = Label(root, font=('Helvetica', 12), justify=CENTER, text=report)
    # text.place(x=70, y=90)
    text.grid(column=1, row=3, sticky=W, padx=5, pady=5)


def show_bonds_data():
    print('Displaying bonds data...')

    bond_reporting_frame = Frame(root)
    bond_reporting_frame.grid(column=0, row=5, sticky=W, padx=5, pady=5)
    bond_report_data = Treeview(root)

    bond_report_data['columns'] = (
        'PurchaseID', 'Symbol', 'Purchase_Price', 'Current_Price', 'Quantity', 'Coupon',
        'Yield',
        'Purchase_Date')

    bond_report_data.column("#0", width=0, stretch=NO)
    bond_report_data.column("PurchaseID", anchor=CENTER, width=320)
    bond_report_data.column("Symbol", anchor=CENTER, width=80)
    bond_report_data.column("Purchase_Price", anchor=CENTER, width=80)
    bond_report_data.column("Current_Price", anchor=CENTER, width=80)
    bond_report_data.column("Quantity", anchor=CENTER, width=80)
    bond_report_data.column("Coupon", anchor=CENTER, width=80)
    bond_report_data.column("Yield", anchor=CENTER, width=80)
    bond_report_data.column("Purchase_Date", anchor=CENTER, width=80)

    bond_report_data.heading("PurchaseID", text="Bond Id", anchor=CENTER)
    bond_report_data.heading("Symbol", text="Symbol", anchor=CENTER)
    bond_report_data.heading("Purchase_Price", text="Purchase Price", anchor=CENTER)
    bond_report_data.heading("Current_Price", text="Current Price", anchor=CENTER)
    bond_report_data.heading("Quantity", text="Quantity", anchor=CENTER)
    bond_report_data.heading("Coupon", text="Coupon", anchor=CENTER)
    bond_report_data.heading("Yield", text="Yield", anchor=CENTER)
    bond_report_data.heading("Purchase_Date", text="Purchase Date", anchor=CENTER)

    for bond in bond_data:
        bond_report_data.insert(parent='', index='end',
                           values=(
                           bond[0], bond[1], bond[2], bond[3], bond[4], bond[5], bond[6],
                           [bond[7]]))

    bond_report_data.grid(column=0, row=5, sticky=W, padx=5, pady=5)


    print('Displaying stock data...')

    reporting_frame = Frame(root)
    # game_frame.pack()
    reporting_frame.grid(column=0, row=4, sticky=W, padx=5, pady=5)
    report_data = Treeview(reporting_frame)

    report_data['columns'] = (
        'PurchaseID', 'Symbol', 'Share_Count', 'Earnings_Loss', 'Yearly_Earning_Loss',
        'Purchase_Date')

    report_data.column("#0", width=0, stretch=NO)
    report_data.column("PurchaseID", anchor=CENTER, width=320)
    report_data.column("Symbol", anchor=CENTER, width=160)
    report_data.column("Share_Count", anchor=CENTER, width=160)
    report_data.column("Earnings_Loss", anchor=CENTER, width=160)
    report_data.column("Yearly_Earning_Loss", anchor=CENTER, width=160)
    report_data.column("Purchase_Date", anchor=CENTER, width=160)

    report_data.heading("PurchaseID", text="Stock Id", anchor=CENTER)
    report_data.heading("Symbol", text="Symbol", anchor=CENTER)
    report_data.heading("Share_Count", text="Share Count", anchor=CENTER)
    report_data.heading("Earnings_Loss", text="Earnings/Loss", anchor=CENTER)
    report_data.heading("Yearly_Earning_Loss", text="Yearly Earning/Loss", anchor=CENTER)
    report_data.heading("Purchase_Date", text="Purchase Date", anchor=CENTER)

    for stock in stock_data:
        report_data.insert(parent='', index='end',
                           values=(
                               stock[0], stock[1], stock[2], stock[3], stock[4], stock[5]))

    report_data.grid(column=0, row=3, sticky=W, padx=5, pady=5)


class Application(Frame):

    def create_widgets(self):
        quit = Button(root, text="QUIT", fg="red", command=lambda: root.quit())
        analytics = Button(root, text="Show Graph", command=show_graph)
        reporting = Button(root, text="Show Report", command=show_bonds_data)

        quit.grid(column=0, row=2, sticky=W, padx=5, pady=5)
        analytics.grid(column=0, row=0, sticky=W, padx=5, pady=5)
        reporting.grid(column=0, row=1, sticky=W, padx=5, pady=5)


# The Stocks class
class Stock:
    def __init__(self, stock, share_count, purchase_price, current_value,
                 purchase_date):
        self.purchase_id = uuid.uuid1()
        self.stock = stock
        self.share_count = share_count
        self.purchase_price = purchase_price
        self.current_value = current_value
        self.purchase_date = purchase_date
        self.close_prices = []
        self.close_dates = []

    def calculate_loss_gain(self):
        return (self.current_value - self.purchase_price) * self.share_count

    def calculate_yearly_earnings(self):
        return (((self.current_value - self.purchase_price) / self.purchase_price) /
                (get_today_date() - get_date_from_string(self.purchase_date)).days) * 100

    def add_close_value(self, close, date):
        self.close_prices.append(close * self.share_count)
        self.close_dates.append(date)


market_data = json.load(open('AllStocks.json', encoding='utf-8'))


def get_close_price_by_date(symbol, date):
    return [x for x in market_data if x['Symbol'] == symbol and datetime.datetime.strptime(x[
                                                                                               'Date'],
                                                                                           '%d-%b-%y') == date]


def filter_stock_from_market_data(symbol):
    return [x for x in market_data if x['Symbol'] == symbol]


class StockMarket:
    def __init__(self, symbol, date, close_price):
        self.symbol = symbol
        self.date = date
        self.close_price = close_price
        self.close_value_prices = []
        self.close_dates = []

    def add_close_value(self, date, value):
        """Add information to the class"""

        self.close_value_prices.append(value)
        self.close_dates.append(date)


# The bonds class
class Bond(Stock):
    def __init__(self, stock, share_count, purchase_price, current_value,
                 purchase_date, bond_coupon, bond_yield):
        super().__init__(stock, share_count, purchase_price, current_value,
                         purchase_date)
        self.bond_coupon = bond_coupon
        self.bond_yield = bond_yield


# Investor class
class Investor:
    def __init__(self, name, phone, address):
        self.investor_id = uuid.uuid1()
        self.name = name
        self.phone = phone
        self.address = address
        self.stocks = []
        self.bonds = []

    # Adds a new stock to the investor's portfolio
    def add_stock(self, stock):
        self.stocks.append(stock)

    # Adds a new bond to the investor's portfolio
    def add_bond(self, bond):
        self.bonds.append(bond)

    # set bonds
    def set_bonds(self, bonds_data):
        self.bonds = bonds_data

    # set bonds
    def set_stocks(self, stocks_data):
        self.stocks = stocks_data


def get_date_from_string(str_date):
    return datetime.datetime.strptime(str_date, date_format).date()


def print_line():
    print("{:<30}".format('=============================='))


def get_today_date():
    return datetime.date.today()


def open_file(file_name):
    try:
        file = open(file_name, 'r', encoding='utf-8')
    except OSError:
        print('An error occurred while opening the csv file. Please make sure that the required '
              'data files exit in your project directory.')
        sys.exit()

    return file


# Reads the data from the csv file and return it in a list format
def get_stock_data_from_csv_file(file_name):
    data = []
    file = open_file(file_name)

    try:
        with file:
            reader = csv.reader(file)
            next(reader)  # skips the headers
            for row in reader:
                data.append(
                    Stock(row[0], float(row[1]), float(row[2]), float(row[3]), row[4]))
    except ValueError:
        print(f'Error occurred while loading the data from {file_name}. Please make sure that '
              f'your data is in the correct format')
        sys.exit()

    return data


# Reads the bonds data from the provided file
def get_bond_data_from_csv_file(file_name):
    data = []
    file = open_file(file_name)
    try:
        with file:
            reader = csv.reader(file)
            next(reader)  # skips the headers
            for row in reader:
                data.append(Bond(row[0], float(row[1]), float(row[2]), float(row[3]), row[4],
                                 float(row[5]), float(row[6])))
    except:
        print(f'Error occurred while loading the data from {file_name}. Please make sure that '
              f'your data is in the correct format')
        sys.exit()

    return data


# Writes the passed content to the file
def write_to_file(file_name, content):
    try:
        file = open(file_name, "a", encoding='utf-8')
        file.write(content)
        file.close()
    except OSError:
        print('An error occurred while writing to the file')
        sys.exit()


if __name__ == '__main__':
    # Creating the investor Bob Smith
    bob = Investor("Bob Smith", "720-000-1234", "123 Main Street, Denver, CO 80123")

    # Adding the stocks
    bob.set_stocks(get_stock_data_from_csv_file('Data_Stocks.csv'))

    # Adding bonds
    bob.set_bonds(get_bond_data_from_csv_file('Data_Bonds.csv'))

    # Get Market Data
    stockDictionary = {}
    with open('AllStocks.json') as data_file:
        market_data = json.load(data_file)

    # Get all the stocks data
    stocks = [["PurchaseID", "Symbol", "Share #", "Earnings/Loss", "Yearly Earning/Loss",
               "Purchase Date"]]
    dateline_chart = pygal.DateLine(x_label_rotation=25)

    for stock in bob.stocks:
        initial_date = datetime.datetime.strptime(stock.purchase_date, '%m/%d/%Y')
        stocks.append([stock.purchase_id, stock.stock, stock.share_count,
                       stock.calculate_loss_gain(),
                       stock.calculate_yearly_earnings(), stock.purchase_date])
        stock_data.append([stock.purchase_id, stock.stock, stock.share_count,
                       stock.calculate_loss_gain(),
                       stock.calculate_yearly_earnings(), stock.purchase_date])

        filtered_data = filter_stock_from_market_data(stock.stock)

        data_list = []

        for data in filtered_data:
            # dates.append(stock['Date'])
            data_date = datetime.datetime.strptime(data['Date'], '%d-%b-%y')
            close_value = data['Close']
            total_value = close_value * stock.share_count

            if initial_date > data_date:
                total_value = 0

            if stock.stock not in stockDictionary:
                newStockMarket = StockMarket(stock.stock, initial_date, total_value)
                print(stock.stock + " added")
                stockDictionary[stock.stock] = newStockMarket
            # else:
            # stockDictionary[stock.stock].stockClose = total_value
            stockDictionary[stock.stock].add_close_value(data_date, total_value)
            data_point = (data_date, total_value)
            data_list.append(data_point)

        dateline_chart.add(stock.stock, data_list)

    # Get all the bonds data
    bonds = [["PurchaseID", "Symbol", "Purchase Price", "Current Price", "Quantity", "Coupon",
              "Yield", "Purchase Date"]]
    for bond in bob.bonds:
        bonds.append([bond.purchase_id, bond.stock, bond.purchase_price, bond.current_value,
                      bond.share_count,
                      bond.bond_coupon, bond.bond_yield, bond.purchase_date])
        bond_data.append([bond.purchase_id, bond.stock, bond.purchase_price, bond.current_value,
                          bond.share_count,
                          bond.bond_coupon, bond.bond_yield, bond.purchase_date])
    # reporting
    report = '\n\nStocks Ownership for ' + bob.name + ":\n" + tabulate(stocks,
                                                                       headers='firstrow',
                                                                       tablefmt='fancy_grid') \
             + '\n\nBonds Ownership for ' + bob.name + ":\n" + tabulate(bonds, headers='firstrow',
                                                                        tablefmt='fancy_grid')

    print(report)  # Prints the report to the console

    write_to_file(bob.name + "_investment_report.txt", report)  # Save the report to a txt file

    # Analytics

    dateline_chart.title = bob.name + "'s Portfolio Evolution"
    dateline_chart.x_title = 'Date'
    dateline_chart.y_title = 'Value'

    dateline_chart.render_to_file('line_chart.svg')

    # UI Integration

    app = Application(master=root)
    # app.pack()
    # app.grid(column=1, row=5, sticky=W, padx=5, pady=5)
    app.create_widgets()
    app.mainloop()
    root.destroy()
