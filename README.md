    # Most Active Cookies
This repository contains two files: `most_active_cookie.py` and `most_active_cookie_tester.py`. 

`most_active_cookie.py`contains the program to calculate the most active cookie(s) on a given date from a CSV log provided in the correct format (cookie, timestamp). The overall running time of the algorithm is `O(n)` with respect to the entries (rows) in the CSV. 

The second file is the tester file, made using Python's `unittest` library. It uses a probabilistic approach to generating the test data, and the random number generators are provided by Python's `random` library. 

## Usage 
The CLI program takes two arguments: 
- The CSV file path
- `-d`, the date argument formatted as YYYY-MM-DD  

**An example is below:**
  
`python most_active_cookie.py test_cases.csv -d 2018-12-08`

The test suite may be run using an IDE like Pycharm or by using the following command to run all available (8) tests:

`python most_active_cookie_tester.py`

