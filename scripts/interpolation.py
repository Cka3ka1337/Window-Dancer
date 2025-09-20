import math

from scripts.constants import *


class Instant:
    def next(self, start_pos: tuple, end_pos: tuple) -> tuple:
        sx, sy = start_pos
        ex, ey = end_pos
        
        delta_x = ex - sx
        delta_y = ey - sy

        return delta_x, delta_y


class Linear:
    threshold = InterpolationParams.INTERPOLATION_THRESHOLD # distance px

    
    def next(self, start_pos: tuple, end_pos: tuple, smooth: float) -> tuple:
        sx, sy = start_pos
        ex, ey = end_pos
        
        delta_x = ex - sx
        delta_y = ey - sy
        
        try:
            distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        except OverflowError:
            return 0, 0
        
        if distance < self.threshold:
            smooth *= 2
        
        if distance < 1:
            return 0, 0
        
        angle = math.atan2(delta_y, delta_x)
        
        direction_x = math.cos(angle)
        direction_y = math.sin(angle)
        
        offset_x = (distance * direction_x) * smooth
        offset_y = (distance * direction_y) * smooth

        return offset_x, offset_y


class SmoothedDirection:
    angle_norm = 0
    angle_scale = 0.2
    threshold = InterpolationParams.INTERPOLATION_THRESHOLD # distance px
    
    prev_start_pos = (0, 0)
    override_start_pos = (0, 0)

        
    def next(self, start_pos: tuple, end_pos: tuple, smooth: float) -> tuple:
        sx, sy = start_pos
        ex, ey = end_pos
        
        delta_x = ex - sx
        delta_y = ey - sy
        
        # if self.prev_start_pos == start_pos and self.override_start_pos != start_pos:
        #     self.override_start_pos = start_pos
        #     print(start_pos)
        
        # self.prev_start_pos = start_pos
        
        
        try:
            distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        except OverflowError:
            print(smooth)
            return 0, 0
        
        if distance < self.threshold:
            smooth *= 2
        
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

        return offset_x, offset_y

    
    def back_normalize_angle(self, angle):
        normalized = angle % 360
        if normalized > 180:
            normalized -= 360
        return normalized * -1

    
    def normalize_angle(self, angle):
        normalized = 360 - (angle % 360)
        return normalized