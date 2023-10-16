# MY FIRST BLOG MADE WITH DJANGO

<div align="center">
<img width = 35% src = "img/blog.jpeg">
</div>

This repo is dedicated to develop our first project on Django. We are going to build a blog following the instructions on [Django 4 by example](https://www.amazon.com/Django-Example-powerful-reliable-applications/dp/1801813051), book made by Antonio Melé. You cand find him in: [Linkedin](https://www.linkedin.com/in/amele/) or [Github](https://github.com/zenx). This blog app is part of first unit in our second year of web aplication development grade.  

### Setup
We will use Python virtual enviroments to install the [requirements](./requirements.txt)
```console
$ python -m venv .venv --prompt mysite
$ source .venv/bin/activate
$ pip install -r requirements.txt
```
We are going to implement some functionalities to send mails, a `.env` file will be required to keep save some data as passwords or personal mails. It will be used also to some database configuration


### Extra files
To streamline some repetitive processes on terminal we are using [Justfile](https://github.com/casey/just), a handy way to run and save commands. For example, in case of make the migrations of an app in django, instead of using `python manage.py makemigrations app` we are using `just makemigrations app`