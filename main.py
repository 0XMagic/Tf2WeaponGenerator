import pyglet
import scenes
import stat_generator


class Application(pyglet.window.Window):
	def __init__(self):
		super().__init__()
		self.set_size(1280, 720)
		#all active elements
		self.scene = {
				"class_limit": scenes.DropDownBox(
						"All Classes",
						"Scout", "Soldier", "Pyro",
						"Demoman", "Heavy", "Engineer",
						"Medic", "Sniper", "Spy",
						caption = "Class"
				).pos(8, 558).size(5),
				"slot_limit":  scenes.DropDownBox(
						"All Slots",
						"Primary", "Secondary", "Melee",
						"PDA",
						caption = "Slot"
				).pos(8, 630).size(5),
				"w_strength":  scenes.DropDownBox(
						"Ridiculous", "Strong", "Normal", "Weak", "What?",
						caption = "Weapon Power"
				).pos(8, 484).size(5).set_text("Normal"),
				"go":          scenes.Button("Generate!", lambda: self.gen_weapon()).pos(8, 8).size(3, 1.25),
				"nwr":         scenes.CheckBox("No stat restrictions").pos(8, 192).size(1.3, 1.3),
				"x100":        scenes.CheckBox("TF2X100").pos(8, 64).size(1.3, 1.3),
				"nrc":         scenes.CheckBox("No Random Critical Hits").pos(8, 128).size(1.3, 1.3),
				"item":        scenes.WeaponContainer().pos(1280-500,720-32)
		}

		#elements that can be clicked on
		self.interactive = [
				"class_limit", "slot_limit", "w_strength", "nwr", "x100", "nrc", "go"
		]

	def on_draw(self):
		self.clear()
		for x in self.scene.values():
			x.draw()

	def on_mouse_press(self, x, y, button, modifiers):
		for c in self.interactive:
			self.scene[c].on_click(x, y, 1)

		#prevent menus from being clicked if they are covered by something else
		self.scene["class_limit"].active = not self.scene["slot_limit"].state
		self.scene["w_strength"].active = not (self.scene["slot_limit"].state or self.scene["class_limit"].state)

	def gen_weapon(self):

		g = stat_generator.Generator()
		g.slot_filter = self.scene["slot_limit"].text.text
		g.class_filter = self.scene["class_limit"].text.text
		g.power = self.scene["w_strength"].text.text
		g.x100 = self.scene["x100"].state
		g.nrc = self.scene["nrc"].state
		g.nwr = self.scene["nwr"].state
		if not g.is_valid():
			print("\nERROR:\tPDA is only available on Engineer and Spy")

		w = g.generate()



		exp = w.export()
		txt = exp["text"]

		_u_alt = txt[0]
		_u = txt[1]
		_d_alt = txt[2]
		_d = txt[3]
		self.scene["item"].up_alt.text = _u_alt
		self.scene["item"].up.text = _u

		self.scene["item"].down_alt.text = _d_alt
		self.scene["item"].down.text = _d


		self.scene["item"].active = True
		self.scene["item"].set_item_title(w.w_class,w.w_type)

		pass


if __name__ == "__main__":
	Application()
	pyglet.app.run()
