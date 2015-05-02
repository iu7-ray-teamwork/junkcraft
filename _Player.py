import engine


class Player(engine.Object):
    def __init__(self, world, **kwargs):
        super().__init__(world, engine.Model("resources/fridge.json"), **kwargs)
        self.__attached_objects = set()

    def attach(self, a, b, a_point, b_point):
        pinned_objects = self.compute_pinned_objects()
        if a in pinned_objects or b in pinned_objects:
            a.pin(b, a_point, b_point)

    def detach(self, a, b):
        pinned_objects = self.compute_pinned_objects()
        if a in pinned_objects or b in pinned_objects:
            a.unpin(b)
