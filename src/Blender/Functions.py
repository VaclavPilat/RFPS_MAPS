## \file
# Functions for working with Blender
import bpy



def setupForDevelopment() -> None:
    """Setting up Blender for easier development
    """
    bpy.context.preferences.view.show_splash = False # Hiding splash screen
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            for space in area.spaces:
                if space.type == "VIEW_3D":
                    space.overlay.show_stats = True # Showing mesh sizes (vertice/edge/face counts)
                    space.overlay.show_face_orientation = True # Setting colors of faces based on their orientation
                    space.shading.type = "MATERIAL" # Showing textures
                    return



def purgeExistingObjects() -> None:
    """Clearing all objects and collections in scene
    """
    for collection in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.unlink(collection)
    for obj in bpy.context.scene.objects:
        bpy.data.objects.remove(obj)