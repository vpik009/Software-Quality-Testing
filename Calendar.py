# Make sure you are logged into your Monash student account.
# Go to: https://developers.google.com/calendar/quickstart/python
# Click on "Enable the Google Calendar API"
# Configure your OAuth client - select "Desktop app", then proceed
# Click on "Download Client Configuration" to obtain a credential.json file
# Do not share your credential.json file with anybody else, and do not commit it to your A2 git repository.
# When app is run for the first time, you will need to sign in using your Monash student account.
# Allow the "View your calendars" permission request.


# Students must have their own api key
# No test cases needed for authentication, but authentication may required for running the app very first time.
# http://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html


# Code adapted from https://developers.google.com/calendar/quickstart/python
from __future__ import print_function
import datetime
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_calendar_api():
    """
    Get an object which allows you to consume the Google Calendar API.
    You do not need to worry about what this function exactly does, nor create test cases for it.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def get_upcoming_events(api, starting_time, number_of_events):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    if number_of_events <= 0:
        raise ValueError("Number of events must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime').execute()

    return events_result.get('items', [])


# Add your methods here.
def get_events_from_past(api, starting_time):
    """ Shows all events at least 5 years in past from the today's date
    """
    events_result = api.events().list(calendarId='primary', timeMax=starting_time,
                                      singleEvents=True, orderBy='startTime').execute()

    return events_result.get('items', [])


def get_reminders(event):
    """ Retrieve reminders for an event
    """
    is_override = event['reminders'].get('overrides')
    is_default_reminder = event['reminders'].get('useDefault')
 
    if is_override is None:
        if is_default_reminder:
            reminder = "Custom reminders: No\nDefault reminders: Yes"
        else:
            reminder = "Custom reminders: No\nDefault reminders: No"
    else:
        reminder = "Custom reminders:\n"
        for item in is_override:
            reminder += "Reminder sent by: " + item['method'] + \
                        "\nTime reminder triggered before event start (minutes): " + str(item['minutes']) + "\n"
        if is_default_reminder:
            reminder += "Default reminders: Yes"
        
        else:
            reminder += "Default reminders: No"
 
    return reminder


def get_events_from_future(api, starting_time):
    """Shows all the planned events in the future
        for at least the next 2 years
    """
    start_date = starting_time[4:]
    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      singleEvents=True, orderBy='startTime').execute()

    return events_result.get('items', [])


def navigate(api, year, month, day):
    """Allows the user to navigate events in years, months and days"""

    if (month > 12 or month < 1) or (year < 0) or (day > 31 or day <= 0):
        raise ValueError("Invalid date. Please ensure the day, month and year selected are correct and exist.")

    if month == 2:  # february

        # checks if the current year is a leap year
        is_leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

        if is_leap:
            days_in_feb = 29
        else:
            days_in_feb = 28

        if day > days_in_feb:
            raise ValueError("Invalid day. Chosen month has", days_in_feb)

    elif (month == 4 or month == 6 or month == 9 or month == 11) and day > 30:
        raise ValueError("Invalid day. Chosen Month has 30 days")

    # initialize time of the event
    starting_time = str(year) + "-" + str(month) + "-" + str(day) + "T00:00:00.000000Z"
    ending_time = str(year) + "-" + str(month) + "-" + str(day) + "T23:59:59.000000Z"

    # make a call
    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      timeMax=ending_time, singleEvents=True, orderBy='startTime').execute()

    return events_result.get('items', []) 


def delete_event(api, events):
    """ Delete event(s) from the calendar

    """
    has_events = False

    for event in events:
        has_events = True
        eventId = event['id']
        api.events().delete(calendarId='primary', eventId=eventId).execute()

    if has_events:
        return "Event(s) successfully deleted\n"
    else:
        return "No events to delete"


def search_for_event(api, user_input):
    """ Search for an event according to the keyword inputted by the user

    """
    user_input = user_input.lower()

    events_result = api.events().list(calendarId='primary', q=user_input,
                                      singleEvents=True, orderBy='startTime').execute()

    found_events = events_result.get('items', [])

    if found_events:
        return found_events
    else:
        return "Event not found in calendar!"


def delete_reminders(api, event):
    """ Delete all default and custom reminders from the event

    """
    is_override = event['reminders'].get('overrides') # get overridden reminder (None is there is no overridden reminder)
    is_default_reminder = event['reminders'].get('useDefault') #get default reminder (boolean)
    if is_override is None:
        if is_default_reminder:
            event['reminders']['useDefault'] = False
        else:
            return "No reminders for this event"
    else:
        event['reminders']['overrides'] = None
        if is_default_reminder:
            event['reminders']['useDefault'] = False

    event_id = event['id']
    api.events().update(calendarId='primary', eventId=event_id, body=event, sendUpdates='all').execute()
    return "All reminders deleted from event"


def menu():
    """Holds all the options the user can click in the menu

    """
    print("\n1. Print the next x number of events")
    print("2. Print all the past events")
    print("3. Print all the future events")
    print("4. Navigate to an event on a certain date")
    print("5. Search for an event")
    print("6. Quit")

    prompt = int(input("Pick an option number: "))
    return prompt


def main():
    api = get_calendar_api()
    time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    not_quit_menu = True
    while not_quit_menu:
        userIn = menu() # user input to indicate which action to perform
        if userIn == 1 :
            number_events = int(input("Select the number of events you want to display: "))
            if number_events < 1:
                raise ValueError("Number of events needs to at least be 1")
            events = get_upcoming_events(api, time_now,number_events)

            print("printing the next",number_events,"events")
            if not events:
                print('No upcoming events found.')
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))

                print(start, event['summary'])
            print("\n\n events for future: \n")

        # everything past here was not originally included in the code
        elif userIn == 2:
            # test the seeing events for the past 5 years
            print("\n\nevents from the past: \n")
            events3 = get_events_from_past(api, time_now)
            if not events3:
                print('No past events found.')
            for event in events3:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])

                # Display reminders
                reminder = get_reminders(event)
                print(reminder)


        elif userIn == 3:
            # test the seeing events for the next 2 years
            events1 = get_events_from_future(api, time_now)
            if not events1:
                print('No upcoming events found.')
            for event in events1:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])

                # Display reminders
                reminder = get_reminders(event)
                print(reminder)

        # testing navigation
        elif userIn == 4:
            print("\n")

            year = int(input("Input the year to navigate to: "))

            all_months = "1. Jan\n2. Feb\n3. Mar\n4. Apr\n5. May\n6. Jun\n7. Jul\n8. Aug\n9. Sep\n10. Oct\n11. Nov\n12. Dec"
            print(all_months)

            # ask the user to input a month
            prompt = input("Please input a month number to navigate to as indicated by numbering: ")

            day = input("Please select a day in this month: ")

            events2 = navigate(api, int(year), int(prompt), int(day))

            if not events2:
                print('No upcoming events found.')
            for event in events2:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])

                # Display reminders
                reminder = get_reminders(event)
                print(reminder)

            for option in range(len(events2)):
                print("\n" + str(option + 1) + ". " + events2[option]['summary'])

            if events2:
                event_num = input("Pick an event number to display more details [enter 'Q' to quit]: ")
                if event_num != "Q":
                    try:
                        event_num = int(event_num)
                    except ValueError:
                        print("Invalid input. Event number must be an integer corresponding to an event in the events list.")
                    else:
                        if 1 <= event_num <= len(events2):
                            event_display = events2[event_num - 1]
                            title = "Event title: " + event_display['summary'] + "\n"
                            creation = "Creation date of event: " + event_display['created'][:10] + "\n"
                            organizer = "Organizer: "
                            for key in event_display['organizer'].keys():
                                if key != 'self':
                                    organizer += event_display['organizer'][key] + " "
                            organizer += "\n"
                            if organizer == "Organizer: \n":
                                organizer = "Organizer: No organizer details \n"

                            if 'description' in event_display:
                                description = "Description: " + event_display['description'] + "\n"
                            else:
                                description = "Description: No description\n"
                            print(title + creation + organizer + description)
                        else:
                            print("Invalid input. Event number must correspond to an event in the events list.")

        elif userIn == 5:
            # test for search event function
            prompt = input("Enter the title of event: ")
            events5 = search_for_event(api, prompt)

            if events5 == "Event not found in calendar!":
                print(events5)
            else:
                #printing
                result= ""
                for event in events5:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    result += start + " " + event['summary'] + "\n"
                    reminders = get_reminders(event)
                    result += reminders + "\n"
                print(result)

                prompt = input("Delete this event(s)?[Y/N]: ")
                if prompt == "Y":
                    print(delete_event(api,events5))
                elif prompt == "N":
                    prompt = input("Delete all reminders of this event(s)?[Y/N]: ")
                    if prompt == "Y":
                        for event in events5:
                            print(delete_reminders(api, event))
        elif userIn == 6:
            not_quit_menu = False


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()
