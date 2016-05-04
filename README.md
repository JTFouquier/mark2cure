# Mark2Cure

[Mark2Cure](http://mark2cure.org/) is a web-based, concept recognition, relationship extraction and validation tool for annotating text. It is intended to be a fun and exploratory way to help biomedical research, but can readily be extended to other disciplines of study where publication rates far exceed a researcher's ability to consume and incorporate knowledge from the literature.

Scientific communication is broken.

Progress in biomedical science is all about incrementally building off of the work of others. Currently, it takes far too long for one scientist's work to reach all the other scientists that would benefit. Mark2Cure will make scientific communication more efficient for everyone, leading to faster discoveries and cures for disease.

To be successful, we need your help. Mark2Cure works by directly involving crowds of people just like you.

### Please note that as of 3/28/2016 Mark2Cure will be officially hosted on Github instead of Bitbucket.  Issues prior to this date were imported using a script, so read carefully or ask for clarification.

## Citizen Scientist Volunteers:

If you are interested in volunteering as a Mark2Curator to read documents and help expedite our annotation process, please go to [Mark2Cure.org]. The information here is primarily for those with computer science, bioinformatics, and/or programming backgrounds who wish to assist with, develop, or build upon the code. If you stumbled upon this accidentally, we sincerely thank you for your interest in Mark2Cure and ask you to join us at [Mark2Cure.org] instead.

## Developers:

Mark2Cure is open-source and welcomes community contributions! Our issue tracker will soon be updated with issues which are readily "up for grabs" and will be marked as **quick fix** and/or **help wanted.**

To work on an issue in our[ issue tracker, ](https://github.com/SuLab/mark2cure/issues)please comment on the issue and provide the following information in your comment:

1. Your intention to address the issue
2. A rough time line from completion

That's it! We will assign it to you if it makes sense.

While we will always try to be responsive, our team is very small. We ask for your patience if we do not accept a pull request immediately. Our workloads fluctuate, which translates to inconsistent response times on these matters.

*Please know that we are very thankful for your help and desire to contribute to this project.*


## Setup

### Server Dependencies

* `sudo apt-get update`
* `sudo apt-get upgrade`
* `sudo apt-get install build-essential python python-dev python-pip python-virtualenv libmysqlclient-dev git-core nginx supervisor rabbitmq-server graphviz libgraphviz-dev pkg-config libncurses5-dev`

### Project Setup

* Make the python virtual environment and activate it
* `virtualenv mark2cure-venv`
* `. /var/www/virtualenvs/mark2cure-venv/bin/activate`

* Make the project folder and download the repo
* `sudo adduser deploy`
* `sudo /home/deploy/webapps`
* `cd /home/deploy/webapps/`
* `git clone https://USER@bitbucket.org/sulab/mark2cure.git && cd mark2cure`

* Install all the python related dependencies
* `sudo /opt/mark2cure-venv/bin/pip install -r requirements.txt`


### Database Migrations

* `sudo /opt/mark2cure-venv/bin/python manage.py schemamigration APP --auto CHANGE_MESSAGE`
* `sudo /opt/mark2cure-venv/bin/python manage.py migrate APP`

### Control

* `. /opt/mark2cure-venv/bin/activate`
* `cd webapps/mark2cure/ && git pull origin HEAD`
* `sudo supervisorctl restart mark2cure`

* `python /opt/python/current/app/manage.py celeryd -v 2 -E -l INFO`
* `python /opt/python/current/app/manage.py celerybeat`
* `sudo chmod a+x /bin/gunicorn_start`

### Utils

* Flow diagram of the database relationships
* `python manage.py graph_models -a -o myapp_models.png`


#### Notes

* Networkx talk: http://www.slideshare.net/arnicas/a-quick-and-dirty-intro-to-networkx-and-d3



# **Mark2Cure** detailed installation instructions for developers

These are instructions, tips, and tricks for how to install **mark2cure** for
developers with more detail than above, assuming you might be unfamiliar
with much of this technology. Please feel free to let us know if anything is
unclear.

Below is the terminal history for installation of **mark2cure** in a
“clean” brand new Macbook Pro. You will likely have a computer that has already
been used for development, so you may run into different issues, but hopefully
none.

First thing!
You will need pip (you probably already have this). pip is important because it
is compatible with virtual environments which we will use to compartmentalize
different projects that require different versions of software. Mark2cure has a
lot of dependencies.

Install [Brew] using the long command below. It’s a package manager for Apple
comps. “installs the stuff you need that Apple didn’t.”

```sh
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Sudo install a few things. You will need to have virtual environments
installed. For more information, see [Python Virtual Environments].

```sh
$ sudo pip install virtualenv
```

You will also need the virtual environment wrapper: [Virtual Environment Wrapper]

```sh
$ sudo pip install virtualenvwrapper
```

Open the /.bash_profile.

```sh
$ nano ~/.bash_profile
```

Add the following *two* lines to your bash profile:

export WORKON_HOME=$HOME/.virtualenvs

source /usr/local/bin/virtualenvwrapper.sh

Then, "source" the profile.

```sh
$ source ~/.bash_profile
```

Make a new directory where you will house your development
version of **mark2cure** (and other development projects you may have).
You could call this something like "repos." Go into this directory.

```sh
$ mkdir repos
$ cd repos/
```

Clone the repository so that you have an exact copy of **mark2cure**. This would
be done in your “repos” folder. No need to make a folder called “mark2cure”
because “git clone” will do this for you. If you want to develop, then you would
make a branch later (see git documentation).

```sh
$ git clone https://your_user_name@bitbucket.org/sulab/mark2cure.git
```

cd into the newly created folder called **mark2cure**, and make a
virtual environment called “**mark2cure**."

```sh
$ mkvirtualenv mark2cure
```

You want to *activate* the virtual environment.

```sh
$ workon mark2cure
```

There are two folders called **mark2cure**. One is a higher level folder, but
you should "cd" into the lower level to install the requirements file. The
requirements file is just a list of software programs that **mark2cure** (or
any program with a requirements.txt file) is dependent on.

```sh
$ cd mark2cure/
$ pip install -r requirements.txt
```

Databases are needed in **mark2cure** to save and recall all of the useful
annotations provided by the Mark2Curators.

Make sure you download MySQL [Sequel Pro] and obtain a copy of the MySQL
"framework" **mark2cure** database. See Max or Jennifer for this.

```sh
$ brew install mysql
$ ln -sfv /usr/local/opt/mysql/*.plist ~/Library/LaunchAgents
$ launchctl load ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist
```

If you have issues with graphviz and pygraphviz, you can remove them from the
requirements.txt file (*for now*). Other dependencies probably should not be
tampered with.

```sh
$ cd repos/
$ cd mark2cure/
$ pip install -r requirements.txt
```

Make new directory called “env_vars”

```sh
$ mk_dir env_vars
$ mkdir env_vars
$ cd env_vars/
$ touch development.sh
$ nano development.sh
```

Inside the development.sh file will live some special information.
Please see Max or Jennifer for the file contents.

```sh
$ cd mark2cure/
$ source env_vars/development.sh
$ echo $MARK2CURE_DATABASE_URL
```

You will also need the NLTK database [Natural Language Tool Kit]. Download NLTK
using the following commands and follow download instructions in the popup
window; download *everything*.

```sh
$ sudo pip install -U nltk
$ python
```
Running the Python shell will allow you test that the download was successful:

```python
import nltk
```

Run the unit tests:

```sh
$ python manage.py test
```

At this point, all tests should be passing. After all the tests
work correctly, then you can run the server.

```sh
$ python manage.py runserver_plus
```

You should now have a *local* development version of Mark2Cure!

Install “tree” so that you can see a data tree of your current working
directory to see the Mark2Cure application layout.

```sh
$ brew install tree
```

# **mark2cure** development details

When doing manual testing of the **mark2cure** application (i.e., using the
website, and not using the command `python manage.py test`), you will go to the
development server site([Django development server]), and you will realize that
you cannot get past the "log in" page. To fix this, you can run these commands
to *force* the development server to let you get to the "test_user" account.

From terminal, use `python manage.py shell_plus` and run the following
Python commands:

```python
User.objects.create_user('test_user', password='password') 
```

This does not solve the issue of a "simulated database with real content for
testing"... more to come.

## Misc. Information about the project (to be expanded):

[Ypet] is a Javascript library built in Marionette.js to rapidly annotate
paragraphs of text on websites. YPet was developed to rapidly annotate
bio-medical literature for **mark2cure** at The Su Lab by Max Nanis.

## Troubleshooting:

You will need to create an account to [Sentry] to log in and monitor error codes
and issues with both development and production versions of **mark2cure**.

When running `$ python manage.py runserver_plus"` did you get this error?:

```sh
Secret value 'SENTRY_PUBLIC_KEY' is not set
```

This indicates that you must do the following:

```sh
$ echo $MARK2CURE_SENTRY_PUBLIC_KEY
```
Oh no, nothing is there, so you must "source" the development file:

```sh
$ source env_vars/development.sh
```

```sh
$ echo $MARK2CURE_SENTRY_PUBLIC_KEY
```
There, now you should see the key output and can run
`$ python manage.py runserver_plus"` successfully for testing on the local
server.

![The Scripps Research Institute](http://www.scripps.edu/files/images/logo120.png "The Scripps Research Institute")

[Mark2Cure](https://bitbucket.org/sulab/mark2cure) is distributed under the MIT License

TEST Travis

[Virtual Environment Wrapper]:http://virtualenvwrapper.readthedocs.org/en/latest/install.html
[Django Web Framework]:https://www.djangoproject.com/start/overview/
[Python Virtual Environments]:http://docs.python-guide.org/en/latest/dev/virtualenvs/
[Ypet]:https://github.com/SuLab/YPet
[Dillinger]:http://dillinger.io/
[Sentry]:http://sentry.sulab.org/tsri/development/
[Brew]:http://brew.sh/
[Sequel Pro]:http://www.sequelpro.com/
[Natural Language Tool Kit]:http://www.nltk.org/
[Mark2Cure.org]:https://mark2cure.org/
[Django development server]:http://127.0.0.1:8000/
