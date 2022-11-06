# DeCempions
Fun small project to play with and learn about Flask framework. Simple guessing game based on your favourite league that you can play with your friends!

## Getting started
To run this project you have to clone or download this repository, with the command:
```bash
git clone https://github.com/A-725-K/DeCempions
```
Then you have to install the `Python3` libraries using the requirements file:
```bash
python3 -m pip install -r requirements.txt
```
Before playing you have to create a `.env` file in the `decempions` directory similarly to `.env.example` with your own personal configuration. Remember also to change the value of the admin token in `decempions/database/decempions.sql` to avoid weak password easy guessing!

Finally you can run `flask run` in the home of the project to start the server, and go to `http://localhost:16000` in your browser to play the game!

Last step before finally enjoying the game, initialize the DB by running:
```bash
flask init-db
```

## Note
I am ***NOT*** a UI developer, and the styling has been made with bare CSS and a lot of effort to learn it better :smile: It is "*responsive*" but the best experience you will get is on a monitor with resolution `1440 × 900`, like the monitor I used to develop the project.

## Future features?
- [ ] Dockerize the project
- [ ] Introduce the *League* concept
  - [ ] Handle multiple leagues
- [ ] Administrator panel/dashboard:
  - [ ] League statistics and overview
  - [ ] Insert/Edit results
  - [ ] Manage players
- [ ] Better handling of next week:
  - [ ] Let the user change/update the guess for the next week
- [ ] Pagination in ranking page
- [ ] Let the users upload their profile pictures
- [ ] Write unit and integration tests
- [ ] Improve UX
- [ ] Improve UI
  - [ ] Better responsiveness
- [ ] Improve security
- [ ] Fix bugs (I am 100% sure there are some :wink:)

## Author

* ***Andrea Canepa*** - 2022
