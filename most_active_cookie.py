import argparse
import csv
import sys


class CookieProcessor:
    def __init__(self):
        self.cookies_dict = {}

    def find_active_cookies(self, date):
        """
        Looks through the count dictionary for a specified date, and return
        the corresponding cookies that have the max count.
        This implementations allows us to avoid having to process all the data again;
        we only need to essentially "query" the max
        :param date:
        :return: set of most active cookies, used in the tester
        """
        most_active_cookies = set()
        res = set()
        if date in self.cookies_dict:
            max_occurrence = max(self.cookies_dict[date].values())
            most_active_cookies = sorted((k, -v) for k,v in self.cookies_dict[date].items())
            for cookie, val in most_active_cookies:
                if -val == max_occurrence:
                    print(cookie)
                    res.add(cookie)
        
        return res

    def process_cookies(self, log_path):
        """
        Process the cookies log CSV file.
        Process the counts here rather than in find_active_cookies() because
        we may choose to change how a "count" is defined, and find_active_cookies()
        is only responsible for finding the max of the counts.
        :param log_path: the path to the log file
        :return: void
        """
        with open(log_path, newline='') as cookie_log:
            log_reader = csv.DictReader(cookie_log)
            for log_row in log_reader:
                cookie, date = log_row['cookie'], log_row['timestamp']
                date = self.process_date(date)
                # update the cookies dictionary
                if date not in self.cookies_dict:
                    self.cookies_dict[date] = {cookie: 1}
                else:
                    if cookie not in self.cookies_dict[date]:
                        self.cookies_dict[date][cookie] = 1
                    else:
                        self.cookies_dict[date][cookie] += 1


    def process_date(self, date):
        """
        Abstract date processing, may be extended to use datetime objects
        Currently just uses string processing to get the year, month, day
        :param date: the UTC date string we process
        :return: str of the processed date
        """
        date_parts = date.split("T")
        # return the year-month-day part of the date
        return date_parts[0]


if __name__ == '__main__':
    # use the argparse library to process the CLI
    arg_parser = argparse.ArgumentParser(
        prog='most_active_cookie.py',
        description='Program to calculate the most active cookies on a date, '
                    'given CSV with cookie and timestamp',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    arg_parser.add_argument("file_path")
    arg_parser.add_argument("--date", "-d")
    args = vars(arg_parser.parse_args(sys.argv[1:]))
    # create a CookieProcessor and process the data
    cookie_processsor = CookieProcessor()
    cookie_processsor.process_cookies(args["file_path"])
    cookie_processsor.find_active_cookies(args["date"])
