from manim import *

class MyScene(Scene):
    def construct(self):
        # Your animation code here
        text = Text("Hello, Manim!", font_size=72)
        self.play(Write(text))
        self.wait(1)

        # Transform into a star
        star = Star(color=YELLOW, fill_opacity=1).scale(2)
        self.play(Transform(text, star))
        self.play(FadeOut(text))
