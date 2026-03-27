from manim import *

class VSTechIntro(Scene):
    def construct(self):
        bg = Rectangle(width=14, height=8).set_fill(BLACK, opacity=1)
        self.add(bg)

        title = Text("VS TECH", font_size=80, color=BLUE).set_glow_factor(0.5)
        subtitle = Text("Visualizing CSE Concepts", font_size=30).next_to(title, DOWN)

        self.play(FadeIn(title, scale=0.5))
        self.play(Write(subtitle))
        self.wait(1)
        self.play(title.animate.scale(0.6).to_edge(UP))
        self.wait(1)


class InputProcessOutput(Scene):
    def construct(self):
        title = Text("How Computer Works").to_edge(UP)
        self.play(Write(title))

        input_box = Rectangle().set_color(BLUE).shift(LEFT*4)
        process_box = Rectangle().set_color(YELLOW)
        output_box = Rectangle().set_color(GREEN).shift(RIGHT*4)

        input_text = Text("Input").move_to(input_box)
        process_text = Text("Process").move_to(process_box)
        output_text = Text("Output").move_to(output_box)

        arrow1 = Arrow(input_box.get_right(), process_box.get_left())
        arrow2 = Arrow(process_box.get_right(), output_box.get_left())

        self.play(FadeIn(input_box, input_text))
        self.play(FadeIn(process_box, process_text), GrowArrow(arrow1))
        self.play(FadeIn(output_box, output_text), GrowArrow(arrow2))

        self.wait(2)


class FunctionalUnits(Scene):
    def construct(self):
        title = Text("Functional Units").to_edge(UP)
        self.play(Write(title))

        input_u = Text("Input Unit").shift(LEFT*4)
        memory = Text("Memory").shift(LEFT*1)
        alu = Text("ALU").shift(RIGHT*2 + UP)
        cu = Text("Control Unit").shift(RIGHT*2 + DOWN)
        output_u = Text("Output Unit").shift(RIGHT*5)

        self.play(FadeIn(input_u))
        self.play(FadeIn(memory))
        self.play(FadeIn(alu), FadeIn(cu))
        self.play(FadeIn(output_u))

        self.wait(2)


class MemoryTypes(Scene):
    def construct(self):
        title = Text("Memory Types").to_edge(UP)
        self.play(Write(title))

        ram = Text("RAM (Temporary)", color=YELLOW).shift(LEFT*3)
        hdd = Text("Hard Disk (Permanent)", color=BLUE).shift(RIGHT*3)

        self.play(FadeIn(ram))
        self.play(FadeIn(hdd))
        self.wait(2)


class SoftwareTypes(Scene):
    def construct(self):
        title = Text("Software Types").to_edge(UP)
        self.play(Write(title))

        system = Text("System Software\n(OS)", color=GREEN).shift(LEFT*3)
        app = Text("Application Software\n(WhatsApp, Chrome)", color=BLUE).shift(RIGHT*3)

        self.play(FadeIn(system))
        self.play(FadeIn(app))
        self.wait(2)


class ProgrammingFlow(Scene):
    def construct(self):
        title = Text("How Code Runs").to_edge(UP)
        self.play(Write(title))

        steps = ["Code", "Compiler", "Assembly", "Machine Code", "Run"]
        group = VGroup(*[Text(s) for s in steps]).arrange(RIGHT, buff=1)

        arrows = VGroup()
        for i in range(len(group)-1):
            arrows.add(Arrow(group[i].get_right(), group[i+1].get_left()))

        self.play(FadeIn(group))
        self.play(*[GrowArrow(a) for a in arrows])
        self.wait(2)


class Ending(Scene):
    def construct(self):
        text = Text("Input → Process → Output", font_size=48)
        self.play(Write(text))
        self.wait(2)