import pyglet
from pyglet.window import key
from pyglet import shapes
import mouse

class Event:
    QUIT = "QUIT"
    def __init__(self):
        self.type = "NONE"
        self.QUIT = Event.QUIT

class Window:
    def __init__(self, title, w, h):
        self.handle = pyglet.window.Window(width=w, height=h, caption=title)
        self._exit_requested = False

        @self.handle.event
        def on_close():
            self._exit_requested = True
            return pyglet.event.EVENT_HANDLED 

    def poll_event(self, _, event_ref):
        self.handle.dispatch_events()
        if self._exit_requested:
            event_ref.type = event_ref.QUIT
            self.handle.close() 
            return True
        return False

class Renderer:
    def __init__(self, win_obj):
        self.window = win_obj.handle
        self.batch = pyglet.graphics.Batch()
        self.color = (0, 0, 0, 255)

    def set_draw_color(self, r, g, b):
        self.color = (r/255, g/255, b/255, 1.0)

    def clear(self):
        from pyglet.gl import glClearColor
        glClearColor(*self.color)
        self.window.clear()

    def present(self):
        self.batch.draw()
        pyglet.clock.tick()
        self.window.flip()

class Texture:
    def __init__(self, renderer, path, x=0, y=0):
        self.image = pyglet.image.load(path)
        self.sprite = pyglet.sprite.Sprite(img=self.image, x=x, y=y, batch=renderer.batch)

    def set_pos(self, x, y):
        self.sprite.x = x
        self.sprite.y = y

    def bind(self):
        pass

    def unbind(self):
        pass

    def resize(self, width, height):
        self.sprite.scale_x = width / self.sprite.width
        self.sprite.scale_y = height / self.sprite.height

class Input:
    def __init__(self, win_obj):
        self.keys = key.KeyStateHandler()
        win_obj.handle.push_handlers(self.keys)
        
        self.key_map = {
            'left': key.LEFT,
            'right': key.RIGHT,
            'up': key.UP,
            'down': key.DOWN,
            'space': key.SPACE
        }
    
    def mouse_pressed(self, button):
        return mouse.is_pressed(button)
    
    def mosue_released(self, button):
        return not mouse.is_pressed(button)

    def mouse_position(self):
        return mouse.get_position()

    def is_key_pressed(self, key_name):
        gl_key = self.key_map.get(key_name.lower())
        if gl_key is not None:
            return self.keys[gl_key]
        return False
    
    def is_key_released(self, key_name):
        gl_key = self.key_map.get(key_name.lower())
        if gl_key is not None:
            return not self.keys[gl_key]
        return False

    def key_pressed_callback(self, key_name, callback):
        gl_key = self.key_map.get(key_name.lower())
        if gl_key is not None:
            @self.keys.event
            def on_key_press(symbol, modifiers):
                if symbol == gl_key:
                    callback()
    
    def key_released_callback(self, key_name, callback):
        gl_key = self.key_map.get(key_name.lower())
        if gl_key is not None:
            @self.keys.event
            def on_key_release(symbol, modifiers):
                if symbol == gl_key:
                    callback()

    def mouse_pressed_callback(self, button, callback):
        @mouse.on_button(button)
        def on_mouse_press(x, y):
            callback()
    
    def mouse_released_callback(self, button, callback):
        @mouse.on_button(button)
        def on_mouse_release(x, y):
            callback()     

class Text:
    def __init__(self, renderer, text, x=0, y=0, font_name='Arial', font_size=12, color=(255, 255, 255)):
        self.label = pyglet.text.Label(text, font_name=font_name, font_size=font_size,
                                       x=x, y=y, color=color+(255,), batch=renderer.batch)

    def set_text(self, new_text):
        self.label.text = new_text

    def set_pos(self, x, y):
        self.label.x = x
        self.label.y = y

    def change_color(self, r, g, b):
        self.label.color = (r, g, b, 255)

    def bind(self):
        pass

    def unbind(self):
        pass

    def change_size(self, new_size):
        self.label.font_size = new_size

    def change_font(self, new_font):
        self.label.font_name = new_font

class Collision:
    @staticmethod
    def get_hitbox(obj):
        if hasattr(obj, 'sprite'): 
            # Use the sprite's width and height, but ensure we check 
            # if they are returning scaled values. 
            return (obj.sprite.x, 
                    obj.sprite.y, 
                    obj.sprite.width, 
                    obj.sprite.height)
        
        # Check if it's a Pyglet shape (which has x, y, width, height)
        # or your own custom object
        return obj.x, obj.y, obj.width, obj.height

    @staticmethod
    def is_colliding(obj1, obj2):
        x1, y1, w1, h1 = Collision.get_hitbox(obj1)
        x2, y2, w2, h2 = Collision.get_hitbox(obj2)

        # AABB Collision logic
        return (x1 < x2 + w2 and
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2)
    
    @staticmethod # <--- Added this so you can call it like mfr.Collision.collision_callback
    def collision_callback(obj1, obj2, callback):
        # We call the static method is_colliding
        if Collision.is_colliding(obj1, obj2):
            callback()

class Drawable:
    @staticmethod
    def rect(renderer, x, y, width, height, color=(255, 255, 255)):
        # Pyglet shapes expect a 3-tuple (R, G, B) or 4-tuple (R, G, B, A)
        return shapes.Rectangle(x, y, width, height, color=color, batch=renderer.batch)
    
    @staticmethod
    def ellipse(renderer, x, y, width, height, color=(255, 255, 255)):
        # Calculate center because Pyglet Ellipses draw from the middle
        cx = x + width // 2
        cy = y + height // 2
        return shapes.Ellipse(cx, cy, width // 2, height // 2, color=color, batch=renderer.batch)
    
    @staticmethod
    def polygon(renderer, points, color=(255, 255, 255)):
        # points should be a list of tuples like [(x1, y1), (x2, y2)...]
        return shapes.Polygon(*points, color=color, batch=renderer.batch)
    
class Sound:
    def __init__(self, path):
        # streaming=False is a MUST for instant restarts
        self.source = pyglet.media.load(path, streaming=False)
        # Create one dedicated player for this sound
        self.player = pyglet.media.Player()
        self.player.queue(self.source)

    def play(self):
        # 1. Rewind the 'needle' to the very start (0.0 seconds)
        self.player.seek(0.0)
        # 2. Start playing
        self.player.play()

    def stop(self):
        self.player.pause()
        self.player.seek(0.0)

    def pause(self):
        self.player.pause()

    def set_volume(self, volume):
        self.player.volume = volume

    def is_playing(self):
        return self.player.playing