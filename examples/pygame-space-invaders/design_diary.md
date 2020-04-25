# Space Invaders Design Diary

Over spring break I developed this PyGame framework in order to simplify making games in PyGame, using an object-oriented approach.  After downloading the art and music assets and examining the original code, it was relatively easy to create all of the necessary objects to replicate the game under this framework. From there, I was able to make several additions to the game, including:
  * A clickable pause menu with a Resume/Quit button,
  * A score and wave counter,
  * Enemies spawn in waves and get faster each wave, as does the player's fire rate,
  * A Boss-type enemy, which requires several shots to take down but is much slower

Overall the game functions well, although the gameplay is not practical beyond a few waves. Additionally, bosses become much easier as your fire rate increases, since your bullets do the same amount of damage to it. Changes to the mechanics of the bullets and enemies could solve these issues, but as a technical demonstration, this game shows some of what can be done in PyGame.

![MenuGif](https://github.com/abbottjord94/pygame-framework/blob/master/examples/pygame-space-invaders/menu.gif)
