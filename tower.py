'''
Created on Feb 20, 2015

@author: 33271
'''
import pygame
import logging
import math, os
import random
from Bullet import *
import logging

logger = logging.getLogger(__name__)
logger.setLevel(100)
path = os.path.dirname(__file__)


class Tower(pygame.sprite.Sprite):

    # Name of this tower type
    name                = "Tower"
    # The image of this tower type. This image must fit into the maze cell
    img                 = "round_barell.png"
    # This is a trick to be able to display the range of the tower when selected
    # The image is a circle with 100 pixels radius, its scale can be adjusted to
    # show the actual range
    range_img           = "range.png"
    # Description of tower type
    description         = "normal tower"
    # switches to make the tower sellable/upgradeable
    sellable            = True
    upgradeable         = True
    # the maximum level of the tower type. this indicates how many entries the
    # upgrades lists must have
    max_level           = 6
    # deprecated, the corrosponding functions shall be used
    cost                = 5
    min_dmg             = 5
    max_dmg             = 10
    # switches to make the tower attack only land/air
    ground_only         = False
    air_only            = False
    # upgrade values for this tower type
    upgrades            = {
                        'damage'        : [(5,10),(4,9),(9,9),(9,15),(20,30),(80,90)],
                        'range'         : [51, 52, 53, 54,55, 150],
                        'reload_time'   : [0.5, 0.49, 0.48, 0.47, 0.48, 2],
                        'cost'          : [5, 6, 7, 10, 100]
    }

    def __init__(self, game):
        """
        initializes attributes and drawing stuff
        @param game: the game the tower plays in
        @type game: L{Game}
        """
        super(Tower, self).__init__(game.loader.image(type(self).img))
        self.rand_sprite = pygame.sprite.Sprite(game.loader.image("tower_rand.png"))
        self.rand_sprite.xy = super(Tower, self).attrgetter("xy")
        # how fast we rotate. this adds up to the reload timer and possibly we
        # we rotate to a target that is no longer in range when we get there, so
        # if this is too low, we will never shoot at a target because we constantly
        # rotate to targets no longer in range
        self.rotation_speed     = 3000
        # reference to our parent
        self.game               = game
        # the current target and whether we have one
        self.targeted           = False
        self.target             = None
        self.upgrading = False
        # if true, we will continue to shoot at our target until it is no longer
        # in range or dead, otherwise we chose a target after each shot
        self.target_lock        = True
        # function to select the target from all the ones in range
        self.select_target      = self.select_target_close_to_exit
        # seconds of silence after a shot
        self.reload_time        = 1
        # at the beginning, we are idle
        self.state              = 0
        # timestamp of the last shot to mesure the reload time
        self.last_shot          = 0
        # faktor inidicating how much of our cost will be returned if the tower is sold
        self.value_faktor       = 0.8
        # our current value
        self.value              = int(type(self).cost * self.value_faktor)
        # true if we block the movement of creeps
        self.blocking           = True
        # sprite displaying our range
        self.range_sprite       = MySprite(game.loader.image(Tower.range_img))
        self.range_sprite.xy    = super(Tower, self).attrgetter("xy")

        self.experience         = 0
        self.total_damage       = 0
        # the type of bullets we shoot
        self.bullet_type        = Bullet
        # the current level
        self.level              = 0
        # set our current damage values
        self._set_min_max_damage()
        # switch to mark activity
        self.active             = True
        # initial sell timer
        self.sell_timer         = 0.5
        # if true we rotate to our target, else we shoot right away
        self.rotation_tower     = True
        # switches for boosted attributes
        self.boosted            = {'damage' : False, 'range' : False, 'speed' : False}
        # the improvements the attributes have through boosts
        self.boost_improvement  = {'damage':0, 'range':0, 'speed':0}
        # the unboosted values of our attributes
        self.boost_fallback     = {'damage':0, 'range':0, 'speed':0}
        # a sprite to mark us as boosted
        self.boost_sprite       = MySprite(game.loader.image("boosted_tower.png"))
        self.boost_sprite.xy    = super(Tower, self).attrgetter("xy")
        # range must include setting the bounding radius for intrusion detection
        # so there is a function for it
        self.set_range(self.upgrades["range"][self.level])
        self.show_rand = False

    def show_tower_rand(self):
        """
        shows a surrounding box
        """
        self.show_rand = True

    def hide_tower_rand(self):
        """
        hides the surrounding box
        """
        self.show_rand = False

    def render(self):
        """
        this is overridden to show the bounding box if needed
        """
        if self.show_rand:
            self.rand_sprite.render()
        super(Tower, self).render()

    def sanity_check(self):
        """
        debug method to schedule when fixing tower locks
        @deprecated: shouldn't be used, by definiton
        """
        pass

    def on_bullet_die(self, bullet):
        """
        callback when one of our bullets dies
        @param bullet: the dieing bullet
        @type bullet: L{Bullet}
        """
        #print "bullet is dead, removing"
        self.game.remove_item(bullet)

    def is_boosted(self):
        """
        return true if we are boosted
        @rtype: Boolean
        """
        return self.boosted['damage'] or self.boosted['range'] or self.boosted['speed']

    def _start_boost_animation(self):
        """graphical start of boosting"""
        self.game.add_item(self.boost_sprite, "other")

    def _stop_boost_animation(self):
        """graphical end of boosting"""
        self.game.remove_item(self.boost_sprite)

    def boost(self, type, improvement):
        """boost attribute type by improvement"""
        # sanity check
        if not type in self.boost_fallback:
            logger.error("unsupported boost: " + str(type))
            return
        # if this is the first boost of this attribute, we have to store
        # the current value for fallback
        if not self.boosted[type]:
            # if it is the first boos overall, we have to show it
            if not self.is_boosted():
                self._start_boost_animation()
            # mark type as boosted
            self.boosted[type] = True
            # store the attribute for fallback
            if type == 'damage':
                self.boost_fallback['damage'] = (self.min_damage, self.max_damage)
            elif type == 'range':
                self.boost_fallback['range'] = self.range
            elif type == 'speed':
                self.boost_fallback['speed'] = self.reload_time
            else:
                logger.error("unimplemented boost type: " + str(type))
                return
        # add the improvement
        self.boost_improvement[type] += improvement
        # transfer the boost to the attribute
        if type == 'damage':
            self._boost_damage()
        elif type == 'range':
            self._boost_range()
        elif type == 'speed':
            self._boost_speed()

    def unboost(self, type, improvement):
        """unboost attribute type by improvement"""
        if not type in self.boost_fallback:
            logger.error("unsupported boost: " + str(type))
            return
        # lower the improvement
        self.boost_improvement[type] -= improvement
        # transform the remaining improvement to the attribute
        if type == 'damage':
            self._boost_damage()
        elif type == 'range':
            self._boost_range()
        elif type == 'speed':
            self._boost_speed()
        else:
            logger.error("unimplemented boost type: " + str(type))
        # if we are not improved any longer, the attribute is not boosted any more
        if self.boost_improvement[type] == 0:
            self.boosted[type] = False
            # if we are not boosted at all any more, remove the visible boost
            if not self.is_boosted():
                self._stop_boost_animation()

    def _boost_damage(self):
        """
        adjusts the damage to the boosted values
        """
        # apply the current improvement to the damage
        # if we are not boosted, this does nothing
        self.min_damage = int(self.boost_fallback['damage'][0] * (1 + self.boost_improvement['damage']))
        self.max_damage = int(self.boost_fallback['damage'][1] * (1 + self.boost_improvement['damage']))

    def _boost_range(self):
        """
        adjusts the range to the boosted value
        """
        # apply the current improvement to the range
        # if we are not boosted, this does nothing
        self.set_range( self.boost_fallback['range'] * (1 + self.boost_improvement['range']))

    def _boost_speed(self):
        """
        adjusts the speed to the boosted value
        """
        # apply the current improvement to the reload time
        # if we are not boosted, this does nothing
        self.reload_time = self.boost_fallback['speed'] * (1 - self.boost_improvement['speed'])

    def _set_min_max_damage(self):
        """
        sets the damage values based on the level
        """
        # sets min/max damage attributes based on our current level
        self.min_damage = type(self).upgrades['damage'][self.level][0]
        self.max_damage = type(self).upgrades['damage'][self.level][1]

    def activate(self):
        """
        activates the tower
        """
        # set active and enter state idle to be noticed about intruders
        self.active = True
        self.state = 0

    def deactivate(self):
        """
        deactivates the tower
        """
        # set inactive and enter idle. the tower will not be notified of intruders
        # because only active towers get notified
        #print id(self), ": Deactivate"
        self.active = False
        self.state = 0

    def rotate_to(self, point):
        """Rotates the tower to point to point"""
        # if we are not a rotating tower, call rotation stop and exit
        self.state = 1
        if not self.rotation_tower:
            self.rotation_stop()
            return
        logger.debug("rotating from " + str(self.xy) + " to " + str(point))

        # the sinus of our angle to the point is gegenkathete / hypothenuse
        hypo    = math.hypot(abs(self.x - point[0]), abs(self.y - point[1]))
        kath    = abs(self.x - point[0])
        sinTo   = kath/hypo
        # to geht the angle out of the sinus, we have to pass this to sin^(-1)
        # and transform the result from bogenmass to degrees
        angle   = math.degrees(math.asin(sinTo))
        #print "Hypothenuse ", hypo
        #print "Gegenkathete ", kath
        #print "Sinus ", sinTo
        #print "angle ", angle
        # dependant on where the creep is relative to us, we have to
        # normalize the angle
        if point[0] < self.x:
            if point[1] < self.y:
                # point is left/down from us, we have to move angle backwards
                angle = 360 - angle
            else:
                # point is left up, we have to move the angle additional to
                # a half turn
                angle = 180 + angle
        else:
            if point[1] < self.y:
                # thats the case the angle is correct
                pass
            else:
                # point is right up, we have to move a half turn and then
                # angle backwards
                angle = 180 - angle
        #print "normalized angle ", angle
        # time for the rotation
        time            = max(angle / self.rotation_speed, 0.1)
        # linear rotation
        #self.rot        = rabbyt.lerp(end = angle, dt = time)
        #print "rotating for ", time
        # schedule the callback for the rotation stop
        self.game.clock.schedule_once(self.rotation_stop, time)
        #rabbyt.scheduler.add(rabbyt.get_time() + time, self.rotation_stop)
        #print self.number,": rotation stop in ", time

    def rotation_stop(self, dt=0):
        """Callback when a rotation has stopped"""
        #print self.number,": ",dt
        # if we are active
        if self.active and self.target and self.target.active:
            if self._is_in_range(self.target):
                # if the target is still in range, shoot
                self.state = 2
                self.shoot()
            else:
                # if not, go idle to receive a new one
                self.state = 0
        elif not self.active:
            print ("Tower.rotation_stop on non-active tower")
            logger.debug("Tower.rotation_stop on non-active tower")
        else:
            self.state = 0

    def shoot(self):
        """ shoots the target """
        if self.active:
            print ("SCHUSS")
            logger.debug("shoot: " + str(self.target) + ". time: " + str(self.game.clock.get_time()))
            # make a bullet
            bullet = self.bullet_type(self)
            # set its target
            bullet.set_target(self.target)
            # and damage
            bullet.set_damage(self.get_damage())
            # as well as position
            bullet.xy = self.xy
            # set it loose
            bullet.fire()
            # tell the game it is there
            self.game.add_item(bullet, "Bullet")
            if not self.target_lock:
                #schedule to go idle when the reload timer is up
                self.game.clock.schedule_once(self.go_idle, self.reload_time)
                #rabbyt.scheduler.add(rabbyt.get_time() + self.reload_time, lambda: self.state_transition(Tower.STATE[0]))
            else:
                # schedule to rotate again when the reload timer is up
                self.game.clock.schedule_once(self.reshoot, self.reload_time)
                #rabbyt.scheduler.add(rabbyt.get_time() + self.reload_time, lambda: self.state_transition(Tower.STATE[1]))
        else:
            self.state = 0
            logger.error("Tower.shoot on non-active Tower")

    def set_rotation_speed(self, speed):
        """setter for the speed"""
        self.rotation_speed     = speed

    def set_range(self, range):
        """setting the range must affect the bounding radius"""
        self.range              = range
        self.bounding_radius    = range
        self.range_sprite.scale = self.range / 50.
        logger.debug("range set to " + str(range))
        #print "range set to ", str(range)

    def get_damage(self):
        """hook for defining the towers damage"""
        return random.randint(int(self.min_damage), int(self.max_damage))

    def get_damage_string(self):
        """returns a string representation of the damage for the info window"""
        #print str(self.min_damage) + " - " + str(self.max_damage)
        return str(int(self.min_damage)) + "-" + str(int(self.max_damage))

    def get_cost(self):
        """
        hook for computing the cost of a tower
        """
        return self.cost

    def process_intruder(self, intruders):
        """
        Called from the game when the tower is idle and creeps come into range.
        It selects one of the creeps as a target.
        @param intruders: the creeps in my range
        @type intruders: list of L{Creep}
        """
        #if self.state == 1:
            #print self.number,": passing intruders: rotating"
        #    return
        #if self.state == 2:
            #print self.number,": passing intruders: reloading"
        #    return
        good = self._filter_intruders(intruders)
        #print "zumindest", good
        if len(good) == 0:
            #print "false alarm!! tower.process_intruder"
            return
        # select one of the creeps
        self.target = self.select_target(good)
        logger.debug("Target set to " + str(self.target))
        #if not self.target or not self.target.active:
        #    print id(self),":target set to ",str(self.target)
        # start rotating
        self.rotate_to(self.target.xy)


    def _filter_intruders(self, intruders):
        """
        filters the list of incomming intruders.
        @return: the filtered list of creeps. All creeps that remain are potential targets
        """
        # deprecated test
        #false = [(intruder, self._get_distance_to_creep(intruder)) for intruder in intruders if self._get_distance_to_creep(intruder) > self.range]
        #if len(false) > 0:
        #    self.logger.error("Received intrusion of creeps that are out of range: " + str(false))
        #good = [c for c in intruders if not c in [f[0] for f in false]]
        good = intruders
        # filter for air creeps if we are ground_only
        if self.ground_only:
            good = [c for c in good if not c.flying]
        # or for air if we are air only
        elif self.air_only:
            good = [c for c in good if c.flying]
        return good

    def select_target_random(self, intruders):
        """ randomly selects a target """
        pos = random.randint(0, len(intruders) - 1)
        res = intruders[pos]
        #print id(self),":selected #", pos, ": ", res, " out of: ", intruders
        return res

    def select_target_close_to_exit(self, intruders):
        """
        @return: the intruder of the list which has the lowest cost to the exit
        """
        intruders.sort(lambda a,b:cmp(a.distance_to_exit, b.distance_to_exit))
        return intruders[0]

    def select_target_distance(self, intruders):
        """
        selects the closest target
        @return: the intruder of the list which is closest to the tower
        """
        intruders.sort(lambda a,b:cmp(self._get_distance_to_creep(a), self._get_distance_to_creep(b)))
        return intruders[0]

    def select_target_unpoisoned(self, intruders):
        """selects the (nearest) unpoisoned target or the nearest"""
        intruders.sort(lambda a,b:cmp(self._get_distance_to_creep(a), self._get_distance_to_creep(b)))
        for creep in intruders:
            if not creep.poisoned:
                return creep
        return intruders[0]

    def go_idle(self, dt=0):
        """
        switches state to idle
        @param dt: ignored

        """
        #print "Idle: ", dt
        self.state = 0

    def reshoot(self, dt=0):
        """
        shoots the same target again.
        @param dt: ignored
        """
        #print "ReShoot: ", dt
        self.rotate_to(self.target.xy)



    def process_hit(self, bullet):
        """Called when the bullet has hit its target"""
        logger.debug("process_hit")
        # give us the experience
        self.experience += bullet.experience
        #print "added experience ", bullet.experience
        self.total_damage += bullet.damage_dealt
        # remove the bullet from the screen
        self.game.remove_item(bullet)
        # if we killed the creep
        if bullet.target.dead and bullet.target.last_tower == self:
            # process it
            self.process_kill(bullet.target)

    def process_leak(self, creep):
        """
        hook to define behavior when a creep leakes. per default, nothing is done
        @param creep: ignored
        """
        pass
        #if self.target == creep:
        #    self.logger.debug("Tower.process_leak(" + str(creep) + ")")
        #    self.state = 0

    def process_kill(self, creep):
        """Called when we killed a creep"""
        logger.debug("Tower.process_kill(" + str(creep) + ")")
        # remove it from the screen
        #self.game.remove_item(creep)
        # if it is our current target
        #if (creep == self.target):
            # go idle
        self.game.process_kill(self, creep)


    def process_dead_creep(self, creep):
        """
        hook to define behavior when a creep dies. per defualt, nothing is done
        @param creep: ignored
        """
        #if (creep == self.target):
        #    self.state = 0
        pass

    def _get_distance_to_creep(self, creep):
        """computes the distance to the creep"""
        distance = math.hypot(abs(self.x - creep.x), abs(self.y - creep.y))
        #print "Distance to ", creep, distance
        return distance

    def _is_in_range(self, creep):
        """checks whether the creep is in range"""
        if not creep or not creep.active or creep.dead:
            return False
        return self._get_distance_to_creep(creep) <= self.bounding_radius

    def sell(self):
        """called when this tower is sold"""
        if self.active:
            self.game.remove_bullets(self)
        else:
            logger.debug("Tower.sell on non-active tower")

    def is_sellable(self):
        """
        @return: True if the tower can be sold.
        """
        return type(self).sellable

    def select(self):
        """called when this tower is selected"""
        if self.active:
            #MySprite.select(self)
            #print "select"
            self.game.add_item(self.range_sprite, "other")
        else:
            logger.debug("Tower.sell on non-active tower")

    def unselect(self):
        """called when this tower is unselected"""
        #MySprite.unselect(self)
        self.game.remove_item(self.range_sprite)

    def upgrade(self):
        """upgrades the tower one level"""
        if self.active:
            if self.level < type(self).max_level:
                self.value += int(self.get_upgrade_cost() * self.value_faktor)
                self.level += 1
                # the sell timer is currently computed statically, this should change
                self.sell_timer *= 1 + (self.level / 10.)
                # if an attribute is boosted we have to unboost,
                # upgrade and boost again
                if self.boosted["range"]:
                    range_boost = self.boost_improvement["range"]
                    self.unboost("range", range_boost)
                    self.set_range(self.upgrades['range'][self.level])
                    self.boost("range", range_boost)
                else:
                    self.set_range(self.upgrades['range'][self.level])
                if self.boosted["speed"]:
                    speed_boost = self.boost_improvement["speed"]
                    self.unboost("speed", speed_boost)
                    self.reload_time = self.upgrades['reload_time'][self.level]
                    self.boost("speed", speed_boost)
                else:
                    self.reload_time = self.upgrades['reload_time'][self.level]
                if self.boosted["damage"]:
                    damage_boost = self.boost_improvement["damage"]
                    self.unboost("damage", self.boost_improvement["damage"])
                    self._set_min_max_damage()
                    self.boost("damage", damage_boost)
                else:
                    self._set_min_max_damage()
                self.upgrading = False
                print ("upgraded: ", self.level, self.reload_time, self.range)
        else:
            logger.debug("Tower.sell on non-active tower")

    def upgrade_anim(self, time):
        """special upgrade anims can be defined here"""
        self.upgrading = True
        target = self.alpha
        #self.alpha = rabbyt.lerp(start = 0, end = target, dt = time)

    def get_upgrade_cost(self):
        """returns the cost for the next upgrade"""
        if self.level < self.max_level:
            ret = self.upgrades['cost'][self.level]
            return ret
        return "max"

    def is_at_max_level(self):
        """returns true if this tower is maxed out"""
        #print self.level, " <> ", self.max_level
        return self.level >= self.max_level