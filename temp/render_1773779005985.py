from manim import *

class ProComputingEcosystem(Scene):
    def construct(self):
        # --- 1. THE DATA TRANSFORMATION (Real-Time Visual) ---
        title = Text("DATA PROCESSING CYCLE", color=BLUE_B).to_edge(UP)
        
        # Create a "Process" Factory
        factory = RoundedRectangle(height=2, width=3, color=WHITE).shift(ORIGIN)
        factory_label = Text("PROCESSOR", font_size=24).next_to(factory, UP)
        
        # Real-time data transformation: Blue Dot (Raw Data) -> Golden Star (Information)
        data_in = Dot(color=BLUE).shift(LEFT * 5)
        info_out = Star(color=GOLD, n_points=5).scale(0.3).shift(RIGHT * 5)
        
        self.play(Write(title), Create(factory), Write(factory_label))
        self.play(data_in.animate.move_to(factory.get_center()), run_time=1.5)
        self.play(Indicate(factory, color=YELLOW), ReplacementTransform(data_in, info_out.move_to(ORIGIN)))
        self.play(info_out.animate.shift(RIGHT * 5), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(factory, factory_label, info_out, title))

        # --- 2. COMPUTER ARCHITECTURE: THE NERVE CENTER ---
        arch_title = Text("VON NEUMANN ARCHITECTURE", color=GOLD).to_edge(UP)
        
        # ALU & CU (The Heart)
        alu = Rectangle(height=1.5, width=3, color=RED, fill_opacity=0.3).shift(UP * 0.8 + RIGHT * 2)
        cu = Rectangle(height=1.5, width=3, color=YELLOW, fill_opacity=0.3).shift(DOWN * 1 + RIGHT * 2)
        alu_text = Text("ALU", font_size=30).move_to(alu)
        cu_text = Text("CONTROL UNIT\n(Nerve Center)", font_size=20).move_to(cu)
        
        # Memory & I/O
        memory = RoundedRectangle(height=3.5, width=2, color=PURPLE, fill_opacity=0.2).shift(LEFT * 1.5)
        mem_text = Text("MEMORY", font_size=25).move_to(memory)
        input_unit = Square(side_length=1.2, color=BLUE).shift(LEFT * 5)
        output_unit = Square(side_length=1.2, color=GREEN).shift(RIGHT * 5)

        # Connections (Buses)
        bus = Line(input_unit.get_right(), memory.get_left(), color=GREY_A)
        bus2 = Line(memory.get_right(), alu.get_left(), color=GREY_A)
        
        self.play(Write(arch_title))
        self.play(Create(VGroup(alu, cu, memory, input_unit, output_unit)), Write(VGroup(alu_text, cu_text, mem_text)))
        self.play(Create(bus), Create(bus2))

        # Dynamic Pulse: Showing CU controlling everything
        pulses = [Flash(m, color=YELLOW, flash_radius=0.5) for m in [alu, memory, input_unit]]
        self.play(Indicate(cu), *pulses, run_time=2)
        
        self.wait(2)
        self.play(FadeOut(Group(*self.mobjects)))

        # --- 3. SOFTWARE LAYERS (PRO VISUALS) ---
        sw_title = Text("SOFTWARE HIERARCHY", color=CYAN).to_edge(UP)
        
        layers = VGroup(
            VGroup(Rectangle(width=6, height=0.8, color=GREY, fill_opacity=0.9), Text("HARDWARE", font_size=24)),
            VGroup(Rectangle(width=7, height=0.8, color=BLUE_E, fill_opacity=0.8), Text("SYSTEM SOFTWARE (OS)", font_size=24)),
            VGroup(Rectangle(width=8, height=0.8, color=GREEN_E, fill_opacity=0.7), Text("APPLICATION SOFTWARE", font_size=24)),
            VGroup(Rectangle(width=9, height=0.8, color=ORANGE, fill_opacity=0.6), Text("USER INTERFACE", font_size=24))
        ).arrange(UP, buff=0.1).shift(DOWN * 0.5)

        self.play(Write(sw_title))
        self.play(LaggedStart(*[FadeIn(l, shift=UP) for l in layers], lag_ratio=0.4))
        self.play(layers[2].animate.set_color(YELLOW), run_time=1) # Highlight App Software
        self.wait(3)