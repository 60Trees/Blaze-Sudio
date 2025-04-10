import BlazeSudio.ldtk.Pyldtk as ldtk

from pygame import Surface, Rect
from typing import List, Tuple
import pygame.draw
import json
import math
import os

class World:
    def __init__(self, path):
        """
        A World!

        Parameters
        ----------
        path : str
            The path to the world
        """
        self.data = json.load(open(path))
        self.ldtk = ldtk.LdtkJSON(self.data, os.path.abspath(path))
    
    def gen_minimap(self, maxsize=(64, 64), highlights={}):
        """
        Makes a minimap!

        Parameters
        ----------
        maxsize : tuple[int], optional
            The size of the minimap, stretch to fit, by default (64, 64)
        highlights : dict{int: tuple[int,int,int]}, optional
            A dictionary of level numbers and their colours shown on the minimap, by default {}

        Returns
        -------
        pygame.Surface
            The surface of the minimap
        """
        sur = Surface((maxsize[0], maxsize[1])).convert_alpha()
        sur.fill((255, 255, 255, 1))
        w = 8-math.ceil(math.sqrt(len(self.ldtk.levels)))
        if w < 2:
            w = 2

        diff = (min([i.worldX for i in self.ldtk.levels]), 
                min([i.worldY for i in self.ldtk.levels]))
        maxs = (maxsize[0]/max([i.worldX+i.width for i in self.ldtk.levels]), 
                maxsize[1]/max([i.worldY+i.height for i in self.ldtk.levels]))
        for i in range(len(self.ldtk.levels)):
            lvl = self.ldtk.levels[i]
            pygame.draw.rect(sur,
                       ((125, 125, 125) if i not in highlights else highlights[i]), 
                       Rect((lvl.worldX-diff[0])*maxs[0], 
                            (lvl.worldY-diff[1])*maxs[1], 
                            lvl.width*maxs[0], 
                            lvl.height*maxs[1]),
                        border_radius=w)
        pygame.draw.rect(sur, (0, 0, 0), sur.get_rect(), w, 4)
        return sur

    def get_level(self, lvl):
        return self.ldtk.levels[lvl]

    def get_pygame(self, lvl=0, transparent_bg=False) -> pygame.Surface:
        return self.ldtk.levels[lvl].Render(transparent_bg)

    def get_pygame_with_parralax(self, lvl=0, transparent_bg=False) -> List[Tuple[Surface, Tuple[float, float]]]:
        """This generates it so that instead of bring one layer, it combines all the layers with the same parralax and seperates them into a list of tuples with the surface and the parralax.

        Args:
            lvl (int, optional): _description_. Defaults to 0.
            transparent_bg (bool, optional): _description_. Defaults to False.

        Returns:
            List[Tuple[Surface, Tuple[float, float]]]: A list of tuples with the surface and the parralax.
        """
        return self.ldtk.levels[lvl].Render_parralax(transparent_bg)