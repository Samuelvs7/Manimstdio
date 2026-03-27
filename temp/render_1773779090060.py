from manim import *

class FullComputingPro(Scene):
    def construct(self):
        # SET COLORS
        COLOR_INPUT = BLUE
        COLOR_CPU = RED
        COLOR_MEM = PURPLE
        COLOR_OUT = GREEN
        
        # --- 1. THE DEFINITION (PRO VISUAL) ---
        title = Text("Fundamentals of Computing", color=BLUE_B).to_edge(UP)
        
        # The 5-Step Logic from Slide 2
        steps = VGroup(
            Text("INPUT", font_size=20),
            Text("STORAGE", font_size=20),
            Text("PROCESS", font_size=20),
            Text("OUTPUT", font_size=20),
            Text("CONTROL", font_size=20)
        ).arrange(RIGHT, buff=0.8).shift(UP*1.5)
        
        icons = VGroup(
            Circle(radius=0.3, color=COLOR_INPUT),
            Square(side_length=0.6, color=COLOR_MEM),
            Triangle(color=COLOR_CPU).scale(0.4),
            RoundedRectangle(width=0.8, height=0.5, color=COLOR_OUT),
            Star(color=YELLOW).scale(0.3)
        )
        
        for i in range(len(icons)):
            icons[i].next_to(steps[i], DOWN)

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(VGroup(steps[i], icons[i]), shift=UP) for i in range(5)], lag_ratio=0.2))
        self.wait(1)
        self.play(FadeOut(steps), FadeOut(icons))

        # --- 2. GENERATIONS (SLIDE 3) - REAL-TIME TIMELINE ---
        gen_text = Text("Evolution of Computer Generations", font_size=32).to_edge(UP)
        timeline = Line(LEFT*5, RIGHT*5, color=GREY).shift(DOWN*1)
        
        # Generation Data
        gen_data = [
            ("1st", "Vacuum Tubes", BLUE_E),
            ("2nd", "Transistors", GREEN_E),
            ("3rd", "ICs", ORANGE),
            ("4th", "VLSI / Micro", RED_B),
            ("5th", "ULSI / AI", PURPLE_A)
        ]
        
        gen_group = VGroup()
        for i, (name, tech, col) in enumerate(gen_data):
            point = Dot(timeline.point_from_proportion(i/4), color=col)
            label = Text(name, font_size=24, color=col).next_to(point, UP)
            desc = Text(tech, font_size=18).next_to(label, UP, buff=0.1)
            gen_group.add(VGroup(point, label, desc))

        self.play(Transform(title, gen_text), Create(timeline))
        self.play(Create(gen_group), run_time=3)
        self.wait(2)
        self.play(FadeOut(gen_group), FadeOut(timeline), FadeOut(title))

        # --- 3. ARCHITECTURE: THE "NERVE CENTER" (SLIDE 9) ---
        arch_title = Text("Inside the System Unit", color=WHITE).to_edge(UP)
        
        # Units
        cpu_box = RoundedRectangle(height=3, width=5, color=WHITE, fill_opacity=0.1)
        alu = Rectangle(height=1, width=2, color=RED, fill_opacity=0.5).move_to(cpu_box.get_center() + UP*0.6)
        cu = Rectangle(height=1, width=2, color=YELLOW, fill_opacity=0.5).move_to(cpu_box.get_center() + DOWN*0.6)
        
        alu_label = Text("ALU", font_size=24).move_to(alu)
        cu_label = Text("Control Unit", font_size=24).move_to(cu)
        
        mem = RoundedRectangle(height=2, width=1.5, color=PURPLE).shift(LEFT*4.5)
        mem_label = Text("Memory", font_size=20).next_to(mem, UP)
        
        # Control signals (Nerve Center Concept)
        signal1 = Arrow(cu.get_left(), mem.get_bottom(), color=YELLOW)
        signal2 = DoubleArrow(cu.get_top(), alu.get_bottom(), color=YELLOW)

        self.play(Write(arch_title))
        self.play(Create(cpu_box), Create(mem), Write(mem_label))
        self.play(FadeIn(alu, alu_label), FadeIn(cu, cu_label))
        
        # Dynamic Signal Animation
        self.play(Indicate(cu), Write(Text("Nerve Center", font_size=20, color=YELLOW).next_to(cu, DOWN)))
        self.play(GrowArrow(signal1), GrowArrow(signal2))
        
        # Real-time Data Flow (Bit Transfer)
        bits = VGroup(*[Dot(radius=0.05, color=BLUE) for _ in range(3)]).arrange(RIGHT, buff=0.1).move_to(mem)
        self.play(bits.animate.move_to(alu.get_center()), run_time=1)
        self.play(Flash(alu, color=RED))
        
        self.wait(2)