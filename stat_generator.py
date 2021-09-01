import json
import random
import os


def text_gen(d, x100 = False):
	random.seed += 12
	rs = random.randint(d["min"], d["max"]) * d["mul"]
	return d["text"].format(rs * (1 + 99 * x100))


#object where the weapon is stored
class ItemResult:
	def __init__(self, cl, tp,x100=False):
		self.w_class = cl
		self.w_type = tp
		self.up = []
		self.down = []
		self.seed = 0
		self.x100 = x100

	def export(self):
		random.seed = self.seed
		_u = [
				[x for x in self.up if x["white text"]],
				[x for x in self.up if not x["white text"]]
		]
		_d = [
				[x for x in self.down if x["white text"]],
				[x for x in self.down if not x["white text"]]
		]
		#the text colors are here
		r_up = '\n'.join([text_gen(w,x100=self.x100) for w in _u[0]])
		r_upw = '\n'.join([text_gen(w,x100=self.x100) for w in _u[1]])
		r_do = '\n'.join([text_gen(w,x100=self.x100) for w in _d[0]])
		r_dow = '\n'.join([text_gen(w,x100=self.x100) for w in _d[1]])

		return {"Class": self.w_class, "Type": self.w_type, "text": [r_up, r_upw, r_do, r_dow]}


class Generator:
	def __init__(self, seed = None):
		self.slot_filter = "All Slots"
		self.class_filter = "All Classes"
		self.power = "Normal"
		self.x100 = False
		self.nrc = False
		self.nwr = False
		self.seed = seed if seed is not None else random.randint(0, 2 ** 32)
		self.recent = None

	def __str__(self):
		t5 = "".join(["\t"] * 5)
		e10 = "".join(["="] * 10)
		t3 = "".join(["\t"] * 3)
		t2 = "".join(["\t"] * 2)
		return '\n'.join(
				[
						f"{e10}WEAPON DETAILS{e10}",
						f"Generator power:{t2}{self.power}",
						f"Class:{t5}{self.class_filter}",
						f"Slot:{t5}{self.slot_filter}",
						f"Seed:{t5}{self.seed}",
						f"No Random Crits:{t2}{self.nrc}",
						f"Restrictions:{t3}{not self.nwr}",
						f"multiply by 100:{t2}{self.x100}"

				]
		)

	def is_valid(self):
		#prevent the PDA slot from working if a class that doesnt have a PDA is filtered
		s_pda = self.slot_filter == "PDA"
		f_class = self.class_filter in ("Engineer", "Spy", "All Classes")
		return self.nwr or (not s_pda or (s_pda and f_class))

	def generate(self):

		with open("assets/data.json", "r") as fl:
			js = json.load(fl)

		cf = self.class_filter
		sf = self.slot_filter

		w = js.get("weapons")
		s = js.get("stats")

		if cf != "All Classes":
			w = {x: y for x, y in w.items() if cf in x}

		if sf != "All Slots":
			w = {x: y for x, y in w.items() if sf in x}

		wp = random.choice(list(w.keys()))

		sg = [s[x] for x in w[wp]["+"]]
		sb = [s[x] for x in w[wp]["-"]]

		#in the future, have this be linked to text boxes
		ng = 3
		nb = 3

		result = ItemResult(
				wp.split(".")[0],
				wp.split(".")[-1],
				x100 = self.x100
		)
		random.seed = self.seed
		result.seed = self.seed

		_u = random.sample(sg, min(ng, len(sg)))
		random.seed += 21
		_u_ids = [x["uid"] for x in _u]
		sb = [x for x in sb if x is not None and x["uid"] not in _u_ids]
		_d = random.sample(sb, min(nb, len(sb)))
		random.seed += 12
		result.up = _u
		result.down = _d
		self.recent = result
		return result


"""
if run by itself, it will print a random weapon with hard-coded adjustments
used for debugging

use the gui to get actual use out of this file
"""
if __name__ == "__main__":
	import stat_json_generator

	stat_json_generator.main()
	g = Generator()
	#g.class_filter = "Spy"
	#g.slot_filter = "PDA"
	g.generate()
