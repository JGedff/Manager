class Move():
    NAME_OBJECTS = []
    OBJECTS = []

    @classmethod
    def save(cls, name, value):
        cls.NAME_OBJECTS.append(name)
        cls.OBJECTS.append(value)

    @classmethod
    def get(cls, name):
        for index, obj in enumerate(cls.NAME_OBJECTS):
            if obj == name:
                return cls.OBJECTS[index]