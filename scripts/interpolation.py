import math

from raylib import *


class Interpolation:
    def __init__(self):
        self.angle_norm = 0
        self.angle_scale = 0.2
        self.threshold = 50 # distance px
        self.prev_end = None
        
        self.raylib_init()
        self.history = [None for i in range(100)]
    
    
    def raylib_init(self) -> None:
        SetConfigFlags(FLAG_WINDOW_MOUSE_PASSTHROUGH)
        SetConfigFlags(FLAG_WINDOW_TRANSPARENT)
        SetConfigFlags(FLAG_WINDOW_UNDECORATED)
        SetConfigFlags(FLAG_WINDOW_TOPMOST)
        
        InitWindow(1920, 1080, b'')
        SetWindowPosition(0, 0)
        SetTargetFPS(0)
    
    
    def draw_history(self) -> None:
        prev = self.history[0]
        
        for point in self.history:
            if point is None:
                return

            DrawLineEx(
                prev, point, 1, (0, 255, 0, 200)
            )
            DrawCircle(int(point[0]), int(point[1]), 2, (0, 0, 255, 255))
            
            prev = point
        
    
    def draw_angle(self, pos, angle_deg, color) -> None:
        angle_deg = math.radians(angle_deg)
        cos, sin = math.cos(angle_deg), math.sin(angle_deg)
        distance = 40
        
        DrawLineEx(
            pos,
            (
                pos[0] + cos * distance,
                pos[1] + sin * distance
            ),
            1,
            color
        )
        
    
    def next(self, start_pos: tuple, end_pos: tuple, smooth: float) -> tuple:
        ####
        BeginDrawing()
        ClearBackground((0, 0, 0, 0))
        
        if tuple(map(round, start_pos)) not in self.history:
            self.history.append(tuple(map(int, start_pos)))
            self.history.pop(0)
            
        self.draw_history()
        ####

        sx, sy = start_pos
        ex, ey = end_pos
        
        delta_x = ex - sx
        delta_y = ey - sy
        
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        
        if distance < 1:
            return 0, 0
        
        angle = math.atan2(delta_y, delta_x)
        angle_deg = math.degrees(angle)
        angle_norm = self.normalize_angle(angle_deg)
        
        if distance > self.threshold:
            
            delta = angle_norm - self.angle_norm
            
            if delta > 180:
                delta -= 360
                
            elif delta < -180:
                delta += 360
            
            self.angle_norm += delta * self.angle_scale
            self.angle_norm %= 360
            
            next_angle = self.back_normalize_angle(self.angle_norm)
        
        else:
            
            self.angle_norm = angle_norm
            next_angle = angle_deg
        
        
        direction_x = math.cos(math.radians(next_angle))
        direction_y = math.sin(math.radians(next_angle))
        
        offset_x = (distance * direction_x) * smooth
        offset_y = (distance * direction_y) * smooth
        
        ###
        self.draw_angle(start_pos, angle_deg, (0, 0, 255, 255))
        self.draw_angle(start_pos, self.back_normalize_angle(self.angle_norm), (0, 255, 0, 255))
        
        DrawText(f'''
Interpolation
                 
StartPos: {start_pos}
EndPos: {end_pos}
Distance: {round(distance)}
Deg: {round(self.angle_norm)} -> {round(angle_norm)}
Fps: {GetFPS()}'''.encode(), 50, 10, 24, (255, 255, 255, 255))
        
        EndDrawing()
        ###
        
        return offset_x, offset_y

    
    def back_normalize_angle(self, angle):
        normalized = angle % 360
        if normalized > 180:
            normalized -= 360
        return normalized * -1

    
    def normalize_angle(self, angle):
        normalized = 360 - (angle % 360)
        return normalized