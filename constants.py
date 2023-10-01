PIXEL_RATIO = 1         # scale up all image graphics
WIDTH = 1100            # window size
HEIGHT = 700
TIME_STEP = 60          # fps
FRAME_RATE = 40         # ms for animations

GRID_SCALE = 120        # grid square dimensions
GRID_SKEW = -.2         # grid skew factor
GRID_X = 325            # grid center
GRID_Y = 275

SPEED = 0.08
JUMP = 0.5

WORD_SCALE = 44
WORD_X = (WIDTH + GRID_X * 2) / 2 + 4
WORD_Y = 275 - 3
MAX_WORDS = 10

QUEUE_X = WIDTH/2
QUEUE_Y = 640
PASS_X = GRID_X * 2 - 164/2
PASS_Y = 100/2

SPELLS = ("SMITE", "SLASH", "STAB", "JAB", "BISECT", "VORTEX", "ZAP", "SHOCK", "JOLT", "BURN", "BEAM", "RAY", "TORCH",
          "FIREBALL", "DOOM", "HAUNT", "HEX", "CURSE", "DARKNESS", "SAVE", "LIFE", "RECOVER", "HEAL", "RADIATE",
          "THUNDER", "SHADOW", "SPARK", "SORROW", "SWING", "SLICE", "CHARGE", "SEVER", "EXECUTE", "REGROWTH", "FLAME",
          "STAPLE", "CHOMP", "TOAST", "VAMPIRE", "LEECH", "DEVOUR", "CONSUME", "HUNGER")
