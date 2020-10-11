# pygame-framework
  A game framework written in Python using PyGame

# Installation
  This framework only requires PyGame as a dependency. Other dependencies can be added by users if they wish.

# Usage
  The goal of this project was to generalize a game loop with event and collision handling using an object-oriented approach. This takes some of the work out of developing games with PyGame, allowing users to develop a wide array of objects for different purposes
  
  ## To install/run a game
   ##### Make sure that Python and pygame are installed. On Windows, this can be done on Powershell by simply typing `python`. If it is not installed, it will take you to the Windows Store page to install it.
   ##### Once python is installed, run `pip install pygame` in the Powershell window to install pygame.
   ##### Once pygame is installed, navigate to the base directory of the game (this is where the `app.py` file is located) and run `python app.py`. The game should load and begin playing.

## Classes


## `Game`
  The main game class, found in game.py. This is where the game loop, event, and collision handling are done. This class also hold a list of GameObjects.

## Variables

##### `_settings(obj)`
  Stores the game settings as a JSON object.

##### `_gameObjects(array)`
  Stores all instantiated GameObjects

##### `_size(tuple)`
  The width and height of the screen

##### `_io_queue(array)`
  An array storing all IO events

##### `_threads(array)`
  A list of threads started by the program

## Methods

##### `loadSettings(file)`
  Loads the settings file and stores the resulting object in the _settings object.

##### `getGameObjectByName(string)`
  Takes a string as an input and searches the _gameObjects array for the first instance of an object with that name, and returns a reference to that object.

##### `instantiate(GameObject)`
  Adds the passed GameObject to the _gameObjects array and returns the instantiated object.

##### `remove(GameObject)`
  Removes the passed GameObject from the _gameObjects array.

##### `handleEvents(event)`
  Handles events; this is mostly just placing the events into _io_queue so that they can be processed by other objects later, but also handles the pygame.QUIT event

##### `findEvent(event_type)`
  Searches the event queue for the type of event passed to the function. Returns None if not present.

##### `run()`
  Runs the game
  
  
  
  
  

## `GameObject`
  The base class for all objects in the Game.

## Variables

##### `_x(Number)`
  The X coordinate of the object

##### `_y(Number)`
  The Y coordinate of the object

##### `_name(String)`
The name of the object

##### `_bounds(pygame.Rect)`
  The boundaries of the object. Initially set to None, the bounds are calculated when _image is loaded.

##### `_image(pygame.Surface)`
  The GameObject's image. The default is an unknown.png that consists of only a single transparent pixel.

## Methods

##### `getName()`
  Returns the name of the object as a string.

##### `getPos()`
  Returns the position of the object as a tuple.

##### `start()`
  This function is run once upon the GameObject's instantiation.

##### `update()`
  This function is run once per frame.

##### `collision(other_obj)`
  Called if another object(referenced by `other_obj`) collides with this object
  
  
  
  
  

## `GameManager` (inherits from GameObject)
  The Game Manager class. This is a gateway for the user to define their own game events, and instantiates the initial objects. Ideally, the user only makes changes to game_manager.py and leaves game.py alone (though the user is free to do what they wish, of course)

## Variables
  None, all are defined by the user or are inherited from GameObject
  
## Methods

##### `start()`
  This function is called once upon the object's initialization. This is where the user might want to instantiate the initial GameObjects.

##### `update()`
  This function is called once per frame. This is where the user would place any logic that needs to be run constantly, i.e.,     the game loop.
