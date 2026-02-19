from manimlib import *
import numpy as np


class SingleChannel1x1(Scene):

    def construct(self):

        # ── palette ──────────────────────────────────
        NEON_GOLD  = "#ffd700"
        SOFT_WHITE = "#e0e0e0"
        NEON_PINK  = "#ff2e6c"

        IN_FILL    = GREEN_E                          # green cells
        IN_EDGE    = GREEN_C
        OUT_FILL   = MAROON_E                         # maroon cells
        OUT_EDGE   = MAROON_B
        RESULT_CLR = MAROON_B                         # filled output tint
        EQ_FILL    = "#2e1052"                        # deep purple card
        EQ_EDGE    = PURPLE_B                         # purple stroke

        weight_val = 2
        np.random.seed(21)
        vals = np.random.randint(1, 10, (4, 4))
        cs = 0.82

        # ── helper: safe move (no Transform) ─────────
        def glide(mob, target_pos, **kw):
            s = mob.get_center().copy()
            e = np.array(target_pos, dtype=float)
            return UpdateFromAlphaFunc(
                mob, lambda m, a: m.move_to(s + a * (e - s)), **kw
            )

        # ═══════════════════════════════════════════════
        #  ACT 1 — TITLE
        # ═══════════════════════════════════════════════

        t1 = Text("1 × 1", font_size=120, weight=BOLD)
        t1.set_color(NEON_GOLD)
        t2 = Text("Convolution", font_size=60, weight=BOLD)
        t2.set_color(SOFT_WHITE)
        t2.next_to(t1, DOWN, buff=0.35)


        self.play(FadeIn(t1, shift=DOWN * 0.4), run_time=0.8)
        self.play(FadeIn(t2, shift=UP * 0.3), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(t1), FadeOut(t2),  run_time=0.6)

        # ═══════════════════════════════════════════════
        #  ACT 2 — BUILD THE STAGE
        # ═══════════════════════════════════════════════

        # ── input 4×4 (GREEN) ────────────────────────
        in_group = VGroup()
        in_cells = {}
        in_nums  = {}
        for i in range(4):
            for j in range(4):
                sq = Square(cs)
                sq.set_fill(IN_FILL, 1)
                sq.set_stroke(IN_EDGE, 1.8)
                sq.move_to(RIGHT * j * cs + DOWN * i * cs)
                num = Text(str(vals[i, j]), font_size=34, weight=BOLD)
                num.set_color(WHITE)
                num.move_to(sq)
                g = VGroup(sq, num)
                in_cells[(i, j)] = g
                in_nums[(i, j)]  = num
                in_group.add(g)
        in_group.center().move_to(LEFT * 4.2)

        in_label = Text("Input", font_size=35, weight=BOLD)
        in_label.set_color(GREEN_A)
        in_label.next_to(in_group, UP, buff=0.55)
        in_dim = Text("4 × 4 × 1", font_size=25, weight=BOLD)
        in_dim.set_color(GREY_B)
        in_dim.next_to(in_label, DOWN, buff=0.15)

        # ── kernel 1×1 ──────────────────────────────
        k_sq = Square(cs)
        k_sq.set_fill(NEON_GOLD, 0.9)
        k_sq.set_stroke(NEON_GOLD, 3)
        k_num = Text(str(weight_val), font_size=35, weight=BOLD)
        k_num.set_color(BLACK)
        k_num.move_to(k_sq)
        kernel = VGroup(k_sq, k_num)
        kernel.set_z_index(5)
        kernel.move_to(ORIGIN + UP * 0.3)
        k_home = kernel.get_center().copy()

        k_label = Text("Kernel", font_size=30, weight=BOLD)
        k_label.set_color(NEON_GOLD)
        k_label.next_to(kernel, UP, buff=0.55)
        k_w = Text("w = 2", font_size=28, weight=BOLD)
        k_w.set_color(NEON_GOLD)
        k_w.next_to(k_label, DOWN, buff=0.12)

        times_sym = Text("*", font_size=50, weight=BOLD)
        times_sym.set_color(GREY_A)
        times_sym.move_to(LEFT * 1.9 + UP * 0.3)

        eq_sym = Text("=", font_size=50, weight=BOLD)
        eq_sym.set_color(GREY_A)
        eq_sym.move_to(RIGHT * 1.9 + UP * 0.3)

        # ── output 4×4 (MAROON) ─────────────────────
        out_group = VGroup()
        out_cells = {}
        out_qmarks = {}
        for i in range(4):
            for j in range(4):
                sq = Square(cs)
                sq.set_fill(OUT_FILL, 1)
                sq.set_stroke(OUT_EDGE, 1.8)
                sq.move_to(RIGHT * j * cs + DOWN * i * cs)
                qm = Text("?", font_size=25, weight=BOLD)
                qm.set_color(GREY_C)
                qm.move_to(sq)
                out_group.add(sq)
                out_cells[(i, j)]  = sq
                out_qmarks[(i, j)] = qm
        out_group.center().move_to(RIGHT * 4.2)
        for i in range(4):
            for j in range(4):
                out_qmarks[(i, j)].move_to(out_cells[(i, j)])

        out_label = Text("Output", font_size=35, weight=BOLD)
        out_label.set_color(MAROON_A)
        out_label.next_to(out_group, UP, buff=0.55)
        out_dim = Text("4 × 4 × 1", font_size=25, weight=BOLD)
        out_dim.set_color(GREY_B)
        out_dim.next_to(out_label, DOWN, buff=0.15)

        # ── reveal everything ────────────────────────
        self.play(
            LaggedStartMap(FadeIn, in_group, lag_ratio=0.03),
            FadeIn(in_label), FadeIn(in_dim),
            run_time=1.2,
        )
        self.play(
            FadeIn(times_sym),
            FadeIn(kernel, scale=1.4),
            FadeIn(k_label), FadeIn(k_w),
            Flash(kernel.get_center(), color=NEON_GOLD,
                  flash_radius=0.7, num_lines=10, run_time=0.6),
            run_time=0.7,
        )
        qm_vg = VGroup(*[out_qmarks[(i, j)] for i in range(4) for j in range(4)])
        self.play(
            FadeIn(eq_sym),
            LaggedStartMap(FadeIn, out_group, lag_ratio=0.03),
            LaggedStartMap(FadeIn, qm_vg, lag_ratio=0.03),
            FadeIn(out_label), FadeIn(out_dim),
            run_time=1.0,
        )
        self.wait(0.8)

        # ═══════════════════════════════════════════════
        #  ACT 3 — DEEP DIVE: first pixel
        #    equation to the LEFT of the grid (not below)
        # ═══════════════════════════════════════════════

        self.play(
            FadeOut(times_sym), FadeOut(eq_sym),
            FadeOut(k_label), FadeOut(k_w),
            run_time=0.4,
        )

        k_sq.set_fill(NEON_GOLD, 0.45)

        # highlight cell (0,0)
        hl = SurroundingRectangle(in_cells[(0, 0)], stroke_width=4, buff=0.04)
        hl.set_color(NEON_PINK)
        hl.set_z_index(6)

        dest = in_cells[(0, 0)][0].get_center().copy()
        self.play(
            glide(kernel, dest),
            ShowCreation(hl),
            run_time=0.7,
        )

        # pan camera LEFT so we see equation to the left of the grid
        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.scale(0.85).move_to(
                in_group.get_center() + LEFT * 2.2
            ),
            run_time=0.7,
        )

        # equation to the LEFT of the input grid, vertically centred
        pv = int(vals[0, 0])
        rv = pv * weight_val
        eq_line = VGroup(
            Text(str(pv), font_size=44, weight=BOLD).set_color(WHITE),
            Text("x", font_size=40, weight=BOLD).set_color(GREY_A),
            Text(str(weight_val), font_size=44, weight=BOLD).set_color(NEON_GOLD),
            Text("=", font_size=44, weight=BOLD).set_color(GREY_A),
            Text(str(rv), font_size=52, weight=BOLD).set_color(RESULT_CLR),
        )
        eq_line.arrange(RIGHT, buff=0.22)
        eq_line.next_to(in_group, LEFT, buff=1.2)

        # purple card behind equation (same style as grid cells)
        eq_card = RoundedRectangle(
            width=eq_line.get_width() + 0.5,
            height=eq_line.get_height() + 0.4,
            corner_radius=0.15,
        )
        eq_card.set_fill(EQ_FILL, 1)
        eq_card.set_stroke(EQ_EDGE, 2)
        eq_card.move_to(eq_line)

        # glowdots fly from cell & kernel to equation
        d1 = GlowDot(in_nums[(0, 0)].get_center(), color=WHITE, radius=0.1)
        d2 = GlowDot(k_num.get_center(), color=NEON_GOLD, radius=0.1)
        d1.set_z_index(10)
        d2.set_z_index(10)
        self.play(
            FadeIn(eq_card),
            glide(d1, eq_line[0].get_center()),
            glide(d2, eq_line[2].get_center()),
            run_time=0.8,
        )
        self.remove(d1, d2)
        self.play(
            FadeIn(eq_line[0]), FadeIn(eq_line[1]), FadeIn(eq_line[2]),
            run_time=0.3,
        )
        self.wait(0.25)
        self.play(
            FadeIn(eq_line[3]),
            FadeIn(eq_line[4], scale=1.3),
            Flash(eq_line[4].get_center(), color=RESULT_CLR,
                  flash_radius=0.5, num_lines=8, run_time=0.5),
            run_time=0.6,
        )
        self.wait(0.6)

        # fly result dot to the output cell
        target_out = out_cells[(0, 0)].get_center().copy()
        rd = GlowDot(eq_line[4].get_center(), color=RESULT_CLR,
                      radius=0.15, glow_factor=2.5)
        rd.set_z_index(10)

        rv_txt = Text(str(rv), font_size=35, weight=BOLD)
        rv_txt.set_color(WHITE)
        rv_txt.move_to(target_out)

        self.play(
            FadeOut(eq_line), FadeOut(eq_card),
            glide(rd, target_out),
            self.camera.frame.animate.restore(),
            FadeOut(hl),
            run_time=1.0,
        )
        self.remove(rd, out_qmarks[(0, 0)])
        out_cells[(0, 0)].set_fill(RESULT_CLR, 0.3)
        self.add(rv_txt)
        out_group.add(rv_txt)
        self.wait(0.3)

        # ═══════════════════════════════════════════════
        #  ACT 4 — SCAN: kernel sweeps the rest
        #    constant speed (no acceleration)
        # ═══════════════════════════════════════════════

        order = [(i, j) for i in range(4) for j in range(4)
                 if not (i == 0 and j == 0)]

        SCAN_SPD = 0.18   # constant speed for every cell

        for idx, (r, c) in enumerate(order):
            dst = in_cells[(r, c)][0].get_center().copy()

            self.play(glide(kernel, dst), run_time=SCAN_SPD)

            pv = int(vals[r, c])
            rv = pv * weight_val

            o_pos = out_cells[(r, c)].get_center().copy()
            dot = GlowDot(dst, color=RESULT_CLR, radius=0.1, glow_factor=2.0)
            dot.set_z_index(10)
            self.play(glide(dot, o_pos), run_time=SCAN_SPD)

            self.remove(dot, out_qmarks[(r, c)])
            t = Text(str(rv), font_size=35, weight=BOLD)
            t.set_color(WHITE)
            t.move_to(o_pos)
            self.add(t)
            out_cells[(r, c)].set_fill(RESULT_CLR, 0.3)
            out_group.add(t)

        # celebrate
        self.play(
            FlashAround(out_group, color=RESULT_CLR,
                        stroke_width=5, time_width=0.7, run_time=1.0),
        )
        self.wait(0.4)

        # ═══════════════════════════════════════════════
        #  ACT 5 — RESTORE LAYOUT
        # ═══════════════════════════════════════════════

        k_sq.set_fill(NEON_GOLD, 0.9)
        self.play(glide(kernel, k_home), run_time=0.5)
        self.play(
            FadeIn(times_sym), FadeIn(eq_sym),
            FadeIn(k_label), FadeIn(k_w),
            run_time=0.4,
        )
        self.wait(0.5)

        # ═══════════════════════════════════════════════
        #  ACT 7 — FORMULA + INSIGHTS
        #    shift camera down enough to see everything
        # ═══════════════════════════════════════════════

        self.play(self.camera.frame.animate.shift(DOWN * 1.15), run_time=0.6)

        formula_left = Text("out(i, j)", font_size=36, weight=BOLD)
        formula_left.set_color(MAROON)
        formula_eq = Text(" = w·", font_size=36, weight=BOLD)
        formula_eq[-2].set_color(YELLOW)
        formula_right = Text("in(i, j)", font_size=36, weight=BOLD)
        formula_right.set_color(GREEN)
        formula = VGroup(formula_left, formula_eq, formula_right)
        formula.arrange(RIGHT, buff=0.12)
        # center below the entire layout (input + kernel + output)
        stage_center = (in_group.get_center() + out_group.get_center()) / 2
        stage_bottom = min(in_group.get_bottom()[1], out_group.get_bottom()[1])
        formula.move_to(stage_center)
        formula.set_y(stage_bottom - 1.0)

        self.play(Write(formula), run_time=1.0)
        self.play(
            FlashAround(formula, color=NEON_GOLD, stroke_width=3,
                        time_width=0.5, run_time=0.7),
        )
        self.wait(0.4)

        ins1 = Text("Every pixel is scaled independently",
                     font_size=34, weight=BOLD)
        ins1.set_color(PURPLE)
        ins1.next_to(formula, DOWN, buff=0.5)
        self.play(Write(ins1), run_time=0.9)

        ins2 = Text("Zero spatial context — receptive field is 1 × 1",
                     font_size=28, weight=BOLD)
        ins2.set_color(GREY_A)
        ins2.next_to(ins1, DOWN, buff=0.4)
        self.play(FadeIn(ins2, shift=UP * 0.15), run_time=0.7)
        self.wait(2)
