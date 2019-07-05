# Universal initialization
import tools
import mcpi.minecraft as mmc
import mcpi.vec3 as vec3
import mcpi.block as block
import mcpi.entity as entity
import mcpi.vec3 as vec3
V3 = vec3.Vec3
print("Loading simple maze...")
while True:
    try:
        natappPort = int(input("Please specify the natapp port if given; \
                               otherwise input 0 to connect to local host: "))
    except ValueError:
        print("That wasn't a valid integer.")
    else:
        break
if natappPort:
    mc = mmc.Minecraft.create("server.natappfree.cc", natappPort)
else:
    mc = mmc.Minecraft.create()
print('Minecraft connection "mc" established!')

# Game init
H, L = 7, 7 # const room Height & Length
spawn = V3(0, 64, 0)
mc.setBlocks(spawn.cubeCenter(64), block.AIR.id) # Clean up the field

##def 
