import mcpi.minecraft as mmc
print('''######################################
#                                    #
#    Raspy Control Initialization    #
#                                    #
######################################
''')
while True:
    try:
        natappPort = int(input("Please specify the natapp port if given; input 0 to connect to local host: "))
    except ValueError:
        print("That wasn't a valid integer.")
    else:
        break
if natappPort:
    mc = mmc.Minecraft.create("server.natappfree.cc", natappPort)
else:
    mc = mmc.Minecraft.create()
print('Minecraft connection "mc" established!')
import mcpi.block as block
import mcpi.entity as entity
