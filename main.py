import enum, bpy

bpy.context.preferences.view.show_splash = False

class Direction:
    FORWARD = (1, 0, 0)
    BACKWARD = (-1, 0, 0)
    LEFT = (0, 1, 0)
    RIGHT = (0, -1, 0)
    UP = (0, 0, 1)
    DOWN = (0, 0, -1)

class Scene:
    @staticmethod
    def clear() -> None:
        for collection in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.unlink(collection)

class Model:
    def __init__(self, vertices: list = [], edges: list = [], faces: list = []) -> None:
        self.vertices = vertices
        self.edges = edges
        self.faces = faces
    def create(self, name: str = "Model") -> None:
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(self.vertices, self.edges, self.faces)
        mesh.update()
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(obj)

Scene.clear()
Model([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]).create("test")