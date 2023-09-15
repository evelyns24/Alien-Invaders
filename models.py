"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

# Evelyn Si es828
# 12/7/21
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GSprite):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self,x=GAME_WIDTH/2, y=SHIP_BOTTOM+SHIP_HEIGHT/2,
                 width=SHIP_WIDTH, height=SHIP_HEIGHT, source=SHIP_IMAGE,
                 format=(2,4)):
        """
        Initializes the Ship object
        """
        super().__init__(source=source,format=format,
                         x=x,y=y,width=width,height=height)


    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def move(self,x):
        """
        Moves the Ship x pixels to the right from its center if x>0;
        otherwise moves Ship x pixels to the left from its center.

        Prevents Ship from getting offscreen

        Parameter x: the number of pixels the Ship should move horizontally
        Precondition: x is a float or int
        """
        if (self.x+x<=GAME_WIDTH-self.width/2 and self.x+x>=self.width/2):
            self.x=self.x+x
        elif (self.x+x<self.width/2):
            self.x=self.width/2
        else:
            self.x=GAME_WIDTH-self.width/2


    def collide(self,b):
        """
        Returns True if a Alien bolt collides with the Ship;
        otherwise return False.

        This method also returns False if the bolt was not fired from an Alien

        Parameter b: the Alien bolt
        Precondition: b is a Bolt object
        """
        assert isinstance(b,Bolt), "b is not a Bolt object"
        if (b.isPlayerBolt()==True):
            return False
        topRight=(b.right,b.top)
        topLeft=(b.left,b.top)
        bottomRight=(b.right,b.bottom)
        bottomLeft=(b.left,b.bottom)
        if (self.contains(topRight)):
            return True
        if (self.contains(topLeft)):
            return True
        if (self.contains(bottomRight)):
            return True
        if (self.contains(bottomLeft)):
            return True
        return False


    # COROUTINE METHOD TO ANIMATE THE SHIP
    def animateShip(self):
        """
        Coroutine to animate the Ship explosion
        """
        time=0
        while time<DEATH_SPEED:
            dt=(yield)
            time=time+dt
            self.frame=int((time/DEATH_SPEED)*7)


    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,x,y,s,width=ALIEN_WIDTH,height=ALIEN_HEIGHT):
        """
        Initializes the Alien object

        Parameter x: horizontal coordinate of the center of the object
        Precondition: x is a float or int

        Parameter y: vertical coordinate of the center of the object
        Precondition: y is a float or int

        Parameter s: source file for the image
        Precondition: s is a strings refering to a valid file
        """
        super().__init__(x=x,y=y,width=width,height=height,
                       source=s)


    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collide(self,b):
        """
        Returns True if a player bolt collides with an Alien;
        otherwise return False.

        This method also returns False if the bolt was not fired from player

        Parameter b: the player bolt
        Precondition: b is a Bolt object
        """
        assert isinstance(b,Bolt), "b is not a Bolt object"
        if (b.isPlayerBolt()==False):
            return False
        topRight=(b.right,b.top)
        topLeft=(b.left,b.top)
        bottomRight=(b.right,b.bottom)
        bottomLeft=(b.left,b.bottom)
        if (self.contains(topRight)):
            return True
        if (self.contains(topLeft)):
            return True
        if (self.contains(bottomRight)):
            return True
        if (self.contains(bottomLeft)):
            return True
        return False


    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVelocity(self):
        """
        Returns the _velocity attribute
        """
        return self._velocity


    def move(self):
        """
        Moves the Bolt in the y direction by _velocity pixels
        """
        self.y=self.y+self.getVelocity()

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,vel,width=BOLT_WIDTH,height=BOLT_HEIGHT):
        """
        Initializes the Bolt

        Parameter x: horizontal coordinate of the center of the Bolt object
        Precondition: x is a float or int

        Parameter y: vertical coordinate of the center of the Bolt object
        Precondition: y is a float or int

        Parameter vel: horizontal velocity of the bolt
        Precondition: vel is a float or int
        """
        super().__init__(x=x,y=y,width=width,height=height,
                       fillcolor='black')
        self._velocity=vel

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        Returns true if the Bolt is shot from the player;
        otherwise, return False
        """
        if(self.getVelocity()<0):
            return False
        return True


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
