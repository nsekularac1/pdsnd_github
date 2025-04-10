import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please enter City(chicago, new york city, washington):').lower()
    while(city not in CITY_DATA):
        city = input('Please enter City(chicago, new york city, washington):').lower()
    # get user input for month (all, january, february, ... , june)
    month = input('Please enter month(all, january, february, ... , june):').lower()
    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please enter day of week (all, monday, tuesday, ... sunday):')

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
   # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month when applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month is:', df['month'].value_counts().idxmax())

    # display the most common day of week
    print('The most common day is:', df['day_of_week'].value_counts().idxmax())


    # display the most common start hour
    print('The most common hour is:', df['Start Time'].dt.hour.value_counts().idxmax())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is:', df['Start Station'].value_counts().idxmax())


    # display most commonly used end station
    print('The most common end station is:', df['End Station'].value_counts().idxmax())


    # display most frequent combination of start station and end station trip
    grouped_df = df.groupby(['Start Station','End Station']).value_counts().idxmax()
    
    print('The most common combination of start and end station trip is: {} and {}'.format(grouped_df[0],grouped_df[1]) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    #create Trip Duration column
    df['Trip Duration']=  (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).dt.total_seconds()
      
    # display total travel time
    print('\nTotal travel time:', df['Trip Duration'].sum()) 

    # display mean travel time
    print('\nMean travel time:',df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCounts of ', df['User Type'].value_counts())

    # Display counts of gender
    try:
        print('\nCounts of ', df['Gender'].value_counts())
    except:
        print("Gender column doesn't exist")

    # Display earliest, most recent, and most common year of birth  
    try:
        print('\nThe earliest year of birth is: {}\nThe most recent year year of birth is: {}\nThe most common year of birth is: {}'.format(int(df['Birth Year'].min()), int(df['Birth Year'].max()), int(df['Birth Year'].value_counts().idxmax())))
    except:
        print("Gender column doesn't exist")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_rows(df):
    more_data=input('Do you want to see 5 lines of raw data(yes/no)?').lower()
    i =0
    while(more_data.lower()=='yes'): 
        print(df[i:i+5])
        i=i+5
        more_data=input('Do you want to see 5 lines of raw data(yes/no)?').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
