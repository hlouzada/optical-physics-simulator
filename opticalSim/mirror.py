#! python
# -*- coding: utf-8 -*-


# Class that defines a concave mirror
class ConcaveMirror(object):

    def __init__(self, radius, position, img, gray1, blue1):
        self.focal_length = radius / 2
        self.position = position
        self.image_position = None
        self.object_position = None
        self.gamma = None  # ratio between height of the image and height of the object
        self.height_object = None
        self.img = img
        self.gray = gray1
        self.blue1 = blue1

    # Place an object in front of the mirror
    def set_object(self, obj_position, height=None):
        self.object_position = obj_position.x
        if not self.height_object or height:
            self.height_object = height
        self._calculate()

    # Calculates position and size of the image
    def _calculate(self):
        # Verificar para termos certeza que não estamos dividindo por zero
        if (self.object_position + self.focal_length) != 0 and self.object_position != 0:
            self.image_position = \
                (self.object_position * self.focal_length) / \
                (self.object_position + self.focal_length)
            self.gamma = float(self.focal_length) / \
                float(self.focal_length + self.object_position)

        # Caso esteja dividindo por zero
        if (self.object_position + self.focal_length) == 0:
            self.image_position = - 1000
            self.gamma = 1000 / self.focal_length

        if self.object_position == 0:
            self.image_position = 0
            self.gamma = 1

    # Draws the mirror and the focus and optical axis of the mirror
    def draw_mirror(self):
        textSize(12)
        pushMatrix()
        translate(self.position.x, self.position.y)  # Coordinate system origin
        # Mirror
        fill(self.blue1)
        stroke(self.blue1)
        strokeWeight(2.5)
        noFill()
        # Desenhando o arco do espelho : x, y, largura, altura, angulo de inicio, angulo de fim
        arc(-self.focal_length, 0, self.focal_length *
            2, self.focal_length * 2, -PI / 6, PI / 6)
        # Axis
        strokeWeight(1)
        stroke(self.gray)
        fill(self.gray)
        line(-self.position.x, 0, self.position.x, 0)
        # Focus
        line(-self.focal_length, -2, -self.focal_length, 2)
        text("F", -self.focal_length, -5)
        # Origin
        line(-self.focal_length * 2, -2, -self.focal_length * 2, 2)
        text("C", -self.focal_length * 2, -5)
        popMatrix()

    # Draws the object
    def draw_object(self, object_color):
        tint(object_color)
        pushMatrix()
        translate(self.position.x + self.object_position, self.position.y)
        image(self.img, -height / 6, -height / 8)
        textSize(12)
        text("Object", 0, -height / 8)
        popMatrix()

    # Draws the image
    def draw_image(self, image_color):
        pushMatrix()
        translate(self.position.x - self.image_position, self.position.y)
        scale(pow(self.gamma, 2), abs(self.gamma))
        if self.gamma < 0:
            rotate(PI)

        tint(image_color, 0.5)
        image(self.img, -height / 6, -height / 8)
        popMatrix()
        strokeWeight(1)

    def draw_rays(self, ray_color):
        pushMatrix()
        translate(self.position.x, self.position.y)
        strokeWeight(2)
        stroke(ray_color, .8)
        if self.object_position < 0:
            line(self.object_position, -self.height_object, 0, 0)
            line(self.object_position, -self.height_object, 0, -self.height_object)
            stroke(ray_color, .6)
            line(0, 0, -self.position.x, -self.gamma*self.height_object*self.position.x/self.image_position)
            line(0, -self.height_object, -self.position.x, -self.height_object + (self.position.x * self.height_object) / self.focal_length)
            if (self.object_position + self.focal_length) < 0:
                line(0, -self.height_object * self.focal_length / (self.object_position + self.focal_length), -self.position.x, -self.height_object * self.focal_length / (self.object_position + self.focal_length))
                stroke(ray_color, .8)
                line(self.object_position, -self.height_object, 0, -self.height_object *self.focal_length / (self.object_position + self.focal_length))
                

            else:
                #line()
                stroke(ray_color, 0.3)
                line(-self.focal_length, 0,
                     self.object_position, -self.height_object)
                line(-self.image_position, -self.gamma *
                     self.height_object, 0, -self.gamma * self.height_object)
                line(-self.image_position, -self.gamma *
                     self.height_object, 0, -self.height_object)
                line(-self.image_position, -self.gamma * self.height_object,
                     self.object_position, -self.height_object)

        if self.object_position > 0:
            line(self.object_position, -self.height_object, 0, 0)
            line(0, -self.height_object, self.object_position, -self.height_object)
            line(self.object_position, -self.height_object, 0, -self.height_object * self.focal_length / (self.object_position + self.focal_length))
            stroke(ray_color, .6)
            line(0, 0, self.position.x, self.height_object * self.position.x /self.object_position)
            line(0, -self.height_object, self.position.x, -self.height_object *(1 + self.position.x / self.focal_length))
            line(0, -self.gamma * self.height_object, self.position.x, -self.gamma * self.height_object)
            stroke(ray_color, .25)
            line(0, 0, -self.position.x, -self.height_object * self.position.x /self.object_position)
            line(0, -self.gamma * self.height_object, -self.position.x, -self.gamma * self.height_object)
            line(0, -self.height_object, -self.position.x, -self.height_object *(1 - self.position.x / self.focal_length))

        popMatrix()


# Class that defines a convex mirror
class ConvexMirror(ConcaveMirror):

    def __init__(self, radius, position, img, gray1, blue1):
        self.focal_length = -radius / 2
        self.position = position
        self.image_position = None
        self.object_position = None
        self.gamma = None  # ratio between height of the image and height of the object
        self.height_object = None
        self.img = img
        self.gray = gray1
        self.blue1 = blue1

    # Draws the mirror and the focus and optical axis of the mirror
    def draw_mirror(self):
        textSize(12)
        pushMatrix()
        translate(self.position.x, self.position.y)  # Coordinate system origin
        # Mirror
        fill(self.blue1)
        stroke(self.blue1)
        strokeWeight(2.5)
        noFill()
        # Desenhando o arco do espelho : x, y, largura, altura, angulo de inicio, angulo de fim
        arc(-self.focal_length, 0, -self.focal_length * 2, -
            self.focal_length * 2, PI * 5 / 6, PI * 7 / 6)
        # Axis
        strokeWeight(1)
        stroke(self.gray)
        fill(self.gray)
        line(-self.position.x, 0, self.position.x, 0)
        # Focus
        line(-self.focal_length, -2, -self.focal_length, 2)
        text("F", -self.focal_length, -5)
        # Origin
        line(-self.focal_length * 2, -2, -self.focal_length * 2, 2)
        text("C", -self.focal_length * 2, -5)
        popMatrix()

    def draw_rays(self, ray_color):
        pushMatrix()
        translate(self.position.x, self.position.y)
        strokeWeight(2)
        stroke(ray_color, .8)
        if self.object_position < 0:
            line(self.object_position, -self.height_object, 0, 0)
            line(0, -self.height_object, self.object_position, -self.height_object)
            line(self.object_position, -self.height_object, 0, -self.height_object * self.focal_length / (self.object_position + self.focal_length))
            stroke(ray_color, .6)
            line(0, 0, -self.position.x, -self.height_object * self.position.x /self.object_position)
            line(0, -self.gamma * self.height_object, -self.position.x, -self.gamma * self.height_object)
            line(0, -self.height_object, -self.position.x, -self.height_object *(1 - self.position.x / self.focal_length))
            stroke(ray_color, .25)
            line(0, 0, self.position.x, -self.height_object * self.position.x /self.object_position)
            line(0, -self.height_object, self.position.x, -self.height_object *(1 + self.position.x / self.focal_length))
            line(0, -self.gamma * self.height_object, self.position.x, -self.gamma * self.height_object)

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
                line(0, self.height_object * self.focal_length / (self.object_position - self.focal_length),
                     self.position.x, self.height_object * self.focal_length / (self.object_position - self.focal_length))
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
                line(-self.image_position, -self.height_object * self.focal_length / (self.object_position + self.focal_length),
                     self.position.x, -self.height_object * self.focal_length / (self.object_position + self.focal_length))  # paralelo ao eixo optico
                line(-self.image_position, -self.height_object * self.focal_length /
                     (self.object_position + self.focal_length), 0, -self.height_object)  # a partir do F'
                line(0, -self.height_object * self.focal_length / (self.object_position +
                                                                   self.focal_length), self.object_position, -self.height_object)

        popMatrix()
