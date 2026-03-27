from manim import *

class Module1Intro(Scene):
    def construct(self):

        # ---------------- BACKGROUND ----------------
        bg = Rectangle(width=14, height=8)
        bg.set_fill(BLACK, opacity=1)
        self.add(bg)

        # ---------------- MAIN TITLE ----------------
        title = Text("Module 1", font_size=80, weight=BOLD)
        title.set_color(BLUE)

        # Glow effect
        glow = title.copy().set_color(BLUE).set_opacity(0.3).scale(1.2)

        # ---------------- SUBTITLE ----------------
        subtitle = Text("Fundamentals of Computing", font_size=40)
        subtitle.next_to(title, DOWN)

        # ---------------- VS TECH LOGO ----------------
        logo = Text("VS TECH", font_size=24).to_corner(UR)

        # ---------------- ANIMATION ----------------

        # Title entry
        self.play(FadeIn(glow, scale=1.5), run_time=1)
        self.play(Write(title), run_time=2)

        # Slight zoom (cinematic)
        self.play(self.camera.frame.animate.scale(0.9), run_time=1)

        # Subtitle appears
        self.play(FadeIn(subtitle, shift=DOWN), run_time=1.5)

        # Add logo
        self.play(FadeIn(logo), run_time=1)

        self.wait(2)

        # ---------------- EXIT TRANSITION ----------------
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(glow),
            self.camera.frame.animate.scale(1.1),
            run_time=1.5
        )