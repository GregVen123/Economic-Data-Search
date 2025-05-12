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
#since its not in percentage form
economic_data["SP500"] = economic_data["SP500"] / 100


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
                beginning_year = int(input("What is the first year in the  range for query (1954 minimum): "))
                end_year = int(input("What year last year in the range for your query (2024 maximum): "))
                if beginning_year> end_year:
                    raise IndexError #raises error if beginning year is greater than end year
                elif (beginning_year <1954 or beginning_year >2024) or (end_year <1954 or end_year >2024): #data starts from 1954 and ends in 2024 so It cant be lower than that
                    raise KeyError #raises error if data is out of range 1954-2024 since that is the first and last year that some of this data is avaliable
                return (beginning_year,end_year) #returns a tuple of first and last year in range to be used in other function
            except IndexError:
                print("ERROR Invalid year range")

            except ValueError: #if user imputs a string
                print("ERROR Not a number")

            except KeyError:
                print("ERROR Year out of range")
    #this function takes an input for what two economic measures the user wants to compare
    #this function will be called in another function
    def take_two_metrics(self,): #This uses a dictionary so the user only has to input a number and it converts it to the 
        dict_pair = {1: "GDP",   # column name so the user doesnt have to input the whole column name
                     2: "SP500",
                     3: "CPI",
                     4: "Average Fed Funds Rate",
                     5: "Inflation",
                     6: "GDP Growth"}
        while True: # for loop to make try block repeat if user puts wrong input
            try: #asks user to input a number 1-6 and each number represents a economic indicator
                num_metric = int(input("Pick a number representing the metric you want to analyze out of the following:" 
                "\n1: GDP\n2: S&P500 Returns\n3: CPI\n4: Average Federal Funds Rate\n5: Inflation\n6: Nominal GDP Growth Rate" 
                "\nPick a number 1-6: "))
                second_num_metric = int(input("Pick a second number representing the metric you want to analyze out of the following:" 
                "\n1: GDP\n2: S&P500 Returns\n3: CPI\n4: Average Federal Funds Rate\n5: Inflation\n6: Nominal GDP Growth Rate" 
                "\nPick a number 1-6: "))
                if num_metric not in dict_pair or second_num_metric not in dict_pair: #checks if input is 1-6
                    raise ValueError
                print(f"SELECTED: {dict_pair[num_metric]}") #prints what user selected
                print(f"SELECTED: {dict_pair[second_num_metric]}")

                break  #since this doesn't return anything it just prints I used a break function to exit the while loop
            except:
                print("ERROR: Not a valid entry")

        return (dict_pair[num_metric],dict_pair[second_num_metric]) #returns tuple of both indicators user wants to compare
        
    
# This function uses plotly to make a graph and calls the other functions for the user to input what he wants to measure
    def make_graph(self):
        year_range = self.take_year_input() #stores tuple of minimum and maximum year in range user wants in variable 
        minnum = year_range[0] #these store the min and max in seperate variables
        maxnum = year_range[1] 
        mets = self.take_two_metrics() #these store the two economic metrics the user wants to use in two variables
        met1 = mets[0]
        met2 = mets[1]
        #using plotly to create a graph comparing the two measures with two Y axis
        specificdf = self.data[(self.data["Year"] >= minnum) & (self.data["Year"] <= maxnum)] #filters dataframe to year range
        fig = make_subplots(specs=[[{"secondary_y": True}]]) #creates a second y axis needed for both economic indicators
        fig.add_trace(go.Scatter(x=specificdf["Year"],y=specificdf[met1], name=met1),secondary_y=False) #uses both met1 and met2 variables for each y axis
        fig.add_trace(go.Scatter(x=specificdf["Year"],y=specificdf[met2], name=met2),secondary_y=True)
        fig.update_yaxes(title_text=f"{met1} Measure", secondary_y=False)
        fig.update_yaxes(title_text=f"{met2} Measure", secondary_y=True)
        correl = specificdf[met1].corr(specificdf[met2])
        if correl >=0:
            print(f"There is a postiive correlation of {correl} between {met1} and {met2}")
        else:
             print(f"There is a negative correlation of {correl} between {met1} and {met2}")
        fig.show() #shows user graph of both metrics on the same plot
        
#This function  will print a summary of that time period including the best and year for both metrics,
#The mean and standard deviation
    def summarize_metrics_in_range(self):
        metrics = self.take_two_metrics() #calls take two metrics function to get metrics user wants to get stats for
        year_range = self.take_year_input() #calls function take_year_input to get the time period user wants to compare
        num1 = year_range[0]
        num2 = year_range[1]
        ranged_years = self.data[(self.data["Year"] >= num1) & (self.data["Year"] <= num2)] #filters dataframe to adjust for the time period
        for metric in metrics: #for loop to give statistical summary for both metrics
            highest_metric = ranged_years[ranged_years[metric] == ranged_years[metric].max()] #these next four lines gat the stats
            lowest_metric = ranged_years[ranged_years[metric] == ranged_years[metric].min()]
            mean_value = ranged_years[metric].mean()
            std = ranged_years[metric].std()
            #Prints summary stats
            print(f"STATISTICAL SUMMARY FOR {metric} \n"
                f"\nIn year range {num1}-{num2}:\nHighest Year for {metric}: {highest_metric['Year'].values[0]} : {highest_metric[metric].values[0]}"
                f"\nLowest Year for {metric}: {lowest_metric['Year'].values[0]} : {lowest_metric[metric].values[0]}"
                f"\nThe Mean {metric} during {num1}-{num2} was: {mean_value}"
                f"\nAnd the Standard Deviation was: {std} \n")
            #shows histogram for for the metric
            fig1 = px.histogram(ranged_years,x=metric,marginal="box",nbins=15,title=f"{metric} Distribution chart")
            fig1.show()
    #this function taskes one metric from the user and a threshold and prints the longest amount of years in the data that the 
    # metric exceeded the threshold in a row. For example if metric = Inflation and threshold = .05 it will print the longest
    #steak of inflation being over 5% in a row
    def longest_streak_one_metric(self):
        #This is the code for take_two_metrics but mofified to take one because we don't need two
        dict_pair = {1: "GDP",   # column name so the user doesnt have to input the whole column name
                     2: "SP500",
                     3: "CPI",
                     4: "Average Fed Funds Rate",
                     5: "Inflation",
                     6: "GDP Growth"}
        while True: # for loop to make try block repeat if user puts wrong input
            try: #asks user to input a number 1-6 and each number represents a economic indicator
                num_metric = int(input("Pick a number representing the metric you want to analyze out of the following:" 
                "\n1: GDP\n2: S&P500 Returns\n3: CPI\n4: Average Federal Funds Rate\n5: Inflation\n6: Nominal GDP Growth Rate" 
                "\nPick a number 1-6: "))
                if num_metric not in dict_pair:
                    raise ValueError
                print(f"SELECTED: {dict_pair[num_metric]}") #prints what user selected
                break  #since this doesn't return anything it just prints I used a break function to exit the while loop
            except:
                print("ERROR: Not a valid entry")
        single_metric = dict_pair[num_metric] #stores the metric in a var
        while True: #user inputs threshold value
            try:
                threshold = float(input(f"Enter a threshold for {single_metric} (EXAMPLE: enter .05 for inflation above 5% (percents should be in decimal form)): "))
                break #if the threshold is a valid number it breaks out of the loop
            except ValueError:
                print("Invalid input. Must be a number.") 
        current_streak = 0 #this tracks the active streak for metric > threshold
        streaks = [0] #list of all streaks, the max is the longest one
        for value in self.data[single_metric]: #for loop iterates through all values in the metric
            if value > threshold: #checks condition
                current_streak += 1 #increases streak
            else:
                if current_streak > 0: #if condition is false 
                    streaks.append(current_streak) #adds streak to list of all streaks
                    current_streak = 0 #resets
        if current_streak > 0: #if it hits 2024 and theres still a streak
            streaks.append(current_streak)
        max_streak = max(streaks) 
        print(f"\nLongest streak in years for {single_metric} above the threshold {threshold} is: {max_streak} years")






    def search_menu(self):#this function will allow the user to choose between finding summary stast for two metrics, or comparing them
        print("***Menu***\nWelcome to the economic data search, please choose an option\n1. I would to get compare two different metrics on a graph and see how they correlate" \
        "\n2. I want to find summary statistics for two different metrics\n3. I want to check a metric's longest streak above a threshold value")
        while True:
            try:
                user_choice = int(input("Please choose an option 1, 2, or 3: "))
                if user_choice == 1:
                    self.make_graph()
                elif user_choice ==2:
                    self.summarize_metrics_in_range()
                elif user_choice ==3:
                    self.longest_streak_one_metric()
                else:
                    raise ValueError
            except:
                print("Invalid, choose either 1 or 2 or 3")
            while True:  
                go_again = input("Would you like to search again? (say either yes/no in lowercase): ")
                if go_again == "yes":
                    break  
                elif go_again == "no":
                    print("Thank you for using the economic search.")
                    return None
                else:
                    print("Invalid input. Please enter 'yes' or 'no'")





dev = search(economic_data)

dev.search_menu()
