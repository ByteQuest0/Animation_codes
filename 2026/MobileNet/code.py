from manimlib import *
import numpy as np


# ── palette ──────────────────────────────────────────────────────────
CH_COLORS = ["#E74C3C", "#27AE60", "#2980B9"]   # R, G, B channels
FILTER_COLOR = "#F39C12"
POINTWISE_COLOR = "#9B59B6"
DARK_BG = "#1a1a2e"
CARD_BG = "#222244"


def make_grid(rows, cols, cell_size=0.45, fill_color=BLUE, fill_opacity=0.6,
              stroke_color=WHITE, stroke_width=1.5):
    """Create a rows×cols grid of squares."""
    cells = VGroup()
    for r in range(rows):
        for c in range(cols):
            sq = Square(side_length=cell_size)
            sq.set_fill(fill_color, opacity=fill_opacity)
            sq.set_stroke(stroke_color, width=stroke_width)
            cells.add(sq)
    cells.arrange_in_grid(n_rows=rows, n_cols=cols, buff=0)
    return cells


def make_channel_stack(n_channels, rows, cols, cell_size=0.45, colors=None,
                       offset=np.array([0.15, -0.15, 0.0])):
    """Stack multiple grids with a diagonal offset to show depth."""
    colors = colors or CH_COLORS
    layers = VGroup()
    for i in range(n_channels):
        g = make_grid(rows, cols, cell_size=cell_size,
                      fill_color=colors[i % len(colors)], fill_opacity=0.55)
        g.shift(i * offset)
        layers.add(g)
    return layers


def labeled_arrow(start, end, label_text, font_size=28, color=YELLOW):
    """Arrow with a text label above it."""
    arrow = Arrow(start, end, buff=0.1, color=color, stroke_width=3)
    label = Text(label_text, font_size=font_size, color=color)
    label.next_to(arrow, UP, buff=0.15)
    return VGroup(arrow, label)


def create_3d_cuboid(h, w, d, color, pos=ORIGIN, cs=0.04):
    """Isometric 3D cuboid (front + top + right face)."""
    front = Rectangle(width=w * cs, height=h * cs)
    front.set_fill(color, opacity=0.85)
    front.set_stroke(WHITE, width=1.5)
    front.move_to(pos)
    dx = min(d, 20) * cs * 0.4
    dy = min(d, 20) * cs * 0.25
    top = Polygon(
        front.get_corner(UL), front.get_corner(UR),
        front.get_corner(UR) + RIGHT * dx + UP * dy,
        front.get_corner(UL) + RIGHT * dx + UP * dy,
    )
    top.set_fill(interpolate_color(color, WHITE, 0.3), opacity=0.85)
    top.set_stroke(WHITE, width=1.5)
    right_f = Polygon(
        front.get_corner(UR), front.get_corner(DR),
        front.get_corner(DR) + RIGHT * dx + UP * dy,
        front.get_corner(UR) + RIGHT * dx + UP * dy,
    )
    right_f.set_fill(interpolate_color(color, BLACK, 0.2), opacity=0.85)
    right_f.set_stroke(WHITE, width=1.5)
    return VGroup(front, top, right_f)


# ══════════════════════════════════════════════════════════════════════
#  SCENE — Standard (Normal) Convolution
# ══════════════════════════════════════════════════════════════════════

class NormalConvolution(Scene):
    def construct(self):
        INPUT_CLR  = "#4A90D9"
        FILTER_CLR = "#E74C3C"
        OUTPUT_CLR = "#2ECC71"
        ACCENT_CLR = "#F39C12"

        # ── helper: cuboid with visible grid on front face ───
        def gridded_cuboid(h, w, d, color, pos=ORIGIN, cs=0.35):
            fw, fh = w * cs, h * cs
            front = Rectangle(width=fw, height=fh)
            front.set_fill(color, opacity=0.85)
            front.set_stroke(WHITE, width=2)
            front.move_to(pos)
            lines = VGroup()
            for r in range(1, h):
                lines.add(Line(
                    pos + LEFT * fw / 2 + UP * (fh / 2 - r * cs),
                    pos + RIGHT * fw / 2 + UP * (fh / 2 - r * cs),
                    stroke_color=WHITE, stroke_width=1.0,
                    stroke_opacity=0.5,
                ))
            for c in range(1, w):
                lines.add(Line(
                    pos + UP * fh / 2 + RIGHT * (c * cs - fw / 2),
                    pos + DOWN * fh / 2 + RIGHT * (c * cs - fw / 2),
                    stroke_color=WHITE, stroke_width=1.0,
                    stroke_opacity=0.5,
                ))
            dx = min(d, 20) * cs * 0.45
            dy = min(d, 20) * cs * 0.28
            top = Polygon(
                front.get_corner(UL), front.get_corner(UR),
                front.get_corner(UR) + RIGHT * dx + UP * dy,
                front.get_corner(UL) + RIGHT * dx + UP * dy,
            )
            top.set_fill(interpolate_color(color, WHITE, 0.3), opacity=0.85)
            top.set_stroke(WHITE, width=2)
            right_f = Polygon(
                front.get_corner(UR), front.get_corner(DR),
                front.get_corner(DR) + RIGHT * dx + UP * dy,
                front.get_corner(UR) + RIGHT * dx + UP * dy,
            )
            right_f.set_fill(interpolate_color(color, BLACK, 0.2),
                             opacity=0.85)
            right_f.set_stroke(WHITE, width=2)
            return VGroup(front, lines, top, right_f)

        # ── plain cuboid (no grid) for real-network section ──
        def plain_cuboid(h, w, d, color, pos=ORIGIN, cs=0.04,
                         depth_scale=0.4):
            fw, fh = w * cs, h * cs
            front = Rectangle(width=fw, height=fh)
            front.set_fill(color, opacity=0.85)
            front.set_stroke(WHITE, width=2)
            front.move_to(pos)
            dx = min(d, 30) * cs * depth_scale
            dy = min(d, 30) * cs * depth_scale * 0.6
            top = Polygon(
                front.get_corner(UL), front.get_corner(UR),
                front.get_corner(UR) + RIGHT * dx + UP * dy,
                front.get_corner(UL) + RIGHT * dx + UP * dy,
            )
            top.set_fill(interpolate_color(color, WHITE, 0.3), opacity=0.85)
            top.set_stroke(WHITE, width=2)
            right_f = Polygon(
                front.get_corner(UR), front.get_corner(DR),
                front.get_corner(DR) + RIGHT * dx + UP * dy,
                front.get_corner(UR) + RIGHT * dx + UP * dy,
            )
            right_f.set_fill(interpolate_color(color, BLACK, 0.2),
                             opacity=0.85)
            right_f.set_stroke(WHITE, width=2)
            return VGroup(front, top, right_f)

        # ── TITLE ────────────────────────────────────────────
        title = Text("Standard Convolution", font_size=69, weight=BOLD)
        self.play(Write(title), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(title), run_time=0.5)

        # ══════════════════════════════════════════════════════
        # PART 1 — Single filter sliding through input
        # ══════════════════════════════════════════════════════
        CS = 0.40

        # Symmetric layout: input left, output right, filter starts center
        inp_pos = LEFT * 3.5 + UP * 0.4
        inp = gridded_cuboid(5, 5, 4, INPUT_CLR, inp_pos, cs=CS)
        inp_lbl = Text("5x5x4", font_size=40,
                        weight=BOLD, color=INPUT_CLR)
        inp_lbl.next_to(inp, DOWN, buff=0.33)
        inp_tag = Text("Input", font_size=34, weight=BOLD, color=GREY_A)
        inp_tag.next_to(inp_lbl, DOWN, buff=0.33)

        self.play(GrowFromCenter(inp), Write(inp_lbl),
                  FadeIn(inp_tag), run_time=0.8)
        self.wait(0.4)


        # Filter — centered, same Y
        filt_start = UP * 0.4
        filt = gridded_cuboid(3, 3, 4, FILTER_CLR, filt_start, cs=CS)
        filt.set_z_index(10)
        filt_lbl = Text("3x3x4", font_size=40,
                         weight=BOLD, color=FILTER_CLR)
        filt_lbl.next_to(filt, DOWN, buff=0.33)
        filt_tag = Text("Filter", font_size=34, weight=BOLD, color=GREY_A)
        filt_tag.next_to(filt_lbl, DOWN, buff=0.33)

        self.play(FadeIn(filt, shift=LEFT * 0.5),
                  Write(filt_lbl), FadeIn(filt_tag), run_time=0.8)

        depth_note = Text("Filter depth = Input channels = 4",
                          font_size=44, weight=BOLD, color=YELLOW)
        depth_note.to_edge(UP, buff=0.5).shift(DOWN*0.47)
        self.play(FadeIn(depth_note), run_time=0.4)
        self.wait(0.8)
        self.play(FadeOut(depth_note), run_time=0.3)

        # Output grid — right side
        OCS = 0.40
        out_pos = RIGHT * 3.5 + UP * 0.4
        out_cells = VGroup()
        for r in range(3):
            for c in range(3):
                sq = Square(side_length=OCS)
                sq.set_fill(BLACK, opacity=0.3)
                sq.set_stroke(WHITE, width=1.5)
                sq.move_to(out_pos + RIGHT * (c - 1) * OCS
                           + DOWN * (r - 1) * OCS)
                out_cells.add(sq)
        out_lbl = Text("3x3", font_size=32,
                        weight=BOLD, color=OUTPUT_CLR)
        out_lbl.next_to(out_cells, DOWN, buff=0.399)
        out_tag = Text("Output", font_size=34, weight=BOLD, color=GREY_A)
        out_tag.next_to(out_lbl, DOWN, buff=0.33)

        self.play(FadeIn(out_cells), Write(out_lbl),
                  FadeIn(out_tag), self.camera.frame.animate.scale(0.8),run_time=0.6)


        # Make input translucent
        inp_top_c = interpolate_color(INPUT_CLR, WHITE, 0.3)
        inp_side_c = interpolate_color(INPUT_CLR, BLACK, 0.2)

        self.play(
            inp[0].animate.set_fill(INPUT_CLR, opacity=0.20),
            inp[1].animate.set_stroke(opacity=0.15),
            inp[2].animate.set_fill(inp_top_c, opacity=0.20),
            inp[3].animate.set_fill(inp_side_c, opacity=0.20),
            run_time=0.5,
        )

        # Slide filter into input — TransformFromCopy to output
        front_off = filt.get_center() - filt[0].get_center()

        def filt_target(r, c):
            fx = inp_pos[0] + (c - 1) * CS
            fy = inp_pos[1] + (1 - r) * CS
            return np.array([fx, fy, 0.0]) + front_off

        self.play(
            filt.animate.move_to(filt_target(0, 0)),
            FadeOut(filt_lbl), FadeOut(filt_tag),
            run_time=0.8,
        )

        idx = 0
        for r in range(3):
            for c in range(3):
                if idx > 0:
                    self.play(
                        filt.animate.move_to(filt_target(r, c)),
                        run_time=0.28 if idx < 4 else 0.16,
                    )
                # TransformFromCopy: copy of filter flies to output cell
                self.remove(out_cells[idx])
                out_cells[idx].set_fill(OUTPUT_CLR, opacity=0.85)
                self.play(
                    TransformFromCopy(filt, out_cells[idx]),
                    run_time=0.25 if idx < 4 else 0.14,
                )
                if idx == 0:
                    pass
                idx += 1

        # Restore input
        self.play(FadeOut(filt), run_time=0.4)
        self.play(
            inp[0].animate.set_fill(INPUT_CLR, opacity=0.85),
            inp[1].animate.set_stroke(opacity=0.5),
            inp[2].animate.set_fill(inp_top_c, opacity=0.85),
            inp[3].animate.set_fill(inp_side_c, opacity=0.85),
            run_time=0.4,
        )

        self.play(
            VGroup(out_cells, out_lbl, out_tag).animate.shift(LEFT),
            VGroup(inp, inp_lbl, inp_tag).animate.shift(RIGHT*0.99)
        )

        self.wait(2)


        # ══════════════════════════════════════════════════════
        # PART 2 — Multiple filters + FLOPs with braces
        # ══════════════════════════════════════════════════════
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        self.camera.frame.shift(UP*0.68).scale(1.09)

        Y_ROW = 1.5

        # Input at -5, filters centered, output at +5 — filters IN BETWEEN
        inp2 = gridded_cuboid(5, 5, 4, INPUT_CLR,
                               np.array([-5.0, Y_ROW, 0]), cs=0.22)
        inp2.shift(RIGHT*1.73)
        inp2_lbl = Text("5 x 5 x 4", font_size=30, weight=BOLD,
                          color=INPUT_CLR)
        inp2_lbl.next_to(inp2, DOWN, buff=0.22)

        # 5 filters stacked vertically — centered between input and output
        f_cols = ["#E74C3C", "#E91E63", "#FF5722", "#FF9800", "#795548"]
        fstack = VGroup()
        for i in range(5):
            fc = gridded_cuboid(3, 3, 4, f_cols[i], ORIGIN, cs=0.15)
            fstack.add(fc)
        fstack.arrange(DOWN, buff=0.22)
        fstack.move_to(np.array([0.0, Y_ROW, 0]))
        for i, fc in enumerate(fstack):
            fc.set_z_index(5 - i)
        fstack_lbl = Text("(3 x 3 x 4 each)", font_size=22,
                           weight=BOLD, color=FILTER_CLR)
        fstack_lbl.next_to(fstack, DOWN, buff=0.22)

        # Output cuboid at +5
        out2 = gridded_cuboid(3, 3, 5, OUTPUT_CLR,
                               np.array([5.0, Y_ROW, 0]), cs=0.30)
        out2.shift(LEFT*1.89)
        out2_lbl = Text("3 x 3 x 5", font_size=30, weight=BOLD,
                          color=OUTPUT_CLR)
        out2_lbl.next_to(out2, DOWN, buff=0.22)

        # Animate all three together
        self.play(
            GrowFromCenter(inp2), Write(inp2_lbl), 
            run_time=0.7,
        )
        self.play(
            LaggedStart(*[GrowFromCenter(f) for f in fstack],
                         lag_ratio=0.06),
            Write(fstack_lbl),
            run_time=0.9,
        )
        self.play(
            GrowFromCenter(out2), Write(out2_lbl), 
            run_time=0.7,
        )

        self.wait(2)


        # ── FLOPs with labeled braces ────────────────────────
        BY = -1.5

        t_fs = Text("3 x 3 x 4", font_size=28, weight=BOLD, color=FILTER_CLR)
        t_x1 = Text("x", font_size=26, color=GREY_A)
        t_os = Text("3 x 3", font_size=28, weight=BOLD, color=OUTPUT_CLR)
        t_x2 = Text("x", font_size=26, color=GREY_A)
        t_nf = Text("5", font_size=28, weight=BOLD, color=ACCENT_CLR)

        mul_row = VGroup(t_fs, t_x1, t_os, t_x2, t_nf)
        mul_row.arrange(RIGHT, buff=0.35)
        mul_row.move_to(np.array([0, BY, 0])).shift(LEFT*0.5)

        br_fs = Brace(t_fs, DOWN, buff=0.1)
        br_fs.set_color(FILTER_CLR)
        br_fs_lbl = Text("Filter Size", font_size=24,
                          weight=BOLD, color=FILTER_CLR)
        br_fs_lbl.next_to(br_fs, DOWN, buff=0.08)

        br_os = Brace(t_os, DOWN, buff=0.1)
        br_os.set_color(OUTPUT_CLR)
        br_os_lbl = Text("Output Size", font_size=24,
                          weight=BOLD, color=OUTPUT_CLR)
        br_os_lbl.next_to(br_os, DOWN, buff=0.08)

        br_nf = Brace(t_nf, RIGHT, buff=0.1)
        br_nf.set_color(ACCENT_CLR)
        br_nf_lbl = Text("No. of Filters", font_size=22,
                          weight=BOLD, color=ACCENT_CLR)
        br_nf_lbl.next_to(br_nf, RIGHT, buff=0.08)

        # TransformFromCopy from labels to numbers
        self.play(TransformFromCopy(fstack_lbl, t_fs), run_time=0.7)
        self.play(FadeIn(t_x1), run_time=0.15)
        self.play(TransformFromCopy(out2_lbl, t_os), run_time=0.7)
        self.play(FadeIn(t_x2), run_time=0.15)
        self.play(TransformFromCopy(fstack_lbl, t_nf), run_time=0.7)

        self.play(
            GrowFromCenter(br_fs), FadeIn(br_fs_lbl),
            GrowFromCenter(br_os), FadeIn(br_os_lbl),
            GrowFromCenter(br_nf), FadeIn(br_nf_lbl),
            run_time=0.6,
        )
        self.wait(1.5)

        # Total
        total = Text("1,620", font_size=50,
                      weight=BOLD, color="#F1C40F").move_to(VGroup(t_x1, t_x2, t_fs, t_os, t_nf)).shift(DOWN*0.44)
        self.play(ReplacementTransform(VGroup(t_x1, t_x2, t_fs), total), 
        FadeOut(VGroup(br_fs, br_os, br_nf, br_fs_lbl, br_os_lbl, br_nf_lbl, t_os, t_nf) ,run_time=0.7))
        
        self.wait(1.3)



        # ══════════════════════════════════════════════════════
        # PART 3 — Real networks (deep plain cuboids, no grids)
        # ══════════════════════════════════════════════════════
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        self.camera.frame.set_height(9).move_to(DOWN * 0.3)

        real_title = Text("In Real Networks...", font_size=60,
                           weight=BOLD, color=GREY_A)
        real_title.to_edge(UP, buff=0.5).shift(DOWN*0.3)
        self.play(Write(real_title), run_time=0.7)

        # Deep cuboids — no grids, no dimension braces
        real_inp = plain_cuboid(15, 15, 25, INPUT_CLR,
                                 LEFT * 3.5 + UP * 0.3, cs=0.09,
                                 depth_scale=0.55).shift(DOWN*0.34+LEFT*0.7)
        real_inp_lbl = Text("56x56x256", font_size=38,
                             weight=BOLD, color=INPUT_CLR)
        real_inp_lbl.next_to(real_inp, DOWN, buff=0.45)

        real_filt_lbl = Text("128 Filters", font_size=38,
                              weight=BOLD, color=FILTER_CLR)
        real_filt_sub = Text("(3x3x256 each)", font_size=32,
                              weight=BOLD, color=FILTER_CLR)
        real_filt_group = VGroup(real_filt_lbl, real_filt_sub)
        real_filt_group.arrange(DOWN, buff=0.45)
        real_filt_group.next_to(real_inp, RIGHT, buff=0.65)

        real_out = plain_cuboid(14, 14, 15, OUTPUT_CLR,
                                 RIGHT * 3.5 + UP * 0.3, cs=0.09,
                                 depth_scale=0.55)
        real_out_lbl = Text("54x54x128", font_size=38,
                             weight=BOLD, color=OUTPUT_CLR)
        real_out_lbl.next_to(real_out, DOWN, buff=0.45)

        self.play(
            GrowFromCenter(real_inp), Write(real_inp_lbl),
            run_time=0.7,
        )
        self.play(
            Write(real_filt_lbl), FadeIn(real_filt_sub),
            run_time=0.6,
        )
        self.play(
            GrowFromCenter(real_out), Write(real_out_lbl),
            run_time=0.7,
        )
        self.wait(1.5)


        # TransformFromCopy -> FLOPs
        real_flops = Text(
            "~ 860 Million",
            font_size=70, weight=BOLD, color="#E74C3C",
        )
        real_flops.next_to(
            VGroup(real_inp, real_out), DOWN, buff=1.0
        ).shift(DOWN*0.48)

        self.play(
            ShowCreation(real_flops),
            run_time=1.0,
        )
        self.wait(1.3)

        per_layer = Text(
            "...and this is just ONE layer",
            font_size=50, weight=BOLD, color=GREY_A,
        )
        per_layer.next_to(real_flops, DOWN, buff=0.5)
        self.play(FadeIn(per_layer, shift=UP * 0.15), run_time=0.5)
        self.wait(0.5)

        need = Text(
            "We need a cheaper alternative!",
            font_size=50, weight=BOLD, color=YELLOW,
        ).set_color(YELLOW)
        need.next_to(per_layer, DOWN, buff=0.55)
        self.play(Write(need), self.camera.frame.animate.scale(1.1).shift(DOWN*0.65) ,run_time=0.8)
        self.wait(2)
