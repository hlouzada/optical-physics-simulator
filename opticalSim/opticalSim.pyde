# imports classes from auxiliary files
from mirror import ConcaveMirror, ConvexMirror
from lens import ConvergingLens, DivergingLens

# Class that defines a button
class Button(object):
    
    def __init__(self, position, bWidth, bHeight, img, highlight):
        # Position of the button
        self.position = position
        # color of the button when not pressed
        self.img = img
        # diameter of the button
        self.bWidth = bWidth
        self.bHeight = bHeight
        # color of the button when hover
        self.highlight = highlight
        self.over = False
        self.pressed = False

        
    def buttonDraw(self):
        
        self._mouse_position(mouseX, mouseY)
        if self.over:
            image(self.highlight, self.position.x, self.position.y, self.bWidth, self.bHeight)
        else:
            image(self.img, self.position.x, self.position.y, self.bWidth, self.bHeight)
        
        
    def _mouse_position(self, X, Y):
        if (X >= self.position.x) and (X <= self.position.x + self.bWidth) and (Y >= self.position.y) and (Y <= self.position.y + self.bHeight) :
            self.over = True
        else:
            self.over = False
            
# Variables that indicate which screen will be shown
screenState = 0
menuScreen = 0
convergingLens = 1
divergingLens = 2
convexMirror = 3
concaveMirror = 4
lensAssociation = 5
# Shows if we are using lens or mirror
#global type



def setup():
    size(1000, 500)
    background(0xff220851)
    
    # Loading the images from the buttons
    convergingImg = loadImage("converging-button.png")
    convergingHighlight = loadImage("converging-button-pressed.png")
    divergingImg = loadImage("diverging-button.png")
    divergingHighlight = loadImage("diverging-button-pressed.png")
    convexImg = loadImage("convex-button.png")
    convexHighlight = loadImage("convex-button-pressed.png")
    concaveImg = loadImage("concave-button.png")
    concaveHighlight = loadImage("concave-button-pressed.png")
    associationImg = loadImage("lens-button.png")
    associationHighlight = loadImage("lens-button-pressed.png")
    menuImg = loadImage("menu-button.png")
    menuHighlight = loadImage("menu-button-pressed.png")
    
    # Buttons
    global convergingButton
    global divergingButton
    global convexButton
    global concaveButton
    global associationButton
    global menuButton
    # Declaring buttons
    convergingButton = Button(PVector(100, 25), 800, 80, convergingImg, convergingHighlight)
    divergingButton = Button(PVector(100, 115), 800, 80, divergingImg, divergingHighlight)
    convexButton = Button(PVector(100, 205), 800, 80, convexImg, convexHighlight)
    concaveButton = Button(PVector(100, 295), 800, 80, concaveImg, concaveHighlight)
    associationButton = Button(PVector(100, 385), 800, 80, associationImg, associationHighlight)
    menuButton = Button(PVector(590, 10), 400, 40, menuImg, menuHighlight)
    
    # Setting up mirrors:
    mirrorSetup()
    lensSetup()

def draw():
    # Checking screen and drawing different screens
    if screenState == menuScreen:
        drawMenu()
    elif screenState == convergingLens:
        type = "lens"
        mirrorDraw(converging, type)
    elif screenState == divergingLens:
        type = "lens"
        mirrorDraw(diverging, type)
    elif screenState == convexMirror:
        type = "mirrors"
        mirrorDraw(convex, type)
    elif screenState == concaveMirror:
        type = "mirrors"
        mirrorDraw(concave, type)
    elif screenState == lensAssociation:
        drawLensAssociation()
        type = "lens"
    else:
        textSize(24)
        strokeWeight(1)
        stroke(color(0,0,0))
        fill(color(0,0,0))
        textAlign(CENTER, CENTER)
        text("Oops, Something went wrong.", width/2, height/2, width, height,)

    
    
"""
------------------------SET UP FUNCTIONS----------------------------------
"""
    
def mirrorSetup():

    global img, over, move, h2, w1, h1, mirror, black1, gray1, red1, white1, blue1, concave, convex

    img = loadImage("white-up-pointing-index_261d.png")

    over = False
    move = False
    h2 = 12

    radius = width / 3

    w1 = int(width / 2)
    h1 = int(height / 2 - h2)
    
    # colors
    colorMode(RGB, 1.0)
    black1 = color(0xff000000)
    gray1 = color(0xffC1C1C1)
    red1 = color(0xffF47F6B)
    white1 = color(0xffFFFFFF)
    blue1 = color(0xff0099CC)

    concave = ConcaveMirror(radius, PVector(w1, h1), img, gray1, blue1)
    convex = ConvexMirror(radius, PVector(w1, h1), img, gray1, blue1)
    concave.set_object(PVector(concave.focal_length, 0), height / 10)
    convex.set_object(PVector(convex.focal_length, 0), height / 10)

    smooth()
    strokeCap(SQUARE)
    frameRate(15)
    textAlign(CENTER, BASELINE)
    
def lensSetup():
    
    global converging, diverging
    
    focal = width / 8

    w1 = int(width / 2)
    h1 = int(height / 2 - h2)
    
    converging = ConvergingLens(focal, PVector(w1,h1), img, gray1, blue1)
    diverging = DivergingLens(-focal, PVector(w1, h1), img, gray1, blue1)
    converging.set_object(PVector(-2 * focal, 0), height / 10)
    diverging.set_object(PVector(-2 * focal, 0), height / 10)

    smooth()
    strokeCap(SQUARE)
    frameRate(15)
    textAlign(CENTER, BASELINE)
    
"""
------------------------ DRAW FUNCTIONS----------------------------------
"""

# Drawing the menu buttons    
def drawMenu():
    noTint()
    background(0xff220851)
    convergingButton.buttonDraw()
    divergingButton.buttonDraw()
    convexButton.buttonDraw()
    concaveButton.buttonDraw()
    associationButton.buttonDraw()

# Drawing the mirror types
def mirrorDraw(mirror, type):
    global over
    background(0xff220851)
    fill(gray1)
    textSize(12)
    noTint()
    menuButton.buttonDraw()

    if mouseX > (w1 + mirror.object_position - 30) and mouseX < (w1 + mirror.object_position + 30) and mouseY < (h1 + mirror.height_object) and mouseY > (h1 - mirror.height_object):
        over = True
        active_color = red1
    else:
        over = False
        active_color = gray1

    if move:
        mirror.set_object(PVector(mouseX - w1, 0))

    if type == "lens":
        mirror.draw_lens()
    elif type == "mirrors":
        mirror.draw_mirror()
    mirror.draw_object(active_color)
    mirror.draw_image(active_color)
    mirror.draw_rays(red1)
    painel(mirror)
    
    
def drawConvergingLens():
    fill(255)
    rect(0,0,1000, 700)
def drawDivergingLens():
    fill(255,0,0)
    rect(0,0,1000, 700)
def drawLensAssociation():
    fill(0)
    rect(0,0,1000, 700)

"""
------------------------ MOUSE FUNCTIONS ----------------------------------
"""

# Checks if the mouse is pressed and sees what screen to goes to
def mousePressed():
    global screenState
    if screenState != menuScreen:
        global move
        if over:
            move = True
        if menuButton.over:
            screenState = menuScreen
    else:
        if convergingButton.over:
            screenState = convergingLens
        if divergingButton.over:
            screenState = divergingLens
        if convexButton.over:
            screenState = convexMirror
        if concaveButton.over:
            screenState = concaveMirror
        if associationButton.over:
            screenState = lensAssociation
    
    
def mouseReleased():
    global move
    move = False
    
"""
------------------------ AUXILIARY FUNCTIONS----------------------------------
"""
    
def painel(mirror):
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
    text("\u0194 lateral = " + nfp(pow(mirror.gamma, 2), 2, 1),
         5 * width / 6, height - 5)
