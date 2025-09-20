class LocalPath:
    path = ''
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(LocalPath, cls).__new__(cls)
            
        return cls.__instance
    

class InterpolationParams:
    SMOOTHNESS_MIN = 2
    SMOOTHNESS_MAX = SMOOTHNESS_MIN + 20
    SMOOTHNESS_DEFAULT = SMOOTHNESS_MIN + (SMOOTHNESS_MAX - SMOOTHNESS_MIN) / 2
    SMOOTHNESS_DEVIDER = 100

    # Расстояние, после которого перестаёт учитываться угол движения при интерполяции
    INTERPOLATION_THRESHOLD = 50
    INTERPOLATION_ANGLE_SCALE = 0.2
    INTERPOLATION_TYPES = ['Instant', 'Linear', 'SDI*']


class Ui:
    SMOOTHNESS_MIN = InterpolationParams.SMOOTHNESS_MIN
    SMOOTHNESS_MAX = InterpolationParams.SMOOTHNESS_MAX
    SMOOTHNESS_DEFAULT = InterpolationParams.SMOOTHNESS_DEFAULT
    
    SCALE_MIN = 5
    SCALE_MAX = 100


class Methods:
    MOVIE_GET = 100
    MOVIE_SET = 101

    SCALE_GET = 102
    SCALE_SET = 103

    SMOOTH_GET = 104
    SMOOTH_SET = 105

    TARGET_GET = 106
    CURRENT_GET = 107
    PREVIOUS_GET = 108


class Variables:
    ANIMATED_MOVEMENT = 200 # BOOL
    INTERPOLATION_TYPE = 201 # STRING


class ConfigKeys:
    WIDTH = 'window.width'
    HEIGHT = 'window.height'
    PATH = 'overlay.path'
    SCALE = 'overlay.scale'
    SMOOTH = 'overlay.smooth'
    UPDATE_OVERLAY_DELAY = 'overlay.update_delay'
    INTERPOLATION_TYPE = 'overlay.interpolation_type'
    

class ConfigDefaults:
    WIDTH = 300
    HEIGHT = 300
    PATH = ''
    SCALE = 50
    SMOOTH = InterpolationParams.SMOOTHNESS_DEFAULT
    UPDATE_OVERLAY_DELAY = 15
    INTERPOLATION_TYPE = 0