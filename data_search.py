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
economic_data["GDP Growth"] = gdp_changes
economic_data["Inflation"] = inflation_rate

#Now I will create a class that allows users to search economic data 
# for a given input year range and they can choose which economic measures to use
class search:
    #initialize and sets the economic data as a self.data
    def __init__(self,df):
        self.data = df
    #this function takes user input year
    def take_year_input(self):
        while True:     #this for loop makes sure the function keeps running until it gets a valid input range
            try: #try block for input
                beginning_year = int(input("What is the first year in the  range for query: "))
                end_year = int(input("What year last year in the range for your query: "))
                if beginning_year> end_year:
                    raise IndexError #raises error if beginning year is greater than end year
                elif (beginning_year <1954 or beginning_year >2024) or (end_year <1954 or end_year >2024): #data starts from 1954 and ends in 2024 so It cant be lower than that
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
    def take_two_metrics(self,):
        dict_pair = {1: "GDP",
                     2: "SP500",
                     3: "CPI",
                     4: "Average Fed Funds Rate",
                     5: "Inflation",
                     6: "GDP Growth"}
        while True:
            try:
                num_metric = int(input("Pick a number representing the metric you want to analyze out of the following:" 
                "\n1: GDP\n2: S&P500 Returns\n3: CPI\n4: Average Federal Funds Rate\n5: Inflation\n6: Nominal GDP Growth Rate" 
                "\nPick a number 1-6: "))
                second_num_metric = int(input("Pick a second number representing the metric you want to analyze out of the following:" 
                "\n1: GDP\n2: S&P500 Returns\n3: CPI\n4: Average Federal Funds Rate\n5: Inflation\n6: Nominal GDP Growth Rate" 
                "\nPick a number 1-6: "))
                if num_metric not in dict_pair or second_num_metric not in dict_pair:
                    raise ValueError
                print(f"SELECTED: {dict_pair[num_metric]}")
                print(f"SELECTED: {dict_pair[second_num_metric]}")

                break  
            except:
                print("ERROR: Not a valid entry")
        #creating dict to make it easy input instead of them having to type in the whole column name

        return (dict_pair[num_metric],dict_pair[second_num_metric])
        
    
# This function uses plotly to make a graph and calls the other functions for the user to input what he wants to measure
    def make_graph(self):
        year_range = self.take_year_input()
        minnum = year_range[0]
        maxnum = year_range[1]
        mets = self.take_two_metrics()
        met1 = mets[0]
        met2 = mets[1]
        #using plotly to create a graph comparing the two measures with two Y axis
        specificdf = self.data[(self.data["Year"] >= minnum) & (self.data["Year"] <= maxnum)]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=specificdf["Year"],y=specificdf[met1], name=met1),secondary_y=False)
        fig.add_trace(go.Scatter(x=specificdf["Year"],y=specificdf[met2], name=met2),secondary_y=True)
        fig.update_yaxes(title_text=f"{met1} Measure", secondary_y=False)
        fig.update_yaxes(title_text=f"{met2} Measure", secondary_y=True)

        fig.show()
#This function will allow the user to search for a specific year range 
#And it will print a summary of that time period including the best and year for the metric,
#The average and standard deviation
    def summarize_metrics_in_range(self):
        metrics = self.take_two_metrics()
        metric1 = metrics[0]
        metric2 = metrics[1]
        year_range = self.take_year_input()
        num1 = year_range[0]
        num2 = year_range[1]
        ranged_years = self.data[(self.data["Year"] >= num1) & (self.data["Year"] <= num2)]
        for metric in metrics:
            highest_metric = ranged_years[ranged_years[metric] == ranged_years[metric].max()]
            lowest_metric = ranged_years[ranged_years[metric] == ranged_years[metric].min()]
            mean_value = ranged_years[metric].mean()
            std = ranged_years[metric].std()
            print(f"STATISTICAL SUMMARY FOR {metric} \n"
                f"\nIn year range {num1}-{num2}:\nHighest Year for {metric}: {highest_metric['Year'].values[0]} : {highest_metric[metric].values[0]}"
                f"\nLowest Year for {metric}: {lowest_metric['Year'].values[0]} : {lowest_metric[metric].values[0]}"
                f"\nMean: {mean_value}"
                f"\nStandard Deviation: {std} \n")
            
