    # Most Active Cookies
This repository contains two files: `most_active_cookie.py` and `most_active_cookie_tester.py`. 

`most_active_cookie.py`contains the program to calculate the most active cookie(s) on a given date from a CSV log provided in the correct format (cookie, timestamp). The overall running time of the algorithm is `O(n)` with respect to the entries (rows) in the CSV. Also note that since we don't care about the order of the most active cookies on some specified date, the order returned may not be necessarily the order of which they occur in the CSV.  

The second file is the tester file, made using Python's `unittest` library. It uses a probabilistic approach to generating the test data, and the random number generators are provided by Python's `random` library. It covers cases such as the specified date not being in the dataset and where all most active cookies occur on the same date, on different dates, and a mix of the two. The probabilistic nature of the data generation cannot necessarily guarantee a test case will occur, e.g., more than one cookie will have the same occurrence, the probabilities are high enough such that it is **expected** that these test cases occur. An in practice, there are additional large test cases and a `test_all_multiple_iter` test that raise the likelihoods of these cases occurring, e.g., running these should make it **extremely likely** that more than one cookie will have the same occurrence. Finally, the order of dates/rows in the CSV are not necessarily increasing in time because the algorithm is implemented using a hashmap of dates, so the algorithm isn't sensitive to the order of dates. 

## Usage 
The CLI program takes two arguments: 
- The CSV file path
- `-d`, the date argument formatted as YYYY-MM-DD  

**An example is below:**
  
`python most_active_cookie.py test_cases.csv -d 2018-12-08`

The test suite may be run using an IDE like Pycharm or by using the following command to run all available (9) tests:

`python most_active_cookie_tester.py`

