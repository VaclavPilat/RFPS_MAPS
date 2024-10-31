## \file
# Class for creating a scene or a map
try:
    from Mesh import Mesh, Object
except:
    from Utils.Mesh import Mesh, Object
import bpy, bmesh



class Scene(Object):
    """Class for a map, a top level object containing meshes
    """
    
    def __iter__(self):
        """Iterating over meshes

        Returns:
            Iterator representing mesh objects
        """
        for obj in self.objects:
            yield from obj
    
    def create(self, root: Object = None) -> None:
        """Creating the scene by materializing meshes and their faces

        Args:
            root (Object, optional): Root object. Defaults to None.
        """
        if root is None:
            root = self
        print(root)
        for obj in root.objects:
            self.create(obj)