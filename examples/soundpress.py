import moonframe as mfr

class GameApp:
    def __init__(self, renderer, input_handler):
        self.renderer = renderer
        self.input_handler = input_handler

        self.label = mfr.Text(self.renderer, "Left click for sound (PRESS EVERY 1 SECOND)", 400, 300, font_size=12)
        self.sound = mfr.Sound("blip.mp3")

    def update(self):
        if self.input_handler.mouse_pressed("left"):
            self.sound.play()

    def draw(self):
        self.renderer.set_draw_color(0, 0, 0)
        self.renderer.clear()

win = mfr.Window("Press for sound", 800, 600)
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