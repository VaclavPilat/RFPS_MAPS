## \file
# Functionality for bridging own data representation with Blender.
from . import Mesh, Vector
# noinspection PyUnresolvedReferences
import bpy, bmesh, math


class Objects:
    """Static methods for constructing Blender objects
    """

    @staticmethod
    def create(obj: Mesh.Object):
        """Creating a blender mesh from face vertices

        Args:
            obj (Mesh.Object): Object whose mesh is being created

        Returns:
            Created mesh object
        """
        data = bpy.data.meshes.new(obj.name)
        mesh = bmesh.new()
        vertices = {}
        for face in obj.faces:
            for vert in face.points:
                if vert not in vertices:
                    vertices[vert] = mesh.verts.new(tuple(vert))
            mesh.faces.new([vertices[vert] for vert in face.points])
        mesh.to_mesh(data)
        return data

    @staticmethod
    def build(obj: Mesh.Object):
        """Building a blender object from an Object instance

        Args:
            obj (Mesh.Object): Object being built

        Returns:
            Built blender object
        """
        data = bpy.data.objects.new(obj.name, Objects.create(obj) if len(obj.faces) else None)
        data.location = list(obj.position)
        data.rotation_euler = [math.radians(value) for value in Vector.V3.UP * obj.rotation]
        bpy.context.scene.collection.objects.link(data)
        for child in obj.objects:
            Objects.build(child).parent = data
        return data


class Setup:
    """Static methods meant for setting up Blender environment etc.
    """

    @staticmethod
    def development() -> None:
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
    def purge() -> None:
        """Clearing all objects and collections in scene
        """
        for collection in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.unlink(collection)
        for obj in bpy.context.scene.objects:
            bpy.data.objects.remove(obj)