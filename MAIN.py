if __name__ == "__main__":
    import os, sys, bpy
    directory = os.path.dirname(bpy.data.filepath)
    if not directory in sys.path:
        sys.path.append(directory)



import bpy, bmesh
from VECTOR import *



class Scene:
    """Class for managing objects in scene
    """

    @staticmethod
    def setup() -> None:
        """Setting up blender window
        """
        bpy.context.preferences.view.show_splash = False
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        space.overlay.show_stats = True
                        space.overlay.show_face_orientation = not space.overlay.show_face_orientation
                        #space.shading.type = "MATERIAL"
                        break

    @staticmethod
    def clear() -> None:
        """Clearing all objects in scene
        """
        for collection in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.unlink(collection)



class Map:
    """Class for creating a mesh of a static map model
    """

    def __init__(self) -> None:
        """Initializing a map mesh
        """
        self.bmesh = bmesh.new()
        self.vertices = {}

    def vertex(self, position: V3) -> "BMVert":
        """Creating a vertex (if it does not exist yet)

        Args:
            position (V3): Vertex coordinates stored in a 3D vector

        Returns:
            BMVert: Created vertex
        """
        if position in self.vertices:
            return self.vertices[position]
        vertex = self.bmesh.verts.new(tuple(position))
        self.vertices[position] = vertex
        return vertex
    
    def face(self, vertices: list[V3]|tuple) -> None:
        """Creating a face from a list of vertices

        Args:
            vertices (list[V3] | tuple): Collection of vertices
        """
        self.bmesh.faces.new([self.vertex(tuple(v)) for v in vertices])

    def create(self, name: str = "Map") -> None:
        """Creating an object from the mesh

        Args:
            name (str, optional): Object name. Defaults to "Map".
        """
        mesh = bpy.data.meshes.new(name)
        self.bmesh.to_mesh(mesh)
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(obj)



if __name__ == "__main__":
    Scene.setup()
    Scene.clear()
    model = Map()
    model.face([V3.ZERO, V3.RIGHT, V3.FORWARD+V3.RIGHT, V3.FORWARD])
    model.create("Square")