from . import math


class Scene:
    def __init__(self, objects=()):
        self.objects = set(objects)

    def render(self, surface, viewport):
        size = surface.size
        viewport_to_surface = math.Matrix.scale(max(size) * math.Vector(+0.5, -0.5)) * math.Matrix.translate(size / 2)
        scene_to_surface = ~viewport.to_scene * viewport_to_surface
        for object in self.objects:
            object.render(surface, scene_to_surface)
