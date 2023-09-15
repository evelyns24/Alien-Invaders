"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

# Evelyn Si es828
# 12/7/21
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    # Attribute _direction: direction of where the Aliens are moving
    # Invariant: _direction is a String that's either 'left' or 'right'
    #
    # Attribute _down: True if the Aliens moved down in previous animation frame
    # Invariant: _down is a boolean
    #
    # Attribute _randomBolt: random rate at which the Aliens will fire a Bolt
    # Invariant: _randomBolt is an int that is between 1 and BOLT_RATE
    #
    # Attribute _alienStep: number of steps since the previous alien bolt is shot
    # Invariant: _alienStep is an int that's >=0
    #
    # Attribute _animating: the animation coroutine for Ship
    # Invariant: _animating is a coroutine or None
    #
    # Attribute _below: True if any Aliens go below defense line
    # Invariant: _below is a boolean
    #
    # Attribute _death: True if Ship exploded
    # Invariant: _death is a boolean



    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLives(self):
        """
        Recturns the _lives attribute
        """
        return self._lives


    def getDeath(self):
        """
        Returns the _animating attribute
        """
        return self._death


    def getAliens(self):
        """
        Returns the _aliens attribute
        """
        return self._aliens


    def getBelow(self):
        """
        Returns the _below attribute
        """
        return self._below


    def setShip(self,s):
        """
        Sets the _ship attribute equal to s

        Parameter s: the new value for _ship
        Precondition: s is a Ship object
        """
        assert isinstance(s,Ship)
        self._ship=s


    def setDeath(self):
        """
        Revives the Ship by changing the _death attribute to False
        """
        self._death=False


    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        self._ship=Ship()
        self._ship.frame=0
        self._initListOfAliens()
        self._bolts=[]
        self._dline=GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
                          linecolor='black', linewidth=2)
        self._lives=SHIP_LIVES
        self._time=0
        self._direction='right'
        self._down=False
        self._randomBolt=random.randint(1,BOLT_RATE)
        self._alienStep=0
        self._animating=None
        self._below=False
        self._death=False



    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Animates the Ship, Bolts, and Aliens

        Parameter input: the key that the user presses
        Precondition: input is instance of GInput

        Parameter dt: time since last animation frame
        Precondition: dt is a float
        """
        if (self._direction=='right'):
            self._moveAliensRight(dt)
        else:
            self._moveAliensLeft(dt)
        self._makeAlienBolts(dt)
        self._fireAlienBolt()
        self._collide(input,dt)
        if (self._animating!=None):
            try:
                self._animating.send(dt)
            except StopIteration:
                self._ship=None
                self._animating=None
                self._bolts.clear()
                self._death=True
        else: #ship no die
            if(input.is_key_down('up') and self._canFirePlayer()):
                self._bolts.append(Bolt(self._ship.x,self._ship.top,BOLT_SPEED))
            self._moveShip(input)
            self._firePlayerBolt()
        self._below=self._alienUnder()




    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the Ship, Aliens, defensive line, and Bolts

        Parameter view: the game view
        Precondidtion: view is an instance of GView
        """
        if (self._ship!=None):
            self._ship.draw(view)
        for r in range(len(self._aliens)):
            for c in range(len(self._aliens[0])):
                if (self._aliens[r][c]!=None):
                    self._aliens[r][c].draw(view)
        for b in self._bolts:
            b.draw(view)
        self._dline.draw(view)


    # HELPER METHOD TO INITIALIZE THE 2D LIST WITH ALIENS
    def _initListOfAliens(self):
        """
        Initializes the _aliens attribute
        """
        self._aliens=[]
        image=-1
        for row in range(ALIEN_ROWS):
            x=ALIEN_WIDTH/2+ALIEN_H_SEP
            if (row==0):
                y=GAME_HEIGHT-(ALIEN_CEILING+((ALIEN_ROWS-1)*
                  (ALIEN_V_SEP+ALIEN_HEIGHT))+ALIEN_HEIGHT/2)
            else:
                y=y+ALIEN_HEIGHT+ALIEN_V_SEP
            alist=[]
            if (row%2==0):
                image=(image+1)%(len(ALIEN_IMAGES))
            for col in range(ALIENS_IN_ROW):
                a=Alien(x,y,ALIEN_IMAGES[image])
                alist.append(a)
                if (col==ALIENS_IN_ROW-1):
                    self._aliens.insert(0,alist)
                else:
                    x=x+ALIEN_WIDTH+ALIEN_H_SEP


    # HELPER METHOD TO MOVE SHIP
    def _moveShip(self,input):
        """
        Moves Ship left if user presses the left key and right if the user
        presses the right key. If no keys were pressed, then the Ship doesn't
        move

        Parameter input: the key that the user presses
        Precondition: input is instance of GInput
        """
        if(self._ship!=None):
            if (input.is_key_down('right')==True):
                self._ship.move(SHIP_MOVEMENT)
            elif (input.is_key_down('left')==True):
                self._ship.move(-1*SHIP_MOVEMENT)


    # HELPER METHOD TO MOVE ALIENS
    def _moveAliensRight(self,dt):
        """
        Moves all Aliens to the right. If the Aliens are going to go offscreen,
        then move the ALiens down

        Parameter dt: time since last animation frame
        Precondition: dt is a float
        """
        self._time=self._time+dt
        if (self._time>=ALIEN_SPEED):
            self._alienStep=self._alienStep+1
            col=self._leftMost()
            if (self._aliens[0][col].right+ALIEN_H_SEP>=GAME_WIDTH and
                self._down==False):
                for row in range(len(self._aliens)):
                    for col in range(len(self._aliens[0])):
                        if(self._aliens[row][col]!=None):
                            y=self._aliens[row][col].y-ALIEN_V_WALK
                            self._aliens[row][col].y=y
                self._time=0
                self._down=True
                self._direction='left'
            else:
                for row in range(len(self._aliens)):
                    for col in range(len(self._aliens[0])):
                        if(self._aliens[row][col]!=None):
                            self._aliens[row][col].x=(self._aliens[row][col].x+
                                                      ALIEN_H_WALK)
                self._time=0
                self._down=False
                self._direction='right'


    # HELPER METHOD TO MOVE ALIENS LEFT
    def _moveAliensLeft(self,dt):
        """
        Moves all Aliens to the left. If the Aliens are going to go offscreen,
        then move the ALiens down

        Parameter dt: time since last animation frame
        Precondition: dt is a float
        """
        self._time=self._time+dt
        if (self._time>=ALIEN_SPEED):
            self._alienStep=self._alienStep+1
            col=self._rightMost()
            if (self._aliens[0][col].left-ALIEN_H_SEP<=0 and
                self._down==False):
                for row in range(len(self._aliens)):
                    for col in range(len(self._aliens[0])):
                        if (self._aliens[row][col]!=None):
                            y=self._aliens[row][col].y-ALIEN_V_WALK
                            self._aliens[row][col].y=y
                self._time=0
                self._down=True
                self._direction='right'
            else:
                for row in range(len(self._aliens)):
                    for col in range(len(self._aliens[0])):
                        if (self._aliens[row][col]!=None):
                            self._aliens[row][col].x=(self._aliens[row][col].x-
                                                      ALIEN_H_WALK)
                self._time=0
                self._down=False
                self._direction='left'

    # HELPER METHOD THAT DETERMINES THE RIGHTMOST COLLUMN THAT HAS AlIEN(s)
    def _rightMost(self):
        """
        Returns the rightmost collumn of _aliens that has at least one Alien
        """
        for col in range(len(self._aliens[0])):
            if(self._aliens[0][col]!=None):
                return col


    # HELPER METHOD THAT DETERMINES THE LEFTMOST COLLUMN THAT HAS ALIEN(s)
    def _leftMost(self):
        """
        Returns the leftmost collumn of _aliens that has at least one Alien
        """
        for col in range(len(self._aliens[0])):
            l=len(self._aliens[0])
            if(self._aliens[0][l-1-col]!=None):
                return l-1-col


    # HELPER METHOD TO DETERMINE IF THERE'S ALREADY A PLAYER BOLT IN _bolts
    def _canFirePlayer(self):
        """
        Returns True if player can fire and False otherwise
        """
        output=True
        for x in self._bolts:
            if (x.isPlayerBolt()==True):
                output=False
        return output


    # HELPER METHOD TO FIRE THE PLAYER BOLT
    def _firePlayerBolt(self):
        """
        Moving the player Bolt. When the bolt goes offscreen, it will be removed
        """
        for x in self._bolts:
            if (x.isPlayerBolt()==True):
                i=self._bolts.index(x)
                if (self._bolts[i].bottom+self._bolts[i].getVelocity()<=
                    GAME_HEIGHT):
                    self._bolts[i].move()
                else:
                    self._bolts.remove(x)

    # HELPER METHOD FOR PICKING RANDOM NONEMPTY COLUMN OF ALIEN(s)
    def _randomCol(self):
        """
        Returns a nonempty random column from _aliens
        """
        r=random.randint(0,len(self._aliens[0])-1)
        while self._aliens[0][r]==None:
            r=random.randint(0,len(self._aliens[0])-1)
        return r


    # HELPER METHOD TO FIND ROW OF THE BOTTOM MOST ALIEN IN THE C COLLUMN
    def _bottomAlien(self,c):
        for r in range(len(self._aliens)):
            if self._aliens[r][c]==None:
                return r-1
            if r==len(self._aliens)-1:
                return r


    # HELPER METHOD FOR CREATING ALIEN BOLTS
    def _makeAlienBolts(self,dt):
        """
        Creating Alien Bolts to fire at random rate between 1 and BOLT_RATE

        Paramter dt: time since last animation frame
        Precondition: dt is a float
        """
        if self._alienStep>=self._randomBolt:
            col=self._randomCol()
            r=self._bottomAlien(col)
            a1=self._aliens[r][col]
            self._bolts.append(Bolt(a1.x,a1.y,-1*BOLT_SPEED))
            self._alienStep=0
            self._randomBolt=random.randint(1,BOLT_RATE)


    # HELPER METHOD TO FIRE THE ALIEN BOLT
    def _fireAlienBolt(self):
        """
        Moving the Alien Bolt. When the bolt goes offscreen, it will be removed
        """
        for x in self._bolts:
            if (x.isPlayerBolt()==False):
                i=self._bolts.index(x)
                if (self._bolts[i].top+self._bolts[i].getVelocity()>=0):
                    self._bolts[i].move()
                else:
                    self._bolts.remove(x)


    # HELPER METHODS FOR COLLISION DETECTION
    def _collide(self,input,dt):
        """
        Check if there are any collisions between the bolt and the Ship,
        if they do collide, then player loses one live, Ship explodes, that
        bolt is removed from _bolts, and player is not allowed to move Ship or
        shoot. This method also checks the collision between the bolt and the
        Aliens. If they do collide then set that Alien equal to None
        """
        for b in self._bolts:
            if(self._ship!=None and self._ship.collide(b)):
                self._animating=self._ship.animateShip()
                next(self._animating)
                self._lives=(self._lives-1)%3
                self._bolts.remove(b)
            for c in range(len(self._aliens[0])):
                a=self._aliens[self._bottomAlien(c)][c]
                if(a!=None):
                    if (a.collide(b)):
                        self._aliens[self._bottomAlien(c)][c]=None
                        self._bolts.remove(b)


    # HELPER METHOD TO DETERMINE IF ANY OF THE ALIENS ARE BELOW THE DEFENSE LINE
    def _alienUnder(self):
        """
        Returns True if the lowest Alien in _aliens is below the defense line;
        otherwise return False
        """
        for r in range(len(self._aliens)):
            for c in range(len(self._aliens[0])):
                if (self._aliens[len(self._aliens)-1-r][c]!=None):
                    a=self._aliens[len(self._aliens)-1-r][c]
                    if(a.bottom<=self._dline.top):
                        return True
        return False
