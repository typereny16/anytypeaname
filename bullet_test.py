'''
Created on Feb 18, 2015

@author: 33271
'''
import math,os
import logging
import pygame

path = os.path.dirname(os.path.dirname(__file__))

logger = logging.getLogger("pytower.Bullet")
logger.setLevel(logging.INFO)
path = os.path.dirname(__file__)

#Taken From: http://bazaar.launchpad.net/~pytower-heros/pytower/main/view/head:/pyTower/Bullet.py
class Bullet(pygame.sprite.Sprite):
    name = "Bullet"
    adjustment_time = 0.2

    def __init__(self, tower, img = None, shape = None):
        """
        img and shape are used exclusively, if no img is given, the shape is
        processed. If an img is given, shape is ignored.

        @type tower: L{Tower}
        @param tower: The L{Tower} that has shot this bullet
        @param img: The texture to instantiate the Sprite with
        @param shape: The rectangular shape parameters to instantiate the Sprite
        """
        """if not img:
            if not shape:
                pygame.sprite.Sprite.__init__(self, None, shape = (2,-2,-2,2))
            else:
                pygame.sprite.Sprite.__init__(self, None, shape = shape)
            self.rgba   = (0, 0, 1, 0.3)
        else:
            pygame.sprite.Sprite.__init__(self, img)"""
        #self.setSpeed(100)
        self.tower  = tower
        self.target = None
        self.damage = -1
        self.damage_dealt = 0
        self.alive  = True
        self.experience = 0
        logger.debug("Created Bullet " + str(id(self)))

    def set_target(self, creep):
        """
        This is a hook to overwrite when the bullet needs to take action once its
        target changes

        @type creep: L{Creep}
        @param creep: The new target
        """
        self.target = creep

    def set_damage(self, damage):
        """
        This is a hook to overwrite when the bullet needs to take action once its
        damage changes

        @type damage: numeric
        @param damage: the new damage
        """
        self.damage = damage

    def check_ready(self):
        """
        This method is called before the bullet is shot to check if everything is
        in place.
        """
        if self.target == None:
            raise Exception("Called fire() on bullet without target")
        if self.damage < 0:
            raise Exception("Called fire() on bullet with negative damage")
        logger.debug("Bullet " + str(id(self)) + " ready")

    def _adjust(self, dt=0):
        """
        This method updates the movement to the current destination of the target
        """
        if not self.target.active:
            self.arrival_on_target()
            return
        self.destination = self.target.xy
        self.adjust_movement()

    def fire(self):
        """
        The Bullet calls L{check_ready}, starts moving towards its target and
        schedules periodic adjustment to the targets position
        """
        self.check_ready()
        self.moveTo(self.target.xy, self.arrival_on_target)
        self.tower.game.clock.schedule_interval(self._adjust, self.adjustment_time)

    def arrival_on_target(self, dt=0):
        """
        Called upon arrival. Unschedules periodic movement adjustment and notifies
        the target and the tower
        """
        #print self, " arrived at ", self.target, ". Passing to the creep and tower."
        self.tower.game.clock.unschedule(self._adjust)
        if self.alive:
            #print "living bullet arrived at target"
            logger.debug(str(self) + " arrived at destination")
            self.target.process_hit(self)
            self.tower.process_hit(self)
        else:
            #print "dead bullet arrived at target"
            logger.debug("Dead Bullet arrived at destination")

    def die(self, dt=0):
        """
        Called when the bullet dies.  Notifies the tower
        """
        self.alive = False
        self.tower.on_bullet_die(self)

class SeekingBullet(Bullet):
    name = "SeekingBullet"
    def __init__(self, tower):
        """
        @type tower: L{Tower}
        @param tower: The L{Tower} which fired the bullet
        """
        super(SeekingBullet, self).__init__(tower, shape = (2,-2,-2,2))
        #self.setSpeed(80)
        self.rgba = (1,0,0,1)
        self.seek_interval = 0.1
        self.boundling_radius = 3
        self.glow_interval = 0.3
        self.speed_improval = 4
        self.start_delay = 0.2
        self.retarget_range = 150
        self.glow()

    def fire(self):
        """
        Calls L{check_ready} and schedules L{seek} to be called after the
        start delay
        """
        self.check_ready()
        self.tower.game.clock.schedule_once(self.seek, self.start_delay)

    def seek(self, dt=0):
        """
        seeks a new target if the current one is no longer present, alive and
        active, also accelerates towards the target
        """
        if self.target.leaked or self.target.dead or not self.target.active:
            #print "target no longer there, dieing!"
            self.retarget()
            return
        distance = math.hypot(self.x - self.target.x, self.y - self.target.y)
        #print id(self), " is ", distance, " away from the target"
        if distance < 5:
            self.arrival_on_target()
        else:
            #self.setSpeed(self.speed + self.speed_improval)
            time = distance/self.speed
            faktor = self.seek_interval / time
            moving_time = time * faktor
            m_x = -(self.x - self.target.x) * faktor
            m_y = -(self.y - self.target.y) * faktor
            #print self.x, self.x + m_x, moving_time
            #print self.y, self.y + m_y, moving_tme
            self.x = self.x + m_x
            self.y = self.y + m_y
            self.tower.game.clock.schedule_once(self.seek, moving_time)
            
    def retarget(self):
        """
        sets the target to a new one or lets the bullet die if none is in range
        """
        new_target = self.tower.game.get_closest_creep(self.xy, self.retarget_range, self.tower.ground_only, self.tower.air_only)
        if new_target:
            self.target = new_target
            #print "Bullet retargetet to ", new_target
            self.seek(0)
        else:
            self.die()

    def arrival_on_target(self, dt=0):
        """
        unschedules the seeking and calls the super method
        """
        clock.unschedule(self.seek)
        super(SeekingBullet, self).arrival_on_target(self)
