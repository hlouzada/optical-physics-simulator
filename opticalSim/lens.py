#! python
# -*- coding: utf-8 -*-

class ConvergingLens(object):
    def __init__(self, focal, pos, img, gray1, blue1):
        self.focal_length = focal
        self.position = pos
        self.image_position = None
        self.object_position = None
        self.gamma = None
        self.height_object = None
        self.img = img
        self.gray = gray1
        self.blue1 = blue1

    def set_object(self, position, height=None):
        self.object_position = position.x
        if not self.height_object or height:
            self.height_object = height
        self._calcul()

    @property
    def focal_length(self):
        return self.__focal_length

    @focal_length.setter
    def focal_length(self, f):
        if f != 0:
            self.__focal_length = f
        if hasattr(self, "object_position"):
            self._calcul()

    def _calcul(self):
        if (self.object_position + self.focal_length) != 0 and self.object_position != 0:
            self.image_position = int(
                self.object_position * self.focal_length / (self.object_position + self.focal_length))
            self.gamma = float(self.focal_length) / \
                float(self.object_position + self.focal_length)

        if (self.object_position + self.focal_length) == 0:
            self.image_position = -1000
            self.gamma = 1000 / self.focal_length

        if self.object_position == 0:
            self.pos_aa = 0
            self.gamma = 1

    def draw_lens(self):
        textSize(12)
        pushMatrix()
        # Centro da origem do sistema de coordenadas
        translate(self.position.x, self.position.y)
        # Lente
        fill(self.blue1)
        stroke(self.blue1)
        strokeWeight(3)
        line(0, self.position.y - 15, 0, -self.position.y + 15)
        beginShape(TRIANGLES)
        vertex(-6, self.position.y - 15)
        vertex(6, self.position.y - 15)
        vertex(0, self.position.y)
        vertex(-6, -self.position.y + 15)
        vertex(6, -self.position.y + 15)
        vertex(0, -self.position.y)
        endShape()
        # Eixo optico
        strokeWeight(1)
        stroke(self.gray)
        fill(self.gray)
        line(-self.position.x, 0, self.position.x, 0)
        # Focos
        line(-self.focal_length, -2, -self.focal_length, 2)
        text("F", -self.focal_length, -5)
        line(self.focal_length, -2, self.focal_length, 2)
        text("F'", self.focal_length, -5)
        popMatrix()

    def draw_object(self, obj_color):
        tint(obj_color)
        pushMatrix()
        translate(self.position.x + self.object_position, self.position.y)
        image(self.img, -height / 6, -height / 8)
        textSize(12)
        text("Object", 0, -height / 8)
        popMatrix()

    def draw_image(self, img_color):
        pushMatrix()
        translate(self.position.x + self.image_position, self.position.y)
        scale(pow(self.gamma, 2), abs(self.gamma))
        if self.gamma < 0:
            rotate(PI)

        tint(img_color, 0.5)
        image(self.img, -height / 6, -height / 8)
        popMatrix()
        strokeWeight(1)

    def draw_rays(self, ray_color):
        pushMatrix()
        translate(self.position.x, self.position.y)
        strokeWeight(2)
        stroke(ray_color, .8)
        if self.object_position < 0:
            line(self.object_position, -self.height_object, self.position.x, -
                 self.height_object * self.position.x / self.object_position)
            line(self.object_position, -self.height_object, 0, -self.height_object)
            line(0, -self.height_object, self.position.x, -self.height_object +
                 (self.position.x * self.height_object) / self.focal_length)
            if (self.object_position + self.focal_length) != 0:
                line(self.object_position, -self.height_object, 0, -self.height_object *
                     self.focal_length / (self.object_position + self.focal_length))
                line(0, -self.height_object * self.focal_length / (self.object_position + self.focal_length),
                     self.position.x, -self.height_object * self.focal_length / (self.object_position + self.focal_length))

            if (self.object_position + self.focal_length) > 0:
                stroke(ray_color, 0.3)
                line(-self.focal_length, 0,
                     self.object_position, -self.height_object)
                line(self.image_position, -self.gamma *
                     self.height_object, 0, -self.gamma * self.height_object)
                line(self.image_position, -self.gamma *
                     self.height_object, 0, -self.height_object)
                line(self.image_position, -self.gamma * self.height_object,
                     self.object_position, -self.height_object)

        if self.object_position > 0:
            line(-self.position.x, self.height_object * self.position.x / self.object_position,
                 self.position.x, -self.height_object * self.position.x / self.object_position)
            line(-self.position.x, -self.height_object, 0, -self.height_object)
            line(0, -self.height_object, self.position.x, -
                 self.height_object * (1 - self.position.x / self.focal_length))
            line(-self.position.x, -self.height_object * (-self.position.x + self.focal_length) / (self.object_position +
                                                                                                   self.focal_length), 0, -self.height_object * self.focal_length / (self.object_position + self.focal_length))
            line(0, -self.height_object * self.focal_length / (self.object_position + self.focal_length),
                 self.position.x, -self.height_object * self.focal_length / (self.object_position + self.focal_length))
            stroke(ray_color, 0.3)
            line(0, -self.height_object, self.object_position, -self.height_object)
            line(0, -self.height_object * self.focal_length / (self.object_position +
                                                               self.focal_length), self.object_position, -self.height_object)

        popMatrix()


class DivergingLens(ConvergingLens):
    def draw_lens(self):
        textSize(12)
        pushMatrix()
        # Centro da origem do sistema de coordenadas
        translate(self.position.x, self.position.y)
        # Lente
        fill(self.blue1)
        stroke(self.blue1)
        strokeWeight(3)
        line(0, self.position.y, 0, -self.position.y)
        beginShape(TRIANGLES)
        vertex(-6, self.position.y)
        vertex(6, self.position.y)
        vertex(0, self.position.y - 15)
        vertex(-6, -self.position.y)
        vertex(6, -self.position.y)
        vertex(0, -self.position.y + 15)
        endShape()
        # Eixo optico
        strokeWeight(1)
        stroke(self.gray)
        fill(self.gray)
        line(-self.position.x, 0, self.position.x, 0)
        # Focos
        line(-self.focal_length, -2, -self.focal_length, 2)
        text("F", -self.focal_length, -5)
        line(self.focal_length, -2, self.focal_length, 2)
        text("F'", self.focal_length, -5)
        popMatrix()

    def draw_rays(self, ray_color):
        pushMatrix()
        translate(self.position.x, self.position.y)
        strokeWeight(2)
        stroke(ray_color, .8)
        if self.object_position < 0:
            line(self.object_position, -self.height_object, self.position.x, -
                 self.height_object * self.position.x / self.object_position)  # passa pela origem
            line(self.object_position, -self.height_object, 0, -
                 self.height_object)  # paralelo ao eixo optico
            line(0, -self.height_object, self.position.x, -self.height_object +
                 (self.position.x * self.height_object) / self.focal_length)
            line(self.object_position, -self.height_object, 0, -self.height_object *
                 self.focal_length / (self.object_position + self.focal_length))  # raio que se prolonga no F
            line(0, -self.height_object * self.focal_length / (self.object_position + self.focal_length), self.position.x, -
                 self.height_object * self.focal_length / (self.object_position + self.focal_length))  # raio emergente paralelo
            stroke(ray_color, 0.25)  # prolongamentos
            line(self.focal_length, 0, self.position.x, -self.height_object + (self.position.x *
                                                                               self.height_object) / self.focal_length)  # prolongamento que passa pelo F'
            line(0, -self.height_object * self.focal_length / (self.object_position +
                                                               self.focal_length), -self.focal_length, 0)  # prolongamento no F
            line(0, -self.gamma * self.height_object,
                 self.image_position, -self.gamma * self.height_object)
        if self.object_position > 0:
            line(-self.position.x, self.height_object * self.position.x / self.object_position,
                 self.position.x, -self.height_object * self.position.x / self.object_position)  # passa pela origem
            line(-self.position.x, -self.height_object, 0, -
                 self.height_object)  # paralelo ao eixo optico
            line(0, -self.height_object, self.position.x, -self.height_object *
                 (1 - self.position.x / self.focal_length))  # a partir do F'
            if self.object_position + self.focal_length < 0:  # objeto antes do F
                line(-self.position.x, -self.height_object * (-self.position.x + self.focal_length) / (self.object_position +
                                                                                                       self.focal_length), 0, -self.height_object * self.focal_length / (self.object_position + self.focal_length))
                line(0, -self.height_object * self.focal_length / (self.object_position + self.focal_length),
                     self.position.x, -self.height_object * self.focal_length / (self.object_position + self.focal_length))
                stroke(ray_color, 0.25)  # prolongamentos
                line(0, -self.height_object, self.object_position, -
                     self.height_object)  # paralelo ao eixo optico
                line(self.focal_length, 0, 0, -
                     self.height_object)  # a partir do F'
                line(0, -self.height_object * self.focal_length / (self.object_position +
                                                                   self.focal_length), self.object_position, -self.height_object)

            if (self.object_position + self.focal_length) > 0:
                line(-self.position.x, -self.height_object * (-self.position.x + self.focal_length) / (self.object_position +
                                                                                                       self.focal_length), 0, -self.height_object * self.focal_length / (self.object_position + self.focal_length))  # passa pelo F
                line(0, -self.height_object * self.focal_length / (self.object_position + self.focal_length), self.position.x, -
                     self.height_object * self.focal_length / (self.object_position + self.focal_length))  # raio emergente paralelo ao eixo optico
                stroke(ray_color, 0.25)  # prolongamentos
                line(0, -self.height_object, self.object_position, -
                     self.height_object)  # paralelo ao eixo optico
                line(self.image_position, -self.height_object * self.focal_length / (self.object_position + self.focal_length),
                     self.position.x, -self.height_object * self.focal_length / (self.object_position + self.focal_length))  # paralelo ao eixo optico
                line(self.image_position, -self.height_object * self.focal_length /
                     (self.object_position + self.focal_length), 0, -self.height_object)  # a partir do F'
                line(0, -self.height_object * self.focal_length / (self.object_position +
                                                                   self.focal_length), self.object_position, -self.height_object)

        popMatrix()
