from manim import *

class ComputerDiagram(Scene):
    def construct(self):

        # ---------------- TITLE ----------------
        title = Text("Computer System", font_size=48)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))  # ✅ FIXED

        # ---------------- INPUT ----------------
        input_box = Rectangle(width=2, height=1).set_color(BLUE).shift(LEFT*5)
        input_text = Text("Input").scale(0.5).move_to(input_box)

        # ---------------- MEMORY ----------------
        memory_box = Rectangle(width=2.5, height=1.5).set_color(YELLOW).shift(LEFT*1)
        memory_text = Text("Memory").scale(0.5).move_to(memory_box)

        # ---------------- CPU ----------------
        cpu_box = Rectangle(width=3, height=2).set_color(RED).shift(RIGHT*2)
        cpu_text = Text("CPU").scale(0.6).move_to(cpu_box)

        alu_text = Text("ALU").scale(0.4).next_to(cpu_text, DOWN)
        cu_text = Text("Control Unit").scale(0.35).next_to(alu_text, DOWN)

        # ---------------- OUTPUT ----------------
        output_box = Rectangle(width=2, height=1).set_color(GREEN).shift(RIGHT*5)
        output_text = Text("Output").scale(0.5).move_to(output_box)

        # ---------------- ARROWS ----------------
        arrow1 = Arrow(input_box.get_right(), memory_box.get_left())
        arrow2 = Arrow(memory_box.get_right(), cpu_box.get_left())
        arrow3 = Arrow(cpu_box.get_right(), output_box.get_left())

        # ---------------- SHOW ELEMENTS ----------------
        self.play(FadeIn(input_box), Write(input_text))
        self.play(GrowArrow(arrow1), FadeIn(memory_box), Write(memory_text))
        self.play(GrowArrow(arrow2), FadeIn(cpu_box), Write(cpu_text), FadeIn(alu_text, cu_text))
        self.play(GrowArrow(arrow3), FadeIn(output_box), Write(output_text))

        self.wait(1)

        # ---------------- HIGHLIGHT PARTS ----------------
        self.play(input_box.animate.set_fill(BLUE, opacity=0.4))
        self.wait(0.5)

        self.play(memory_box.animate.set_fill(YELLOW, opacity=0.4))
        self.wait(0.5)

        self.play(cpu_box.animate.set_fill(RED, opacity=0.4))
        self.wait(0.5)

        self.play(output_box.animate.set_fill(GREEN, opacity=0.4))
        self.wait(1)

        # ---------------- DATA FLOW DOT ----------------
        dot = Dot(color=WHITE).move_to(input_box.get_center())

        self.play(FadeIn(dot))

        # Smooth flow animation
        self.play(MoveAlongPath(dot, arrow1), run_time=1.2)
        self.play(MoveAlongPath(dot, arrow2), run_time=1.2)
        self.play(MoveAlongPath(dot, arrow3), run_time=1.2)

        self.wait(1)

        # ---------------- FINAL TEXT ----------------
        final_text = Text("Input → Process → Output", font_size=36)
        final_text.to_edge(DOWN)

        self.play(Write(final_text))
        self.wait(2)