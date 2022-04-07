# Home Manager

## Table of contents
* [About the project](#about-the-project)
* [Built with](#built-with)
* [Setup](#setup)
* [Future features](#future-features)

## About the project

![screenshot](home-manager.png?raw=true "Screen shot")

Home Manager is a kanban-board based app for managing tasks between a group of people. The main functionality is said board, with three fields that represent tasks to do, tasks currently in progress and finished tasks. Users can create tasks in their board and commit to do a task which is then assigned to them and moved to "In progress" field. After completing the task it's moved to the third column.

The project contains a messagebox app to let users communicate.

<p align="right">(<a href="#top">back to top</a>)</p>


## Built with
* Back-end: Django
* Front-end: HTML, CSS, Bootstrap and HTMX

<p align="right">(<a href="#top">back to top</a>)</p>
    
## Setup
To run this project locally:

```
$ pip3 install -r requirements
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```

<p align="right">(<a href="#top">back to top</a>)</p>

## Future features:

* A calendar app to manage time-sensitive tasks and appointments
* Different language versions (English and Polish)
* Possibility of using more than one board by one user
* Shared shopping lists
    

<p align="right">(<a href="#top">back to top</a>)</p>

