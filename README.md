# Due Date Calculator

This project calculates a due date for an imaginary issue tracker based on the
time of submission and turnaround time. It also takes work days and working
hours into consideration.

# Installation

Make sure you have python3 (3.7.7) and [virtualenv](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv) installed.

Then run:

```bash
virtualenv venv
source venv/bin/activate
```

Next install the dependencies

```bash
poetry install

OR

pip install -r requirements.txt (if you don't want to use poetry)
```

# Testing

The testing package is [pytest](https://docs.pytest.org/en/stable/) and to run
tests, type the following:

```bash
pytest
```

Make sure you have virtualenv activated.
