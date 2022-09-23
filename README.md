# Online Polls for Kasetsart University
An application for conducting a poll or survey, written in Python using Django. It is based on the [Django Tutorial project][django-tutorial],
with additional functionality. <br>
This application is part of the [Individual Software Process](https://cpske.github.io/ISP) course at [Kasetsart University](https://ku.ac.th).

## How to Install and Run
1. Clone this repository
```
git clone https://github.com/Supakrit65/ku-polls.git
```
2. Go to project directory
```
cd ku-polls
```
3. Create virtual environments using following commands.  
```
python -m venv env
```

4. Then, activate the created virtual environments.  
&nbsp;For **macOS/Linux** use this:
```
. env/bin/activate
```
&ensp;&ensp;&ensp;&ensp;For **Windows** use this:
```
. env/Scripts/activate
```
5. Install items in requirements.txt using command below.  
```
pip install -r requirements.txt
```

**Note that to exit** the virtualenv, type `deactivate`, or close the terminal window.

6. Create `.env` file in the project directory.  
Then copy contents in `sample.env` and paste them in `.env` file.  
**Note** that you can generate your **secret key** [here](https://djecrety.ir).
 
7. Next, **create** database and **load** the data by using these commands.
```
python manage.py migrate
python manage.py loaddata data/polls.json data/users.json
```
8. Run server by running command below.
```
python manage.py runserver
```
9. Then, visit the following url.  
`http://127.0.0.1:8000/` or `localhost:8000/`.


## Demo Admin
| Username | password      |
|----------|---------------|
| admin65  | controller11  |

## Demo Users
| Username | password  |
|----------|-----------|
| tan      | tan4668   |
| demo1    | demopass1 |


## [Project Documents](https://github.com/Supakrit65/ku-polls/wiki)
All project documents are in the [Project Wiki](../../wiki/Home)

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Project Plan](../../wiki/Development%20Plan)
- [Task Board Overview](https://github.com/users/Supakrit65/projects/4/views/8)
- [Iteration 1 Plan](../../wiki/Iteration%201%20Plan) and [Task Board](https://github.com/users/Supakrit65/projects/4/views/1) 
- [Iteration 2 Plan](../../wiki/Iteration%202%20Plan) and [Task Board](https://github.com/users/Supakrit65/projects/4/views/5)
- [Iteration 3 Plan](../../wiki/Iteration%203%20Plan) and [Task Board](https://github.com/users/Supakrit65/projects/4/views/7)
- [Iteration 4 Plan](../../wiki/Iteration%204%20Plan) and [Task Board](https://github.com/users/Supakrit65/projects/4/views/9)

[django-tutorial]: https://docs.djangoproject.com/en/4.1/intro/tutorial01/
