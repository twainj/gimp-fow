#!/usr/bin/env python2

from gimpfu import *
import gtk
import gobject
from array import array


def dOut(text):
    pdb.gimp_message(text)

# Entry functions to register (implementation details start around line 140)
def fow_config(image, layer):
    dlg = FowConfigDlg(image, layer)
    dlg.set_title("Config Fog-of-War")
    dlg.show_all()
    
def fow_setupHintLayer(image):
    hintLayer = FowHintLayer(image)
    
def fow_clearFow(image):
    dOut("testing clearFow")
    clearAction = ClearFowAction(image)
    clearAction.execute()
    
def fow_openDoor(image, layer):
    actPt = CurrentPath(image, layer).get_primePt()
    hintLayer = FowHintLayer(image)
    hintLayer.openDoorAt(actPt)
    
def fow_closeDoor(image, layer):
    actPt = CurrentPath(image, layer).get_primePt()
    hintLayer = FowHintLayer(image)
    hintLayer.load()
    hintLayer.closeDoorAt(actPt)

# Entry function Registrations
register(
    "fow-config",
    N_("Configure Fog-of-War"),
    "Provides settings for Fog-of-War plugin",
    "Jason Jones",
    "Jason Jones",
    "2021",
    N_("_Configure..."),
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image",       "Input image", None),
        (PF_LAYER, "layer", "Input layer", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
    ],
    [],
    fow_config,
    menu="<Image>/Tools/Fog-of-War",
    domain=("gimp20-python", gimp.locale_directory)
    )

register(
    "fow-hintlayer-setup",
    N_("Create a fog-of-war hint layer"),
    "Creates a layer where you can add hints for how to clear the fog of war",
    "Jason Jones",
    "Jason Jones",
    "2021",
    N_("Setup _Hint Layer"),
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image",       "Input image", None),
    ],
    [],
    fow_setupHintLayer,
    menu="<Image>/Tools/Fog-of-War",
    domain=("gimp20-python", gimp.locale_directory)
    )

register(
    "fow-clear",
    N_("Clear the Fog of War from the current path"),
    "Clears the fog of war according to current paramenters, starting from the first point of the current path.",
    "Jason Jones",
    "Jason Jones",
    "2021",
    N_("Clear here"),
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image",       "Input image", None),
    ],
    [],
    fow_clearFow,
    menu="<Image>/Tools/Fog-of-War",
    domain=("gimp20-python", gimp.locale_directory)
    )

register(
    "fow-open-door",
    N_("Mark a door on the hint layer as 'open'"),
    "Sets a door (as marked on the hint layer) at the current path as 'open' so that the fog can be cleared through it",
    "Jason Jones",
    "Jason Jones",
    "2021",
    N_("Open door"),
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image",       "Input image", None),
        (PF_LAYER, "layer", "Input layer", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
    ],
    [],
    fow_openDoor,
    menu="<Image>/Tools/Fog-of-War",
    domain=("gimp20-python", gimp.locale_directory)
    )

register(
    "fow-close-door",
    N_("Mark a door on the hint layer as 'closed'"),
    "Sets a door (as marked on the hint layer) at the current path as 'closed' so that the fog cannot be cleared through it",
    "Jason Jones",
    "Jason Jones",
    "2021",
    N_("Close door"),
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image",       "Input image", None),
        (PF_LAYER, "layer", "Input layer", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
    ],
    [],
    fow_closeDoor,
    menu="<Image>/Tools/Fog-of-War",
    domain=("gimp20-python", gimp.locale_directory)
    )


# Classes to implement the entry functions

class FowConfig(object):
    def __init__(self):
        self.visibility = 10 * 12 # pixels/box * boxes/visibility. Assuming box= 5ft, and visibility is 60ft
        self.hintLayerName = 'fow-hint'
        self.mapLayerName = 'fow-map'
        self.fogLayerName = 'fow-fog'
        self.wallMinThickness = 5
        self.visibilityDist = 100

# TODO Class to manage the functionality of the config dlg
class FowConfigDlg(gtk.Window):
    def __init__(self, image, layer):
        super(FowConfigDlg, self).__init__()
        
        # TODO: input for hint clear color
        # TODO: input for hint block color
        # TODO: input for open door color
        # TODO: input for closed door color
        # TODO: input for wall thickness (px)
        # TODO: input for visibility distance
    
class FowLayer(object):
    def __init__(self, image, name):
        dOut("in FowLayer ctor")
        self.image = image
        self.name = name
        ls = [l for l in self.image.layers if l.name == self.name]
        if len(ls) > 0:
            self.layer = ls[0]
            # TODO: Maybe bring this layer to the top for easy edit?
        else:
            self.layer = self.image.new_layer(self.name, self.image.width, self.image.height, 0,0,1,0,1,NORMAL_MODE, FILL_TRANSPARENT)
    
    def setRegion(self, x,y,w,h,writable):
        self.region = self.layer.get_pixel_rgn(x, y, w, h, writable, writable)
        self._pixels = array("B", self.region[0:w, 0:h])


class FowHintLayer(FowLayer):
    def __init__(self, image):
        dOut("in FowHintLayer ctor")
        cfg = FowConfig()
        dOut("FHL got config: " + cfg.hintLayerName)
        super(FowHintLayer, self).__init__(image, cfg.hintLayerName)

class CurrentPath(object):
    def __init__(self, image):
        self.image = image
        
    def get_primePt(self):
        vectors = pdb.gimp_image_get_active_vectors(self.image)
        return vectors.strokes[0].points[0][2:4]

# TODO: implement action to clear the Fog-of-War
class ClearFowAction(object):
    def __init__(self, image):
        self.image = image
        
    # TODO: implement function to do the block fill algorithm for the fow clear
    def execute(self):
        dOut("ClearFowAction.execute is not fully implemented yet")
        cfg = FowConfig()
        hintLayer = FowHintLayer(self.image)
        mapLayer = FowLayer(self.image, cfg.mapLayerName)
        fogLayer = FowLayer(self.image, cfg.fogLayerName)
        

        curPath = CurrentPath(self.image)
        x1,y1 = curPath.get_primePt()
        
        # TODO: Run algorithm starting from that point
        # Using pixel region thing...
        # setup - initialize the regions and get their contents into arrays:
        rgnX,rgnY = x1 - cfg.visibilityDist, y1 - cfg.visibilityDist
        width = height = cfg.visibilityDist * 2
        
        hintLayer.setRegion(x, y, width, height, False)
        mapLayer.setRegion(x, y, width, height, False)
        fogLayer.setRegion(x, y, width, height, True)
        
        #---TODO: Following code is untranslated

        dstRgn = destDrawable.get_pixel_rgn(0, 0, newWidth, newHeight, True, True)
        p_size = len(srcRgn[0,0])               
        dest_pixels = array("B", "\x00" * (newWidth * newHeight * p_size))

        # for the loop over x/y
        src_pos = (x + srcWidth * y) * p_size
        dest_pos = (newx + newWidth * newy) * p_size
        
        newval = src_pixels[src_pos: src_pos + p_size]
        dest_pixels[dest_pos : dest_pos + p_size] = newval

        # After loop, Copy the whole array back to the pixel region:
        dstRgn[0:newWidth, 0:newHeight] = dest_pixels.tostring() 


if __name__ == "__main__":
    main()
