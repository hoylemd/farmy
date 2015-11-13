import pyglet


class Game(object):
    def __init__(self, fullscreen=True, name="Mike's Game"):
        self.name = name

        self.window = pyglet.window.Window(fullscreen=fullscreen)
        self.main_batch = pyglet.graphics.Batch()
        self.ui_batch = pyglet.graphics.Batch()
        self.game_objects = []
        self.console_log = ["Welcome to " + self.name]

    def update(self, dt):
        new_objects = []

        # update each object
        for obj in self.game_objects:
            obj.update(dt)
            if obj.new_objects:
                new_objects.extend(obj.new_objects)
                obj.new_objects = []

        # remove dead objects
        for to_remove in [obj for obj in self.game_objects if obj.dead]:
            to_remove.delete()
            self.game_objects.remove(to_remove)

        # add new objects
        self.game_objects.extend(new_objects)

    def draw(self):
        self.window.clear()
        self.main_batch.draw()
        self.ui_batch.draw()

    def log(self, message):
        self.console_log += message
