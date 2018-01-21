"""APoint 类用于记录点，AScript 类用于生成脚本"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class APoint:
    """二维点类"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @property
    def string(self):
        return self.__to_string()
    @staticmethod
    def generate_points(list_X, list_Y, ratio_X = 1, ratio_Y = 1):
        points = []
        my_range = range(0, min(len(list_X), len(list_Y)))
        for i in my_range:
            points.append(APoint(list_X[i] * ratio_X, list_Y[i] * ratio_Y))
        return points
    def __to_string(self):
        return '{0:.2f},{1:.2f}'.format(self.x, self.y)
    def multiply(self, multiplier):
        if isinstance(multiplier, APoint):
            self.x *= multiplier.x
            self.y *= multiplier.y
        else:
            self.x *= multiplier
            self.y *= multiplier
        return self
    def add(self, point):
        if isinstance(point, APoint):
            self.x += point.x
            self.y += point.y
        return self
    def substrate(self, point):
        if isinstance(point, APoint):
            self.x -= point.x
            self.y -= point.y
        return self

class AScript:
    def __init__(self):
        self.commands = []
        self.layers = ['0']
        self.clean_up()
        self.osnap_set(False)
    def create(self, path, name, suffix = 'scr'):
        f = open(path + '/' + name + '.' + suffix, 'w')
        for c in self.commands:
            f.write(c)
        f.close()
        print('AutoCAD 脚本 {0}.{1} 创建完成。'.format(name, suffix))
    def clean_up(self):
        paragraph = 'ERASE ALL \n'
        self.commands.append(paragraph)
        return paragraph
    def osnap_set(self, state):
        s = 'OFF'
        if state:
            s = 'ON' 
        else: 
            s = 'OFF'
        paragraph = 'OSNAP {0}  \n'.format(s)
        self.commands.append(paragraph)
        return paragraph
    def layer_add(self, name, color = 'WHITE'):
        if name not in self.layers:
            self.layers.append(name)
            paragraph = 'LAYER N {0} C {1} {0} \n'.format(name, color)
            self.commands.append(paragraph)
            return len(self.layers) - 1
    def layer_set(self, index):
        if index >= len(self.layers):
            return False
        paragraph = 'LAYER S {0} \n'.format(self.layers[index])
        self.commands.append(paragraph)
        return paragraph
    def draw_line(self, start_point, end_point):
        paragraph = 'LINE {0} {1} \n'.format(start_point.string, end_point.string)
        self.commands.append(paragraph)
        return paragraph
    def draw_spline(self, *args, start = 0):
        paragraph = 'SPLINE '
        for arg in args:
            if isinstance(arg, list):
                for i in range(start, len(arg)):
                    paragraph += arg[i].string + ' '
            elif isinstance(arg, APoint):
                paragraph += arg.string + ' '
        paragraph += '  \n'
        self.commands.append(paragraph)
        return paragraph
    def draw_circle(self, point, r):
        paragraph = 'CIRCLE {0} {1:.2f} \n'.format(point.string, r)
        self.commands.append(paragraph)
        return paragraph
    def draw_text(self, point, text, h = 1, a = 0):
        paragraph = 'TEXT {0} {1} {2} {3} \n'.format(point.string, h, a, text)
        self.commands.append(paragraph)
        return paragraph
    def draw_grid(self, nrow, ncol, offset_width = 1, offset_height = 1):
        for i in range(0, nrow):
            p = 'LINE {0} {1} \n'.format(APoint(0, offset_height * i).string, APoint((ncol - 1) * offset_width, offset_height * i).string)
            self.commands.append(p)
        for i in range(0, ncol):
            p = 'LINE {0} {1} \n'.format(APoint(offset_width * i, 0).string, APoint(offset_width * i, (nrow - 1) * offset_height).string)
            self.commands.append(p)
        return
