import datetime
import unittest
import csv
import random
import math

from most_active_cookie import CookieProcessor
from string import ascii_letters
from random import randint
from datetime import timezone


class DataGenerator:

    def generate_random_date(self, dummy_date=False):
        """
        Generate a random date and return it as a string in the required format
        Each part of the date, e.g., year is uniformly sampled from a range
        If dummy_date then we specify a "fake" date
        :param dummy_date: should we specify a fake date
        :return: str of a random date
        """
        year, month, day = randint(2000, 2021), randint(1, 12), randint(1, 28)
        hour, minute, second = randint(1, 23), randint(1, 59), randint(1, 59)
        if dummy_date:
            year, month, day = 9999, 9, 9
        date = datetime.datetime(year, month, day, hour, minute, second,
                                 tzinfo=timezone.utc)
        return date.strftime("%Y-%m-%dT%H:%M:%S%z")

    def generate_date_mask(self, count_mask, max_same_date, num_dates=10):
        """
        Generate the date mask, i.e., a list of indices that we give to
        each of the unique cookies.
        :param count_mask: The count mask for each cookie
        :param max_same_date: Should all cookies that occur the most occur on the same day?
        :param num_dates: The number of dates
        :return: list of date mask, index of the query date in the date list
        """
        date_mask = []
        max_count = max(count_mask)
        max_occurrences = count_mask.count(max_count)
        max_query_day_count = randint(1,
                                      max_occurrences) if not max_same_date else max_occurrences
        other_query_day_count = randint(1,
                                        num_dates - max_occurrences) if num_dates - max_occurrences > 0 else 0
        query_date_index = randint(0, num_dates - 1)
        excluded_list = list(range(num_dates))
        excluded_list.pop(query_date_index)
        for count in count_mask:
            if count == max_count:
                if max_query_day_count > 0:
                    date_mask.append(query_date_index)
                    max_query_day_count -= 1
                else:
                    date_index = random.choice(excluded_list)
                    date_mask.append(date_index)
            else:
                if other_query_day_count > 0:
                    date_mask.append(query_date_index)
                    other_query_day_count -= 1
                else:
                    date_index = random.choice(excluded_list)
                    date_mask.append(date_index)

        return date_mask, query_date_index

    def generate_count_mask(self, num_unique_cookies, num_cookies,
                            max_same_date):
        """
        Generate a count mask, i.e, how many times each unique cookie occurs
        :param num_unique_cookies: The number of unique cookies
        :param num_cookies: The total number of cookies
        :param max_same_date: Should all cookies that occur the most occur on the same day?
        :return: list of the count masks
        """
        count_mask = []
        cookies_left = num_cookies
        for i in range(num_unique_cookies):
            if i < num_unique_cookies - 1:
                add_amount = randint(1, math.ceil(
                    num_cookies // num_unique_cookies))
            else:
                # Increase the likelihood of more than 1 most active cookie on the query date
                # however, the number of cookies may be less than num_cookies
                if max_same_date:
                    add_amount = randint(1, math.ceil(
                        num_cookies // num_unique_cookies))
                else:
                    add_amount = cookies_left
            count_mask.append(add_amount)
            cookies_left -= add_amount
        return count_mask

    def generate_test_data(self, exists=True, max_same_date=False,
                           num_unique_cookies=10, num_cookies=20, num_dates=10):
        """
        Generate the test data, by generating a list of cookies, dates, and
        the respective counts for the cookies
        :param exists: If the query date exists in the dataset
        :param max_same_date: If all cookies that occur the most happen on the same day
        :param num_unique_cookies: The number of unique cookies
        :param num_cookies: The number of cookies
        :param num_dates: The number of dates
        :return: list of list, where each nested list is a row
        """
        cookie_list = self.generate_cookies(num_unique_cookies)
        date_list = [self.generate_random_date() for i in range(num_dates)]
        # sample an occurrence in the CSV randomly from a uniform distribution
        count_mask = self.generate_count_mask(num_unique_cookies, num_cookies,
                                              max_same_date)
        max_count = max(count_mask)
        # create a date mask based on the count_mask list
        date_mask, query_date_index = self.generate_date_mask(count_mask,
                                                              max_same_date,
                                                              num_dates)
        test_data, test_solutions = [], set()
        # get the date we want to query
        query_date = date_list[
            query_date_index] if exists else self.generate_random_date(
            dummy_date=True)
        # create the data
        for cookie_num in range(num_unique_cookies):
            rows = []
            cookie, num_rows = cookie_list[cookie_num], count_mask[cookie_num]
            date = date_list[date_mask[cookie_num]]
            for row_num in range(num_rows):
                rows.append([cookie, date])
            # our solutions have the most occurrences possible and a date of
            # the query date
            if num_rows == max_count and date == query_date:
                test_solutions.add(cookie)
            test_data.extend(rows)
        self.write_csv(test_data)
        return query_date.split("T")[0], test_solutions

    def write_csv(self, data):
        """
        Write the CSV, provided a nested list of lists, where each
        nested list is a row of the CSV
        :param data: list of list
        :return: void
        """
        with open("test_data.csv", "w") as test_file:
            csv_writer = csv.writer(test_file)
            csv_writer.writerow(["cookie", "timestamp"])
            for row in data:
                csv_writer.writerow(row)

    def generate_cookies(self, num_unique=10):
        """
        Generate num_unique number of cookies
        :param num_unique: The number of unique cookies
        :return: list of cookies
        """
        cookie_list = []
        valid_symbols = list(ascii_letters)
        valid_symbols.extend([0, 1, 2, 3, 5, 6, 7, 8, 9])
        for i in range(num_unique):
            cookie = "".join(
                [str(random.choice(valid_symbols)) for _ in range(30)])
            cookie_list.append(cookie)
        return cookie_list


class CookieProcessorTester(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_generator = DataGenerator()

    def test_nonexistent(self):
        """
        Tests where the query date is not in the dataset
        :return: void
        """
        cookie_processor = CookieProcessor()
        test_date, solutions = self.data_generator.generate_test_data(
            exists=False)
        cookie_processor.process_cookies("test_data.csv")
        computed_cookies = cookie_processor.find_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def test_same_day_max(self):
        """
        A simple test where the maximum occurrence cookies occur on the query date
        :return: void
        """
        cookie_processor = CookieProcessor()
        test_date, solutions = self.data_generator.generate_test_data(
            max_same_date=True, num_unique_cookies=10, num_cookies=20,
            num_dates=2)
        cookie_processor.process_cookies("test_data.csv")
        computed_cookies = cookie_processor.find_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def test_mixed_days(self):
        """
        A test where the maximum occurrence cookies occur likely on different dates
        :return: void
        """
        cookie_processor = CookieProcessor()
        test_date, solutions = self.data_generator.generate_test_data()
        cookie_processor.process_cookies("test_data.csv")
        computed_cookies = cookie_processor.find_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def test_medium(self):
        """
        A test with a medium sized dataset
        :return: void
        """
        cookie_processor = CookieProcessor()
        test_date, solutions = self.data_generator.generate_test_data(
            num_cookies=5000, num_dates=25)
        cookie_processor.process_cookies("test_data.csv")
        computed_cookies = cookie_processor.find_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def test_large(self):
        """
        A test with a large dataset
        :return: void
        """
        cookie_processor = CookieProcessor()
        test_date, solutions = self.data_generator.generate_test_data(
            num_unique_cookies= 250,
            num_cookies=25000, num_dates=25)
        cookie_processor.process_cookies("test_data.csv")
        computed_cookies = cookie_processor.find_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def test_very_large(self):
        """
        A test with a very large dataset
        :return: void
        """
        cookie_processor = CookieProcessor()
        test_date, solutions = self.data_generator.generate_test_data(
            num_unique_cookies=500,
            num_cookies=50000, num_dates=25)
        cookie_processor.process_cookies("test_data.csv")
        computed_cookies = cookie_processor.find_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def test_large_overlaps(self):
        """
        A test with a large dataset but with likely multiple maximum occurrence
        cookies on the same day
        :return: void
        """
        cookie_processor = CookieProcessor()
        test_date, solutions = self.data_generator.generate_test_data(
            max_same_date=True,
            num_unique_cookies=500,
            num_cookies=25000, num_dates=25)
        cookie_processor.process_cookies("test_data.csv")
        computed_cookies = cookie_processor.find_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def test_very_large_overlaps(self):
        """
        A test with a very large dataset but with likely multiple maximum occurrence
        cookies on the same day
        :return: void
        """
        cookie_processor = CookieProcessor()
        test_date, solutions = self.data_generator.generate_test_data(
            max_same_date=True,
            num_unique_cookies=500,
            num_cookies=50000, num_dates=25)
        cookie_processor.process_cookies("test_data.csv")
        computed_cookies = cookie_processor.find_active_cookies(test_date)
        self.assertEqual(solutions, computed_cookies)

    def test_all_multiple_iter(self, iterations=10):
        """
        Run all tests iteration number of times
        :param iterations: number of times to run all tests (new data generated per run of each test)
        :return: void
        """
        for iteration in range(iterations):
            self.test_nonexistent()
            self.test_mixed_days()
            self.test_same_day_max()
            self.test_medium()
            self.test_large()
            self.test_very_large()
            self.test_large_overlaps()
            self.test_very_large_overlaps()


if __name__ == '__main__':
    unittest.main()
