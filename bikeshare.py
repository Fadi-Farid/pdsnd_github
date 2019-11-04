import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['all' , 'january', 'february', 'march', 'april', 'may', 'june' , 'july' , 
          'august' , 'september' , 'october' , 'november' , 'december']
days= ['all' , 'monday' , 'tuesday', 'wednesday' , 'thursday' , 'friday' , 'saturday' ,
        'sunday' ]
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input (" Kindly enter city from chicago, new york city, washington\n")
    city_lower = city.lower()
    while True :
        if city_lower  in CITY_DATA :
                break 
            
        city = input (" Wrong value Kindly enter city from chicago, new york city, washington\n")
        city_lower = city.lower()
    # TO DO: get user input for month (all, january, february, ... , june)

    month = input ("kindly choose certain month or all\n")
    month_lower = month.lower()
    while  month_lower not in months:
        month = input ("Wrong value kindly choose certain month or all\n")
        month_lower = month.lower()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input ("kindly choose certain day or all\n") 
    day_lower = day.lower()
    while day_lower not in days:
        day = input ("Wrong value kindly choose certain day or all\n")
        day_lower = day.lower()
    print('-'*40)
    return city_lower ,  month_lower , day_lower


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
    # load data file into a dataframe.
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime .
    df['Start Time'] = pd.to_datetime(df['Start Time'])
   # extract start hour

    df['start hour'] = df['Start Time'].dt.hour
        
    # extract month and day of week from Start Time to create new columns.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month 
   
        
    if month != 'all':
        
            month = months.index(month) + 1
    
            df = df[df['month'] == month]

    # filter by day of week 
    if day != 'all':
       
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
  """Displays statistics on the most frequent times of travel."""

  print('Calculating The Most Frequent Times of Travel...')
  start_time = time.time()

  # display the most common month

  print('Most Popular Start month:', months[df['month'].mode()[0]-1] )
  # display the most common day of week

  print('Most Popular day of week:' , df['day_of_week'].mode()[0] )

  
   # find the most popular hour
  print('Most Popular hour:' , df['start hour'].mode()[0])

  print("\nThis took %s seconds." % (time.time() - start_time))
  print('-'*40)

def station_stats(df) :

    #Displays statistics on the most popular stations and trip.
  
    print('Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
   
    print('Most commonly used start station :' , df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most commonly used end station :' , df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df ['start station and end station trip'] = df["Start Station"].astype(str) + " to " + df["End Station"].astype(str)
    print('Most commonly used combination of start station and end station trip :' , df['start station and end station trip'].mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    #Displays statistics on the total and average trip duration.

    print('\nCalculating Trip Duration...\n' )
    # start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum() / 120
    print('Total travel time :' , travel_time , 'hours' )
    # display mean travel time
    print('Mean travel time :' , df['Trip Duration'].mean()/120 ,'hours'  )
    #print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def user_stats(df , city):
 #   Displays statistics on bikeshare users.

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types 
    print('Counts of user types :')
    new_types = df.filter(['User Type' , 'Trip Duration'], axis=1)
    new_types.rename(columns={ 'Trip Duration':'Counts'},inplace=True)
    print(new_types.groupby(['User Type']).count())
   
    # Display counts of gender   

    try:
        new = df.filter(['Gender','User Type'], axis=1)
        new.rename(columns={  'User Type':'Counts'},inplace=True)
        print( 'Counts of gender :')
        print(new.groupby(['Gender']).count())
        
        # Display earliest, most recent, and most common year of birth.
        print ( 'The earliest, most recent, and most common year of birth:\n')
        df['year'] = df['Start Time'].dt.year
    
        earliest_year = df['Birth Year'].min()
    
        most_recent_year = df['Birth Year'].max()
    
        print('The earliest year of birth:',earliest_year)
        print('The most recent year of birth', most_recent_year)
        print('The most common year of birth' , df['Birth Year'].mode()[0])
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except:
        print('User Type and Gender coulmns are not available')
 
   
    
def main():
    while True:
        #function to load data.
        city, month, day = get_filters()
        df = load_data(city, month, day)
        # function to calculate certain values from data.
        time_stats(df )
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df , city)
        
        #removing added rows  .    
        df.drop(['Start Time','month','start hour','day_of_week',
                 'start station and end station trip'], axis =1 , inplace = True) 
        # print 5 rows at a time and wait for user inputs.
        start = 0
        end = 5 
        while end <= df.shape[0] :
            
           print(df[df.columns[0:]].iloc[start : end ])
           end = end + 5
           start = start + 5
           if input('\nWould you like to view more rows ? Enter yes or no .').lower() == 'no':
                    break

                
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

