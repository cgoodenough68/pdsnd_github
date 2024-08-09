import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new-york-city.csv',
              'washington': 'washington.csv' }
MONTHS =['January', 'February', 'March', 'April', 'May', 'June']
DAYS = {'Monday':0, 'Tuesday': 1,'Wednesday':2,'Thursday':3,'Friday': 4,'Saturday':5, 'Sunday': 6}

def get_filters():
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    reply = ''
    # Get the city of interest
    while reply not in CITY_DATA:
        reply = input('Which city would you like to explore? (Chicago, New York City, or Washington): ').lower()
    #add dashes if there are spaces in the city name
    city_file = CITY_DATA[reply]
    city = reply.title()
    # Get month of interest
    while reply not in MONTHS:
        reply = input('What month would you like to filter on? (January, February, ..., June): ').title()
    month = reply
    #Get day of interest
    while reply not in DAYS:
        reply = input('What day of the week would you like to filter on? (Monday, Tuesday,... Sunday): ').title()
    day = DAYS[reply]

    print('-'*40)

    return city_file, city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by
        (str) day - name of the day of week to filter by
    Returns:
        df - Pandas DataFrame containing city data unfiltered
        fdf - Pandas DataFrame containing filtered by month and day
    """
    df = pd.read_csv('./Data/'+city)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    #Create month and day columns
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.dayofweek
    df['Hour'] = df['Start Time'].dt.hour
    #create Trip column (comination Start and End Stations)
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    #create filtered data set
    fdf = df[df['Start Time'].dt.month_name() == month.title()]
    fdf = fdf[fdf['Start Time'].dt.day_of_week == day]

    return df,fdf

def time_stats(df, city, month):
    """Displays statistics on the most frequent times of travel for the unfiltered data set."""

    print('\nCalculating The Most Frequent Times of Travel in unfiltered {} dataset...\n'.format(city))
    start_time = time.time()

    # display the most common month
    print('The most common month of travel in {} is {} with {} rides'.format(city.title(),df['Month'].mode()[0],
                                                            df[df['Month']==df['Month'].mode()[0]].count()['Start Time']))
    # display the most common day of week
    #modified solution from https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
    print("The most popular day of travel is", list(DAYS.keys())
          [list(DAYS.values()).index(df['Day'].mode()[0])])

    # display the most common start hour
    print('The most common hour of travel is {}'.format(df['Hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(fdf,city, month,day):
    """Displays statistics on the most popular stations and trip for filtered data set."""

    print('\nCalculating The Most Popular Stations and Trip in {} in {} on {}...\n'.format(city, month, list(DAYS.keys())
          [list(DAYS.values()).index(fdf['Day'].mode()[0])]))
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is {}.\n'.format(fdf['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most common end station is {}\n.'.format(fdf['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print('The most common trip is {}.'.format(fdf['Trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(fdf, city, month, day):
    """Displays statistics on the total and average trip duration on the filtered data."""

    print('\nCalculating Trip Duration in {} in {} on {}...\n'.format(city, month, list(DAYS.keys())
          [list(DAYS.values()).index(fdf['Day'].mode()[0])]))
    start_time = time.time()

    # display total travel time
    print('The total travel time is {}.'.format(fdf['Trip Duration'].sum()))
    # display mean travel time
    print('The total travel time is {}.'.format(fdf['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(fdf, city, month, day):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats for {} in {} on {}...\n'.format(city, month, list(DAYS.keys())
          [list(DAYS.values()).index(fdf['Day'].mode()[0])]))
    start_time = time.time()

    # Display counts of user types
    print("\nNumber of users in each user type:")
    print(fdf['User Type'].value_counts())

    # Display counts of gender
    print("\nNumber of users of each gender:")
    try:
        print(fdf['Gender'].value_counts())
    except:
        print('\nThis data set contains no gender information.')

    # Display earliest, most recent, and most common year of birth
    
    try:
        print('\nThe earliest user birth year is {}'.format(fdf['Birth Year'].min()))
        print('\nThe latest user birth year is {}'.format(fdf['Birth Year'].max()))
        print('\nThe most common user birth year is {}'.format(fdf['Birth Year'].mode()[0]))
    except:
        print('\nThis data does not contain birth year information.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    display_data = input('Do you want to look at the first five rows of raw data (yes/no)?').lower()[0]
    if display_data == 'y':
        n = 0
        chunk_size = 5
        while n < len(df):
            print(df.iloc[n:n + chunk_size])
            n += chunk_size
            more_data = input("Do you want to see the next 5 lines of raw data? (yes/no): ").strip().lower()
            if more_data != 'yes':
                break

def main():
    while True:
        city_file, city, month, day = get_filters()
        df, fdf = load_data(city_file, month, day)

        display_raw_data(df)
        time_stats(df,city,month)
        station_stats(fdf, city, month, list(DAYS.keys())[list(DAYS.values()).index(df['Day'].mode()[0])])
        trip_duration_stats(fdf, city, month, day)
        user_stats(fdf, city, month, day)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
