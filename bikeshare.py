import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def generate_warning_message(input_value, input_type):
    warning_message = '{} is not a valid {} option. Please try again!\n'
    return warning_message.format(input_value, input_type)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = None
    month = None
    day = None

    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
        if city in CITY_DATA:
            break
        else:
            print(generate_warning_message(city, 'city'))

    # Determint what filter we want to apply to the data, month, day, both, or none
    filter_options = ['month', 'day', 'both', 'none']
    while True:
        filter_option = input('Would you like to filter the data by month, day, both, or not at all?'
        + ' Type "none" for no time filter.\n').lower()
        if filter_option in filter_options:
            break
        else:
            print(generate_warning_message(filter_option, 'filter'))

    # Get user input for month (all, january, february, ... , june)
    if filter_option in ['month', 'both']:
        while True:
            month = input('Which month? ? January, February, March, April, May, or June?\n').lower()
            if month in MONTHS:
                break
            else:
                print(generate_warning_message(month, 'month'))

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_option in ['day', 'both']:
        while True:
            day = input('Which day? Please type your response as an integer (e.g. 1=Sunday).\n')

            try:
                dayint = int(day)
            except ValueError:
                print('Please input an integer value!')
                continue

            if dayint in range(1, 8):
                day = dayint
                break
            else:
                print(generate_warning_message(day, 'day'))

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
    df = pd.read_csv(CITY_DATA.get(city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    if month is not None:
        month_index = MONTHS.index(month) + 1
        df = df[df['month'] == month_index]

    if day is not None:
        # Input: Monday is 2, and Sunday is 1
        # dt.weekday: Monday is 0, and Sunday is 6
        day_index = (day + 5) % 7
        df = df[df['day_of_week'] == day_index]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month_index = df['month'].mode()[0] - 1
    print('The most common month is {}.\n'.format(MONTHS[common_month_index].title()))

    # Display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of week is {}.\n'.format(DAYS[common_day_of_week]))

    # Display the most common start hour
    common_start_hour = df['Start Time'].dt.hour.mode()[0]
    print('The most common hour is {}.\n'.format(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('The most commonly used start station is {}.\n'.format(df['Start Station'].mode()[0]))

    # Display most commonly used end station
    print('The most commonly used end station is {}.\n'.format(df['End Station'].mode()[0]))

    # Display most frequent combination of start station and end station trip
    stations = df.groupby(['Start Station', 'End Station']).size().nlargest(1).reset_index(name='count')
    print('The most frequent combination of start station and end station trip is:\n{}\n'
    .format(stations))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print('The total travel time is {}.\n'.format(df['Trip Duration'].sum()))

    # Display mean travel time
    print('The mean travel time is {}.\n'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The counts of user types are:\n{}\n'.format(df['User Type'].value_counts()))

    # Display counts of gender
    if 'Gender' in df:
        print('The counts of gender are:\n{}\n'.format(df['Gender'].value_counts()))
    else:
        print('Gender data is not available for this dataset.\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('The earlist year of birth is: {}\n'.format(df['Birth Year'].min()))
        print('The most recent year of birth is: {}\n'.format(df['Birth Year'].max()))
        print('The most common year of birth is: {}\n'.format(df['Birth Year'].mode()[0]))
    else:
        print('Birth Year data is not available for this dataset.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    df['Start Time'] = df['Start Time'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    df.drop(['month', 'day_of_week'], axis = 1, inplace = True)
    index = 1
    while True:
        if index + 5 < df.shape[0]:
            print(df.iloc[index:index + 5].to_json(orient='records', lines=True).replace(',', ',\n'))
        else:
            print(df.iloc[index:].to_json(orient='records', lines=True).replace(',', ',\n'))
            break
        more_lines = input('\nWould you like to view individual trip data? Type \'yes\' or \'no\'.\n').lower()
        if more_lines == 'yes':
            index += 5
            continue
        elif more_lines == 'no':
            break
        else:
            print(generate_warning_message(more_lines, 'input'))

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
