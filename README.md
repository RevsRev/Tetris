# Tetris
Basic Tetris game written in python, using matplotlib for user interface

There are some issues with this game - it was one of my first projects in python with little coding experience before so needs a lot of improvement, which currently I do not have the time to do.
The biggest issue is an error in the logic to do with rotating the long 4x1 piece close to the right wall - I tried to take a shortcut in the coding and as a result there is an infinite recursion in one specific scenario. It's a quick fix, but I haven't had the time to do this yet (soon). Main other issue is the keyboard events handler isn't great, and you cant see what pieces come next. I hope to redo this game (perhaps using pyglet rather than matplotlib) at some point.

To play, import Tetris and type Tetris.play_tetris()
