from datetime import datetime
import pytz

class DateUtil:

    @staticmethod
    def ymd2Y_m_d(ymd):
        # Parse the input string with the specified format
        date_object = None
        try:
            date_object = datetime.strptime(ymd, "%y%m%d")
        except Exception:
            date_object = datetime.strptime(ymd, "%Y%m%d")
            pass

        # Convert the date object to the desired format
        formatted_date = date_object.strftime("%Y-%m-%d")

        return formatted_date

    @staticmethod
    def ten_digit_2_Ymd(ten_digit):
        # Convert the string to an integer
        timestamp = int(ten_digit)

        # Convert the Unix timestamp to a datetime object
        datetime_object = datetime.utcfromtimestamp(timestamp)

        # Format the datetime object as a string in "yyyy-MM-dd hh:mm:ss" format
        formatted_date_time = datetime_object.strftime("%Y-%m-%d")

        # Print the formatted date and time
        return formatted_date_time

    @staticmethod
    def format_milliseconds(milliseconds, format):

        timestamp_milliseconds = float(milliseconds)
        timestamp_seconds = timestamp_milliseconds / 1000.0

        # Convert to a datetime object in UTC
        datetime_utc = datetime.utcfromtimestamp(timestamp_seconds)

        # Define the Seoul time zone
        seoul_timezone = pytz.timezone('Asia/Seoul')

        # Convert UTC datetime to Seoul time
        datetime_seoul = datetime_utc.replace(tzinfo=pytz.utc).astimezone(seoul_timezone)

        # Format the datetime object as a string
        formatted_date = datetime_seoul.strftime(format)

        return formatted_date