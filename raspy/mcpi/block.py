class Block:
    """Minecraft PI block description. Can be sent to Minecraft.setBlock/s"""

    def __init__(self, id, data=0):
        self.id = id
        self.data = data

    def __cmp__(self, rhs):
        return hash(self) - hash(rhs)

    def __eq__(self, rhs):
        return self.id == rhs.id and self.data == rhs.data

    def __hash__(self):
        return (self.id << 8) + self.data

    def withData(self, data):
        return Block(self.id, data)

    def __iter__(self):
        """Allows a Block to be sent whenever id [and data] is needed"""
        return iter((self.id, self.data))

    def __repr__(self):
        return "Block(%d, %d)" % (self.id, self.data)


AIR = Block(0)
STONE = Block(1)
GRASS = Block(2)
DIRT = Block(3)
COBBLESTONE = Block(4)
WOOD_PLANKS = Block(5)
SAPLING = Block(6)
BEDROCK = Block(7)
WATER_FLOWING = Block(8)
WATER = WATER_FLOWING
WATER_STATIONARY = Block(9)
LAVA_FLOWING = Block(10)
LAVA = LAVA_FLOWING
LAVA_STATIONARY = Block(11)
SAND = Block(12)
GRAVEL = Block(13)
GOLD_ORE = Block(14)
IRON_ORE = Block(15)
COAL_ORE = Block(16)
WOOD = Block(17)
LEAVES = Block(18)
SPONGE = Block(19)
GLASS = Block(20)
LAPIS_LAZULI_ORE = Block(21)
LAPIS_LAZULI_BLOCK = Block(22)
DISPENSER = Block(23)
SANDSTONE = Block(24)
NOTE_BLOCK = Block(25)
BED = Block(26)
RAIL_POWERED = Block(27)
RAIL_DETECTOR = Block(28)
STICKY_PISTON = Block(29)
COBWEB = Block(30)
GRASS_TALL = Block(31)
DEAD_BUSH = Block(32)
PISTON = Block(33)
PISTON_HEAD = Block(34)
WOOL = Block(35)
PISTON_EXTENSION = Block(36)
FLOWER_YELLOW = Block(37)
FLOWER_CYAN = Block(38)
MUSHROOM_BROWN = Block(39)
MUSHROOM_RED = Block(40)
GOLD_BLOCK = Block(41)
IRON_BLOCK = Block(42)
STONE_SLAB_DOUBLE = Block(43)
STONE_SLAB = Block(44)
BRICK_BLOCK = Block(45)
TNT = Block(46)
BOOKSHELF = Block(47)
MOSS_STONE = Block(48)
OBSIDIAN = Block(49)
TORCH = Block(50)
FIRE = Block(51)
MOB_SPAWNER = Block(52)
STAIRS_WOOD = Block(53)
CHEST = Block(54)
REDSTONE_WIRE = Block(55)
DIAMOND_ORE = Block(56)
DIAMOND_BLOCK = Block(57)
CRAFTING_TABLE = Block(58)
WHEAT = Block(59)
FARMLAND = Block(60)
FURNACE_INACTIVE = Block(61)
FURNACE_ACTIVE = Block(62)
SIGN_STANDING = Block(63)
DOOR_WOOD = Block(64)
LADDER = Block(65)
RAIL = Block(66)
STAIRS_COBBLESTONE = Block(67)
SIGN_WALL = Block(68)
LEVER = Block(69)
STONE_PRESSURE_PLATE = Block(70)
DOOR_IRON = Block(71)
WOODEN_PRESSURE_PLATE = Block(72)
REDSTONE_ORE = Block(73)
LIT_REDSTONE_ORE = Block(74)
UNLIT_REDSTONE_TORCH = Block(75)
REDSTONE_TORCH = Block(76)
STONE_BUTTON = Block(77)
SNOW = Block(78)
ICE = Block(79)
SNOW_BLOCK = Block(80)
CACTUS = Block(81)
CLAY = Block(82)
SUGAR_CANE = Block(83)
JUKEBOX = Block(84)
FENCE = Block(85)
PUMPKIN = Block(86)
NETHERRACK = Block(87)
SOUL_SAND = Block(88)
GLOWSTONE_BLOCK = Block(89)
PORTAL = Block(90)
LIT_PUMPKIN = Block(91)
CAKE = Block(92)
UNPOWERED_REPEATER = Block(93)
POWERED_REPEATER = Block(94)
STAINED_GLASS = Block(95)
TRAPDOOR = Block(96)
MONSTER_EGG = Block(97)
STONE_BRICK = Block(98)
BROWN_MUSHROOM_BLOCK = Block(99)
RED_MUSHROOM_BLOCK = Block(100)
IRON_BARS = Block(101)
GLASS_PANE = Block(102)
MELON = Block(103)
FENCE_GATE = Block(107)
STAIRS_BRICK = Block(108)
STAIRS_STONE_BRICK = Block(109)
MYCELIUM = Block(110)
NETHER_BRICK = Block(112)
FENCE_NETHER_BRICK = Block(113)
STAIRS_NETHER_BRICK = Block(114)
END_STONE = Block(121)
WOODEN_SLAB = Block(126)
STAIRS_SANDSTONE = Block(128)
EMERALD_ORE = Block(129)
ENDER_CHEST = Block(130)
COMMAND_BLOCK = Block(137)
BEACON = Block(138)
WOODEN_BUTTON = Block(143)
ANVIL = Block(145)
QUARTZ_BLOCK = Block(155)
QUARTZ_STAIRS = Block(156)
RAIL_ACTIVATOR = Block(157)
STAINED_HARDENED_CLAY = Block(159)
LEAVES2 = Block(161)
BARRIER = Block(166)
TRAPDOOR_IRON = Block(167)
PACKED_ICE = Block(174)
FENCE_SPRUCE = Block(188)
FENCE_BIRCH = Block(189)
FENCE_JUNGLE = Block(190)
FENCE_DARK_OAK = Block(191)
FENCE_ACACIA = Block(192)
DOOR_SPRUCE = Block(193)
DOOR_BIRCH = Block(194)
DOOR_JUNGLE = Block(195)
DOOR_ACACIA = Block(196)
DOOR_DARK_OAK = Block(197)
MAGMA_BLOCK = Block(213)
BONE_BLOCK = Block(216)
LIGHT_BLUE_GLAZED_TERRACOTTA = Block(238)