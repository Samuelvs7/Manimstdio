from manim import *
import numpy as np
from collections import deque


class BFSCompleteVideo(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"

        self.play_intro()
        self.play_what_is_graph()
        self.play_what_is_bfs()
        self.play_algorithm_steps()
        self.play_queue_explanation()
        self.play_bfs_traversal_tree()
        self.play_bfs_traversal_cyclic()
        self.play_complexity()
        self.play_bfs_vs_dfs()
        self.play_python_code()
        self.play_applications()
        self.play_summary()

    # ────────────────────────────────────────────────────────
    # HELPER: clear screen with a slide direction
    # ────────────────────────────────────────────────────────
    def clear_screen(self, direction=LEFT, distance=16):
        if self.mobjects:
            self.play(
                *[m.animate.shift(direction * distance) for m in self.mobjects],
                run_time=1.2,
                rate_func=smooth,
            )
            self.clear()

    # ────────────────────────────────────────────────────────
    # HELPER: section heading with underline
    # ────────────────────────────────────────────────────────
    def section_heading(self, text, color=YELLOW):
        heading = Text(text, font_size=48, color=color, weight=BOLD).to_edge(
            UP, buff=0.4
        )
        underline = Line(
            heading.get_left() + DOWN * 0.35,
            heading.get_right() + DOWN * 0.35,
            color=color,
            stroke_width=2,
        )
        self.play(FadeIn(heading, shift=DOWN * 0.5), Create(underline), run_time=1)
        return VGroup(heading, underline)

    # ────────────────────────────────────────────────────────
    # HELPER: build a node circle with label
    # ────────────────────────────────────────────────────────
    def make_node(self, label, pos, radius=0.4, color=BLUE):
        c = Circle(
            radius=radius, color=color, fill_opacity=0.15, stroke_width=3
        ).move_to(pos)
        t = Text(label, font_size=26, color=WHITE, weight=BOLD).move_to(pos)
        return VGroup(c, t)

    # ────────────────────────────────────────────────────────
    # HELPER: build edge line shortened to not overlap nodes
    # ────────────────────────────────────────────────────────
    def make_edge(self, pos_a, pos_b, radius=0.4, color=GREY_B):
        direction = pos_b - pos_a
        dist = np.linalg.norm(direction)
        if dist == 0:
            return Line(pos_a, pos_b, color=color, stroke_width=2.5)
        unit = direction / dist
        start = pos_a + unit * radius
        end = pos_b - unit * radius
        return Line(start, end, color=color, stroke_width=2.5)

    # ============================================================
    # 1. INTRO
    # ============================================================
    def play_intro(self):
        title = Text("Breadth First Search", font_size=72, color=WHITE, weight=BOLD)
        bfs_short = Text("(BFS)", font_size=60, color=YELLOW).next_to(
            title, DOWN, buff=0.3
        )
        tagline = Text(
            "A Complete Visual Guide", font_size=36, color=BLUE_B
        ).next_to(bfs_short, DOWN, buff=0.5)
        underline = Line(LEFT * 4, RIGHT * 4, color=YELLOW).next_to(
            tagline, DOWN, buff=0.4
        )
        sub = Text(
            "Graph Traversal Algorithm", font_size=28, color=GREY_B
        ).next_to(underline, DOWN, buff=0.4)

        self.play(FadeIn(title, shift=DOWN * 1.5), run_time=1.5)
        self.play(FadeIn(bfs_short, shift=UP * 0.5), run_time=0.8)
        self.play(Write(tagline), run_time=1)
        self.play(Create(underline), run_time=0.6)
        self.play(FadeIn(sub, shift=UP * 0.3))
        self.wait(2)
        self.clear_screen(LEFT)

    # ============================================================
    # 2. WHAT IS A GRAPH
    # ============================================================
    def play_what_is_graph(self):
        hg = self.section_heading("What is a Graph?")

        defn = VGroup(
            Text("A Graph consists of:", font_size=30, color=WHITE),
            Text("  • Vertices (Nodes) — entities", font_size=26, color=BLUE_B),
            Text(
                "  • Edges (Links) — connections between them",
                font_size=26,
                color=GREEN_B,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        defn.next_to(hg, DOWN, buff=0.5).shift(LEFT * 2)
        box = SurroundingRectangle(defn, color=BLUE, buff=0.25, corner_radius=0.1)
        self.play(FadeIn(defn, shift=UP * 0.5), Create(box), run_time=1.2)
        self.wait(1)

        # Small example graph on the right
        positions = {
            "1": np.array([3.0, 0.5, 0]),
            "2": np.array([1.5, -0.8, 0]),
            "3": np.array([4.5, -0.8, 0]),
            "4": np.array([3.0, -2.0, 0]),
        }
        edge_pairs = [("1", "2"), ("1", "3"), ("2", "4"), ("3", "4"), ("2", "3")]
        edges = VGroup(
            *[
                self.make_edge(positions[a], positions[b])
                for a, b in edge_pairs
            ]
        )
        nodes = VGroup(*[self.make_node(k, v) for k, v in positions.items()])

        example_label = Text("Example:", font_size=24, color=GREY_B).next_to(
            nodes, UP, buff=0.3
        )
        self.play(Write(example_label), run_time=0.5)
        self.play(Create(edges), run_time=0.8)
        self.play(FadeIn(nodes), run_time=0.8)

        # Annotate vertex & edge
        v_arrow = Arrow(
            positions["4"] + LEFT * 1.2 + DOWN * 0.5,
            positions["4"] + LEFT * 0.45,
            color=YELLOW,
            stroke_width=2,
            buff=0.05,
        )
        v_label = Text("Vertex", font_size=20, color=YELLOW).next_to(
            v_arrow, LEFT, buff=0.1
        )
        e_mid = (positions["1"] + positions["3"]) / 2
        e_arrow = Arrow(
            e_mid + RIGHT * 1.2 + UP * 0.3,
            e_mid + RIGHT * 0.15,
            color=GREEN,
            stroke_width=2,
            buff=0.05,
        )
        e_label = Text("Edge", font_size=20, color=GREEN).next_to(
            e_arrow, RIGHT, buff=0.1
        )
        self.play(
            Create(v_arrow),
            Write(v_label),
            Create(e_arrow),
            Write(e_label),
            run_time=0.8,
        )
        self.wait(2.5)
        self.clear_screen(LEFT)

    # ============================================================
    # 3. WHAT IS BFS
    # ============================================================
    def play_what_is_bfs(self):
        hg = self.section_heading("What is BFS?")

        points = [
            ("BFS = Breadth First Search", WHITE),
            ("Explores a graph LEVEL by LEVEL", BLUE_B),
            ("Uses a QUEUE data structure (FIFO)", GREEN_B),
            ("Starts from a SOURCE node", ORANGE),
            ("Visits ALL neighbors before going deeper", TEAL_B),
            ("Guarantees SHORTEST PATH in unweighted graphs", YELLOW),
        ]
        mobs = []
        for txt, col in points:
            m = Text(f"→  {txt}", font_size=26, color=col)
            mobs.append(m)
        group = VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        group.next_to(hg, DOWN, buff=0.6).shift(LEFT * 1)

        for mob in mobs:
            self.play(FadeIn(mob, shift=RIGHT * 1.5), run_time=0.6)
            self.wait(0.3)

        analogy = VGroup(
            Text("Think of it like:", font_size=28, color=WHITE),
            Text(
                "Dropping a stone in water — ripples spread",
                font_size=24,
                color=BLUE_C,
            ),
            Text("outward level by level, ring by ring!", font_size=24, color=BLUE_C),
        ).arrange(DOWN, buff=0.15)
        analogy.to_edge(DOWN, buff=0.6)
        a_box = SurroundingRectangle(analogy, color=BLUE, buff=0.25, corner_radius=0.12)
        self.play(FadeIn(analogy, shift=UP * 0.5), Create(a_box), run_time=1)
        self.wait(2.5)
        self.clear_screen(RIGHT)

    # ============================================================
    # 4. ALGORITHM STEPS + PSEUDOCODE
    # ============================================================
    def play_algorithm_steps(self):
        hg = self.section_heading("BFS Algorithm Steps")

        steps = [
            ("Step 1:", "Pick a starting node, mark it VISITED", BLUE),
            ("Step 2:", "Add it to the QUEUE", GREEN),
            ("Step 3:", "While queue is NOT empty:", ORANGE),
            ("Step 4:", "    Dequeue node from front", TEAL),
            ("Step 5:", "    Visit all UNVISITED neighbors", PURPLE_B),
            ("Step 6:", "    Mark them visited & enqueue", RED_B),
            ("Step 7:", "    Repeat until queue is empty", YELLOW),
        ]
        step_mobs = []
        for num, desc, col in steps:
            line = VGroup(
                Text(num, font_size=26, color=col, weight=BOLD),
                Text(desc, font_size=24, color=WHITE),
            ).arrange(RIGHT, buff=0.25)
            step_mobs.append(line)

        sg = VGroup(*step_mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        sg.next_to(hg, DOWN, buff=0.5).shift(LEFT * 1.5)

        for i, sm in enumerate(step_mobs):
            d = LEFT if i % 2 == 0 else RIGHT
            sm.shift(d * 12)
            self.play(sm.animate.shift(-d * 12), run_time=0.55, rate_func=smooth)
            self.wait(0.15)

        self.wait(1.5)

        # Transition to pseudocode
        self.play(*[FadeOut(m) for m in step_mobs], run_time=0.6)

        pseudo_title = (
            Text("Pseudocode:", font_size=32, color=GREEN, weight=BOLD)
            .next_to(hg, DOWN, buff=0.4)
            .to_edge(LEFT, buff=1)
        )
        code_lines = [
            "BFS(graph, start):",
            "    visited = {start}",
            "    queue = [start]",
            "",
            "    while queue is not empty:",
            "        node = queue.dequeue()",
            "        process(node)",
            "",
            "        for neighbor in graph[node]:",
            "            if neighbor not in visited:",
            "                visited.add(neighbor)",
            "                queue.enqueue(neighbor)",
        ]
        code = Code(
            code="\n".join(code_lines),
            tab_width=4,
            language="Python",
            font_size=20,
            background="window",
            insert_line_no=True,
            style="monokai",
        )
        code.next_to(pseudo_title, DOWN, buff=0.25).shift(RIGHT * 0.5)
        self.play(Write(pseudo_title), run_time=0.5)
        self.play(FadeIn(code, shift=UP * 0.5), run_time=1.2)
        self.wait(3)
        self.clear_screen(DOWN)

    # ============================================================
    # 5. QUEUE DATA STRUCTURE EXPLANATION
    # ============================================================
    def play_queue_explanation(self):
        hg = self.section_heading("The Queue — Heart of BFS")

        fifo = Text("FIFO = First In, First Out", font_size=34, color=BLUE_B).next_to(
            hg, DOWN, buff=0.5
        )
        self.play(Write(fifo), run_time=0.8)

        # Visual queue
        num_slots = 6
        boxes = VGroup(
            *[
                Rectangle(width=1.1, height=0.8, color=WHITE, fill_opacity=0.05, stroke_width=2)
                for _ in range(num_slots)
            ]
        )
        boxes.arrange(RIGHT, buff=0).shift(UP * 0.2)

        front_arr = Arrow(
            boxes[0].get_bottom() + DOWN * 0.4,
            boxes[0].get_bottom(),
            color=GREEN,
            buff=0.05,
            stroke_width=2,
        )
        front_lbl = Text("FRONT\n(Dequeue)", font_size=18, color=GREEN).next_to(
            front_arr, DOWN, buff=0.05
        )
        back_arr = Arrow(
            boxes[-1].get_bottom() + DOWN * 0.4,
            boxes[-1].get_bottom(),
            color=RED,
            buff=0.05,
            stroke_width=2,
        )
        back_lbl = Text("BACK\n(Enqueue)", font_size=18, color=RED).next_to(
            back_arr, DOWN, buff=0.05
        )

        self.play(Create(boxes), run_time=0.8)
        self.play(
            Create(front_arr), Write(front_lbl), Create(back_arr), Write(back_lbl), run_time=0.7
        )

        # Enqueue
        enq_label = Text("Enqueue A, B, C, D:", font_size=24, color=GREEN).shift(DOWN * 2.2)
        self.play(Write(enq_label), run_time=0.5)

        items_text = ["A", "B", "C", "D"]
        item_mobs = []
        for i, it in enumerate(items_text):
            t = Text(it, font_size=26, color=YELLOW, weight=BOLD)
            t.move_to(boxes[i].get_center() + RIGHT * 8)
            self.play(
                t.animate.move_to(boxes[i].get_center()),
                boxes[i].animate.set_fill(BLUE, opacity=0.25),
                run_time=0.5,
                rate_func=smooth,
            )
            item_mobs.append(t)
            self.wait(0.15)

        self.wait(0.8)

        # Dequeue
        deq_label = Text("Dequeue → A leaves first:", font_size=24, color=RED).shift(
            DOWN * 2.8
        )
        self.play(Write(deq_label), run_time=0.5)

        for i in range(2):
            self.play(
                item_mobs[i].animate.shift(LEFT * 5).set_opacity(0),
                boxes[i].animate.set_fill(BLACK, opacity=0),
                run_time=0.5,
            )
            self.wait(0.2)

        result = Text(
            "First In → First Out  (FIFO)", font_size=28, color=TEAL
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(result), run_time=0.6)
        self.wait(2)
        self.clear_screen(UP)

    # ============================================================
    # 6. FULL BFS ON A TREE-LIKE GRAPH (main visualization)
    # ============================================================
    def play_bfs_traversal_tree(self):
        hg = self.section_heading("BFS Traversal — Tree Graph")

        # Graph layout
        positions = {
            "A": np.array([0.0, 1.8, 0]),
            "B": np.array([-2.5, 0.2, 0]),
            "C": np.array([2.5, 0.2, 0]),
            "D": np.array([-3.8, -1.6, 0]),
            "E": np.array([-1.3, -1.6, 0]),
            "F": np.array([1.3, -1.6, 0]),
            "G": np.array([3.8, -1.6, 0]),
        }
        adj = {
            "A": ["B", "C"],
            "B": ["D", "E"],
            "C": ["F", "G"],
            "D": [],
            "E": [],
            "F": [],
            "G": [],
        }
        edge_pairs = [
            ("A", "B"), ("A", "C"),
            ("B", "D"), ("B", "E"),
            ("C", "F"), ("C", "G"),
        ]

        radius = 0.4
        node_groups = {}
        for k, p in positions.items():
            node_groups[k] = self.make_node(k, p, radius=radius)

        edge_lines = {}
        for a, b in edge_pairs:
            edge_lines[(a, b)] = self.make_edge(positions[a], positions[b], radius=radius)

        all_edges = VGroup(*edge_lines.values())
        all_nodes = VGroup(*node_groups.values())

        self.play(Create(all_edges), run_time=0.8)
        self.play(FadeIn(all_nodes), run_time=0.8)
        self.wait(0.5)

        # Queue display
        q_label = (
            Text("Queue: ", font_size=24, color=GREEN, weight=BOLD)
            .to_edge(DOWN, buff=1.6)
            .to_edge(LEFT, buff=0.4)
        )
        v_label = (
            Text("Visited: ", font_size=24, color=ORANGE, weight=BOLD)
            .to_edge(DOWN, buff=0.8)
            .to_edge(LEFT, buff=0.4)
        )
        level_text = Text("Level: 0", font_size=24, color=TEAL).to_edge(
            RIGHT, buff=0.6
        ).to_edge(UP, buff=1.0)
        self.play(Write(q_label), Write(v_label), Write(level_text), run_time=0.6)

        level_colors = [RED, GREEN_B, BLUE_B, PURPLE_B, ORANGE, TEAL]

        # ── BFS ──
        start = "A"
        visited = {start}
        bfs_queue = deque([(start, 0)])

        queue_mob_list = []  # list of VGroups (box+text)
        visited_mob_list = []

        def make_q_box(label, color=WHITE):
            r = RoundedRectangle(
                width=0.65, height=0.6, corner_radius=0.08,
                color=color, fill_opacity=0.2, stroke_width=2,
            )
            t = Text(label, font_size=22, color=color, weight=BOLD).move_to(r)
            return VGroup(r, t)

        def arrange_queue():
            if not queue_mob_list:
                return
            temp = VGroup(*queue_mob_list).arrange(RIGHT, buff=0.1)
            temp.next_to(q_label, RIGHT, buff=0.2)

        # Enqueue start
        first_box = make_q_box("A", YELLOW)
        queue_mob_list.append(first_box)
        arrange_queue()
        self.play(FadeIn(first_box, shift=UP * 0.3), run_time=0.4)

        # Mark start
        self.play(
            node_groups["A"][0].animate.set_fill(YELLOW, opacity=0.5).set_stroke(YELLOW, width=4),
            run_time=0.4,
        )

        current_level = -1

        while bfs_queue:
            current_node, node_level = bfs_queue.popleft()
            lc = level_colors[node_level % len(level_colors)]

            # Update level
            if node_level != current_level:
                current_level = node_level
                new_lt = Text(
                    f"Level: {current_level}", font_size=24, color=lc
                ).move_to(level_text)
                self.play(Transform(level_text, new_lt), run_time=0.35)

            # Dequeue animation
            if queue_mob_list:
                removed = queue_mob_list.pop(0)
                self.play(
                    removed.animate.shift(UP * 0.4).set_opacity(0), run_time=0.35
                )
                self.remove(removed)
                if queue_mob_list:
                    arrange_queue()
                    anims = []
                    temp = VGroup(*queue_mob_list).arrange(RIGHT, buff=0.1)
                    temp.next_to(q_label, RIGHT, buff=0.2)
                    for idx2, bx in enumerate(queue_mob_list):
                        anims.append(bx.animate.move_to(temp[idx2]))
                    self.play(*anims, run_time=0.25)

            # Pulse on current node
            pulse = Circle(radius=0.55, color=lc, stroke_width=4).move_to(
                node_groups[current_node]
            )
            self.play(
                Create(pulse),
                node_groups[current_node][0]
                .animate.set_fill(lc, opacity=0.55)
                .set_stroke(lc, width=4),
                run_time=0.5,
            )

            # Add to visited display
            if visited_mob_list:
                arr = Text("→", font_size=18, color=GREY)
                visited_mob_list.append(arr)
            v_t = Text(current_node, font_size=24, color=lc, weight=BOLD)
            visited_mob_list.append(v_t)
            vg = VGroup(*visited_mob_list).arrange(RIGHT, buff=0.08)
            vg.next_to(v_label, RIGHT, buff=0.2)
            self.play(FadeIn(v_t, shift=UP * 0.15), run_time=0.25)

            # Explore neighbors
            for neighbor in adj[current_node]:
                if neighbor not in visited:
                    # Highlight edge
                    ek = (
                        (current_node, neighbor)
                        if (current_node, neighbor) in edge_lines
                        else (neighbor, current_node)
                    )
                    if ek in edge_lines:
                        self.play(
                            edge_lines[ek].animate.set_color(lc).set_stroke(width=4),
                            run_time=0.3,
                        )

                    # Flash on discovered node
                    self.play(
                        Flash(
                            node_groups[neighbor],
                            color=lc,
                            line_length=0.25,
                            num_lines=8,
                            run_time=0.4,
                        )
                    )

                    visited.add(neighbor)
                    bfs_queue.append((neighbor, node_level + 1))

                    # Enqueue box
                    nb = make_q_box(neighbor, lc)
                    queue_mob_list.append(nb)
                    arrange_queue()
                    nb.move_to(
                        VGroup(*queue_mob_list)
                        .arrange(RIGHT, buff=0.1)
                        .next_to(q_label, RIGHT, buff=0.2)[-1]
                    )
                    self.play(FadeIn(nb, shift=DOWN * 0.25), run_time=0.25)

                    # Lightly stroke discovered node
                    self.play(
                        node_groups[neighbor][0].animate.set_stroke(lc, width=3),
                        run_time=0.15,
                    )

            self.play(FadeOut(pulse), run_time=0.2)
            self.wait(0.2)

        done = Text(
            "BFS Complete!  Order: A → B → C → D → E → F → G",
            font_size=26,
            color=GREEN,
            weight=BOLD,
        ).to_edge(DOWN, buff=0.15)
        self.play(Write(done), run_time=0.8)
        self.wait(2.5)
        self.clear_screen(LEFT)

    # ============================================================
    # 7. BFS ON A CYCLIC GRAPH
    # ============================================================
    def play_bfs_traversal_cyclic(self):
        hg = self.section_heading("BFS on a Cyclic Graph")

        positions = {
            "0": np.array([0.0, 2.0, 0]),
            "1": np.array([-2.0, 0.6, 0]),
            "2": np.array([2.0, 0.6, 0]),
            "3": np.array([-2.5, -1.2, 0]),
            "4": np.array([2.5, -1.2, 0]),
            "5": np.array([0.0, -2.5, 0]),
        }
        adj = {
            "0": ["1", "2"],
            "1": ["0", "2", "3"],
            "2": ["0", "1", "4"],
            "3": ["1", "4", "5"],
            "4": ["2", "3", "5"],
            "5": ["3", "4"],
        }
        edge_pairs = [
            ("0", "1"), ("0", "2"), ("1", "2"),
            ("1", "3"), ("2", "4"), ("3", "4"),
            ("3", "5"), ("4", "5"),
        ]

        radius = 0.4
        node_groups = {}
        for k, p in positions.items():
            node_groups[k] = self.make_node(k, p, radius=radius)

        edge_lines = {}
        for a, b in edge_pairs:
            edge_lines[(a, b)] = self.make_edge(positions[a], positions[b], radius=radius)

        self.play(Create(VGroup(*edge_lines.values())), run_time=0.8)
        self.play(FadeIn(VGroup(*node_groups.values())), run_time=0.8)

        note = Text(
            "This graph has CYCLES — BFS handles them with visited set",
            font_size=22,
            color=ORANGE,
        ).to_edge(DOWN, buff=2.2)
        self.play(Write(note), run_time=0.6)
        self.wait(1)
        self.play(FadeOut(note), run_time=0.4)

        # Visited display
        v_label = (
            Text("Visited: ", font_size=24, color=ORANGE, weight=BOLD)
            .to_edge(DOWN, buff=0.5)
            .to_edge(LEFT, buff=0.5)
        )
        self.play(Write(v_label), run_time=0.3)

        level_colors = [RED, YELLOW, GREEN_B, TEAL, PURPLE_B, ORANGE]
        visited = {"0"}
        bfs_queue = deque([("0", 0)])
        visited_texts = []
        visit_order = []

        while bfs_queue:
            cur, lvl = bfs_queue.popleft()
            visit_order.append(cur)
            lc = level_colors[lvl % len(level_colors)]

            ring = Circle(radius=0.55, color=lc, stroke_width=5).move_to(
                node_groups[cur]
            )
            self.play(
                Create(ring),
                node_groups[cur][0]
                .animate.set_fill(lc, opacity=0.55)
                .set_stroke(lc, width=4),
                run_time=0.45,
            )

            if visited_texts:
                visited_texts.append(Text("→", font_size=18, color=GREY))
            vt = Text(cur, font_size=24, color=lc, weight=BOLD)
            visited_texts.append(vt)
            vg = VGroup(*visited_texts).arrange(RIGHT, buff=0.08)
            vg.next_to(v_label, RIGHT, buff=0.2)
            self.play(FadeIn(vt, shift=UP * 0.15), run_time=0.2)

            for nb in adj[cur]:
                if nb not in visited:
                    ek = (
                        (cur, nb) if (cur, nb) in edge_lines else (nb, cur)
                    )
                    if ek in edge_lines:
                        self.play(
                            edge_lines[ek].animate.set_color(lc).set_stroke(width=4),
                            run_time=0.25,
                        )
                    visited.add(nb)
                    bfs_queue.append((nb, lvl + 1))

            self.play(FadeOut(ring), run_time=0.2)

        order_str = " → ".join(visit_order)
        done = Text(
            f"BFS Order: {order_str}", font_size=28, color=GREEN, weight=BOLD
        ).to_edge(DOWN, buff=0.1)
        self.play(Write(done), run_time=0.7)
        self.wait(2.5)
        self.clear_screen(RIGHT)

    # ============================================================
    # 8. TIME & SPACE COMPLEXITY
    # ============================================================
    def play_complexity(self):
        hg = self.section_heading("Time & Space Complexity")

        # Time
        t_head = Text("Time Complexity", font_size=34, color=GREEN, weight=BOLD).shift(
            UP * 1.3 + LEFT * 3
        )
        t_form = MathTex(r"O(V + E)", font_size=56, color=WHITE).next_to(
            t_head, DOWN, buff=0.25
        )
        t_exp = VGroup(
            Text("V = vertices visited once", font_size=22, color=BLUE_B),
            Text("E = edges examined once", font_size=22, color=BLUE_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        t_exp.next_to(t_form, DOWN, buff=0.25)

        # Space
        s_head = Text("Space Complexity", font_size=34, color=RED, weight=BOLD).shift(
            UP * 1.3 + RIGHT * 3
        )
        s_form = MathTex(r"O(V)", font_size=56, color=WHITE).next_to(
            s_head, DOWN, buff=0.25
        )
        s_exp = VGroup(
            Text("Queue holds up to V nodes", font_size=22, color=ORANGE),
            Text("Visited set stores V nodes", font_size=22, color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        s_exp.next_to(s_form, DOWN, buff=0.25)

        divider = Line(UP * 1.8, DOWN * 1.8, color=GREY, stroke_width=1)

        self.play(Write(t_head), Write(s_head), run_time=0.6)
        self.play(Write(t_form), Write(s_form), run_time=0.8)
        self.play(FadeIn(t_exp), FadeIn(s_exp), Create(divider), run_time=0.8)

        note = Text(
            "BFS uses more memory than DFS but guarantees shortest path",
            font_size=24,
            color=TEAL,
        ).to_edge(DOWN, buff=0.5)
        nbox = SurroundingRectangle(note, color=TEAL, buff=0.15, corner_radius=0.1)
        self.play(Write(note), Create(nbox), run_time=0.8)
        self.wait(3)
        self.clear_screen(DOWN)

    # ============================================================
    # 9. BFS vs DFS
    # ============================================================
    def play_bfs_vs_dfs(self):
        hg = self.section_heading("BFS  vs  DFS")

        bfs_h = Text("BFS", font_size=36, color=BLUE, weight=BOLD).shift(
            LEFT * 3 + UP * 1.3
        )
        dfs_h = Text("DFS", font_size=36, color=RED, weight=BOLD).shift(
            RIGHT * 3 + UP * 1.3
        )
        vs = Text("VS", font_size=28, color=YELLOW).shift(UP * 1.3)

        self.play(Write(bfs_h), Write(dfs_h), Write(vs), run_time=0.6)

        rows = [
            ("Queue (FIFO)", "Stack (LIFO)"),
            ("Level by level", "Goes deep first"),
            ("Shortest path ✓", "No shortest guarantee"),
            ("More memory", "Less memory"),
            ("O(V+E) time", "O(V+E) time"),
            ("Wide exploration", "Deep exploration"),
        ]

        y = 0.5
        for bfs_t, dfs_t in rows:
            bl = Text(bfs_t, font_size=22, color=BLUE_B).shift(LEFT * 3 + UP * y)
            dl = Text(dfs_t, font_size=22, color=RED_B).shift(RIGHT * 3 + UP * y)
            dot = Dot(color=GREY).shift(UP * y)
            self.play(FadeIn(bl, shift=LEFT * 0.5), FadeIn(dl, shift=RIGHT * 0.5), FadeIn(dot), run_time=0.45)
            y -= 0.55

        divider = Line(UP * 1.8, DOWN * 2.5, color=YELLOW, stroke_width=2)
        self.play(Create(divider), run_time=0.5)
        self.wait(3)
        self.clear_screen(LEFT)

    # ============================================================
    # 10. PYTHON CODE
    # ============================================================
    def play_python_code(self):
        hg = self.section_heading("Python Implementation")

        code_str = """\
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result

# Example
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [], 'E': [],
    'F': [], 'G': []
}
print(bfs(graph, 'A'))
# ['A','B','C','D','E','F','G']"""

        code = Code(
            code=code_str,
            tab_width=4,
            language="Python",
            font_size=18,
            background="window",
            insert_line_no=True,
            style="monokai",
        )
        code.next_to(hg, DOWN, buff=0.25).scale(0.82)
        code.shift(DOWN * 6)
        self.play(code.animate.shift(UP * 6), run_time=1.8, rate_func=smooth)
        self.wait(4)
        self.clear_screen(RIGHT)

    # ============================================================
    # 11. APPLICATIONS
    # ============================================================
    def play_applications(self):
        hg = self.section_heading("BFS Applications")

        apps = [
            ("Shortest Path in unweighted graphs", BLUE_B),
            ("Web Crawling (page by page)", GREEN_B),
            ("Network Broadcasting", ORANGE),
            ("Solving Puzzles (Rubik's, 8-puzzle)", PURPLE_B),
            ("Social Networks — degrees of separation", TEAL),
            ("Level-Order Tree Traversal", RED_B),
            ("Finding Connected Components", YELLOW),
            ("GPS Navigation Systems", MAROON_B),
        ]

        mobs = []
        for txt, col in apps:
            m = Text(f"▸  {txt}", font_size=25, color=col)
            mobs.append(m)

        g = VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        g.next_to(hg, DOWN, buff=0.5).shift(LEFT * 1)

        for mob in mobs:
            mob.shift(RIGHT * 14)
            self.play(mob.animate.shift(LEFT * 14), run_time=0.4, rate_func=smooth)
            self.wait(0.1)

        self.wait(3)
        self.clear_screen(LEFT)

    # ============================================================
    # 12. SUMMARY & OUTRO
    # ============================================================
    def play_summary(self):
        hg = self.section_heading("Summary")

        points = [
            ("BFS traverses graphs LEVEL by LEVEL", GREEN),
            ("Uses a QUEUE (FIFO) data structure", BLUE),
            ("Time: O(V+E)   Space: O(V)", ORANGE),
            ("Finds SHORTEST PATH in unweighted graphs", TEAL),
            ("Marks nodes VISITED to handle cycles", PURPLE_B),
            ("Used in GPS, web crawling, networking & more", RED_B),
        ]
        mobs = []
        for txt, col in points:
            m = Text(f"✓  {txt}", font_size=26, color=col)
            mobs.append(m)

        g = VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        g.next_to(hg, DOWN, buff=0.5).shift(LEFT * 1)

        for m in mobs:
            self.play(FadeIn(m, shift=UP * 0.4), run_time=0.5)
            self.wait(0.2)

        self.wait(2)
        self.play(*[FadeOut(m) for m in [*mobs, *hg]], run_time=0.8)

        thanks = Text(
            "Thank You for Watching!", font_size=56, color=YELLOW, weight=BOLD
        )
        sub = Text(
            "Like & Subscribe for more Algorithm Visualizations",
            font_size=28,
            color=BLUE_B,
        ).next_to(thanks, DOWN, buff=0.5)

        self.play(FadeIn(thanks, scale=0.5), run_time=1.2)
        self.play(Write(sub), run_time=0.8)
        self.wait(3)

        self.play(
            thanks.animate.scale(1.5).set_opacity(0),
            sub.animate.shift(DOWN * 3).set_opacity(0),
            run_time=1.5,
        )
        self.wait(0.5)