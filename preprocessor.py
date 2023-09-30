import re
import pandas as pd

def preprocess(lines):
    # Define the regex pattern to match the date and time pattern
    pattern = r'\[\d{1,2}/\d{1,2}/\d{1,2}, \d{1,2}:\d{1,2}:\d{1,2} (AM|PM)\]'

    # Initialize lists to store matches and sentences
    match_list = []
    sentence_list = []

    # Initialize variables to store the current message and timestamp
    current_message = ''
    current_timestamp = None

    for line in lines:
        line = re.sub(r'^\u200e', '', line, flags=re.MULTILINE)
        match = re.search(pattern, line)
        if match:
            # If a timestamp is found, save the previous message
            if current_message:
                match_list.append(current_timestamp)
                sentence_list.append(current_message.strip())
            current_timestamp = match.group()
            current_message = line[len(current_timestamp):].strip()
        else:
            # If no timestamp is found, append the line to the current message
            current_message += ' ' + line.strip()

    # Add the last message to the lists
    if current_message:
        match_list.append(current_timestamp)
        sentence_list.append(current_message.strip())

    # Create a DataFrame with extracted data
    df = pd.DataFrame({'message_date': match_list, 'user_message': sentence_list})

    # Convert the 'date' column to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='[%d/%m/%y, %I:%M:%S %p]')

    # Rename columns
    df.rename(columns={'message_date': 'datetime', 'user_message': 'message'}, inplace=True)

    df['user'] = df['message'].str.extract(r'(.+?):')

    # Replace NaN values in 'user' with 'group_notification'
    df['user'].fillna('group_notification', inplace=True)

    df['message'] = df['message'].str.replace(r'.+?:', '', n=1).str.strip()

    # Extract date components
    df['only_date'] = df['datetime'].dt.date
    df['year'] = df['datetime'].dt.year
    df['month_num'] = df['datetime'].dt.month
    df['month'] = df['datetime'].dt.strftime('%B')
    df['day'] = df['datetime'].dt.day
    df['day_name'] = df['datetime'].dt.strftime('%A')
    df['hour'] = df['datetime'].dt.strftime('%I %p')
    df['minute'] = df['datetime'].dt.strftime('%M')
    df['seconds'] = df['datetime'].dt.strftime('%S')

    period = []
    for hour in df['hour']:
        # Extract the hour and period (AM/PM) from the 'hour' column
        hour, period_indicator = hour.split()

        if hour == '11' and period_indicator == 'PM':
            # Midnight (12:00 AM) should be represented as '11 PM-12 AM'
            period.append('11 PM-12 AM')
        elif hour == '12' and period_indicator == 'PM':
            # Midnight (12:00 AM) should be represented as '11 PM-12 AM'
            period.append('12 PM-1 PM')
        elif hour == '12' and period_indicator == 'AM':
            # Midnight (12:00 AM) should be represented as '11 PM-12 AM'
            period.append('12 AM-1 AM')
        elif hour == '11' and period_indicator == 'AM':
            # Noon (12:00 PM) should be represented as '12 PM-1 PM'
            period.append('11 AM-12 PM')
        elif period_indicator == 'AM':
            # Adjust periods for AM hours
            period.append(hour + ' AM-' + str(int(hour) + 1) + ' AM')
        elif period_indicator == 'PM':
            # Adjust periods for PM hours
            period.append(hour + ' PM-' + str(int(hour) + 1) + ' PM')

    # Add the 'period' column to the DataFrame
    df['period'] = period

    return df

