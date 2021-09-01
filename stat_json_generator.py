"""
does not run with the main script (don't import this!)
this is used to generate assets/data.json
so much easier to do it procedurally!

run this if you fucked up the data file
"""
import os
import json

uid = 0


#probabillities for stats in each power mode
class Weight:
	def __init__(self, what, weak, normal, strong, ridiculous):
		self.what = what
		self.weak = weak
		self.normal = normal
		self.strong = strong
		self.ridiculous = ridiculous

	def export(self):
		return {
				"what?":      self.what,
				"weak":       self.weak,
				"normal":     self.normal,
				"strong":     self.strong,
				"ridiculous": self.ridiculous
		}


class Number:
	def __init__(self, name, *args, white_text = False):
		self.up_text = ""
		self.down_text = ""
		self.range_up = [0, 0]
		self.range_down = [0, 0]
		self.mul_up = 0
		self.mul_down = 0
		self.tags = args
		self.name = name
		self.weight_up = Weight(0, 0, 0, 0, 0)
		self.weight_down = Weight(0, 0, 0, 0, 0)
		global uid
		uid += 1
		self.uid = uid
		self.no_up = True
		self.no_down = True
		self.white_text = white_text

	def up(self, text, r_min, r_max, mul, weight = Weight(0, 1, 1, 1, 1)):
		self.up_text = text
		self.range_up = [r_min, r_max]
		self.mul_up = mul
		self.weight_up = weight
		self.no_up = False
		return self

	def down(self, text, r_min, r_max, mul, weight = Weight(1, 1, 1, 1, 0)):
		self.down_text = text
		self.range_down = [r_min, r_max]
		self.mul_down = mul
		self.weight_down = weight
		self.no_down = False
		return self

	def export(self):
		result = {
				"+": {
						"uid":        self.uid,
						"white text": self.white_text,
						"text":       self.up_text,
						"min":        self.range_up[0],
						"max":        self.range_up[1],
						"mul":        self.mul_up,
						"weight":     self.weight_up.export()
				},
				"-": {
						"uid":        self.uid,
						"white text": self.white_text,
						"text":       self.down_text,
						"min":        self.range_down[0],
						"max":        self.range_down[1],
						"mul":        self.mul_down,
						"weight":     self.weight_down.export()
				}}

		if self.no_up:
			result.pop("+")
		if self.no_down:
			result.pop("-")
		return self.name, self.tags, result


def generate(*args):
	wep = dict()
	lb = dict()
	lb_i = dict()
	n = 0
	for x in args:
		name, tag, content = x.export()

		c1 = content.get("+", None)
		s1 = str(c1)
		if s1 not in lb_i:
			lb[n] = c1
			lb_i[s1] = str(n)
			n += 1

		c2 = content.get("-", None)
		s2 = str(c2)
		if s2 not in lb_i:
			lb[n] = c2
			lb_i[s2] = str(n)
			n += 1

		for t in tag:
			if t not in wep:
				wep[t] = {
						"+": list(),
						"-": list()
				}
			if s1 in lb_i:
				wep[t]["+"].append(str(lb_i[s1]))
			if s2 in lb_i:
				wep[t]["-"].append(str(lb_i[s2]))

	result = {
			"weapons": wep,
			"stats":   lb
	}
	fp = "assets/data.json"
	with open(fp, "w" if os.path.isfile(fp) else "a") as fl:
		json.dump(result, fl, indent = 1)
		pass

	pass


#combine lists, removing duplicates
def join(*args):
	result = list()
	for x in args: result += [y for y in x if y not in result]
	return result


#remove all entries of exc from base
def exclude(base, exc):
	return [x for x in base if x not in exc]


#only items that are in both a and b
def intersect(a, b):
	return [x for x in a if x in b]


#get all items that have a string segment
def kw(ls, p):
	return [x for x in ls if p in x]


#shortcut for joining lists based on keywords
def kw_join(a, b):
	return join(*[kw(a, x) for x in b])


"""
Number(name, *tags)
.up/down(text,min,max,mul,weight)

doing string operations like this are slow af but the end user doesnt have to run it so whatever
"""


def main():
	item = [
			"Scout.Primary.Scattergun",
			"Scout.Secondary.Pistol",
			"Scout.Secondary.Jar",
			"Scout.Secondary.Cleaver",
			"Scout.Secondary.Lunchbox",
			"Scout.Melee.Bat",
			"Scout.Melee.Baseball Bat",

			"Soldier.Primary.Rocket Launcher",
			"Soldier.Primary.Laser Launcher",
			"Soldier.Secondary.Shotgun",
			"Soldier.Secondary.Indivisible particle smasher",
			"Soldier.Secondary.Banner",
			"Soldier.Secondary.Boots",
			"Soldier.Melee.Shovel",
			"Soldier.Melee.Pickaxe",
			"Soldier.Melee.Whip",

			"Pyro.Primary.Flamethrower",
			"Pyro.Primary.Flame Launcher",
			"Pyro.Secondary.Shotgun",
			"Pyro.Secondary.Flaregun",
			"Pyro.Secondary.Gas can",
			"Pyro.Melee.Axe",
			"Pyro.Melee.Hammer",

			"Demoman.Primary.Grenade Launcher",
			"Demoman.Primary.Boots",
			"Demoman.Secondary.Stickybomb Launcher",
			"Demoman.Secondary.Shield",
			"Demoman.Melee.Sword",
			"Demoman.Melee.Bottle",

			"Heavy.Primary.Minigun",
			"Heavy.Secondary.Shotgun",
			"Heavy.Secondary.Lunchbox",
			"Heavy.Melee.Fists",

			"Engineer.Primary.Shotgun",
			"Engineer.Primary.Laser gun",
			"Engineer.Primary.Bolt gun",
			"Engineer.Secondary.Wrangler",
			"Engineer.Secondary.Short circuit",
			"Engineer.Secondary.Pistol",
			"Engineer.Melee.Wrench",
			"Engineer.Melee.Robot arm",
			"Engineer.PDA.PDA",

			"Medic.Primary.Needle gun",
			"Medic.Primary.Crossbow",
			"Medic.Secondary.Medigun",
			"Medic.Melee.Bonesaw",

			"Sniper.Primary.Sniper Rifle",
			"Sniper.Primary.Bow",
			"Sniper.Secondary.Backpack",
			"Sniper.Secondary.Smg",
			"Sniper.Secondary.Jar",
			"Sniper.Melee.Kukri",

			"Spy.Primary.Revolver",
			"Spy.Secondary.Sapper",
			"Spy.Melee.Knife",
			"Spy.PDA.Watch",
			"Spy.PDA.Ringer"

	]

	w_no_damage = kw_join(item, [
			".Jar", ".Sapper", ".PDA", ".Backpack", ".Lunchbox", ".Wrangler", ".Medigun", ".Boots", ".Banner"
	])

	w_damage = exclude(item, w_no_damage)

	w_bullets = kw_join(w_damage, [
			"Minigun", "Revolver", "Sniper Rifle", "Smg",
			"Shotgun", "Pistol", "Scattergun"
	])

	w_projectile = kw_join(item, [
			"Cleaver", "Jar", "Baseball Bat", "Launcher", "Bow", "Crossbow", "Bolt gun", "Indivisible particle smasher",
			"Short circuit",
			"Gas can", "Flaregun"
	])

	w_clip = exclude(
			w_damage,
			kw_join(w_damage,
			        ["Flaregun", "Cleaver", "Baseball Bat", "Bow", "Flamethrower", "Minigun", "Melee", "Flame","circuit"])
	)

	w_explosive = exclude(
			w_projectile,
			kw_join(w_damage, [
					"Cleaver", "Baseball Bat", "Bow", "Crossbow", "Bolt gun", "Indivisible particle smasher",
					"Engineer.Primary.Laser gun"
			])
	)

	generate(
			Number("clip", *w_clip).up(
					"{}% increased clip size", 1, 20, 10
			).down(
					"{}% decreased clip size", 1, 9, 10
			),

			Number("damage", *w_damage).up(
					"{}% damage bonus", 1, 12, 10
			).down(
					"{}% damage reduction", 1, 9, 10
			),

			Number("rate", *exclude(w_damage, ["Pyro.Primary.Flamethrower"])).up(
					"{}% Faster fire rate", 1, 25, 10
			).down(
					"{}% Slower fire rate", 1, 9, 10
			),

			Number("hp_passive", *item).up(
					"{}% increased health on wearer", 2, 10, 5
			).down(
					"{}% decreased health on wearer", 1, 5, 10
			),

			Number("hp_passive_regen", *item).up(
					"+{} health regenerated per second", 2, 10, 5
			),

			Number("flame_life", *kw_join(item, ["Pyro.Primary"])).up(
					"+{}% flame particle life", 1, 20, 10
			).down(
					"-{}% flame particle life", 1, 9, 10
			),

			Number("flame_speed", *kw_join(item, ["Pyro.Primary"])).up(
					"+{}% flame speed", 1, 20, 10
			).down(
					"-{}% flame speed", 1, 9, 10
			),

			Number("flame_size", *kw_join(item, ["Pyro.Primary"])).up(
					"+{}% flame size", 1, 20, 10
			).down(
					"-{}% flame size", 1, 9, 10
			),

			Number("whole_clip", *w_clip).up(
					"Fires the whole clip at once!", 1, 2, 3
			),

			Number("beggars", *w_clip).up(
					"Hold Fire to load clip\nRelease to unleash a barrage", 1, 2, 3
			),
			Number("bullets_per_shot_multi", *kw_join(item, ["Shotgun", "Minigun", "Scattergun"])).up(
					"+{}% bullets per shot", 1, 8, 25
			).down(
					"-{}% bullets per shot", 1, 9, 10
			),

	)


if __name__ == "__main__":
	main()
