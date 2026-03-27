from manim import *

class QueueExplanationScene(Scene):

    def construct(self):
        self.play_queue_explanation()

    # ============================================================
    # HELPER: Section Heading
    # ============================================================
    def section_heading(self, text):
        title = Text(text, font_size=40, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title), run_time=0.8)
        return title

    # ============================================================
    # HELPER: Clear Screen
    # ============================================================
    def clear_screen(self, direction=UP):
        self.play(*[FadeOut(mob, shift=direction) for mob in self.mobjects])

    # ============================================================
    # 5. QUEUE DATA STRUCTURE EXPLANATION
    # ============================================================
    def play_queue_explanation(self):

        hg = self.section_heading("The Queue — Heart of BFS")

        fifo = Text(
            "FIFO = First In, First Out",
            font_size=34,
            color=BLUE_B
        ).next_to(hg, DOWN, buff=0.5)

        self.play(Write(fifo), run_time=0.8)

        # ---------------------------
        # Visual Queue Boxes
        # ---------------------------
        num_slots = 6

        boxes = VGroup(*[
            Rectangle(
                width=1.1,
                height=0.8,
                color=WHITE,
                fill_opacity=0.05,
                stroke_width=2
            )
            for _ in range(num_slots)
        ])

        boxes.arrange(RIGHT, buff=0.1).shift(UP * 0.5)

        # ---------------------------
        # FRONT & BACK indicators
        # ---------------------------
        front_arr = Arrow(
            boxes[0].get_bottom() + DOWN * 0.5,
            boxes[0].get_bottom(),
            color=GREEN,
            stroke_width=2
        )

        front_lbl = Text(
            "FRONT\n(Dequeue)",
            font_size=18,
            color=GREEN
        ).next_to(front_arr, DOWN, buff=0.05)

        back_arr = Arrow(
            boxes[-1].get_bottom() + DOWN * 0.5,
            boxes[-1].get_bottom(),
            color=RED,
            stroke_width=2
        )

        back_lbl = Text(
            "BACK\n(Enqueue)",
            font_size=18,
            color=RED
        ).next_to(back_arr, DOWN, buff=0.05)

        self.play(Create(boxes), run_time=0.8)
        self.play(
            Create(front_arr),
            Write(front_lbl),
            Create(back_arr),
            Write(back_lbl),
            run_time=0.7
        )

        # ---------------------------
        # Enqueue Operation
        # ---------------------------
        enq_label = Text(
            "Enqueue A, B, C, D:",
            font_size=24,
            color=GREEN
        ).to_edge(DOWN).shift(UP * 1.2)

        self.play(Write(enq_label), run_time=0.5)

        items_text = ["A", "B", "C", "D"]
        item_mobs = []

        for i, it in enumerate(items_text):
            t = Text(it, font_size=26, color=YELLOW, weight=BOLD)

            t.move_to(boxes[i].get_center() + RIGHT * 4)

            self.play(
                t.animate.move_to(boxes[i].get_center()),
                boxes[i].animate.set_fill(BLUE, opacity=0.3),
                run_time=0.5,
                rate_func=smooth
            )

            item_mobs.append(t)
            self.wait(0.15)

        self.wait(0.8)

        # ---------------------------
        # Dequeue Operation
        # ---------------------------
        deq_label = Text(
            "Dequeue → A leaves first:",
            font_size=24,
            color=RED
        ).next_to(enq_label, DOWN, buff=0.3)

        self.play(Write(deq_label), run_time=0.5)

        for i in range(2):
            self.play(
                item_mobs[i].animate.shift(LEFT * 4).set_opacity(0),
                boxes[i].animate.set_fill(BLACK, opacity=0),
                run_time=0.5
            )
            self.wait(0.2)

        # ---------------------------
        # Final Result
        # ---------------------------
        result = Text(
            "First In → First Out (FIFO)",
            font_size=28,
            color=TEAL
        ).to_edge(DOWN, buff=0.3)

        self.play(Write(result), run_time=0.6)

        self.wait(2)

        self.clear_screen(UP)