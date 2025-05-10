#imports pandas and plotly to be used
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Economic data in this file includes annual data for GDP per year, CPI (inflation measure), stock market returns,
# and the average interest rate per year.
economic_data = pd.read_csv("Economic Data.csv")
#Data does not include percentage change in GDP and CPI year over year so I used a for loop to make that
#Set first value to none since theres no previous data for year 1
gdp_changes = [None] 
for GDP in range(len(economic_data["GDP"]) - 1):
    change = round(float((economic_data["GDP"][GDP+1] - economic_data["GDP"][GDP]) / economic_data["GDP"][GDP]), 4)
    gdp_changes.append(change)
#Same thing for CPI
inflation_rate = [None]
for CPI in range(len(economic_data["CPI"]) - 1):
    change = round(float((economic_data["CPI"][CPI+1] - economic_data["CPI"][CPI]) / economic_data["CPI"][CPI]), 4)
    inflation_rate.append(change)
#appending the new columns to the dataframe
economic_data["Nominal GDP Growth"] = gdp_changes
economic_data["Inflation Rate"] = inflation_rate

#Now I will create a class that allows users to search economic data 
# for a given input year range and they can choose which economic measures to use
class search:
    def __init__(self,df):
        self.data = df
    #this function takes user input year
    def take_year_input(self):
        while True:    
            try:
                beginning_year = int(input("What is the first year in the  range for query: "))
                end_year = int(input("What year last year in the range for your query: "))
                if beginning_year> end_year:
                    raise IndexError("Invalid year range") 
                elif (beginning_year <1954 or beginning_year >2024) or (end_year <1954 or end_year >2024):
                    raise KeyError
                return (beginning_year,end_year)
            except IndexError:
                print("ERROR Invalid year range")

            except ValueError:
                print("ERROR Not a number")

            except KeyError:
                print("ERROR Year out of range")
    #this function takes an input for what two economic measures the user wants to compare
    #this function will be called in another function
    def compare_two_metrics(self,):
        while True:
            try:
                self.metric1 = input("Which will be the first metric you compare out of (GDP,CPI,SP500,RATES) PLEASE TYPE ONE OF THOSE: ")
                self.metric2 = input("Which will be the second metric you compare out of (GDP,CPI,SP500,RATES) PLEASE TYPE ONE OF THOSE: ")
                if self.metric1 == "RATES":
                    self.metric1 = "Average Fed Funds Rate"
                if self.metric2 == "RATES":
                    self.metric2 = "Average Fed Funds Rate"
                if not self.metric1 in ["GDP","CPI","SP500","RATES"]:
                    raise ValueError
                elif not self.metric2 in ["GDP","CPI","SP500","RATES"]:
                    raise ValueError
                else:
                    return (self.metric1,self.metric2)
            except ValueError:
                print("Invalid Option please choose either GDP,CPI,SP500, or RATES")
# This function uses plotly to make a graph and calls the other functions for the user to input what he wants to measure
    def make_graph(self):
        year_range = self.take_year_input()
        minnum = year_range[0]
        maxnum = year_range[1]
        mets = self.compare_two_metrics()
        met1 = mets[0]
        met2 = mets[1]
        specificdf = self.data[(self.data["Year"] >= minnum) & (self.data["Year"] <= maxnum)]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=specificdf["Year"],y=specificdf[met1], name=met1),secondary_y=False)
        fig.add_trace(go.Scatter(x=specificdf["Year"],y=specificdf[met2], name=met2),secondary_y=True)
        fig.update_yaxes(title_text=f"{met1} Measure", secondary_y=False)
        fig.update_yaxes(title_text=f"{met2} Measure", secondary_y=True)

        fig.show()




dev = search(economic_data)

dev.make_graph()

    
