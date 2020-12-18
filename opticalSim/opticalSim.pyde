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


def setup():
    size(1000, 500)
    background(34,8,81)
    
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
    menuImg = loadImage("lens-button.png")
    menuHighlight = loadImage("lens-button-pressed.png")
    
    # Buttons
    global convergingButton
    global divergingButton
    global convexButton
    global concaveButton
    global associationButton
    # Declaring buttons
    convergingButton = Button(PVector(100, 25), 800, 80, convergingImg, convergingHighlight)
    divergingButton = Button(PVector(100, 115), 800, 80, divergingImg, divergingHighlight)
    convexButton = Button(PVector(100, 205), 800, 80, convexImg, convexHighlight)
    concaveButton = Button(PVector(100, 295), 800, 80, concaveImg, concaveHighlight)
    associationButton = Button(PVector(100, 385), 800, 80, associationImg, associationHighlight)

def draw():
    # Checking screen and drawing different screens
    if screenState == menuScreen:
        drawMenu()
    elif screenState == convergingLens:
        drawConvergingLens()
    elif screenState == divergingLens:
        drawDivergingLens()
    elif screenState == convexMirror:
        drawConvexMirror()
    elif screenState == concaveMirror:
        drawConcaveMirror()
    elif screenState == lensAssociation:
        drawLensAssociation()
    else:
        textSize(24)
        strokeWeight(1)
        stroke(color(0,0,0))
        fill(color(0,0,0))
        textAlign(CENTER, CENTER)
        text("Oops, Something went wrong.", width/2, height/2, width, height,)

# Drawing the menu buttons    
def drawMenu():
    convergingButton.buttonDraw()
    divergingButton.buttonDraw()
    convexButton.buttonDraw()
    concaveButton.buttonDraw()
    associationButton.buttonDraw()
    
def drawConvergingLens():
    fill(255)
    rect(0,0,1000, 700)
def drawDivergingLens():
    fill(255,0,0)
    rect(0,0,1000, 700)
def drawConvexMirror():
    fill(0, 255, 0)
    rect(0,0,1000, 700)
def drawConcaveMirror():
    fill(0,0,255)
    rect(0,0,1000, 700)
def drawLensAssociation():
    fill(0)
    rect(0,0,1000, 700)

# Checks if the mouse is pressed and sees what screen to goes to
def mousePressed():
    global screenState
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
