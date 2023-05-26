## Library system with Login Authentication
This demo app is a simple register/login system that saves users in a database. Those users can borrow and return books.

## Technologies
- Flask
- Bootstrap
- SQLAlchemy
- HTML
- CSS

# Setup
Create the Virtual environment by executing one of the commands below:

```
python -m venv project_env
```
```
python3 -m venv project_env
```
This depends on the python version that is installed on the local machine.

In the same directory type the following to activate the environment for Linux:

```
. project_env\bin\activate
```
The following command is for Windows:

```
project_env\Scripts\activate
```

Install required dependencies from requirements.txt file

```
pip install -r requirements.txt
```

# Usage

## How to run the app

Depending on the python version run one of the following commands to run the app:

```
python3 run.py
``` 
or 
```
python run.py
```

## What does the app do?

Once launched the following IP address will be displayed **http://127.0.0.1:5000/**. By following that IP or **localhost:5000** you will be taken to the home page of a website.<br>
There is a navigation bar with a few buttons: **Home**, **Login** and **Register**. Since you won't have an account, you will have to register and then log in. Once authenticated a new button will appear called **Books**. This takes you to the library system, where you can borrow books by pressing the "Borrow" button. Once borrowed, you can return the books by opening your account which will be located next to the Home button.

## Deactivation of the virtual environment

To deactivate the virtual environment type the following in the terminal once you're done with the demo:
```
deactivate
```