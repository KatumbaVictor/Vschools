from datetime import datetime
import pytz

def get_interview_times_in_user_timezone(interview):
    utc = pytz.UTC
    user_timezone = pytz.timezone(interview.timezone)

    start_date_naive = datetime.combine(interview.interview_date, interview.start_time)
    end_date_naive = datetime.combine(interview.interview_date, interview.end_time)

    #Localizing to UTC
    start_date_utc = utc.localize(start_date_naive)
    end_date_utc = utc.localize(end_date_naive)

    #Convert to user timezone
    start_date_user = start_date_utc.astimezone(user_timezone)
    end_date_user = end_date_utc.astimezone(user_timezone)

    #Formatting output
    formated_start_date = start_date_user.strftime('%Y-%m-%d %I:%M %p %Z')
    formated_start_time = start_date_user.strftime('%I:%M %p %Z')
    formated_end_time = end_date_user.strftime('%I:%M %p %Z')

    return formated_start_date, formated_start_time, formated_end_time