from .connection import Connection
from .vec3 import Vec3
from .event import BlockEvent, ChatEvent
from .entity import Entity
from .block import Block
import math
from .util import flatten

""" Minecraft PI low level api v0.1_1

    Note: many methods have the parameter *arg. This solution makes it
    simple to allow different types, and variable number of arguments.
    The actual magic is a mix of flatten_parameters() and __iter__. Example:
    A Cube class could implement __iter__ to work in Minecraft.setBlocks(c, id).

    (Because of this, it's possible to "erase" arguments. CmdPlayer removes
     entityId, by injecting [] that flattens to nothing)

    @author: Aron Nieminen, Mojang AB"""

""" Updated to include functionality provided by RaspberryJuice:
- getBlocks()
- getDirection()
- getPitch()
- getRotation()
- getPlayerEntityId()
- pollChatPosts()
- setSign()
- spawnEntity()"""


def intFloor(*args):
    return [int(math.floor(x)) for x in flatten(args)]


class CmdPositioner:
    """Methods for setting and getting positions"""

    def __init__(self, connection, packagePrefix):
        self.conn = connection
        self.pkg = packagePrefix

    def getPos(self, id):
        """Get entity position (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + b".getPos", id)
        return Vec3(*list(map(float, s.split(","))))

    def setPos(self, id, *args):
        """Set entity position (entityId:int, x,y,z)"""
        self.conn.send(self.pkg + b".setPos", id, args)

    def getTilePos(self, id):
        """Get entity tile position (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + b".getTile", id)
        return Vec3(*list(map(int, s.split(","))))

    def setTilePos(self, id, *args):
        """Set entity tile position (entityId:int) => Vec3"""
        self.conn.send(self.pkg + b".setTile", id, intFloor(*args))

    def setDirection(self, id, *args):
        """Set entity direction (entityId:int, x,y,z)"""
        self.conn.send(self.pkg + b".setDirection", id, args)

    def getDirection(self, id):
        """Get entity direction (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + b".getDirection", id)
        return Vec3(*map(float, s.split(",")))

    def setRotation(self, id, yaw):
        """Set entity rotation (entityId:int, yaw)"""
        self.conn.send(self.pkg + b".setRotation", id, yaw)

    def getRotation(self, id):
        """get entity rotation (entityId:int) => float"""
        return float(self.conn.sendReceive(self.pkg + b".getRotation", id))

    def setPitch(self, id, pitch):
        """Set entity pitch (entityId:int, pitch)"""
        self.conn.send(self.pkg + b".setPitch", id, pitch)

    def getPitch(self, id):
        """get entity pitch (entityId:int) => float"""
        return float(self.conn.sendReceive(self.pkg + b".getPitch", id))

    def setting(self, setting, status):
        """Set a player setting (setting, status). keys: autojump"""
        self.conn.send(self.pkg + b".setting", setting, 1 if bool(status) else 0)


class CmdEntity(CmdPositioner):
    """Methods for entities"""

    def __init__(self, connection):
        CmdPositioner.__init__(self, connection, b"entity")

    def getName(self, id):
        """Get the list name of the player with entity id => [name:str]
        
        Also can be used to find name of entity if entity is not a player."""
        return self.conn.sendReceive(b"entity.getName", id)


class CmdPlayer(CmdPositioner):
    """Methods for the host (Raspberry Pi) player"""

    def __init__(self, connection):
        CmdPositioner.__init__(self, connection, b"player")
        self.conn = connection

    def getPos(self):
        return CmdPositioner.getPos(self, [])

    def setPos(self, *args):
        return CmdPositioner.setPos(self, [], args)

    def getTilePos(self):
        return CmdPositioner.getTilePos(self, [])

    def setTilePos(self, *args):
        return CmdPositioner.setTilePos(self, [], args)

    def setDirection(self, *args):
        return CmdPositioner.setDirection(self, [], args)

    def getDirection(self):
        return CmdPositioner.getDirection(self, [])

    def setRotation(self, yaw):
        return CmdPositioner.setRotation(self, [], yaw)

    def getRotation(self):
        return CmdPositioner.getRotation(self, [])

    def setPitch(self, pitch):
        return CmdPositioner.setPitch(self, [], pitch)

    def getPitch(self):
        return CmdPositioner.getPitch(self, [])


class CmdCamera:
    def __init__(self, connection):
        self.conn = connection

    def setNormal(self, *args):
        """Set camera mode to normal Minecraft view ([entityId])"""
        self.conn.send(b"camera.mode.setNormal", args)

    def setFixed(self):
        """Set camera mode to fixed view"""
        self.conn.send(b"camera.mode.setFixed")

    def setFollow(self, *args):
        """Set camera mode to follow an entity ([entityId])"""
        self.conn.send(b"camera.mode.setFollow", args)

    def setPos(self, *args):
        """Set camera entity position (x,y,z)"""
        self.conn.send(b"camera.setPos", args)


class CmdEvents:
    """Events"""

    def __init__(self, connection):
        self.conn = connection

    def clearAll(self):
        """Clear all old events"""
        self.conn.send(b"events.clear")

    def pollBlockHits(self):
        """Only triggered by sword => [BlockEvent]"""
        s = self.conn.sendReceive(b"events.block.hits")
        events = [e for e in s.split("|") if e]
        return [BlockEvent.Hit(*list(map(int, e.split(",")))) for e in events]

    def pollChatPosts(self):
        """Triggered by posts to chat => [ChatEvent]"""
        s = self.conn.sendReceive(b"events.chat.posts")
        events = [e for e in s.split("|") if e]
        return [ChatEvent.Post(int(e[:e.find(",")]), e[e.find(",") + 1:]) for e in events]


class Minecraft:
    """The main class to interact with a running instance of Minecraft Pi."""

    def __init__(self, connection):
        self.conn = connection

        self.camera = CmdCamera(connection)
        self.entity = CmdEntity(connection)
        self.player = CmdPlayer(connection)
        self.events = CmdEvents(connection)

    def getBlock(self, *args):
        """Get block (x,y,z) => id:int"""
        return int(self.conn.sendReceive(b"world.getBlock", intFloor(args)))

    def getBlockWithData(self, *args):
        """Get block with data (x,y,z) => Block"""
        ans = self.conn.sendReceive(b"world.getBlockWithData", intFloor(args))
        return Block(*list(map(int, ans.split(","))))

    def getBlocks(self, *args):
        """Get a cuboid of blocks (x0,y0,z0,x1,y1,z1) => [id:int]"""
        s = self.conn.sendReceive(b"world.getBlocks", intFloor(args))
        return map(int, s.split(","))

    def setBlock(self, *args):
        """Set block (x,y,z,id,[data])"""
        self.conn.send(b"world.setBlock", intFloor(args))

    def setBlocks(self, *args):
        """Set a cuboid of blocks (x0,y0,z0,x1,y1,z1,id,[data])"""
        self.conn.send(b"world.setBlocks", intFloor(args))

    def setNoteBlock(self, *args, data=''):
        """Set note box (x,y,z,pitch,[data]), 0 <= pitch <= 24"""
        self.conn.send(b"world.setNoteBlock", intFloor(args), data)

    def setPitch(self, *args):
        """(x,y,z,pitch) Set note to target pitch if the target location is a noteblock"""
        self.conn.send(b"world.setNote", intFloor(args))

    def setSign(self, *args):
        """Set a sign (x,y,z,id,data,[line1,line2,line3,line4])
        
        Wall signs (id=68) require data for facing direction 2=north, 3=south, 4=west, 5=east
        Standing signs (id=63) require data for facing rotation (0-15) 0=south, 4=west, 8=north, 12=east
        @author: Tim Cummings https://www.triptera.com.au/wordpress/"""
        lines = []
        flatargs = []
        for arg in flatten(args):
            flatargs.append(arg)
        for flatarg in flatargs[5:]:
            lines.append(flatarg.replace(",", ";").replace(")", "]").replace("(", "["))
        self.conn.send(b"world.setSign", intFloor(flatargs[0:5]) + lines)

    def spawnEntity(self, *args):
        """Spawn entity (x,y,z,id,[data])"""
        return int(self.conn.sendReceive(b"world.spawnEntity", intFloor(args)))

    def getHeight(self, *args):
        """Get the height of the world (x,z) => int"""
        return int(self.conn.sendReceive(b"world.getHeight", intFloor(args)))

    def getPlayerEntityIds(self):
        """Get the entity ids of the connected players => [id:int]"""
        ids = self.conn.sendReceive(b"world.getPlayerIds")
        return list(map(int, ids.split("|")))

    def getPlayerEntityId(self, name):
        """Get the entity id of the named player => [id:int]"""
        return int(self.conn.sendReceive(b"world.getPlayerId", name))

    def saveCheckpoint(self):
        """Save a checkpoint that can be used for restoring the world"""
        self.conn.send(b"world.checkpoint.save")

    def restoreCheckpoint(self):
        """Restore the world state to the checkpoint"""
        self.conn.send(b"world.checkpoint.restore")

    def postToChat(self, msg):
        """Post a message to the game chat"""
        self.conn.send(b"chat.post", msg)

    def execute(self, cmd: str):
        """Execute vanilla command (cmd)"""
        self.conn.send(b"server.executeCommand", cmd)

    def setting(self, setting, status):
        """Set a world setting (setting, status). keys: world_immutable, nametags_visible"""
        self.conn.send(b"world.setting", setting, 1 if bool(status) else 0)

    def getEntityTypes(self):
        """Return a list of Entity objects representing all the entity types in Minecraft"""
        s = self.conn.sendReceive(b"world.getEntityTypes")
        types = [t for t in s.split("|") if t]
        return [Entity(int(e[:e.find(",")]), e[e.find(",") + 1:]) for e in types]

    # Pseudo-commands
    def setGamemode(self, id: int, gamemode: str):
        """gamemode can only be 'survival', 'creative', 'adventure' or 'spectator'"""
        self.execute(' '.join(["gamemode", gamemode, self.entity.getName(id)]))

    def clearDrop(self):
        """Clear all dropped items"""
        self.execute("kill @e[type=item]")

    def tpAllPlayers(self, pos: Vec3):
        """Spectators excluded"""
        self.execute("tp @a {} {} {}".format(*pos))

    def clearInventory(self, id: int):
        self.execute("clear " + self.entity.getName(id))

    def tell(self, id: int, message: str):
        """Send message to a player"""
        self.execute(' '.join(["tell", self.entity.getName(id), message]))

    def setWeather(self, weather: str, time=0):
        """weather can only be "clear", "rain" or "thunder\""""
        self.execute(' '.join(["weather", weather, str(time) if time > 0 else '']))

    @staticmethod
    def create(address="localhost", port=4711):
        return Minecraft(Connection(address, port))


if __name__ == "__main__":
    mc = Minecraft.create()
    mc.postToChat("Hello, Minecraft!")
