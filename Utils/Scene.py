## \file
# Class for creating a scene or a map
try:
    from Object import Mesh, Object
except:
    from Utils.Object import Mesh, Object
import bpy, bmesh



class Scene(Object):
    """Class for a map, a top level object containing meshes
    """
    
    def __iter__(self) -> None:
        """Iterating over meshes

        Returns:
            Iterator representing mesh objects
        """
        for obj in self.objects:
            yield from obj
    
    def create(self, mesh: Mesh) -> None:
        """Creating faces for a Mesh instances

        Args:
            mesh (Mesh): Mesh instance to create faces of
        """
        obj = bpy.data.objects.new(mesh.name, bpy.data.meshes.new(mesh.name))
        bpy.context.scene.collection.objects.link(obj)
    
    def show(self) -> None:
        """Creating the scene by materializing meshes and their faces
        """
        for obj in self:
            self.create(obj)