from manim import *

class ComputerDiagram(Scene):
    def construct(self):

        # Title
        title = Text("Computer System", font_size=48)
        self.play(Write(title))
        self.play(title.to_edge, UP)

        # INPUT
        input_box = Rectangle(width=2, height=1).set_color(BLUE).shift(LEFT*5)
        input_text = Text("Input").scale(0.5).move_to(input_box)

        # MEMORY
        memory_box = Rectangle(width=2.5, height=1.5).set_color(YELLOW).shift(LEFT*1)
        memory_text = Text("Memory").scale(0.5).move_to(memory_box)

        # CPU (ALU + CU)
        cpu_box = Rectangle(width=3, height=2).set_color(RED).shift(RIGHT*2)
        cpu_text = Text("CPU").scale(0.6).move_to(cpu_box)

        alu_text = Text("ALU").scale(0.4).next_to(cpu_text, DOWN)
        cu_text = Text("CU").scale(0.4).next_to(alu_text, DOWN)

        # OUTPUT
        output_box = Rectangle(width=2, height=1).set_color(GREEN).shift(RIGHT*5)
        output_text = Text("Output").scale(0.5).move_to(output_box)

        # Arrows
        arrow1 = Arrow(input_box.get_right(), memory_box.get_left())
        arrow2 = Arrow(memory_box.get_right(), cpu_box.get_left())
        arrow3 = Arrow(cpu_box.get_right(), output_box.get_left())

        # Show all
        self.play(FadeIn(input_box, input_text))
        self.play(FadeIn(memory_box, memory_text), GrowArrow(arrow1))
        self.play(FadeIn(cpu_box, cpu_text, alu_text, cu_text), GrowArrow(arrow2))
        self.play(FadeIn(output_box, output_text), GrowArrow(arrow3))

        self.wait(1)

        # 🔥 Highlight Input
        self.play(input_box.animate.set_fill(BLUE, opacity=0.5))
        self.wait(1)

        # 🔥 Highlight Memory
        self.play(memory_box.animate.set_fill(YELLOW, opacity=0.5))
        self.wait(1)

        # 🔥 Highlight CPU
        self.play(cpu_box.animate.set_fill(RED, opacity=0.5))
        self.wait(1)

        # 🔥 Highlight Output
        self.play(output_box.animate.set_fill(GREEN, opacity=0.5))
        self.wait(1)

        # 🚀 Data Flow Animation
        dot = Dot(color=WHITE).move_to(input_box)

        self.play(MoveAlongPath(dot, arrow1), run_time=1)
        self.play(MoveAlongPath(dot, arrow2), run_time=1)
        self.play(MoveAlongPath(dot, arrow3), run_time=1)

        self.wait(2)