

# Raspy

A python & Minecraft project that implements many modules, based on [*RaspberryJuice*](https://github.com/zhuowei/RaspberryJuice). Please at least read the **Config** part before beginning.

#### Developing Environment
 - Python 3.7
 - Client: Minecraft Java Edition 1.12.2
 - Server: [PaperMC 1.12.2](https://papermc.io/downloads#Paper-1.12) #1615
 - Server plugin version: raspy-1.0.jar

## Modules

### Maze

A simple maze of adjustable size with completely random paths. The original intention of the design is to learn how to use code.

### Escape

A Parkour game with customizable levels. The master program is called `Chase`. As long as you implement the ABC `Level` in the interface file, you can invent new levels for your own fun.
#### Available Levels
 - Angry Anvil
 - Funny Glass
 - Terrify Lava
 - Calm Ladder
 - Funny (Cactus)

Run/modify `chase.py` to play.

### Music

Automatically read from a midi file and construct it as a redstone music project in Minecraft! Read the `README.md` file in `/raspy/music` for more instructions.
 
### Arch

Some block-setting examples. Proceed with caution with the ones which go in for large-scale construction.


## Commands

*Raspy* supports all including ["extra-commands"](https://github.com/zhuowei/RaspberryJuice/#extra-commands) of *RaspberryJuice*. In addition, these commands below are available in `minecraft.py`.

 - getBlocks(x1,y1,z1,x2,y2,z2) has been implemented
 - execute(cmd) - execute any **server console** command. Powerful and handy. A few pseudo-commands are implemented this way.
     - setGamemode(id: int, gamemode: str)
     - clearDrop()
     - tpAllPlayers(pos: Vec3)
     - clearInventory(id: int)
     - tell(id: int, message: str)
     - setWeather(weather: str, time=0)
 - setNoteBlock(self, x,y,z,pitch, data='') - set one note block,  0 <= pitch <= 24
 - setPitch(x,y,z,pitch) - set note to target pitch if the target location is a noteblock
 - Poll corresponding player events
     - pollDeaths()
     - pollLogins()
     - pollRespawns()
     - pollQuits()

## Config

*Raspy* uses ABSOLUTE coordinates. Please modify the config.yml generated by *RaspberryJuice*.
 **IMPORTANT: Change `location` from RELATIVE to ABSOLUTE**

`start.py` gives an interactive interface, while `tools.py` provides a function to help in-file programming.

## Version history

 - 1.0 Initial release
   - maze
   - arch
   - music
   - escape

## No Warranty

Actually made by beginners with uneven levels, this project delivers lots of defects. Please feel free to improve it. PRs are highly appreciated.
An MIT License was originally planned, but it was cancelled because *RaspberryJuice* has no License.

## Contributors

 - [ArkciaDragone](https://github.com/ArkciaDragone/)
 - [HarryTerpee](https://github.com/HarryTerpee)
 - [ClayLivince](https://github.com/ClayLivince)
 - [Howard-C](https://github.com/Howard-C)
 - [JerryLv007](https://github.com/JerryLv007)
 - [fanqianhua0310](https://github.com/fanqianhua0310)
 - [Kurryyzp](https://github.com/Kurryyzp)

And great honor to *RaspberryJuice*!
