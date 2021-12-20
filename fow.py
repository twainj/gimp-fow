#!/usr/bin/env python2

from gimpfu import *
import gtk
import gobject



def fow_config(image, layer):
    dlg = FowConfigDlg(image, layer)
    dlg.set_title("Config Fog-of-War")
    dlg.show_all()
    
def fow_setupHintLayer(image, layer):
    hintLayer = FowHintLayer(image, layer)
    hintLayer.create()
    
def fow_clearFow(image, layer):
    clearAction = ClearFowAction(image, layer)
    clearAction.execute()
    
def fow_openDoor(image, layer):
    actPt = CurrentPath(image, layer).get_primePt()
    hintLayer = FowHintLayer(image, layer)
    hintLayer.load()
    hintLayer.openDoorAt(actPt)
    
def fow_closeDoor(image, layer):
    actPt = CurrentPath(image, layer).get_primePt()
    hintLayer = FowHintLayer(image, layer)
    hintLayer.load()
    hintLayer.closeDoorAt(actPt)


# TODO: Register a function that opens the config dialog


# TODO: Registar a function to set up the hint layer
# TODO: Register a function to clear the Fog-of-War
# TODO: Register a function to open a door
# TODO: Register a function to close a door

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
    
# TODO: Implement hint layer creation
class FowHintLayer():
    def __init__(self, image, layer):
    def load():
    def create():

class CurrentPath():
    def __init__(self, image, layer):
    def get_primePt():

# TODO: implement action to clear the Fog-of-War
class ClearFowAction():
    def __init__(self, image, layer):
    # TODO: implement function to do the block fill algorithm for the fow clear
    def execute():

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
    menu="<Image>/Filters/Decor",
    domain=("gimp20-python", gimp.locale_directory)
    )

main()
