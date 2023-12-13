# HelpingHand

A web base platform, where clients can hire worker easily.

## Techs
- Flask
- PostgreSQL
- Flask-SQLAlchemy
- Flask-Migrate
- HTML
- CSS
- JavaScript


## Build Instructions
- Clone the repo using ```git clone https://github.com/swapnilGhosh007/helepinghand.git```
- Make sure you have Python 3.9 or higher installed
- To install dependencies,
    - ```conda create -n helpinghand python=3.9```
    - ```conda activate helpinghand```
    - ```pip install -r requirements.txt```
- Create a PostgreSQL database named HelpingHand
- Create an account in [Stripe](http://stripe.com), copy your public_key and api_key from Stripe Developer site   
- Create a .env file in the root directory and add the following variables:
    - DEV_DB=`postgresql://<username>:<password>@localhost/animatrix`
    - STRIPE_PUBLIC_KEY=`Your public key`
    - STRIPE_API_KEY=`Your API key`

- Initialize database using 
    - ```flask db init```
    - ```flask db migrate```
    - ```flask db upgrade```
- Run the app using ```flask run```

## Modules and Features

### Worker:
- Can update CV.
- Can post and update their schedule.
- Can give Platform feedback 
- Can update profile.
- Can update password

### Client:
- Can see hired workers.
- Can update profile.
- Can see available workers according to the selected schedule.
- Can submit a review and rating about workers.
- Can give Platform feedback
- Can see worker profile 

### Services:
- Easy Navigation.
- Advanced search. 
- Workers can see their assigned hourly rate
- Workers can see their past Reviews.
- Clients can do payments.

### Admin:
- Account approval.
- Account ban.
- Can see all users.
- Can set worker hurley rate



