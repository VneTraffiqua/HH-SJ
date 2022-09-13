# Programming vacancies compare


The script downloads developer jobs from HeadHunter and SuperJob and
calculates the average salary for each programming language.

### How to install

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```pip install -r requirements.txt```

Recommended to use [virtualenv/venv](https://docs.python.org/3/library/venv.html) for isolate the project

## Launch.

You need to register the SuperJob application to get [Secret key](https://api.superjob.ru/register).

Added to `.env` file:

 `SJ_API` -  SuperJob Secret Key

Run `main.py`
### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).