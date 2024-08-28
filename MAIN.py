import enum, bpy, bmesh

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

class Map:
    def __init__(self) -> None:
        self.bmesh = bmesh.new()
        self.vertices = {}

    def vertex(self, v: "V"):
        if v in self.vertices:
            return self.vertices[v]
        vertex = self.bmesh.verts.new(tuple(v))
        self.vertices[v] = vertex
        return vertex
    
    def face(self, vertices: list|tuple) -> list|tuple:
        self.bmesh.faces.new([self.vertex(tuple(v)) for v in vertices])
        return vertices

    def create(self, name: str = "Map") -> None:
        mesh = bpy.data.meshes.new(name)
        self.bmesh.to_mesh(mesh)
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(obj)