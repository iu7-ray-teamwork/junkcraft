import engine


class Player(engine.Object):
    def __init__(self, world, position=(0, 0), angle=0, scale=1):
        model = engine.Model("resources/fridge.json")
        super().__init__(world, model, position, angle, scale)
        self.__attached_objects = set()

    def attach(self, old, new, old_point=None, new_point=None):
        if old is self or old in self.__attached_objects:
            self.__attached_objects.add(new)
            old.pin(new, old_point, new_point)
            return True
        return False

    def detach(self, object):
        if object is self or object in self.__attached_objects:
            object.unpin()
            return True
        return False
