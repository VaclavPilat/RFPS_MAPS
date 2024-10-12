## \file
# Functionality for generating object meshes
# \todo Finish Metro map
# \todo Create Babel map
# \todo Create Warehouse map



if __name__ == "__main__":
    import os, sys, bpy
    directory = os.path.dirname(bpy.data.filepath)
    if not directory in sys.path:
        sys.path.append(directory)



import bpy, bmesh, enum, math, mathutils
from VECTOR import *
from MODIFIERS import *



class LitCamera:
    """Camera with a sun behind it
    """

    def __init__(self, position: list|tuple = (0, 0, 0), rotation: list|tuple = (0, 0, 0), strength: int|float = 3) -> None:
        """Creating a lit camera with a sun light behind it

        Args:
            position (list | tuple, optional): Camera position. Defaults to (0, 0, 0).
            rotation (list | tuple, optional): Camera euler rotation. Defaults to (0, 0, 0).
            strength (list | tuple, optional): Camera light strength. Defaults to 3.
        """
        self.cam = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
        self.cam.location = position
        self.cam.rotation_euler = rotation
        bpy.context.scene.collection.objects.link(self.cam)
        self.light = bpy.data.objects.new("Light", bpy.data.lights.new("Light", type="SUN"))
        self.light.location = position
        self.light.rotation_euler = rotation
        bpy.context.scene.collection.objects.link(self.light)
        self.light.data.energy = strength

    def isometric(self, scale: int) -> None:
        """Making the camera isometric

        Args:
            scale (int): Ortho scale
        """
        self.cam.data.type = 'ORTHO'
        self.cam.data.ortho_scale = scale
    
    def render(self, filepath: str = "render.png") -> None:
        """Rendering an image from camera

        Args:
            filepath (str, optional): Image file path. Defaults to "render.png".
        """
        bpy.context.scene.camera = self.cam
        bpy.context.scene.render.filepath = filepath
        bpy.context.scene.render.engine = "BLENDER_EEVEE"
        bpy.context.scene.render.film_transparent = True
        bpy.ops.render.render(write_still=True)

    def destroy(self) -> None:
        """Removing used objects from scene
        """
        bpy.data.objects.remove(self.cam)
        bpy.data.objects.remove(self.light)



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
                        space.shading.type = "MATERIAL"
                        break
    
    @staticmethod
    def forceDepthMaterial() -> None:
        """Assigning a "depth" material to all objects in scene
        """
        for obj in bpy.data.objects:
            index = len(obj.data.materials)
            obj.data.materials.append(Material.depth())
            for polygon in obj.data.polygons:
                polygon.material_index = index
    
    @staticmethod
    def topIsoRender() -> None:
        """Creating an isometric top-down view of the scene
        """
        camera = LitCamera((0, 0, 100), mathutils.Euler((0, 0, math.radians(90))))
        camera.cam.data.type = 'ORTHO'
        camera.cam.data.ortho_scale = 50
        camera.render()
        camera.destroy()

    @staticmethod
    def clear() -> None:
        """Clearing all objects in scene
        """
        for collection in bpy.context.scene.collection.children:
            for obj in collection.objects:
                bpy.data.objects.remove(obj)
            bpy.context.scene.collection.children.unlink(collection)



class Pivot(enum.Enum):
    """Tile pivot position
    """
    CENTER = 1
    TOP_LEFT = 2



class Map:
    """Class for creating a mesh of a static map model
    """

    def __init__(self) -> None:
        """Initializing a map mesh
        """
        self.bmesh = bmesh.new()
        self.vertices = {}
        self.faces = 0
        self.materials = {}

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
    
    def face(self, vertices: list|tuple, material: list|tuple = None) -> None:
        """Creating a face from a list of vertices

        Args:
            vertices (list[V3] | tuple): Collection of vertices
            material (list|tuple, optional): Material (Class/method, *args). Defaults to None.
        """
        self.bmesh.faces.new([self.vertex(tuple(v)) for v in vertices])
        if material is not None:
            if material in self.materials:
                self.materials[material].append(self.faces)
            else:
                self.materials[material] = [self.faces]
        self.faces += 1
    
    def load(self, func, position: V3 = V3.ZERO, size: list|tuple = (1, 1), pivot: Pivot = Pivot.TOP_LEFT, modifiers: list|tuple = []) -> "Tile":
        """Loading a tile into the mesh

        Args:
            func (func): Tile func type
            position (V3, optional): Tile position. Defaults to V3.ZERO.
            size (list | tuple, optional): Tile size (x,y). Defaults to (1, 1).
            pivot (Pivot, optional): Pivot position. Defaults to Pivot.TOP_LEFT.
            modifiers (list | tuple, optional): List of vector modifiers. Defaults to [].

        Returns:
            Tile: Loaded tile instance
        """
        loaded = Tile(self, position, size, pivot, modifiers)
        loaded.create = func
        loaded.create(loaded)
        return loaded

    def create(self, name: str = "Map") -> None:
        """Creating an object from the mesh

        Args:
            name (str, optional): Object name. Defaults to "Map".
        """
        mesh = bpy.data.meshes.new(name)
        self.bmesh.to_mesh(mesh)
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(obj)
        for index, material in enumerate(self.materials):
            obj.data.materials.append(material[0](*material[1:]))
            for i in self.materials[material]:
                obj.data.polygons[i].material_index = index



class Material:
    """Class for generating custom materials
    """

    @staticmethod
    def color(name: str, color: list|tuple):
        """Creating a simple material with a diffuse color

        Args:
            name (str): Material name
            color (list | tuple): Color (r,g,b,a)

        Returns:
            Created Blender material
        """
        material = bpy.data.materials.new(name=name)
        material.diffuse_color = color
        return material

    @staticmethod
    def depth(name: str = "Depth material"):
        """Creating a depth material using nodes

        Args:
            name (str, optional): Material name. Defaults to "Depth material".

        Returns:
            Created Blender material
        """
        material = bpy.data.materials.new(name=name)
        material.use_backface_culling = True
        material.use_nodes = True
        nodes = material.node_tree.nodes
        nodes.clear()
        texture = nodes.new("ShaderNodeTexCoord")
        separate = nodes.new("ShaderNodeSeparateXYZ")
        ramp = nodes.new("ShaderNodeValToRGB")
        output = nodes.new("ShaderNodeOutputMaterial")
        material.node_tree.links.new(output.inputs[0], ramp.outputs[0])
        material.node_tree.links.new(ramp.inputs[0], separate.outputs[2])
        material.node_tree.links.new(separate.inputs[0], texture.outputs[0])
        ramp.color_ramp.interpolation = "EASE"
        return material



class Tile:
    """Class for representing a single tile inside of a Map mesh
    """

    def __init__(self, mesh: Map, position: V3 = V3.ZERO, size: list|tuple = (1, 1), pivot: Pivot = Pivot.TOP_LEFT, modifiers: list|tuple = []) -> None:
        """Preparing variables for tile generation

        Args:
            mesh (Map): Map object
            position (V3, optional): Tile position. Defaults to V3.ZERO.
            size (list | tuple, optional): Tile size (x,y). Defaults to (1, 1).
            pivot (Pivot, optional): Pivot position. Defaults to Pivot.TOP_LEFT.
            modifiers (list | tuple, optional): List of vector modifiers. Defaults to [].

        Raises:
            ValueError: Thrown if unknown Pivot value was provided
        """
        self.mesh = mesh
        self.position = position
        self.size = size
        self.pivot = pivot
        self.modifiers = modifiers
        if pivot == Pivot.CENTER:
            self.C = position
            self.TL = position + size[0]/2 * V3.FORWARD + size[1]/2 * V3.LEFT
            self.TR = position + size[0]/2 * V3.FORWARD + size[1]/2 * V3.RIGHT
            self.BL = position + size[0]/2 * V3.BACKWARD + size[1]/2 * V3.LEFT
            self.BR = position + size[0]/2 * V3.BACKWARD + size[1]/2 * V3.RIGHT
        elif pivot == Pivot.TOP_LEFT:
            self.TL = position
            self.TR = position + size[1] * V3.RIGHT
            self.BL = position + size[0] * V3.BACKWARD
            self.BR = position + size[1] * V3.RIGHT + size[0] * V3.BACKWARD
            self.C = position + size[1]/2 * V3.RIGHT + size[0]/2 * V3.BACKWARD
        else:
            raise ValueError("Unknown Pivot value")
    
    def create(self) -> None:
        """Drawing an image

        Raises:
            NotImplemented: Thrown if not overriden
        """
        raise NotImplemented
    
    def load(self, func, position: V3 = None, size: list|tuple = None, pivot: Pivot = None, modifiers: int = []) -> None:
        """Loading a tile into the mesh

        Args:
            func (func): Tile func type
            position (V3, optional): Tile position. Defaults to None.
            size (list | tuple, optional): Tile size (x,y). Defaults to None.
            pivot (Pivot, optional): Pivot position. Defaults to None.
            modifiers (list | tuple, optional): List of vector modifiers. Defaults to [].
        """
        if position is None:
            position = self.position
        if size is None:
            size = self.size
        if pivot is None:
            pivot = self.pivot
        return self.mesh.load(func, position, size, pivot, self.modifiers + modifiers)
    
    def face(self, vertices: list|tuple, material: list|tuple = None) -> None:
        """Creating a face from a list of vertices

        Args:
            vertices (list[V3] | tuple): Collection of vertices
            material (list|tuple, optional): Material (Class/method, *args). Defaults to None.
        """
        vertices = list((self.modify(a) for a in vertices))
        if list((isinstance(a, FlipX) for a in self.modifiers)).count(True) % 2 == 1:
            vertices = vertices[::-1]
        self.mesh.face(vertices, material)
    
    def modify(self, vertex: V3) -> V3:
        """Updating vertex position based on used modifiers

        Args:
            vertex (V3): Position of a vertex

        Returns:
            V3: Modified vertex position
        """
        difference = vertex - self.C
        for modifier in self.modifiers:
            difference = modifier.execute(difference)
        return self.C + difference



if __name__ == "__main__":
    Scene.setup()
    Scene.clear()
    model = Map()
    model.face([V3.ZERO, V3.RIGHT, V3.FORWARD+V3.RIGHT, V3.FORWARD])
    model.create("Square")