import time
import math
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = {"chicago": 1, "new york city": 2, "washington": 3}

months = {'january': 1, 'February': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}

days = { 'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5,'sunday': 6, 'all': 7}

def get_key(val, my_dict):
    for key, value in my_dict.items():
         if val == value:
             return key

    return "key doesn't exist"

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    print("please enter the number corresponding to the city that you would like to analyze the data for : ")
    print('chicago: 1')
    print('new york city: 2')
    print('washington: 3')
    city = None
    month = None
    day = None
    try :
        city = int(input())

        while city not in cities.values():
            print("Invalid input!! \n")
            print("please enter the number corresponding to the city that you would like to analyze the data for : ")
            print('chicago: 1')
            print('new york city: 2')
            print('washington: 3')
            city = int(input())

        city = get_key(city, cities)
        # get the month
        print("please enter the number corresponding to the month that you would like to use as a filter : ")
        print('January: 1')
        print('February: 2')
        print('March: 3')
        print('April: 4')
        print('May: 5')
        print('June: 6')
        print('all: 7')

        month = int(input())
        while month not in months.values():
            print("Invalid input!! \n")
            print("please enter the number corresponding to the month that you would like to use as a filter : ")
            print('January: 1')
            print('February: 2')
            print('March: 3')
            print('April: 4')
            print('May: 5')
            print('June: 6')
            print('all: 7')
            month = int(input())

        month = get_key(month, months)
        # get the day of the week
        print("please enter the number corresponding to the day that you would like to use as a filter : ")
        print('monday: 0')
        print('tuesday: 1')
        print('wednesday: 2')
        print('thursday: 3')
        print('friday: 4')
        print('saturday: 5')
        print('sunday: 6')
        print('all: 7')
        day = int(input())

        while day not in days.values():
            print("Invalid input!! \n")
            print("please enter the number corresponding to the day that you would like to use as a filter : ")
            print('monday: 0')
            print('tuesday: 1')
            print('wednesday: 2')
            print('thursday: 3')
            print('friday: 4')
            print('saturday: 5')
            print('sunday: 6')
            print('all: 7')
            day = int(input())

        day = get_key(day, days)

    except Exception as e:
        print("Exception occurred: {}".format(e))

    finally:
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
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months[month]

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

    try:
        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # display the most common month
        common_month = df['Start Time'].dt.month.mode()[0]
        common_month = get_key(common_month, months)
        print('The most common month is: ', common_month.title())

        # display the most common day of week
        common_day = df['Start Time'].dt.weekday_name.mode()[0]
        print('The most common day is: ', common_day)

        # display the most common start hour
        df['hour']=pd.to_datetime(df['Start Time']).dt.hour
        common_hour = df['hour'].mode()[0]
        print('The most common hour for travel is {}'.format(common_hour))

    except Exception as e:
        print("Exception occurred: {}".format(e))

    finally:
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    try:
        # Display most commonly used start station
        most_common_station('Start Station')

        # Display most commonly used end station
        most_common_station('End Station')

        # Display most frequent combination of start station and end station trip
        frequent_trip = df.loc[:, 'Start Station':'End Station'].mode()[0:]
        frequent_trip_amt = df.groupby(["Start Station", "End Station"]).size().max()
        print('the most frequent trip is:\n', frequent_trip, ' and was driven', frequent_trip_amt,'times')

    except Exception as e:
        print("Exception occurred: {}".format(e))

    finally:
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def most_common_station(direction):
    """
        Displays the most common station

        Args:
            (str) direction: wether it is a start or end station

    """
    common_station = df[direction].mode()[0]
    common_station_counts = df[direction].value_counts()[0]
    print('The most common ', direction , ' is: ',common_station, 'and it was used ', common_station_counts, ' times.')

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    try:
        # Display total travel time
        travel_durations = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
        travel_duration_sum = df['Trip Duration'].sum()
        sum_seconds = travel_duration_sum%60
        sum_minutes = travel_duration_sum//60%60
        sum_hours = travel_duration_sum//3600%60
        sum_days = travel_duration_sum//24//3600
        print('Passengers travelled a total of {} days, {} hours, {} minutes and {} seconds'.format(sum_days, sum_hours, sum_minutes, sum_seconds))

        # Display mean travel time
        travel_mean = math.ceil(df['Trip Duration'].mean())
        mean_seconds = travel_mean%60
        mean_minutes = travel_mean//60%60
        mean_hours = travel_mean//3600%60
        mean_days = travel_mean//24//3600
        print('Passengers travelled an average of {} hours, {} minutes and {} seconds'.format(mean_hours, mean_minutes, mean_seconds))

    except Exception as e:
        print("Exception occurred: {}".format(e))

    finally:
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        # Display counts of user types
        user_types = df['User Type'].value_counts()
        print('The counts of user types are: ', user_types)

        # Display counts of gender
        gender = df['Gender'].value_counts()
        print('The counts of gender are: ', gender)

        # Display earliest, most recent, and most common year of birth
        info_year()

    except Exception as e:
        print("Exception occurred: {}".format(e))

    finally:
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

# Display earliest, most recent, and most common year of birth
def info_year():
    """
    Displays the earliest, most recent, and most common year of birth
    """
    earliest_year = df['Birth Year'].min()
    most_recent_year = df['Birth Year'].max()
    most_common_year = df['Birth Year'].mode()
    print('The oldest customer was born in: ', int(earliest_year),'\n' 'the youngest one was born in:', int(most_recent_year),'\n' 'most of our customers are born in:', int(most_common_year))


#Function to display data to the user on request
def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city."""

    print('Calculating User Stats...\n')
    start_time = time.time()

    try:
        print('Columns details :\n')
        pd.set_option('display.max_columns', None)

        columns = [column for column in df.columns if column not in ['trip', 'Unnamed: 0']]
        print(df[columns].info())
        print('The 5 first rows of the Data are : \n')
        print(df[columns].head(5))
        print()

        count = 5
        while count <= len(df) :
            continue_display = input('Would you display the next 5 lines of raw data? "y" for yes, "n" for no.\nYou can even jump to a specified row where the row number between 0 and {} : '.format(len(df) - 1))
            print("-"*79)
            if continue_display.lower() == "y" or continue_display.lower() == "yes":
                print(df[columns].iloc[count:(count + 5), :])
                count += 5
            elif continue_display.lower() == "n" or continue_display.lower() == "no":
                break
            elif (continue_display.isdigit()) and (int(continue_display) in range(len(df))) and (int(continue_display) >= 0):
                count = int(continue_display)
                print(df[columns].iloc[int(continue_display):(int(continue_display) + 5), :])
                count += 5
            else:
                print("Invalid input.\n")

    except Exception as e:
        print("Exception occurred: {}".format(e))

    finally:
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
