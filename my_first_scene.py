from manim import *

class HelloManim(Scene):
    def construct(self):
        # 1. Create a text object
        text = Text("Hello, Manim!", font_size=72)
        
        # 2. Write the text to the screen
        self.play(Write(text))
        
        # 3. Wait for 1 second
        self.wait(1)
        
        # 4. Transform the text into a Star
        star = Star(color=YELLOW, fill_opacity=1).scale(2)
        self.play(Transform(text, star))
        
        # 5. Make the star disappear
        self.play(FadeOut(text))
