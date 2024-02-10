import time
import pandas as pd
import numpy as np
import inquirer
from datetime import datetime
import calendar


#week dic will be used later on data filtering
week = {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6, 'all':7}
#inverse dic idea from (source: https://stackoverflow.com/a/66464410)
inv_dict = {value:key for key, value in week.items()}
#month list for input validation
valid_month = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    city=month=day= None
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # for better user experince nquirer has been used 
    while city not in CITY_DATA.keys():
        try:
            city = input("Please type name of city you wish for analysis\nOptions: Chicago, New york, Washington\n").lower()
        except:
            print("Invalid input, please try again")
    

    while month not in valid_month:
        try:
            month = input("Please type name of month you wish for analysis or type all for no monthly filter\nOptions: all, January, February, March', April, May, June\n").lower()
        except:
            print("Invalid input, please try again")
    
    while day not in week.keys():
        try:
            day = input("Please type name of day you wish for analysis or type all for no daily filter\nOptions: all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n").lower()
        except:
            print("Invalid input, please try again")
    
   
   
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(f'./{CITY_DATA[city]}')  
    #create day/month/hour columns
    df['Month'] = pd.DatetimeIndex(df['Start Time']).month
    df['Day'] = pd.DatetimeIndex(df['Start Time']).day_of_week
    df['Hour'] = pd.DatetimeIndex(df['Start Time']).hour

     
    #check if user choose filter option, if so apply filter
    if month != 'all':

        #get numerical value if selected month
        n =  datetime.strptime(month, '%B').month
        #create filter
        m_filter = df['Month'] == n
        df = df[m_filter]

    if day != 'all':
        d_filter = df['Day'] == week[day]
        df = df[d_filter]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    c_month = df['Month'].mode()
    print(f"The most frequent month of travel is {calendar.month_name[c_month.values[0]]}")

    # display the most common day of week
    c_day = df['Day'].mode()
    print(f"The most frequent day of travel is {inv_dict[c_day.values[0]]}")

    # display the most common start hour
    c_hour = df['Hour'].mode()
    print(f"The most frequent hour of travel is {c_hour.values[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    p_ss = df['Start Station'].mode()
    print(f"The most popular start station is {p_ss.values[0]}")


    # display most commonly used end station
    p_es = df['End Station'].mode()
    print(f"The most popular end station is {p_es.values[0]}")


    # display most frequent combination of start station and end station trip
    #solution inspired by (source : https://stackoverflow.com/a/53037757)

    start_route, end_route = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"The most popular route is {start_route} to {end_route}")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time   
    print(f"Total tarvel time is {df['Trip Duration'].sum()}")

    # display mean travel time
    mean_tt= df['Trip Duration'].mean()
    print(f"Total tarvel time is {df['Trip Duration'].mean()}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    c_types = df['User Type'].value_counts()
    print(f"Counts of each user type: {c_types}")

    if city == 'washington': 
        return
    else: 
    # Display counts of gender
        c_genders = df['Gender'].value_counts()
        print(f"Counts of each gender: {c_genders}")

    # Display earliest, most recent, and most common year of birth
        c_year = df['Birth Year'].mode()
        print(f"Earliest birth year of is {df['Birth Year'].min()} \nMost recent birth year is {df['Birth Year'].max()}\nMost common birth year is {c_year.values[0]}  ")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def read_row(df):
    """Read row data into terminal besed on user prefrence"""

    questions = [
    inquirer.List('read',
                message="Would you like to see first 5 lines of raw data ?",
                choices=['Yes', 'No' ])]
    answers = inquirer.prompt(questions) 
    read = answers['read']
    if read == 'Yes':
        counter1 = 5
        counter2 = 0
        while (read == 'Yes'):
            print(df[counter2:counter1]) 
            counter1 += 5
            counter2 += 5
            questions = [
            inquirer.List('read',
                message="Would you like to see the next 5 lines of raw data ?",
                choices=['Yes', 'No' ])]
            answers = inquirer.prompt(questions)
            read = answers['read'] 
            

    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        read_row(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
