# The Ultimate Flask Course - Udemy

https://www.udemy.com/course/the-ultimate-flask-course
Tutorial from Udemy.com on Flask, user registration/login, and database use.

# Dependencies

Create a virtual env and source it with:
`python -m venv .venv`
`source .venv/Scripts/activate`

## Install Dependencies

`pip install -r requirements.txt`

## Creating the intitial database

`flask shell`
`db.create_all()`
`exit()`

## Donwload SQL Lite

https://www.sqlite.org/download.html
Donwload Command line tools zip file for Windows
Copy files to your C:\sqlite folder
You may need to add this to your windows path env var.
If you open an new command line and cd to project directory.
Run:
`sqlite3 instance/db.sqlite3`
It should open sql lite with the database.

## Confirming db is there

`.tables`
shows the tables
`.schema`
shows the schema

You should see a users table.
