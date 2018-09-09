# Lore

An education-oriented social media, created for the CS A-Level.

## Lore's Backend
Flask handles the backend of this social media. This includes: posting, following, storing users data (username/password). 
The front-end, built in React, makes AJAX calls to the backend in order to retrieve/follow users. Every time a change in data is detected, states and properties are updated. 


### Endpoints
All accessible API endpoints are accessed with /api/example/. 

These are the accessible endpoints:
1. /user/ - Retrieves user information via username.
2. /register/ - Allows a user to register to the database.
3. /follow/ - Follows given user.
4. /unfollow/ - Unfollows given user.
5. /post/ - Submits a post on given users account.
6. /posts/ - Retrieves posts
7. /edit/
    - /account/ - Edits the information of an account.
    - /post/ - Edits te information of a post.


### Example API Requests
All requests must contain a token in the header.
i.e. "token": "xxxx-xxxx-xxxx";

**Example:** Request to retrieve the posts of a user using username.
POST request to /api/posts/,
```
{
    "username": "Mushy"
}
``` 
RESPONSE - 200 OK
```
{
    "user-info": {
        "uuid": "1",
        "username": "Mushy",
        "email": "mushysaurus@gmail.com"
    },
    "posts": [
        {"id": "1", "body": "This is the body of the first post.", "publish_date": "utc-datetime"},
        {"id": "2", "body": "This is the body of the second post.", "publish_date": "utc-datetime"},
        {"id": "3", "body": "This is the body of the third post.", "publish_date": "utc-datetime"}
    ]
    "followed_posts": [
        {"id": "1", "body": "This is the body of the first post.", "publish_date": "utc-datetime"},
        {"id": "2", "body": "This is the body of the second post.", "publish_date": "utc-datetime"},
        {"id": "3", "body": "This is the body of the third post.", "publish_date": "utc-datetime"}
    ]
}
``` 

RESPONSE - 404 NOT FOUND
```
{
    "response": "Could not find that user".
}
```

**Example #2:** Request to retrieve the information of a user with a username.
POST request to /api/user/,
```
{
    "username": "Mushy"
}
```
RESPONSE - 200 OK
```
{
    "about_me": null,
    "email": "mushy@Gmail.com",
    "first_name": "mushy",
    "last_name": "mushy",
    "last_seen": "Mon, 13 Aug 2018 21:03:16 GMT",
    "username": "mushy",
    "uuid": 2
}
```

**Example #3:** Following a user with a username.
POST request to /api/follow/
```
{
    "username": "Mushy",
    "to_follow": "Leooo"
}
```
RESPONSE - 200 OK
```
{
    "response": "Successfully followed."
}
```
REPONSE - 404 NOT FOUND
```
{
    "resposne": "Can not find that user!"
}
```
or
```
{
    "response": "Can not follow yourself!"
}
``` 

**Example #4**: Submitting a registration form.
POST request to /api/register,
{
    "username": "Mushy",
    "email": "hello@gmail.com",
    "first_name": "Robert",
    "last_name": "Andrew",
    "password": "hellohello123"
}

REPONSE
{
    response: "There was an error submitting your form.",
    errors: [
        {"username": "Username is already taken."},
        {"email": "Email is already taken"}
    ]
}
or 
{
    "status": 200,
    response: "There was an error submitting your form.",
    errors: [
        {"username": "Username is already taken."},
        {"email": "Email is already taken"}
    ]
}

