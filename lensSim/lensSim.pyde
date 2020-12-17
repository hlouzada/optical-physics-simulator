class ConvergingLens(object):
    def __init__(self, focal, pos):
        self.focal = focal
        self.pos = pos
        self.pos_img = None
        self.pos_obj = None
        self.gamma = None
        self.h_obj = None

    def set_object(self, pos, height=None):
        self.pos_obj = pos.x
        if not self.h_obj or height:
            self.h_obj = height
        self._calcul()

    def _calcul(self):
        if (self.pos_obj + self.focal) != 0 and self.pos_obj != 0:
            self.pos_img = int(self.pos_obj * self.focal / (self.pos_obj + self.focal))
            self.gamma = float(self.focal) / float(self.pos_obj + self.focal)

        if (self.pos_obj + self.focal) == 0:
            self.pos_img = -1000
            self.gamma = 1000 / self.focal

        if self.pos_obj == 0:
            self.pos_aa = 0
            self.gamma = 1

    def draw_lens(self):
        textSize(12)
        pushMatrix()
        translate(self.pos.x, self.pos.y)  # Centro da origem do sistema de coordenadas
        # Lente
        fill(blue1)
        stroke(blue1)
        strokeWeight(3)
        line(0, self.pos.y - 15, 0, -self.pos.y + 15)
        beginShape(TRIANGLES)
        vertex(-6, self.pos.y - 15)
        vertex(6, self.pos.y - 15)
        vertex(0, self.pos.y)
        vertex(-6, -self.pos.y + 15)
        vertex(6, -self.pos.y + 15)
        vertex(0, -self.pos.y)
        endShape()
        # Eixo optico
        strokeWeight(1)
        stroke(gray1)
        fill(gray1)
        line(-self.pos.x, 0, self.pos.x, 0)
        # Focos
        line(-self.focal, -2, -self.focal, 2)
        text("F", -self.focal, -5)
        line(self.focal, -2, self.focal, 2)
        text("F'", self.focal, -5)
        popMatrix()

    def draw_object(self, obj_color):
        tint(obj_color)
        pushMatrix()
        translate(self.pos.x + self.pos_obj, self.pos.y)
        image(img, -height / 6, -height / 8)
        textSize(12)
        text("Object", 0, -height / 8)
        popMatrix()

    def draw_image(self, img_color):
        pushMatrix()
        translate(self.pos.x + self.pos_img, self.pos.y)
        scale(pow(self.gamma, 2), abs(self.gamma))
        if self.gamma < 0:
            rotate(PI)

        tint(img_color, 0.5)
        image(img, -height / 6, -height / 8)
        popMatrix()
        strokeWeight(1)

    def draw_rays(self, ray_color):
        pushMatrix()
        translate(self.pos.x, self.pos.y)
        strokeWeight(2)
        stroke(ray_color, .8)
        if self.pos_obj < 0:
            line(self.pos_obj, -self.h_obj, self.pos.x, -self.h_obj * self.pos.x / self.pos_obj)
            line(self.pos_obj, -self.h_obj, 0, -self.h_obj)
            line(0, -self.h_obj, self.pos.x, -self.h_obj + (self.pos.x * self.h_obj) / self.focal)
            if (self.pos_obj + self.focal) != 0:
                line(self.pos_obj, -self.h_obj, 0, -self.h_obj * self.focal / (self.pos_obj + self.focal))
                line(0, -self.h_obj * self.focal / (self.pos_obj + self.focal), self.pos.x, -self.h_obj * self.focal / (self.pos_obj + self.focal))

            if (self.pos_obj + self.focal) > 0:
                stroke(ray_color, 0.3)
                line(-self.focal, 0, self.pos_obj, -self.h_obj)
                line(self.pos_img, -self.gamma * self.h_obj, 0, -self.gamma * self.h_obj)
                line(self.pos_img, -self.gamma * self.h_obj, 0, -self.h_obj)
                line(self.pos_img, -self.gamma * self.h_obj, self.pos_obj, -self.h_obj)

        if self.pos_obj > 0:
            line(-self.pos.x, self.h_obj * self.pos.x / self.pos_obj, self.pos.x, -self.h_obj * self.pos.x / self.pos_obj)
            line(-self.pos.x, -self.h_obj, 0, -self.h_obj)
            line(0, -self.h_obj, self.pos.x, -self.h_obj * (1 - self.pos.x / self.focal))
            line(-self.pos.x, -self.h_obj * (-self.pos.x + self.focal) / (self.pos_obj + self.focal), 0, -self.h_obj * self.focal / (self.pos_obj + self.focal))
            line(0, -self.h_obj * self.focal / (self.pos_obj + self.focal), self.pos.x, -self.h_obj * self.focal / (self.pos_obj + self.focal))
            stroke(ray_color, 0.3)
            line(0, -self.h_obj, self.pos_obj, -self.h_obj)
            line(0, -self.h_obj * self.focal / (self.pos_obj + self.focal), self.pos_obj, -self.h_obj)

        popMatrix()


class DivergingLens(ConvergingLens):
    def draw_lens(self):
        textSize(12)
        pushMatrix()
        translate(self.pos.x, self.pos.y)  # Centro da origem do sistema de coordenadas
        # Lente
        fill(blue1)
        stroke(blue1)
        strokeWeight(3)
        line(0, self.pos.y, 0, -self.pos.y)
        beginShape(TRIANGLES)
        vertex(-6, self.pos.y)
        vertex(6, self.pos.y)
        vertex(0, self.pos.y - 15)
        vertex(-6, -self.pos.y)
        vertex(6, -self.pos.y)
        vertex(0, -self.pos.y + 15)
        endShape()
        # Eixo optico
        strokeWeight(1)
        stroke(gray1)
        fill(gray1)
        line(-self.pos.x, 0, self.pos.x, 0)
        # Focos
        line(-self.focal, -2, -self.focal, 2)
        text("F", -self.focal, -5)
        line(self.focal, -2, self.focal, 2)
        text("F'", self.focal, -5)
        popMatrix()

    def draw_rays(self, ray_color):
        pushMatrix()
        translate(self.pos.x, self.pos.y)
        strokeWeight(2)
        stroke(ray_color, .8)
        if self.pos_obj < 0:
            line(self.pos_obj, -self.h_obj, self.pos.x, -self.h_obj * self.pos.x / self.pos_obj)  # passa pela origem
            line(self.pos_obj, -self.h_obj, 0, -self.h_obj)  # paralelo ao eixo optico
            line(0, -self.h_obj, self.pos.x, -self.h_obj + (self.pos.x * self.h_obj) / self.focal)
            line(self.pos_obj, -self.h_obj, 0, -self.h_obj * self.focal / (self.pos_obj + self.focal))  # raio que se prolonga no F
            line(0, -self.h_obj * self.focal / (self.pos_obj + self.focal), self.pos.x, -self.h_obj * self.focal / (self.pos_obj + self.focal))  # raio emergente paralelo
            stroke(ray_color, 0.25)  # prolongamentos
            line(self.focal, 0, self.pos.x, -self.h_obj + (self.pos.x * self.h_obj) / self.focal)  # prolongamento que passa pelo F'
            line(0, -self.h_obj * self.focal / (self.pos_obj + self.focal), -self.focal, 0)  # prolongamento no F
            line(0, -self.gamma * self.h_obj, self.pos_img, -self.gamma * self.h_obj)
        if self.pos_obj > 0:
            line(-self.pos.x, self.h_obj * self.pos.x / self.pos_obj, self.pos.x, -self.h_obj * self.pos.x / self.pos_obj)  # passa pela origem
            line(-self.pos.x, -self.h_obj, 0, -self.h_obj)  # paralelo ao eixo optico
            line(0, -self.h_obj, self.pos.x, -self.h_obj * (1 - self.pos.x / self.focal))  # a partir do F'
            if self.pos_obj + self.focal < 0:  # objeto antes do F
                line(-self.pos.x, -self.h_obj * (-self.pos.x + self.focal) / (self.pos_obj + self.focal), 0, -self.h_obj * self.focal / (self.pos_obj + self.focal))
                line(0, -self.h_obj * self.focal / (self.pos_obj + self.focal), self.pos.x, -self.h_obj * self.focal / (self.pos_obj + self.focal))
                stroke(ray_color, 0.25)  # prolongamentos
                line(0, -self.h_obj, self.pos_obj, -self.h_obj)  # paralelo ao eixo optico
                line(self.focal, 0, 0, -self.h_obj)  # a partir do F'
                line(0, -self.h_obj * self.focal / (self.pos_obj + self.focal), self.pos_obj, -self.h_obj)

            if (self.pos_obj + self.focal) > 0:
                line(-self.pos.x, -self.h_obj * (-self.pos.x + self.focal) / (self.pos_obj + self.focal), 0, -self.h_obj * self.focal / (self.pos_obj + self.focal))  # passa pelo F
                line(0, -self.h_obj * self.focal / (self.pos_obj + self.focal), self.pos.x, -self.h_obj * self.focal / (self.pos_obj + self.focal))  # raio emergente paralelo ao eixo optico
                stroke(ray_color, 0.25)  # prolongamentos
                line(0, -self.h_obj, self.pos_obj, -self.h_obj)  # paralelo ao eixo optico
                line(self.pos_img, -self.h_obj * self.focal / (self.pos_obj + self.focal), self.pos.x, -self.h_obj * self.focal / (self.pos_obj + self.focal))  # paralelo ao eixo optico
                line(self.pos_img, -self.h_obj * self.focal / (self.pos_obj + self.focal), 0, -self.h_obj)  # a partir do F'
                line(0, -self.h_obj * self.focal / (self.pos_obj + self.focal), self.pos_obj, -self.h_obj)

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

    if mouseX > (w1 + mirror.pos_obj - 30) and mouseX < (w1 + mirror.pos_obj + 30) and mouseY < (h1 + mirror.h_obj) and mouseY > (h1 - mirror.h_obj):
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
    if mirror.pos_obj < 0:
        text("Real Object", width / 12, height - 5)
    else:
        text("Virtual Object", width / 12, height - 5)

    if mirror.pos_img < 0:
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
