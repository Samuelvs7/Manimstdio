from manim import *

class HandwritingLesson(Scene):
    def construct(self):
        # 1. Load a Pen or Hand SVG (standard Manim path)
        # For this example, we'll use a Triangle to represent the pen tip
        pen = Triangle(color=WHITE, fill_opacity=1).scale(0.15).rotate(-PI/2)
        
        # --- TITLE: DRAWING THE DEFINITION ---
        title = Text("Computer Functionalities", font_size=40).to_edge(UP)
        
        # Step 1: Writing the text and making the pen follow it
        self.add(pen)
        self.play(pen.animate.move_to(title.get_left()))
        
        # The 'Write' animation makes it look like it's being written
        self.play(
            Write(title),
            MoveAlongPath(pen, title.get_submobjects()[0]), # Pen follows first letter
            run_time=2
        )
        self.play(pen.animate.shift(RIGHT * 0.5)) # Move pen away when done
        
        # --- THE HARDWARE vs SOFTWARE DRAWING ---
        # Drawing System Software (Low-level) [cite: 72, 74]
        system_box = Rectangle(width=4, height=1, color=BLUE)
        sys_text = Text("System Software (OS)", font_size=24).move_to(system_box)
        
        # Drawing Application Software (High-level) [cite: 76, 79]
        app_box = Rectangle(width=4, height=1, color=GREEN).next_to(system_box, UP, buff=0)
        app_text = Text("Application Software", font_size=24).move_to(app_box)

        # Animate the "Drawing" of the Stack
        self.play(pen.animate.move_to(system_box.get_corner(UL)))
        self.play(Create(system_box), pen.animate.move_to(system_box.get_corner(UR)), run_time=1)
        self.play(Write(sys_text))

        self.play(pen.animate.move_to(app_box.get_corner(UL)))
        self.play(Create(app_box), pen.animate.move_to(app_box.get_corner(UR)), run_time=1)
        self.play(Write(app_text))
        
        # Real-time indication of use [cite: 77, 78]
        self.play(Indicate(app_text), pen.animate.scale(1.2))
        self.wait(2)