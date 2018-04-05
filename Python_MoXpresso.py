# MoSelection from Python
# authored by bazz : http://www.bazz1.com
import c4d

width = 3
height = 3

doc.StartUndo()

cloner = c4d.BaseObject(1018544)
# create cloner
doc.InsertObject(cloner, parent = None, pred = None, checknames = True)
# create Cube
cube = c4d.BaseObject(c4d.Ocube)
doc.InsertObject(cube, parent = cloner, pred = None, checknames = True)

# Create xpresso on cloner
xtag = c4d.BaseTag(c4d.Texpresso)
cloner.InsertTag(xtag)
nodemaster = xtag.GetNodeMaster()

# change Cloner -> Object -> Mode to "Grid Array"
cloner[c4d.ID_MG_MOTIONGENERATOR_MODE] = 3

# change Cloner -> Object -> Count(3) to (width, height, 1)
cloner[c4d.MG_GRID_RESOLUTION] = c4d.Vector(3,3,1)

# change Cloner -> Object -> Size(3) to (width * cubeX, height * cubeY, nonimportant value)
cloner[c4d.MG_GRID_SIZE] = c4d.Vector(width * cube[c4d.PRIM_CUBE_LEN].x, height * cube[c4d.PRIM_CUBE_LEN].y, 1)


## completely unnecessary code because C4D is messed up
## Need this code to access the "Object" Port on the actual Mograph Selection Tag in Xpresso
## this is because there is a bug in C4D and you cannot Add the Object port
bc = c4d.GetCustomDataTypeDefault(c4d.DTYPE_BASELISTLINK) 
bc[c4d.DESC_NAME] = "obj" 


## Make mograph selection tag
ms_tag = c4d.BaseTag(1021338) # mograph selection tag
## Note, clone grid array y axis in inverted tile 0 is bottom-left
## Name the mograph selection tag by the color it represents : ie (255,255,255)
ms_tag.SetName("Mograph Selection Tag")
linkDataType = ms_tag.AddUserData(bc)
ms_tag[linkDataType] = ms_tag
# ms_tag.__setitem__((c4d.ID_USERDATA,1), ms_tag)
## Add tag to cloner
cloner.InsertTag(ms_tag)
# Add the MoSelection tag to XPresso
### XPRESSO
xnode_mograph_selection_tag = nodemaster.CreateNode(nodemaster.GetRoot(),c4d.ID_OPERATOR_OBJECT,None)
xnode_mograph_selection_tag[c4d.GV_OBJECT_OBJECT_ID] = ms_tag
# Create Object output port
xnode_mograph_selection_tag_port_out_object = xnode_mograph_selection_tag.AddPort(c4d.GV_PORT_OUTPUT, \
c4d.DescID(c4d.DescLevel(c4d.ID_USERDATA, c4d.DTYPE_SUBCONTAINER, 0), c4d.DescLevel(1)), message = True)

# Add mograph selection node to Xpresso
xnode_mograph_selection = nodemaster.CreateNode(nodemaster.GetRoot(),1021344,None,550,0)	# Xpresso mograph selection ID
# xnode_mograph_selection_port_in_selection_tag = xnode_mograph_selection.AddPort(c4d.GV_PORT_INPUT, 1000) # would have added Selection tag, but it already exists at index 0
xnode_mograph_selection_port_in_selection_tag = xnode_mograph_selection.GetInPort(0) #should probably be getting the ports by name
xnode_mograph_selection_port_in_index = xnode_mograph_selection.GetInPort(1)
xnode_mograph_selection_port_in_select = xnode_mograph_selection.AddPort(c4d.GV_PORT_INPUT, 1001) # add Select index 2
# Connect~~
xnode_mograph_selection_tag_port_out_object.Connect(xnode_mograph_selection_port_in_selection_tag)


# Create Iteration node
xnode_iteration = nodemaster.CreateNode(nodemaster.GetRoot(),c4d.ID_OPERATOR_ITERATE, None, 0, 100)
xnode_iteration[c4d.GV_ITERATE_INPUT_LOWER] = 0
xnode_iteration[c4d.GV_ITERATE_INPUT_UPPER] = (width*height) - 1 #inclusive

xnode_iteration_OUT_iteration = xnode_iteration.GetOutPort(0)
# Connect Iteration Iteration -> Mograph Selection - Index
xnode_iteration_OUT_iteration.Connect(xnode_mograph_selection_port_in_index)

# Create Python Node
xnode_python = nodemaster.CreateNode(nodemaster.GetRoot(),1022471,insert=None, x=300, y=200) #Create python node
# alter Python Text
xnode_python[c4d.GV_PYTHON_CODE] = \
"""
import c4d
def main():
	global Select
	Select = 0
	if Index % 2:
		Select = 1"""
# Python Ports configuration
xnode_python_Index_IN = xnode_python.GetInPort(0)
xnode_python_Index_IN.SetName("Index")
xnode_python_Select_OUT = xnode_python.GetOutPort(0)
xnode_python_Select_OUT.SetName("Select")

# Connect Iteration Iteration -> Python - Index
xnode_iteration_OUT_iteration.Connect(xnode_python_Index_IN)
# Connect Python - Select -> Mograph Selection - Select
xnode_python_Select_OUT.Connect(xnode_mograph_selection_port_in_select)


doc.EndUndo()
c4d.EventAdd()