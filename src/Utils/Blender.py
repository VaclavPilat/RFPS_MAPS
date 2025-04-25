## \file
# Functionality for bridging Blender usage with the rest of code
from . import Mesh, Vector
# noinspection PyUnresolvedReferences
import bpy, bmesh, math


def create(self):
    """Creating a blender mesh from face vertices

    Returns:
        Created mesh object
    """
    mesh = bpy.data.meshes.new(self.name)
    bm = bmesh.new()
    vertices = {}
    for face in self.faces:
        for vert in face.points:
            if vert not in vertices:
                vertices[vert] = bm.verts.new(tuple(vert))
        bm.faces.new([vertices[vert] for vert in face.points])
    bm.to_mesh(mesh)
    return mesh


def build(self):
    """Building a blender object from an Object instance

    Returns:
        Built blender object
    """
    obj = bpy.data.objects.new(self.name, self.create() if len(self.faces) else None)
    obj.location = list(self.position)
    obj.rotation_euler = [math.radians(value) for value in Vector.V3.UP * self.rotation]
    bpy.context.scene.collection.objects.link(obj)
    for child in self.objects:
        child.build().parent = obj
    return obj


Mesh.Object.create = create
Mesh.Object.build = build


class Setup:
    """Static methods meant for setting up Blender environment etc.
    """

    @staticmethod
    def setupForDevelopment() -> None:
        """Setting up Blender for easier development
        """
        # Hiding splash screen
        bpy.context.preferences.view.show_splash = False
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        # Showing mesh sizes (vertice/edge/face counts)
                        space.overlay.show_stats = True
                        # Setting colors of faces based on their orientation
                        space.overlay.show_face_orientation = True
                        # Showing textures
                        space.shading.type = "MATERIAL"
                        return

    @staticmethod
    def purgeExistingObjects() -> None:
        """Clearing all objects and collections in scene
        """
        for collection in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.unlink(collection)
        for obj in bpy.context.scene.objects:
            bpy.data.objects.remove(obj)