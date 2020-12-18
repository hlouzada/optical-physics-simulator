class ConvergingLens(object):
    def __init__(self, focal, pos):
        self.focal_length = focal
        self.pos = pos
        self.image_position = None
        self.object_position = None
        self.gamma = None
        self.height_object = None

    def set_object(self, pos, height=None):
        self.object_position = position.x
        if not self.height_object or height:
            self.height_object = height
        self._calcul()

    def _calcul(self):
        if (self.object_position + self.focal_length) != 0 and self.object_position != 0:
            self.image_position = int(self.object_position * self.focal_length / (self.object_position + self.focal_length))
            self.gamma = float(self.focal_length) / float(self.object_position + self.focal_length)

        if (self.object_position + self.focal_length) == 0:
            self.image_position = -1000
            self.gamma = 1000 / self.focal_length

        if self.object_position == 0:
            self.pos_aa = 0
            self.gamma = 1

    def draw_lens(self):
        textSize(12)
        pushMatrix()
        translate(self.position.x, self.position.y)  # Centro da origem do sistema de coordenadas
        # Lente
        fill(blue1)
        stroke(blue1)
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
        stroke(gray1)
        fill(gray1)
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
        image(img, -height / 6, -height / 8)
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
        image(img, -height / 6, -height / 8)
        popMatrix()
        strokeWeight(1)

    def draw_rays(self, ray_color):
        pushMatrix()
        translate(self.position.x, self.position.y)
        strokeWeight(2)
        stroke(ray_color, .8)
        if self.object_position < 0:
            line(self.object_position, -self.height_object, self.position.x, -self.height_object * self.position.x / self.object_position)
            line(self.object_position, -self.height_object, 0, -self.height_object)
            line(0, -self.height_object, self.position.x, -self.height_object + (self.position.x * self.height_object) / self.focal_length)
            if (self.object_position + self.focal_length) != 0:
                line(self.object_position, -self.height_object, 0, -self.height_object * self.focal_length / (self.object_position + self.focal_length))
                line(0, -self.height_object * self.focal_length / (self.object_position + self.focal_length), self.position.x, -self.height_object * self.focal_length / (self.object_position + self.focal_length))

            if (self.object_position + self.focal_length) > 0:
                stroke(ray_color, 0.3)
                line(-self.focal_length, 0, self.object_position, -self.height_object)
                line(self.image_position, -self.gamma * self.height_object, 0, -self.gamma * self.height_object)
                line(self.image_position, -self.gamma * self.height_object, 0, -self.height_object)
                line(self.image_position, -self.gamma * self.height_object, self.object_position, -self.height_object)

        if self.object_position > 0:
            line(-self.position.x, self.height_object * self.position.x / self.object_position, self.position.x, -self.height_object * self.position.x / self.object_position)
            line(-self.position.x, -self.height_object, 0, -self.height_object)
            line(0, -self.height_object, self.position.x, -self.height_object * (1 - self.position.x / self.focal_length))
            line(-self.position.x, -self.height_object * (-self.position.x + self.focal_length) / (self.object_position + self.focal_length), 0, -self.height_object * self.focal_length / (self.object_position + self.focal_length))
            line(0, -self.height_object * self.focal_length / (self.object_position + self.focal_length), self.position.x, -self.height_object * self.focal_length / (self.object_position + self.focal_length))
            stroke(ray_color, 0.3)
            line(0, -self.height_object, self.object_position, -self.height_object)
            line(0, -self.height_object * self.focal_length / (self.object_position + self.focal_length), self.object_position, -self.height_object)

        popMatrix()


class DivergingLens(ConvergingLens):
    def draw_lens(self):
        textSize(12)
        pushMatrix()
        translate(self.position.x, self.position.y)  # Centro da origem do sistema de coordenadas
        # Lente
        fill(blue1)
        stroke(blue1)
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
        stroke(gray1)
        fill(gray1)
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
            line(self.object_position, -self.height_object, self.position.x, -self.height_object * self.position.x / self.object_position)  # passa pela origem
            line(self.object_position, -self.height_object, 0, -self.height_object)  # paralelo ao eixo optico
            line(0, -self.height_object, self.position.x, -self.height_object + (self.position.x * self.height_object) / self.focal_length)
            line(self.object_position, -self.height_object, 0, -self.height_object * self.focal_length / (self.object_position + self.focal_length))  # raio que se prolonga no F
            line(0, -self.height_object * self.focal_length / (self.object_position + self.focal_length), self.position.x, -self.height_object * self.focal_length / (self.object_position + self.focal_length))  # raio emergente paralelo
            stroke(ray_color, 0.25)  # prolongamentos
            line(self.focal_length, 0, self.position.x, -self.height_object + (self.position.x * self.height_object) / self.focal_length)  # prolongamento que passa pelo F'
            line(0, -self.height_object * self.focal_length / (self.object_position + self.focal_length), -self.focal_length, 0)  # prolongamento no F
            line(0, -self.gamma * self.height_object, self.image_position, -self.gamma * self.height_object)
        if self.object_position > 0:
            line(-self.position.x, self.height_object * self.position.x / self.object_position, self.position.x, -self.height_object * self.position.x / self.object_position)  # passa pela origem
            line(-self.position.x, -self.height_object, 0, -self.height_object)  # paralelo ao eixo optico
            line(0, -self.height_object, self.position.x, -self.height_object * (1 - self.position.x / self.focal_length))  # a partir do F'
            if self.object_position + self.focal_length < 0:  # objeto antes do F
                line(-self.position.x, -self.height_object * (-self.position.x + self.focal_length) / (self.object_position + self.focal_length), 0, -self.height_object * self.focal_length / (self.object_position + self.focal_length))
                line(0, -self.height_object * self.focal_length / (self.object_position + self.focal_length), self.position.x, -self.height_object * self.focal_length / (self.object_position + self.focal_length))
                stroke(ray_color, 0.25)  # prolongamentos
                line(0, -self.height_object, self.object_position, -self.height_object)  # paralelo ao eixo optico
                line(self.focal_length, 0, 0, -self.height_object)  # a partir do F'
                line(0, -self.height_object * self.focal_length / (self.object_position + self.focal_length), self.object_position, -self.height_object)

            if (self.object_position + self.focal_length) > 0:
                line(-self.position.x, -self.height_object * (-self.position.x + self.focal_length) / (self.object_position + self.focal_length), 0, -self.height_object * self.focal_length / (self.object_position + self.focal_length))  # passa pelo F
                line(0, -self.height_object * self.focal_length / (self.object_position + self.focal_length), self.position.x, -self.height_object * self.focal_length / (self.object_position + self.focal_length))  # raio emergente paralelo ao eixo optico
                stroke(ray_color, 0.25)  # prolongamentos
                line(0, -self.height_object, self.object_position, -self.height_object)  # paralelo ao eixo optico
                line(self.image_position, -self.height_object * self.focal_length / (self.object_position + self.focal_length), self.position.x, -self.height_object * self.focal_length / (self.object_position + self.focal_length))  # paralelo ao eixo optico
                line(self.image_position, -self.height_object * self.focal_length / (self.object_position + self.focal_length), 0, -self.height_object)  # a partir do F'
                line(0, -self.height_object * self.focal_length / (self.object_position + self.focal_length), self.object_position, -self.height_object)

        popMatrix()


def setup():
    size(1000, 1000 / 2)
    global img, over, move, h2, w1, h1, mirror, black1, gray1, red1, white1, blue1, orange1

    img = loadImage("white-up-pointing-index_261d.png")

    over = False
    move = False
    h2 = 12

    focal = width / 8

    w1 = int(width / 2)
    h1 = int(height / 2 - h2)

    #mirror = ConvergingLens(focal, PVector(w1,h1))
    mirror = DivergingLens(-focal, PVector(w1, h1))
    mirror.set_object(PVector(-2 * focal, 0), height / 10)

    smooth()
    strokeCap(SQUARE)
    frameRate(15)
    textAlign(CENTER, BASELINE)

    # couleurs
    colorMode(RGB, 1.0)
    black1 = color(0.15, 0.15, 0.15, 0.5)
    gray1 = color(0.6, 0.6, 0.6)
    red1 = color(1, 0, 0)
    white1 = color(1, 1, 1)
    blue1 = color(0xff0099CC)
    orange1 = color(0xffff9d00)


def draw():
    global over
    background(.25)
    fill(gray1)
    textSize(12)

    if mouseX > (w1 + mirror.object_position - 30) and mouseX < (w1 + mirror.object_position + 30) and mouseY < (h1 + mirror.height_object) and mouseY > (h1 - mirror.height_object):
        over = True
        active_color = red1
    else:
        over = False
        active_color = gray1

    if move:
        mirror.set_object(PVector(mouseX - w1, 0))

    mirror.draw_lens()
    mirror.draw_object(active_color)
    mirror.draw_image(active_color)
    mirror.draw_rays(red1)
    painel()


def painel():
    fill(black1)
    noStroke()
    rect(0, height - 20, width, 20)
    textSize(12)
    fill(white1)
    if mirror.object_position < 0:
        text("Real Object", width / 12, height - 5)
    else:
        text("Virtual Object", width / 12, height - 5)

    if mirror.image_position < 0:
        text("Virtual Image", width / 4, height - 5)
    else:
        text("Real Image", width / 4, height - 5)

    text("\u0194 transversal = " + nfp(mirror.gamma, 2, 1), width / 2, height - 5)
    text("\u0194 lateral = " + nfp(pow(mirror.gamma, 2), 2, 1), 5 * width / 6, height - 5)


def mousePressed():
    global move
    if over:
        move = True


def mouseReleased():
    global move
    move = False
