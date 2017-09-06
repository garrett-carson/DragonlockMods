import sys

dir = "C://Users//garrett//Documents//Blend//"
if not dir in sys.path:
	sys.path.insert(0,dir)
	print(sys.path)

import dlmutils



dlmutils.dlmutils.makeof("D://3d//FDG0160U_DLUDungeonStarterSet_03012017//FDG0160U_DLU_Wall1.stl")
dlmutils.dlmutils.makeof("D://3d//FDG0160U_DLUDungeonStarterSet_03012017//FDG0160U_DLU_Wall2.stl")
dlmutils.dlmutils.makeof("D://3d//FDG0160U_DLUDungeonStarterSet_03012017//FDG0160U_DLU_Corner.stl")