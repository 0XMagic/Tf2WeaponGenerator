import pyglet

#this is where all the hard-coded stuff goes
pyglet.font.add_file("assets/tf2build.ttf")
font = pyglet.font.load("TF2 Build")
images = {
		"common": pyglet.image.ImageGrid(
				pyglet.image.load("assets/common.png"),
				512 // 32, 512 // 32
		)
}

graphics = {
		"box border":  images.get("common")[(512 // 32 - 1, 6)],
		"arrow":       images.get("common")[(512 // 32 - 1, 7)],
		"checkbox":    images.get("common")[(512 // 32 - 1, 0)],
		"check":       images.get("common")[(512 // 32 - 1, 1)],
		"button_side": images.get("common")[(512 // 32 - 1, 2)],
		"button":      images.get("common")[(512 // 32 - 1, 3)]

}


class WeaponContainer:
	def __init__(self):
		self.active = False
		self.title = self.text = pyglet.text.Label(
				"new item acquired", font_name = 'TF2 Build', anchor_x = 'center', anchor_y = 'center', font_size = 45,
				color = (236, 227, 203, 255)
		)
		self.you = self.text = pyglet.text.Label(
				"you", font_name = 'TF2 Build', anchor_x = 'center', anchor_y = 'center', font_size = 30,
				color = (236, 227, 203, 255)
		)
		self.found = self.text = pyglet.text.Label(
				"found", font_name = 'TF2 Build', anchor_x = 'center', anchor_y = 'center', font_size = 30,
				color = (201, 79, 57, 255)
		)
		self.item_name = self.text = pyglet.text.Label(
				"a new ??? for ???", font_name = 'TF2 Build', anchor_x = 'center', anchor_y = 'center', font_size = 25,
				color = (255, 216, 0, 255)
		)
		self.up_alt = self.text = pyglet.text.Label(
				"good stats (alternate text color)", font_name = 'TF2 Build', anchor_x = 'center', anchor_y = 'center',
				multiline = True, width = 400, color = (236, 227, 203, 255)
		)
		self.up = self.text = pyglet.text.Label(
				"good stats", font_name = 'TF2 Build', anchor_x = 'center', anchor_y = 'center',
				multiline = True, width = 400,color = (122, 160, 197, 255)
		)
		self.down_alt = self.text = pyglet.text.Label(
				"bad stats (alternate text color)", font_name = 'TF2 Build', anchor_x = 'center', anchor_y = 'center',
				multiline = True, width = 400, color = (236, 227, 203, 255)
		)
		self.down = self.text = pyglet.text.Label(
				"bad stats", font_name = 'TF2 Build', anchor_x = 'center', anchor_y = 'center',
				multiline = True, width = 400, color = (255, 62, 62, 255)
		)
		self.pos(0, 0)

	def pos(self, x, y):
		self.title.position = (x, y)
		_t = 65
		self.you.position = (x - _t, y - 70)
		self.found.position = (x + _t, y - 70)
		self.item_name.position = (x, y - 120)

		self.up_alt.position = (x - 250, y - 180)
		self.up.position = (x - 250, y - 180 - self.up_alt.content_height)

		self.down_alt.position = (x + 250, y - 180)
		self.down.position = (x + 250, y - 180 - self.up_alt.content_height)
		return self

	def update(self):
		self.pos(*self.title.position)

	def set_item_title(self, w_class, w_type):
		self.item_name.text = f"a new {w_type} for {w_class}"

		if w_type.endswith("s"):
			self.item_name.text = self.item_name.text[2:]

	def draw(self):
		if not self.active: return
		self.title.draw()
		self.you.draw()
		self.found.draw()
		self.item_name.draw()
		self.up_alt.draw()
		self.up.draw()
		self.down_alt.draw()
		self.down.draw()


class Button:
	def __init__(self, text, on_press):
		self.function = on_press
		self.active = True
		self.state = False
		self.side_l = pyglet.sprite.Sprite(img = graphics.get("button_side"), subpixel = True)
		self.side_r = pyglet.sprite.Sprite(img = graphics.get("button_side"), subpixel = True)
		self.middle = pyglet.sprite.Sprite(img = graphics.get("button"), subpixel = True)
		self.side_r.rotation = 180
		self.text = pyglet.text.Label(
				text, font_name = 'TF2 Build', anchor_x = 'center', anchor_y = 'center'
		)
		self.pos(0, 0)

	def size(self, x, y):
		self.side_l.scale_y = y
		self.side_r.scale_y = y
		self.middle.scale_x = x
		self.middle.scale_y = y
		self.pos(*self.side_l.position)

		return self

	def pos(self, x, y):
		self.side_l.position = (x, y)
		self.middle.position = (x + 32, y)
		self.side_r.position = (x + 64 + self.middle.scale_x * 32, y + 32 * self.middle.scale_y)
		self.text.position = (
				self.middle.position[0] + 16 * self.middle.scale_x,
				self.middle.position[1] + 16 * self.middle.scale_y
		)
		return self

	def on_click(self, x, y, mode):
		if not self.active:
			return
		x1, y1 = self.side_l.position
		x2, y2 = x1 + 64 + 32 * self.middle.scale_x, y1 + 32 * self.middle.scale_y
		click = (x1 <= x <= x2) * (y1 <= y <= y2)
		if click:
			self.function()

	def draw(self):
		self.side_l.draw()
		self.side_r.draw()
		self.middle.draw()
		self.text.draw()


class CheckBox:
	def __init__(self, text):
		self.active = True
		self.state = False
		self.box = pyglet.sprite.Sprite(img = graphics.get("checkbox"), subpixel = True)
		self.check = pyglet.sprite.Sprite(img = graphics.get("check"), subpixel = True)
		self.text = pyglet.text.Label(
				text, font_name = 'TF2 Build'
		)
		self.pos(0, 0)

	def size(self, x, y):
		self.box.scale_x = x
		self.box.scale_y = y
		self.check.scale_x = x
		self.check.scale_y = y

		self.pos(*self.box.position)
		return self

	def pos(self, x, y):
		self.box.position = (x, y)
		self.check.position = (x, y)
		self.text.position = (x + 8 + 32 * self.box.scale_x, y + 16)
		return self

	def on_click(self, x, y, mode):
		if not self.active:
			return
		x1, y1 = self.box.position
		x2, y2 = x1 + 32 * self.box.scale_x, y1 + 32 * self.box.scale_y
		click = (x1 <= x <= x2) * (y1 <= y <= y2)
		if click:
			self.state = not self.state

	def draw(self):
		self.box.draw()
		self.text.draw()
		if self.state:
			self.check.draw()


class DropDownBox:
	def __init__(self, *args, caption = "no name"):
		self.active = True
		self.state = False
		self.box = [
				pyglet.sprite.Sprite(img = graphics.get("box border"), subpixel = True),
				pyglet.sprite.Sprite(img = graphics.get("box border"), subpixel = True),
				pyglet.sprite.Sprite(img = graphics.get("box border"), subpixel = True),
				pyglet.sprite.Sprite(img = graphics.get("box border"), subpixel = True)
		]
		for n, b in enumerate(self.box):
			b.rotation = 90.0 * n

		self.arrow = pyglet.sprite.Sprite(img = graphics.get("arrow"))
		self.tc = args
		self.caption = pyglet.text.Label(
				caption, font_name = 'TF2 Build'
		)
		self.text = pyglet.text.Label(
				args[0], font_name = 'TF2 Build'
		)
		self.content = [pyglet.text.Label(
				x, font_name = 'TF2 Build'
		) for x in args]

		self.pos(0, 0)
		self.size(1)

	def set_text(self, t):
		self.text.text = t
		return self

	def pos(self, x, y):
		self.box[0].position = (x, y)
		self.box[1].position = (x + 32 * (self.box[0].scale_x - 1), y + 32)
		self.box[2].position = (x + 32 * self.box[0].scale_x, y + 32 - self.state * 32 * len(self.tc))
		self.box[3].position = (x + 32, y - self.state * 32 * len(self.tc))
		self.arrow.position = (x + 32 * (self.box[0].scale_x - 1) - 4, y + 32 * self.state)
		self.text.position = (x + 4, y + 9)
		self.caption.position = (x + 4, y + 41)
		for n, t in enumerate(self.content):
			t.position = (x + 4, y + 9 - 32 * (n + 1))

		return self

	def size(self, x):
		for n, b in enumerate(self.box):
			if n % 2 == 0:
				b.scale_x = x
			elif self.state:
				b.scale_x = len(self.tc) + 1
			else:
				b.scale_x = 1
		self.pos(*self.box[0].position)
		return self

	def on_click(self, x, y, mode):
		if not self.active:
			return
		x1, y1 = self.box[0].position
		x2, y2 = x1 + 32 * self.box[0].scale_x, y1 + 32 * self.box[0].scale_y
		click = (x1 <= x <= x2) * (y1 <= y <= y2)
		if click:
			self.state = not self.state
			self.arrow.scale_y = self.state * -2 + 1

		if self.state:
			for p in range(len(self.tc)):
				if (x1 <= x <= x2) * (y1 - 32 * (p + 1) <= y <= y2 - 32 * (p + 1)):
					self.text.text = self.tc[p]
					break

		if not click:
			self.state = False
			self.arrow.scale_y = 1

		self.size(self.box[0].scale_x)

	def draw(self):
		if not self.active:
			return
		self.caption.draw()
		self.arrow.draw()
		for n, b in enumerate(self.box):
			b.draw()
		self.text.draw()
		if self.state:
			for t in self.content:
				t.draw()
