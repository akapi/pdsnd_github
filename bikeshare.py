import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday']

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
    city = None
    while not city:
        user_input = input("Enter the city (chicago, new york city, washington): ")
        user_input_formatted = user_input.strip().lower()
        if user_input_formatted in CITY_DATA:
            city = user_input_formatted
        else:
            print(f"Given input '{user_input}' is not accepted. Please enter a valid city") 


    # get user input for month (all, january, february, ... , june)
    month = None
    while not month:
        user_input = input("Enter the month (all, january, february, ... , june): ")
        user_input_formatted = user_input.strip().lower()
        if user_input_formatted in MONTHS:
            month = user_input_formatted
        else:
            print(f"Given input '{user_input}' for month is not accepted. Please enter a valid value") 

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    while not day:
        user_input = input("Enter the day (all, monday, tuesday, ... sunday): ")
        user_input_formatted = user_input.strip().lower()
        if user_input_formatted in DAYS:
            day = user_input_formatted
        else:
            print(f"Given input '{user_input}' for day is not accepted. Please enter a valid value") 

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
    # convert the Start Time and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month)
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
    most_common_month = df['month'].mode()[0]
    month_name = MONTHS[most_common_month].title()
    print(' * most common month:', month_name)

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(' * most common day of week:', most_common_day)

    # display the most common start hour
    ## extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(' * most common start hour:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_most_used = df['Start Station'].mode()[0]
    print(' * most commonly used start station:', start_station_most_used)
    
    # display most commonly used end station
    end_station_most_used = df['End Station'].mode()[0]
    print(' * most commonly used end station:', end_station_most_used)

    # display most frequent combination of start station and end station trip
    df['Start and Stop Stations'] = df['Start Station'] + " -> " + df['End Station']
    start_and_end_stations = df['Start and Stop Stations'].mode()[0]
    print(' * most frequent combination of start and end:', start_and_end_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def _print_duration(display_text, time_diff):
    """Display time duration in readable format
    
    display_text: string to print before the time diff
    time_diff: timedelta object
    """
    days = time_diff.days
    hours = time_diff.seconds // 3600
    minutes = (time_diff.seconds % 3600) // 60
    seconds = time_diff.seconds % 60
    print(f"{display_text}: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # calculate travel time
    df['Travel Time'] = df['End Time'] - df['Start Time']

    # display total travel time
    total_travel_time = df['Travel Time'].sum()
    _print_duration(" * total travel time", total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Travel Time'].mean()
    _print_duration(" * mean travel time", mean_travel_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user tpyes: ", user_types )
    
    # Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print("\nCounts of genders: ", genders )
    else:
        print("\nCounts of genders could not reported, since missing in the current csv data!")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_earliest = int(df['Birth Year'].min())
        birth_recent = int(df['Birth Year'].max())
        birth_most = int(df['Birth Year'].mode()[0])
        print(" * earliest year of birth: ", birth_earliest)
        print(" * most recent year of birth: ", birth_recent)
        print(" * most common year of birth: ", birth_most)
    else:
        print("\nStatistic of 'Birth Year' could not reported, since missing in the current csv data!")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_raw_data = None
        while show_raw_data is None:
           user_input_received = input('\nWould you like to see raw data? Enter yes or no.\n')
           if user_input_received.lower().strip() == 'yes':
               show_raw_data = True
           elif user_input_received.lower().strip() == 'no':
               show_raw_data = False
           else:
               print("Input '%s' not accepted." % user_input_received)
        
        item_index = 0
        chunk_size = 5
        while show_raw_data:
            if item_index >= len(df):
                print("all data was shown.")
                break
            print(df.iloc[item_index:item_index + chunk_size])
            item_index += chunk_size
            
            continue_print = None
            while continue_print is None:
                user_input_continue = input('\nWould you like to see next 5 items? Enter yes to or no.\n')
                if user_input_continue.lower().strip() == 'yes':
                    continue_print = True
                elif user_input_continue.lower().strip() == 'no':
                    continue_print = False
                else:
                    print("Input '%s' not accepted." % user_input_continue)
            
            if not continue_print:
                break

        restart = input('\nWould you like to restart? Enter yes to restart. Any other key to exit.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
