"""
Inception Module — Naive (No Bottleneck) Visual Explanation
===========================================================
Run:
    manimgl inception_bottleneck.py NaiveInceptionCost
"""

from manimlib import *
import numpy as np


# ── Color palette ────────────────────────────────────────────────────
INPUT_COLOR   = "#27AE60"
CONV1x1_COLOR = "#F1C40F"
CONV3x3_COLOR = "#9B59B6"
CONV5x5_COLOR = "#2980B9"
POOL_COLOR    = "#E74C3C"
CONCAT_COLOR  = "#E67E22"
CARD_BG       = 0.30

# ── Stack-block geometry ─────────────────────────────────────────────
# Front face fixed at FRONT_W × FRONT_H.
# Depth: dx = sqrt(ch) * DEPTH_MULT  (chosen so dx > FRONT_W always).
#   ch=32  → dx ≈ 1.13  > 1.0  ✓
#   ch=64  → dx ≈ 1.60  > 1.0  ✓
#   ch=128 → dx ≈ 2.26  > 1.0  ✓
FRONT_W    = 1.0
FRONT_H    = 1.0
DEPTH_MULT = 0.20


def stack_iso(ch):
    """(dx, dy) for a block with `ch` channels in the stacked view."""
    dx = (ch ** 0.5) * DEPTH_MULT
    return dx, dx * 0.42


def create_stack_block(ch, color, front_left_x, base_y):
    """
    Cuboid for the stacked-concat view.
    front_left_x  : left edge of the front face
    base_y        : vertical centre of the front face
    No text inside — caller adds labels externally.
    Returns: (VGroup, dx, dy)
    """
    dx, dy = stack_iso(ch)
    fc  = np.array([front_left_x + FRONT_W / 2, base_y, 0.0])
    dv  = np.array([dx, dy, 0.0])

    front = Rectangle(width=FRONT_W, height=FRONT_H)
    front.set_fill(color, opacity=1.0)
    front.set_stroke(WHITE, width=2.0)
    front.move_to(fc)

    top = Polygon(
        front.get_corner(UL),
        front.get_corner(UR),
        front.get_corner(UR) + dv,
        front.get_corner(UL) + dv,
    )
    top.set_fill(interpolate_color(color, WHITE, 0.38), opacity=1.0)
    top.set_stroke(WHITE, width=2.0)

    right_face = Polygon(
        front.get_corner(UR),
        front.get_corner(DR),
        front.get_corner(DR) + dv,
        front.get_corner(UR) + dv,
    )
    right_face.set_fill(interpolate_color(color, BLACK, 0.22), opacity=1.0)
    right_face.set_stroke(WHITE, width=2.0)

    return VGroup(front, top, right_face), dx, dy


# ── Branch helpers ───────────────────────────────────────────────────

def create_3d_cuboid(height, width, depth_ch, color,
                     position=ORIGIN, cell_size=0.04):
    front = Rectangle(width=width * cell_size, height=height * cell_size)
    front.set_fill(color, opacity=1.0)
    front.set_stroke(WHITE, width=1.5)
    front.move_to(position)

    dv_ = (depth_ch ** 0.5) * 5.95
    dx  = dv_ * cell_size * 0.38
    dy  = dv_ * cell_size * 0.24
    dv  = np.array([dx, dy, 0.0])

    top = Polygon(
        front.get_corner(UL), front.get_corner(UR),
        front.get_corner(UR) + dv, front.get_corner(UL) + dv,
    )
    top.set_fill(interpolate_color(color, WHITE, 0.25), opacity=1.0)
    top.set_stroke(WHITE, width=1.5)

    rf = Polygon(
        front.get_corner(UR), front.get_corner(DR),
        front.get_corner(DR) + dv, front.get_corner(UR) + dv,
    )
    rf.set_fill(interpolate_color(color, BLACK, 0.15), opacity=1.0)
    rf.set_stroke(WHITE, width=1.5)

    return VGroup(front, top, rf)


def make_conv_card(kernel_text, filter_text, color,
                   width=1.8, height=1.1):
    """Returns (card_group, filter_label).
    card_group contains only the kernel text inside.
    filter_label is positioned separately below the card by the caller.
    """
    card = RoundedRectangle(width=width, height=height, corner_radius=0.12)
    card.set_fill(color, opacity=CARD_BG)
    card.set_stroke(color, width=3.0)

    # Kernel label — larger and bold, centred inside the card
    kern_lbl = Text(kernel_text, font_size=32, weight=BOLD)
    kern_lbl.set_color(WHITE)
    kern_lbl.move_to(card.get_center())

    # Filter label — caller places this BELOW the card
    filt_lbl = Text(filter_text, font_size=32, weight=BOLD)
    filt_lbl.set_color(interpolate_color(WHITE, color, 0.25))

    return VGroup(card, kern_lbl), filt_lbl


def straight_arrow(start_obj, end_obj, y_pos, color=WHITE):
    sx = start_obj.get_right()[0] + 0.08
    ex = end_obj.get_left()[0] - 0.08
    if ex - sx < 0.15:
        ex = sx + 0.15
    arr = Arrow(np.array([sx, y_pos, 0]),
                np.array([ex, y_pos, 0]),
                buff=0, stroke_width=3)
    arr.set_color(color)
    arr.set_z_index(-1)
    return arr


def make_arrow(start_pt, end_pt, color, thickness=3.0):
    arr = Arrow(start_pt, end_pt, buff=0,
                fill_color=color, thickness=thickness)
    arr.set_z_index(-1)
    return arr


def make_vert_line(start_pt, end_pt, color):
    vl = Line(start_pt, end_pt, stroke_color=color, stroke_width=2.5)
    vl.set_z_index(-1)
    return vl


# ====================================================================
#  Naive Inception — No Bottlenecks
# ====================================================================

class NaiveInceptionCost(Scene):

    def construct(self):
        # ── Layout constants ──────────────────────────────────────
        ROW_Y   = [3.8, 0.8, -1.8, -5.0]
        INPUT_X = -6.0
        SPINE_X = -3.0
        CONV_X  = -1.2
        OUT_X   =  2.5
        CELL    =  0.04

        # ─────────────────────────────────────────────────────────
        # CAMERA: Set manually OUTSIDE the loop.
        # Wide enough to keep input block visible on the left while
        # the camera pans vertically to each branch row.
        # frame_width=17 gives a good horizontal span; centre starts
        # at the midpoint between input and output columns.
        # ─────────────────────────────────────────────────────────
        FRAME_W  = 17.0          # fixed horizontal width throughout
        CAM_MID_X = (INPUT_X + OUT_X) / 2 + 0.5   # ≈ −1.5

        # ── Input cuboid ─────────────────────────────────────────
        input_pos   = np.array([INPUT_X, 0, 0])
        input_block = create_3d_cuboid(32, 32, 128, INPUT_COLOR,
                                       input_pos, cell_size=CELL)
        input_label = Text("32 x 32 x 128", font_size=30, weight=BOLD)
        input_label.next_to(input_block, DOWN, buff=0.4)

        self.camera.frame.shift(LEFT * 4).scale(0.85)

        self.play(GrowFromCenter(input_block), Write(input_label), run_time=1.0)
        self.wait(1.5)


        # Arrow from input block rightward to the spine
        input_connector = make_arrow(
            np.array([input_block.get_right()[0] + 0.05, 0, 0]),
            np.array([SPINE_X, 0, 0]),
            WHITE, thickness=3.0
        )
        self.play(GrowArrow(input_connector), run_time=0.5)
        self.wait(0.3)

        # ── Branch definitions ───────────────────────────────────
        branch_defs = [
            ("1x1",      "32 filters", CONV1x1_COLOR,  32,  32, 1.8),
            ("3x3",      "64 filters", CONV3x3_COLOR,  64,  64, 1.8),
            ("5x5",      "32 filters", CONV5x5_COLOR,  32,  32, 1.8),
            ("3x3 Pool", "same",       POOL_COLOR,    128, 128, 2.4),
        ]

        output_cuboids = []
        output_labels  = []
        arr2_list      = []
        extra_mobs     = []   # kept for fade-out at concat stage

        self.play(self.camera.frame.animate.scale(1.1))
        # ─────────────────────────────────────────────────────────
        # Per-branch animation.
        # Camera ONLY moves vertically (Y) to each branch row.
        # X stays fixed at CAM_MID_X so input is always visible left.
        # ─────────────────────────────────────────────────────────
        for i, (kern_lbl, filt_lbl, conv_col, filt, out_ch, card_w) in enumerate(branch_defs):
            y = ROW_Y[i]

            # ── 1. Pan camera between input (y=0) and branch row ─
            # Move to the midpoint so both input block and the
            # current branch's filter+output stay in frame.
            self.play(
                self.camera.frame.animate.move_to(
                    np.array([CAM_MID_X, y / 2 - (0.8 if i == 3 else 0), 0])
                ),
                run_time=0.65
            )

            # ── 2. Spine vertical line from mid-point to branch y ─
            # Branches 0,1,2 all start from y=0 (where input arrow lands).
            # Branch 3 (red/pool) continues from the previous branch's y.
            spine_top = np.array([SPINE_X, ROW_Y[i - 1] if i == 3 else 0, 0])
            spine_bot = np.array([SPINE_X, y, 0])
            vl = make_vert_line(spine_top, spine_bot, conv_col)
            self.play(ShowCreation(vl), run_time=0.30)

            # ── 3. Horizontal arrow from spine → filter card ──────
            arr1 = make_arrow(
                np.array([SPINE_X, y, 0]),
                np.array([CONV_X - card_w / 2 - 0.04, y, 0]),
                conv_col, thickness=3.0
            )
            self.play(GrowArrow(arr1), run_time=0.35)

            # ── 4. Filter card + label ────────────────────────────
            card, filt_label_mob = make_conv_card(kern_lbl, filt_lbl, conv_col,
                                                   width=card_w, height=1.1)
            card.move_to(np.array([CONV_X, y, 0]))
            filt_label_mob.next_to(card, DOWN, buff=0.28)

            self.play(
                FadeIn(card, scale=0.85),
                FadeIn(filt_label_mob, shift=UP * 0.1),
                run_time=0.50
            )

            # ── 5. Arrow from card → output cuboid ───────────────
            out_pos   = np.array([OUT_X, y, 0])
            out_block = create_3d_cuboid(32, 32, out_ch, conv_col,
                                         out_pos, cell_size=CELL)
            out_lbl   = Text(f"32 x 32 x {out_ch}", font_size=28,
                             weight=BOLD, color=conv_col)
            out_lbl.next_to(out_block, DOWN, buff=0.4)

            arr2 = straight_arrow(card, out_block, y, conv_col)
            self.play(GrowArrow(arr2), run_time=0.35)

            # ── 6. Output cuboid ──────────────────────────────────
            self.play(
                GrowFromCenter(out_block),
                Write(out_lbl),
                run_time=0.70
            )
            self.wait(0.30)

            # Collect for later use
            output_cuboids.append(out_block)
            output_labels.append(out_lbl)
            arr2_list.append(arr2)
            extra_mobs += [vl, card, filt_label_mob, arr1, arr2]

        self.wait(0.5)


        self.play(self.camera.frame.animate.scale(1.67).shift(RIGHT*3.45+UP*2.51))

        self.camera.frame.save_state()


        # ════════════════════════════════════════════════════════════
        #  STACKED 3-D CONCAT
        #
        #  The four branch output cuboids TRANSFORM & FLY into a
        #  proper 3-D stacked layout.  No text inside blocks —
        #  only outside labels.
        #
        #  Chain rule:  block i+1 front-left-x = block i front-left-x + dx_i
        #  Because dx_i > FRONT_W for all channel counts, blocks never overlap.
        #
        #  Draw order:  pool (rearmost, z=1) first → 1×1 (frontmost, z=4) last
        # ════════════════════════════════════════════════════════════

        channel_counts = [32,           64,           32,           128]
        stack_colors   = [CONV1x1_COLOR, CONV3x3_COLOR,
                          CONV5x5_COLOR, POOL_COLOR]

        # ── Stacked positions ────────────────────────────────────
        rightmost_x = max(a.get_end()[0] for a in arr2_list)
        STACK_X = rightmost_x + 2.2

        fl_x, b_y = STACK_X, -0.65   # shifted down
        stack_pos = []
        for ch in channel_counts:
            stack_pos.append((fl_x, b_y))
            dx, dy = stack_iso(ch)
            fl_x += dx
            b_y  += dy

        # ── Build target stack blocks (not yet in scene) ─────────
        # z-index per branch (user-specified, frontmost = highest):
        #   index 0  1×1  yellow  z= 1
        #   index 1  3×3  purple  z=-1
        #   index 2  5×5  blue    z=-2
        #   index 3  pool red     z=-4
        Z_INDICES = [1, -1, -2, -4]

        target_blocks = []
        for i, ch in enumerate(channel_counts):
            fl, by = stack_pos[i]
            grp, _, _ = create_stack_block(ch, stack_colors[i], fl, by)
            grp.set_z_index(Z_INDICES[i])
            target_blocks.append(grp)

        # Apply the SAME z-indices to the source output_cuboids RIGHT NOW,
        # before the transform runs.  This prevents Manim from snapping the
        # z-index in a single frame when the ReplacementTransform fires.
        for i, ob in enumerate(output_cuboids):
            ob.set_z_index(Z_INDICES[i])

        # ── Camera framing ───────────────────────────────────────
        total_x  = fl_x - STACK_X + FRONT_W
        stack_mid = np.array([STACK_X + total_x / 2,
                               b_y / 2,
                               0.0])




        # ── Title label ──────────────────────────────────────────
        concat_title = Text("Concatenate",
                            font_size=60, weight=BOLD, color=CONCAT_COLOR)
        concat_title.move_to(stack_mid + UP * (b_y / 2 + FRONT_H / 2 + 0.9))
        self.play(FadeIn(concat_title, shift=DOWN * 0.2), run_time=0.5)

        # ── All 4 blocks transform & fly simultaneously ─────────
        # Running all ReplacementTransforms in ONE self.play() call
        # prevents the per-block "sudden frame jump" that happens when
        # each block pops back from its off-screen branch position
        # before starting to animate.
        self.play(
            *[ReplacementTransform(output_cuboids[i], target_blocks[i])
              for i in range(len(channel_counts))],
            *[FadeOut(ol) for ol in output_labels],
            run_time=1.1
        )

        # ── Total dimension label ────────────────────────────────
        stacked_grp = VGroup(*target_blocks)
        concat_dim  = Text("32  x  32  x  256",
                           font_size=57, weight=BOLD, color=CONCAT_COLOR)
        concat_dim.next_to(stacked_grp, DOWN, buff=1.3)
        self.play(Write(concat_dim), run_time=0.9)

        self.play(FadeOut(concat_title), run_time=0.5)

        self.play(self.camera.frame.animate.restore().scale(0.8).shift(RIGHT*3.4), run_time=0.5)

        self.wait(1.5)

        self.play(self.camera.frame.animate.restore(), run_time=0.85)


        # ════════════════════════════════════════════════════════════
        #  REVERSE: Unstack back to branch outputs
        # ════════════════════════════════════════════════════════════

        # Recreate output cuboids at original branch positions
        rev_cuboids = []
        rev_labels = []
        for i, (kern_t, filt_t, conv_col, filt, out_ch, card_w) in enumerate(branch_defs):
            y = ROW_Y[i]
            out_pos = np.array([OUT_X, y, 0])
            blk = create_3d_cuboid(32, 32, out_ch, conv_col, out_pos, cell_size=CELL)
            blk.set_z_index(Z_INDICES[i])
            lbl = Text(f"32 x 32 x {out_ch}", font_size=28,
                        weight=BOLD, color=conv_col)
            lbl.next_to(blk, DOWN, buff=0.4)
            rev_cuboids.append(blk)
            rev_labels.append(lbl)


        # Reverse transform: stacked → individual branch outputs
        self.play(
            *[ReplacementTransform(target_blocks[i], rev_cuboids[i])
              for i in range(4)],
            FadeOut(concat_dim),
            run_time=1.1,
        )
        self.play(
            *[FadeIn(lbl) for lbl in rev_labels],
            run_time=0.6,
        )
        self.wait(1.5)

        self.play(self.camera.frame.animate.restore().scale(0.7).shift(UP*2))


        # ════════════════════════════════════════════════════════════
        #  COMPUTATIONAL COST — no camera moves, no loops
        # ════════════════════════════════════════════════════════════

        # References to card kernel text and filter labels
        kern_1x1 = extra_mobs[0 * 5 + 1][1]   # Text("1x1")
        kern_3x3 = extra_mobs[1 * 5 + 1][1]   # Text("3x3")
        kern_5x5 = extra_mobs[2 * 5 + 1][1]   # Text("5x5")
        kern_pool = extra_mobs[3 * 5 + 1][1]  # Text("3x3 Pool")

        filt_1x1 = extra_mobs[0 * 5 + 2]      # Text("32 filters")
        filt_3x3 = extra_mobs[1 * 5 + 2]      # Text("64 filters")
        filt_5x5 = extra_mobs[2 * 5 + 2]      # Text("32 filters")
        filt_pool = extra_mobs[3 * 5 + 2]     # Text("same")

        CALC_X = 7.5

        # ── 1x1 Conv: 1*1*128*32*32*32 = 4,194,304 ──────────────
        mult_1x1 = Text(
            "1 x 1 x 128 x 32 x 32 x 32",
            font_size=25, color=CONV1x1_COLOR, weight=BOLD
        )
        mult_1x1.next_to(rev_cuboids[0], RIGHT, buff=0.58)

        self.play(
            TransformFromCopy(kern_1x1, mult_1x1[:7]),
            TransformFromCopy(rev_labels[0], mult_1x1[7:]),
            run_time=0.9,
        )

        rect = SurroundingRectangle(mult_1x1, color="#ff0000", ).scale(1.08)
        self.play(ShowCreation(rect), self.camera.frame.animate.scale(0.8).shift(UP*1.6+RIGHT*2),run_time=0.5)
        self.wait(2)


        result_1x1 = Text(
            "4,194,304", font_size=50, weight=BOLD, color=CONV1x1_COLOR,
        ).set_color(CONV1x1_COLOR)
        result_1x1.move_to(mult_1x1.get_center())

        self.play(FadeOut(rect), ReplacementTransform(mult_1x1, result_1x1), run_time=0.6)
        self.wait(1.3)

        self.play(self.camera.frame.animate.scale(1.14).shift(LEFT*1.12+DOWN*1.4))


        # ── 3x3 Conv: 3*3*128*64*32*32 = 75,497,472 ─────────────
        mult_3x3 = Text(
            "3 x 3 x 128 x 32 x 32 x 64",
            font_size=25, color=CONV3x3_COLOR, weight=BOLD
        )
        mult_3x3.next_to(rev_cuboids[1], RIGHT, buff=0.58)

        self.play(
            TransformFromCopy(kern_3x3, mult_3x3[:7]),
            TransformFromCopy(rev_labels[1], mult_3x3[7:]),
            run_time=0.9,
        )

        rect = SurroundingRectangle(mult_3x3, color="#ff0000", ).scale(1.08)
        self.play(ShowCreation(rect), self.camera.frame.animate.scale(0.88).shift(UP*0.1+RIGHT*2),run_time=0.5)
        self.wait(2)


        result_3x3 = Text(
            "75,497,472", font_size=50, weight=BOLD, color=CONV3x3_COLOR,
        ).set_color(CONV3x3_COLOR)
        result_3x3.move_to(mult_3x3.get_center())


        self.play(FadeOut(rect), ReplacementTransform(mult_3x3, result_3x3), run_time=0.6)
        self.play(self.camera.frame.animate.scale(1.14).shift(LEFT*1.12+DOWN*1.99))
        self.wait(1.3)


        # ── 5x5 Conv: 5*5*128*32*32*32 = 104,857,600 ────────────
        mult_5x5 = Text(
            "5 x 5 x 128 x 32 x 32 x 32",
            font_size=28, color=CONV5x5_COLOR, weight=BOLD
        )
        mult_5x5.next_to(rev_cuboids[2], RIGHT, buff=0.68)

        self.play(
            TransformFromCopy(kern_5x5, mult_5x5[:7]),
            TransformFromCopy(rev_labels[2], mult_5x5[7:]),
            run_time=0.9,
        )

        rect = SurroundingRectangle(mult_5x5, color="#ff0000", ).scale(1.08)
        self.play(ShowCreation(rect), self.camera.frame.animate.shift(DOWN*1.2),run_time=0.5)
        self.wait(2)


        result_5x5 = Text(
            "104,857,600", font_size=50, weight=BOLD, color=CONV5x5_COLOR,
        ).set_color(BLUE_B)
        result_5x5.move_to(mult_5x5.get_center())

        self.play(FadeOut(rect), ReplacementTransform(mult_5x5, result_5x5), run_time=0.6)
        self.wait(0.3)

        self.play(self.camera.frame.animate.scale(1.14).shift(LEFT*1.12+DOWN*1.99))

        # ── 3x3 Pool: 0 ─────────────────────────────────────────
        result_pool = Text(
            "0", font_size=60, weight=BOLD, color=POOL_COLOR,
        ).set_color(RED_B)
        result_pool.next_to(rev_cuboids[3], RIGHT, buff=2.793)

        self.play(
            TransformFromCopy(kern_pool, result_pool),
            run_time=0.8,
        )
        self.wait(1.3)

        self.play(self.camera.frame.animate.restore())

        # ── Merge all 4 → single total ───────────────────────────
        all_vg = VGroup(result_1x1, result_3x3, result_5x5, result_pool)

        total_text = Text(
            "~ 185 Million FLOPs",
            font_size=52, weight=BOLD, color=CONCAT_COLOR,
        )
        total_text.move_to(all_vg.get_center()).shift(RIGHT*1.84)

        self.play(
            ReplacementTransform(all_vg, total_text),
            self.camera.frame.animate.shift(RIGHT*0.8),
            run_time=1.2,
        )

        rect = SurroundingRectangle(total_text, color="#00ff00", buff=0.2).scale(1.07)
        self.play(ShowCreation(rect), run_time=0.5)
        self.wait(2.5)

        self.embed()


class BottleneckExplicitCalc(Scene):


    def construct(self):
        CELL   = 0.04
        NAIVE_Y = 2.5
        BTN_Y   = -2.2

        self.camera.frame.shift(UP*2.3)


        # ══════════════════════════════════════════════════════════
        #  TOP ROW — Naive 5×5  (show directly — no verbose calc)
        # ══════════════════════════════════════════════════════════

        inp_n = create_3d_cuboid(28, 28, 128, INPUT_COLOR,
                                  np.array([-5.5, NAIVE_Y, 0]), CELL)
        inp_n_lbl = Text("32x32x128", font_size=30, weight=BOLD)
        inp_n_lbl.next_to(inp_n, DOWN, buff=0.3)
        self.play(GrowFromCenter(inp_n), Write(inp_n_lbl), run_time=0.65)


        card_n, flbl_n = make_conv_card("5x5", "32 filters",
                                         CONV5x5_COLOR, 1.8, 1.0)
        card_n.move_to(np.array([-1.5, NAIVE_Y, 0]))
        flbl_n.next_to(card_n, DOWN, buff=0.25)
        a1_n = straight_arrow(inp_n, card_n, NAIVE_Y, CONV5x5_COLOR)
        self.play(GrowArrow(a1_n), run_time=0.3)
        self.play(FadeIn(card_n, scale=0.85),
                  FadeIn(flbl_n, shift=UP * 0.1), run_time=0.45)

        out_n = create_3d_cuboid(28, 28, 32, CONV5x5_COLOR,
                                  np.array([2.2, NAIVE_Y, 0]), CELL)
        out_n_lbl = Text("32x32x32", font_size=30, weight=BOLD,
                          color=CONV5x5_COLOR)
        out_n_lbl.next_to(out_n, DOWN, buff=0.3)
        a2_n = straight_arrow(card_n, out_n, NAIVE_Y, CONV5x5_COLOR)
        self.play(GrowArrow(a2_n), run_time=0.3)
        self.play(GrowFromCenter(out_n), Write(out_n_lbl), run_time=0.55)

        # ── Direct FLOPs reveal (no multiplication shown) ────────
        result_n = Text("~ 105 M", font_size=52, weight=BOLD)
        result_n.set_color_by_gradient("#FF6B6B", "#FF0000")
        result_n.move_to(np.array([6.5, NAIVE_Y, 0]))

        glow_n = SurroundingRectangle(result_n, color="#FF4444", buff=0.25)
        glow_n.set_stroke(width=4)
        glow_n.set_fill("#FF0000", opacity=0.10)

        self.play(FadeIn(result_n, scale=0.6), self.camera.frame.animate.shift(RIGHT).scale(1.2) ,run_time=0.55)
        self.play(ShowCreation(glow_n), run_time=0.4)
        self.wait(1.6)

        self.camera.frame.save_state()

        # ══════════════════════════════════════════════════════════
        #  DIVIDER — thin horizontal separator
        # ══════════════════════════════════════════════════════════
        divider = Line(
            np.array([-500.0, 0.2, 0]),
            np.array([ 500.0, 0.2, 0]),
            stroke_color="#444444", stroke_width=1.5)
        self.play(ShowCreation(divider), run_time=0.3)
        self.play(self.camera.frame.animate.shift(DOWN*2.66+LEFT))

        # ══════════════════════════════════════════════════════════
        #  BOTTOM ROW — 1×1 Bottleneck → 5×5  (tighter card padding)
        # ══════════════════════════════════════════════════════════

        inp_b = create_3d_cuboid(28, 28, 128, INPUT_COLOR,
                                  np.array([-7.0, BTN_Y, 0]), CELL)
        inp_b_lbl = Text("32x32x128", font_size=30, weight=BOLD)
        inp_b_lbl.next_to(inp_b, DOWN, buff=0.45)
        self.play(GrowFromCenter(inp_b), Write(inp_b_lbl), run_time=0.6)
        self.wait(2)

        # 1×1 card
        card_b1, flbl_b1 = make_conv_card("1x1", "16 filters",
                                            CONV1x1_COLOR, 1.2, 1.0)
        card_b1.move_to(np.array([-3.5, BTN_Y, 0]))
        flbl_b1.next_to(card_b1, DOWN, buff=0.55)
        a1_b = straight_arrow(inp_b, card_b1, BTN_Y, CONV1x1_COLOR)
        self.play(GrowArrow(a1_b), run_time=0.25)
        self.play(FadeIn(card_b1, scale=0.85),
                  FadeIn(flbl_b1, shift=UP * 0.1), run_time=0.4)

        # "Bottleneck" label — plain yellow text below "16 filters"
        btn_card_label = Text("Bottleneck", font_size=30, weight=BOLD,
                               color=YELLOW).set_color(YELLOW)
        btn_card_label.next_to(flbl_b1, DOWN, buff=0.36)
        self.play(FadeIn(btn_card_label, scale=0.85), run_time=0.35)
        self.wait(2)

        # Compressed intermediate cuboid
        mid_b = create_3d_cuboid(28, 28, 16, CONV1x1_COLOR,
                                  np.array([-1, BTN_Y, 0]), CELL)
        mid_b_lbl = Text("32x32x16", font_size=28, weight=BOLD,
                          color=CONV1x1_COLOR)
        mid_b_lbl.next_to(mid_b, DOWN, buff=0.5)
        a2_b = straight_arrow(card_b1, mid_b, BTN_Y, CONV1x1_COLOR)
        self.play(GrowArrow(a2_b), run_time=0.25)
        self.play(GrowFromCenter(mid_b), Write(mid_b_lbl), run_time=0.5)
        self.wait(2)


        # FLOPs for 1×1 stage — direct number above
        flops_b1 = Text("2,097,152", font_size=26, weight=BOLD,
                         color=CONV1x1_COLOR).scale(1.5)
        flops_b1.move_to(np.array([-2.35, BTN_Y + 1.85, 0]))
        self.play(FadeIn(flops_b1, shift=DOWN * 0.12), run_time=0.3)
        self.wait(2)

        # 5×5 card
        card_b2, flbl_b2 = make_conv_card("5x5", "32 filters",
                                            CONV5x5_COLOR, 1.2, 1.0)
        card_b2.move_to(np.array([1.8, BTN_Y, 0]))
        flbl_b2.next_to(card_b2, DOWN, buff=0.55)
        a3_b = straight_arrow(mid_b, card_b2, BTN_Y, CONV5x5_COLOR)
        self.play(GrowArrow(a3_b), run_time=0.25)
        self.play(FadeIn(card_b2, scale=0.85),
                  FadeIn(flbl_b2, shift=UP * 0.1), run_time=0.4)
        self.wait(2)

        out_b = create_3d_cuboid(28, 28, 32, CONV5x5_COLOR,
                                  np.array([4.6, BTN_Y, 0]), CELL)
        out_b_lbl = Text("32x32x32", font_size=30, weight=BOLD,
                          color=CONV5x5_COLOR)
        out_b_lbl.next_to(out_b, DOWN, buff=0.5)
        a4_b = straight_arrow(card_b2, out_b, BTN_Y, CONV5x5_COLOR)
        self.play(GrowArrow(a4_b), run_time=0.25)
        self.play(GrowFromCenter(out_b), Write(out_b_lbl), run_time=0.55)
        self.wait(2)

        # FLOPs for 5×5 stage — direct number above
        flops_b2 = Text("13,107,200", font_size=26, weight=BOLD,
                          color=CONV5x5_COLOR).scale(1.5)
        flops_b2.move_to(np.array([3.3, BTN_Y + 1.85, 0]))
        self.play(FadeIn(flops_b2, shift=DOWN * 0.12), run_time=0.3)
        self.wait(2)

        # Plus sign scaled up
        plus_sign = Text("+", font_size=30, weight=BOLD, color=WHITE).scale(2)
        plus_sign.move_to(np.array([0.49, BTN_Y + 1.85, 0]))
        self.play(FadeIn(plus_sign, scale=0.8), run_time=0.2)

        # Sum underline
        underline = Line(
            np.array([flops_b1.get_left()[0] - 0.15, BTN_Y + 1.35, 0]),
            np.array([flops_b2.get_right()[0] + 0.15, BTN_Y + 1.35, 0]),
            stroke_color="#AAAAAA", stroke_width=2)
        self.play(ShowCreation(underline), run_time=0.3)
        self.wait(2)

        # ── Direct total FLOPs for bottleneck (compact) ─────────────
        result_b = Text("~ 15.2 M", font_size=52, weight=BOLD)
        result_b.set_color_by_gradient("#55FF77", "#00CC44")
        result_b.move_to(np.array([8.44, BTN_Y, 0]))

        glow_b = SurroundingRectangle(result_b, color="#00FF55", buff=0.25)
        glow_b.set_stroke(width=4)
        glow_b.set_fill("#00AA33", opacity=0.10)

        self.play(FadeIn(result_b, scale=0.6), self.camera.frame.animate.scale(1.14).shift(RIGHT*1.54) ,run_time=0.55)
        self.play(ShowCreation(glow_b), run_time=0.4)
        self.wait(2)

        self.embed()

