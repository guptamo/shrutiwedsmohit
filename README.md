# shrutiwedsmohit
A Last Minute Wedding Website For Those Who Hate Spam
Getting a website from theknot.com or any other big free wedding website mills can be like calling an airstrike on your mailbox. I wanted to make a wedding website for my wedding that didn't have anything to do with email and allowed me to take RSVPs and count my guests and their meals. 

## SECURITY WARNING!!!
This site is meant to be simple and make creating and managing invites as simple as possible. For this reason it generates relatively simple passwords that aren't meant to be easily reproducible with the right info! Keep that in mind if you ever plan on adding anything having to do with email to this site. 

## Installation
NOTE: Make sure that you have a dedicated python3 virtual environment with pip to run this website in.

### 1. Git Clone
Clone this into your virtual environment of choice. 

```
git clone https://github.com/guptamo/shrutiwedsmohit .
```

### 2. Pip Install
Install all the python3 requirements.

```
pip install -r requirements.txt
```

### 4. Install the Application Server of Your Choice
I recommend gunicorn, but decided against inclduing it in the requirements.txt since it's an easy dependency to add yourself that can cater to your own needs.

### 5. Create your Superuser
You're going to need this to manage all of your invitations and guests
```
./manage.py superuser
```

### 6. Migrate your Databse
```
./manage.py migrate
```

## Notes
This site is heavily tailored to a hindu style wedding ie. the events are ceremony, reception, and sangeeet. If you want to customize it to another style wedding, give me a shout and I'm more than happy to help out.
