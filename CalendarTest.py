import unittest
from unittest.mock import Mock
import Calendar


# Add other imports here if needed


class CalendarTest(unittest.TestCase):
    # This test tests number of upcoming events.
    def test_get_upcoming_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = ["an event"]
        events = Calendar.get_upcoming_events(mock_api, time, num_events)

        self.assertEqual(mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['maxResults'], num_events)
        # test to see if the output == the expected output
        self.assertEqual(events, ["an event"] )
        
        # Test if the function raises error appropriately (error is raised when number of events <= 0)
        with self.assertRaises(ValueError, msg="The exception is not correctly raised"):
            Calendar.get_upcoming_events(mock_api, time, 0)

    def test_get_events_from_future(self):

        time = "2020-08-03T00:00:00.000000Z"
        mock_api = Mock()

        event = {'summary': "tea time", 'start': {
            'dateTime': "",
            'timeZone': "Asia/Kuala_Lumpur",
        }, 'end': {
            'dateTime': "2021-08-03T00:00:00.000000Z",
            'timeZone': "Asia/Kuala_Lumpur",
        }, 'attendees': [], 'reminders': {
            'useDefault': True
        }}

        # setting expected output
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = [event]
        # calling the function
        events = Calendar.get_events_from_future(mock_api, time)
        # making sure the list of events has been executed and used get
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)
        # ensure the parameter for time has been passed correctly
        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['timeMin'], time)

        # checking the output against expected output
        self.assertEqual(events, mock_api.events.return_value.list.return_value.execute.return_value.get.return_value)

    def test_get_events_from_past(self):
        mock_api = Mock()

        time = "2021-08-03T00:00:00.000000Z"

        event = {'summary': "abc", 'start': {
            'dateTime': "",
            'timeZone': "Asia/Kuala_Lumpur",
        }, 'end': {
            'dateTime': "2019-08-03T00:00:00.000000Z",
            'timeZone': "Asia/Kuala_Lumpur",
        }, 'attendees': [], 'reminders': {
            'useDefault': True
        }}

        # setting expected output
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = [event]
        # calling the function
        events = Calendar.get_events_from_past(mock_api, time)
        # making sure the list of events has been executed and used get
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)
        # ensure the parameter for time has been passed correctly
        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['timeMax'], time)

        # checking the output against expected output
        self.assertEqual(events, mock_api.events.return_value.list.return_value.execute.return_value.get.return_value)

    def test_navigate(self):
        mock_api = Mock()
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = []

        # MC/DC for branch 1: if ((day>31 or day<=0) or (year<0) or (month>12 or month<1))
        # test case 4: Should raise an error since days cannot exceed 31
        with self.assertRaises(ValueError):
            events = Calendar.navigate(mock_api,  2020, 4, 55)
        # test case 6: Should raise an error since year cannot be <= 0
        with self.assertRaises(ValueError):
            events = Calendar.navigate(mock_api, -21, 6, 15)
        # test case 7: Should raise an error since month cannot be >12
        with self.assertRaises(ValueError):
            events = Calendar.navigate(mock_api, 2015, 22, 6)

        # test case 8: Should return a result as all the inputs are correct and acceptable by the function
        events = Calendar.navigate(mock_api, 2021, 1, 5)
        self.assertEqual(events,
                         mock_api.events.return_value.list.return_value.execute.return_value.get.return_value)  # check result against expected result
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        # Path Coverage
        # Test case 1: {api, -5, 66, 45}, should raise an error since year cannot be a negative value
        with self.assertRaises(ValueError):
            events = Calendar.navigate(mock_api, -5, 66, 45)

        # Test case 2: {api, 2008, 2, 30}, should raise an error since february doesnt have day 30
        with self.assertRaises(ValueError):
            events = Calendar.navigate(mock_api, 2008, 2, 30)

        # Test Case 3: {api, 2012, 2, 28}, should return a result with the correct event.
        events = Calendar.navigate(mock_api, 2012, 2, 28)
        #check to make sure the return is the same as the expected output
        self.assertEqual(events,
                         mock_api.events.return_value.list.return_value.execute.return_value.get.return_value)  # check result against expected result
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.return_value.get.call_count,
                         2)  # check to see if the mock has been called

        # Test case 4: {api, 2002, 2, 30}, should raise an error since february does not have day 30
        with self.assertRaises(ValueError):
            events = Calendar.navigate(mock_api, 2002, 2, 30)

        # Test Case 5: {api, 2019, 2, 28}
        # set and expected output to be similar to an actual event
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = [
            {'kind': 'calendar#event', 'etag': '"3203047949026000"', 'id': '60lonipdgua0t4m7uhh3v112q2',
             'status': 'confirmed',
             'htmlLink': 'https://www.google.com/calendar/event?eid=NjBsb25pcGRndWEwdDRtN3VoaDN2MTEycTIgdnBpazAwMDFAc3R1ZGVudC5tb25hc2guZWR1',
             'created': '2020-10-01T03:46:14.000Z', 'updated': '2020-10-01T03:46:14.513Z', 'summary': 'test',
             'creator': {'email': 'vpik0001@student.monash.edu', 'self': True},
             'organizer': {'email': 'vpik0001@student.monash.edu', 'self': True}, 'start': {'date': '2020-10-20'},
             'end': {'date': '2020-10-21'}, 'transparency': 'transparent',
             'iCalUID': '60lonipdgua0t4m7uhh3v112q2@google.com', 'sequence': 0, 'reminders': {'useDefault': False}}
        ]

        events = Calendar.navigate(mock_api, 2019, 2, 28)
        #should return an event. checking against expected output
        self.assertEqual(events,
                         mock_api.events.return_value.list.return_value.execute.return_value.get.return_value)  # check result against expected  result
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.return_value.get.call_count,
                         3)  # make sure the call to mock has been made to get the result

        # Test case 6: {api, 2005, 4, 31}, should raise an error since day 31 does not exist
        with self.assertRaises(ValueError):
            events = Calendar.navigate(mock_api, 2005, 4, 31)

        # Test Case 7:  {api, 2020, 5, 31}
        events = Calendar.navigate(mock_api, 2020, 5, 31)
        #check output against expected output
        self.assertEqual(events,
                         mock_api.events.return_value.list.return_value.execute.return_value.get.return_value)  # check result against expected result
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.return_value.get.call_count,
                         4)  # make sure the call to mock has been made to get the result

    def test_delete_reminders(self):
        mock_api = Mock()
        event = {'summary': "abc", 'start': {
            'dateTime': "",
            'timeZone': "Asia/Kuala_Lumpur",
        }, 'end': {
            'dateTime': "",
            'timeZone': "Asia/Kuala_Lumpur",
        }, 'attendees': [], 'reminders': {
            'useDefault': True,
            'overrides': None
        }, 'id': Mock()}

        # Test to delete reminders from an event with default reminders only
        event_res = Calendar.delete_reminders(mock_api, event)
        # Ensure the event update function is executed
        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 1)
        # Ensure both default reminders and custom reminders have been removed from the event
        self.assertFalse(event['reminders']['useDefault'])
        self.assertEqual(event['reminders']['overrides'], None)
        # Ensure the function returns the correct output string
        self.assertEqual(event_res, "All reminders deleted from event")

        # Test to delete reminders from an event without any reminders
        event['reminders']['useDefault'] = False
        event_res = Calendar.delete_reminders(mock_api, event)
        # Ensure the event update function is not executed
        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 1)
        # Ensure both default reminders and custom reminders have been removed from the event
        self.assertFalse(event['reminders']['useDefault'])
        self.assertEqual(event['reminders']['overrides'], None)
        # Ensure the function returns the correct output string
        self.assertEqual(event_res, "No reminders for this event")

        # Test to delete reminders from an event with custom reminders only
        event['reminders']['overrides'] = [{'method': 'email', 'minutes': 100}]
        event_res = Calendar.delete_reminders(mock_api, event)
        # Ensure the event update function is executed
        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 2)
        # Ensure both default reminders and custom reminders have been removed from the event
        self.assertFalse(event['reminders']['useDefault'])
        self.assertEqual(event['reminders']['overrides'], None)
        # Ensure the function returns the correct output string
        self.assertEqual(event_res, "All reminders deleted from event")

        # Test to delete reminders from an event with custom reminders and default reminders
        event['reminders']['useDefault'] = True
        event['reminders']['overrides'] = [{'method': 'email', 'minutes': 100}]
        event_res = Calendar.delete_reminders(mock_api, event)
        # Ensure the event update function is executed
        self.assertEqual(mock_api.events.return_value.update.return_value.execute.call_count, 3)
        # Ensure both default reminders and custom reminders have been removed from the event
        self.assertFalse(event['reminders']['useDefault'])
        self.assertEqual(event['reminders']['overrides'], None)
        # Ensure the function returns the correct output string
        self.assertEqual(event_res, "All reminders deleted from event")

    def test_get_reminders(self):
        event = {'summary': "abc", 'start': {
            'dateTime': "",
            'timeZone': "Asia/Kuala_Lumpur",
        }, 'end': {
            'dateTime': "",
            'timeZone': "Asia/Kuala_Lumpur",
        }, 'attendees': [], 'reminders': {
            'useDefault': True
        }}

        # Test if getting reminders from an event with default reminders only returns the expected output
        event_res = Calendar.get_reminders(event)
        self.assertEqual(event_res, "Custom reminders: No\nDefault reminders: Yes")

        # Test if getting reminders from an event without any reminders returns the expected output
        event['reminders']['useDefault'] = False
        event_res = Calendar.get_reminders(event)
        self.assertEqual(event_res, "Custom reminders: No\nDefault reminders: No")

        # Test if getting reminders from an event with custom reminders only returns the expected output
        event['reminders']['overrides'] = [{'method': 'email', 'minutes': 100}]
        event_res = Calendar.get_reminders(event)
        self.assertEqual(event_res, "Custom reminders:\nReminder sent by: email\nTime reminder triggered before event "
                                    "start (minutes): 100\nDefault reminders: No")

        # Test if getting reminders from an event with custom reminders and default reminders
        # returns the expected output
        event['reminders']['useDefault'] = True
        event_res = Calendar.get_reminders(event)
        self.assertEqual(event_res, "Custom reminders:\nReminder sent by: email\nTime reminder triggered before event "
                                    "start (minutes): 100\nDefault reminders: Yes")

    def test_delete_event(self):
        mock_api = Mock()

        event = {'summary': "abc", 'start': {
            'dateTime': "",
            'timeZone': "Asia/Kuala_Lumpur",
        }, 'end': {
            'dateTime': "",
            'timeZone': "Asia/Kuala_Lumpur",
        }, 'attendees': [], 'reminders': {
            'useDefault': True
        }, 'id': Mock()}

        events = [event for i in range(5)]

        # Test if events are deleted given that there are events to be deleted
        event_res = Calendar.delete_event(mock_api, events)
        self.assertEqual(event_res, "Event(s) successfully deleted\n")  # check result against expected result
        # check if event delete function is executed according to the number of events to be deleted
        self.assertEqual(mock_api.events.return_value.delete.return_value.execute.call_count, 5)

        # Test if the result matches the expected output given that there are no events to be deleted
        events = []
        event_res = Calendar.delete_event(mock_api, events)
        self.assertEqual(event_res, "No events to delete")  # check result against expected result
        # check if event delete function is not executed
        self.assertEqual(mock_api.events.return_value.delete.return_value.execute.call_count, 5)

    def test_search_event(self):
        mock_api = Mock()

        events_data = [{'summary': "testing", 'start': {
            'dateTime': "",
            'timeZone': "Asia/Kuala_Lumpur",
        }, 'end': {
            'dateTime': "",
            'timeZone': "Asia/Kuala_Lumpur",
        }, 'attendees': [], 'reminders': {
            'useDefault': True
        }, 'id': Mock()}]

        #
        def load_events(keyword):
            res = []
            for event in events_data:
                if keyword in event['summary']:
                    res.append(event)
            return res

        # Test if searching with a keyword that matches an event title returns the expected output
        user_input = "testing"
        # setting expected output
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = load_events(user_input)
        # calling the function
        events_res = Calendar.search_for_event(mock_api, user_input)
        # check if event list function is executed and get is used
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)
        self.assertEqual(events_res, events_data)

        # Test if searching with a keyword that does not match any event titles returns the expected output
        user_input = "abc"
        # setting expected output
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = load_events(user_input)
        # calling the function
        events_res = Calendar.search_for_event(mock_api, user_input)
        # check if event list function is executed and get is used
        self.assertEqual(mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 2)
        self.assertEqual(events_res, "Event not found in calendar!")


def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=1).run(suite)


if __name__ == "__main__":
    main()
