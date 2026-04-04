import moonframe as mfr

class GameApp:
    def __init__(self, renderer, input_handler):
        self.renderer = renderer
        self.input = input_handler
        self.x, self.y = 100, 100
        
        self.cat = mfr.Texture(renderer, r"cat.avif", x=self.x, y=self.y)
        self.cat.resize(128, 128)

    def update(self):
        if self.input.is_key_pressed('right'): self.x += 5
        if self.input.is_key_pressed('down'): self.y -= 5
        if self.input.is_key_pressed('up'): self.y += 5
        if self.input.is_key_pressed('left'): self.x -= 5

        self.cat.set_pos(self.x, self.y)

    def draw(self):
        self.renderer.set_draw_color(20, 20, 30)
        self.renderer.clear()

win = mfr.Window("Cool Cat", 800, 600)
renderer = mfr.Renderer(win)
event = mfr.Event()
input_handler = mfr.Input(win)
app = GameApp(renderer, input_handler)

running = True
while running:
    while win.poll_event(win, event):
        if event.type == event.QUIT:
            running = False
            break

    if not running:
        break
    
    app.update()
    app.draw()
    renderer.present()

win.handle.close()