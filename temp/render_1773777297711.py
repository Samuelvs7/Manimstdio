from manim import *

class RealComputer(Scene):
    def construct(self):

        # ---------------- TITLE ----------------
        title = Text("How Computer Works", font_size=48)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # ---------------- MONITOR ----------------
        monitor = Rectangle(width=4, height=2.5).set_color(BLUE)
        screen = Rectangle(width=3.6, height=2).set_fill(BLACK, opacity=1).move_to(monitor)

        stand = Line(monitor.get_bottom(), monitor.get_bottom() + DOWN*1)
        base = Rectangle(width=2, height=0.3).next_to(stand, DOWN)

        monitor_group = VGroup(monitor, screen, stand, base).shift(UP*1)

        # ---------------- KEYBOARD ----------------
        keyboard = Rectangle(width=4, height=0.6).set_color(GREY).shift(DOWN*2)

        # ---------------- CPU CABINET ----------------
        cpu = Rectangle(width=1.5, height=3).set_color(RED).shift(RIGHT*4)

        # ---------------- SHOW COMPUTER ----------------
        self.play(FadeIn(monitor_group))
        self.play(FadeIn(keyboard))
        self.play(FadeIn(cpu))

        self.wait(1)

        # ---------------- INPUT (TYPING EFFECT) ----------------
        typing_text = Text("Typing...", font_size=30).next_to(keyboard, UP)
        self.play(Write(typing_text))

        dot = Dot(color=YELLOW).move_to(keyboard.get_top())

        # Input flow
        self.play(MoveAlongPath(dot, Line(keyboard.get_top(), monitor.get_bottom())), run_time=1)

        self.wait(1)

        # ---------------- INSIDE COMPUTER ----------------
        cpu_label = Text("CPU Processing", font_size=28).move_to(screen)
        self.play(Transform(screen, cpu_label))

        self.wait(1)

        # ---------------- OUTPUT ----------------
        output_text = Text("Result Displayed", font_size=28).move_to(screen)
        self.play(Transform(cpu_label, output_text))

        self.wait(2)

        # ---------------- FINAL FLOW TEXT ----------------
        final = Text("Input → Process → Output", font_size=36).to_edge(DOWN)
        self.play(Write(final))

        self.wait(2)