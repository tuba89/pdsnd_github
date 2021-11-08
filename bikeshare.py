#!/usr/bin/env python
# coding: utf-8

from datetime import datetime
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
CITY_LIST = ['chicago', 'new york city', 'washington']
MONTH_LIST = ['january', 'february', 'march', 'april', 'may', 'june']
DAY_LIST = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Enter the name of the City to analyse (Chicago, New York City, Washington): ")
        city.lower()
        if city in CITY_LIST:
            break
        print("\nInvalid City !, Try Again please ...\n")
        
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter the month(january, february, ... , june), Type ALL to apply no month filter: ")
        month.lower()
        if month in MONTH_LIST or month == "ALL".lower():
            break
        print("\nInvalid month !, Try Again please ...\n")
        
    # get user input for day of week (all, monday, tuesday, ... sunday
    while True:
        day = input("Enter the day of week (monday, tuesday, ... sunday), Type ALL to apply no day filter: ")
        day.lower()
        if day in DAY_LIST or day == "ALL".lower():
            break
        print("\nInvalid day !, Try Again please ...\n")
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
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month_name()

    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    # Filter the month & create new dataframe
    if month != "all":
        df = df[df['month'].str.startswith(month.title())]

        
    #Filter the day & create new dataframe
    if day != 'all':
        df = df[df['day_of_week'].str.startswith(day.title())]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    print('.'*48)
    start_time = time.time()

    df['month'] = df['Start Time'].dt.month_name()
    most_common_month = df['month'].mode()[0]
    print('\nThe Most common month: ', most_common_month)
    
   
    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    most_common_day = df['day_of_week'].mode()[0]
    print('\nThe Most common day of week: ', most_common_day)

    # display the most common start hour
    start_hour = df['hour'].mode()[0]
    
    # Converting int hour to (AM or PM)
    best_hour = datetime.strptime(str(start_hour), "%H")
    best_start_hour = best_hour .strftime("%I %p")
    print('\nThe Most common start hour: ', best_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    print('.'*49)
    start_time = time.time()

    # display most commonly used start station
    print('\nThe most commonly used start station is:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('\nThe most commonly used end station is:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    # ['Lake Shore Dr & Monroe St', 'Streeter Dr & Grand Ave']
    combination = (df['Start Station'] + ' ==> To ==> ' + df['End Station']).mode()[0]
    print('\nThe most frequent combination of start station and end station trip are:\n',combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def hms(seconds):
    """
    INPUT: seconds INT
    This is a function of calcuting how many hours/days, minutes in total of seconds
    and how much seconds left,
    OUTPUT e.i:  578 hour or(24 day), 06 minutes, 40 seconds.
    """
    h = seconds // 3600
    d = h // 24
    m = seconds % 3600 // 60
    s = seconds % 3600 % 60
    return ' {:1g} hour or({} day), {:1g} minutes, {:1g} seconds.'.format(h, d, m, s).rstrip('0').rstrip('.')

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    print('.'*28)
    start_time = time.time()

    # display total travel time
    total_trip = df['Trip Duration'].sum()
    print("The Total Travel time in seconds = ", total_trip)
    t = hms(total_trip)
    print("which means : ", t)


    # display mean travel time
    avg_trip = df['Trip Duration'].mean()
    print("The Average Travel time = {0:.2f}".format(avg_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    print('.'*25)
    start_time = time.time()

    # Display counts of user types
    user_t = df['User Type'].value_counts().to_string()
    print("The count of the User Types is:\n",user_t)
    
    # there's not gender & birthday columns in Washington dataset
    if city.title() == 'Chicago' or city.title() == 'New York City':

        # Display counts of gender
        user_gen = df['Gender'].value_counts().to_string()
        print("Counts of the gender is:\n",user_gen)

        # Display earliest, most recent, and most common year of birth
        # 1- the earliest year of birth
        eraliestBirthYear = df['Birth Year'].min()
        # 2- the most recent year of birth
        recentBirthYear = df['Birth Year'].max()
        # 3- the most common year of birth
        commonBirthYear = df['Birth Year'].mode()[0]
        print("The earliest year of Birth is= ", int(eraliestBirthYear))
        print("The most recent year of Birth is= ", int(recentBirthYear))
        print("The common year of Birth is= ", int(commonBirthYear))
    elif city.title() == 'Washington':
        print("OOPS! we are sorry, The Gender and Birth of year doesn't exist")  
 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """ display raw data on screen """
    number = 5
    print(df.head(number))
    while True:
        raw_data = input("\nWould you like to see more raw data? Type: (yes) or (no)\n").lower()
        if raw_data == 'no':
            break
        elif raw_data == 'yes':
            number += 5
            print(df.iloc[number-5:number, :])
        else:
            print('\nInvalid input, Please Try again ... ')
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city) # there is missing columns is Washington dataset
        
        while True:
            view_raw_data = input("\nWould you like to see more raw data? Type: (yes) or (no)\n")
            if view_raw_data.lower() != 'yes':
                break
            display_raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
 
 

