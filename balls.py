import pygame
import random
import numpy as np


# base class for circles/balls
class CircleClass(object):

    def __init__(self, surface, ballCentre, ballRadius, ballColor, ballWidth):
        self.Surface = surface
        self.Center = np.asarray(ballCentre)
        self.Radius = ballRadius
        self.Color = ballColor
        self.Width = ballWidth

    # draws the circle in the window
    def Draw(self):
        self.Sprite = pygame.draw.circle(
            surface=self.Surface,
            center=tuple(self.Center),
            radius=self.Radius,
            color=self.Color,
            width=self.Width
        )


# class for the boundary circle
class BoundaryClass(CircleClass):

    def __init__(self, surface):
        X = 0.5 * surface.get_width()
        Y = 0.5 * surface.get_height()
        Radius = 0.45 * min(surface.get_size())

        # calls the superclass constructor
        super(BoundaryClass, self).__init__(
            surface=surface,
            ballCentre=(X, Y),
            ballRadius=Radius,
            ballColor="white",
            ballWidth=1
        )


# BALL CLASS
class BallClass(CircleClass):

    def __init__(self, surface, ballCentre, ballRadius, ballColor, aVelocity):
        super(BallClass, self).__init__(
            surface=surface,
            ballCentre=ballCentre,
            ballRadius=ballRadius,
            ballColor=ballColor,
            ballWidth=0
        )
        self.Velocity = np.asarray(aVelocity)

    # checks collision with the boundary and adjusts velocity if needed
    def CheckBoundaryClassCollision(self, boundaryClass):
        Distance = np.linalg.norm(self.Center - boundaryClass.Center)
        if boundaryClass.Radius - self.Radius > Distance:
            return
        Normal = self.Center - boundaryClass.Center
        Normal = Normal / np.linalg.norm(Normal)
        NormalVelocity = np.dot(Normal, self.Velocity) * Normal
        Direction = self.Velocity - 2.0 * NormalVelocity
        Direction = Direction / np.linalg.norm(Direction)
        self.Velocity = np.linalg.norm(self.Velocity) * Direction

    # update the ball position
    def Move(self):
        self.Center += self.Velocity


# main game loop
class ApplicationClass(object):

    def __init__(self, windowWidth, windowHeight):
        self.Running = False
        self.Size = (windowWidth, windowHeight)

    def Init(self):
        pygame.init()
        self.Surface = pygame.display.set_mode(
            size=self.Size,
            flags=pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self.SetupBoundaryClass()
        self.SetupBalls()
        self.Running = True

    def SetupBoundaryClass(self):
        self.BoundaryClass = BoundaryClass(self.Surface)
        self.BoundaryClass.Draw()

    def SetupBalls(self, numBalls=20, scaleBalls=3):
        self.Balls = []

        Radius = 0.35 * min(self.Surface.get_size())
        Coords = np.linspace(-0.5, 0.5, numBalls) * Radius

        X = 0.5 * self.Surface.get_width()
        Y = 0.5 * self.Surface.get_height()

        for Coord in Coords:
            Color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            Ball = BallClass(
                surface=self.Surface,
                ballCentre=(X + Coord, Y),
                ballRadius=scaleBalls * 0.5 * Radius / (numBalls - 1.0),
                ballColor=Color,
                aVelocity=[0.0, -2.0]
            )
            Ball.Draw()
            self.Balls.append(Ball)

    def Event(self, aEvent):
        if aEvent.type == pygame.QUIT:
            self.Running = False

    def Loop(self):
        for Ball in self.Balls:
            Ball.CheckBoundaryClassCollision(self.BoundaryClass)
            Ball.Move()

    def Render(self):
        self.Surface.fill("black")
        Items = [self.BoundaryClass] + [Ball for Ball in self.Balls]
        for Item in Items:
            Item.Draw()
        pygame.display.update()

    def Cleanup(self):
        pygame.quit()

    def Execute(self):
        while self.Running:
            for Event in pygame.event.get():
                self.Event(Event)
            self.Loop()
            self.Render()

        self.Cleanup()


if __name__ == "__main__":
    Application = ApplicationClass(windowWidth=800, windowHeight=800)
    Application.Init()
    Application.Execute()
