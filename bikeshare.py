"""
Jose Luis Rivera Torres
Jose.Rivera@axity.com
Explore US Bikeshare Data Project
"""
import time
import pandas as pd
import numpy as np

#Dictionary: city in lower case: dataset csv file name
CITY_DATA = { 
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv' }

#Dictionary: available months name in lower case: month id
MONTHS = { 
    'all': 'all',
    'january': '1',
    'february': '2',
    'march': '3',
    'april': '4',
    'may': '5',
    'june': '6' }

#Dictionary: day of the week lower case: day of the week in dt
DAYS_OF_WEEK = { 
    'all': 'all',
    'monday' : 'Monday',
    'tuesday': 'Tuesday',
    'wednesday':'Wednesday',
    'thursday': 'Thursday',
    'friday': 'Friday',
    'saturday': 'Saturday',
    'sunday': 'Sunday' }

def read_string_and_select(filter_type, valid_values_dictionary):
    """
    Asks user to specify a filter_type. Enter for the first value in the dictionary as default.
    Parameters:
        (str) filter_type - name of the filter type select option.
        (dic) valid_values_dictionary - dictionary with the possible options to select.
    Returns:
        (str) value of the input dictionary that tyhe user selecteder
    """
    default_value = list(valid_values_dictionary.keys())[0]
    options = ""
    for option in list(valid_values_dictionary):
        options += option + ", "
    options = options[0:-2]
    request_msg = "\nPlease type one of the followig {} to analize data: {}. (Enter to select default {}):  ".format(filter_type, options,default_value)
    is_captured = False
    while not is_captured:
        read_str = input(request_msg)
        read_clean_str = read_str.strip().lower()
        if len(read_clean_str) == 0:
            return valid_values_dictionary.get(default_value)
        elif valid_values_dictionary.get(read_clean_str) is not None:
            return valid_values_dictionary[read_clean_str]
        else:
            print("\nYou typed \'{}\'. It is not a valid option, try again.\n".format(read_str))
    return valid_values_dictionary.get(default_value)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = read_string_and_select("cities", CITY_DATA)

    # TO DO: get user input for month (all, january, february, ... , june)
    month = read_string_and_select("months", MONTHS)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = read_string_and_select("days of the week", DAYS_OF_WEEK)

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
    df = pd.read_csv(city)
    # set index
    columns = list(df.columns)
    columns[0] = 'ids'
    df.columns = columns
    df.set_index('ids', inplace=True)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['Start End Station'] = df['Start Station'] + ' - ' + df['End Station']
    df['Total Travel Time'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == int(month)]
    
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.capitalize()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Common Month: ', popular_month)

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week: ', popular_day)

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station: ', most_common_start_station)

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station: ', most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    most_common_stations = df['Start End Station'].mode()[0]
    print('Most Popular Start-End Station: ', most_common_stations)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total Travel Time: ', df['Total Travel Time'].sum())

    # TO DO: display mean travel time
    print('Mean Travel Time: ', df['Total Travel Time'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def print_index_value(to_print):
    """Prints the Indexes an values of the Serie passed as parameter.
    Args:
        (serie) to_print - Serie to print
    """
    indexes = list(to_print.index)
    for i in indexes:
        print(i + ': ' + str(to_print[i]))


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('\nCounts of User Types:')
    print_index_value(df.groupby('User Type')['User Type'].count())
    print()
    if 'Gender' in df:
        # TO DO: Display counts of gender
        print('\nCounts of Gender:')
        print_index_value(df.groupby('Gender')['Gender'].count())

        # TO DO: Display earliest, most recent, and most common year of birth
        print('\nEarliest Year of birth: ', df['Birth Year'].min())
        print('Most Recent Year of birth: ', df['Birth Year'].max())
        print('Most Common Year of birth: ', df['Birth Year'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df, row_num = 5):
    """Displays row_num rows of the data frame df up to read different than y from the user 
    Parameters:
        (dataframe) df - dataframe to print.
        (int) row_num - number of row to print for time.
    """    
    for i in range(len(df)//5) :
        is_shown = input("\nWould you like to see next 5 lines of the data? Enter yes or no.\n").strip().lower()
        if is_shown == 'yes':
            print(df.iloc[i*5:(i+1)*5,0:len(df.columns)-5])
        else:
            break
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
