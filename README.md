# FuelCostCalculator

## Running

Assuming you have Python 3.3 or later installed you should create a virtual environment using the `venv` command.
```
python3 -m venv .venv
```

Then, dependencies must be installed and this can be done using pip and the requirements.txt file
```
pip install -r flask/requirements.txt
```

You can run the project by running the main.py file
```
python3 main.py
```

## Running Tests

Unit tests are found in the `/tests` folder and can be run by executing the `test.py` file
```
python tests.py
```

Coverage reports can be generated like so:
```
coverage run test.py && coverage report -m
```