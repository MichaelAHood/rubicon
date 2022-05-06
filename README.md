# Overview

**Note:** For instructions on running the code jump down to the section titled **How to Run This Code**.

This repo contains code that I created over the last several days while attempting to solve Rubicon. It is a work in progress as my knowledge about how to use browser dev tools and javascript were nonexistent three days ago.

# How we got here

First, a little background on how I ended up with this current incarnation of a solution.

After playing about a dozen games of Rubicon the rules were mostly clear. Then it was relatively straightforward to beat the AI. However, when attempting to play against the "robo" adversaries -- the ones with the absurdly low five second limit -- it was obvious that the only way to win was to somehow "cheat" and get an edge over the AI. 

Following the breadcrumbs left by the Eng team led me to investigate the Chrome dev tools and discover `src/auto-move.js` and the ability to modify some of that file's functions. I also discovered the console which allowed me to run arbitrary Javascript. As I have been recently playing Security CTF games, my first thought was to begin playing around with board state and game state to see if I could give myself something akin to God Mode.

My attempts to assign myself nodes or change node ownership using the board state object didn't go anywhere. The same with game state, as I hoped I might be able to assign myself extra moves. Alas, there was no `timeRemaining` field in the game state that I could modify. I realized that the board and game state were read only. There didn't appear to be any obvious means to send modified local state objects back to the server. Since I could run basically any Javascript I wanted in the console, I thought there might be some kind of public methods available that I could use to serialize json and post it back to the game server. This proved to be a dead end.

I next realized that the methods in `auto-move.js` comprise the essential functional components of a reinforcement learning (RL) environment. The game outputs environment state represented by the `boardState` and `gameState` objects, and accepts input actions in the form of `nodeIds`. 

From here, I needed to figure out how to programmatically get data in and out of the browser environment. I had heard of local storage, but didn't really know much about it. I discovered it was fairly easy to use Chromedriver to read/write to browser local storage. Now I could modify the functions in `auto-move.js` to send game data to local storage, and read the actions that my -- as of yet to be created -- RL agent would submit.

While alternating between reading literature for using RL in 2-player full information games, I occasionally stopped to play Rubicon myself. I hoped to get a better intuition for how to best represent the game and what kinds of RL approaches may work. However, I soon noticed something rather surprising. The AI always appears to make the same moves for a given configuration of the board. In other words it appeared to have no stochastic element to the moves it played. This means that moves I used to win earlier games should work every time. They just needed to be executed by a program that submits all the moves in less than 5 seconds. This was a relief because I was planning on spending at least a week training, evaluating, and tweaking an agent to play this game. The last three nights of staying up late to nerd out on this challenge were starting to take a toll. I needed to sleep. But first, I needed to win.

With this insight, I decided to go for the quick win before somebody at Synthesis pushed a code update that broke my highly effective yet extremely overfit strategy.

# How to Run This Code

Get chromedriver if you don't have it:
```
make setup
```
Note: the `get_chromedriver.sh` script assumes you are running on a mac, so change the chromedriver version as necessary.

Install the dependencies.
```
make env
```

Run linter checks, if you want.
```
make lint
```

There are three "policies" to use: `baby`, `julius`, and `caesar`. Run them like so:
```
make POLICY=caesar play-rubicon
```
This will launch the browser and copy the modified Javascript to your clipboard that you can use to override the contents of `src/auto-move.js` using the browser developer tools. Be sure to hit `cmd-s` to save. Then click to start the game. Make sure you pick the opponent that corresponds to your specified policy, e.g. the `baby` policy should work on `Baby Julius`, `Genius Baby`, and `Robo Baby`.

Have fun!

**Note 1:** The `baby` policy is the only policy that doesn't win by crossing the Rubicon. Rather it obtains a commanding lead and once no more moves are taken, you have to click on the `Pass` button in order to win.

**Note 2:** After the python script `play_rubicon.py` uses `chromedriver` to get the website, it waits a default period of 10 seconds before it begins polling the browser local storage to determine if the game has begun. If you somehow manage to open the browser, dev tools, paste the new contents of `src/auto-move.js`, and start the game before 10 seconds are up, then nothing will happen until the full 10 second time has elapsed.

# To Do:
- Figure out how to programmatically override the contents of `src/auto-move.js` in the browser. This way we don't have to open dev tools every time. Maybe `selenium` can do this.
- Create a proper RL policy that responds to changes in game state, rather than a manual one tailored to each opponent.