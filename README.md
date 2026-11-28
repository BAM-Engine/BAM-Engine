# BAM-Engine
Game Engine
Python scripts (excluding backend stuff, like that of Socket), are Proof of Concept (POC) only.
Rust & C++ versions are to come soon

# Explosion: The language of BAM! Engine
File extension: `.exp`
Example Script:
```
tree.root(scene); -- The path to the scene
tree.inherit(nodeType); -- What main node the scene is

use keyboard;
use output;

-- Variable Declerations:
new int myInt;
myInt = 5;

new double myDouble;
myDouble = 0.2;

new string myString;
myString = "This is my string.";

new bool myBool;
myBool = false;

-- Proper Examples:
new int moveSpeed;
moveSpeed = 5;

new reference kb;
kb = keyboard;

-- Reference object from the engine tree
new tree.call(objectType) myObject;
myObject.path = "myPath";

def openRun {
  ; -- The same as Python's `pass` statement
}

def mainLoop {
  output.extend(tick as t, f"New Tick: {t}");
  
  if (kb.action == "a") {
    myObject.move(new translate(-moveSpeed:0));
  } else if (kb.action == "d") {
    myObject.move(new translate(moveSpeed:0));
  }

  if (kb.action == "w") {
    myObject.move(new translate(0:moveSpeed));
  } else if (kb.action == "s") {
    myObject.move(new translate(0:-moveSpeed));
  }

  -- Keeps loop running
  -- The bool `stillTicking` is a hidden (undeclared) variable that checks if the mainLoop (the same as _process in Godot 4) is still running
  -- `tick` is the same as `delta`
  if (stillTicking == true) {
    tick++;
  }
}
```
