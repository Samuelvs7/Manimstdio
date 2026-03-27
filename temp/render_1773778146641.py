from manim import *

class ComputingFundamentals(Scene):
    def construct(self):
        # --- SCENE 1: WHAT IS A COMPUTER? ---
        title = Text("What is a Computer?", font_size=48).to_edge(UP)
        definition = Text(
            "An electronic device that accepts data,\nprocesses it, and generates output.",
            font_size=32, line_spacing=1.5
        ).shift(UP * 0.5)

        # Real-time Visuals for Process
        input_box = RoundedRectangle(height=1.5, width=2.5, color=BLUE).shift(LEFT * 4 + DOWN * 1.5)
        process_box = RoundedRectangle(height=1.5, width=2.5, color=YELLOW).shift(DOWN * 1.5)
        output_box = RoundedRectangle(height=1.5, width=2.5, color=GREEN).shift(RIGHT * 4 + DOWN * 1.5)

        labels = VGroup(
            Text("INPUT", font_size=24).next_to(input_box, UP),
            Text("PROCESS", font_size=24).next_to(process_box, UP),
            Text("OUTPUT", font_size=24).next_to(output_box, UP)
        )

        data_particle = Dot(color=WHITE).move_to(input_box.get_center())

        self.play(Write(title))
        self.play(FadeIn(definition, shift=UP))
        self.play(Create(VGroup(input_box, process_box, output_box)), Write(labels))
        
        # Animate the Data Flow (Real-time Example)
        self.play(data_particle.animate.move_to(process_box.get_center()), run_time=1)
        self.play(Indicate(process_box), data_particle.animate.scale(2).set_color(YELLOW))
        self.play(data_particle.animate.move_to(output_box.get_center()), run_time=1)
        self.wait(1)
        self.play(FadeOut(title, definition, input_box, process_box, output_box, labels, data_particle))

        # --- SCENE 2: FUNCTIONAL UNITS (PRO BLOCK DIAGRAM) ---
        units_title = Text("Functional Units of a Computer", font_size=40).to_edge(UP)
        
        # Central Processor Group
        cpu_rect = Rectangle(height=4, width=5, color=GREY_B).shift(RIGHT * 2)
        alu = Rectangle(height=1, width=3, color=RED).move_to(cpu_rect.get_top() + DOWN * 0.8)
        cu = Rectangle(height=1, width=3, color=ORANGE).move_to(cpu_rect.get_bottom() + UP * 0.8)
        alu_text = Text("ALU", font_size=24).move_to(alu.get_center())
        cu_text = Text("Control Unit", font_size=24).move_to(cu.get_center())
        
        # External Units
        mem = RoundedRectangle(height=2, width=2, color=PURPLE).shift(LEFT * 3)
        mem_text = Text("Memory", font_size=24).move_to(mem.get_center())
        
        # Arrows representing "Nerve Center" control
        arrow_cu_mem = CurvedArrow(cu.get_left(), mem.get_bottom(), angle=-TAU/4)
        arrow_cu_alu = DoubleArrow(cu.get_top(), alu.get_bottom(), color=WHITE)

        self.play(Write(units_title))
        self.play(Create(cpu_rect), Create(mem))
        self.play(
            LaggedStart(
                FadeIn(alu, alu_text),
                FadeIn(cu, cu_text),
                FadeIn(mem_text),
                lag_ratio=0.3
            )
        )
        
        # Highlight CU as "Nerve Center"
        self.play(Indicate(cu), cu_text.animate.set_color(YELLOW))
        self.play(Create(arrow_cu_mem), Create(arrow_cu_alu))
        
        # Pulse of "Data" moving between Memory and ALU
        pulse = Dot(color=YELLOW).move_to(mem.get_center())
        self.play(pulse.animate.move_to(alu.get_center()), run_time=1.5, rate_func=slow_into)
        self.play(Flash(alu, color=YELLOW))
        self.play(pulse.animate.move_to(mem.get_center()), run_time=1)

        self.wait(2)