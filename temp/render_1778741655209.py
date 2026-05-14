from manim import *

class WhatIsComputer(MovingCameraScene):
    def construct(self):

        # ---------------- TITLE ----------------
        title = Text("What is a Computer?", font_size=48)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # ---------------- INPUT / PROCESS / OUTPUT ----------------
        input_box = Rectangle(width=3, height=1.5).set_color(BLUE).shift(LEFT*4)
        process_box = Rectangle(width=3, height=1.5).set_color(YELLOW)
        output_box = Rectangle(width=3, height=1.5).set_color(GREEN).shift(RIGHT*4)

        input_text = Text("Input").scale(0.7).move_to(input_box)
        process_text = Text("Process").scale(0.7).move_to(process_box)
        output_text = Text("Output").scale(0.7).move_to(output_box)

        arrow1 = Arrow(input_box.get_right(), process_box.get_left())
        arrow2 = Arrow(process_box.get_right(), output_box.get_left())

        # Show structure
        self.play(FadeIn(input_box), Write(input_text))
        self.play(GrowArrow(arrow1), FadeIn(process_box), Write(process_text))
        self.play(GrowArrow(arrow2), FadeIn(output_box), Write(output_text))

        self.wait(1)

        # ---------------- STEP TEXT ----------------
        step1 = Text("Accepts Input", font_size=28).next_to(input_box, DOWN)
        step2 = Text("Processes Data", font_size=28).next_to(process_box, DOWN)
        step3 = Text("Gives Output", font_size=28).next_to(output_box, DOWN)

        self.play(Write(step1))
        self.play(Write(step2))
        self.play(Write(step3))

        self.wait(1)

        # ---------------- DATA FLOW ----------------
        dot = Dot(color=WHITE).move_to(input_box.get_center())
        self.play(FadeIn(dot))

        self.play(MoveAlongPath(dot, arrow1), run_time=1.2)
        self.play(MoveAlongPath(dot, arrow2), run_time=1.2)

        self.wait(1)

        # ---------------- REAL-LIFE EXAMPLE ----------------
        example_title = Text("Real Life Example", font_size=32).to_edge(DOWN)
        self.play(Write(example_title))

        self.wait(1)

        # Replace labels with example
        food_input = Text("Order Food", font_size=26).move_to(input_box)
        app_process = Text("App Processes", font_size=26).move_to(process_box)
        food_output = Text("Food Delivered", font_size=26).move_to(output_box)

        self.play(
            Transform(input_text, food_input),
            Transform(process_text, app_process),
            Transform(output_text, food_output)
        )

        self.wait(1)

        # Flow again for example
        dot2 = Dot(color=YELLOW).move_to(input_box.get_center())
        self.play(FadeIn(dot2))

        self.play(MoveAlongPath(dot2, arrow1), run_time=1.2)
        self.play(MoveAlongPath(dot2, arrow2), run_time=1.2)

        self.wait(1)

        # ---------------- HIGHLIGHT ----------------
        self.play(input_box.animate.set_fill(BLUE, opacity=0.4))
        self.play(process_box.animate.set_fill(YELLOW, opacity=0.4))
        self.play(output_box.animate.set_fill(GREEN, opacity=0.4))

        self.wait(1)

        # ---------------- FINAL STATEMENT ----------------
        final = Text("Input → Process → Output", font_size=40)
        final.to_edge(DOWN)

        self.play(Transform(example_title, final))

        self.wait(2)