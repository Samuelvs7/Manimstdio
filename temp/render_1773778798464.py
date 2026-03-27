from manim import *

class FullComputingModule(Scene):
    def construct(self):
        # --- 1. THE DEFINITION (TRANSFORMATION VISUAL) ---
        title = Text("Fundamentals of Computing", color=BLUE_D).to_edge(UP)
        def_text = Text("Data → Processing → Information", font_size=36).shift(UP*1.5)
        
        # Visualizing the 5 Steps of Functionality [cite: 5-9]
        steps = VGroup(
            Text("1. Input", color=BLUE),
            Text("2. Store", color=PURPLE),
            Text("3. Process", color=RED),
            Text("4. Output", color=GREEN),
            Text("5. Control", color=YELLOW)
        ).arrange(RIGHT, buff=0.5).scale(0.6).next_to(def_text, DOWN)

        self.play(Write(title), DrawBorderThenFill(def_text))
        self.play(LaggedStart(*[FadeIn(s, shift=UP) for s in steps], lag_ratio=0.2))
        self.wait(2)
        self.play(FadeOut(def_text), FadeOut(steps))

        # --- 2. GENERATIONS TIMELINE (GLOWING CARDS)  ---
        gen_title = Text("Evolution of Technology", font_size=40, color=GOLD).to_edge(UP)
        gens = VGroup(
            self.create_gen_card("1st", "Vacuum Tubes", "1946-59", BLUE_E),
            self.create_gen_card("2nd", "Transistors", "1959-65", GREEN_E),
            self.create_gen_card("3rd", "ICs", "1965-71", ORANGE),
            self.create_gen_card("4th", "VLSI / Micro", "1971-80", RED_E),
            self.create_gen_card("5th", "ULSI / AI", "1980+", PURPLE_E)
        ).arrange(RIGHT, buff=0.2).scale(0.7).shift(DOWN*0.5)

        self.play(Transform(title, gen_title))
        self.play(LaggedStart(*[FadeIn(g, scale=0.5) for g in gens], lag_ratio=0.3))
        self.wait(2)
        self.play(FadeOut(gens))

        # --- 3. HARDWARE ARCHITECTURE (THE HEART) [cite: 25, 35] ---
        arch_title = Text("Internal Structure (The Processor)", color=WHITE).to_edge(UP)
        
        # Central Hub
        cpu_box = RoundedRectangle(height=4, width=6, color=GREY_A, fill_opacity=0.1)
        alu = Rectangle(height=1.2, width=2.5, color=RED, fill_opacity=0.5).move_to(cpu_box.get_top() + DOWN*1)
        cu = Rectangle(height=1.2, width=2.5, color=YELLOW, fill_opacity=0.5).move_to(cpu_box.get_bottom() + UP*1)
        alu_lab = Text("ALU (Math/Logic)", font_size=20).move_to(alu)
        cu_lab = Text("Control Unit (Nerve Center)", font_size=20).move_to(cu)

        # External units
        input_unit = Square(side_length=1.5, color=BLUE).shift(LEFT*5)
        output_unit = Square(side_length=1.5, color=GREEN).shift(RIGHT*5)
        mem_unit = RoundedRectangle(height=2, width=1.5, color=PURPLE).next_to(cpu_box, UP, buff=0.5)

        self.play(Transform(title, arch_title))
        self.play(Create(cpu_box), Create(input_unit), Create(output_unit), Create(mem_unit))
        self.play(FadeIn(alu, alu_lab), FadeIn(cu, cu_lab))

        # Real-time Data Flow [cite: 43, 45, 62]
        data_packet = Dot(color=WHITE).move_to(input_unit)
        self.play(data_packet.animate.move_to(mem_unit), run_time=1)
        self.play(data_packet.animate.move_to(alu), Indicate(alu))
        self.play(data_packet.animate.move_to(output_unit), run_time=1)
        self.play(Flash(output_unit, color=GREEN))
        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))

        # --- 4. SOFTWARE STACK (3D LAYERS) [cite: 71-80] ---
        sw_title = Text("The Software Ecosystem", color=CYAN).to_edge(UP)
        
        hw_layer = self.create_layer("HARDWARE (Silicon/Circuits)", GREY, 0)
        sys_layer = self.create_layer("SYSTEM SW (OS/Drivers)", BLUE_D, 1)
        app_layer = self.create_layer("APPLICATION SW (Apps/Web)", GREEN_D, 2)

        self.add(sw_title)
        self.play(FadeIn(hw_layer, shift=UP))
        self.play(FadeIn(sys_layer, shift=UP))
        self.play(FadeIn(app_layer, shift=UP))
        
        # Show specific purpose [cite: 80]
        self.play(app_layer.animate.set_color(YELLOW), Indicate(app_layer))
        self.wait(2)

    # Helper functions for pro visuals
    def create_gen_card(self, num, tech, years, col):
        card = VGroup(
            Rectangle(width=2, height=3, color=col, fill_opacity=0.3),
            Text(num, font_size=30, color=col).shift(UP*1),
            Text(tech, font_size=20).shift(ORIGIN),
            Text(years, font_size=16, color=GREY).shift(DOWN*1)
        )
        return card

    def create_layer(self, txt, col, level):
        return VGroup(
            FixedSizeRoundedRectangle(width=8, height=1, color=col, fill_opacity=0.8),
            Text(txt, font_size=28)
        ).shift(DOWN*(1.5 - level*1.2))

class FixedSizeRoundedRectangle(RoundedRectangle):
    pass # Helper for sizing