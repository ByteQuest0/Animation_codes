from manimlib import *
import numpy as np


class VolumeConv1x1(Scene):
    """
    General case: 1x1 convolution over a 3D volume.
    Input 4x4x4, Filter 1x1x4 → Output 4x4x1 (one filter)
    Then 3 filters → 4x4x3.  ReLU at the end.
    """

    def construct(self):

        # ── palette ──────────────────────────────────
        NEON_GOLD   = "#ffd700"
        SOFT_WHITE  = "#e0e0e0"
        NEON_CYAN   = "#00e5ff"
        NEON_PINK   = "#ff2e6c"
        INPUT_CLR   = "#2979ff"
        OUT_CLR     = "#00e676"
        MULTI_CLR   = "#e040fb"
        RELU_CLR    = "#ff9100"

        CZ = 0.38                       # cell size for cuboids
        N  = 4                          # grid dimension

        # ── helper: safe move ────────────────────────
        def glide(mob, target_pos, **kw):
            s = mob.get_center().copy()
            e = np.array(target_pos, dtype=float)
            return UpdateFromAlphaFunc(
                mob, lambda m, a: m.move_to(s + a * (e - s)), **kw
            )

        # ── helper: 3D cuboid (front + top + right) ─
        def cuboid(h, w, d, color, pos=ORIGIN, cz=CZ, opacity=0.85):
            front = Rectangle(width=w * cz, height=h * cz)
            front.set_fill(color, opacity)
            front.set_stroke(WHITE, 1.5)
            front.move_to(pos)

            dx = min(d, 12) * cz * 0.35
            dy = min(d, 12) * cz * 0.22

            top = Polygon(
                front.get_corner(UL),
                front.get_corner(UR),
                front.get_corner(UR) + RIGHT * dx + UP * dy,
                front.get_corner(UL) + RIGHT * dx + UP * dy,
            )
            top.set_fill(interpolate_color(color, WHITE, 0.3), opacity)
            top.set_stroke(WHITE, 1.5)

            side = Polygon(
                front.get_corner(UR),
                front.get_corner(DR),
                front.get_corner(DR) + RIGHT * dx + UP * dy,
                front.get_corner(UR) + RIGHT * dx + UP * dy,
            )
            side.set_fill(interpolate_color(color, BLACK, 0.2), opacity)
            side.set_stroke(WHITE, 1.5)

            return VGroup(front, top, side)

        # helper: position on a cuboid's front grid (row i, col j)
        def grid_pos(front_rect, i, j):
            """Center of cell (i,j) on the front face."""
            left = front_rect.get_left()[0]
            top  = front_rect.get_top()[1]
            x = left + (j + 0.5) * CZ
            y = top  - (i + 0.5) * CZ
            return np.array([x, y, 0.0])

        # ═══════════════════════════════════════════════
        #  ACT 1 — TITLE
        # ═══════════════════════════════════════════════

        t1 = Text("1 x 1 Convolution", font_size=80, weight=BOLD)
        t1.set_color(NEON_GOLD)
        t2 = Text("on a Volume", font_size=50, weight=BOLD)
        t2.set_color(SOFT_WHITE)
        t2.next_to(t1, DOWN, buff=0.35)
        tag = Text("multi-channel · pointwise", font_size=28, weight=BOLD)
        tag.set_color(GREY_A)
        tag.next_to(t2, DOWN, buff=0.5)

        self.play(FadeIn(t1, shift=DOWN * 0.4), run_time=0.8)
        self.play(FadeIn(t2, shift=UP * 0.3), run_time=0.6)
        self.play(
            FadeIn(tag, shift=UP * 0.15),
            Flash(t1.get_center(), color=NEON_GOLD,
                  flash_radius=2.0, line_length=0.5, num_lines=16,
                  run_time=0.8),
            run_time=0.8,
        )
        self.wait(1.2)
        self.play(FadeOut(t1), FadeOut(t2), FadeOut(tag), run_time=0.6)

        # ═══════════════════════════════════════════════
        #  ACT 2 — SHOW INPUT * FILTER = OUTPUT
        # ═══════════════════════════════════════════════

        inp = cuboid(N, N, N, INPUT_CLR, pos=LEFT * 4.5)
        inp_label = Text("Input", font_size=32, weight=BOLD)
        inp_label.set_color(NEON_CYAN)
        inp_label.next_to(inp, UP, buff=0.5)
        inp_dim = Text("4 x 4 x 4", font_size=22, weight=BOLD)
        inp_dim.set_color(GREY_B)
        inp_dim.next_to(inp_label, DOWN, buff=0.12)

        # grid lines on front face to show 4x4 spatial cells
        grid_lines = VGroup()
        fr = inp[0]
        for k in range(1, N):
            # horizontal
            hl = Line(
                fr.get_left() + DOWN * k * CZ + UP * fr.get_height() / 2,
                fr.get_right() + DOWN * k * CZ + UP * fr.get_height() / 2,
                stroke_width=1,
            )
            hl.set_color(WHITE)
            hl.set_opacity(0.4)
            grid_lines.add(hl)
            # vertical
            vl = Line(
                fr.get_top() + RIGHT * k * CZ - RIGHT * fr.get_width() / 2,
                fr.get_bottom() + RIGHT * k * CZ - RIGHT * fr.get_width() / 2,
                stroke_width=1,
            )
            vl.set_color(WHITE)
            vl.set_opacity(0.4)
            grid_lines.add(vl)

        # filter 1x1x4 (thin bar matching depth)
        filt = cuboid(1, 1, N, NEON_GOLD, pos=LEFT * 0.8, opacity=0.9)
        filt_home = filt.get_center().copy()
        f_label = Text("Filter", font_size=28, weight=BOLD)
        f_label.set_color(NEON_GOLD)
        f_label.next_to(filt, UP, buff=0.5)
        f_dim = Text("1 x 1 x 4", font_size=22, weight=BOLD)
        f_dim.set_color(NEON_GOLD)
        f_dim.next_to(f_label, DOWN, buff=0.1)

        times_sym = Text("*", font_size=55, weight=BOLD)
        times_sym.set_color(GREY_A)
        times_sym.move_to(LEFT * 2.5)

        eq_sym = Text("=", font_size=55, weight=BOLD)
        eq_sym.set_color(GREY_A)
        eq_sym.move_to(RIGHT * 1.5)

        # output 4x4x1 (flat 2D — no depth)
        out_rect = Rectangle(width=N * CZ, height=N * CZ)
        out_rect.set_fill(OUT_CLR, 0.4)
        out_rect.set_stroke(WHITE, 1.5)
        out_rect.move_to(RIGHT * 4.5)
        out = VGroup(out_rect)
        o_label = Text("Output", font_size=32, weight=BOLD)
        o_label.set_color(OUT_CLR)
        o_label.next_to(out, UP, buff=0.5)
        o_dim = Text("4 x 4 x 1", font_size=22, weight=BOLD)
        o_dim.set_color(GREY_B)
        o_dim.next_to(o_label, DOWN, buff=0.12)

        # output grid lines
        out_grid = VGroup()
        ofr = out[0]
        for k in range(1, N):
            hl = Line(
                ofr.get_left() + DOWN * k * CZ + UP * ofr.get_height() / 2,
                ofr.get_right() + DOWN * k * CZ + UP * ofr.get_height() / 2,
                stroke_width=1,
            )
            hl.set_color(WHITE)
            hl.set_opacity(0.4)
            out_grid.add(hl)
            vl = Line(
                ofr.get_top() + RIGHT * k * CZ - RIGHT * ofr.get_width() / 2,
                ofr.get_bottom() + RIGHT * k * CZ - RIGHT * ofr.get_width() / 2,
                stroke_width=1,
            )
            vl.set_color(WHITE)
            vl.set_opacity(0.4)
            out_grid.add(vl)

        # reveal
        self.play(FadeIn(inp, scale=0.8), run_time=0.8)
        self.play(
            FadeIn(inp_label), FadeIn(inp_dim),
            FadeIn(grid_lines),
            run_time=0.5,
        )
        self.wait(0.3)
        self.play(
            FadeIn(times_sym),
            FadeIn(filt, scale=1.4),
            FadeIn(f_label), FadeIn(f_dim),
            Flash(filt.get_center(), color=NEON_GOLD,
                  flash_radius=0.6, num_lines=10, run_time=0.6),
            run_time=0.7,
        )
        self.wait(0.3)
        self.play(
            FadeIn(eq_sym),
            FadeIn(out, scale=0.8),
            FadeIn(o_label), FadeIn(o_dim),
            FadeIn(out_grid),
            run_time=0.8,
        )
        self.wait(0.8)

        # ═══════════════════════════════════════════════
        #  ACT 3 — FIRST PIXEL + SCAN
        #    filter moves INTO input volume, dot flies out
        # ═══════════════════════════════════════════════

        self.play(
            FadeOut(times_sym), FadeOut(eq_sym),
            FadeOut(f_label), FadeOut(f_dim),
            run_time=0.4,
        )


        # bring input & output closer, then zoom in
        inp_grp = VGroup(inp, inp_label, inp_dim, grid_lines)
        out_grp = VGroup(out, o_label, o_dim, out_grid)
        self.play(
            inp_grp.animate.shift(RIGHT * 2.0),
            out_grp.animate.shift(LEFT * 2.0),
            self.camera.frame.animate.scale(0.85),
            run_time=0.8,
        )
        self.wait(0.3)

        # depth offset so filter sits INSIDE the volume, not on the face
        inp_dx = min(N, 12) * CZ * 0.35
        inp_dy = min(N, 12) * CZ * 0.22
        depth_shift = RIGHT * inp_dx * 0.5 + UP * inp_dy * 0.5
       
        self.play(self.camera.frame.animate.scale(0.8))

        # highlight square on input face
        hl = Square(CZ)
        hl.set_fill(NEON_GOLD, 0.35)
        hl.set_stroke(NEON_GOLD, 3)
        hl.move_to(grid_pos(fr, 0, 0))
        hl.set_z_index(5)

        # move filter INTO input at (0,0) + reduce input opacity
        first_cell = grid_pos(fr, 0, 0) + depth_shift
        self.play(
            glide(filt, first_cell),
            FadeIn(hl),
            inp[0].animate.set_fill(INPUT_CLR, 0.3),
            inp[1].animate.set_fill(interpolate_color(INPUT_CLR, WHITE, 0.3), 0.3),
            inp[2].animate.set_fill(interpolate_color(INPUT_CLR, BLACK, 0.2), 0.3),
            run_time=0.8,
        )
        filt.set_z_index(4)
        self.wait(0.3)

        # fly dot directly to output cell (0,0)
        out_pos_00 = grid_pos(ofr, 0, 0)
        gd = GlowDot(first_cell, color=OUT_CLR, radius=0.12, glow_factor=2.5)
        gd.set_z_index(10)
        self.play(glide(gd, out_pos_00), run_time=0.6)
        self.remove(gd)
        self.play(
            Flash(out_pos_00, color=OUT_CLR,
                  flash_radius=0.3, num_lines=8, run_time=0.5),
        )

        # fill output cell (0,0)
        filled_00 = Square(CZ)
        filled_00.set_fill(OUT_CLR, 0.7)
        filled_00.set_stroke(width=0)
        filled_00.move_to(out_pos_00)
        self.add(filled_00)
        self.wait(0.3)

        # ── scan the rest ────────────────────────────

        SCAN_SPD = 0.18
        filled_cells = VGroup(filled_00)

        order = [(i, j) for i in range(N) for j in range(N)
                 if not (i == 0 and j == 0)]

        prev_row = 0


        for (r, c) in order:
            cell_c = grid_pos(fr, r, c) + depth_shift
            hl_c   = grid_pos(fr, r, c)
            out_c  = grid_pos(ofr, r, c)

            # move filter + highlight to next cell
            self.play(
                glide(filt, cell_c),
                glide(hl, hl_c),
                run_time=SCAN_SPD,
            )

            

            # create dot at filter, fly to output
            dot = GlowDot(cell_c, color=OUT_CLR, radius=0.1, glow_factor=2.0)
            dot.set_z_index(10)
            self.play(glide(dot, out_c), run_time=SCAN_SPD)
            self.remove(dot)

            # fill output cell
            sq = Square(CZ)
            sq.set_fill(OUT_CLR, 0.7)
            sq.set_stroke(width=0)
            sq.move_to(out_c)
            self.add(sq)
            filled_cells.add(sq)

            # flash at end of each row
            if c == N - 1 and r != N - 1:
                row_center = np.array([
                    ofr.get_center()[0],
                    grid_pos(ofr, r, 0)[1],
                    0.0,
                ])
                self.play(
                    Flash(row_center, color=OUT_CLR,
                          flash_radius=0.4, num_lines=6, run_time=0.25),
                )

        self.play(FadeOut(hl), run_time=0.2)

        # celebrate with double flash
        self.play(
            FlashAround(out, color=OUT_CLR,
                        stroke_width=5, time_width=0.6, run_time=0.8),
        )
        self.play(
            FlashAround(filled_cells, color=NEON_CYAN,
                        stroke_width=3, time_width=0.5, run_time=0.6),
        )

        # restore input opacity
        self.play(
            inp[0].animate.set_fill(INPUT_CLR, 0.85),
            inp[1].animate.set_fill(interpolate_color(INPUT_CLR, WHITE, 0.3), 0.85),
            inp[2].animate.set_fill(interpolate_color(INPUT_CLR, BLACK, 0.2), 0.85),
            run_time=0.4,
        )
        self.wait(0.6)

        self.play(self.camera.frame.animate.scale(1/0.9))


        # ═══════════════════════════════════════════════
        #  ACT 5 — 3 FILTERS → 4 x 4 x 3
        # ═══════════════════════════════════════════════

        # fade single-filter stuff
        self.play(
            FadeOut(out), FadeOut(o_label), FadeOut(o_dim),
            FadeOut(out_grid), FadeOut(filled_cells),
            FadeOut(filt),
            run_time=0.5,
        )

        # reset camera + move input back to the left
        self.play(
            self.camera.frame.animate.scale(1 / 0.85).move_to(ORIGIN),
            inp_grp.animate.shift(LEFT * 2.0),
            run_time=0.7,
        )

        # three filters stacked
        nf = 3
        f_colors = [NEON_GOLD, NEON_PINK, NEON_CYAN]
        filters_vg = VGroup()
        for k in range(nf):
            f = cuboid(1, 1, N, f_colors[k], pos=ORIGIN, opacity=0.85)
            f.move_to(LEFT * 0.5 + UP * (0.55 - k * 0.55))
            filters_vg.add(f)

        nf_label = Text("3 filters", font_size=26, weight=BOLD)
        nf_label.set_color(MULTI_CLR)
        nf_label.next_to(filters_vg, UP, buff=0.6)
        nf_dim = Text("each 1 x 1 x 4", font_size=20, weight=BOLD)
        nf_dim.set_color(GREY_A)
        nf_dim.next_to(nf_label, DOWN, buff=0.12)

        eq2 = Text("=", font_size=55, weight=BOLD)
        eq2.set_color(GREY_A)
        eq2.move_to(RIGHT * 0.8)

        relu_txt = Text("ReLU", font_size=32, weight=BOLD)
        relu_txt.set_color(RELU_CLR)
        relu_txt.next_to(eq2, UP, buff=0.25)

        # output volume 4x4x3 (thicker)
        out_vol = cuboid(N, N, nf, MULTI_CLR, pos=RIGHT * 2.8, opacity=0.7)
        ov_label = Text("Output", font_size=32, weight=BOLD)
        ov_label.set_color(MULTI_CLR)
        ov_label.next_to(out_vol, UP, buff=0.5)
        ov_dim = Text("4 x 4 x 3", font_size=22, weight=BOLD)
        ov_dim.set_color(GREY_B)
        ov_dim.next_to(ov_label, DOWN, buff=0.12)

        # grid lines on output volume front face
        ov_grid = VGroup()
        ovfr = out_vol[0]
        for k in range(1, N):
            hl_line = Line(
                ovfr.get_left() + DOWN * k * CZ + UP * ovfr.get_height() / 2,
                ovfr.get_right() + DOWN * k * CZ + UP * ovfr.get_height() / 2,
                stroke_width=1,
            )
            hl_line.set_color(WHITE)
            hl_line.set_opacity(0.4)
            ov_grid.add(hl_line)
            vl_line = Line(
                ovfr.get_top() + RIGHT * k * CZ - RIGHT * ovfr.get_width() / 2,
                ovfr.get_bottom() + RIGHT * k * CZ - RIGHT * ovfr.get_width() / 2,
                stroke_width=1,
            )
            vl_line.set_color(WHITE)
            vl_line.set_opacity(0.4)
            ov_grid.add(vl_line)

        # reveal filters with stagger flash
        self.play(
            LaggedStartMap(FadeIn, filters_vg, lag_ratio=0.15, scale=1.3),
            run_time=0.8,
        )
        for k in range(nf):
            self.play(
                Flash(filters_vg[k].get_center(), color=f_colors[k],
                      flash_radius=0.35, num_lines=6, run_time=0.25),
            )
        self.play(FadeIn(nf_label), FadeIn(nf_dim), run_time=0.4)
        self.wait(0.3)

        # equals + ReLU above it
        self.play(FadeIn(eq2), run_time=0.3)
        self.play(
            FadeIn(relu_txt, shift=DOWN * 0.15),
            Flash(relu_txt.get_center(), color=RELU_CLR,
                  flash_radius=0.4, num_lines=8, run_time=0.4),
            run_time=0.5,
        )

        # output volume
        self.play(
            FadeIn(out_vol, scale=0.8),
            FadeIn(ov_label), FadeIn(ov_dim),
            FadeIn(ov_grid),
            run_time=0.8,
        )

        # glow dots from each filter → output depth slice
        for k in range(nf):
            gd = GlowDot(
                filters_vg[k].get_center(), color=f_colors[k],
                radius=0.12, glow_factor=2.5,
            )
            gd.set_z_index(10)
            target_y = out_vol[0].get_top()[1] - (k + 0.5) / nf * out_vol[0].get_height()
            target = np.array([out_vol[0].get_center()[0], target_y, 0.0])
            self.play(glide(gd, target), run_time=0.4)
            self.remove(gd)
            # flash at landing
            self.play(
                Flash(target, color=f_colors[k],
                      flash_radius=0.25, num_lines=6, run_time=0.2),
            )

        # double celebration
        self.play(
            FlashAround(out_vol, color=MULTI_CLR,
                        stroke_width=5, time_width=0.6, run_time=0.8),
        )
        self.play(
            FlashAround(out_vol, color=NEON_GOLD,
                        stroke_width=3, time_width=0.4, run_time=0.6),
        )
        self.wait(0.6)

        # ═══════════════════════════════════════════════
        #  ACT 6 — INSIGHT TEXT
        # ═══════════════════════════════════════════════

        self.play(self.camera.frame.animate.scale(0.95).shift(DOWN * 0.3 + LEFT * 0.6), run_time=0.6)

        stage_cx = (inp.get_center()[0] + out_vol.get_center()[0]) / 2
        stage_bot = min(inp.get_bottom()[1], out_vol.get_bottom()[1])

        ins1 = Text("1x1 conv = learned weighted sum across channels",
                     font_size=28, weight=BOLD)
        ins1.set_color(NEON_GOLD)
        ins1.move_to(RIGHT * stage_cx)
        ins1.set_y(stage_bot - 0.8)
        self.play(Write(ins1), run_time=0.9)
        self.play(
            FlashAround(ins1, color=NEON_GOLD, stroke_width=2,
                        time_width=0.4, run_time=0.5),
        )

        ins2 = Text("Changes depth from C to Nf  —  spatial dims unchanged",
                     font_size=24, weight=BOLD)
        ins2.set_color(GREY_A)
        ins2.next_to(ins1, DOWN, buff=0.3)
        self.play(FadeIn(ins2, shift=UP * 0.1), run_time=0.7)
        self.wait(3)

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
