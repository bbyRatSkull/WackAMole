class Button():
	# altered to make buttons move, added 3 more info passes after "pos"
	def __init__(self, image, pos, base_screen_info, game_size, gen_coords, text_input, font, base_color, hovering_color):
		self.image = image
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)

		#stuff to auto place button based off game/window size \/
		x_percent      = pos[0] / base_screen_info[0]
		y_percent      = pos[1] / base_screen_info[1]

		self.x_pos = (x_percent * game_size[0]) + gen_coords[0]
		self.y_pos = (y_percent * game_size[1]) + gen_coords[1]
		#end of changes /\

		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)