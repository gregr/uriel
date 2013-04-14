# Gregory Rosenblatt
# 1/11/06

from uriel.playersenses import *
from uriel.core.enum import Enum

# possibilities: mechanical, chemical, biological
# ie. biological for examining health-related internal states?
mediumTypes = Enum([
					"visual",
					"auditory",
					"electromagnetic",	# include temperature..?
					"mineral",	# or something hilarious?
					"ethereal",	# or psionic? psi?
					"admin"	# for admin-only perception
					])

visualScale = 1
auditoryScale = 5
mediumTraits = [(mediumTypes.visual, visualScale)
				,(mediumTypes.auditory, auditoryScale)]

stepsPerSecond = 20
