# Gregory Rosenblatt
# 1/7/06

from settings import mediumTypes
from simulation.entity import *

class VisibleEntity(Entity):
	mediums = Entity.mediums + [mediumTypes.visual]
