## \file
# Functions for setting up Blender
import bpy



class Blender:
    """Blender setup functions
    """
    
    @staticmethod
    def setup() -> None:
        """Setting up Blender for easier development
        """
        bpy.context.preferences.view.show_splash = False
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        space.overlay.show_stats = True
                        space.overlay.show_face_orientation = not space.overlay.show_face_orientation
                        space.shading.type = "MATERIAL"
                        return

    @staticmethod
    def purge() -> None:
        """Clearing all objects and collections in scene
        """
        for collection in bpy.context.scene.collection.children:
            for obj in collection.objects:
                bpy.data.objects.remove(obj)
            bpy.context.scene.collection.children.unlink(collection)