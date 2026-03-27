from manim import *
import numpy as np

# ============================================================
# SCENE 1: INTRO / TITLE
# ============================================================
class Scene01_Intro(Scene):
    def construct(self):
        # Background color
        self.camera.background_color = "#1a1a2e"

        # Title with gradient effect
        title = Text(
            "Breadth First Search",
            font_size=72,
            color=WHITE,
            weight=BOLD
        )
        bfs_short = Text(
            "(BFS)",
            font_size=60,
            color=YELLOW
        ).next_to(title, DOWN, buff=0.3)

        tagline = Text(
            "A Complete Visual Guide",
            font_size=36,
            color=BLUE_B
        ).next_to(bfs_short, DOWN, buff=0.5)

        # Decorative line
        line_left = Line(LEFT * 4, ORIGIN, color=YELLOW)
        line_right = Line(ORIGIN, RIGHT * 4, color=YELLOW)
        lines = VGroup(line_left, line_right).next_to(tagline, DOWN, buff=0.4)

        author = Text(
            "Graph Traversal Algorithm",
            font_size=28,
            color=GREY_B
        ).next_to(lines, DOWN, buff=0.4)

        # Animations - sliding in
        self.play(
            title.animate.shift(UP * 0),
            FadeIn(title, shift=DOWN * 2),
            run_time=1.5
        )
        self.play(
            FadeIn(bfs_short, shift=UP),
            run_time=1
        )
        self.play(
            Write(tagline),
            run_time=1
        )
        self.play(
            Create(line_left),
            Create(line_right),
            run_time=0.8
        )
        self.play(FadeIn(author, shift=UP * 0.5))
        self.wait(2)

        # Slide everything out to the left
        everything = VGroup(title, bfs_short, tagline, lines, author)
        self.play(
            everything.animate.shift(LEFT * 15),
            run_time=1.5,
            rate_func=smooth
        )
        self.wait(0.5)


# ============================================================
# SCENE 2: WHAT IS A GRAPH?
# ============================================================
class Scene02_WhatIsGraph(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"

        # Slide in heading from right
        heading = Text(
            "What is a Graph?",
            font_size=52,
            color=YELLOW,
            weight=BOLD
        ).to_edge(UP, buff=0.5)
        heading.shift(RIGHT * 15)

        self.play(
            heading.animate.shift(LEFT * 15),
            run_time=1.2,
            rate_func=smooth
        )

        # Definition box
        definition = VGroup(
            Text("A Graph consists of:", font_size=32, color=WHITE),
            Text("• Vertices (Nodes) - The entities", font_size=28, color=BLUE_B),
            Text("• Edges (Links) - Connections between entities", font_size=28, color=GREEN_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        definition.shift(LEFT * 2.5 + UP * 0.5)

        box = SurroundingRectangle(definition, color=BLUE, buff=0.3, corner_radius=0.1)

        self.play(FadeIn(definition, shift=UP), Create(box), run_time=1.5)
        self.wait(1.5)

        # Draw a simple example graph on the right
        example_label = Text(
            "Example Graph:",
            font_size=28,
            color=GREY_B
        ).shift(RIGHT * 3 + UP * 1.5)

        # Node positions
        pos = {
            "1": RIGHT * 3 + UP * 0.5,
            "2": RIGHT * 1.5 + DOWN * 0.8,
            "3": RIGHT * 4.5 + DOWN * 0.8,
            "4": RIGHT * 3 + DOWN * 2,
        }

        node_circles = {}
        node_labels = {}
        for key, p in pos.items():
            c = Circle(radius=0.35, color=BLUE, fill_opacity=0.3).move_to(p)
            l = Text(key, font_size=26, color=WHITE).move_to(p)
            node_circles[key] = c
            node_labels[key] = l

        edge_pairs = [("1", "2"), ("1", "3"), ("2", "4"), ("3", "4")]
        edge_lines = []
        for a, b in edge_pairs:
            line = Line(
                pos[a], pos[b],
                color=GREY_B,
                stroke_width=2.5
            )
            edge_lines.append(line)

        self.play(Write(example_label))

        # Draw edges first
        self.play(*[Create(e) for e in edge_lines], run_time=1)

        # Draw nodes on top
        for key in node_circles:
            self.play(
                Create(node_circles[key]),
                Write(node_labels[key]),
                run_time=0.4
            )

        # Label vertex and edge
        vertex_arrow = Arrow(
            RIGHT * 0.5 + DOWN * 2, pos["4"] + LEFT * 0.4,
            color=YELLOW,
            buff=0.1,
            stroke_width=2
        )
        vertex_text = Text("Vertex", font_size=22, color=YELLOW).next_to(vertex_arrow, LEFT, buff=0.1)

        edge_mid = (np.array(pos["1"]) + np.array(pos["3"])) / 2
        edge_arrow = Arrow(
            RIGHT * 5.5 + UP * 0.2, edge_mid + RIGHT * 0.2,
            color=GREEN,
            buff=0.1,
            stroke_width=2
        )
        edge_text = Text("Edge", font_size=22, color=GREEN).next_to(edge_arrow, RIGHT, buff=0.1)

        self.play(
            Create(vertex_arrow), Write(vertex_text),
            Create(edge_arrow), Write(edge_text),
            run_time=1
        )

        self.wait(3)

        # Slide everything out
        all_mobs = VGroup(*self.mobjects)
        self.play(all_mobs.animate.shift(LEFT * 16), run_time=1.5)


# ============================================================
# SCENE 3: WHAT IS BFS?
# ============================================================
class Scene03_WhatIsBFS(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"

        # Heading slides in from top
        heading = Text(
            "What is BFS?",
            font_size=52,
            color=YELLOW,
            weight=BOLD
        ).to_edge(UP, buff=0.5)
        heading.shift(UP * 5)

        self.play(
            heading.animate.shift(DOWN * 5),
            run_time=1,
            rate_func=smooth
        )

        # Points appear one by one with fade
        points = [
            "BFS = Breadth First Search",
            "It explores a graph LEVEL by LEVEL",
            "Uses a QUEUE data structure (FIFO)",
            "Starts from a SOURCE node",
            "Visits ALL neighbors before going deeper",
            "Guarantees SHORTEST PATH in unweighted graphs",
        ]

        point_mobs = []
        for i, p in enumerate(points):
            color = [WHITE, BLUE_B, GREEN_B, ORANGE, TEAL_B, YELLOW][i]
            bullet = Text(f"→  {p}", font_size=28, color=color)
            point_mobs.append(bullet)

        points_group = VGroup(*point_mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        points_group.next_to(heading, DOWN, buff=0.8)
        points_group.shift(LEFT * 1)

        for pm in point_mobs:
            self.play(FadeIn(pm, shift=RIGHT * 2), run_time=0.8)
            self.wait(0.5)

        self.wait(2)

        # Analogy box
        analogy_box = VGroup(
            Text("🌊 Think of it like:", font_size=30, color=WHITE),
            Text(
                "Dropping a stone in water - ripples spread outward",
                font_size=26,
                color=BLUE_C
            ),
            Text(
                "level by level, ring by ring!",
                font_size=26,
                color=BLUE_C
            ),
        ).arrange(DOWN, buff=0.2)
        analogy_box.to_edge(DOWN, buff=0.8)
        box = SurroundingRectangle(analogy_box, color=BLUE, buff=0.3, corner_radius=0.15)

        self.play(FadeIn(analogy_box, shift=UP), Create(box), run_time=1.5)
        self.wait(3)

        all_mobs = VGroup(*self.mobjects)
        self.play(all_mobs.animate.shift(RIGHT * 16), run_time=1.5)


# ============================================================
# SCENE 4: BFS ALGORITHM STEPS
# ============================================================
class Scene04_AlgorithmSteps(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"

        heading = Text(
            "BFS Algorithm Steps",
            font_size=48,
            color=YELLOW,
            weight=BOLD
        ).to_edge(UP, buff=0.4)

        self.play(FadeIn(heading, shift=DOWN))

        steps = [
            ("Step 1:", "Pick a starting node, mark it VISITED", BLUE),
            ("Step 2:", "Add it to the QUEUE", GREEN),
            ("Step 3:", "While queue is NOT empty:", ORANGE),
            ("Step 4:", "   Dequeue a node from the front", TEAL),
            ("Step 5:", "   Visit all its UNVISITED neighbors", PURPLE),
            ("Step 6:", "   Mark them VISITED & add to queue", RED_B),
            ("Step 7:", "   Repeat until queue is empty", YELLOW),
        ]

        step_mobs = []
        for num, desc, color in steps:
            line = VGroup(
                Text(num, font_size=28, color=color, weight=BOLD),
                Text(desc, font_size=26, color=WHITE),
            ).arrange(RIGHT, buff=0.3)
            step_mobs.append(line)

        steps_group = VGroup(*step_mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        steps_group.next_to(heading, DOWN, buff=0.6)
        steps_group.shift(LEFT * 1.5)

        for i, sm in enumerate(step_mobs):
            # Each step slides in from alternating sides
            direction = LEFT if i % 2 == 0 else RIGHT
            sm.shift(direction * 10)
            self.play(
                sm.animate.shift(-direction * 10),
                run_time=0.7,
                rate_func=smooth
            )
            self.wait(0.3)

        self.wait(2)

        # Pseudocode
        self.play(*[FadeOut(m) for m in step_mobs], run_time=0.8)

        pseudo_heading = Text(
            "Pseudocode:",
            font_size=36,
            color=GREEN,
            weight=BOLD
        ).next_to(heading, DOWN, buff=0.5).to_edge(LEFT, buff=1)

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

        code_text = Code(
            code="\n".join(code_lines),
            tab_width=4,
            language="Python",
            font_size=22,
            background="window",
            insert_line_no=True,
            style="monokai",
        )
        code_text.next_to(pseudo_heading, DOWN, buff=0.3)
        code_text.shift(RIGHT * 0.5)

        self.play(Write(pseudo_heading))
        self.play(FadeIn(code_text, shift=UP), run_time=1.5)
        self.wait(4)

        all_mobs = VGroup(*self.mobjects)
        self.play(all_mobs.animate.shift(DOWN * 10), run_time=1.5)


# ============================================================
# SCENE 5: FULL BFS TRAVERSAL WITH QUEUE (MAIN SCENE)
# ============================================================
class Scene05_BFSTraversal(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"

        heading = Text(
            "BFS Traversal - Step by Step",
            font_size=44,
            color=YELLOW,
            weight=BOLD
        ).to_edge(UP, buff=0.3)
        self.play(FadeIn(heading, shift=DOWN))

        # ---- GRAPH SETUP ----
        # Positions for a tree-like graph
        positions = {
            "A": UP * 1.5 + LEFT * 0,
            "B": UP * 0 + LEFT * 2.5,
            "C": UP * 0 + RIGHT * 2.5,
            "D": DOWN * 1.5 + LEFT * 4,
            "E": DOWN * 1.5 + LEFT * 1.5,
            "F": DOWN * 1.5 + RIGHT * 1.5,
            "G": DOWN * 1.5 + RIGHT * 4,
        }

        # Shift graph slightly up-left
        graph_offset = LEFT * 0.5 + UP * 0.3

        node_color = BLUE
        node_radius = 0.4

        node_circles = {}
        node_labels = {}

        for key, pos in positions.items():
            actual_pos = pos + graph_offset
            c = Circle(
                radius=node_radius,
                color=node_color,
                fill_opacity=0.15,
                stroke_width=3
            ).move_to(actual_pos)
            l = Text(key, font_size=28, color=WHITE, weight=BOLD).move_to(actual_pos)
            node_circles[key] = c
            node_labels[key] = l

        edge_list = [
            ("A", "B"), ("A", "C"),
            ("B", "D"), ("B", "E"),
            ("C", "F"), ("C", "G"),
        ]

        edge_lines = {}
        for a, b in edge_list:
            pa = positions[a] + graph_offset
            pb = positions[b] + graph_offset
            # Shorten lines so they don't overlap circles
            direction = pb - pa
            unit = direction / np.linalg.norm(direction)
            start = pa + unit * node_radius
            end = pb - unit * node_radius
            line = Line(start, end, color=GREY_B, stroke_width=2.5)
            edge_lines[(a, b)] = line

        # Adjacency list for BFS
        adj = {
            "A": ["B", "C"],
            "B": ["A", "D", "E"],
            "C": ["A", "F", "G"],
            "D": ["B"],
            "E": ["B"],
            "F": ["C"],
            "G": ["C"],
        }

        # Draw graph with animation
        self.play(*[Create(e) for e in edge_lines.values()], run_time=1)
        self.play(
            *[Create(node_circles[n]) for n in node_circles],
            run_time=0.8
        )
        self.play(
            *[Write(node_labels[n]) for n in node_labels],
            run_time=0.8
        )
        self.wait(1)

        # ---- QUEUE VISUALIZATION SETUP ----
        queue_heading = Text(
            "Queue:",
            font_size=28,
            color=GREEN,
            weight=BOLD
        ).to_edge(DOWN, buff=1.8).to_edge(LEFT, buff=0.5)

        visited_heading = Text(
            "Visited Order:",
            font_size=28,
            color=ORANGE,
            weight=BOLD
        ).to_edge(DOWN, buff=0.5).to_edge(LEFT, buff=0.5)

        self.play(Write(queue_heading), Write(visited_heading))

        # Current queue display
        queue_mobs = VGroup()
        queue_mobs.next_to(queue_heading, RIGHT, buff=0.3)

        visited_mobs = VGroup()
        visited_mobs.next_to(visited_heading, RIGHT, buff=0.3)

        # ---- LEVEL LABEL ----
        level_label = Text(
            "Level: 0",
            font_size=28,
            color=TEAL
        ).to_edge(RIGHT, buff=0.8).to_edge(UP, buff=1.2)
        self.play(Write(level_label))

        # ---- BFS ALGORITHM ----
        # Color scheme for levels
        level_colors = [RED, GREEN, BLUE, PURPLE, ORANGE, YELLOW, TEAL]

        start_node = "A"
        visited = set()
        queue = [(start_node, 0)]  # (node, level)
        visited.add(start_node)

        # Track queue box mobjects
        queue_box_list = []
        visited_text_list = []

        def create_queue_box(label, color=WHITE):
            box = VGroup(
                RoundedRectangle(
                    width=0.7, height=0.7,
                    corner_radius=0.1,
                    color=color,
                    fill_opacity=0.2,
                    stroke_width=2
                ),
                Text(label, font_size=24, color=color)
            )
            box[1].move_to(box[0])
            return box

        def update_queue_display(q_list, heading_mob):
            """Rebuild queue display"""
            new_group = VGroup()
            for item in q_list:
                new_group.add(item)
            new_group.arrange(RIGHT, buff=0.15)
            new_group.next_to(heading_mob, RIGHT, buff=0.3)
            return new_group

        # Enqueue start node
        start_box = create_queue_box("A", YELLOW)
        queue_box_list.append(start_box)
        arranged = update_queue_display(queue_box_list, queue_heading)
        self.play(FadeIn(arranged, shift=UP * 0.3), run_time=0.5)

        # Highlight start node
        self.play(
            node_circles["A"].animate.set_fill(YELLOW, opacity=0.5),
            node_circles["A"].animate.set_stroke(YELLOW, width=4),
            run_time=0.5
        )

        current_level = 0
        step_counter = 0

        # Step info text
        step_info = Text("", font_size=24, color=WHITE)
        step_info.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)

        while queue:
            current_node, node_level = queue.pop(0)

            # Update level display
            if node_level != current_level:
                current_level = node_level
                new_level_label = Text(
                    f"Level: {current_level}",
                    font_size=28,
                    color=level_colors[current_level % len(level_colors)]
                ).move_to(level_label)
                self.play(
                    Transform(level_label, new_level_label),
                    run_time=0.5
                )

            step_counter += 1
            lc = level_colors[node_level % len(level_colors)]

            # --- DEQUEUE animation ---
            # Show which node we're processing
            new_step = Text(
                f"Process: {current_node}",
                font_size=26,
                color=lc,
                weight=BOLD
            ).move_to(step_info.get_center())
            if step_info.text == "":
                step_info = new_step
                self.play(Write(step_info), run_time=0.4)
            else:
                self.play(Transform(step_info, new_step), run_time=0.4)

            # Dequeue - remove first box
            if queue_box_list:
                removed = queue_box_list.pop(0)
                self.play(
                    removed.animate.shift(UP * 0.5).set_opacity(0),
                    run_time=0.4
                )
                self.remove(removed)
                # Rearrange remaining queue
                if queue_box_list:
                    arranged = update_queue_display(queue_box_list, queue_heading)
                    self.play(
                        *[box.animate.move_to(arranged[i])
                          for i, box in enumerate(queue_box_list)],
                        run_time=0.3
                    )

            # Highlight current node being processed
            pulse = Circle(
                radius=0.55,
                color=lc,
                stroke_width=4
            ).move_to(node_circles[current_node])

            self.play(
                Create(pulse),
                node_circles[current_node].animate.set_fill(lc, opacity=0.6),
                node_circles[current_node].animate.set_stroke(lc, width=4),
                run_time=0.6
            )

            # Add to visited display
            v_text = Text(
                current_node,
                font_size=26,
                color=lc,
                weight=BOLD
            )
            if visited_text_list:
                arrow_text = Text(" → ", font_size=22, color=GREY)
                visited_text_list.append(arrow_text)
            visited_text_list.append(v_text)

            visited_display = VGroup(*visited_text_list).arrange(RIGHT, buff=0.05)
            visited_display.next_to(visited_heading, RIGHT, buff=0.3)

            self.play(
                *[mob.animate.move_to(visited_display[i])
                  for i, mob in enumerate(visited_text_list)],
                run_time=0.3
            )
            if len(visited_text_list) <= 2:
                self.add(*visited_text_list)
                self.play(FadeIn(v_text, shift=DOWN * 0.2), run_time=0.3)

            # --- EXPLORE NEIGHBORS ---
            neighbors = adj[current_node]
            for neighbor in neighbors:
                if neighbor not in visited:
                    # Highlight the edge
                    edge_key = None
                    if (current_node, neighbor) in edge_lines:
                        edge_key = (current_node, neighbor)
                    elif (neighbor, current_node) in edge_lines:
                        edge_key = (neighbor, current_node)

                    if edge_key:
                        self.play(
                            edge_lines[edge_key].animate.set_color(lc).set_stroke(width=4),
                            run_time=0.4
                        )

                    # Discover neighbor
                    discover_flash = Flash(
                        node_circles[neighbor],
                        color=lc,
                        line_length=0.3,
                        num_lines=8,
                        run_time=0.5
                    )
                    self.play(discover_flash)

                    # Mark as visited
                    visited.add(neighbor)
                    queue.append((neighbor, node_level + 1))

                    # Add to queue display
                    new_box = create_queue_box(neighbor, lc)
                    queue_box_list.append(new_box)
                    arranged = update_queue_display(queue_box_list, queue_heading)
                    # Position new box and fade in
                    new_box.move_to(arranged[-1])
                    self.play(FadeIn(new_box, shift=DOWN * 0.3), run_time=0.3)

                    # Light highlight on discovered node
                    self.play(
                        node_circles[neighbor].animate.set_stroke(lc, width=3),
                        run_time=0.2
                    )

            # Remove pulse
            self.play(FadeOut(pulse), run_time=0.3)
            self.wait(0.3)

        # Final visited order highlight
        final_text = Text(
            "BFS Complete! All nodes visited.",
            font_size=32,
            color=GREEN,
            weight=BOLD
        ).to_edge(RIGHT, buff=0.5).shift(DOWN * 1.5)

        self.play(Write(final_text))
        self.wait(3)

        # Slide out
        all_mobs = VGroup(*self.mobjects)
        self.play(all_mobs.animate.shift(LEFT * 16), run_time=1.5)


# ============================================================
# SCENE 6: ANOTHER EXAMPLE - NON-TREE GRAPH
# ============================================================
class Scene06_CyclicGraphBFS(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"

        heading = Text(
            "BFS on a Cyclic Graph",
            font_size=44,
            color=YELLOW,
            weight=BOLD
        ).to_edge(UP, buff=0.4)
        self.play(FadeIn(heading, shift=DOWN))

        # Hexagonal graph with cycles
        positions = {
            "0": UP * 2,
            "1": UP * 0.7 + LEFT * 2,
            "2": UP * 0.7 + RIGHT * 2,
            "3": DOWN * 1 + LEFT * 2.5,
            "4": DOWN * 1 + RIGHT * 2.5,
            "5": DOWN * 2.5,
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

        node_radius = 0.4
        node_circles = {}
        node_labels = {}

        for key, pos in positions.items():
            c = Circle(
                radius=node_radius,
                color=BLUE,
                fill_opacity=0.15,
                stroke_width=3
            ).move_to(pos)
            l = Text(key, font_size=28, color=WHITE, weight=BOLD).move_to(pos)
            node_circles[key] = c
            node_labels[key] = l

        edge_lines = {}
        for a, b in edge_pairs:
            pa = np.array(positions[a])
            pb = np.array(positions[b])
            direction = pb - pa
            dist = np.linalg.norm(direction)
            unit = direction / dist
            start = pa + unit * node_radius
            end = pb - unit * node_radius
            line = Line(start, end, color=GREY_B, stroke_width=2.5)
            edge_lines[(a, b)] = line

        # Draw
        self.play(*[Create(e) for e in edge_lines.values()], run_time=1)
        self.play(
            *[Create(node_circles[n]) for n in node_circles],
            *[Write(node_labels[n]) for n in node_labels],
            run_time=1
        )

        note = Text(
            "Notice: This graph has CYCLES (1-2, 3-4-5)",
            font_size=24,
            color=ORANGE
        ).to_edge(DOWN, buff=2)
        self.play(Write(note))
        self.wait(1.5)
        self.play(FadeOut(note))

        # BFS from node 0
        info = Text(
            "Starting BFS from node 0",
            font_size=28,
            color=GREEN
        ).to_edge(DOWN, buff=2)
        self.play(Write(info))

        visited = set()
        queue = [("0", 0)]
        visited.add("0")
        visit_order = []

        level_colors = [RED, YELLOW, GREEN_B, TEAL, PURPLE, ORANGE]

        # Visited text at bottom
        visited_label = Text("Visited: ", font_size=26, color=ORANGE).to_edge(DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        self.play(Write(visited_label))
        visited_texts = []

        while queue:
            current, level = queue.pop(0)
            visit_order.append(current)
            lc = level_colors[level % len(level_colors)]

            # Animate visiting
            ring = Circle(radius=0.55, color=lc, stroke_width=5).move_to(node_circles[current])
            self.play(
                Create(ring),
                node_circles[current].animate.set_fill(lc, opacity=0.6).set_stroke(lc, width=4),
                run_time=0.5
            )

            # Add to visited display
            if visited_texts:
                arrow = Text("→", font_size=20, color=GREY)
                visited_texts.append(arrow)
            v_t = Text(current, font_size=26, color=lc, weight=BOLD)
            visited_texts.append(v_t)
            vg = VGroup(*visited_texts).arrange(RIGHT, buff=0.1)
            vg.next_to(visited_label, RIGHT, buff=0.2)
            self.play(FadeIn(v_t, shift=UP * 0.2), run_time=0.3)

            # Explore neighbors
            for neighbor in adj[current]:
                if neighbor not in visited:
                    # Highlight edge
                    ek = None
                    if (current, neighbor) in edge_lines:
                        ek = (current, neighbor)
                    elif (neighbor, current) in edge_lines:
                        ek = (neighbor, current)
                    if ek:
                        self.play(
                            edge_lines[ek].animate.set_color(lc).set_stroke(width=4),
                            run_time=0.3
                        )
                    visited.add(neighbor)
                    queue.append((neighbor, level + 1))
                else:
                    # Show that we skip already visited
                    ek = None
                    if (current, neighbor) in edge_lines:
                        ek = (current, neighbor)
                    elif (neighbor, current) in edge_lines:
                        ek = (neighbor, current)
                    if ek and edge_lines[ek].get_color() == Color(GREY_B):
                        # Flash red briefly for skipped
                        self.play(
                            edge_lines[ek].animate.set_color(RED_A).set_stroke(width=2),
                            run_time=0.2
                        )

            self.play(FadeOut(ring), run_time=0.2)

        # Update info
        new_info = Text(
            f"BFS Order: {' → '.join(visit_order)}",
            font_size=30,
            color=GREEN,
            weight=BOLD
        ).to_edge(DOWN, buff=1.5)
        self.play(Transform(info, new_info))
        self.wait(3)

        all_mobs = VGroup(*self.mobjects)
        self.play(all_mobs.animate.shift(RIGHT * 16), run_time=1.5)


# ============================================================
# SCENE 7: QUEUE DATA STRUCTURE EXPLANATION
# ============================================================
class Scene07_QueueExplanation(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"

        heading = Text(
            "The Queue - Heart of BFS",
            font_size=48,
            color=YELLOW,
            weight=BOLD
        ).to_edge(UP, buff=0.4)
        self.play(FadeIn(heading, shift=DOWN))

        # FIFO explanation
        fifo = Text(
            "FIFO = First In, First Out",
            font_size=36,
            color=BLUE_B
        ).next_to(heading, DOWN, buff=0.5)
        self.play(Write(fifo))

        # Visual queue
        box_width = 1.2
        box_height = 0.8
        num_slots = 6

        queue_boxes = VGroup()
        for i in range(num_slots):
            box = Rectangle(
                width=box_width,
                height=box_height,
                color=WHITE,
                fill_opacity=0.05,
                stroke_width=2
            )
            queue_boxes.add(box)

        queue_boxes.arrange(RIGHT, buff=0)
        queue_boxes.shift(UP * 0.3)

        # Labels
        front_arrow = Arrow(
            queue_boxes[0].get_bottom() + DOWN * 0.3,
            queue_boxes[0].get_bottom(),
            color=GREEN,
            buff=0.05
        )
        front_text = Text("FRONT\n(Dequeue)", font_size=20, color=GREEN).next_to(front_arrow, DOWN, buff=0.1)

        back_arrow = Arrow(
            queue_boxes[-1].get_bottom() + DOWN * 0.3,
            queue_boxes[-1].get_bottom(),
            color=RED,
            buff=0.05
        )
        back_text = Text("BACK\n(Enqueue)", font_size=20, color=RED).next_to(back_arrow, DOWN, buff=0.1)

        self.play(Create(queue_boxes), run_time=1)
        self.play(
            Create(front_arrow), Write(front_text),
            Create(back_arrow), Write(back_text),
            run_time=0.8
        )

        # Animate enqueue operations
        enqueue_label = Text("Enqueue operations:", font_size=26, color=GREEN).shift(DOWN * 2)
        self.play(Write(enqueue_label))

        items = ["A", "B", "C", "D"]
        item_mobs = []

        for i, item in enumerate(items):
            t = Text(item, font_size=28, color=YELLOW, weight=BOLD)
            t.move_to(queue_boxes[i])
            t.shift(RIGHT * 8)  # start off screen

            self.play(
                t.animate.move_to(queue_boxes[i]),
                queue_boxes[i].animate.set_fill(BLUE, opacity=0.3),
                run_time=0.6,
                rate_func=smooth
            )
            item_mobs.append(t)
            self.wait(0.2)

        self.wait(1)

        # Animate dequeue
        dequeue_label = Text("Dequeue operations:", font_size=26, color=RED).shift(DOWN * 2.8)
        self.play(Write(dequeue_label))

        for i in range(2):
            self.play(
                item_mobs[i].animate.shift(LEFT * 5).set_opacity(0),
                queue_boxes[i].animate.set_fill(BLACK, opacity=0),
                run_time=0.6
            )
            self.wait(0.3)

        result = Text(
            "A came first → A leaves first (FIFO!)",
            font_size=28,
            color=TEAL
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(result))
        self.wait(3)

        all_mobs = VGroup(*self.mobjects)
        self.play(all_mobs.animate.shift(UP * 10), run_time=1.5)


# ============================================================
# SCENE 8: BFS APPLICATIONS
# ============================================================
class Scene08_Applications(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"

        heading = Text(
            "BFS Applications",
            font_size=52,
            color=YELLOW,
            weight=BOLD
        ).to_edge(UP, buff=0.4)
        self.play(FadeIn(heading, shift=DOWN))

        apps = [
            ("🗺️", "Shortest Path in Unweighted Graphs", BLUE_B),
            ("🌐", "Web Crawling (page by page)", GREEN_B),
            ("📡", "Network Broadcasting", ORANGE),
            ("🧩", "Solving Puzzles (Rubik's, 8-puzzle)", PURPLE),
            ("👥", "Social Network - Degrees of Separation", TEAL),
            ("🗂️", "Level Order Tree Traversal", RED_B),
            ("🔍", "Finding Connected Components", YELLOW),
            ("🚗", "GPS Navigation Systems", MAROON_B),
        ]

        app_mobs = []
        for emoji, text, color in apps:
            line = VGroup(
                Text(emoji, font_size=32),
                Text(text, font_size=26, color=color),
            ).arrange(RIGHT, buff=0.3)
            app_mobs.append(line)

        apps_group = VGroup(*app_mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        apps_group.next_to(heading, DOWN, buff=0.6)
        apps_group.shift(LEFT * 1)

        for i, am in enumerate(app_mobs):
            am.shift(RIGHT * 12)
            self.play(
                am.animate.shift(LEFT * 12),
                run_time=0.5,
                rate_func=smooth
            )
            self.wait(0.2)

        self.wait(3)

        all_mobs = VGroup(*self.mobjects)
        self.play(
            all_mobs.animate.scale(0.1).set_opacity(0),
            run_time=1.5
        )


# ============================================================
# SCENE 9: TIME & SPACE COMPLEXITY
# ============================================================
class Scene09_Complexity(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"

        heading = Text(
            "Time & Space Complexity",
            font_size=48,
            color=YELLOW,
            weight=BOLD
        ).to_edge(UP, buff=0.4)
        self.play(FadeIn(heading, shift=DOWN))

        # Time complexity
        time_heading = Text(
            "Time Complexity",
            font_size=36,
            color=GREEN,
            weight=BOLD
        ).shift(UP * 1.5 + LEFT * 3)

        time_formula = MathTex(
            r"O(V + E)",
            font_size=60,
            color=WHITE
        ).next_to(time_heading, DOWN, buff=0.3)

        time_explain = VGroup(
            Text("V = Number of Vertices (nodes)", font_size=24, color=BLUE_B),
            Text("E = Number of Edges (connections)", font_size=24, color=BLUE_B),
            Text("Each vertex is visited ONCE", font_size=24, color=GREEN_B),
            Text("Each edge is examined ONCE", font_size=24, color=GREEN_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        time_explain.next_to(time_formula, DOWN, buff=0.3)

        self.play(Write(time_heading))
        self.play(Write(time_formula), run_time=1)
        self.play(FadeIn(time_explain, shift=UP * 0.5), run_time=1)
        self.wait(1)

        # Space complexity
        space_heading = Text(
            "Space Complexity",
            font_size=36,
            color=RED,
            weight=BOLD
        ).shift(UP * 1.5 + RIGHT * 3)

        space_formula = MathTex(
            r"O(V)",
            font_size=60,
            color=WHITE
        ).next_to(space_heading, DOWN, buff=0.3)

        space_explain = VGroup(
            Text("Queue can hold up to V nodes", font_size=24, color=ORANGE),
            Text("Visited set stores V nodes", font_size=24, color=ORANGE),
            Text("Worst case: all nodes in queue", font_size=24, color=RED_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        space_explain.next_to(space_formula, DOWN, buff=0.3)

        self.play(Write(space_heading))
        self.play(Write(space_formula), run_time=1)
        self.play(FadeIn(space_explain, shift=UP * 0.5), run_time=1)
        self.wait(1)

        # Divider
        divider = Line(UP * 2, DOWN * 2.5, color=GREY, stroke_width=1).shift(LEFT * 0)
        self.play(Create(divider))

        # Comparison table at bottom
        comparison = Text(
            "BFS vs DFS: BFS uses MORE memory but finds SHORTEST path",
            font_size=26,
            color=TEAL
        ).to_edge(DOWN, buff=0.5)
        box = SurroundingRectangle(comparison, color=TEAL, buff=0.2, corner_radius=0.1)

        self.play(Write(comparison), Create(box))
        self.wait(4)

        all_mobs = VGroup(*self.mobjects)
        self.play(all_mobs.animate.shift(DOWN * 10), run_time=1.5)


# ============================================================
# SCENE 10: BFS vs DFS COMPARISON
# ============================================================
class Scene10_BFSvsDFS(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"

        heading = Text(
            "BFS vs DFS",
            font_size=52,
            color=YELLOW,
            weight=BOLD
        ).to_edge(UP, buff=0.4)
        self.play(FadeIn(heading, shift=DOWN))

        # Table headers
        bfs_head = Text("BFS", font_size=36, color=BLUE, weight=BOLD).shift(LEFT * 3 + UP * 1.5)
        dfs_head = Text("DFS", font_size=36, color=RED, weight=BOLD).shift(RIGHT * 3 + UP * 1.5)
        vs_text = Text("VS", font_size=30, color=YELLOW).shift(UP * 1.5)

        self.play(Write(bfs_head), Write(dfs_head), Write(vs_text))

        comparisons = [
            ("Uses Queue (FIFO)", "Uses Stack (LIFO)"),
            ("Level by level", "Goes deep first"),
            ("Shortest path ✓", "No shortest path guarantee"),
            ("More memory", "Less memory"),
            ("O(V + E) time", "O(V + E) time"),
            ("Wide exploration", "Deep exploration"),
        ]

        y_start = 0.7
        for i, (bfs_point, dfs_point) in enumerate(comparisons):
            y = y_start - i * 0.6

            bfs_text = Text(bfs_point, font_size=22, color=BLUE_B).shift(LEFT * 3 + UP * y)
            dfs_text = Text(dfs_point, font_size=22, color=RED_B).shift(RIGHT * 3 + UP * y)
            dot = Dot(color=GREY).shift(UP * y)

            self.play(
                FadeIn(bfs_text, shift=LEFT),
                FadeIn(dfs_text, shift=RIGHT),
                FadeIn(dot),
                run_time=0.6
            )

        # Divider line
        divider = Line(UP * 2, DOWN * 3, color=YELLOW, stroke_width=2)
        self.play(Create(divider))

        self.wait(4)

        all_mobs = VGroup(*self.mobjects)
        self.play(all_mobs.animate.shift(LEFT * 16), run_time=1.5)


# ============================================================
# SCENE 11: PYTHON CODE IMPLEMENTATION
# ============================================================
class Scene11_PythonCode(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"

        heading = Text(
            "Python Implementation",
            font_size=48,
            color=YELLOW,
            weight=BOLD
        ).to_edge(UP, buff=0.3)
        self.play(FadeIn(heading, shift=DOWN))

        code_string = """from collections import deque

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

# Example Graph (Adjacency List)
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F', 'G'],
    'D': ['B'], 'E': ['B'],
    'F': ['C'], 'G': ['C']
}

print(bfs(graph, 'A'))
# Output: ['A','B','C','D','E','F','G']"""

        code = Code(
            code=code_string,
            tab_width=4,
            language="Python",
            font_size=18,
            background="window",
            insert_line_no=True,
            style="monokai",
        )
        code.next_to(heading, DOWN, buff=0.3)
        code.scale(0.85)

        # Slide code in from bottom
        code.shift(DOWN * 8)
        self.play(
            code.animate.shift(UP * 8),
            run_time=2,
            rate_func=smooth
        )
        self.wait(5)

        # Highlight important parts
        highlight_box = SurroundingRectangle(
            code,
            color=GREEN,
            buff=0.15,
            corner_radius=0.1,
            stroke_width=3
        )
        self.play(Create(highlight_box))
        self.wait(2)

        all_mobs = VGroup(*self.mobjects)
        self.play(all_mobs.animate.shift(RIGHT * 16), run_time=1.5)


# ============================================================
# SCENE 12: SUMMARY & OUTRO
# ============================================================
class Scene12_Summary(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"

        heading = Text(
            "Summary",
            font_size=56,
            color=YELLOW,
            weight=BOLD
        ).to_edge(UP, buff=0.5)
        self.play(FadeIn(heading, shift=DOWN))

        summary_points = [
            ("✅", "BFS traverses graphs LEVEL by LEVEL", GREEN),
            ("✅", "Uses a QUEUE (FIFO) data structure", BLUE),
            ("✅", "Time: O(V + E), Space: O(V)", ORANGE),
            ("✅", "Finds SHORTEST PATH in unweighted graphs", TEAL),
            ("✅", "Marks nodes as VISITED to avoid cycles", PURPLE),
            ("✅", "Used in GPS, web crawling, networking & more", RED_B),
        ]

        mobs = []
        for emoji, text, color in summary_points:
            line = VGroup(
                Text(emoji, font_size=30),
                Text(text, font_size=26, color=color),
            ).arrange(RIGHT, buff=0.3)
            mobs.append(line)

        summary_group = VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        summary_group.next_to(heading, DOWN, buff=0.6)
        summary_group.shift(LEFT * 1)

        for m in mobs:
            self.play(FadeIn(m, shift=UP * 0.5), run_time=0.6)
            self.wait(0.3)

        self.wait(2)

        # Thank you
        self.play(*[FadeOut(m) for m in mobs], FadeOut(heading), run_time=1)

        thanks = Text(
            "Thank You for Watching!",
            font_size=56,
            color=YELLOW,
            weight=BOLD
        )
        subscribe = Text(
            "Like & Subscribe for more Algorithm Visualizations",
            font_size=30,
            color=BLUE_B
        ).next_to(thanks, DOWN, buff=0.5)

        self.play(FadeIn(thanks, scale=0.5), run_time=1.5)
        self.play(Write(subscribe))
        self.wait(3)

        # Final fade
        self.play(
            thanks.animate.scale(1.5).set_opacity(0),
            subscribe.animate.shift(DOWN * 3).set_opacity(0),
            run_time=2
        )


# ============================================================
# MASTER SCENE - COMBINES ALL SCENES
# ============================================================
class BFS_Full_Video(Scene):
    def construct(self):
        scenes = [
            Scene01_Intro,
            Scene02_WhatIsGraph,
            Scene03_WhatIsBFS,
            Scene04_AlgorithmSteps,
            Scene05_BFSTraversal,
            Scene06_CyclicGraphBFS,
            Scene07_QueueExplanation,
            Scene08_Applications,
            Scene09_Complexity,
            Scene10_BFSvsDFS,
            Scene11_PythonCode,
            Scene12_Summary,
        ]

        for scene_class in scenes:
            scene_instance = scene_class()
            scene_instance.camera = self.camera
            scene_instance.renderer = self.renderer
            scene_instance.construct()