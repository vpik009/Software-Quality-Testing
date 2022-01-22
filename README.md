# Introduction
 This repository demonstrates a variety of different software testing techniques ranging from white box to black box testing. This md file will further elaborate on the specific tests that have been conducted for each functionality. Furthermore, to view the coverage tests, you can proceed to view the html coverage documents in the htmlcov folder.

### delete_events functionality:
 
 The main strategy for testing this functionality is branch coverage and line coverage. Due to the fact that there are two if statements in the function, and both of them contain only one condition, it seems unnecessary to use MC/DC, or condition coverage.  This function is called upon searching for a specific event either on a specific date, or by searching using keyword. Hence, if there are no events found on the date, or using the keyword, and the user decides to delete the events, it needs to first check if the produced list of events is empty. Hence, we check if the list of events provided as an argument to the function is empty. If it is, we find its id, and delete the event with the id, then repeat until the list is empty. Otherwise, we need to mention that there are no events to be deleted. Hence, we need to check the function with an empty list of events and a non-empty list of events. 
 
 On top of that, the second if statement checks to see if the boolean variable has_events is true. It is initially set to False,and then to True in the loop block where events are deleted. Hence, if there are no events in the events list provided as an argument, this branch will be false, otherwise it will be true. Therefore, there are two obvious test cases for this function:
 1. event list is not empty
 2. event list is empty
 
 
 
 ### navigate functionality:

 Navigate functionality has 5 branches. The first branch has several conditions that it needs to meet in order to evaluate to true or false:

 if ((day>31 or day<=0) or (year<0) or (month>12 or month<1))

 
  It would be ideal to perform c/dc test to evaluate this branch and test each condition. However we decided to use MC/DC in order to reduce the number of test cases required to test this specific branch.

Condition A: day>31 or day<=0
Condition B: year<0
Condition C: month>12 or month<1

The if condition has 3 conditions that need to be tested, hence the truth table for the if statement is as follows: 


| Test case number | Condition A | Condition B | Condition C | Outcome |
|:-----------------|:-----------:|:-----------:|:-----------:|--------:|
|        1         |     T       |     T       |       T     |    T    |
|        2         |     T       |     T       |       F     |    T    |
|        3         |     T       |     F       |       T     |    T    |
|        4         |     T       |     F       |       F     |    T    |
|        5         |     F       |     T       |       T     |    T    |
|        6         |     F       |     T       |       F     |    T    |
|        7         |     F       |     F       |       T     |    T    |
|        8         |     F       |     F       |       F     |    F    |


In the truth table above, True (T), signifies that that this test case should allow the test to go inside the branch
In the truth table above, False (F), signifies that that this test case should not allow the test to go inside the branch

Testable test cases for condition A: {4,8}
Testable test cases for condition B: {6,8}
Testable test cases for condition C: {7,8}

The test cases were chosen based on the fact that in order to test one condition we need to keep other conditions constant and make sure the Oucome differs. For instance: test case for condition A was chosen because in test case 3, all conditions other than A (B,C), are false, and the outcome is true, in condition 8, the only thing that differs between the 2 cases is the value of A, and the outcome. Which is idea for testing the condition.

Using the identified test cases for the three conditions we can identify the most relevant tests: 
{4,6,7,8}

Some possible test cases are:
1. navigate(api, 2020, 4, 55)
Condition A should evaluate to true since the year is >31, and Condition C and B should evaluate to false, hence testing test case 4 in the truth table.

2. navigate(api, -21, 6, 15)
Condition A and C should evaluate to false, and Condition B should evaluate to true since the year is <=0, hence testing test case 6 from the truth table

3. navigate(api, 2015, 22, 6)
Condition A and B should evaluate to false and Condition C should evaluate to true since the month is >12, hence testing test case 7 from the truth table

4. navigate(api, 2021, 1, 5)
All conditions should evaluate to false, and hence should not go inside the branch. Therefore, it tests test case 8 from the truth table.


These test cases will also allow us to test the branch for a false outcome and a true outcome, resulting in full branch coverage.

To go through the rest of the function, we will use path coverage to go through all of the possible paths in the function.
There are 5 branches in the function, in order to go through each path, we need to identify all possible combinations of the conditional statement oucomes:

Conditional Statement A: if ((day>31 or day<=0) or (year<0) or (month>12 or month<1))
Conditional Statement B: if (month == 2)
Conditional Statement C: if (is_leap)
Conditional Statement D: if (day > days_in_feb)
Conditional Statement E: if ((month == 4 or month == 6 or month == 9 or month == 11) and day > 30)


The truth table for the combinations is as follows:

| Test case number | Condition A | Condition B | Condition C | Condition D | Condition E | Outcome |
|:-----------------|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|--------:|
|        1         |     T       |             |             |             |             |    F    | 
|        2         |     F       |     T       |       T     |      T      |             |    F    |
|        3         |     F       |     T       |       T     |      F      |             |    T    |
|        4         |     F       |     T       |       F     |      T      |             |    F    |
|        5         |     F       |     T       |       F     |      F      |             |    T    |
|        6         |     F       |     F       |             |             |      T      |    F    |
|        7         |     F       |     F       |             |             |      F      |    T    |

A true outcome (T), represents that the function has successfully completed and should return a value.
A false outcome (F), represents that the functions unsuccessfully completed and should raise a ValueError.

Ideally, to give a full path coverage the number of test cases required to test all combination is 2^n, where n is the number of conditions, hence: 2^5 = 32 test cases.
Nevertheless, this is not the case in this scenario as the paths branch off from one another, which results in not being able to test reach all branches given one test cases. 

Hence, the possible test cases for path coverage of this function are:
format: {api, year, month, day}

1.  navigate(api, -5, 66, 45)
This should evaluate to false since year cannot be less than 0. Hence, passes condition A, and raises an exception

2.  navigate(api, 2008, 2, 30) 
This should evaluate to false since February (2), does not have 30 days in the month. Hence raises and exception.

3.  navigate(api, 2012, 2, 28)
This should evaluate to True since all arguments are accepted and are correct.

4.  navigate(api, 2002, 2, 30)
This should evaluate to False since February (2) does not have 30 days


5.  navigate(api, 2019, 2, 28)
This should evaluate to True since all arguments are accepted and are correct.


6.  navigate(api, 2005, 4, 31)
This should evaluate to False since April (4) does not have 30 days

7.  navigate(api, 2020, 5, 31)
This should evaluate to True since all arguments are accepted and are correct.


### delete reminders functionality:

The delete reminders functionality is tested by using C/DC coverage. C/DC coverage is used instead of branch coverage is to ensure each condition have tested True and False at least once and each decision in the function have tested for all the outcomes.
The delete reminders functionality contains 4 branches. This function is called when the user searches for events.

There are 2 conditions that are to be considered in the function:
1. if event custom reminders is None
2. if event default reminders is True
For each of the conditions, the outcomes can be True or False.

For full C/DC coverage, 4 test cases are required where the the test inputs are as follows:
1. event custom reminders is None, event default reminders is True
2. event custom reminders is None, event default reminders is False
3. event custom reminders is not None, event default reminders is True
4. event custom reminders is not None, event default reminders is False

For every test, the event's default reminders is checked if it is set to False and the event's custom reminders is checked if it is None. This is to ensure that it was set correctly before updating the event.



### search events functionality:

Branch coverage and line coverage is used to test the search events functionality as the function only consists of one if-else statement.
The condition that is checked in the function is if there are events in the list. 

Therefore, 2 test cases are required and the test inputs to achieve full branch coverage is:
1. A user input where it matches an event title in the calendar
2. A user input where it does not match any event titles in the calendar

The 2 decision branches are tested according to the array of searched events, ensuring that it returns the correct output.



### see past events functionality:

To perform tests for this functionality we are going to use statement / line coverage. This is applicable in this functionality since it only contains 2 lines of code excluding the return statement, and does not have branches or pre-conditions of any sort. The argument passed to the function is starting_time. This argument is passed from the main function where the starting_time is gotten automatically using Python's datetime. Therefore, since it is not a user input, we do not have to check for its correctness. Hence a test case to test the functions functionality is:

1. get_events_from_future(api, '2020-08-03T00:00:00.000000Z')

It is tested by ensuring that the events list function is executed once and the minimum time parameter passed into the list function is set correctly.
This single test case will result in full line coverage for the functionality.



### see future events functionality:

To perform tests for this functionality we are going to use statement / line coverage. Line coverage fir this functionality is sufficient, as similar to the get_events_from_future function, it does not have any branches or if statements. Therefore, we do not have to consider branch coverage, c/dc, mc/dc or path coverage to fully test this functionality. A suitable test case to execute all lines of code in this function is: 

1. get_events_from_past(api, "2021-08-03T00:00:00.000000Z")

It is tested by ensuring that the events list function is executed once and the minimum time parameter passed into the list function is set correctly.
This single test case will result in full line coverage for the functionality.



### get reminders functionality

The get reminders functionality is tested by using C/DC coverage. C/DC coverage is used instead of branch coverage is to ensure each condition have tested True and False at least once and each decision in the function have tested for all the outcomes.
The get reminders functionality contains 4 branches. This function is called when the user displays events in the past or displays events in the future, as well as navigating through the calendar and searching for events.

There are 2 conditions that are to be considered in the function:
1. if event custom reminders is None
2. if event default reminders is True
For each of the conditions, the outcomes can be True or False.

For full C/DC coverage, 4 test cases are required where the the test inputs are as follows:
1. event custom reminders is None, event default reminders is True
2. event custom reminders is None, event default reminders is False
3. event custom reminders is not None, event default reminders is False
4. event custom reminders is not None, event default reminders is True



### get_upcoming_events_number

To test this functionality we need to perform branch coverage. Since the function contains one if condition that checks for whether the argument (number_if_events) passed into it is smaller than or equals to 0.
In order to get full branch coverage and as a result 100% line coverage in this functionality we need to ensure that the if condition evaluates to both true and false. Suitable test cases to accomplish that are:

1. get_upcoming_events(api, "2020-08-03T00:00:00.000000Z", 0)
2. get_upcoming_events(api, "2020-08-03T00:00:00.000000Z", 2)

These two test cases will result in full branch coverage for the function.
