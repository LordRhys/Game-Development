import tcod as libt
from game_messages import Message

class Fighter:
    def __init__(self, hp, defense, power, xp=0, coins=0):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.xp = xp
        self.coins = coins  # for use later with npc merchants, coins dropped by mobs or sold items

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp, 'coins': self.coins})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def add_coins(self, coins):
        self.coins += coins        

    def spend_coins(self, coins):
        if self.coins - coins < 0:
            return None # add message about not enough coins

        self.coins -= coins 

    def attack(self, target):
        results = []

        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(self.owner.name.capitalize(), 
                                                target.name, str(damage)), libt.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(self.owner.name.capitalize(), 
                                                                                            target.name), libt.white)})

        return results
