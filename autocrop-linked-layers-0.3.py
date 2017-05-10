#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GIMP plugin to autocrop layers by the truckload
# (c) Ofnuts 2012
# (c) NWeyand 2017
#
#   History:
#
#   v0.0: 2011-06-06: First published version
#   v0.1: 2011-06-07: Fix use of autocrop-layer
#   v0.2: 2012-03-27: Add autocrop-all-layers, work on all types
#   v0.3: 2017-05-10: Added support for layer groups
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from gimpfu import *


def autocrop(image,layer):
	pdb.gimp_image_set_active_layer(image, layer)
	pdb.plug_in_autocrop_layer(image, layer)


def autocropLinkedRecursive(image,layer):
	if layer.linked and pdb.gimp_item_is_group(layer):
		group_info = pdb.gimp_item_get_children(layer)
		group_layer_ids = group_info[1]
		for layer_id in group_layer_ids:
			child_layer = gimp.Item.from_id(layer_id)
			if pdb.gimp_item_is_layer(child_layer):
				autocrop(image, child_layer)
			autocropLinkedRecursive(image, child_layer)


def autocropLinkedLayers(image,drawable):
	for layer in image.layers:
		autocrop(image, layer)
		autocropLinkedRecursive(image, layer)


def autocropAllRecursive(image,layer):
	if pdb.gimp_item_is_group(layer):
		group_info = pdb.gimp_item_get_children(layer)
		group_layer_ids = group_info[1]
		for layer_id in group_layer_ids:
			child_layer = gimp.Item.from_id(layer_id)
			if pdb.gimp_item_is_layer(child_layer):
				autocrop(image, child_layer)
			autocropAllRecursive(image, child_layer)


def autocropAllLayers(image,drawable):
	for layer in image.layers:
		autocrop(image, layer)
		autocropAllRecursive(image, layer)


### Registrations
    
register(
    "autocrop-linked-layers",
    N_("Autocrop linked layers"),
    "Autocrop linked layers",
    "Ofnuts, NWeyand", "Ofnuts, NWeyand", "2017",
    N_("Autocrop linked layers..."),
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
    ],
    [],
    autocropLinkedLayers,
    menu="<Image>/Image",
    domain=("gimp20-python", gimp.locale_directory)
)
register(
    "autocrop-all-layers",
    N_("Autocrop all layers"),
    "Autocrop all layers",
    "Ofnuts, NWeyand", "Ofnuts, NWeyand", "2017",
    N_("Autocrop all layers..."),
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
    ],
    [],
    autocropAllLayers,
    menu="<Image>/Image",
    domain=("gimp20-python", gimp.locale_directory)
)

main()
