"""
Transformers — Attention Is All You Need
=========================================
Scene classes (one per topic, run individually):
    manimgl a.py RNNLimitations -w --hd
    manimgl a.py WordEmbeddings -w --hd
"""

from manimlib import *
import numpy as np


# ── Color palette ────────────────────────────────────────────────────
C_RNN       = "#1ABC9C"     # RNN cell teal
C_LSTM      = "#3498DB"     # LSTM cell blue
C_GRU       = "#F39C12"     # GRU cell amber
C_SIGNAL    = "#2ECC71"     # strong signal green
C_HIGHWAY   = "#5DADE2"     # cell state highway blue
C_WORD      = "#A8DADC"     # word/token blue
C_FAIL      = "#FF4444"     # warning red
C_FADE      = "#E74C3C"     # faded signal red
C_SUCCESS   = "#27AE60"     # success green
C_ENC       = "#2980B9"     # encoder blue
C_DEC       = "#27AE60"     # decoder green
C_QUERY     = "#E74C3C"     # query red
C_KEY       = "#F39C12"     # key amber
C_VALUE     = "#3498DB"     # value blue
C_FFN       = "#9B59B6"     # feed-forward purple
C_NORM      = "#1ABC9C"     # add & norm teal
C_POS       = "#F1C40F"     # positional encoding gold
C_EMB       = "#8E44AD"     # embedding purple
C_HEAD1     = "#E74C3C"     # attention head 1
C_HEAD2     = "#3498DB"     # attention head 2
C_HEAD3     = "#2ECC71"     # attention head 3
C_HEAD4     = "#F39C12"     # attention head 4
C_SOFT      = "#D35400"     # softmax orange
C_OUT       = "#F1C40F"     # output gold
C_ATT       = "#FF6B9D"     # attention pink
SOFT_GRAY   = "#95A5A6"     # subtle gray
DARK_BG     = "#1a1a2e"     # dark background


# ── Helper functions ─────────────────────────────────────────────────

def make_cell(pos, col, tex_str, r=0.44, fs=26):
    """Square node with LaTeX label."""
    side = r * 2
    c = RoundedRectangle(width=side, height=side, corner_radius=0.08)
    c.set_fill(col, opacity=0.90)
    c.set_stroke(WHITE, width=2.5)
    c.move_to(pos)
    lb = Tex(tex_str, font_size=fs)
    lb.set_color(WHITE); lb.move_to(pos)
    return VGroup(c, lb)


def make_block(pos, w, h, col, txt, fs=22, opacity=0.88):
    """Rounded rectangle with text label."""
    bx = RoundedRectangle(width=w, height=h, corner_radius=0.12)
    bx.set_fill(col, opacity=opacity)
    bx.set_stroke(WHITE, width=2.0)
    bx.move_to(pos)
    lb = Text(txt, font_size=fs, weight=BOLD)
    lb.set_color(WHITE); lb.move_to(pos)
    return VGroup(bx, lb)


def make_arr(a, b, col, sw=2.5, bf=0.08):
    """Arrow from a to b."""
    ar = Arrow(a, b, buff=bf, stroke_width=sw,
               max_tip_length_to_length_ratio=0.14)
    ar.set_color(col)
    return ar


def make_title(txt, pos, col=WHITE, fs=30):
    """Bold title text."""
    t = Text(txt, font_size=fs, weight=BOLD)
    t.set_color(col); t.move_to(pos)
    return t


def flash_arrow(mob, tw=0.45, rt=0.50):
    """Data-flow flash on an arrow."""
    return ShowPassingFlash(mob.copy().set_color(WHITE),
                           time_width=tw, run_time=rt)



# ═══════════════════════════════════════════════════════════════════
#  SCENE 2 — Word Embeddings  (~3 min, all 2D, multiple analogies)
# ═══════════════════════════════════════════════════════════════════

class WordEmbeddings(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.22)
        frame = self.camera.frame

        # ── Helpers ──────────────────────────────────────────────────
        C_ROYAL = "#F1C40F"    # gold for royalty
        C_MALE  = "#5DADE2"    # blue for male
        C_FEM   = "#FF69B4"    # pink for female
        C_ANIM  = "#58D68D"    # green for animals
        C_WRONG = "#FF4444"    # red for wrong/errors
        C_DIR   = "#F39C12"    # amber for direction arrows
        C_QUEEN = "#9B59B6"    # purple for queen (distinct from woman pink)

        def wcard(text, col=C_WORD, fs=24):
            lb = Text(text, font_size=fs, weight=BOLD)
            lb.set_color(WHITE)
            w = max(lb.get_width() + 0.50, 1.10)
            card = RoundedRectangle(width=w, height=0.62, corner_radius=0.10)
            card.set_fill(col, opacity=0.85)
            card.set_stroke(WHITE, width=1.5)
            lb.move_to(card.get_center())
            return VGroup(card, lb)

        def gdot(pos, col, txt, d=UP, r=0.13, fs=20):
            outer = Circle(radius=r * 2.8)
            outer.set_fill(col, opacity=0.20)
            outer.set_stroke(width=0)
            outer.move_to(pos)
            inner = Circle(radius=r)
            inner.set_fill(col, opacity=1.0)
            inner.set_stroke(WHITE, width=1.5)
            inner.move_to(pos)
            lb = Text(txt, font_size=fs, weight=BOLD)
            lb.set_color(col)
            lb.next_to(inner, d, buff=0.15)
            return VGroup(outer, inner, lb)

        def subtle_grid(xr=(-6, 7), yr=(-4, 5), op=0.10):
            g = VGroup()
            for x in range(*xr):
                sw = 2.0 if x == 0 else 0.5
                ln = Line(np.array([x, yr[0], 0]), np.array([x, yr[1], 0]),
                          stroke_width=sw)
                ln.set_color(WHITE if x == 0 else SOFT_GRAY)
                ln.set_opacity(0.22 if x == 0 else op)
                g.add(ln)
            for y in range(*yr):
                sw = 2.0 if y == 0 else 0.5
                ln = Line(np.array([xr[0], y, 0]), np.array([xr[1], y, 0]),
                          stroke_width=sw)
                ln.set_color(WHITE if y == 0 else SOFT_GRAY)
                ln.set_opacity(0.22 if y == 0 else op)
                g.add(ln)
            return g

        CARD_BG = "#34495E"  # dark slate for card fills
        CARD_H  = 0.62      # FIXED height for ALL word cards everywhere

        # ══════════════════════════════════════════════════════════════
        # PHASE 0 — Tokenization
        # ══════════════════════════════════════════════════════════════
        sub0 = make_title("Tokenization", UP * 3.8, C_POS, fs=42)
        sub0.scale(1.3)
        self.play(Write(sub0), run_time=0.60)
        self.wait(1.0)

        sentence = Text('"The king and the queen rule the kingdom"',
                         font_size=30, weight=BOLD)
        sentence.set_color(WHITE)
        sentence.move_to(UP * 2.2)
        self.play(Write(sentence), run_time=1.20)
        self.wait(1.0)

        tok_note = Text("Tokenizers break text into small pieces",
                         font_size=24, weight=BOLD)
        tok_note.set_color(WHITE)
        tok_note.move_to(UP * 1.0)
        self.play(FadeIn(tok_note), run_time=0.50)
        self.wait(1.0)

        sub_tok_txt = Text(
            '[ "Th", "e", "ki", "ng", "and", "the", "qu", "een", "ru", "le" ... ]',
            font_size=24, weight=BOLD,
        )
        sub_tok_txt.set_color(C_DIR)
        sub_tok_txt.move_to(DOWN * 0.3)
        sub_tok_note = Text("These pieces are not always words!",
                             font_size=24, weight=BOLD)
        sub_tok_note.set_color(WHITE)
        sub_tok_note.move_to(DOWN * 1.4)
        self.play(FadeIn(sub_tok_txt), run_time=0.50)
        self.wait(1.0)
        self.play(FadeIn(sub_tok_note), run_time=0.40)
        self.wait(2.5)

        simplify = Text("For simplicity: 1 word = 1 token",
                          font_size=28, weight=BOLD)
        simplify.scale(1.3)
        simplify.set_color(C_SIGNAL)
        simplify.move_to(ORIGIN)
        self.play(
            FadeOut(sentence), FadeOut(tok_note),
            FadeOut(sub_tok_txt), FadeOut(sub_tok_note),
            FadeIn(simplify),
            run_time=0.50,
        )
        self.wait(2.0)
        self.play(FadeOut(simplify), run_time=0.30)

        # Word cards — use VGroup + arrange for equal spacing
        tok_words = ["The", "king", "and", "the", "queen", "rule", "the", "kingdom"]
        tok_cols = [CARD_BG, C_ROYAL, CARD_BG, CARD_BG, C_FEM,
                    C_MALE, CARD_BG, C_ROYAL]
        cards = VGroup()
        for w, col in zip(tok_words, tok_cols):
            lb = Text(w, font_size=26, weight=BOLD)
            lb.set_color(WHITE)
            bg = RoundedRectangle(width=lb.get_width() + 0.50,
                                  height=0.72, corner_radius=0.10)
            bg.set_fill(col, opacity=0.85)
            bg.set_stroke(WHITE, width=1.5)
            lb.move_to(bg.get_center())
            cards.add(VGroup(bg, lb))
        cards.arrange(RIGHT, buff=0.18)
        cards.move_to(UP * 0.8)

        tok_idxs = []
        for i in range(len(tok_words)):
            idx = Text(str(i), font_size=26, weight=BOLD)
            idx.set_color(WHITE)
            idx.next_to(cards[i], DOWN, buff=0.22)
            tok_idxs.append(idx)

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.18) for c in cards],
                        lag_ratio=0.06, run_time=1.00),
        )
        self.wait(0.80)
        self.play(
            LaggedStart(*[FadeIn(t) for t in tok_idxs],
                        lag_ratio=0.04, run_time=0.60),
        )
        self.wait(1.0)

        pipeline = Text("Text  -->  Tokens  -->  IDs",
                          font_size=34, weight=BOLD)
        pipeline.set_color(WHITE)
        pipeline.move_to(DOWN * 1.5)
        self.play(FadeIn(pipeline), run_time=0.50)
        self.wait(2.5)

        p0 = [sub0, pipeline, *cards, *tok_idxs]
        self.play(*[FadeOut(m) for m in p0], run_time=0.65)
        self.wait(0.80)

        # ══════════════════════════════════════════════════════════════
        # PHASE 1 — One-Hot Encoding
        # ══════════════════════════════════════════════════════════════
        sub1 = make_title("One-Hot Encoding", UP * 3.8, C_SIGNAL, fs=38)
        sub1.scale(1.2)
        self.play(FadeIn(sub1), run_time=0.50)

        sent_lbl = Text('"King loves Queen"', font_size=28, weight=BOLD)
        sent_lbl.set_color(WHITE)
        sent_lbl.move_to(UP * 2.8)
        self.play(Write(sent_lbl), run_time=0.50)
        self.wait(1.0)

        # Vocabulary — sorted ALPHABETICALLY
        vocab_title = Text("Vocabulary:", font_size=24, weight=BOLD)
        vocab_title.set_color(RED_A)
        vocab_title.move_to(UP * 1.9)
        self.play(FadeIn(vocab_title), run_time=0.40)

        words = ["cat", "King", "loves", "Queen", "the"]  # alphabetical
        N = 5
        vocab_row = VGroup()
        for w in words:
            lb = Text(w, font_size=24, weight=BOLD)
            lb.set_color(WHITE)
            bg = RoundedRectangle(width=lb.get_width() + 0.45,
                                  height=CARD_H, corner_radius=0.10)
            bg.set_fill(CARD_BG, opacity=0.85)
            bg.set_stroke(WHITE, width=1.5)
            lb.move_to(bg.get_center())
            vocab_row.add(VGroup(bg, lb))
        vocab_row.arrange(RIGHT, buff=0.18)
        vocab_row.scale(1.15)
        vocab_row.move_to(UP * 1.1)

        vocab_idxs = []
        for i in range(N):
            idx = Text(f"#{i}", font_size=20, weight=BOLD)
            idx.set_color(WHITE)
            idx.next_to(vocab_row[i], DOWN, buff=0.18)
            vocab_idxs.append(idx)

        self.play(
            LaggedStart(*[FadeIn(c) for c in vocab_row],
                        lag_ratio=0.06, run_time=0.60),
        )
        self.play(
            LaggedStart(*[FadeIn(t) for t in vocab_idxs],
                        lag_ratio=0.04, run_time=0.40),
        )
        self.wait(1.5)

        rule = Text(
            "Put a 1 at the position of the current word, 0 everywhere else",
            font_size=22, weight=BOLD,  # already BOLD
        )
        rule.scale(1.25)
        rule.set_color(C_POS)
        rule.move_to(DOWN * 0.2)
        self.play(FadeIn(rule), run_time=0.50)
        self.wait(2.0)

        # One-hot grid: ONLY 3 rows (King, loves, Queen) but 5 columns
        # Build each row as: label = grid_row, then scale + shift the whole thing
        oh_words = ["King", "loves", "Queen"]
        oh_indices = [1, 2, 3]  # positions in alphabetical vocab
        ROW_H = 0.72;  CELL_W = 0.90;  CELL_GAP = 0.12
        GRID_STEP = CELL_W + CELL_GAP

        oh_rows_grp = VGroup()  # will hold all 3 rows
        # Find widest label to make all same width
        LABEL_W = 1.2  # fixed width for all labels
        w_lbls = [];  eq_signs = [];  oh_cells = []
        for ri, (word, one_pos) in enumerate(zip(oh_words, oh_indices)):
            row_grp = VGroup()
            lb = Text(word, font_size=24, weight=BOLD)
            lb.set_color(C_WORD)
            # Wrap in fixed-width container so all labels align
            lb_box = VGroup(lb)
            lb_box.set_width(LABEL_W, stretch=False)
            w_lbls.append(lb_box)
            eq = Tex("=", font_size=26)
            eq.set_color(SOFT_GRAY)
            eq_signs.append(eq)
            row_grp.add(lb_box, eq)
            for j in range(N):
                rect = RoundedRectangle(width=CELL_W, height=ROW_H,
                                         corner_radius=0.06)
                if j == one_pos:
                    rect.set_fill(C_POS, opacity=0.90)
                    rect.set_stroke(C_POS, width=1.5)
                    vt = Text("1", font_size=26, weight=BOLD)
                    vt.set_color(WHITE)
                else:
                    rect.set_fill(DARK_BG, opacity=0.45)
                    rect.set_stroke(SOFT_GRAY, width=0.5)
                    vt = Text("0", font_size=22, weight=BOLD)
                    vt.set_color(SOFT_GRAY)
                cell = VGroup(rect, vt)
                vt.move_to(rect.get_center())
                row_grp.add(cell)
                oh_cells.append(cell)
            # Arrange: label eq cell0 cell1 cell2 cell3 cell4
            row_grp.arrange(RIGHT, buff=0.15)
            oh_rows_grp.add(row_grp)

        oh_rows_grp.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        oh_rows_grp.scale(1.1)
        oh_rows_grp.move_to(DOWN * 2.25)
        oh_rows_grp.shift(DOWN * 0.20)

        for ri in range(3):
            self.play(FadeIn(oh_rows_grp[ri]), run_time=0.50)
        self.wait(3.0)

        # Fade out: one-hot title + "King loves Queen" + vocab stay for transition
        self.play(FadeOut(sub1), FadeOut(sent_lbl), run_time=0.40)

        # Show vocab size note — two separate texts
        vocab_note1 = Text("Real vocabularies might have 10,000+ words",
                            font_size=24, weight=BOLD)
        vocab_note1.scale(1.3)
        vocab_note1.set_color(WHITE)
        vocab_note1.move_to(UP * 3.6)

        vocab_note2 = Text("One-hot is very inefficient!",
                            font_size=24, weight=BOLD)
        vocab_note2.scale(1.3)
        vocab_note2.set_color(C_WRONG)
        vocab_note2.next_to(vocab_note1, DOWN, buff=0.20)

        self.play(FadeIn(vocab_note1), run_time=0.50)
        self.play(FadeIn(vocab_note2), run_time=0.50)
        self.wait(2.5)

        p1 = ([vocab_title, vocab_note1, vocab_note2, rule,
               *vocab_row, *vocab_idxs]
              + [oh_rows_grp])
        self.play(*[FadeOut(m) for m in p1], run_time=0.65)
        self.wait(0.80)

        # ══════════════════════════════════════════════════════════════
        # PHASE 2 — Dense Embedding Table
        # ══════════════════════════════════════════════════════════════
        sub2 = make_title("Word Embeddings", UP * 3.8, C_EMB, fs=36)
        sub2.scale(1.2)
        self.play(Write(sub2), run_time=0.50)
        self.wait(1.0)

        feat_exp = Text("Assign each word a score for different properties:",
                          font_size=28, weight=BOLD)
        feat_exp.set_color(WHITE)
        feat_exp.move_to(UP * 2.6)
        self.play(FadeIn(feat_exp), run_time=0.50)
        self.wait(1.0)

        features = ["Royal", "Gender", "Animal", "Power", "Softness"]
        emb_words = ["King", "loves", "Queen", "the", "cat"]
        vals = [
            [0.9,  0.8,  0.0, 0.95, 0.2],
            [0.0,  0.0,  0.0, 0.10, 0.1],
            [0.9, -0.8,  0.0, 0.90, 0.3],
            [0.0,  0.0,  0.0, 0.05, 0.0],
            [0.0,  0.0,  0.9, 0.10, 0.8],
        ]
        TX0 = -1.5;  TCW = 1.35
        TY0 = 0.4;   TRH = 0.68

        # Column headers — bigger font, more buff above grid
        col_hdrs = []
        for j, feat in enumerate(features):
            hdr = Text(feat, font_size=22, weight=BOLD)
            hdr.set_color(C_POS)
            hdr.move_to(np.array([TX0 + j * TCW, TY0 + 0.65, 0]))
            col_hdrs.append(hdr)
        row_lbls = []
        for i, w in enumerate(emb_words):
            lb = Text(w, font_size=22, weight=BOLD)
            lb.set_color(C_WORD)
            lb.move_to(np.array([TX0 - 1.5, TY0 - i * TRH, 0]))
            row_lbls.append(lb)

        hm_all = [];  hm_rows = []
        for i in range(N):
            row = []
            for j in range(N):
                x = TX0 + j * TCW
                y = TY0 - i * TRH
                val = vals[i][j]
                cell = RoundedRectangle(
                    width=TCW - 0.10, height=TRH - 0.10,
                    corner_radius=0.06,
                )
                intensity = abs(val)
                cell.set_fill(
                    C_SIGNAL if val >= 0 else C_WRONG,
                    opacity=max(0.06, intensity * 0.80),
                )
                cell.set_stroke(WHITE, width=0.8, opacity=0.25)
                cell.move_to(np.array([x, y, 0]))
                vt = Text(f"{val:.1f}", font_size=18, weight=BOLD)
                vt.set_color(WHITE)
                vt.move_to(cell.get_center())
                grp = VGroup(cell, vt)
                row.append(grp);  hm_all.append(grp)
            hm_rows.append(row)

        # Collect entire table into a group, scale up 1.15 and shift up 0.3
        table_grp = VGroup(*col_hdrs, *row_lbls, *hm_all)
        table_grp.scale(1.15)
        table_grp.shift(UP * 0.3)

        self.play(LaggedStart(*[FadeIn(h) for h in col_hdrs],
                  lag_ratio=0.08, run_time=0.50))
        self.wait(0.80)
        for i in range(N):
            self.play(
                FadeIn(row_lbls[i]),
                LaggedStart(*[FadeIn(c) for c in hm_rows[i]],
                            lag_ratio=0.05, run_time=0.30),
                run_time=0.40,
            )
            self.wait(0.25)
        self.wait(1.5)

        # Highlight King
        king_rect = SurroundingRectangle(
            VGroup(row_lbls[0], *hm_rows[0]),
            color=C_EMB, buff=0.08, stroke_width=2.5,
        )
        king_rect.set_fill(C_EMB, opacity=0.12)
        self.play(ShowCreation(king_rect), run_time=0.60)
        self.wait(1.5)

        # Highlight Queen
        queen_rect = SurroundingRectangle(
            VGroup(row_lbls[2], *hm_rows[2]),
            color=C_FEM, buff=0.08, stroke_width=2.5,
        )
        queen_rect.set_fill(C_FEM, opacity=0.10)
        self.play(ShowCreation(queen_rect), run_time=0.60)
        self.wait(2.5)

        # Transform both highlights to Cat row
        cat_rect = SurroundingRectangle(
            VGroup(row_lbls[4], *hm_rows[4]),
            color=C_ANIM, buff=0.08, stroke_width=2.5,
        )
        cat_rect.set_fill(C_ANIM, opacity=0.12)
        self.play(
            Transform(king_rect, cat_rect),
            FadeOut(queen_rect),
            run_time=0.80,
        )
        self.wait(2.0)

        # No compare_lbl — just the green dense text, scaled 1.2
        dense_lbl = Text("Dense, meaningful vectors instead of sparse one-hot",
                          font_size=24, weight=BOLD)
        dense_lbl.scale(1.2)
        dense_lbl.set_color(C_SIGNAL)
        dense_lbl.move_to(DOWN * 3.6)
        self.play(FadeIn(dense_lbl), run_time=0.50)
        self.wait(2.5)

        p2 = ([sub2, feat_exp, king_rect, queen_rect, dense_lbl]
              + col_hdrs + row_lbls + hm_all)
        self.play(*[FadeOut(m) for m in p2], run_time=0.65)
        self.wait(0.80)

        # ══════════════════════════════════════════════════════════════
        # PHASE 3 — 2D Embedding Space + Training (NO camera zoom)
        # ══════════════════════════════════════════════════════════════
        grid = subtle_grid(xr=(-8, 9), yr=(-5, 6))
        self.play(FadeIn(grid), run_time=0.50)
        self.wait(0.80)

        wd = [
            (np.array([-2.1, 2.2, 0]),  np.array([ 3.5,-2.5, 0]), "King",   C_ROYAL, UP),
            (np.array([-0.6, 2.5, 0]),  np.array([-4.0, 1.0, 0]), "Queen",  C_FEM,   UP),
            (np.array([-3.5, 0.2, 0]),  np.array([ 1.0, 3.5, 0]), "Man",    C_MALE,  LEFT),
            (np.array([-2.0,-0.3, 0]),  np.array([-1.5,-3.5, 0]), "Woman",  C_FEM,   DOWN),
            (np.array([ 3.2,-2.2, 0]),  np.array([ 2.5, 2.5, 0]), "Cat",    C_ANIM,  DOWN),
            (np.array([ 4.5,-1.5, 0]),  np.array([-0.5,-1.0, 0]), "Dog",    C_ANIM,  RIGHT),
            (np.array([ 1.8, 1.2, 0]),  np.array([-3.5, 3.0, 0]), "Apple",  C_DIR,   UR),
            (np.array([ 3.2, 0.5, 0]),  np.array([ 0.5, 0.0, 0]), "Banana", C_DIR,   RIGHT),
        ]

        dot_mobs = []
        for final, rand, name, col, d in wd:
            dot = gdot(rand, col, name, d=d, r=0.12, fs=18)
            dot_mobs.append(dot)

        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in dot_mobs],
                        lag_ratio=0.06, run_time=0.80),
        )
        self.wait(2.0)

        # Wrong proximity: Apple near Banana random positions (indices 6,7)
        wrong_line = Line(wd[6][1], wd[7][1], stroke_width=2.5)
        wrong_line.set_color(C_WRONG)
        wrong_line.set_opacity(0.60)
        self.play(ShowCreation(wrong_line), run_time=0.50)
        self.wait(2.0)

        self.play(FadeOut(wrong_line), run_time=0.30)

        train_lbl = Text("Training...", font_size=26, weight=BOLD)
        train_lbl.scale(2.0)
        train_lbl.set_color(C_POS)
        train_lbl.move_to(DOWN * 3.6)
        self.play(FadeIn(train_lbl), run_time=0.40)

        trails = VGroup()
        for final, rand, name, col, d in wd:
            trail = Line(rand, final, stroke_width=1.0)
            trail.set_color(col)
            trail.set_opacity(0.15)
            trails.add(trail)
        self.add(trails)

        move_anims = []
        for i, (final, rand, name, col, d) in enumerate(wd):
            outer, inner, lb = dot_mobs[i]
            move_anims.append(outer.animate.move_to(final))
            move_anims.append(inner.animate.move_to(final))
            offset = (UP * 0.30 if d is UP else
                      DOWN * 0.30 if d is DOWN else
                      LEFT * 0.35 if d is LEFT else
                      RIGHT * 0.35 if d is RIGHT else
                      (UP + RIGHT) * 0.22)
            move_anims.append(lb.animate.move_to(final + offset))
        self.play(*move_anims, run_time=3.0)
        self.wait(1.0)
        self.play(FadeOut(train_lbl), FadeOut(trails), run_time=0.30)

        prox = VGroup()
        for a, b in [(0, 1), (2, 3), (4, 5), (6, 7)]:
            ln = Line(wd[a][0], wd[b][0], stroke_width=3.0)
            ln.set_color(C_SIGNAL)
            ln.set_opacity(0.55)
            prox.add(ln)
        self.play(*[ShowCreation(l) for l in prox], run_time=0.70)
        self.wait(2.0)

        meaning_lbl = Text("Meaning emerges from data",
                            font_size=28, weight=BOLD)
        meaning_lbl.scale(1.35)
        meaning_lbl.set_color(C_POS)
        meaning_lbl.move_to(DOWN * 3.9)
        self.play(FadeIn(meaning_lbl), run_time=0.60)
        self.wait(3.0)

        p3 = [grid, prox, meaning_lbl] + dot_mobs
        self.play(*[FadeOut(m) for m in p3], run_time=0.65)
        self.wait(0.80)

        # ══════════════════════════════════════════════════════════════
        # PHASE 4 — 2D Vector Arithmetic
        # ══════════════════════════════════════════════════════════════
        # Shift camera down slightly so equations at bottom are visible
        self.play(frame.animate.shift(DOWN * 0.5), run_time=0.40)

        grid4 = subtle_grid(xr=(-8, 9), yr=(-6, 6), op=0.07)
        self.play(FadeIn(grid4), run_time=0.30)

        # Helper for color-coded equations
        def color_eq(parts, pos):
            """parts = list of (text, color)"""
            grp = VGroup()
            for txt, col in parts:
                t = Text(txt, font_size=28, weight=BOLD)
                t.set_color(col)
                grp.add(t)
            grp.arrange(RIGHT, buff=0.12)
            grp.scale(1.3)
            grp.move_to(pos)
            grp.shift(UP * 0.2)
            return grp

        # Equation FIRST at BOTTOM
        eq1 = color_eq([
            ("King", C_ROYAL), ("-", WHITE), ("Man", C_MALE),
            ("+", WHITE), ("Woman", C_FEM), ("≈", WHITE), ("???", C_DIR),
        ], DOWN * 4.5)
        self.play(FadeIn(eq1), run_time=0.60)
        self.wait(1.5)

        MAN_P   = np.array([-2.2, -1.3, 0])
        WOMAN_P = np.array([ 1.9, -1.4, 0])
        KING_P  = np.array([-2.1,  1.6, 0])
        QUEEN_P = np.array([ 2.0,  1.5, 0])
        NEAR_Q  = np.array([ 2.15, 1.38, 0])

        d_king = gdot(KING_P, C_ROYAL, "King", d=UL, r=0.14, fs=22)
        d_man  = gdot(MAN_P,  C_MALE,  "Man",  d=DL, r=0.14, fs=22)

        self.play(GrowFromCenter(d_king), run_time=0.60)
        self.wait(0.80)
        self.play(GrowFromCenter(d_man), run_time=0.60)
        self.wait(1.0)

        a_king = Arrow(ORIGIN, KING_P, buff=0.0, stroke_width=3.0)
        a_king.set_color(C_ROYAL)
        a_man = Arrow(ORIGIN, MAN_P, buff=0.0, stroke_width=3.0)
        a_man.set_color(C_MALE)
        self.play(GrowArrow(a_king), run_time=0.60)
        self.play(GrowArrow(a_man), run_time=0.60)
        self.wait(1.0)

        roy = Arrow(MAN_P, KING_P, buff=0.16, stroke_width=5.0)
        roy.set_color(C_DIR)
        roy_lbl = Text("Direction:\nRoyalty", font_size=18, weight=BOLD)
        roy_lbl.set_color(C_DIR)
        roy_lbl.next_to(roy, LEFT, buff=0.20)
        self.play(GrowArrow(roy), run_time=0.80)
        self.play(FadeIn(roy_lbl), run_time=0.40)
        self.wait(2.5)

        d_woman = gdot(WOMAN_P, C_FEM, "Woman", d=DR, r=0.14, fs=22)
        self.play(GrowFromCenter(d_woman), run_time=0.60)
        self.wait(1.5)

        roy_copy = Arrow(WOMAN_P, NEAR_Q, buff=0.16, stroke_width=5.0)
        roy_copy.set_color(C_DIR)
        self.play(TransformFromCopy(roy, roy_copy), run_time=1.20)
        self.wait(1.5)

        d_queen = gdot(QUEEN_P, C_QUEEN, "Queen!", d=UR, r=0.18, fs=26)
        self.play(GrowFromCenter(d_queen), run_time=0.80)
        self.play(
            Flash(QUEEN_P, color=C_ROYAL, line_length=0.6,
                  flash_radius=0.5, num_lines=16),
            Indicate(d_queen, color=WHITE, scale_factor=1.4),
            run_time=0.80,
        )

        # Transform equation ??? → Queen
        eq1_done = color_eq([
            ("King", C_ROYAL), ("-", WHITE), ("Man", C_MALE),
            ("+", WHITE), ("Woman", C_FEM), ("≈", WHITE), ("Queen", C_QUEEN),
        ], DOWN * 4.5)
        self.play(Transform(eq1, eq1_done), run_time=0.60)
        self.wait(1.0)

        para = VGroup(
            DashedLine(MAN_P, KING_P, dash_length=0.12, stroke_width=1.5),
            DashedLine(MAN_P, WOMAN_P, dash_length=0.12, stroke_width=1.5),
            DashedLine(KING_P, QUEEN_P, dash_length=0.12, stroke_width=1.5),
            DashedLine(WOMAN_P, QUEEN_P, dash_length=0.12, stroke_width=1.5),
        )
        para.set_color(SOFT_GRAY)
        para.set_opacity(0.40)
        self.play(ShowCreation(para), run_time=0.80)
        self.wait(2.5)

        p4a = [eq1, grid4, d_king, d_man, d_woman, d_queen,
               a_king, a_man, roy, roy_copy, roy_lbl, para]
        self.play(*[FadeOut(m) for m in p4a], run_time=0.65)
        self.wait(0.60)

        # ── Example 2: Paris - France + Italy ≈ Rome ──
        grid4b = subtle_grid(xr=(-8, 9), yr=(-6, 6), op=0.06)
        self.play(FadeIn(grid4b), run_time=0.25)

        eq2 = color_eq([
            ("Paris", "#E74C3C"), ("-", WHITE), ("France", "#3498DB"),
            ("+", WHITE), ("Italy", "#2ECC71"), ("≈", WHITE), ("???", C_DIR),
        ], DOWN * 4.5)
        self.play(FadeIn(eq2), run_time=0.40)
        self.wait(1.5)

        FR_P   = np.array([-3.0, -2.0, 0])
        PAR_P  = np.array([-2.8,  2.0, 0])
        IT_P   = np.array([ 3.0, -2.2, 0])
        ROM_P  = np.array([ 3.2,  1.8, 0])
        NEAR_R = np.array([ 3.05, 1.95, 0])

        d_par = gdot(PAR_P, "#E74C3C", "Paris",   d=UL, r=0.12, fs=20)
        d_fr  = gdot(FR_P,  "#3498DB", "France",  d=DL, r=0.12, fs=20)
        d_it  = gdot(IT_P,  "#2ECC71", "Italy",   d=DR, r=0.12, fs=20)
        self.play(GrowFromCenter(d_par), GrowFromCenter(d_fr),
                  GrowFromCenter(d_it), run_time=0.60)
        self.wait(1.0)

        cap_dir = Arrow(FR_P, PAR_P, buff=0.16, stroke_width=4.5)
        cap_dir.set_color(C_DIR)
        cap_lbl2 = Text("Capital\ndirection", font_size=16, weight=BOLD)
        cap_lbl2.set_color(C_DIR)
        cap_lbl2.next_to(cap_dir, LEFT, buff=0.18)
        self.play(GrowArrow(cap_dir), FadeIn(cap_lbl2), run_time=0.60)
        self.wait(1.0)

        cap_copy = Arrow(IT_P, NEAR_R, buff=0.16, stroke_width=4.5)
        cap_copy.set_color(C_DIR)
        self.play(TransformFromCopy(cap_dir, cap_copy), run_time=0.80)
        self.wait(1.5)

        d_rom = gdot(ROM_P, "#E67E22", "Rome!", d=UR, r=0.14, fs=22)
        self.play(GrowFromCenter(d_rom), run_time=0.60)
        self.play(Flash(ROM_P, color=C_DIR, line_length=0.4,
                        flash_radius=0.4, num_lines=12), run_time=0.50)

        para2 = VGroup(
            DashedLine(FR_P, PAR_P, dash_length=0.12, stroke_width=1.5),
            DashedLine(FR_P, IT_P, dash_length=0.12, stroke_width=1.5),
            DashedLine(PAR_P, ROM_P, dash_length=0.12, stroke_width=1.5),
            DashedLine(IT_P, ROM_P, dash_length=0.12, stroke_width=1.5),
        )
        para2.set_color(SOFT_GRAY)
        para2.set_opacity(0.35)
        self.play(ShowCreation(para2), run_time=0.60)

        eq2_done = color_eq([
            ("Paris", "#E74C3C"), ("-", WHITE), ("France", "#3498DB"),
            ("+", WHITE), ("Italy", "#2ECC71"), ("≈", WHITE), ("Rome", "#E67E22"),
        ], DOWN * 4.5)
        self.play(Transform(eq2, eq2_done), run_time=0.50)
        self.wait(2.5)

        p4b = [eq2, grid4b, d_par, d_fr, d_it, d_rom,
               cap_dir, cap_copy, cap_lbl2, para2]
        self.play(*[FadeOut(m) for m in p4b], run_time=0.50)
        self.wait(0.60)

        # ── Example 3: Walking - Walk + Swim ≈ Swimming ──
        grid4c = subtle_grid(xr=(-8, 9), yr=(-6, 6), op=0.06)
        self.play(FadeIn(grid4c), run_time=0.25)

        eq3 = color_eq([
            ("Walking", C_MALE), ("-", WHITE), ("Walk", C_MALE),
            ("+", WHITE), ("Swim", C_ANIM), ("≈", WHITE), ("???", C_DIR),
        ], DOWN * 4.5)
        self.play(FadeIn(eq3), run_time=0.40)
        self.wait(1.5)

        WK_P  = np.array([-3.0, -1.5, 0])
        WKG_P = np.array([-2.8,  2.0, 0])
        SW_P  = np.array([ 3.0, -1.8, 0])
        SWG_P = np.array([ 3.2,  1.7, 0])
        NEAR_S = np.array([ 3.10, 1.85, 0])

        d_wk  = gdot(WK_P,  C_MALE, "Walk",    d=DL, r=0.12, fs=20)
        d_wkg = gdot(WKG_P, C_MALE, "Walking", d=UL, r=0.12, fs=20)
        d_sw  = gdot(SW_P,  C_ANIM, "Swim",    d=DR, r=0.12, fs=20)
        self.play(GrowFromCenter(d_wk), GrowFromCenter(d_wkg),
                  GrowFromCenter(d_sw), run_time=0.60)
        self.wait(1.0)

        tense_dir = Arrow(WK_P, WKG_P, buff=0.16, stroke_width=4.5)
        tense_dir.set_color(C_DIR)
        tense_lbl = Text("Tense\ndirection", font_size=16, weight=BOLD)
        tense_lbl.set_color(C_DIR)
        tense_lbl.next_to(tense_dir, LEFT, buff=0.18)
        self.play(GrowArrow(tense_dir), FadeIn(tense_lbl), run_time=0.60)
        self.wait(1.5)

        tense_copy = Arrow(SW_P, NEAR_S, buff=0.16, stroke_width=4.5)
        tense_copy.set_color(C_DIR)
        self.play(TransformFromCopy(tense_dir, tense_copy), run_time=0.80)
        self.wait(0.60)

        d_swg = gdot(SWG_P, "#1ABC9C", "Swimming!", d=UR, r=0.14, fs=22)
        self.play(GrowFromCenter(d_swg), run_time=0.60)
        self.play(Flash(SWG_P, color=C_DIR, line_length=0.4,
                        flash_radius=0.4, num_lines=12), run_time=0.50)

        para3 = VGroup(
            DashedLine(WK_P, WKG_P, dash_length=0.12, stroke_width=1.5),
            DashedLine(WK_P, SW_P, dash_length=0.12, stroke_width=1.5),
            DashedLine(WKG_P, SWG_P, dash_length=0.12, stroke_width=1.5),
            DashedLine(SW_P, SWG_P, dash_length=0.12, stroke_width=1.5),
        )
        para3.set_color(SOFT_GRAY)
        para3.set_opacity(0.35)
        self.play(ShowCreation(para3), run_time=0.60)

        eq3_done = color_eq([
            ("Walking", C_MALE), ("-", WHITE), ("Walk", C_MALE),
            ("+", WHITE), ("Swim", C_ANIM), ("≈", WHITE), ("Swimming", "#1ABC9C"),
        ], DOWN * 4.5)
        self.play(Transform(eq3, eq3_done), run_time=0.50)
        self.wait(3.0)

        p4c = [eq3, grid4c, d_wk, d_wkg, d_sw, d_swg,
               tense_dir, tense_copy, tense_lbl, para3]
        self.play(*[FadeOut(m) for m in p4c], run_time=0.65)
        self.wait(0.60)

        # Reset camera shift from Phase 4
        self.play(frame.animate.shift(UP * 0.5), run_time=0.40)

        # ══════════════════════════════════════════════════════════════
        # PHASE 5 — Summary  (~20 s)
        # ══════════════════════════════════════════════════════════════
        s1 = Text("One-hot  -->  no meaning", font_size=28, weight=BOLD)
        s1.set_color(C_WRONG)
        s2 = Text("Embeddings  -->  meaningful geometry",
                    font_size=28, weight=BOLD)
        s2.set_color(C_SIGNAL)
        s3 = Text("Vector arithmetic reveals relationships",
                    font_size=28, weight=BOLD)
        s3.set_color(C_DIR)

        sum_grp = VGroup(s1, s2, s3)
        sum_grp.arrange(DOWN, buff=0.60)
        sum_grp.scale(1.5)
        sum_grp.move_to(ORIGIN)

        for sm in [s1, s2, s3]:
            self.play(FadeIn(sm, shift=UP * 0.15), run_time=0.60)
            self.wait(1.5)

        self.wait(4.0)

        self.play(FadeOut(sum_grp), run_time=0.70)
        self.wait(1.5)


# ═══════════════════════════════════════════════════════════════════
#  SCENE 3 — Self-Attention Intro (context-aware embeddings)
# ═══════════════════════════════════════════════════════════════════

class SelfAttentionIntro(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 1 — Hook: same word, two meanings
        # ══════════════════════════════════════════════════════════════
        title = make_title("Same Word, Different Meaning",
                           np.array([0, 3.7, 0]), C_FADE, fs=60)
        self.play(Write(title), run_time=0.60)


        # Two sentences where "bank" means different things
        s1 = Text('"I went to the bank"', font_size=48, weight=BOLD)
        s1.set_color(WHITE); s1.move_to(UP * 1.8)

        s2 = Text('"Fish swim near the bank"', font_size=48, weight=BOLD)
        s2.set_color(WHITE).shift(UP*0.33)

        self.play(Write(s1), run_time=0.80)
        self.wait(1.0)
        self.play(Write(s2), run_time=0.80)
        self.wait(1.5)

        temp_a = ImageMobject("bank.png").next_to(s2, DOWN, buff=0.68).scale(0.8)
        self.play(FadeIn(temp_a))
        self.wait(2)



        # Embedding vector is the same — problem!
        same_txt = Text(
            "Embedding vector will be the same!",
            font_size=56, weight=BOLD,
        )
        same_txt.set_color(YELLOW); same_txt.move_to(title)
        self.play(Transform(title, same_txt), run_time=0.50)
        self.wait(2.0)

        # We need something that takes context
        need_txt = Text("We need something new...", font_size=56, weight=BOLD)
        need_txt.set_color(C_POS); need_txt.move_to(title)
        self.play(Transform(title, need_txt), run_time=0.50)
        self.wait(2.0)

        ctx_txt = Text(
            "Something that takes context \n      around the word",
            font_size=56, weight=BOLD,
        )
        ctx_txt.set_color(C_POS); ctx_txt.move_to(title)
        self.play(Transform(title, ctx_txt), run_time=0.50)
        self.wait(2.0)

        # Fade out Phase 1
        p1 = [title, s1,  s2, temp_a]
        self.play(*[FadeOut(m) for m in p1], run_time=0.55)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 2 — Word cards one-by-one, attention arcs, embeddings
        # ══════════════════════════════════════════════════════════════
        words = ["I", "loved", "her"]
        word_colors = ["#2ECC71", "#E74C3C", "#3498DB"]

        # Word cards (colored background rectangles)
        cards = VGroup()
        for w, c in zip(words, word_colors):
            lb = Text(w, font_size=65, weight=BOLD)
            lb.set_color(WHITE)
            bg = RoundedRectangle(
                width=lb.get_width() + 0.70, height=1,
                corner_radius=0.10,
            )
            bg.set_fill(c, opacity=0.85)
            bg.set_stroke(WHITE, width=1.5)
            lb.move_to(bg.get_center())
            cards.add(VGroup(bg, lb))

        cards.arrange(RIGHT, buff=1.20)
        cards.move_to(UP * 1.1)

        # Show cards one by one: I, loved, her
        for i in range(3):
            self.play(FadeIn(cards[i], shift=DOWN * 0.10), run_time=0.40)
            self.wait(0.25)
        self.wait(0.50)

        # ── Attention arcs: each word connects to every other ──
        # Relation weights (row=src, col=tgt)
        #                    I     loved  her
        rel = [
            [0.00, 0.40, 0.20],  # I:     strong→loved (subject-verb)
            [0.35, 0.00, 0.45],  # loved: strong→her (verb-object), moderate→I
            [0.20, 0.45, 0.00],  # her:   strong→loved (object-verb), moderate→I
        ]
        for src in range(3):
            src_arcs = []
            for tgt in range(3):
                if tgt == src:
                    continue
                wt = rel[src][tgt]
                sw = wt * 20 + 1.0
                op = wt * 1.6 + 0.12
                op = min(op, 1.0)
                s = cards[src].get_top() + UP * 0.08
                e = cards[tgt].get_top() + UP * 0.08
                ang = -PI / 3 if src < tgt else PI / 3
                arc = ArcBetweenPoints(s, e, angle=ang)
                arc.set_stroke(word_colors[src], width=sw, opacity=op)
                src_arcs.append(arc)
            self.play(*[ShowCreation(a) for a in src_arcs], run_time=0.60)
            self.wait(2.0)
            self.play(*[Uncreate(a) for a in src_arcs], run_time=0.50)
            self.wait(0.20)

        # 3-cell horizontal embedding vector below each word
        cs = 0.65
        emb_vecs = VGroup()
        for i, c in enumerate(word_colors):
            row = VGroup()
            for j in range(3):
                sq = Square(side_length=cs)
                sq.set_fill(c, opacity=1.0)
                sq.set_stroke(WHITE, width=1.0)
                sq.move_to(RIGHT * j * cs)
                row.add(sq)
            row.move_to(ORIGIN)
            row.next_to(cards[i], DOWN, buff=0.49)
            emb_vecs.add(row)

        self.play(
            LaggedStart(*[FadeIn(v, shift=DOWN * 0.10) for v in emb_vecs],
                        lag_ratio=0.08, run_time=0.80),
        )
        self.wait(1.5)

        # ══════════════════════════════════════════════════════════════
        # PHASE 3 — Colored weighted-sum equation with Ē (bar)
        # ══════════════════════════════════════════════════════════════
        eq_data = [
            (r"\boldsymbol{\bar{E}_{\mathbf{her}}}", "#3498DB"),
            (r"=",                                    WHITE),
            (r"\mathbf{0.20} \times",                 WHITE),
            (r"\boldsymbol{E_{\mathbf{I}}}",          "#2ECC71"),
            (r"+",                                    WHITE),
            (r"\mathbf{0.45} \times",                 WHITE),
            (r"\boldsymbol{E_{\mathbf{loved}}}",      "#E74C3C"),
            (r"+",                                    WHITE),
            (r"\mathbf{0.35} \times",                 WHITE),
            (r"\boldsymbol{E_{\mathbf{her}}}",        "#3498DB"),
        ]
        eq = VGroup()
        for tex_str, col in eq_data:
            t = Tex(tex_str, font_size=34)
            t.set_color(col)
            eq.add(t)
        eq.arrange(RIGHT, buff=0.10)
        eq.next_to(emb_vecs, DOWN, buff=0.99)
        eq.shift(DOWN * 0.66).scale(1.7).scale(1.34)
        self.play(Write(eq), self.camera.frame.animate.shift(DOWN), run_time=1.50)
        self.wait(1.1)

        rect = Brace(eq[2:4], DOWN, buff=0.54)
        rect.set_color(YELLOW)
        self.play(GrowFromEdge(rect, DOWN), run_time=0.50)
        self.wait(2)

        self.play(Transform(rect, Brace(eq[5:7], DOWN, buff=0.54).set_color(YELLOW)))
        self.wait(2)

        self.play(Transform(rect, Brace(eq[8:10], DOWN, buff=0.54).set_color(YELLOW)))
        self.wait(2)

        self.play(FadeOut(rect))

        rect1 = SurroundingRectangle(eq[2][:4], color=YELLOW)
        rect2 = SurroundingRectangle(eq[5][:4], color=YELLOW)
        rect3 = SurroundingRectangle(eq[8][:4], color=YELLOW)

        self.play(ShowCreation(rect1), ShowCreation(rect2), ShowCreation(rect3), run_time=0.50)
        self.wait(2)

        self.play(FadeOut(rect1), FadeOut(rect2), FadeOut(rect3))
        self.wait(2)

        # Transform: replace numeric weights with dot products
        eq2_data = [
            (r"\boldsymbol{\bar{E}_{\mathbf{her}}}", "#3498DB"),
            (r"=",                                    WHITE),
            (r"(",                                    WHITE),
            (r"\boldsymbol{E_{\mathbf{I}}}",          "#2ECC71"),
            (r"\cdot",                                WHITE),
            (r"\boldsymbol{E_{\mathbf{her}}}",        "#3498DB"),
            (r")",                                    WHITE),
            (r"\boldsymbol{E_{\mathbf{I}}}",          "#2ECC71"),
            (r"+",                                    WHITE),
            (r"(",                                    WHITE),
            (r"\boldsymbol{E_{\mathbf{loved}}}",      "#E74C3C"),
            (r"\cdot",                                WHITE),
            (r"\boldsymbol{E_{\mathbf{her}}}",        "#3498DB"),
            (r")",                                    WHITE),
            (r"\boldsymbol{E_{\mathbf{loved}}}",      "#E74C3C"),
            (r"+",                                    WHITE),
            (r"(",                                    WHITE),
            (r"\boldsymbol{E_{\mathbf{her}}}",        "#3498DB"),
            (r"\cdot",                                WHITE),
            (r"\boldsymbol{E_{\mathbf{her}}}",        "#3498DB"),
            (r")",                                    WHITE),
            (r"\boldsymbol{E_{\mathbf{her}}}",        "#3498DB"),
        ]
        eq2 = VGroup()
        for tex_str, col in eq2_data:
            t = Tex(tex_str, font_size=34)
            t.set_color(col)
            eq2.add(t)
        eq2.arrange(RIGHT, buff=0.10)
        eq2.move_to(eq.get_center())
        eq2.match_height(eq)
        eq2.scale(0.75).shift(RIGHT*0.3)
        self.play(Transform(eq, eq2), run_time=1.50)
        self.wait(2.0)

        brace1 = Brace(eq[2:8], DOWN, buff=0.54)
        brace1.set_color(YELLOW)
        self.play(GrowFromEdge(brace1, DOWN), run_time=0.50)
        self.wait(2)

        self.play(Transform(brace1, Brace(eq[2:7], DOWN, buff=0.54).set_color(YELLOW)))
        self.wait(2)

        self.play(Transform(brace1, Brace(eq[9:15], DOWN, buff=0.54).set_color(YELLOW)))
        self.wait(2)

        self.play(Transform(brace1, Brace(eq[9:14], DOWN, buff=0.54).set_color(YELLOW)))
        self.wait(2)

        self.play(Transform(brace1, Brace(eq[16:], DOWN, buff=0.54).set_color(YELLOW)))
        self.wait(2)

        self.play(Transform(brace1, Brace(eq[16:-1], DOWN, buff=0.54).set_color(YELLOW)))
        self.wait(2)


        self.play(FadeOut(brace1))

        # Ē_I equation below the current equation
        eq_i_data = [
            (r"\boldsymbol{\bar{E}_{\mathbf{I}}}", "#2ECC71"),
            (r"=",                                  WHITE),
            (r"(",                                  WHITE),
            (r"\boldsymbol{E_{\mathbf{I}}}",        "#2ECC71"),
            (r"\cdot",                              WHITE),
            (r"\boldsymbol{E_{\mathbf{I}}}",        "#2ECC71"),
            (r")",                                  WHITE),
            (r"\boldsymbol{E_{\mathbf{I}}}",        "#2ECC71"),
            (r"+",                                  WHITE),
            (r"(",                                  WHITE),
            (r"\boldsymbol{E_{\mathbf{loved}}}",    "#E74C3C"),
            (r"\cdot",                              WHITE),
            (r"\boldsymbol{E_{\mathbf{I}}}",        "#2ECC71"),
            (r")",                                  WHITE),
            (r"\boldsymbol{E_{\mathbf{loved}}}",    "#E74C3C"),
            (r"+",                                  WHITE),
            (r"(",                                  WHITE),
            (r"\boldsymbol{E_{\mathbf{her}}}",      "#3498DB"),
            (r"\cdot",                              WHITE),
            (r"\boldsymbol{E_{\mathbf{I}}}",        "#2ECC71"),
            (r")",                                  WHITE),
            (r"\boldsymbol{E_{\mathbf{her}}}",      "#3498DB"),
        ]
        eq_i = VGroup()
        for tex_str, col in eq_i_data:
            t = Tex(tex_str, font_size=34)
            t.set_color(col)
            eq_i.add(t)
        eq_i.arrange(RIGHT, buff=0.10)
        eq_i.match_height(eq)
        eq_i.next_to(eq, DOWN, buff=0.60)

        self.play(Write(eq_i), self.camera.frame.animate.shift(DOWN*0.66) ,run_time=1.50)
        self.wait()

        # Ē_loved equation below Ē_I
        eq_l_data = [
            (r"\boldsymbol{\bar{E}_{\mathbf{loved}}}", "#E74C3C"),
            (r"=",                                      WHITE),
            (r"(",                                      WHITE),
            (r"\boldsymbol{E_{\mathbf{I}}}",            "#2ECC71"),
            (r"\cdot",                                  WHITE),
            (r"\boldsymbol{E_{\mathbf{loved}}}",        "#E74C3C"),
            (r")",                                      WHITE),
            (r"\boldsymbol{E_{\mathbf{I}}}",            "#2ECC71"),
            (r"+",                                      WHITE),
            (r"(",                                      WHITE),
            (r"\boldsymbol{E_{\mathbf{loved}}}",        "#E74C3C"),
            (r"\cdot",                                  WHITE),
            (r"\boldsymbol{E_{\mathbf{loved}}}",        "#E74C3C"),
            (r")",                                      WHITE),
            (r"\boldsymbol{E_{\mathbf{loved}}}",        "#E74C3C"),
            (r"+",                                      WHITE),
            (r"(",                                      WHITE),
            (r"\boldsymbol{E_{\mathbf{her}}}",          "#3498DB"),
            (r"\cdot",                                  WHITE),
            (r"\boldsymbol{E_{\mathbf{loved}}}",        "#E74C3C"),
            (r")",                                      WHITE),
            (r"\boldsymbol{E_{\mathbf{her}}}",          "#3498DB"),
        ]
        eq_l = VGroup()
        for tex_str, col in eq_l_data:
            t = Tex(tex_str, font_size=34)
            t.set_color(col)
            eq_l.add(t)
        eq_l.arrange(RIGHT, buff=0.10)
        eq_l.match_height(eq)
        eq_l.next_to(eq_i, DOWN, buff=0.60).scale(0.928)

        self.play(Write(eq_l), run_time=1.50)
        self.wait(2.0)

        # Transform all three: replace dot products with attention weights (a)
        FS = 39

        def _build_w_eq(parts):
            grp = VGroup()
            for tex_str, col in parts:
                t = Tex(tex_str, font_size=FS)
                t.set_color(col)
                grp.add(t)
            grp.arrange(RIGHT, buff=0.10)
            return grp



        # Ē_her = W_IH · E_I + W_LH · E_loved + W_HH · E_her
        eq_her_w = _build_w_eq([
            (r"\boldsymbol{\bar{E}_{\mathbf{her}}}", "#3498DB"),
            (r"=",                                    WHITE),
            (r"\mathbf{a_{IH}}",                      ORANGE),
            (r"\boldsymbol{E_{\mathbf{I}}}",          "#2ECC71"),
            (r"+",                                    WHITE),
            (r"\mathbf{a_{LH}}",                      ORANGE),
            (r"\boldsymbol{E_{\mathbf{loved}}}",      "#E74C3C"),
            (r"+",                                    WHITE),
            (r"\mathbf{a_{HH}}",                      ORANGE),
            (r"\boldsymbol{E_{\mathbf{her}}}",        "#3498DB"),
        ])

        # Ē_I = W_II · E_I + W_LI · E_loved + W_HI · E_her
        eq_i_w = _build_w_eq([
            (r"\boldsymbol{\bar{E}_{\mathbf{I}}}", "#2ECC71"),
            (r"=",                                  WHITE),
            (r"\mathbf{a_{II}}",                    ORANGE),
            (r"\boldsymbol{E_{\mathbf{I}}}",        "#2ECC71"),
            (r"+",                                  WHITE),
            (r"\mathbf{a_{LI}}",                    ORANGE),
            (r"\boldsymbol{E_{\mathbf{loved}}}",    "#E74C3C"),
            (r"+",                                  WHITE),
            (r"\mathbf{a_{HI}}",                    ORANGE),
            (r"\boldsymbol{E_{\mathbf{her}}}",      "#3498DB"),
        ])

        # Ē_loved = W_IL · E_I + W_LL · E_loved + W_HL · E_her
        eq_l_w = _build_w_eq([
            (r"\boldsymbol{\bar{E}_{\mathbf{loved}}}", "#E74C3C"),
            (r"=",                                      WHITE),
            (r"\mathbf{a_{IL}}",                        ORANGE),
            (r"\boldsymbol{E_{\mathbf{I}}}",            "#2ECC71"),
            (r"+",                                      WHITE),
            (r"\mathbf{a_{LL}}",                        ORANGE),
            (r"\boldsymbol{E_{\mathbf{loved}}}",        "#E74C3C"),
            (r"+",                                      WHITE),
            (r"\mathbf{a_{HL}}",                        ORANGE),
            (r"\boldsymbol{E_{\mathbf{her}}}",          "#3498DB"),
        ])


        # Position them to match current equations
        eq_her_w.move_to(eq.get_center()).match_height(eq)
        eq_i_w.move_to(eq_i.get_center()).match_height(eq)
        eq_l_w.move_to(eq_l.get_center()).match_height(eq)

        self.camera.frame.save_state()

        self.play(
            Transform(eq, eq_her_w),
            Transform(eq_i, eq_i_w),
            Transform(eq_l, eq_l_w),
            self.camera.frame.animate.scale(0.9),
            run_time=1.50,
        )
        self.wait(2.0)


        # Show how w_IH is calculated from a_IH using softmax
        sm_title = Text("How do we get the Normalized weights?", font_size=46, weight=BOLD)
        sm_title.set_color(C_POS)
        self.play(self.camera.frame.animate.shift(RIGHT * 14))
        sm_title.move_to(self.camera.frame.get_center() + UP * 3.0)
        self.play(Write(sm_title), run_time=0.60)
        self.wait(1.0)

        # Build as single Tex for proper fraction rendering
        sm_eq = Tex(
            r"\mathbf{w_{IH}} \ = \ \frac{e^{a_{IH}}}{e^{a_{IH}} + e^{a_{LH}} + e^{a_{HH}}}",
            font_size=78,
        )
        sm_eq.move_to(self.camera.frame.get_center() + UP * 1.0)
        # Color the w yellow
        sm_eq[0:3].set_color(YELLOW).scale(1.4).shift(DOWN*0.15)
        self.play(Write(sm_eq), run_time=1.20)
        self.wait(2.0)

        # General softmax label
        sm_gen = Tex(
            r"\mathbf{w_{ij}} = \frac{e^{a_{ij}}}{\sum_k e^{a_{kj}}}",
            font_size=78,
        )
        sm_gen.move_to(self.camera.frame.get_center() + DOWN * 1.5)
        sm_label = Text("Softmax normalization", font_size=66, weight=BOLD)
        sm_label.set_color(C_SOFT)
        sm_label.next_to(sm_gen, DOWN, buff=0.65)

        self.play(Write(sm_gen), FadeIn(sm_label), run_time=1.00)
        self.wait(2.0)

        # Show what softmax does
        sm_note = Text("Ensures all weights sum to 1", font_size=58, weight=BOLD)
        sm_note.set_color(C_SIGNAL)
        sm_note.move_to(sm_label).shift(DOWN*0.1)
        self.play(FadeIn(sm_note), FadeOut(sm_label), run_time=0.50)
        self.wait(2.5)

        # Fade out softmax explanation
        self.play(
            FadeOut(sm_title), FadeOut(sm_eq),
            FadeOut(sm_gen), FadeOut(sm_note),
            self.camera.frame.animate.shift(LEFT * 14), run_time=0.60,
        )

        self.wait(2)



        # Transform all three equations: replace a weights with w weights
        eq_her_final = _build_w_eq([
            (r"\boldsymbol{\bar{E}_{\mathbf{her}}}", "#3498DB"),
            (r"=",                                    WHITE),
            (r"\mathbf{w_{IH}}",                      YELLOW),
            (r"\boldsymbol{E_{\mathbf{I}}}",          "#2ECC71"),
            (r"+",                                    WHITE),
            (r"\mathbf{w_{LH}}",                      YELLOW),
            (r"\boldsymbol{E_{\mathbf{loved}}}",      "#E74C3C"),
            (r"+",                                    WHITE),
            (r"\mathbf{w_{HH}}",                      YELLOW),
            (r"\boldsymbol{E_{\mathbf{her}}}",        "#3498DB"),
        ])

        eq_i_final = _build_w_eq([
            (r"\boldsymbol{\bar{E}_{\mathbf{I}}}", "#2ECC71"),
            (r"=",                                  WHITE),
            (r"\mathbf{w_{II}}",                    YELLOW),
            (r"\boldsymbol{E_{\mathbf{I}}}",        "#2ECC71"),
            (r"+",                                  WHITE),
            (r"\mathbf{w_{LI}}",                    YELLOW),
            (r"\boldsymbol{E_{\mathbf{loved}}}",    "#E74C3C"),
            (r"+",                                  WHITE),
            (r"\mathbf{w_{HI}}",                    YELLOW),
            (r"\boldsymbol{E_{\mathbf{her}}}",      "#3498DB"),
        ])

        eq_l_final = _build_w_eq([
            (r"\boldsymbol{\bar{E}_{\mathbf{loved}}}", "#E74C3C"),
            (r"=",                                      WHITE),
            (r"\mathbf{w_{IL}}",                        YELLOW),
            (r"\boldsymbol{E_{\mathbf{I}}}",            "#2ECC71"),
            (r"+",                                      WHITE),
            (r"\mathbf{w_{LL}}",                        YELLOW),
            (r"\boldsymbol{E_{\mathbf{loved}}}",        "#E74C3C"),
            (r"+",                                      WHITE),
            (r"\mathbf{w_{HL}}",                        YELLOW),
            (r"\boldsymbol{E_{\mathbf{her}}}",          "#3498DB"),
        ])

        eq_her_final.move_to(eq.get_center()).match_height(eq)
        eq_i_final.move_to(eq_i.get_center()).match_height(eq)
        eq_l_final.move_to(eq_l.get_center()).match_height(eq)

        self.play(
            Transform(eq, eq_her_final),
            Transform(eq_i, eq_i_final),
            Transform(eq_l, eq_l_final),
            run_time=1.50,
        )
        self.wait(2.0)

        # ══════════════════════════════════════════════════════════════
        # PHASE — Parallelism demonstration
        # ══════════════════════════════════════════════════════════════

        # Fade out the 3 equations
        all_eqs = VGroup(eq, eq_i, eq_l)
        self.play(FadeOut(all_eqs), run_time=0.60)
        self.wait(0.50)

        # Big text
        par_title = Text("This Process is Parallel!", font_size=58, weight=BOLD)
        par_title.set_color(C_POS)
        par_title.move_to(self.camera.frame.get_center()).shift(DOWN)
        self.play(Write(par_title), run_time=0.80)
        self.wait(2.0)
        self.play(FadeOut(par_title), run_time=0.50)
        self.wait(1.5)



        CENTER = self.camera.frame.get_center()
        # Place everything below the embedding row
        # emb_vecs bottom ≈ cards(UP*1.1) - card_h(1) - buff(0.49) - emb_h(0.65) ≈ -1.04
        BASE_Y = emb_vecs.get_bottom()[1] - 0.60  # further below embeddings
        EMB_SZ = 0.65  # match original embedding cell size
        C_ORANGE = "#E67E22"
        emb_colors = ["#2ECC71", "#E74C3C", "#3498DB"]
        # Bright pure versions for final context
        ctx_colors = ["#00FF66", "#FF3333", "#33BBFF"]

        def make_h_block(col, sz=EMB_SZ):
            row = VGroup()
            for j in range(3):
                sq = Square(side_length=sz)
                sq.set_fill(col, opacity=1.0)
                sq.set_stroke(WHITE, width=1.0)
                row.add(sq)
            row.arrange(RIGHT, buff=0)
            return row

        def make_v_block(col, sz=EMB_SZ):
            blk = VGroup()
            for j in range(3):
                sq = Square(side_length=sz)
                sq.set_fill(col, opacity=1.0)
                sq.set_stroke(WHITE, width=1.0)
                blk.add(sq)
            blk.arrange(DOWN, buff=0)
            return blk

        # ── PART A: Single dot products for "I" ──
        part_a_title = Text("Computing weights for one word",
                            font_size=36, weight=BOLD)
        part_a_title.set_color(WHITE)
        part_a_title.move_to(np.array([0, BASE_Y - 0.15, 0])).shift(DOWN*0.23)
        part_a_title.scale(1.3)
        self.play(FadeIn(part_a_title), run_time=0.40)
        self.wait(0.50)

        dp_x = [-5.0, 0.0, 5.0]
        dp_y = BASE_Y - 2.55
        a_subs = ["II", "IL", "IH"]

        dp_groups = []
        for idx, (col, _) in enumerate(zip(emb_colors, ["I", "loved", "her"])):
            cx = dp_x[idx]

            h_blk = make_h_block("#2ECC71")
            h_blk.move_to(np.array([cx - 1.2, dp_y, 0]))

            dot_sym = Tex(r"\cdot", font_size=40)
            dot_sym.set_color(WHITE)
            dot_sym.next_to(h_blk, RIGHT, buff=0.15)

            v_blk = make_v_block(col)
            v_blk.next_to(dot_sym, RIGHT, buff=0.15)

            a_lbl = Tex(r"\mathbf{a_{" + a_subs[idx] + r"}}", font_size=28)
            a_lbl.set_color(C_ORANGE)
            a_lbl.move_to(np.array([cx, dp_y - 1.6, 0]))
            a_lbl.scale(2)

            self.play(
                TransformFromCopy(emb_vecs[0], h_blk),
                run_time=0.50,
            )
            self.play(
                TransformFromCopy(emb_vecs[idx], v_blk),
                FadeIn(dot_sym),
                run_time=0.50,
            )
            self.play(FadeIn(a_lbl), run_time=0.40)
            self.wait(1.5)

            dp_groups.extend([h_blk, dot_sym, v_blk, a_lbl])

        self.wait(1.0)
        self.play(*[FadeOut(m) for m in dp_groups], FadeOut(part_a_title),
                  run_time=0.50)
        self.wait(0.30)

        seq_line1 = Text("We did this one at a time...", font_size=24, weight=BOLD)
        seq_line1.set_color(C_FADE)
        seq_line2 = Text("but we don't have to!", font_size=24, weight=BOLD)
        seq_line2.set_color(C_FADE)
        seq_note = VGroup(seq_line1, seq_line2)
        seq_note.arrange(DOWN, buff=0.15, aligned_edge=ORIGIN)
        seq_note.scale(1.99)
        seq_note.move_to(np.array([0, BASE_Y - 2.3, 0]))
        self.play(FadeIn(seq_note), run_time=0.50)
        self.wait(2.0)
        self.play(FadeOut(seq_note), run_time=0.40)
        self.wait(0.30)

        # ── PART B: Full matrix pipeline ──
        # All positioned between BASE_Y and bottom of visible frame
        MID_Y = BASE_Y - 2.8  # vertical center for matrices (further down)

        part_b_title = Text("All weights at once — matrix multiply!",
                            font_size=32, weight=BOLD)
        part_b_title.set_color(C_POS)
        part_b_title.move_to(np.array([0, BASE_Y - 0.5, 0]))
        part_b_title.scale(1.2)
        self.play(FadeIn(part_b_title), run_time=0.40)

        # E matrix (3 rows stacked) — build pipeline then center
        GAP = 0.3  # gap between matrix and operator

        mat_E = VGroup(*[make_h_block(c) for c in emb_colors])
        mat_E.arrange(DOWN, buff=0)

        times1 = Tex(r"\times", font_size=34)
        times1.set_color(WHITE)

        mat_ET = VGroup(*[make_v_block(c) for c in emb_colors])
        mat_ET.arrange(RIGHT, buff=0)

        eq1 = Tex(r"=", font_size=34)
        eq1.set_color(WHITE)

        mat_A = VGroup()
        for i in range(3):
            a_row = VGroup()
            for j in range(3):
                sq = Square(side_length=EMB_SZ)
                sq.set_fill(C_ORANGE, opacity=1.0)
                sq.set_stroke(WHITE, width=1.0)
                a_row.add(sq)
            a_row.arrange(RIGHT, buff=0)
            mat_A.add(a_row)
        mat_A.arrange(DOWN, buff=0)

        # Weights after softmax — each row sums to 1
        w_nums = [
            [0.1, 0.6, 0.3],
            [0.3, 0.2, 0.5],
            [0.2, 0.5, 0.3],
        ]
        mat_W = VGroup()
        for i in range(3):
            w_row = VGroup()
            for j in range(3):
                sq = Square(side_length=EMB_SZ)
                sq.set_fill(YELLOW, opacity=0.25 + w_nums[i][j] * 0.75)
                sq.set_stroke(WHITE, width=1.0)
                nm = Text(f"{w_nums[i][j]:.1f}", font_size=18, weight=BOLD)
                nm.set_color(WHITE)
                nm.move_to(sq.get_center())
                w_row.add(VGroup(sq, nm))
            w_row.arrange(RIGHT, buff=0)
            mat_W.add(w_row)
        mat_W.arrange(DOWN, buff=0)

        # Layout: E × E^T = A → softmax → W, all centered
        # Arrange left-to-right with consistent gaps
        ARROW_LEN = 2.2
        pipeline_items = VGroup(mat_E, times1, mat_ET, eq1, mat_A)
        pipeline_items.arrange(RIGHT, buff=GAP)
        # Position the whole pipeline centered at MID_Y
        pipeline_items.move_to(np.array([-1.0, MID_Y, 0]))

        # Softmax arrow and W placed relative to A
        sm_arrow = Arrow(
            mat_A.get_right() + RIGHT * 0.12,
            mat_A.get_right() + RIGHT * ARROW_LEN,
            buff=0, stroke_width=3.5, color=WHITE,
        )
        sm_arrow.set_color(WHITE)
        sm_label = Text("softmax", font_size=27, weight=BOLD)
        sm_label.set_color(C_SOFT)
        sm_label.next_to(sm_arrow, UP, buff=0.15)

        mat_W.next_to(sm_arrow, RIGHT, buff=0.12)

        # Now center the entire thing (E to W) horizontally
        full_pipeline = VGroup(mat_E, times1, mat_ET, eq1, mat_A,
                               sm_arrow, mat_W)
        full_center_x = full_pipeline.get_center()[0]
        shift_x = -full_center_x  # center at x=0
        for mob in [mat_E, times1, mat_ET, eq1, mat_A, sm_arrow, mat_W]:
            mob.shift(RIGHT * shift_x)
        sm_label.next_to(sm_arrow, UP, buff=0.08)

        # Labels below each matrix
        E_label = Tex(r"\mathbf{E}", font_size=50)
        E_label.set_color(WHITE)
        E_label.next_to(mat_E, DOWN, buff=0.25)

        ET_label = Tex(r"\mathbf{E}^T", font_size=50)
        ET_label.set_color(WHITE)
        ET_label.next_to(mat_ET, DOWN, buff=0.25)

        A_label = Tex(r"\mathbf{A}", font_size=50)
        A_label.set_color(C_ORANGE)
        A_label.next_to(mat_A, DOWN, buff=0.25)

        W_label = Tex(r"\mathbf{W}", font_size=50)
        W_label.set_color(YELLOW)
        W_label.next_to(mat_W, DOWN, buff=0.25)

        # Animate piece by piece
        self.play(
            *[TransformFromCopy(emb_vecs[i], mat_E[i]) for i in range(3)],
            FadeIn(E_label),
            run_time=0.80,
        )
        self.wait(0.80)

        self.play(
            *[TransformFromCopy(emb_vecs[i], mat_ET[i]) for i in range(3)],
            FadeIn(times1), FadeIn(ET_label),
            run_time=0.80,
        )
        self.wait(0.80)

        self.play(FadeIn(eq1), FadeIn(mat_A), FadeIn(A_label), run_time=0.80)
        self.wait(1.5)

        # Flash all 9 A cells
        flash_a = []
        for row in mat_A:
            for cell in row:
                flash_a.append(Indicate(cell, color=WHITE, scale_factor=1.2))
        self.play(*flash_a, run_time=0.80)

        self.play(GrowArrow(sm_arrow), FadeIn(sm_label), run_time=0.60)
        self.wait(0.80)

        self.play(TransformFromCopy(mat_A, mat_W), FadeIn(W_label), run_time=0.80)
        self.wait(2.0)


        # Fade E×E^T=A + softmax, keep W
        self.play(
            FadeOut(mat_E), FadeOut(E_label),
            FadeOut(times1), FadeOut(mat_ET), FadeOut(ET_label),
            FadeOut(eq1), FadeOut(mat_A), FadeOut(A_label),
            FadeOut(sm_arrow), FadeOut(sm_label),
            FadeOut(part_b_title),
            run_time=0.50,
        )

        # W × E = Ē
        final_title = Text("Final context embeddings",
                           font_size=36, weight=BOLD)
        final_title.set_color(C_POS)
        final_title.move_to(np.array([0, BASE_Y - 0.15, 0]))
        final_title.shift(DOWN * 0.33).scale(1.45)
        self.play(FadeIn(final_title), run_time=0.40)

        # Move W to the left
        w_target_x = -6.55

        self.play(
            mat_W.animate.move_to(np.array([w_target_x, MID_Y, 0])),
            W_label.animate.next_to(
                np.array([w_target_x, MID_Y - EMB_SZ * 1.5 - 0.15, 0]), DOWN, buff=0),
            run_time=0.60,
        )


        times2 = Tex(r"\times", font_size=50)
        times2.set_color(WHITE)
        times2.next_to(mat_W, RIGHT, buff=0.25)

        mat_E2 = VGroup(*[make_h_block(c) for c in emb_colors])
        mat_E2.arrange(DOWN, buff=0)
        mat_E2.next_to(times2, RIGHT, buff=0.25)

        E2_label = Tex(r"\mathbf{E}", font_size=50)
        E2_label.set_color(WHITE)
        E2_label.next_to(mat_E2, DOWN, buff=0.25)

        eq2 = Tex(r"=", font_size=50)
        eq2.set_color(WHITE)
        eq2.next_to(mat_E2, RIGHT, buff=0.25)

        # Ē — lighter colors, no text
        mat_ctx = VGroup(*[make_h_block(c) for c in ctx_colors])
        mat_ctx.arrange(DOWN, buff=0)
        mat_ctx.next_to(eq2, RIGHT, buff=0.25)

        ctx_label = Tex(r"\bar{\mathbf{E}}", font_size=50)
        ctx_label.set_color(C_POS)
        ctx_label.next_to(mat_ctx, DOWN, buff=0.25)

        self.play(
            FadeIn(times2),
            *[TransformFromCopy(emb_vecs[i], mat_E2[i]) for i in range(3)],
            FadeIn(E2_label),
            run_time=0.60,
        )
        self.wait(0.80)

        self.play(FadeIn(eq2), FadeIn(mat_ctx), FadeIn(ctx_label), run_time=0.80)
        self.wait(1.0)

        ctx_note = Text("Context-aware embeddings!", font_size=37, weight=BOLD)
        ctx_note.set_color(C_POS)
        ctx_note.next_to(mat_ctx, RIGHT, buff=0.30)
        self.play(FadeIn(ctx_note), run_time=0.50)
        self.wait(1.5)

        self.camera.frame.save_state()

        par_note = Text("All computed in parallel — GPUs love this!",
                        font_size=40, weight=BOLD)
        par_note.set_color(C_SIGNAL)
        par_note.move_to(part_b_title)
        self.play(FadeIn(par_note, shift=UP * 0.10), FadeOut(final_title) ,run_time=0.50)
        self.wait(3.0)






# ═══════════════════════════════════════════════════════════════════
#  SCENE 4 — Why we need Q, K, V (from first principles)

# ═══════════════════════════════════════════════════════════════════
#  SCENE 4 — Why we need Q, K, V (from first principles)

# ═══════════════════════════════════════════════════════════════════
#  SCENE 4 — Self-Attention Pipeline
#  manimgl a.py SelfAttentionFinal -w -l
# ═══════════════════════════════════════════════════════════════════

class SelfAttentionFinal(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.30)

        C_I     = "#2ECC71"
        C_LOVED = "#E74C3C"
        C_HER   = "#3498DB"
        C_ORANGE = "#E67E22"
        C_Q     = "#E74C3C"
        C_K     = "#F39C12"
        C_V     = "#3498DB"
        emb_colors = [C_I, C_LOVED, C_HER]
        words = ["I", "loved", "her"]
        SZ = 0.50

        def make_h_block(col, sz=SZ):
            row = VGroup()
            for j in range(3):
                sq = Square(side_length=sz)
                sq.set_fill(col, opacity=1.0)
                sq.set_stroke(WHITE, width=1.0)
                row.add(sq)
            row.arrange(RIGHT, buff=0)
            return row

        def make_v_block(col, sz=SZ):
            blk = VGroup()
            for j in range(3):
                sq = Square(side_length=sz)
                sq.set_fill(col, opacity=1.0)
                sq.set_stroke(WHITE, width=1.0)
                blk.add(sq)
            blk.arrange(DOWN, buff=0)
            return blk

        def make_3x3(col, sz=SZ):
            mat = VGroup()
            for i in range(3):
                row = VGroup()
                for j in range(3):
                    sq = Square(side_length=sz)
                    sq.set_fill(col, opacity=1.0)
                    sq.set_stroke(WHITE, width=1.0)
                    row.add(sq)
                row.arrange(RIGHT, buff=0)
                mat.add(row)
            mat.arrange(DOWN, buff=0)
            return mat

        def stacked_E(sz=SZ):
            mat = VGroup()
            for c in emb_colors:
                mat.add(make_h_block(c, sz))
            mat.arrange(DOWN, buff=0)
            return mat

        # ── Word cards at top ──
        cards = VGroup()
        for w, c in zip(words, emb_colors):
            lb = Text(w, font_size=55, weight=BOLD)
            lb.set_color(WHITE)
            bg = RoundedRectangle(
                width=lb.get_width() + 0.60, height=0.90,
                corner_radius=0.10,
            )
            bg.set_fill(c, opacity=0.85)
            bg.set_stroke(WHITE, width=1.5)
            lb.move_to(bg.get_center())
            cards.add(VGroup(bg, lb))
        cards.arrange(RIGHT, buff=1.20)
        cards.move_to(UP * 3.0)

        cs = 0.55
        emb_vecs = VGroup()
        for i, c in enumerate(emb_colors):
            row = VGroup()
            for j in range(3):
                sq = Square(side_length=cs)
                sq.set_fill(c, opacity=1.0)
                sq.set_stroke(WHITE, width=1.0)
                row.add(sq)
            row.arrange(RIGHT, buff=0)
            row.next_to(cards[i], DOWN, buff=0.35)
            emb_vecs.add(row)

        self.play(
            LaggedStart(*[FadeIn(c, shift=DOWN * 0.10) for c in cards],
                        lag_ratio=0.08, run_time=0.70),
        )
        self.wait(0.30)
        self.play(
            LaggedStart(*[FadeIn(v, shift=DOWN * 0.10) for v in emb_vecs],
                        lag_ratio=0.08, run_time=0.60),
        )
        self.wait(1.0)

        # ── Full pipeline in one line below embeddings ──
        # E × E^T = Scores → softmax → Weights × E = Output
        PSZ = SZ * 0.70
        GAP = 0.12

        mat_E = stacked_E(PSZ)
        t1 = Tex(r"\times", font_size=22).set_color(WHITE)
        mat_ET = VGroup(*[make_v_block(c, PSZ) for c in emb_colors])
        mat_ET.arrange(RIGHT, buff=0)
        eq1 = Tex(r"=", font_size=22).set_color(WHITE)
        mat_scores = make_3x3(C_ORANGE, PSZ)
        sm_arr = Arrow(ORIGIN, RIGHT * 1.5,
                       buff=0, stroke_width=3.0, color=WHITE).set_color(WHITE)
        sm_lbl = Tex(r"\mathrm{softmax}", font_size=16).set_color(C_SOFT)
        # Weights after softmax — rows sum to 1
        w_nums1 = [
            [0.1, 0.6, 0.3],
            [0.3, 0.2, 0.5],
            [0.2, 0.5, 0.3],
        ]
        mat_W = VGroup()
        for i in range(3):
            w_row = VGroup()
            for j in range(3):
                sq = Square(side_length=PSZ)
                sq.set_fill(YELLOW, opacity=0.25 + w_nums1[i][j] * 0.75)
                sq.set_stroke(WHITE, width=1.0)
                nm = Text(f"{w_nums1[i][j]:.1f}", font_size=9, weight=BOLD)
                nm.set_color(WHITE)
                nm.move_to(sq.get_center())
                w_row.add(VGroup(sq, nm))
            w_row.arrange(RIGHT, buff=0)
            mat_W.add(w_row)
        mat_W.arrange(DOWN, buff=0)

        t2 = Tex(r"\times", font_size=22).set_color(WHITE)
        mat_Eval = stacked_E(PSZ)
        eq2 = Tex(r"=", font_size=22).set_color(WHITE)
        ctx_cols = ["#00FF66", "#FF3333", "#33BBFF"]
        mat_out = VGroup(*[make_h_block(c, PSZ) for c in ctx_cols])
        mat_out.arrange(DOWN, buff=0)

        pipe = VGroup(mat_E, t1, mat_ET, eq1, mat_scores,
                      sm_arr, mat_W, t2, mat_Eval, eq2, mat_out)
        pipe.arrange(RIGHT, buff=GAP)
        pipe.scale(1.76)
        pipe.move_to(DOWN * 1.5)
        sm_lbl.next_to(sm_arr, UP, buff=0.21)
        sm_lbl.scale(3.6)

        # Labels
        BF = 0.40
        E_lbl = Tex(r"\mathbf{E}", font_size=24).set_color(WHITE)
        E_lbl.next_to(mat_E, DOWN, buff=BF).scale(2)
        ET_lbl = Tex(r"\mathbf{E}^T", font_size=24).set_color(WHITE)
        ET_lbl.next_to(mat_ET, DOWN, buff=BF).scale(2)
        sc_lbl = Text("Scores", font_size=16, weight=BOLD).set_color(C_ORANGE)
        sc_lbl.next_to(mat_scores, DOWN, buff=BF).scale(2)
        w_lbl = Text("Weights", font_size=16, weight=BOLD).set_color(YELLOW)
        w_lbl.next_to(mat_W, DOWN, buff=BF).scale(2)
        Ev_lbl = Tex(r"\mathbf{E}", font_size=24).set_color(WHITE)
        Ev_lbl.next_to(mat_Eval, DOWN, buff=BF).scale(2)
        out_lbl = Tex(r"\bar{\mathbf{E}}", font_size=26).set_color(C_SIGNAL)
        out_lbl.next_to(mat_out, DOWN, buff=BF).scale(2)

        # Animate step by step
        self.play(
            *[TransformFromCopy(emb_vecs[i], mat_E[i]) for i in range(3)],
            FadeIn(E_lbl), run_time=0.60,
        )
        self.wait(0.30)
        self.play(
            *[TransformFromCopy(emb_vecs[i], mat_ET[i]) for i in range(3)],
            FadeIn(t1), FadeIn(ET_lbl), run_time=0.60,
        )
        self.wait(0.30)
        self.play(FadeIn(eq1), FadeIn(mat_scores), FadeIn(sc_lbl),
                  run_time=0.40)
        self.wait(0.40)
        self.play(GrowArrow(sm_arr), FadeIn(sm_lbl), run_time=0.35)
        self.play(FadeIn(mat_W), FadeIn(w_lbl), run_time=0.35)
        self.wait(0.40)
        self.play(
            *[TransformFromCopy(emb_vecs[i], mat_Eval[i]) for i in range(3)],
            FadeIn(t2), FadeIn(Ev_lbl), run_time=0.60,
        )
        self.play(FadeIn(eq2), FadeIn(mat_out), FadeIn(out_lbl),
                  run_time=0.40)
        self.wait(2.0)

        # Purple brace walkthrough
        br1 = Brace(VGroup(E_lbl, ET_lbl), DOWN, buff=0.5)
        br1.set_color("#9B59B6")
        self.play(GrowFromEdge(br1, UP), run_time=0.50)
        self.wait(2.0)

        br2 = Brace(sc_lbl, DOWN, buff=0.5)
        br2.set_color("#9B59B6")
        self.play(Transform(br1, br2), run_time=0.50)
        self.wait(2.0)

        br3 = Brace(w_lbl, DOWN, buff=0.5)
        br3.set_color("#9B59B6")
        self.play(Transform(br1, br3), run_time=0.50)
        self.wait(2.0)

        br4 = Brace(VGroup(w_lbl, Ev_lbl), DOWN, buff=0.5)
        br4.set_color("#9B59B6")
        self.play(Transform(br1, br4), run_time=0.50)
        self.wait(2.0)

        br5 = Brace(mat_out, DOWN, buff=1.0)
        br5.set_color("#9B59B6")
        self.play(Transform(br1, br5), run_time=0.50)
        self.wait(2.0)

        self.play(FadeOut(br1), run_time=0.40)

        self.camera.frame.save_state()
        
        self.play(self.camera.frame.animate.shift(DOWN*0.67))

        a = Text("No Learnable Parameters", weight=BOLD).scale(1.599)
        a.set_color(RED)
        a.next_to(sc_lbl, DOWN, buff=0.95).shift(RIGHT*2.32)
        self.play(Write(a), run_time=0.60)
        self.wait(2.0)
        self.play(FadeOut(a), run_time=0.40)

        # ── Highlight: same E used 3 times for different purposes ──
        TXT_Y = a.get_center()[1]  # same y as "No Learnable Parameters" was

        # 1) Highlight E (query-like role)
        C_QV = "#FF6B9D"
        C_KV = "#FFB347"
        C_VV = "#77DDaa"
        rect_E = SurroundingRectangle(VGroup(mat_E, E_lbl), buff=0.08, stroke_width=3.0)
        rect_E.set_color(C_QV)
        rect_E.set_fill(C_QV, opacity=0.15)
        role_txt = Text("This acts as the Query - it asks the question",
                        font_size=29, weight=BOLD)
        role_txt.set_color(C_QV)
        role_txt.move_to(np.array([0, TXT_Y, 0]))
        role_txt.scale(1.5)

        self.play(ShowCreation(rect_E), FadeIn(role_txt), run_time=0.50)
        self.wait(2.5)

        # 2) Move to E^T (key-like role)
        rect_ET = SurroundingRectangle(VGroup(mat_ET, ET_lbl), buff=0.08, stroke_width=3.0)
        rect_ET.set_color(C_KV)
        rect_ET.set_fill(C_KV, opacity=0.15)
        role_txt2 = Text("This acts as the Key - it answers the question",
                         font_size=29, weight=BOLD)
        role_txt2.set_color(C_KV)
        role_txt2.move_to(np.array([0, TXT_Y, 0]))
        role_txt2.scale(1.5)

        self.play(
            Transform(rect_E, rect_ET),
            Transform(role_txt, role_txt2),
            run_time=0.50,
        )
        self.wait(2.5)

        # 3) Move to E_val (value role)
        rect_Ev = SurroundingRectangle(VGroup(mat_Eval, Ev_lbl), buff=0.08, stroke_width=3.0)
        rect_Ev.set_color(C_VV)
        rect_Ev.set_fill(C_VV, opacity=0.15)
        role_txt3 = Text("This acts as the Value - it carries the information",
                         font_size=28, weight=BOLD)
        role_txt3.set_color(C_VV)
        role_txt3.move_to(np.array([0, TXT_Y, 0]))
        role_txt3.scale(1.5)

        self.play(
            Transform(rect_E, rect_Ev),
            Transform(role_txt, role_txt3),
            run_time=0.50,
        )
        self.wait(2.5)

        # Fade out rectangles and text
        self.play(FadeOut(rect_E), FadeOut(role_txt), run_time=0.40)
        self.wait(1.0)

        # Fade out entire pipeline below
        pipe_all = [mat_E, t1, mat_ET, eq1, mat_scores, sm_arr, sm_lbl,
                    mat_W, t2, mat_Eval, eq2, mat_out,
                    E_lbl, ET_lbl, sc_lbl, w_lbl, Ev_lbl, out_lbl]
        self.play(*[FadeOut(m) for m in pipe_all], run_time=0.60)
        self.wait(0.50)

        # ── Show how Q, K, V are computed: branching from E ──
        MID_Y = emb_vecs.get_bottom()[1] - 3.9
        SPREAD = 2.2
        WSZ = PSZ * 0.85

        # E matrix centered-left
        mat_E_qkv = VGroup(*[make_h_block(c, WSZ) for c in emb_colors])
        mat_E_qkv.arrange(DOWN, buff=0)
        mat_E_qkv.scale(1.5)
        mat_E_qkv.move_to(np.array([-4.8, MID_Y, 0]))
        e_qkv_lbl = Tex(r"\mathbf{E}", font_size=28).set_color(WHITE)
        e_qkv_lbl.scale(2).next_to(mat_E_qkv, DOWN, buff=0.30)

        self.play(
            *[TransformFromCopy(emb_vecs[i], mat_E_qkv[i]) for i in range(3)],
            FadeIn(e_qkv_lbl), run_time=0.60,
        )
        self.wait(0.50)

        # Stem line from E going right
        STEM_X = -2.6
        branch_pt = np.array([STEM_X, MID_Y, 0])
        stem = Line(
            mat_E_qkv.get_right() + RIGHT * 0.08, branch_pt,
            stroke_width=3.5, color=WHITE,
        )
        self.play(ShowCreation(stem), run_time=0.35)

        # Three branches: up→Q, straight→K, down→V
        qkv_branch = [
            (C_QV, r"\mathbf{W}_Q", r"\mathbf{Q}", MID_Y + SPREAD),
            (C_KV, r"\mathbf{W}_K", r"\mathbf{K}", MID_Y),
            (C_VV, r"\mathbf{W}_V", r"\mathbf{V}", MID_Y - SPREAD),
        ]

        W_X = -0.3
        RES_X = 2.5
        all_qkv_mobs = [stem]

        for col, w_tex, out_tex, y_pos in qkv_branch:
            # Vertical line (skip for middle/K)
            if y_pos != MID_Y:
                vert = Line(branch_pt, np.array([STEM_X, y_pos, 0]),
                            stroke_width=3.0, color=col)
                self.play(ShowCreation(vert), run_time=0.20)
                all_qkv_mobs.append(vert)

            # Horizontal arrow to W matrix
            h_arr = Arrow(
                np.array([STEM_X, y_pos, 0]),
                np.array([W_X - 0.8, y_pos, 0]),
                buff=0, stroke_width=3.0, color=col,
            ).set_color(col)
            self.play(GrowArrow(h_arr), run_time=0.20)

            # W matrix
            w_mat = make_3x3(col, WSZ)
            w_mat.scale(1.5)
            w_mat.move_to(np.array([W_X, y_pos, 0]))
            w_lbl_c = Tex(w_tex, font_size=22).set_color(col)
            w_lbl_c.scale(1.8).next_to(w_mat, DOWN, buff=0.20)
            self.play(FadeIn(w_mat), FadeIn(w_lbl_c), run_time=0.25)

            # = sign and result
            eq_s = Tex(r"=", font_size=22).set_color(WHITE)
            eq_s.scale(1.5)
            eq_s.next_to(w_mat, RIGHT, buff=0.15)

            # Result Q/K/V matrix
            res_mat = make_3x3(col, WSZ)
            res_mat.scale(1.5)
            res_mat.next_to(eq_s, RIGHT, buff=0.15)
            res_lbl = Tex(out_tex, font_size=22).set_color(col)
            res_lbl.scale(2).next_to(res_mat, DOWN, buff=0.20)

            self.play(FadeIn(eq_s),
                      FadeIn(res_mat), FadeIn(res_lbl), run_time=0.35)
            self.wait(1.0)

            all_qkv_mobs.extend([h_arr, w_mat, w_lbl_c,
                                  eq_s, res_mat, res_lbl])

        self.wait(2.0)

        # Fade all QKV computation
        all_qkv_mobs.extend([mat_E_qkv, e_qkv_lbl])
        self.play(*[FadeOut(m) for m in all_qkv_mobs], run_time=0.60)
        self.wait(0.50)

        # Create Q, K, V embedding vectors below "I loved her" cards
        # Colors already defined above

        qkv_cs = 0.55
        q_vecs = VGroup()
        k_vecs = VGroup()
        v_vecs = VGroup()

        for i in range(3):
            q_row = VGroup()
            k_row = VGroup()
            v_row = VGroup()
            for j in range(3):
                sq_q = Square(side_length=qkv_cs)
                sq_q.set_fill(C_QV, opacity=1.0)
                sq_q.set_stroke(WHITE, width=1.0)
                q_row.add(sq_q)

                sq_k = Square(side_length=qkv_cs)
                sq_k.set_fill(C_KV, opacity=1.0)
                sq_k.set_stroke(WHITE, width=1.0)
                k_row.add(sq_k)

                sq_v = Square(side_length=qkv_cs)
                sq_v.set_fill(C_VV, opacity=1.0)
                sq_v.set_stroke(WHITE, width=1.0)
                v_row.add(sq_v)

            q_row.arrange(RIGHT, buff=0)
            k_row.arrange(RIGHT, buff=0)
            v_row.arrange(RIGHT, buff=0)

            q_row.next_to(emb_vecs[i], DOWN, buff=0.35)
            k_row.next_to(q_row, DOWN, buff=0.20)
            v_row.next_to(k_row, DOWN, buff=0.20)

            q_vecs.add(q_row)
            k_vecs.add(k_row)
            v_vecs.add(v_row)

        # Q, K, V labels — first letter only, scaled up
        q_lbls = VGroup()
        k_lbls = VGroup()
        v_lbls = VGroup()
        word_initials = ["I", "l", "h"]
        for i, w in enumerate(word_initials):
            ql = Tex(r"\mathbf{Q}_{" + w + r"}", font_size=22).set_color(C_QV)
            ql.scale(2).next_to(q_vecs[i], LEFT, buff=0.15)
            q_lbls.add(ql)

            kl = Tex(r"\mathbf{K}_{" + w + r"}", font_size=22).set_color(C_KV)
            kl.scale(2).next_to(k_vecs[i], LEFT, buff=0.15)
            k_lbls.add(kl)

            vl = Tex(r"\mathbf{V}_{" + w + r"}", font_size=22).set_color(C_VV)
            vl.scale(2).next_to(v_vecs[i], LEFT, buff=0.15)
            v_lbls.add(vl)

        # Animate Q vectors appearing
        self.play(
            LaggedStart(*[FadeIn(q, shift=DOWN * 0.10) for q in q_vecs],
                        lag_ratio=0.08, run_time=0.60),
            LaggedStart(*[FadeIn(l) for l in q_lbls],
                        lag_ratio=0.08, run_time=0.60),
        )
        self.wait(0.80)

        # Animate K vectors
        self.play(
            LaggedStart(*[FadeIn(k, shift=DOWN * 0.10) for k in k_vecs],
                        lag_ratio=0.08, run_time=0.60),
            LaggedStart(*[FadeIn(l) for l in k_lbls],
                        lag_ratio=0.08, run_time=0.60),
        )
        self.wait(0.80)

        # Animate V vectors
        self.play(
            LaggedStart(*[FadeIn(v, shift=DOWN * 0.10) for v in v_vecs],
                        lag_ratio=0.08, run_time=0.60),
            LaggedStart(*[FadeIn(l) for l in v_lbls],
                        lag_ratio=0.08, run_time=0.60),
        )
        self.wait(2.0)

        # ── New pipeline using Q, K, V ──
        # Place below the V vectors
        PIPE_Y = v_vecs.get_bottom()[1] - 2.39

        mat_Q = VGroup(*[make_h_block(C_QV, PSZ) for _ in range(3)])
        mat_Q.arrange(DOWN, buff=0)
        pt1 = Tex(r"\times", font_size=22).set_color(WHITE)
        mat_KT = VGroup(*[make_v_block(C_KV, PSZ) for _ in range(3)])
        mat_KT.arrange(RIGHT, buff=0)
        peq1 = Tex(r"=", font_size=22).set_color(WHITE)
        mat_sc2 = make_3x3(C_ORANGE, PSZ)
        sm_arr2 = Arrow(ORIGIN, RIGHT * 1.5,
                        buff=0, stroke_width=3.0, color=WHITE).set_color(WHITE)
        sm_lbl2 = Tex(r"\mathrm{softmax}", font_size=16).set_color(C_SOFT)
        # Weights after softmax — rows sum to 1
        w_nums2 = [
            [0.2, 0.6, 0.2],
            [0.4, 0.1, 0.5],
            [0.3, 0.4, 0.3],
        ]
        mat_W2 = VGroup()
        for i in range(3):
            w_row = VGroup()
            for j in range(3):
                sq = Square(side_length=PSZ)
                sq.set_fill(YELLOW, opacity=0.25 + w_nums2[i][j] * 0.75)
                sq.set_stroke(WHITE, width=1.0)
                nm = Text(f"{w_nums2[i][j]:.1f}", font_size=9, weight=BOLD)
                nm.set_color(WHITE)
                nm.move_to(sq.get_center())
                w_row.add(VGroup(sq, nm))
            w_row.arrange(RIGHT, buff=0)
            mat_W2.add(w_row)
        mat_W2.arrange(DOWN, buff=0)

        pt2 = Tex(r"\times", font_size=22).set_color(WHITE)
        mat_V2 = VGroup(*[make_h_block(C_VV, PSZ) for _ in range(3)])
        mat_V2.arrange(DOWN, buff=0)
        peq2 = Tex(r"=", font_size=22).set_color(WHITE)
        ctx_cols2 = ["#00FF66", "#FF3333", "#33BBFF"]
        mat_out2 = VGroup(*[make_h_block(c, PSZ) for c in ctx_cols2])
        mat_out2.arrange(DOWN, buff=0)

        pipe2 = VGroup(mat_Q, pt1, mat_KT, peq1, mat_sc2,
                        sm_arr2, mat_W2, pt2, mat_V2, peq2, mat_out2)
        pipe2.arrange(RIGHT, buff=GAP)
        pipe2.scale(1.76)
        pipe2.move_to(np.array([0, PIPE_Y, 0]))
        sm_lbl2.next_to(sm_arr2, UP, buff=0.15).scale(3.6)

        # Labels
        BF2 = 0.40
        Q_lbl2 = Tex(r"\mathbf{Q}", font_size=24).set_color(C_QV)
        Q_lbl2.next_to(mat_Q, DOWN, buff=BF2).scale(2)
        KT_lbl2 = Tex(r"\mathbf{K}^T", font_size=24).set_color(C_KV)
        KT_lbl2.next_to(mat_KT, DOWN, buff=BF2).scale(2)
        sc_lbl2 = Text("Scores", font_size=16, weight=BOLD).set_color(C_ORANGE)
        sc_lbl2.next_to(mat_sc2, DOWN, buff=BF2).scale(2)
        w_lbl2 = Text("Weights", font_size=16, weight=BOLD).set_color(YELLOW)
        w_lbl2.next_to(mat_W2, DOWN, buff=BF2).scale(2)
        V_lbl2 = Tex(r"\mathbf{V}", font_size=24).set_color(C_VV)
        V_lbl2.next_to(mat_V2, DOWN, buff=BF2).scale(2)
        out_lbl2 = Tex(r"\bar{\mathbf{E}}", font_size=26).set_color(C_SIGNAL)
        out_lbl2.next_to(mat_out2, DOWN, buff=BF2).scale(2)

        # Animate step by step
        self.play(
            *[TransformFromCopy(q_vecs[i], mat_Q[i]) for i in range(3)],
            FadeIn(Q_lbl2), run_time=0.60,
        )
        self.wait(0.30)
        self.play(
            *[TransformFromCopy(k_vecs[i], mat_KT[i]) for i in range(3)],
            FadeIn(pt1), FadeIn(KT_lbl2), run_time=0.60,
        )
        self.wait(0.30)
        self.play(FadeIn(peq1), FadeIn(mat_sc2), FadeIn(sc_lbl2),
                  run_time=0.40)
        self.wait(0.40)
        self.play(GrowArrow(sm_arr2), FadeIn(sm_lbl2), run_time=0.35)
        self.play(FadeIn(mat_W2), FadeIn(w_lbl2), run_time=0.35)
        self.wait(0.40)
        self.play(
            *[TransformFromCopy(v_vecs[i], mat_V2[i]) for i in range(3)],
            FadeIn(pt2), FadeIn(V_lbl2), run_time=0.60,
        )
        self.play(FadeIn(peq2), FadeIn(mat_out2), FadeIn(out_lbl2),
                  run_time=0.40)
        self.wait(2.0)

        # Fade pipeline, replace with formula
        pipe2_all = [mat_Q, pt1, mat_KT, peq1, mat_sc2,
                     sm_arr2, sm_lbl2, mat_W2, pt2, mat_V2, peq2, mat_out2,
                     Q_lbl2, KT_lbl2, sc_lbl2, w_lbl2, V_lbl2, out_lbl2]
        self.play(*[FadeOut(m) for m in pipe2_all], run_time=0.60)
        self.wait(1.50)

        # Attention = Softmax(Q K^T) V — single Tex, colored parts
        attn_eq = Tex(
            r"Attention",
            r"\ =\ ",
            r"Softmax(",
            r"\mathbf{Q}",
            r"\cdot",
            r"\mathbf{K}^T",
            r")",
            r"\cdot",
            r"\mathbf{V}",
            font_size=38,
        )

        attn_eq.scale(2.75)
        attn_eq.move_to(np.array([0, PIPE_Y, 0])).shift(DOWN*0.2)

        attn_eq[:9].set_color(C_SIGNAL)
        attn_eq[10:17].set_color(ORANGE)
        attn_eq[18].set_color(C_QV)
        attn_eq[20:22].set_color(C_KV)
        attn_eq[24].set_color(C_VV)

        self.play(Write(attn_eq), run_time=1.20)
        self.wait(2.0)

        # Transform to scaled version with sqrt(d_k)
        attn_eq2 = Tex(
            r"Attention",
            r"\ =\ ",
            r"Softmax(",
            r"\frac{",
            r"\mathbf{Q}",
            r"\cdot",
            r"\mathbf{K}^T",
            r"}{",
            r"\sqrt{d_k}",
            r"}",
            r")",
            r"\cdot",
            r"\mathbf{V}",
            font_size=38,
        )
        attn_eq2.scale(2.75)
        attn_eq2.move_to(attn_eq.get_center())

        # Color matching: find the right submobject indices
        # Render and color by matching the same pattern
        attn_eq2[:9].set_color(C_SIGNAL)        # Attention
        attn_eq2[10:17].set_color(ORANGE)        # Softmax(
        attn_eq2[18].set_color(C_QV)             # Q
        attn_eq2[20:22].set_color(C_KV)          # K^T
        attn_eq2[23:27].set_color(C_KV)          # sqrt(d_k) — same as K^T
        attn_eq2[-1].set_color(C_VV)             # V

        self.play(Transform(attn_eq, attn_eq2), run_time=0.9)
        self.wait(3.0)




# ═══════════════════════════════════════════════════════════════════

class DotProductSpace(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.22)

        # ── Colors ──
        C_BANK   = "#E74C3C"
        C_MONEY  = "#F1C40F"
        C_DEPOSIT = "#F39C12"
        C_RIVER  = "#3498DB"
        C_WATER  = "#5DADE2"
        C_FISH   = "#2ECC71"

        def gdot(pos, col, txt, d=UP, r=0.13, fs=20):
            outer = Circle(radius=r * 2.8)
            outer.set_fill(col, opacity=0.20)
            outer.set_stroke(width=0)
            outer.move_to(pos)
            inner = Circle(radius=r)
            inner.set_fill(col, opacity=1.0)
            inner.set_stroke(WHITE, width=1.5)
            inner.move_to(pos)
            lb = Text(txt, font_size=fs, weight=BOLD)
            lb.set_color(col)
            lb.next_to(inner, d, buff=0.15)
            return VGroup(outer, inner, lb)

        def subtle_grid(xr=(-8, 9), yr=(-5, 6), op=0.08):
            g = VGroup()
            for x in range(*xr):
                sw = 2.0 if x == 0 else 0.5
                ln = Line(np.array([x, yr[0], 0]), np.array([x, yr[1], 0]),
                          stroke_width=sw)
                ln.set_color(WHITE if x == 0 else SOFT_GRAY)
                ln.set_opacity(0.22 if x == 0 else op)
                g.add(ln)
            for y in range(*yr):
                sw = 2.0 if y == 0 else 0.5
                ln = Line(np.array([xr[0], y, 0]), np.array([xr[1], y, 0]),
                          stroke_width=sw)
                ln.set_color(WHITE if y == 0 else SOFT_GRAY)
                ln.set_opacity(0.22 if y == 0 else op)
                g.add(ln)
            return g

        # ══════════════════════════════════════════════════════════════
        # PHASE 1 — Word vectors in 2D space with "bank" ambiguity
        # ══════════════════════════════════════════════════════════════
        title2 = Text('"Bank of the river"', font_size=40, weight=BOLD)
        title2.set_color(WHITE)
        title2.move_to(DOWN * 3.8)
        title2.scale(1.1)
        self.play(Write(title2), run_time=0.60)
        self.wait(1.0)

        grid2 = subtle_grid(xr=(-9, 10), yr=(-6, 7))
        self.play(FadeIn(grid2), run_time=0.40)

        # Word positions — two clusters + bank in between
        # Financial cluster (top-left)
        pos_money   = np.array([-4.0,  3.0, 0])
        pos_deposit = np.array([-3.0,  1.8, 0])
        # Nature cluster (top-right)
        pos_river   = np.array([ 4.0,  2.5, 0])
        pos_water   = np.array([ 3.5,  1.0, 0])
        pos_fish    = np.array([ 5.0,  0.5, 0])
        # Bank in the middle (ambiguous)
        pos_bank    = np.array([ 0.0, -0.5, 0])

        d_money   = gdot(pos_money,   C_MONEY,   "money",   d=UP,    r=0.14, fs=20)
        d_deposit = gdot(pos_deposit, C_DEPOSIT, "deposit", d=LEFT,  r=0.14, fs=20)
        d_river   = gdot(pos_river,   C_RIVER,   "river",   d=UP,    r=0.14, fs=20)
        d_water   = gdot(pos_water,   C_WATER,   "water",   d=RIGHT, r=0.14, fs=20)
        d_fish    = gdot(pos_fish,    C_FISH,    "fish",    d=RIGHT, r=0.14, fs=20)
        d_bank    = gdot(pos_bank,    C_BANK,    "bank",    d=DOWN,  r=0.18, fs=24)

        all_dots = [d_money, d_deposit, d_river, d_water, d_fish, d_bank]

        # Show dots one by one
        for d in all_dots:
            self.play(GrowFromCenter(d), run_time=0.40)
            self.wait(0.30)
        self.wait(1.0)

        # Cluster labels
        fin_lbl = Text("Financial", font_size=18, weight=BOLD)
        fin_lbl.set_color(C_MONEY)
        fin_lbl.move_to(np.array([-3.5, 4.0, 0]))
        nat_lbl = Text("Nature", font_size=18, weight=BOLD)
        nat_lbl.set_color(C_RIVER)
        nat_lbl.move_to(np.array([4.2, 3.8, 0]))

        # Dashed cluster circles
        fin_circle = Circle(radius=1.8)
        fin_circle.set_stroke(C_MONEY, width=1.5, opacity=0.30)
        fin_circle.move_to(np.array([-3.5, 2.4, 0]))
        nat_circle = Circle(radius=2.0)
        nat_circle.set_stroke(C_RIVER, width=1.5, opacity=0.30)
        nat_circle.move_to(np.array([4.2, 1.3, 0]))

        self.play(
            FadeIn(fin_lbl), FadeIn(nat_lbl),
            ShowCreation(fin_circle), ShowCreation(nat_circle),
            run_time=0.60,
        )
        self.wait(1.5)

        # Highlight bank is equidistant — ambiguous
        amb_txt = Text('"bank" is equally close to both clusters!',
                       font_size=24, weight=BOLD)
        amb_txt.set_color(C_BANK)
        amb_txt.move_to(DOWN * 2.8)
        amb_txt.scale(1.2)

        line_fin = DashedLine(pos_bank, pos_money, dash_length=0.12,
                              stroke_width=2.0, color=C_MONEY)
        line_fin.set_opacity(0.50)
        line_nat = DashedLine(pos_bank, pos_river, dash_length=0.12,
                              stroke_width=2.0, color=C_RIVER)
        line_nat.set_opacity(0.50)

        self.play(
            ShowCreation(line_fin), ShowCreation(line_nat),
            FadeIn(amb_txt),
            run_time=0.60,
        )
        self.wait(2.5)

        # ══════════════════════════════════════════════════════════════
        # PHASE 3 — Attention computes weights, bank moves
        # ══════════════════════════════════════════════════════════════
        self.play(FadeOut(amb_txt), FadeOut(line_fin), FadeOut(line_nat),
                  run_time=0.40)

        attn_txt = Text("Self-attention reads the context...",
                        font_size=26, weight=BOLD)
        attn_txt.set_color(C_SIGNAL)
        attn_txt.move_to(DOWN * 2.8)
        attn_txt.scale(1.2)
        self.play(FadeIn(attn_txt), run_time=0.50)
        self.wait(1.5)

        # Show attention arcs from bank to river, water, fish
        arc_colors = [C_RIVER, C_WATER, C_FISH]
        arc_targets = [pos_river, pos_water, pos_fish]
        arc_weights = [0.40, 0.30, 0.25]  # strong to nature words
        arcs = []
        for tgt, col, wt in zip(arc_targets, arc_colors, arc_weights):
            left = min(pos_bank[0], tgt[0])
            right = max(pos_bank[0], tgt[0])
            s = pos_bank + UP * 0.25
            e = tgt + UP * 0.25
            ang = -PI / 4 if pos_bank[0] < tgt[0] else PI / 4
            arc = ArcBetweenPoints(s, e, angle=ang)
            sw = wt * 16 + 2.0
            op = wt * 1.5 + 0.20
            arc.set_stroke(col, width=sw, opacity=min(op, 1.0))
            arcs.append(arc)

        # Weak arcs to financial words
        arc_fin_colors = [C_MONEY, C_DEPOSIT]
        arc_fin_targets = [pos_money, pos_deposit]
        arc_fin_weights = [0.03, 0.02]
        for tgt, col, wt in zip(arc_fin_targets, arc_fin_colors, arc_fin_weights):
            s = pos_bank + UP * 0.25
            e = tgt + UP * 0.25
            ang = PI / 4 if pos_bank[0] > tgt[0] else -PI / 4
            arc = ArcBetweenPoints(s, e, angle=ang)
            sw = wt * 16 + 1.0
            op = wt * 1.5 + 0.10
            arc.set_stroke(col, width=sw, opacity=min(op, 0.30))
            arcs.append(arc)

        self.play(
            *[ShowCreation(a) for a in arcs],
            run_time=0.80,
        )
        self.wait(2.0)

        self.play(
            Transform(attn_txt, Text("Context says: this is a RIVER bank!",
                      font_size=26, weight=BOLD).set_color(C_SIGNAL).move_to(
                      DOWN * 2.8).scale(1.2)),
            run_time=0.60,
        )
        self.wait(2.0)

        # Fade arcs
        self.play(*[FadeOut(a) for a in arcs], 
                  run_time=0.40)

        # Move bank toward the nature cluster!
        bank_target = np.array([3.8, 0.0, 0])  # near river/water/fish
        outer, inner, lb = d_bank

        # Trail line showing movement
        trail = Line(pos_bank, bank_target, stroke_width=1.5)
        trail.set_color(C_BANK)
        trail.set_opacity(0.25)
        self.add(trail)

        self.play(
            outer.animate.move_to(bank_target),
            inner.animate.move_to(bank_target),
            lb.animate.move_to(bank_target + DOWN * 0.40),
            run_time=2.0,
        )
        self.wait(1.0)

        # Flash to celebrate — only Flash, no Indicate (it shifts the group)
        self.play(
            Flash(bank_target, color=C_BANK, line_length=0.5,
                  flash_radius=0.5, num_lines=14),
            run_time=0.60,
        )
        self.wait(1.0)

        # New label
        ctx_lbl = Text("Context-aware embedding!", font_size=24, weight=BOLD)
        ctx_lbl.set_color(C_SIGNAL)
        ctx_lbl.next_to(d_bank, DOWN, buff=0.40)
        self.play(FadeIn(ctx_lbl), run_time=0.50)
        self.wait(1.0)

        # Update title
        new_title = Text('"bank" now means RIVER bank!', font_size=34, weight=BOLD)
        new_title.set_color(C_SIGNAL)
        new_title.move_to(title2)
        self.play(Transform(title2, new_title), run_time=0.60)
        self.wait(1.0)

        # Final note
        self.play(
            Transform(attn_txt,
                      Text("Self-attention moves words based on context",
                           font_size=28, weight=BOLD).set_color(C_SIGNAL).move_to(
                           DOWN * 2.8).scale(1.2)),
            run_time=0.60,
        )
        self.wait(3.0)

        # Fade all
        p_all = ([title2, grid2, attn_txt, ctx_lbl, trail,
                  fin_lbl, nat_lbl, fin_circle, nat_circle]
                 + all_dots)
        self.play(*[FadeOut(m) for m in p_all], run_time=0.70)
        self.wait(1.0)


# ═══════════════════════════════════════════════════════════════════
#  SCENE — Dot Product Similarity between two vectors
#  manimgl a.py DotProductSimilarity -w --hd
# ═══════════════════════════════════════════════════════════════════

class DotProductSimilarity(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.22)

        def subtle_grid(xr=(-9, 10), yr=(-6, 7), op=0.08):
            g = VGroup()
            for x in range(*xr):
                sw = 2.0 if x == 0 else 0.5
                ln = Line(np.array([x, yr[0], 0]), np.array([x, yr[1], 0]),
                          stroke_width=sw)
                ln.set_color(WHITE if x == 0 else SOFT_GRAY)
                ln.set_opacity(0.22 if x == 0 else op)
                g.add(ln)
            for y in range(*yr):
                sw = 2.0 if y == 0 else 0.5
                ln = Line(np.array([xr[0], y, 0]), np.array([xr[1], y, 0]),
                          stroke_width=sw)
                ln.set_color(WHITE if y == 0 else SOFT_GRAY)
                ln.set_opacity(0.22 if y == 0 else op)
                g.add(ln)
            return g

        # Full-screen grid
        grid = subtle_grid()
        self.play(FadeIn(grid), run_time=0.40)

        # ── Two similar vectors (close angle) ──
        A_end = np.array([4.0, 2.5, 0])
        B_end = np.array([3.0, 3.5, 0])

        vec_A = Arrow(ORIGIN, A_end, buff=0, stroke_width=4.0, color=C_SIGNAL)
        vec_A.set_color(C_SIGNAL)
        vec_B = Arrow(ORIGIN, B_end, buff=0, stroke_width=4.0, color=C_POS)
        vec_B.set_color(C_POS)

        A_lbl = Tex(r"\vec{A}", font_size=34)
        A_lbl.set_color(C_SIGNAL)
        A_lbl.next_to(vec_A.get_end(), DR, buff=0.12)
        B_lbl = Tex(r"\vec{B}", font_size=34)
        B_lbl.set_color(C_POS)
        B_lbl.next_to(vec_B.get_end(), UL, buff=0.12)

        self.play(GrowArrow(vec_A), FadeIn(A_lbl), run_time=0.60)
        self.play(GrowArrow(vec_B), FadeIn(B_lbl), run_time=0.60)
        self.wait(1.0)

        # Small angle arc
        ang_A = np.arctan2(A_end[1], A_end[0])
        ang_B = np.arctan2(B_end[1], B_end[0])
        arc1 = Arc(
            start_angle=ang_A,
            angle=ang_B - ang_A,
            radius=1.5, color=C_SIGNAL, stroke_width=2.5,
        )
        theta1 = Tex(r"\theta", font_size=30)
        theta1.set_color(C_SIGNAL)
        theta1.move_to(np.array([2.0, 1.8, 0]))
        self.play(ShowCreation(arc1), FadeIn(theta1), run_time=0.50)
        self.wait(0.80)

        # Dot product formula
        formula = Tex(
            r"\vec{A} \cdot \vec{B} = |\vec{A}||\vec{B}|\cos\theta",
            font_size=36,
        )
        formula.move_to(DOWN * 2.5)
        formula.scale(1.3)
        self.play(Write(formula), run_time=0.80)
        self.wait(1.5)

        # Result: HIGH
        res1 = Text("Small angle  -->  cos(theta) ~ 1  -->  HIGH similarity",
                     font_size=22, weight=BOLD)
        res1.set_color(C_SIGNAL)
        res1.move_to(DOWN * 3.8)
        res1.scale(1.2)
        self.play(FadeIn(res1), run_time=0.50)
        self.wait(2.5)

        # ── Rotate B to be far away (large angle) ──
        B_far = np.array([-3.5, 2.0, 0])
        vec_B2 = Arrow(ORIGIN, B_far, buff=0, stroke_width=4.0, color=C_FADE)
        vec_B2.set_color(C_FADE)
        B_lbl2 = Tex(r"\vec{B}", font_size=34)
        B_lbl2.set_color(C_FADE)
        B_lbl2.next_to(vec_B2.get_end(), UL, buff=0.12)

        self.play(
            Transform(vec_B, vec_B2),
            Transform(B_lbl, B_lbl2),
            FadeOut(arc1), FadeOut(theta1), FadeOut(res1),
            run_time=1.00,
        )
        self.wait(0.50)

        # Large angle arc
        ang_B2 = np.arctan2(B_far[1], B_far[0])
        arc2 = Arc(
            start_angle=ang_A,
            angle=ang_B2 - ang_A,
            radius=1.0, color=C_FADE, stroke_width=2.5,
        )
        theta2 = Tex(r"\theta", font_size=30)
        theta2.set_color(C_FADE)
        theta2.move_to(np.array([0.0, 1.8, 0]))
        self.play(ShowCreation(arc2), FadeIn(theta2), run_time=0.50)

        res2 = Text("Large angle  -->  cos(theta) ~ 0  -->  LOW similarity",
                     font_size=22, weight=BOLD)
        res2.set_color(C_FADE)
        res2.move_to(DOWN * 3.8)
        res2.scale(1.2)
        self.play(FadeIn(res2), run_time=0.50)
        self.wait(2.5)

        # ── Rotate B to opposite direction (negative dot product) ──
        B_opp = np.array([-4.0, -2.5, 0])
        vec_B3 = Arrow(ORIGIN, B_opp, buff=0, stroke_width=4.0, color="#E74C3C")
        vec_B3.set_color("#E74C3C")
        B_lbl3 = Tex(r"\vec{B}", font_size=34)
        B_lbl3.set_color("#E74C3C")
        B_lbl3.next_to(vec_B3.get_end(), DL, buff=0.12)

        self.play(
            Transform(vec_B, vec_B3),
            Transform(B_lbl, B_lbl3),
            FadeOut(arc2), FadeOut(theta2), FadeOut(res2),
            run_time=1.00,
        )
        self.wait(0.50)

        ang_B3 = np.arctan2(B_opp[1], B_opp[0])
        arc3 = Arc(
            start_angle=ang_A,
            angle=ang_B3 - ang_A,
            radius=0.8, color="#E74C3C", stroke_width=2.5,
        )
        theta3 = Tex(r"\theta", font_size=30)
        theta3.set_color("#E74C3C")
        theta3.move_to(np.array([1.0, -0.5, 0]))
        self.play(ShowCreation(arc3), FadeIn(theta3), run_time=0.50)

        res3 = Text("Opposite  -->  cos(theta) ~ -1  -->  OPPOSITE meaning",
                     font_size=22, weight=BOLD)
        res3.set_color("#E74C3C")
        res3.move_to(DOWN * 3.8)
        res3.scale(1.2)
        self.play(FadeIn(res3), run_time=0.50)
        self.wait(3.0)

        # ── Summary ──
        self.play(
            FadeOut(vec_A), FadeOut(vec_B), FadeOut(A_lbl), FadeOut(B_lbl),
            FadeOut(arc3), FadeOut(theta3), FadeOut(res3),
            FadeOut(formula), FadeOut(grid),
            run_time=0.60,
        )

        summary = VGroup(
            Text("Dot product measures how aligned two vectors are",
                 font_size=26, weight=BOLD),
            Text("Same direction  =  high score  =  similar",
                 font_size=24, weight=BOLD),
            Text("Perpendicular  =  zero score  =  unrelated",
                 font_size=24, weight=BOLD),
            Text("Opposite  =  negative score  =  opposite meaning",
                 font_size=24, weight=BOLD),
        )
        summary[0].set_color(WHITE)
        summary[1].set_color(C_SIGNAL)
        summary[2].set_color(C_POS)
        summary[3].set_color("#E74C3C")
        summary.arrange(DOWN, buff=0.50)
        summary.scale(1.3)
        summary.move_to(ORIGIN)

        for line in summary:
            self.play(FadeIn(line, shift=UP * 0.10), run_time=0.50)
            self.wait(1.5)

        self.wait(3.0)
        self.play(FadeOut(summary), run_time=0.60)
        self.wait(1.0)

class SoftmaxScaling(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 1 — What is Softmax? Visual with animated bars
        # ══════════════════════════════════════════════════════════════
        sm_formula = Tex(
            r"\mathrm{softmax}(x_i) = \frac{e^{x_i}}{\sum_j e^{x_j}}",
            font_size=42,
        )
        sm_formula.move_to(UP * 3).scale(1.9)
        self.play(Write(sm_formula), run_time=1.00)
        self.wait(2.0)


        in_vals = [2.0, 5.0, 1.0, 3.0]
        in_colors = ["#3498DB", "#E74C3C", "#2ECC71", "#F39C12"]
        out_vals = [0.04, 0.84, 0.02, 0.11]

        in_lbl = Text("Input scores", font_size=36, weight=BOLD)
        in_lbl.set_color(SOFT_GRAY)
        in_lbl.move_to(LEFT * 4.5 + UP * 0.9).scale(1.1)
        self.play(FadeIn(in_lbl), run_time=0.30)

        in_nums = VGroup()
        for i, (v, c) in enumerate(zip(in_vals, in_colors)):
            t = Text(f"{v:.1f}", font_size=36, weight=BOLD)
            t.set_color(c)
            t.move_to(LEFT * 4.5 + DOWN * (0.0 + i * 1.19) + DOWN*0.49)
            in_nums.add(t)
            self.play(FadeIn(t), run_time=0.25)
        self.wait(0.50)

        arrow1 = Arrow(LEFT * 3.2, LEFT * 1.2, buff=0,
                        stroke_width=3.5, color=WHITE).set_color(WHITE)
        arrow1.move_to(LEFT * 2.2 + DOWN * 2.2)
        sm_txt = Text("Softmax", font_size=30).set_color(C_SOFT)
        sm_txt.next_to(arrow1, UP, buff=0.15)
        self.play(GrowArrow(arrow1), FadeIn(sm_txt), run_time=0.50)

        BAR_H = 0.55
        MAX_W = 5.5
        out_bars = VGroup()
        out_probs = VGroup()
        for i, (v, c) in enumerate(zip(out_vals, in_colors)):
            bar = Rectangle(width=v * MAX_W, height=BAR_H)
            bar.set_fill(c, opacity=0.85).set_stroke(WHITE, width=1.0)
            bar.move_to(RIGHT * 2.0 + DOWN * (0.0 + i * 1.19) + DOWN*0.49)
            bar.align_to(RIGHT * -0.2, LEFT)
            out_bars.add(bar)

            prob = Text(f"{v:.2f}", font_size=26, weight=BOLD)
            prob.set_color(c)
            prob.next_to(bar, RIGHT, buff=0.18)
            out_probs.add(prob)

        out_lbl = Text("Probabilities (sum = 1)", font_size=38, weight=BOLD)
        out_lbl.set_color(C_SIGNAL)
        out_lbl.move_to(RIGHT * 3.0 + UP * 0.87).scale(1.01)

        self.play(FadeIn(out_lbl), run_time=0.30)
        for i in range(4):
            self.play(GrowFromEdge(out_bars[i], LEFT),
                      FadeIn(out_probs[i]), run_time=0.40)
        self.wait(1.5)


        p1 = [sm_formula, in_lbl, arrow1, sm_txt, out_lbl,
              *in_nums, *out_bars, *out_probs]
        self.play(*[FadeOut(m) for m in p1], run_time=0.60)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 2 — Small vs Large: softmax spikes
        # ══════════════════════════════════════════════════════════════
        small_title = Text("Small inputs", font_size=45, weight=BOLD)
        small_title.set_color(C_SIGNAL)
        small_title.move_to(LEFT * 4.0 + UP * 3.8).scale(1.1)

        large_title = Text("Large inputs", font_size=45, weight=BOLD)
        large_title.set_color(C_FAIL)
        large_title.move_to(RIGHT * 4.0 + UP * 3.8).scale(1.1)

        self.play(FadeIn(small_title), FadeIn(large_title), run_time=0.40)

        small_in = [1.0, 1.5, 1.2]
        small_out = [0.27, 0.41, 0.32]
        large_in = [10.0, 15.0, 12.0]
        large_out = [0.01, 0.95, 0.04]
        bar_cols = ["#3498DB", "#E74C3C", "#2ECC71"]

        BARY = UP * 1.8
        BH = 0.65
        MW = 3.8

        small_bars = VGroup()
        small_lbls = VGroup()
        for i, (v, ov, c) in enumerate(zip(small_in, small_out, bar_cols)):
            num = Text(f"{v:.1f}", font_size=34, weight=BOLD).set_color(c)
            num.move_to(LEFT * 6.0 + BARY + DOWN * i * 1.22)
            bar = Rectangle(width=ov * MW, height=BH)
            bar.set_fill(c, opacity=0.85).set_stroke(WHITE, width=1.0)
            bar.move_to(LEFT * 3.5 + BARY + DOWN * i * 1.22)
            bar.align_to(LEFT * 5.2, LEFT)
            prob = Text(f"{ov:.2f}", font_size=32, weight=BOLD).set_color(c)
            prob.next_to(bar, RIGHT, buff=0.22)
            small_bars.add(bar)
            small_lbls.add(VGroup(num, prob))
            self.play(FadeIn(num), GrowFromEdge(bar, LEFT),
                      FadeIn(prob), run_time=0.30)
        self.wait(0.50)

        balanced = Text("Balanced!", font_size=40, weight=BOLD)
        balanced.set_color(C_SIGNAL)
        balanced.move_to(LEFT * 4.0 + DOWN * 1.99).scale(1.2)
        self.play(FadeIn(balanced), run_time=0.40)

        large_bars = VGroup()
        large_lbls = VGroup()
        for i, (v, ov, c) in enumerate(zip(large_in, large_out, bar_cols)):
            num = Text(f"{v:.1f}", font_size=34, weight=BOLD).set_color(c)
            num.move_to(RIGHT * 2.0 + BARY + DOWN * i * 1.22)
            bar = Rectangle(width=ov * MW, height=BH)
            bar.set_fill(c, opacity=0.85).set_stroke(WHITE, width=1.0)
            bar.move_to(RIGHT * 4.5 + BARY + DOWN * i * 1.22)
            bar.align_to(RIGHT * 2.8, LEFT)
            prob = Text(f"{ov:.2f}", font_size=32, weight=BOLD).set_color(c)
            prob.next_to(bar, RIGHT, buff=0.22)
            large_bars.add(bar)
            large_lbls.add(VGroup(num, prob))
            self.play(FadeIn(num), GrowFromEdge(bar, LEFT),
                      FadeIn(prob), run_time=0.30)
        self.wait(0.50)

        spiky = Text("Not balanced!", font_size=40, weight=BOLD)
        spiky.set_color(C_FAIL)
        spiky.move_to(RIGHT * 4.0 + DOWN * 1.99).scale(1.2)
        self.play(FadeIn(spiky), run_time=0.40)
        self.wait(2.0)

        divider = DashedLine(UP * 4.2, DOWN * 2.5, dash_length=0.15,
                              stroke_width=2.0, color=SOFT_GRAY).set_opacity(0.40)
        self.play(ShowCreation(divider), run_time=0.30)

        warn = Text("Larger inputs make softmax spike!",
                     font_size=40, weight=BOLD)
        warn.set_color(C_FAIL)
        warn.move_to(DOWN * 3.99).scale(1.2)
        self.play(FadeIn(warn), run_time=0.50)
        self.wait(3.0)


        p2 = [small_title, large_title, balanced, spiky, divider, warn,
              *small_bars, *large_bars,
              *[x for g in small_lbls for x in g],
              *[x for g in large_lbls for x in g]]
        self.play(*[FadeOut(m) for m in p2], run_time=0.60)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 3 — Variance of dot product grows with dimension
        # ══════════════════════════════════════════════════════════════

        # Assumption
        assume = Tex(
            r"q_i, k_i \sim \mathcal{N}(0, 1)",
            font_size=62,
        )
        assume.move_to(UP * 3.5).scale(1.3)
        self.play(Write(assume), run_time=0.60)
        self.wait(1.5)

        assume_note = Text("Each dimension: mean = 0, variance = 1",
                           font_size=40, weight=BOLD)
        assume_note.set_color(GREEN_B)
        assume_note.move_to(UP * 2.0).scale(1.2)
        self.play(FadeIn(assume_note), run_time=0.40)
        self.wait(2.0)

        # Each term has Var = 1
        var_each = Tex(
            r"\mathrm{Var}(q_i \cdot k_i) = 1",
            font_size=68,
        )
        var_each.move_to(UP * 0.3).scale(1.2)
        self.play(Write(var_each), run_time=0.60)
        self.wait(1.5)

        # Sum formula = d_k
        var_sum = Tex(
            r"\mathrm{Var}(q \cdot k) = \sum_{i=1}^{d_k} \mathrm{Var}(q_i k_i) = d_k",
            font_size=60,
        )
        var_sum.move_to(DOWN * 1.64).scale(1.2)
        self.play(Write(var_sum), run_time=0.80)
        self.wait(2.0)

        # Point out: this Σ is exactly Q·K^T
        qkt_link = Tex(
            r"\mathrm{This}\ \sum\ \mathrm{is\ exactly\ what}\ Q \cdot K^T\ \mathrm{computes!}",
            font_size=59,
        )
        qkt_link.set_color(C_POS)
        qkt_link.move_to(DOWN * 3.99).scale(1.2)
        self.play(FadeIn(qkt_link), run_time=0.50)
        self.wait(3.0)

        self.play(FadeOut(assume), FadeOut(assume_note),
                  FadeOut(var_each), FadeOut(var_sum),
                  FadeOut(qkt_link), run_time=0.50)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 4 — Var(cX) = c² pattern + exploding bars
        # ══════════════════════════════════════════════════════════════
        # Scaling rule
        rule = Tex(
            r"\mathrm{Var}(c \cdot X) = c^2 \cdot \mathrm{Var}(X)",
            font_size=55,
        )
        rule.move_to(UP * 3.2).scale(1.3)
        self.play(Write(rule), run_time=0.80)
        self.wait(2.0)


        scale_data = [
            ("1", "1",  C_SIGNAL),
            ("2", "4",  TEAL),
            ("3", "9",  C_POS),
            ("4", "16", "#E67E22"),
            ("8", "64", C_FAIL),
        ]
        scale_mobs = []
        for i, (c_val, result, col) in enumerate(scale_data):
            eq = Tex(
                r"\mathrm{Var}(" + c_val + r"X) = " + c_val +
                r"^2 \cdot \mathrm{Var}(X)",
                font_size=55,
            )
            eq.set_color(col)
            eq.move_to(DOWN * (-0.2 + i * 1.25)).shift(UP*0.66)
            eq.scale(1.2).shift(UP*0.4)
            self.play(Write(eq), run_time=0.40)
            self.wait(0.60)
            scale_mobs.append(eq)

        self.wait(2.0)
        p4a = [rule] + scale_mobs
        self.play(*[FadeOut(m) for m in p4a], run_time=0.60)
        self.wait(0.30)


        # Exploding bars: d_k = 4, 16, 64, 256
        var_eq2 = Tex(
            r"\mathrm{Var}(q \cdot k) = d_k",
            font_size=62,
        )
        var_eq2.move_to(UP * 3.2).scale(1.3)
        self.play(Write(var_eq2), run_time=0.60)
        self.wait(1.0)

        dk_vals = [4, 16, 64, 256]
        dk_colors = [C_SIGNAL, C_POS, "#E67E22", C_FAIL]
        MAX_BAR_H = 3.8

        bar_group = VGroup()
        for i, (dk, col) in enumerate(zip(dk_vals, dk_colors)):
            h = (dk / 256) * MAX_BAR_H + 0.25
            bar = Rectangle(width=1.2, height=h)
            bar.set_fill(col, opacity=0.80).set_stroke(WHITE, width=1.0)
            bar.move_to(LEFT * 3.75 + RIGHT * i * 2.5 + DOWN * 0.3)
            bar.align_to(DOWN * 3.1, DOWN)

            lbl = Tex(r"d_k=" + str(dk), font_size=45)
            lbl.set_color(col)
            lbl.next_to(bar, DOWN, buff=0.48).scale(1.3)

            val = Tex(r"\mathrm{Var}=" + str(dk), font_size=33)
            val.set_color(col)
            val.next_to(bar, UP, buff=0.45).scale(1.3)

            bar_group.add(VGroup(bar, lbl, val))

        for bg in bar_group:
            self.play(GrowFromEdge(bg[0], DOWN),
                      FadeIn(bg[1]), FadeIn(bg[2]), run_time=0.50)
            self.wait(0.50)
        self.wait(2.0)


        stack_warn = Text("More dimensions = larger dot products = softmax spikes!",
                          font_size=30, weight=BOLD)
        stack_warn.set_color(C_FAIL)
        stack_warn.move_to(var_eq2).scale(1.2)
        self.play(FadeIn(stack_warn),FadeOut(var_eq2) ,run_time=0.50)
        self.wait(3.0)

        p4b = [stack_warn, *bar_group]
        self.play(*[FadeOut(m) for m in p4b], run_time=0.60)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 5 — sqrt(d_k) fixes it
        # ══════════════════════════════════════════════════════════════
        prob_eq = Tex(
            r"\mathrm{Var}(q \cdot k) = d_k",
            font_size=62,
        )
        prob_eq.set_color(C_FAIL)
        prob_eq.move_to(UP * 2.99).scale(1.3)
        prob_lbl = Text("Problem:", font_size=45, weight=BOLD)
        prob_lbl.set_color(C_FAIL)
        prob_lbl.next_to(prob_eq, LEFT, buff=0.50)
        self.play(FadeIn(prob_lbl), Write(prob_eq), run_time=0.60)
        self.wait(2.0)

        set_c = Tex(
            r"\mathrm{Divide\ by}\ \sqrt{d_k} :",
            font_size=65,
        )
        set_c.move_to(UP * 0.85).scale(1.3)
        self.play(Write(set_c), run_time=0.60)
        self.wait(1.5)

        fix_eq = Tex(
            r"\mathrm{Var}(\frac{q \cdot k}{\sqrt{d_k}}) = \frac{1}{d_k} \cdot d_k = 1",
            font_size=62,
        )
        fix_eq.set_color(C_SIGNAL)
        fix_eq.move_to(DOWN * 1.5).scale(1.3)
        self.play(Write(fix_eq), run_time=1.00)
        self.wait(2.0)

        result = Text("Variance = 1 always - softmax stays smooth!",
                       font_size=30, weight=BOLD)
        result.set_color(C_SIGNAL)
        result.move_to(DOWN * 3.75).scale(1.46)
        self.play(FadeIn(result), run_time=0.50)
        self.wait(3.0)


        p5 = [prob_lbl, prob_eq, set_c, fix_eq, result]
        self.play(*[FadeOut(m) for m in p5], run_time=0.60)
        self.wait(0.30)



        # ══════════════════════════════════════════════════════════════
        # PHASE 6 — Before/after bars + final formula
        # ══════════════════════════════════════════════════════════════
        bf_title = Text("Without scaling", font_size=38, weight=BOLD)
        bf_title.set_color(C_FAIL).move_to(LEFT * 4.0 + UP * 3.5).scale(1.1)
        af_title = Tex(r"\mathrm{With}\ /\sqrt{d_k}", font_size=38)
        af_title.set_color(C_SIGNAL).move_to(RIGHT * 4.0 + UP * 3.5).scale(1.4)
        self.play(FadeIn(bf_title), FadeIn(af_title), run_time=0.40)

        before_vals = [0.01, 0.95, 0.04]
        after_vals = [0.21, 0.52, 0.27]
        bcols = ["#3498DB", "#E74C3C", "#2ECC71"]
        BW = 3.2

        bf_bars = VGroup()
        af_bars = VGroup()
        for i, (bv, av, c) in enumerate(zip(before_vals, after_vals, bcols)):
            bb = Rectangle(width=bv * BW, height=0.60)
            bb.set_fill(c, opacity=0.85).set_stroke(WHITE, width=1.0)
            bb.move_to(LEFT * 4.0 + UP * (1.8 - i * 1.2))
            bb.align_to(LEFT * 5.5, LEFT)
            bp = Text(f"{bv:.2f}", font_size=32, weight=BOLD).set_color(c)
            bp.next_to(bb, RIGHT, buff=0.22)
            bf_bars.add(VGroup(bb, bp))

            ab = Rectangle(width=av * BW, height=0.60)
            ab.set_fill(c, opacity=0.85).set_stroke(WHITE, width=1.0)
            ab.move_to(RIGHT * 4.0 + UP * (1.8 - i * 1.2))
            ab.align_to(RIGHT * 2.2, LEFT)
            ap = Text(f"{av:.2f}", font_size=32, weight=BOLD).set_color(c)
            ap.next_to(ab, RIGHT, buff=0.22)
            af_bars.add(VGroup(ab, ap))

        for i in range(3):
            self.play(
                GrowFromEdge(bf_bars[i][0], LEFT), FadeIn(bf_bars[i][1]),
                GrowFromEdge(af_bars[i][0], LEFT), FadeIn(af_bars[i][1]),
                run_time=0.40,
            )
        self.wait(1.0)

        spiky2 = Text("Spiky!", font_size=40, weight=BOLD)
        spiky2.set_color(C_FAIL).move_to(LEFT * 4.0 + DOWN * 1.8).scale(1.1)
        smooth2 = Text("Smooth!", font_size=40, weight=BOLD)
        smooth2.set_color(C_SIGNAL).move_to(RIGHT * 4.0 + DOWN * 1.8).scale(1.1)
        self.play(FadeIn(spiky2), FadeIn(smooth2), run_time=0.40)
        self.wait(2.0)

        # Final formula
        final_eq = Tex(
            r"Attention = Softmax(\frac{Q \cdot K^T}{\sqrt{d_k}}) \cdot V",
            font_size=42,
        )
        final_eq.move_to(DOWN * 3.86).scale(1.73)
        self.play(Write(final_eq), run_time=1.00)
        self.wait(3.0)

        p6 = [bf_title, af_title, spiky2, smooth2, final_eq,
              *bf_bars, *af_bars]
        self.play(*[FadeOut(m) for m in p6], run_time=0.70)
        self.wait(1.0)



# ═══════════════════════════════════════════════════════════════════
#  SCENE — Positional Encoding


# ═══════════════════════════════════════════════════════════════════
#  SCENE — Positional Encoding (detailed visual)
#  manimgl a.py PositionalEncoding -w -l
# ═══════════════════════════════════════════════════════════════════

class PositionalEncoding(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.15)

        # ── Constants ────────────────────────────────────────────────
        C_DOG   = "#2ECC71"
        C_BITES = "#E74C3C"
        C_MAN   = "#3498DB"
        C_PE    = "#9B59B6"
        emb_colors = [C_DOG, C_BITES, C_MAN]
        words = ["Dog", "bites", "man"]
        SZ = 0.50
        N_DIM = 4  # 4-dimensional embeddings

        FS_TITLE = 44
        FS_BODY  = 34
        FS_SMALL = 28
        FS_TINY  = 24

        def make_h_block(col, sz=SZ, n=N_DIM):
            row = VGroup()
            for j in range(n):
                sq = Square(side_length=sz)
                sq.set_fill(col, opacity=1.0)
                sq.set_stroke(WHITE, width=1.0)
                row.add(sq)
            row.arrange(RIGHT, buff=0)
            return row

        # ══════════════════════════════════════════════════════════════
        # PHASE 1 — "Dog bites man" + embeddings — no position info
        # ══════════════════════════════════════════════════════════════
        cards = VGroup()
        for w, c in zip(words, emb_colors):
            lb = Text(w, font_size=56, weight=BOLD)
            lb.set_color(WHITE)
            bg = RoundedRectangle(
                width=lb.get_width() + 0.60, height=0.90,
                corner_radius=0.10,
            )
            bg.set_fill(c, opacity=0.85)
            bg.set_stroke(WHITE, width=1.5)
            lb.move_to(bg)
            cards.add(VGroup(bg, lb))
        cards.arrange(RIGHT, buff=1.80)
        cards.move_to(UP * 2)

        emb_vecs = VGroup()
        for i, c in enumerate(emb_colors):
            row = make_h_block(c)
            row.next_to(cards[i], DOWN, buff=0.30)
            emb_vecs.add(row)

        self.play(
            LaggedStart(*[FadeIn(c, shift=DOWN * 0.10) for c in cards],
                        lag_ratio=0.08, run_time=0.70),
        )
        self.wait(0.30)
        self.play(
            LaggedStart(*[FadeIn(v, shift=DOWN * 0.10) for v in emb_vecs],
                        lag_ratio=0.08, run_time=0.60),
        )
        self.wait(1.0)


        prob = Text("No position information!",
                    font_size=FS_BODY*1.7, weight=BOLD)
        prob.set_color(C_FAIL)
        prob.next_to(emb_vecs, DOWN, buff=1.5)
        self.play(FadeIn(prob), run_time=0.50)
        self.wait(1.5)

        prob2 = Text('"Dog bites man" = "man bites Dog"',
                     font_size=FS_SMALL*1.9, weight=BOLD)
        prob2.set_color(C_FAIL)
        prob2.move_to(prob).shift(DOWN*0.8)
        self.play(FadeIn(prob2), FadeOut(prob) ,run_time=0.50)
        self.wait(3.0)

        self.play(FadeOut(prob2), run_time=0.40)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 2 — Naive: position number (BLACK text in YELLOW cell)
        # ══════════════════════════════════════════════════════════════
        idea1 = Text("Idea: Add position number to embedding",
                     font_size=FS_BODY*1.35, weight=BOLD)
        idea1.set_color(C_POS)
        idea1.next_to(emb_vecs, DOWN, buff=1.5)
        self.play(FadeIn(idea1), run_time=0.50)
        self.wait(1.5)

        extra_cells = VGroup()
        for i in range(3):
            sq = Square(side_length=SZ)
            sq.set_fill(C_POS, opacity=1.0)
            sq.set_stroke(WHITE, width=1.0)
            sq.next_to(emb_vecs[i], RIGHT, buff=0)
            num = Text(str(i), font_size=FS_SMALL, weight=BOLD)
            num.set_color(BLACK)
            num.move_to(sq)
            extra_cells.add(VGroup(sq, num))

        self.play(
            LaggedStart(*[FadeIn(e, shift=RIGHT * 0.10) for e in extra_cells],
                        lag_ratio=0.10, run_time=0.60),
        )
        self.wait(2.0)

        p1 = Text("Position 500 would dominate the embedding!",
                   font_size=FS_SMALL*1.53, weight=BOLD)
        p1.set_color(C_FAIL)
        p1.next_to(idea1, DOWN, buff=0.5)
        self.play(FadeIn(p1), run_time=0.50)
        self.wait(1.5)

        p2 = Text("Sentence length 5 vs 500 — different scales!",
                   font_size=FS_SMALL*1.53, weight=BOLD)
        p2.set_color(C_FAIL)
        p2.next_to(p1, DOWN, buff=0.5)
        self.play(FadeIn(p2), run_time=0.50)
        self.wait(1.5)

        p3_text = Text("Model can't learn — scale keeps changing!",
                        font_size=FS_SMALL*1.53, weight=BOLD)
        p3_text.set_color(C_FAIL)
        p3_text.move_to(Group(p2, p1).get_center())
        self.play(FadeIn(p3_text), FadeOut(p1), FadeOut(p2), run_time=0.50)
        self.wait(2.5)



        cross1 = Line(
            idea1.get_corner(UL) + UL * 0.05,
            idea1.get_corner(DR) + DR * 0.05,
            stroke_width=4.0, color=C_FAIL,
        )
        cross2 = Line(
            idea1.get_corner(DL) + UL * 0.05,
            idea1.get_corner(UR) + DR * 0.05,
            stroke_width=4.0, color=C_FAIL,
        )
        self.play(ShowCreation(cross2), run_time=0.40)
        self.play(ShowCreation(cross1), run_time=0.40)
        self.wait(1.5)

        self.play(FadeOut(idea1), FadeOut(cross1), FadeOut(cross2), FadeOut(extra_cells),
                  FadeOut(p3_text), run_time=0.50)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 3 — Sin wave: bounded, show computation
        # ══════════════════════════════════════════════════════════════
        self.play(
            cards.animate.shift(UP * 1),
            emb_vecs.animate.shift(UP * 1),
            run_time=0.50,
        )



        sin_title = Text("What if we use sin(position)?",
                         font_size=FS_BODY*1.7, weight=BOLD)
        sin_title.set_color(C_SIGNAL)
        sin_title.move_to(UP * 1).shift(DOWN)

        bounded = Text("Always between -1 and 1!",
                       font_size=FS_SMALL*1.7, weight=BOLD)
        bounded.set_color(C_SIGNAL)
        bounded.next_to(sin_title, DOWN, buff=0.50)

        self.play(FadeIn(sin_title), run_time=0.40)
        self.play(FadeIn(bounded), run_time=0.30)
        self.wait(2.0)

        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[-1.3, 1.3, 0.5],
            width=12, height=3.5,
            axis_config={"stroke_width": 2.0, "color": SOFT_GRAY},
        )
        axes.move_to(DOWN * 0.99)
        x_lbl = Text("position", font_size=FS_TINY*1.66, weight=BOLD)
        x_lbl.set_color(SOFT_GRAY)
        x_lbl.next_to(axes, DOWN, buff=0.50)

        sin_graph = axes.get_graph(
            lambda x: np.sin(x),
            color=C_SIGNAL, stroke_width=3.0,
        )
        sin_lbl = Tex(r"\sin(pos)", font_size=65)
        sin_lbl.set_color(C_SIGNAL)
        sin_lbl.next_to(axes, UP, buff=0).shift(DOWN*0.53)

        self.play(FadeIn(axes), FadeIn(x_lbl), FadeOut(Group(sin_title, bounded)) ,run_time=0.40)
        self.play(ShowCreation(sin_graph), FadeIn(sin_lbl), run_time=1.00)
        self.wait(1.5)

        pos_vals = [0, 1, 2]
        sin_vals = [np.sin(0), np.sin(1), np.sin(2)]
        pos_colors = [C_DOG, C_BITES, C_MAN]
        pos_labels_txt = ["pos=0", "pos=1", "pos=2"]
        sin_results = [f"{v:.2f}" for v in sin_vals]

        dashed_mobs = []
        for i, (pos, sv, col, plbl, res) in enumerate(
            zip(pos_vals, sin_vals, pos_colors, pos_labels_txt, sin_results)
        ):
            x_pt = axes.c2p(pos, 0)
            curve_pt = axes.c2p(pos, sv)
            y_pt = axes.c2p(0, sv)

            v_dash = DashedLine(x_pt, curve_pt, dash_length=0.08,
                                stroke_width=2.0, color=col)
            h_dash = DashedLine(curve_pt, y_pt, dash_length=0.08,
                                stroke_width=2.0, color=col)
            dot = Dot(curve_pt, radius=0.10, color=col)

            p_lbl = Text(plbl, font_size=25, weight=BOLD)
            p_lbl.set_color(col)
            p_lbl.next_to(x_pt, DOWN, buff=0.23)

            r_lbl = Text(res, font_size=22, weight=BOLD)
            r_lbl.set_color(col)
            if i == 0:
                r_lbl.next_to(y_pt, LEFT, buff=0.12).shift(LEFT * 0.12)
            else:
                r_lbl.next_to(dot, UP, buff=0.12)

            self.play(ShowCreation(v_dash), run_time=0.25)
            self.play(FadeIn(dot), ShowCreation(h_dash), run_time=0.25)
            self.play(FadeIn(p_lbl), FadeIn(r_lbl), run_time=0.20)
            self.wait(0.40)

            dashed_mobs.extend([v_dash, h_dash, dot, p_lbl, r_lbl])

        self.wait(2.0)


        # ══════════════════════════════════════════════════════════════
        # PHASE 4 — Collision: sin(0) ≈ sin(2π) ≈ 0
        # ══════════════════════════════════════════════════════════════
        # Show periodicity problem — sin repeats every 2π
        # Draw the full period bracket
        period_start = axes.c2p(0, -1.1)
        period_end = axes.c2p(np.pi * 2, -1.1)
        period_brace = Brace(
            Line(period_start, period_end), DOWN, buff=0.05,
        )
        period_brace.set_color(C_FAIL)
        period_tex = Tex(r"2\pi", font_size=60)
        period_tex.set_color(C_FAIL)
        period_tex.next_to(period_brace, DOWN, buff=0.28)

        self.play(FadeIn(period_brace), FadeOut(x_lbl), FadeIn(period_tex), run_time=0.50)
        self.wait(1.99)



        collision_note = Text("Distant positions will map to same values!",
                              font_size=FS_BODY*1.2, weight=BOLD)
        collision_note.set_color(C_FAIL)
        collision_note.move_to(DOWN * 3.95)
        self.play(FadeIn(collision_note), run_time=0.50)
        self.wait(2.5)


        phase34 = [sin_lbl, collision_note,
                   period_brace, period_tex] + dashed_mobs
        self.play(*[FadeOut(m) for m in phase34], run_time=0.50)
        self.wait(0.30)


        # ══════════════════════════════════════════════════════════════
        # PHASE 5 — Add cos: (sin,cos) pair, still collides at 2π
        # ══════════════════════════════════════════════════════════════
        cos_title = Text("Add cos - now a (sin, cos) pair!",
                         font_size=FS_BODY*1.35, weight=BOLD)
        cos_title.set_color(C_POS)
        cos_title.move_to(DOWN * 3.599)
        self.play(FadeIn(cos_title), run_time=0.40)

        cos_graph = axes.get_graph(
            lambda x: np.cos(x),
            color=C_POS, stroke_width=3.0,
        )
        cos_lbl = Tex(r"\cos(pos)", font_size=50)
        cos_lbl.set_color(C_POS)
        sin_lbl2 = Tex(r"\sin(pos)", font_size=50)
        sin_lbl2.set_color(C_SIGNAL)
        lbl_grp = VGroup(sin_lbl2, cos_lbl).arrange(RIGHT, buff=0.20)
        lbl_grp.next_to(axes, UP, buff=0).shift(DOWN*0.42)

        self.play(ShowCreation(cos_graph), FadeIn(lbl_grp), run_time=0.80)
        self.wait(1.5)

        pair0 = Tex(
            r"\mathrm{pos}=0:\ (\sin=0.00,\ \cos=1.00)",
            font_size=60,
        ).set_color(C_DOG)

        pair6 = Tex(
            r"\mathrm{pos}=2\pi:\ (\sin=0.00,\ \cos=1.00)",
            font_size=60,
        ).set_color(C_FAIL)

        pair_grp = VGroup(pair0, pair6).arrange(DOWN, buff=0.30)
        pair_grp.move_to(DOWN * 3.55)

        self.play(FadeIn(pair0),FadeOut(cos_title), run_time=0.40)
        self.wait(1.8)
        self.play(FadeIn(pair6), run_time=0.40)
        self.wait(1.75)

        still_col = Text("Still collides! Same pair!",
                         font_size=FS_BODY*1.5, weight=BOLD)
        still_col.set_color(C_FAIL)
        still_col.move_to(DOWN * 3.59)
        self.play(FadeIn(still_col), FadeOut(pair0), FadeOut(pair6), run_time=0.50)
        self.wait(3.0)

        p5 = [cos_graph, lbl_grp,
              still_col, sin_graph, axes,]
        self.play(*[FadeOut(m) for m in p5], run_time=0.60)
        self.wait(1.3)

        # ══════════════════════════════════════════════════════════════
        # PHASE 6 — Multiple frequencies
        # ══════════════════════════════════════════════════════════════
        many_title = Text("Solution: Use MANY different frequencies!",
                          font_size=FS_BODY*1.28, weight=BOLD)
        many_title.set_color(C_SIGNAL)
        many_title.move_to(DOWN * 0.99)
        self.play(FadeIn(many_title), run_time=0.50)
        self.wait(2)

        # Sin waves (top)
        sin_lbl_p6 = Tex(r"\sin", font_size=60)
        sin_lbl_p6.set_color(C_SIGNAL)
        sin_lbl_p6.move_to(LEFT * 6.0 + DOWN * 0.2)

        axes_sin = Axes(
            x_range=[0, 20, 5],
            y_range=[-1.3, 1.3, 0.5],
            width=9, height=2.0,
            axis_config={"stroke_width": 1.5, "color": SOFT_GRAY},
        )
        axes_sin.move_to(DOWN * 0.39)

        # Cos waves (bottom)
        cos_lbl_p6 = Tex(r"\cos", font_size=60)
        cos_lbl_p6.set_color(C_POS)
        cos_lbl_p6.move_to(LEFT * 6.0 + DOWN * 2.8)

        axes_cos = Axes(
            x_range=[0, 20, 5],
            y_range=[-1.3, 1.3, 0.5],
            width=9, height=2.0,
            axis_config={"stroke_width": 1.5, "color": SOFT_GRAY},
        )
        axes_cos.move_to(DOWN * 2.8)

        self.play(FadeIn(axes_sin), FadeIn(sin_lbl_p6),
                  FadeIn(axes_cos), FadeIn(cos_lbl_p6), FadeOut(many_title), run_time=0.40)

        freqs = [1.0, 0.5, 0.25, 0.1]
        freq_colors = [C_SIGNAL, C_POS, "#E67E22", "#E74C3C"]
        freq_labels = ["f=1.0", "f=0.5", "f=0.25", "f=0.1"]
        sin_graphs = []
        cos_graphs = []
        freq_lbl_mobs = []

        for i, (f, col, fl) in enumerate(zip(freqs, freq_colors, freq_labels)):
            sg = axes_sin.get_graph(
                lambda x, freq=f: np.sin(x * freq),
                color=col, stroke_width=2.5,
            )
            cg = axes_cos.get_graph(
                lambda x, freq=f: np.cos(x * freq),
                color=col, stroke_width=2.5,
            )
            sin_graphs.append(sg)
            cos_graphs.append(cg)
            lbl = Text(fl, font_size=45, weight=BOLD)
            lbl.set_color(col)
            lbl.move_to(RIGHT * 6.45 + UP * (0.01 - i * 0.9))
            freq_lbl_mobs.append(lbl)
            self.play(ShowCreation(sg), ShowCreation(cg),
                      FadeIn(lbl), run_time=0.50)
            self.wait(0.30)

        self.wait(1.5)


        # Colored pair explanation: sin green, cos yellow
        p_t1 = Text("Each frequency gives a (", font_size=FS_SMALL, weight=BOLD)
        p_t1.set_color(WHITE)
        p_sin = Text("sin", font_size=FS_SMALL, weight=BOLD)
        p_sin.set_color(C_SIGNAL)
        p_comma = Text("-", font_size=FS_SMALL, weight=BOLD)
        p_comma.set_color(WHITE)
        p_cos = Text("cos", font_size=FS_SMALL, weight=BOLD)
        p_cos.set_color(C_POS)
        p_t2 = Text(") PAIR", font_size=FS_SMALL, weight=BOLD)
        p_t2.set_color(WHITE)
        pairs_note = VGroup(p_t1, p_sin, p_comma, p_cos, p_t2)
        pairs_note.arrange(RIGHT, buff=0.08)
        pairs_note.move_to(DOWN * 4.6).scale(1.53)
        self.play(FadeIn(pairs_note), self.camera.frame.animate.shift(DOWN*0.65), run_time=0.40)
        self.wait(1.5)

        stack_note = Text("We stack these pairs to build the PE vector",
                          font_size=FS_SMALL*1.44, weight=BOLD)
        stack_note.set_color(C_SIGNAL)
        stack_note.move_to(pairs_note)
        self.play(FadeIn(stack_note),FadeOut(pairs_note) ,run_time=0.40)
        self.wait(2.0)

        many_note = Text("Unique fingerprint per position!",
                         font_size=FS_SMALL*1.6, weight=BOLD)
        many_note.set_color(C_SIGNAL)
        many_note.move_to(stack_note)
        self.play(FadeIn(many_note),FadeOut(stack_note) ,run_time=0.40)
        self.wait(2.5)

        p6 = [axes_sin, axes_cos, sin_lbl_p6, cos_lbl_p6,
              many_note,
              ] + sin_graphs + cos_graphs + freq_lbl_mobs
        self.play(*[FadeOut(m) for m in p6], self.camera.frame.animate.shift(UP*0.65) ,run_time=0.60)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 7 — The formula from the paper
        # ══════════════════════════════════════════════════════════════

        pe_sin = Tex(
            r"PE_{(pos,\, 2i)} = \sin(\frac{pos}{10000^{2i/d}})",
            font_size=75,
        ).set_color(C_SIGNAL)
        pe_sin.next_to(emb_vecs, DOWN, buff=1)

        pe_cos = Tex(
            r"PE_{(pos,\, 2i+1)} = \cos(\frac{pos}{10000^{2i/d}})",
            font_size=75,
        ).set_color(C_POS)
        pe_cos.next_to(pe_sin, DOWN, buff=0.9)

        self.play(Write(pe_sin), run_time=0.80)
        self.wait(1.5)
        self.play(Write(pe_cos), run_time=0.80)
        self.wait(2.0)


        dim_note = Tex(
            r"d = 512\ \mathrm{in\ the\ original\ Transformer}",
            font_size=68,
        )
        dim_note.set_color(WHITE)
        dim_note.move_to(DOWN * 4)
        self.play(FadeIn(dim_note), run_time=0.50)
        self.wait(3.0)

        self.play(FadeOut(pe_sin), FadeOut(pe_cos),
                  FadeOut(dim_note),
                  run_time=0.60)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 8 — Compute PE for "bites" (pos=1, d=4) — NO GRAPHS
        # ══════════════════════════════════════════════════════════════
        calc_title = Text("Computing PE for 'bites' (pos=1, d=4)",
                          font_size=FS_BODY, weight=BOLD)
        calc_title.set_color(WHITE)
        calc_title.next_to(emb_vecs, DOWN, buff=1).scale(1.3).shift(DOWN*1.9)
        self.play(FadeIn(calc_title), run_time=0.40)
        self.wait(2)
        self.play(FadeOut(calc_title), run_time=0.40)

        # Actual computation
        pos = 1
        d = 4
        pe_vals = []
        for i_dim in range(d // 2):
            denom = 10000 ** (2 * i_dim / d)
            pe_vals.append(round(np.sin(pos / denom), 2))
            pe_vals.append(round(np.cos(pos / denom), 2))
        # pe_vals = [0.84, 0.54, 0.01, 1.0]

        # Show each computation step
        calc_lines = [
            (r"i=0:\ PE(1,0) = \sin(\frac{1}{10000^{0/4}}) = \sin(1) \approx 0.84", C_SIGNAL),
            (r"i=0:\ PE(1,1) = \cos(\frac{1}{10000^{0/4}}) = \cos(1) \approx 0.54", C_POS),
            (r"i=1:\ PE(1,2) = \sin(\frac{1}{10000^{2/4}}) = \sin(0.01) \approx 0.01", C_SIGNAL),
            (r"i=1:\ PE(1,3) = \cos(\frac{1}{10000^{2/4}}) = \cos(0.01) \approx 1.00", C_POS),
        ]

        calc_texs = VGroup()
        for tex_str, col in calc_lines:
            t = Tex(tex_str, font_size=32)
            t.set_color(col)
            calc_texs.add(t)

        calc_texs.arrange(DOWN, buff=0.40, aligned_edge=LEFT)
       
        calc_texs.move_to(UP * 1.0)

        calc_texs.shift(2.6*DOWN).scale(1.3)

        for ct in calc_texs:
            self.play(FadeIn(ct), run_time=0.50)
            self.wait(0.80)

        self.wait(1.5)



        pe_cells = VGroup()
        pe_val_labels = VGroup()
        for j, val in enumerate(pe_vals):
            sq = Square(side_length=1.2)
            sq.set_fill(C_PE, opacity=0.80)
            sq.set_stroke(WHITE, width=1.5)
            pe_cells.add(sq)

            vl = Text(str(val), font_size=30, weight=BOLD)
            vl.set_color(WHITE)
            pe_val_labels.add(vl)

        pe_cells.arrange(RIGHT, buff=0)
        pe_cells.move_to(DOWN * 1.2)

        for j in range(N_DIM):
            pe_val_labels[j].move_to(pe_cells[j])

        self.play(FadeOut(calc_texs), 
            LaggedStart(*[FadeIn(sq) for sq in pe_cells],
                        lag_ratio=0.08, run_time=0.50),
            LaggedStart(*[FadeIn(vl) for vl in pe_val_labels],
                        lag_ratio=0.08, run_time=0.50),
        )
        self.wait(1.0)

        # Dim labels below cells
        dim_labels_txt = ["dim 0", "dim 1", "dim 2", "dim 3"]
        dim_col = [C_SIGNAL, C_POS, C_SIGNAL, C_POS]
        dim_lbl_grp = VGroup()
        for j in range(N_DIM):
            dl = Text(dim_labels_txt[j], font_size=22, weight=BOLD)
            dl.set_color(dim_col[j])
            dl.next_to(pe_cells[j], DOWN, buff=0.10)
            dim_lbl_grp.add(dl)

        self.play(FadeIn(dim_lbl_grp), run_time=0.30)
        self.wait(1.0)

        sin_cos_note = Text("sin, cos, sin, cos - alternating!",
                            font_size=FS_SMALL*1.28, weight=BOLD)
        sin_cos_note.set_color(SOFT_GRAY)
        sin_cos_note.next_to(pe_cells, DOWN, buff=1.2).scale(1.3)
        self.play(FadeIn(sin_cos_note), run_time=0.40)
        self.wait(3.0)

        p8_all = [pe_cells, pe_val_labels, dim_lbl_grp, sin_cos_note]
        self.play(*[FadeOut(m) for m in p8_all], run_time=0.60)
        self.wait(0.30)


        # ══════════════════════════════════════════════════════════════
        # PHASE 9 — E + PE = final embedding (element-wise addition)
        # ══════════════════════════════════════════════════════════════

        add_title = Text("Element-wise Addition: E + PE",
                         font_size=FS_TITLE, weight=BOLD)
        add_title.set_color(WHITE)
        add_title.move_to(UP * 0.01).scale(1.2)
        self.play(FadeIn(add_title), run_time=0.40)
        self.wait(2)
        self.play(FadeOut(add_title), run_time=0.40)

        # Focus on "bites" (index 1)
        focus_rect = SurroundingRectangle(
            VGroup(cards[1], emb_vecs[1]), buff=0.12,
            color=C_POS, stroke_width=2.5,
        )
        self.play(ShowCreation(focus_rect), run_time=0.40)
        self.wait(1.0)

        # Show E + PE = result vertically for "bites"
        C_RESULT = "#1ABC9C"
        mid_x = ORIGIN  # center of screen

        # E row
        e_row = make_h_block(C_BITES, sz=1.1, n=N_DIM)
        e_row.move_to(mid_x)
        e_lbl = Tex(r"E", font_size=54)
        e_lbl.set_color(WHITE)
        e_lbl.next_to(e_row, LEFT, buff=0.30)

        # PE row with values
        pe_row = VGroup()
        pe_row_vals = VGroup()
        for j, val in enumerate(pe_vals):
            sq = Square(side_length=1.1)
            sq.set_fill(C_PE, opacity=0.80)
            sq.set_stroke(WHITE, width=1.5)
            pe_row.add(sq)
            vl = Text(str(val), font_size=30, weight=BOLD)
            vl.set_color(WHITE)
            pe_row_vals.add(vl)
        pe_row.arrange(RIGHT, buff=0)
        pe_row.move_to(mid_x + DOWN * 1.5)
        for j in range(N_DIM):
            pe_row_vals[j].move_to(pe_row[j])
        pe_lbl = Tex(r"PE", font_size=54)
        pe_lbl.set_color(C_PE)
        pe_lbl.next_to(pe_row, LEFT, buff=0.30)

        # + sign
        plus = Tex(r"+", font_size=54)
        plus.set_color(WHITE)
        plus.move_to(
            (e_row.get_center() + pe_row.get_center()) / 2
            + LEFT * (e_row.get_width() / 2 + 0.50)
        )

        # = sign
        eq_sign = Tex(r"=", font_size=54)
        eq_sign.set_color(WHITE)
        eq_sign.next_to(pe_row, DOWN, buff=0.25)
        eq_sign.align_to(plus, RIGHT)

        # Result row
        res_row = make_h_block(C_RESULT, sz=1.1, n=N_DIM)
        res_row.next_to(eq_sign, DOWN, buff=0.15)
        res_row.align_to(e_row, LEFT)
        res_lbl = Tex(r"E + PE", font_size=52)
        res_lbl.set_color(C_RESULT)
        res_lbl.next_to(res_row, LEFT, buff=0.20)

        # Animate
        self.play(FadeIn(e_row), FadeIn(e_lbl), run_time=0.40)
        self.wait(0.50)

        self.play(
            FadeIn(pe_row), FadeIn(pe_row_vals), FadeIn(pe_lbl),
            FadeIn(plus),
            run_time=0.50,
        )
        self.wait(1.0)

        self.play(
            FadeIn(eq_sign), FadeIn(res_row), FadeIn(res_lbl),
            run_time=0.50,
        )
        self.wait(1.0)


        # Fade the detailed E+PE view
        p_detail = [focus_rect,
                    e_row, e_lbl, pe_row, pe_row_vals, pe_lbl,
                    plus, eq_sign, res_row, res_lbl]
        self.play(*[FadeOut(m) for m in p_detail], run_time=0.50)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 9.5 — Show PE + result for ALL 3 words at once
        # ══════════════════════════════════════════════════════════════
        all_title = Text("Positional Encoding for Every Word",
                         font_size=FS_TITLE, weight=BOLD)
        all_title.set_color(WHITE)
        all_title.move_to(ORIGIN).shift(DOWN).scale(1.2)
        self.play(FadeIn(all_title), run_time=0.40)
        self.wait(2)
        self.play(FadeOut(all_title), run_time=0.40)

        # PE vectors (purple, no text inside) below each embedding
        pe_all = VGroup()
        for i in range(3):
            pv = make_h_block(C_PE, sz=SZ, n=N_DIM)
            pv.next_to(emb_vecs[i], DOWN, buff=0.25)
            pe_all.add(pv)

        # + signs
        plus_all = VGroup()
        for i in range(3):
            p = Tex(r"+", font_size=30)
            p.set_color(WHITE)
            mid = (emb_vecs[i].get_center() + pe_all[i].get_center()) / 2
            p.move_to(mid + LEFT * (emb_vecs[i].get_width() / 2 + 0.20))
            plus_all.add(p)

        # = signs
        eq_all = VGroup()
        for i in range(3):
            e = Tex(r"=", font_size=30)
            e.set_color(WHITE)
            e.next_to(pe_all[i], DOWN, buff=0.20)
            e.align_to(plus_all[i], RIGHT)
            eq_all.add(e)

        # Result vectors — color is mix of original + purple
        # Interpolate: mix(emb_color, purple, 0.5)
        def hex_to_rgb(h):
            h = h.lstrip('#')
            return [int(h[i:i+2], 16) for i in (0, 2, 4)]

        def rgb_to_hex(r, g, b):
            return "#{:02x}{:02x}{:02x}".format(int(r), int(g), int(b))

        def mix_colors(c1, c2, t=0.5):
            r1 = hex_to_rgb(c1)
            r2 = hex_to_rgb(c2)
            return rgb_to_hex(
                r1[0] * (1-t) + r2[0] * t,
                r1[1] * (1-t) + r2[1] * t,
                r1[2] * (1-t) + r2[2] * t,
            )

        result_colors = [
            mix_colors(C_DOG, C_PE, 0.4),
            mix_colors(C_BITES, C_PE, 0.4),
            mix_colors(C_MAN, C_PE, 0.4),
        ]

        res_all = VGroup()
        for i in range(3):
            rv = make_h_block(result_colors[i], sz=SZ, n=N_DIM)
            rv.next_to(eq_all[i], DOWN, buff=0.12)
            rv.align_to(emb_vecs[i], LEFT)
            res_all.add(rv)

        # Labels
        e_lbl2 = Tex(r"E", font_size=30).set_color(WHITE)
        e_lbl2.next_to(emb_vecs[0], LEFT, buff=0.25)
        pe_lbl2 = Tex(r"PE", font_size=30).set_color(C_PE)
        pe_lbl2.next_to(pe_all[0], LEFT, buff=0.25)
        res_lbl2 = Tex(r"E + PE", font_size=28).set_color(WHITE)
        res_lbl2.next_to(res_all[0], LEFT, buff=0.15)

        self.play(self.camera.frame.animate.shift(UP).scale(0.88))

        # Animate: PE vectors fade in
        self.play(
            LaggedStart(*[FadeIn(pv, shift=DOWN * 0.10) for pv in pe_all],
                        lag_ratio=0.08, run_time=0.60),
            FadeIn(pe_lbl2), FadeIn(e_lbl2),
            LaggedStart(*[FadeIn(p) for p in plus_all],
                        lag_ratio=0.08, run_time=0.40),
            
        )
        self.wait(1.0)


        # Result vectors fade in
        self.play(
            LaggedStart(*[FadeIn(rv, shift=DOWN * 0.10) for rv in res_all],
                        lag_ratio=0.08, run_time=0.60),
            LaggedStart(*[FadeIn(e) for e in eq_all],
                        lag_ratio=0.08, run_time=0.40),
            FadeIn(res_lbl2),
        )
        self.wait(1.0)


        all_note = Text("Every word now has position baked in!",
                        font_size=FS_BODY*1.23, weight=BOLD)
        all_note.set_color(C_SIGNAL)
        all_note.move_to(ORIGIN).shift(DOWN*1.4)
        self.play(FadeIn(all_note), run_time=0.50)
        self.wait(3.0)

        # Fade everything
        p_all = [*cards, *emb_vecs, *pe_all, *plus_all, *eq_all,
                 *res_all, e_lbl2, pe_lbl2, res_lbl2, all_note]
        self.play(*[FadeOut(m) for m in p_all], self.camera.frame.animate.shift(DOWN).scale(1/0.88) , run_time=0.70)
        self.wait(0.30)


        # ══════════════════════════════════════════════════════════════
        # PHASE 10 — Heatmap: Position × Depth
        # ══════════════════════════════════════════════════════════════
        heat_title = Text("Visualizing Positional Encoding",
                          font_size=FS_TITLE*1.23, weight=BOLD)
        heat_title.set_color(WHITE)
        heat_title.move_to(UP * 3)
        self.play(FadeIn(heat_title), run_time=0.40)

        # Compute PE values
        n_pos, n_dim = 50, 128
        pe_arr = np.zeros((n_pos, n_dim))
        for p in range(n_pos):
            for i_d in range(n_dim // 2):
                denom = 10000 ** (2 * i_d / n_dim)
                pe_arr[p, 2 * i_d] = np.sin(p / denom)
                pe_arr[p, 2 * i_d + 1] = np.cos(p / denom)

        # Blue-White-Red colormap
        t = (pe_arr + 1) / 2
        rgb = np.zeros((n_pos, n_dim, 3), dtype=np.uint8)
        mask_lo = t <= 0.5
        s_lo = np.clip(t / 0.5, 0, 1)
        s_hi = np.clip((t - 0.5) / 0.5, 0, 1)
        rgb[:, :, 0] = np.where(mask_lo, (s_lo * 255).astype(int), 255)
        rgb[:, :, 1] = np.where(mask_lo, (s_lo * 255).astype(int),
                                ((1 - s_hi) * 255).astype(int))
        rgb[:, :, 2] = np.where(mask_lo, 255,
                                ((1 - s_hi) * 255).astype(int))

        sc = 5
        big_rgb = np.repeat(np.repeat(rgb, sc, axis=0), sc, axis=1)

        from PIL import Image as PILImage
        import tempfile, os
        tmp_path = os.path.join(tempfile.gettempdir(), "pe_heatmap.png")
        PILImage.fromarray(big_rgb).save(tmp_path)

        heatmap = ImageMobject(tmp_path)
        heatmap.set_height(3.8)
        heatmap.move_to(LEFT * 1.0 + DOWN * 0.3).shift(DOWN*0.4+RIGHT*0.4)

        self.play(FadeIn(heatmap), run_time=1.0)
        self.wait(1.0)

        y_label = Text("Position", font_size=FS_SMALL*1.3, weight=BOLD)
        y_label.set_color(WHITE)
        y_label.rotate(PI / 2)
        y_label.next_to(heatmap, LEFT, buff=0.4)

        x_label = Text("Dimension", font_size=FS_SMALL*1.3, weight=BOLD)
        x_label.set_color(WHITE)
        x_label.next_to(heatmap, DOWN, buff=0.35)

        self.play(FadeIn(y_label), FadeIn(x_label), run_time=0.40)
        self.wait(1.0)

        # Freq annotations above heatmap
        hi_freq = Text("High freq", font_size=FS_TINY*1.45, weight=BOLD)
        hi_freq.set_color(C_SIGNAL)
        hi_freq.next_to(heatmap, UP, buff=0.24)
        hi_freq.align_to(heatmap, LEFT).shift(RIGHT * 0.2)

        lo_freq = Text("Low freq", font_size=FS_TINY*1.45, weight=BOLD)
        lo_freq.set_color("#E74C3C")
        lo_freq.next_to(heatmap, UP, buff=0.24)
        lo_freq.align_to(heatmap, RIGHT).shift(LEFT * 0.2)

        h_arrow = Arrow(
            hi_freq.get_right() + RIGHT * 0.10,
            lo_freq.get_left() + LEFT * 0.10,
            buff=0, stroke_width=2,
        )
        h_arrow.set_color(SOFT_GRAY)

        self.play(FadeIn(hi_freq), FadeIn(lo_freq),
                  ShowCreation(h_arrow), run_time=0.50)
        self.wait(1.0)

        # Color legend
        legend = VGroup()
        for val, col, lbl_str in [
            (1, "#CC0000", "+1"),
            (0, WHITE, " 0"),
            (-1, "#0000CC", "-1"),
        ]:
            sq = Square(side_length=0.6)
            sq.set_fill(col, opacity=1.0)
            sq.set_stroke(WHITE if val != 0 else GREY, width=1)
            lbl = Text(lbl_str, font_size=FS_TINY*1.45, weight=BOLD)
            lbl.set_color(WHITE)
            legend.add(VGroup(sq, lbl).arrange(RIGHT, buff=0.10))
        legend.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        legend.next_to(heatmap, RIGHT, buff=0.99)

        self.play(FadeIn(legend), run_time=0.40)
        self.wait(2.0)




        # Intuition facts — show one at a time
        facts = [
            "Each row is a unique encoding \n    for that position",
            "Nearby positions have similar patterns",
            "   Left columns (high freq) \nchange fast across positions",
            "Right columns (low freq) change slowly",
            "No two rows are identical \nevery position is unique!",
        ]
        fact_mob = Text(facts[0], font_size=FS_SMALL*1.42, weight=BOLD)
        fact_mob.set_color(YELLOW)
        fact_mob.move_to(DOWN * 4.5)
        self.play(FadeIn(fact_mob), FadeOut(heat_title) , self.camera.frame.animate.shift(DOWN*1.5).scale(0.93), run_time=0.40)
        self.wait(2.5)

        for f in facts[1:]:
            new_fact = Text(f, font_size=FS_SMALL*1.42, weight=BOLD)
            new_fact.set_color(YELLOW)
            new_fact.move_to(DOWN * 4.5)
            self.play(FadeOut(fact_mob), FadeIn(new_fact), run_time=0.40)
            fact_mob = new_fact
            self.wait(2.5)

        self.wait(2.0)

        p_heat = [ heatmap, y_label, x_label,
                  hi_freq, lo_freq, h_arrow, legend, fact_mob]
        self.play(*[FadeOut(m) for m in p_heat], run_time=0.60)
        self.wait(1.0)

class MultiHeadAttention(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.30)

        FS_TITLE = 44
        FS_BODY  = 34
        FS_SMALL = 28
        FS_TINY  = 24

        # ══════════════════════════════════════════════════════════════
        # PHASE 1 — Self-Attention Recap (brief)
        # ══════════════════════════════════════════════════════════════
        title = Text("Self-Attention Recap", font_size=62, weight=BOLD)
        title.set_color(WHITE)
        title.move_to(UP * 4).shift(DOWN*0.25)
        self.play(FadeIn(title), run_time=0.40)


        q_eq = Tex(r"Q = X W_Q", font_size=48)
        q_eq.set_color(C_HEAD1)
        k_eq = Tex(r"K = X W_K", font_size=48)
        k_eq.set_color(C_HEAD4)
        v_eq = Tex(r"V = X W_V", font_size=48)
        v_eq.set_color(C_HEAD2)

        qkv_grp = VGroup(q_eq, k_eq, v_eq).arrange(RIGHT, buff=0.8)
        qkv_grp.scale(1.7)
        qkv_grp.move_to(UP * 1.52)

        self.play(Write(q_eq), run_time=0.50)
        self.wait(0.30)
        self.play(Write(k_eq), run_time=0.50)
        self.wait(0.30)
        self.play(Write(v_eq), run_time=0.50)
        self.wait(1.0)

        attn_eq = Tex(
            r"\mathrm{Attention}(Q,K,V) = \mathrm{softmax}(\frac{QK^T}{\sqrt{d_k}})\, V",
            font_size=46,
        )
        attn_eq.scale(1.64)
        attn_eq.move_to(DOWN * 1.0)
        self.play(Write(attn_eq), run_time=0.80)
        self.wait(1.5)

        one_set = Text("One set of W = ONE attention pattern",
                       font_size=FS_BODY, weight=BOLD)
        one_set.set_color(C_POS)
        one_set.scale(1.37)
        one_set.move_to(DOWN * 3.1).shift(DOWN*0.46)
        self.play(FadeIn(one_set), run_time=0.50)
        self.wait(2.0)

        self.play(FadeOut(title), FadeOut(qkv_grp), FadeOut(attn_eq),
                  FadeOut(one_set), run_time=0.50)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 2 — Sentence + images (no meaning text lines)
        # ══════════════════════════════════════════════════════════════
        words = ["He", "fed", "her", "cat", "food"]
        w_colors = ["#1ABC9C", "#E67E22", "#FF6B9D", "#2ECC71", "#9B59B6"]

        cards = VGroup()
        for w, c in zip(words, w_colors):
            lb = Text(w, font_size=52, weight=BOLD)
            lb.set_color(WHITE)
            bg = RoundedRectangle(
                width=max(lb.get_width() + 0.55, 1.3),
                height=0.85, corner_radius=0.10,
            )
            bg.set_fill(c, opacity=0.85)
            bg.set_stroke(WHITE, width=1.5)
            lb.move_to(bg)
            cards.add(VGroup(bg, lb))
        cards.arrange(RIGHT, buff=0.70)
        cards.move_to(UP * 0.5)

        def make_arc(i, j, col, sw=3.0, op=0.8):
            s = cards[i].get_top() + UP * 0.08
            e = cards[j].get_top() + UP * 0.08
            ang = -PI / 3 if i < j else PI / 3
            arc = ArcBetweenPoints(s, e, angle=ang)
            arc.set_stroke(col, width=sw, opacity=op)
            return arc

        s_title = Text("Single-Head Self-Attention",
                       font_size=51, weight=BOLD)
        s_title.set_color(WHITE)
        s_title.move_to(UP * 3.76)

        self.play(FadeIn(s_title), run_time=0.40)

        self.play(
            LaggedStart(*[FadeIn(c, shift=DOWN * 0.10) for c in cards],
                        lag_ratio=0.08, run_time=0.70),
        )
        self.wait(1.0)

        # Shift up, show images directly (no meaning text)
        self.play(
            cards.animate.shift(UP * 1.12),
            run_time=0.60,
        )
        self.wait(0.30)

        img_b = ImageMobject("b.png")
        img_b.set_height(3.5)
        img_b.move_to(LEFT * 3.5 + DOWN * 1.99)

        img_a = ImageMobject("a.png")
        img_a.set_height(3.5)
        img_a.move_to(RIGHT * 3.5 + DOWN * 1.99)

        self.play(FadeIn(img_b), run_time=0.60)
        self.wait(1.5)
        self.play(FadeIn(img_a), run_time=0.60)
        self.wait(3.0)

        self.play(FadeOut(img_b), FadeOut(img_a), run_time=0.50)
        self.play(
            cards.animate.shift(DOWN * 1.12),
            run_time=0.60,
        )
        self.wait(0.30)


        # ══════════════════════════════════════════════════════════════
        # PHASE 3 — Single head limitation + "we need both"
        # ══════════════════════════════════════════════════════════════
        single_lbl = Text("Single head captures only ONE pattern",
                          font_size=FS_SMALL*1.6, weight=BOLD)
        single_lbl.set_color(ORANGE)
        single_lbl.move_to(s_title)
        self.play(FadeIn(single_lbl), FadeOut(s_title), run_time=0.30)

        self.wait(1.2)

        arc_her_cat = make_arc(2, 3, WHITE, sw=5.0, op=0.9)
        arc_cat_food = make_arc(3, 4, WHITE, sw=1.5, op=0.25)

        self.play(ShowCreation(arc_her_cat), run_time=0.40)
        self.wait(0.50)
        self.play(ShowCreation(arc_cat_food), run_time=0.30)
        self.wait(1.5)

        captured = Text("Captured: 'her cat'",
                        font_size=50, weight=BOLD)
        captured.set_color(C_SIGNAL)
        captured.move_to(DOWN * 1.5)

        missed = Text("Missed: 'cat food'!",
                      font_size=50, weight=BOLD)
        missed.set_color(C_FAIL)
        missed.move_to(DOWN * 2.75)

        need_both = Text("We need BOTH contexts!",
                         font_size=50, weight=BOLD)
        need_both.set_color(C_POS)
        need_both.move_to(DOWN * 3.99)

        self.play(FadeIn(captured), run_time=0.40)
        self.wait(0.80)
        self.play(FadeIn(missed), run_time=0.40)
        self.wait(1.0)
        self.play(FadeIn(need_both), run_time=0.50)
        self.wait(2.5)

        self.play(FadeOut(single_lbl),
                  FadeOut(arc_her_cat), FadeOut(arc_cat_food),
                  FadeOut(captured), FadeOut(missed), FadeOut(need_both),
                  run_time=0.50)
        self.wait(1.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 4 — 2 heads with W_Q^{(1)}, W_Q^{(2)} on dummy example
        # ══════════════════════════════════════════════════════════════
        m_title = Text("Multi-Head Attention",
                       font_size=FS_TITLE*1.4, weight=BOLD)
        m_title.set_color(WHITE)
        m_title.move_to(UP * 3.75)
        self.play(FadeIn(m_title), run_time=0.40)

        # Head labels above arcs, between sentence and title
        h1_lbl = Text("Head 1: 'her cat'",
                      font_size=46, weight=BOLD)
        h1_lbl.set_color(C_HEAD1)
        h1_lbl.move_to(LEFT * 3.99 + UP * 2.3)

        h2_lbl = Text("Head 2: 'cat food'",
                      font_size=46, weight=BOLD)
        h2_lbl.set_color(C_HEAD2)
        h2_lbl.move_to(RIGHT * 3.99 + UP * 2.3)

        # Show head formulas with (i) notation
        h1_eq = Tex(
            r"\mathrm{Head\ 1:}\quad Q^{(1)} = X W_Q^{(1)} \quad K^{(1)} = X W_K^{(1)} \quad V^{(1)} = X W_V^{(1)}",
            font_size=38,
        )
        h1_eq.scale(1.6)
        h1_eq.set_color(C_HEAD1)
        h1_eq.move_to(DOWN * 1.8)

        h2_eq = Tex(
            r"\mathrm{Head\ 2:}\quad Q^{(2)} = X W_Q^{(2)} \quad K^{(2)} = X W_K^{(2)} \quad V^{(2)} = X W_V^{(2)}",
            font_size=38,
        )
        h2_eq.scale(1.6)
        h2_eq.set_color(C_HEAD2)
        h2_eq.move_to(DOWN * 3.6)

        # Head 1 arc: "her" <-> "cat"
        h1_arc = make_arc(2, 3, C_HEAD1, sw=5.0, op=0.9)

        self.play(ShowCreation(h1_arc), FadeIn(h1_lbl), run_time=0.50)
        self.play(FadeIn(h1_eq), run_time=0.40)
        self.wait(2.0)


        # Head 2 arc: "cat" <-> "food"
        h2_arc = make_arc(3, 4, C_HEAD2, sw=5.0, op=0.9)

        self.play(ShowCreation(h2_arc), FadeIn(h2_lbl), run_time=0.50)
        self.play(FadeIn(h2_eq), run_time=0.40)
        self.wait(2.5)

        # FadeOut formulas, then show summary notes
        self.play(FadeOut(h1_eq), FadeOut(h2_eq), run_time=0.40)
        self.wait(0.30)

        both_note = Text("Both meanings captured!",
                         font_size=50, weight=BOLD)
        both_note.set_color(C_SIGNAL)
        both_note.move_to(DOWN * 2.0)

        subspace = Text("Each Head attends to a different subspace",
                        font_size=47, weight=BOLD)
        subspace.set_color(C_POS)
        subspace.move_to(DOWN * 3.6)

        self.play(FadeIn(both_note), run_time=0.40)
        self.wait(1.0)
        self.play(FadeIn(subspace), run_time=0.40)
        self.wait(3.0)

        self.play(FadeOut(h1_arc), FadeOut(h2_arc),
                  FadeOut(h1_lbl), FadeOut(h2_lbl),
                  FadeOut(both_note), FadeOut(subspace),
                  FadeOut(m_title),
                  *[FadeOut(c) for c in cards],
                  run_time=0.50)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 4.5 — Detailed pipeline: data flow with dimensions
        # ══════════════════════════════════════════════════════════════

        head_colors = [C_HEAD1, C_HEAD2]
        BAR_W = 6   # full d_model width
        DK_W  = 3   # exactly half = d_k width
        BAR_H = 0.60  # consistent height for all bars

        # -- Step 1: Show E as a wide bar --
        e_bar = Rectangle(width=BAR_W, height=BAR_H)
        e_bar.set_fill(C_EMB, opacity=1)
        e_bar.set_stroke(WHITE, width=2)
        e_bar.move_to(UP * 3.95)
        e_dim = Tex(r"d_{in}", font_size=35)
        e_dim.scale(1.55)
        e_dim.set_color(WHITE)
        e_dim.next_to(e_bar, DOWN, buff=0.15)
        e_lbl = Tex(r"E", font_size=54)
        e_lbl.set_color(WHITE)
        e_lbl.next_to(e_bar, LEFT, buff=0.25)

        self.play(FadeIn(e_bar), FadeIn(e_dim), FadeIn(e_lbl),
                  run_time=0.50)
        self.wait(1.5)




        e_copy1 = e_bar.copy()
        e_copy2 = e_bar.copy()
        h1_lbl = Text("Head 1", font_size=FS_SMALL*1.3, weight=BOLD)
        h1_lbl.set_color(C_HEAD1)
        h2_lbl = Text("Head 2", font_size=FS_SMALL*1.3, weight=BOLD)
        h2_lbl.set_color(C_HEAD2)

        self.play(
            e_copy1.animate.move_to(LEFT * 4.5 + UP * 1.4)
                   .set_fill(C_HEAD1, opacity=1)
                   .stretch_to_fit_width(BAR_W).stretch_to_fit_height(BAR_H),
            e_copy2.animate.move_to(RIGHT * 4.5 + UP * 1.4)
                   .set_fill(C_HEAD2, opacity=1)
                   .stretch_to_fit_width(BAR_W).stretch_to_fit_height(BAR_H),
            run_time=0.80,
        )

        h1_lbl.next_to(e_copy1, UP, buff=0.40).scale(1.2)
        h2_lbl.next_to(e_copy2, UP, buff=0.40).scale(1.2)
        self.play(FadeIn(h1_lbl), FadeIn(h2_lbl), run_time=0.30)
        self.wait(1.5)


        # -- Step 3: Each head multiplies by W_Q, W_K, W_V -> smaller Q,K,V --
        step3 = Text("Each head projects to a smaller subspace",
                      font_size=FS_SMALL*1.34, weight=BOLD)
        step3.set_color(C_POS)
        step3.move_to(UP * 2.2).shift(DOWN*2.4)
        self.play(FadeIn(step3), run_time=0.30)
        self.wait(2)
        self.play(FadeOut(step3), run_time=0.30)

        # W labels under each copy (no \times prefix)
        w1_tex = Tex(
            r"W_Q^{(1)},\ W_K^{(1)},\ W_V^{(1)}",
            font_size=22,
        )
        w1_tex.scale(1.89)
        w1_tex.set_color(C_HEAD1)
        w1_tex.next_to(e_copy1, DOWN, buff=0.32)

        w2_tex = Tex(
            r"W_Q^{(2)},\ W_K^{(2)},\ W_V^{(2)}",
            font_size=22,
        )
        w2_tex.scale(1.89)
        w2_tex.set_color(C_HEAD2)
        w2_tex.next_to(e_copy2, DOWN, buff=0.32)

        self.play(FadeIn(w1_tex), FadeIn(w2_tex), run_time=0.40)
        self.wait(1.5)

        

        # Arrows down + smaller output bars
        arr1 = Arrow(w1_tex.get_bottom(),
                     LEFT * 4.5 + DOWN * 1.6 + UP * 0.30,
                     buff=0.05, stroke_width=2.5)
        arr1.set_color(C_HEAD1)
        arr2 = Arrow(w2_tex.get_bottom(),
                     RIGHT * 4.5 + DOWN * 1.6 + UP * 0.30,
                     buff=0.05, stroke_width=2.5)
        arr2.set_color(C_HEAD2)

        h1_out = Rectangle(width=DK_W, height=BAR_H)
        h1_out.set_fill(C_HEAD1, opacity=1)
        h1_out.set_stroke(WHITE, width=2)
        h1_out.move_to(LEFT * 4.5 + DOWN * 1.6)
        dk1 = Tex(r"d_k", font_size=34)
        dk1.scale(2)
        dk1.next_to(h1_out, DOWN, buff=0.18)

        h2_out = Rectangle(width=DK_W, height=BAR_H)
        h2_out.set_fill(C_HEAD2, opacity=1)
        h2_out.set_stroke(WHITE, width=2)
        h2_out.move_to(RIGHT * 4.5 + DOWN * 1.6)
        dk2 = Tex(r"d_k", font_size=34)
        dk2.scale(2)
        dk2.next_to(h2_out, DOWN, buff=0.18)

        self.play(ShowCreation(arr1), ShowCreation(arr2),
                  run_time=0.40)
        self.play(FadeIn(h1_out), FadeIn(dk1),
                  FadeIn(h2_out), FadeIn(dk2), run_time=0.50)
        
        self.wait(1.4)

        shrink = Text("Dimension shrinks!",
                      font_size=FS_TINY*1.6, weight=BOLD)
        shrink.set_color(C_POS)
        shrink.move_to(DOWN * 0.8)
        self.play(FadeIn(shrink), run_time=0.30)
        self.wait(2.0)
        self.play(FadeOut(shrink), run_time=0.25)

        # -- Step 4: Attention inside each head (glow effect) --
        step4 = Text("Self-Attention runs inside each head",
                      font_size=FS_SMALL*1.774, weight=BOLD)
        step4.set_color(C_SIGNAL)
        step4.move_to(DOWN * 3.6)
        self.play(FadeIn(step4), run_time=0.30)

        attn1 = Text("Attention", font_size=28, weight=BOLD)
        attn1.set_color(WHITE)
        attn1.move_to(h1_out)
        attn2 = Text("Attention", font_size=28, weight=BOLD)
        attn2.set_color(WHITE)
        attn2.move_to(h2_out)

        # Glow: brighten then dim
        self.play(
            h1_out.animate.set_fill(C_HEAD1, opacity=1.0),
            h2_out.animate.set_fill(C_HEAD2, opacity=1.0),
            FadeIn(attn1), FadeIn(attn2),
            run_time=0.50,
        )
        self.wait(1.0)

        self.play(FadeOut(step4), run_time=0.25)


        # -- Step 5: Concat — outputs slide together (same y as head outputs) --
        step5 = Text("Concatenate all head outputs",
                      font_size=FS_SMALL*1.7, weight=BOLD)
        step5.set_color(YELLOW)
        step5.move_to(DOWN * 3.96)
        self.play(FadeIn(step5), run_time=0.30)

        # Keep concat at same vertical position as h1_out/h2_out (DOWN * 0.8)
        concat_y = DOWN * 1.2
        self.play(
            h1_out.animate.move_to(concat_y + LEFT * DK_W / 2),
            h2_out.animate.move_to(concat_y + RIGHT * DK_W / 2),
            attn1.animate.move_to(concat_y + LEFT * DK_W / 2),
            attn2.animate.move_to(concat_y + RIGHT * DK_W / 2),
            FadeOut(dk1), FadeOut(dk2),
            FadeOut(arr1), FadeOut(arr2),
            run_time=0.80,
        )

        concat_dim = Tex(
            r"d_k + d_k = d_{in}", font_size=45,
        )
        concat_dim.scale(1.3)
        concat_dim.set_color(WHITE)
        concat_dim.next_to(VGroup(h1_out, h2_out), DOWN, buff=0.3)

        self.play(FadeIn(concat_dim), run_time=0.40)
        self.wait(2.0)
        self.play(FadeOut(step5), run_time=0.25)

        # -- Step 6: Multiply by W^O -> final output --
        step6 = Tex(
            r"\mathrm{Multiply\ by\ } W^O",
            font_size=86,
        )
        step6.set_color(C_OUT)
        step6.move_to(DOWN* 3.86)
        self.play(FadeIn(step6), run_time=0.30)
        self.wait(1.7)


        final_bar = Rectangle(width=BAR_W, height=BAR_H)
        final_bar.set_fill(C_NORM, opacity=1)
        final_bar.set_stroke(WHITE, width=2)
        final_bar.move_to(DOWN * 3.6)
        out_dim = Tex(r"d_{in}", font_size=45).scale(1.6)
        out_dim.set_color(WHITE)
        out_dim.next_to(final_bar, DOWN, buff=0.3)
        out_lbl = Text("Output", font_size=FS_SMALL*1.7, weight=BOLD)
        out_lbl.set_color(C_NORM)
        out_lbl.next_to(final_bar, LEFT, buff=0.3)

        self.play(FadeIn(final_bar), FadeOut(step6), FadeIn(out_dim), FadeIn(out_lbl),
                  run_time=0.60)
        self.wait(1.5)


        # Fade all
        p_pipe = [e_bar, e_dim, e_lbl,
                  e_copy1, e_copy2, h1_lbl, h2_lbl,
                  w1_tex, w2_tex,
                  h1_out, h2_out, attn1, attn2,
                  concat_dim,
                  final_bar, out_dim, out_lbl]
        self.play(*[FadeOut(m) for m in p_pipe], run_time=0.60)
        self.wait(0.30)


        # ══════════════════════════════════════════════════════════════
        # PHASE 5 — General case: formulas + dimensionality
        # ══════════════════════════════════════════════════════════════
        gen_title = Text("General Multi-Head Attention",
                         font_size=FS_TITLE*1.35, weight=BOLD)
        gen_title.set_color(ORANGE)
        gen_title.move_to(UP * 3.7)
        self.play(FadeIn(gen_title), run_time=0.40)

        # General formula with (i)
        gen_eq = Tex(
            r"\mathrm{Head}_i = \mathrm{Attention}(X W_Q^{(i)},\ X W_K^{(i)},\ X W_V^{(i)})",
            font_size=75,
        )
        gen_eq.move_to(UP * 1.05)
        self.play(Write(gen_eq), run_time=0.80)
        self.wait(2.0)

        # Concat formula
        concat_eq = Tex(
            r"\mathrm{MultiHead} = \mathrm{Concat}(\mathrm{Head}_1, \ldots, \mathrm{Head}_h)\, W^O",
            font_size=75,
        )
        concat_eq.next_to(gen_eq, DOWN, buff=0.86)
        self.play(Write(concat_eq), run_time=0.80)
        self.wait(2.0)



        dim_eq1 = Tex(
            r"W_Q^{(i)} \in \mathbb{R}^{d_{in} \times d_k}",
            font_size=110,
        )
        dim_eq1.set_color(GREEN)
        dim_eq1.next_to(concat_eq, DOWN, buff=0.5).shift(DOWN*0.8)

        self.play(FadeIn(dim_eq1), run_time=0.40)
        self.wait(1.5)

        same_compute = Tex(
            r"h \times d_k = h \times \frac{d_{in}}{h} = d_{in}",
            font_size=100,
        )
        same_compute.set_color(C_SIGNAL)
        same_compute.move_to(dim_eq1)
        self.play(FadeIn(same_compute), FadeOut(dim_eq1), run_time=0.40)
        self.wait(1.5)

        same_note = Text("Same total compute as single head!",
                         font_size=FS_SMALL*2, weight=BOLD)
        same_note.set_color(C_SIGNAL)
        same_note.move_to(same_compute)
        self.play(FadeIn(same_note), FadeOut(same_compute), run_time=0.40)
        self.wait(3.0)


        self.play(FadeOut(gen_title), FadeOut(gen_eq), FadeOut(concat_eq),
                  FadeOut(same_note),
                  run_time=0.60)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 6 — Visual dimension splitting (bar -> 8 chunks)
        # ══════════════════════════════════════════════════════════════
        dim_title = Text("How Dimensions Are Split",
                         font_size=FS_TITLE*1.55, weight=BOLD)
        dim_title.set_color(ORANGE)
        dim_title.move_to(UP * 3.6)
        self.play(FadeIn(dim_title), run_time=0.40)

        h_val = 8
        head_cols = [C_HEAD1, C_HEAD2, C_HEAD3, C_HEAD4,
                     "#9B59B6", "#1ABC9C", "#E67E22", "#FF6B9D"]

        # Full bar
        full_bar = Rectangle(width=10, height=0.8)
        full_bar.set_fill(C_EMB, opacity=0.7)
        full_bar.set_stroke(WHITE, width=2)
        full_bar.move_to(UP * 1.35)
        d_lbl = Tex(r"d_{in} = 512", font_size=60)
        d_lbl.set_color(WHITE)
        d_lbl.next_to(full_bar, UP, buff=0.3)

        self.play(FadeIn(full_bar), FadeIn(d_lbl), run_time=0.50)
        self.wait(1.5)

        # Split formula
        split_eq = Tex(
            r"d_k = \frac{d_{in}}{h} = \frac{512}{8} = 64",
            font_size=62,
        )
        split_eq.set_color(C_POS)
        split_eq.scale(1.7).next_to(full_bar, DOWN, buff=1).shift(DOWN*0.55)
        self.play(Write(split_eq), run_time=0.80)
        self.wait(2.0)

        # 8 colored chunks
        chunk_w = 10 / h_val
        chunks = VGroup()
        for i in range(h_val):
            chunk = Rectangle(width=chunk_w, height=0.8)
            chunk.set_fill(head_cols[i], opacity=0.8)
            chunk.set_stroke(WHITE, width=2)
            chunks.add(chunk)
        chunks.arrange(RIGHT, buff=0)
        chunks.move_to(DOWN * 1.2)
        
        self.play(FadeOut(split_eq))
        self.play(FadeIn(chunks), run_time=0.80)
        self.wait(0.50)

        # 64 labels below + H_i labels above
        chunk_labels = VGroup()
        head_top_lbls = VGroup()
        for i in range(h_val):
            cl = Tex(r"64", font_size=50)
            cl.set_color(WHITE)
            cl.next_to(chunks[i], DOWN, buff=0.3)
            chunk_labels.add(cl)

            hl = Tex(r"H_{%d}" % (i + 1), font_size=50)
            hl.set_color(head_cols[i])
            hl.next_to(chunks[i], UP, buff=0.3)
            head_top_lbls.add(hl)

        self.play(
            LaggedStart(*[FadeIn(l) for l in chunk_labels],
                        lag_ratio=0.04, run_time=0.50),
            LaggedStart(*[FadeIn(l) for l in head_top_lbls],
                        lag_ratio=0.04, run_time=0.50),
        )
        self.wait(1.5)

        # Insights
        insight1 = Text("Each head gets 64 dimensions",
                        font_size=FS_SMALL, weight=BOLD)
        insight1.set_color(C_SIGNAL).scale(2)
        insight1.next_to(chunks, DOWN, buff=1.99)

        math_eq = Tex(
            r"h \times d_k = 8 \times 64 = 512 = d_{in}",
            font_size=79,
        )
        math_eq.set_color(WHITE)
        math_eq.move_to(insight1)

        self.play(FadeIn(insight1), run_time=0.40)
        self.wait(2.0)
        self.play(FadeOut(insight1))

        self.play(FadeIn(math_eq), run_time=0.40)
        self.wait(3.0)

        self.play(FadeOut(dim_title), FadeOut(full_bar), FadeOut(d_lbl),
                  FadeOut(chunks), FadeOut(chunk_labels),
                  FadeOut(head_top_lbls), FadeOut(math_eq),
                  run_time=0.60)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE FINAL — Summary pipeline (HORIZONTAL: left -> right)
        # ══════════════════════════════════════════════════════════════
        sum_title = Text("Multi-Head Attention - Summary",
                         font_size=FS_TITLE*1.5, weight=BOLD)
        sum_title.set_color(ORANGE)
        sum_title.move_to(UP * 3.56).scale(0.78)
        self.play(FadeIn(sum_title), run_time=0.40)

        # Input on the left
        inp_blk = make_block(LEFT * 8.0, 1.0, 2.5, C_EMB, "X", fs=FS_SMALL*2)
        self.play(FadeIn(inp_blk), run_time=0.40)
        self.wait(0.50)

        # 4 rows: Head 1, Head 2, dots, Head h
        head_y_pos = [UP * 1.5, UP * 0.5, DOWN * 0.5, DOWN * 1.5]
        sum_head_cols = [C_HEAD1, C_HEAD2, SOFT_GRAY, C_HEAD3]
        sum_head_names = ["Head 1", "Head 2", "...", "Head h"]
        head_x_pos = LEFT * 3.5
        head_blks2 = VGroup()
        inp_to_heads = VGroup()

        for i in range(4):
            if i == 2:
                dots = Tex(r":", font_size=50)
                dots.set_color(SOFT_GRAY)
                dots.move_to(head_x_pos + head_y_pos[i])
                head_blks2.add(dots)
            else:
                hb = make_block(head_x_pos + head_y_pos[i], 1.8, 0.65,
                                sum_head_cols[i], sum_head_names[i], fs=28)
                head_blks2.add(hb)

                arr = Arrow(
                    inp_blk.get_right() + RIGHT * 0.03,
                    hb.get_left() + LEFT * 0.03,
                    buff=0.05, stroke_width=2.0,
                )
                arr.set_color(sum_head_cols[i])
                inp_to_heads.add(arr)

        self.play(
            LaggedStart(*[FadeIn(h) for h in head_blks2],
                        lag_ratio=0.08, run_time=0.60),
            LaggedStart(*[ShowCreation(a) for a in inp_to_heads],
                        lag_ratio=0.08, run_time=0.50),
        )
        self.wait(1.0)

        # Concat block to the right of heads
        concat_blk2 = make_block(RIGHT * 1.0, 1.5, 2.5, C_FFN,
                                 "Concat", fs=24)
        heads_to_concat = VGroup()
        for i in [0, 1, 3]:  # skip dots
            arr = Arrow(
                head_blks2[i].get_right() + RIGHT * 0.03,
                concat_blk2.get_left() + LEFT * 0.03 + head_y_pos[i] * 0.25,
                buff=0.05, stroke_width=2.0,
            )
            arr.set_color(sum_head_cols[i])
            heads_to_concat.add(arr)

        self.play(
            FadeIn(concat_blk2),
            LaggedStart(*[ShowCreation(a) for a in heads_to_concat],
                        lag_ratio=0.10, run_time=0.50),
        )
        self.wait(0.50)

        # W^O block — BLACK text
        wo_bg2 = RoundedRectangle(width=1.2, height=0.8, corner_radius=0.12)
        wo_bg2.set_fill(C_OUT, opacity=0.88)
        wo_bg2.set_stroke(WHITE, width=2.0)
        wo_bg2.move_to(RIGHT * 4.5)
        wo_tex2 = Tex(r"W^O", font_size=43)
        wo_tex2.set_color(BLACK)
        wo_tex2.move_to(wo_bg2)
        wo_blk2 = VGroup(wo_bg2, wo_tex2)

        c_to_wo2 = Arrow(
            concat_blk2.get_right() + RIGHT * 0.03,
            wo_blk2.get_left() + LEFT * 0.03,
            buff=0.05, stroke_width=2.5,
        )
        c_to_wo2.set_color(WHITE)

        self.play(ShowCreation(c_to_wo2), FadeIn(wo_blk2), run_time=0.40)
        self.wait(0.50)

        # Output block
        out_blk2 = make_block(RIGHT * 7.5, 1.5, 0.8, C_NORM,
                              "Output", fs=24)
        wo_to_out2 = Arrow(
            wo_blk2.get_right() + RIGHT * 0.03,
            out_blk2.get_left() + LEFT * 0.03,
            buff=0.05, stroke_width=2.5,
        )
        wo_to_out2.set_color(WHITE)

        self.play(ShowCreation(wo_to_out2), FadeIn(out_blk2), run_time=0.40)
        self.wait(2.0)

        # Formula below
        formula = Tex(
            r"\mathrm{MultiHead} = \mathrm{Concat}(\mathrm{Head}_1, \ldots, \mathrm{Head}_h)\, W^O",
            font_size=80,
        )
        formula.set_color(C_POS)
        formula.move_to(DOWN * 3.74)
        self.play(FadeIn(formula), run_time=0.50)
        self.wait(4.0)

        # Fade all
        p_sum = [sum_title, inp_blk, *head_blks2, *inp_to_heads,
                 concat_blk2, *heads_to_concat,
                 c_to_wo2, wo_blk2, wo_to_out2, out_blk2,
                 formula]
        self.play(*[FadeOut(m) for m in p_sum], run_time=0.70)
        self.wait(1.0)


# ═══════════════════════════════════════════════════════════════════
#  SCENE — Masked Multi-Head Attention
#  manimgl a.py MaskedMultiHeadAttention -w --hd
# ═══════════════════════════════════════════════════════════════════

class MaskedMultiHeadAttention(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.30)

        FS_TITLE = 44
        FS_BODY  = 34
        FS_SMALL = 28
        FS_TINY  = 24

        C_SHE   = "#1ABC9C"
        C_LOVES = "#E74C3C"
        C_DANC  = "#3498DB"
        C_EVERY = "#E67E22"
        C_MASK  = "#E74C3C"
        C_OK    = "#2ECC71"
        C_BLOCK = "#FF4444"

        words = ["she", "loves", "dancing", "everyday"]
        w_colors = [C_SHE, C_LOVES, C_DANC, C_EVERY]

        # ══════════════════════════════════════════════════════════════
        # PHASE 1 — Why Masking? Autoregressive generation
        # ══════════════════════════════════════════════════════════════

        # Decoder generates one token at a time
        gen_note = Text("The decoder generates tokens one at a time",
                        font_size=FS_BODY, weight=BOLD)
        gen_note.set_color(C_POS)
        gen_note.scale(1.39).to_edge(UP).shift(DOWN*0.05)
        self.play(FadeIn(gen_note), run_time=0.50)
        self.wait(2.0)


        # Show step-by-step generation
        steps_data = [
            ("Step 1:", ["she"], "Predict first word"),
            ("Step 2:", ["she", "loves"], "Can only see 'she'"),
            ("Step 3:", ["she", "loves", "dancing"], "Can see 'she', 'loves'"),
            ("Step 4:", ["she", "loves", "dancing", "everyday"], "Can see first 3"),
        ]

        step_cards_all = VGroup()
        step_labels = VGroup()
        step_notes = VGroup()

        for si, (slbl, toks, note_txt) in enumerate(steps_data):
            sl = Text(slbl, font_size=FS_SMALL*1.3, weight=BOLD)
            sl.set_color(SOFT_GRAY)
            sl.move_to(LEFT * 7.3 + UP*1.55 + DOWN * (0.3 + si * 1.40))
            step_labels.add(sl)

            row = VGroup()
            for ti, tok in enumerate(toks):
                col_idx = ["she", "loves", "dancing", "everyday"].index(tok)
                lb = Text(tok, font_size=FS_SMALL*1.3, weight=BOLD)
                lb.set_color(WHITE)
                bg = RoundedRectangle(
                    width=max(lb.get_width() + 0.45, 1.10),
                    height=0.65, corner_radius=0.10,
                )
                bg.set_fill(w_colors[col_idx], opacity=0.85)
                bg.set_stroke(WHITE, width=1.5)
                lb.move_to(bg.get_center())
                row.add(VGroup(bg, lb))
            row.arrange(RIGHT, buff=0.36)
            row.next_to(sl, RIGHT, buff=0.40)
            step_cards_all.add(row)

            nt = Text(note_txt, font_size=FS_TINY*1.45, weight=BOLD)
            nt.set_color("#00ff00")
            nt.next_to(row, RIGHT, buff=0.40)
            step_notes.add(nt)

        for si in range(4):
            self.play(
                FadeIn(step_labels[si]),
                LaggedStart(*[FadeIn(c, shift=RIGHT * 0.10) for c in step_cards_all[si]],
                            lag_ratio=0.10, run_time=0.50),
                FadeIn(step_notes[si]),
                run_time=0.60,
            )
            self.wait(1.0)

        self.wait(1.5)


        # Key insight
        insight = Text("At each step, the model must NOT see future tokens!",
                       font_size=FS_BODY, weight=BOLD)
        insight.set_color(C_MASK)
        insight.scale(1.2)
        insight.next_to(step_cards_all, DOWN, buff=0.80).shift(RIGHT*0.85)
        self.play(FadeIn(insight), self.camera.frame.animate.shift(DOWN*0.5) ,run_time=0.50)
        self.wait(3.0)

        # Fade phase 1
        p1 = [gen_note, insight,
              *step_labels, *step_cards_all, *step_notes]
        self.play(*[FadeOut(m) for m in p1], run_time=0.50)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 2 — Visual: which tokens can attend to which
        # ══════════════════════════════════════════════════════════════
        title2 = Text("Masked Attention - Who Can See Whom?",
                      font_size=FS_TITLE * 1.23, weight=BOLD)
        title2.set_color(WHITE)
        title2.move_to(UP * 3.3)
        self.play(Write(title2), run_time=0.60)
        self.wait(0.50)

        # Word cards
        cards = VGroup()
        for w, c in zip(words, w_colors):
            lb = Text(w, font_size=48, weight=BOLD)
            lb.set_color(WHITE)
            bg = RoundedRectangle(
                width=max(lb.get_width() + 0.55, 1.30), height=0.85,
                corner_radius=0.10,
            )
            bg.set_fill(c, opacity=0.85)
            bg.set_stroke(WHITE, width=1.5)
            lb.move_to(bg.get_center())
            cards.add(VGroup(bg, lb))
        cards.arrange(RIGHT, buff=0.90)
        cards.move_to(ORIGIN).shift(DOWN*0.86)

        self.play(
            LaggedStart(*[FadeIn(c, shift=DOWN * 0.10) for c in cards],
                        lag_ratio=0.08, run_time=0.70),
        )
        self.wait(0.80)

        def make_arc(i, j, col, sw=7.0, op=0.85):
            s = cards[i].get_top() + UP * 0.08
            e = cards[j].get_top() + UP * 0.08
            ang = -PI / 3 if i < j else PI / 3
            arc = ArcBetweenPoints(s, e, angle=ang)
            arc.set_stroke(col, width=sw, opacity=op)
            return arc

        # Self-loop: curved arrow from upper-left to upper-right of card
        def self_loop(i, col):
            card = cards[i]
            ul = card.get_corner(UL) + UP * 0.06 + RIGHT * 0.12
            ur = card.get_corner(UR) + UP * 0.06 + LEFT * 0.12
            arrow = CurvedArrow(ul, ur, angle=-TAU * 0.35)
            arrow.set_color(col)
            arrow.set_stroke(width=3.5, opacity=0.85)
            return arrow

        # Token "she" — can only see itself
        lbl_0 = Text('"she" can see: itself only', font_size=FS_SMALL*1.8, weight=BOLD)
        lbl_0.set_color(C_SHE)
        lbl_0.next_to(cards, DOWN, buff=1.80)

        self_0 = self_loop(0, C_OK)
        self_0_lbl = Text("itself", font_size=FS_TINY*1.5, weight=BOLD)
        self_0_lbl.set_color(C_OK)
        self_0_lbl.next_to(self_0, UP, buff=0.35)

        self.play(FadeIn(lbl_0), run_time=0.30)
        self.play(ShowCreation(self_0), FadeIn(self_0_lbl), run_time=0.40)
        self.wait(1.5)

        # Blocked: "she" cannot see "loves", "dancing", "everyday"
        blocked_arcs_0 = [make_arc(0, j, C_BLOCK, sw=2.5, op=0.50) for j in [1, 2, 3]]
        x_marks_0 = []
        for arc in blocked_arcs_0:
            x = Tex(r"\times", font_size=66)
            x.set_color(C_BLOCK)
            x.move_to(arc.get_center() + UP * 0.30)
            x_marks_0.append(x)

        self.play(
            *[ShowCreation(a) for a in blocked_arcs_0],
            *[FadeIn(x) for x in x_marks_0],
            run_time=0.50,
        )
        self.wait(2.0)

        self.play(
            FadeOut(self_0), FadeOut(self_0_lbl), FadeOut(lbl_0),
            *[FadeOut(a) for a in blocked_arcs_0],
            *[FadeOut(x) for x in x_marks_0],
            run_time=0.40,
        )
        self.wait(0.20)

        # Token "loves" — can see "she" and itself
        lbl_1 = Text('"loves" can see: "she" and itself', font_size=FS_SMALL*1.7, weight=BOLD)
        lbl_1.set_color(C_LOVES)
        lbl_1.next_to(cards, DOWN, buff=1.80)

        arc_1_0 = make_arc(1, 0, C_OK, sw=4.0, op=0.85)
        self_1 = self_loop(1, C_OK)

        blocked_arcs_1 = [make_arc(1, j, C_BLOCK, sw=2.5, op=0.50) for j in [2, 3]]
        x_marks_1 = []
        for arc in blocked_arcs_1:
            x = Tex(r"\times", font_size=66)
            x.set_color(C_BLOCK)
            x.move_to(arc.get_center() + UP * 0.30)
            x_marks_1.append(x)

        self.play(FadeIn(lbl_1), run_time=0.30)
        self.play(
            ShowCreation(arc_1_0), ShowCreation(self_1),
            run_time=0.50,
        )
        self.wait(1.0)
        self.play(
            *[ShowCreation(a) for a in blocked_arcs_1],
            *[FadeIn(x) for x in x_marks_1],
            run_time=0.40,
        )
        self.wait(2.0)

        self.play(
            FadeOut(arc_1_0), FadeOut(self_1), FadeOut(lbl_1),
            *[FadeOut(a) for a in blocked_arcs_1],
            *[FadeOut(x) for x in x_marks_1],
            run_time=0.40,
        )
        self.wait(0.20)

        # Token "dancing" — can see "she", "loves", and itself
        lbl_2 = Text('"dancing" can see: "she", "loves" and itself', font_size=FS_SMALL*1.6, weight=BOLD)
        lbl_2.set_color(C_DANC)
        lbl_2.next_to(cards, DOWN, buff=1.80)

        arc_2_0 = make_arc(2, 0, C_OK, sw=4.0, op=0.85)
        arc_2_1 = make_arc(2, 1, C_OK, sw=4.0, op=0.85)
        self_2 = self_loop(2, C_OK)

        block_2_3 = make_arc(2, 3, C_BLOCK, sw=2.5, op=0.50)
        x_2_3 = Tex(r"\times", font_size=66)
        x_2_3.set_color(C_BLOCK)
        x_2_3.move_to(block_2_3.get_center() + UP * 0.30)

        self.play(FadeIn(lbl_2), run_time=0.30)
        self.play(
            ShowCreation(arc_2_0), ShowCreation(arc_2_1),
            ShowCreation(self_2),
            run_time=0.50,
        )
        self.wait(1.0)
        self.play(ShowCreation(block_2_3), FadeIn(x_2_3), run_time=0.40)
        self.wait(2.0)

        self.play(
            FadeOut(arc_2_0), FadeOut(arc_2_1), FadeOut(self_2),
            FadeOut(block_2_3), FadeOut(x_2_3), FadeOut(lbl_2),
            run_time=0.40,
        )
        self.wait(0.20)

        # Token "everyday" — can see all previous tokens
        lbl_3 = Text('"everyday" can see all previous tokens',
                      font_size=FS_SMALL*1.7, weight=BOLD)
        lbl_3.set_color(C_EVERY)
        lbl_3.next_to(cards, DOWN, buff=1.80)

        arc_3_0 = make_arc(3, 0, C_OK, sw=4.0, op=0.85)
        arc_3_1 = make_arc(3, 1, C_OK, sw=4.0, op=0.85)
        arc_3_2 = make_arc(3, 2, C_OK, sw=4.0, op=0.85)
        self_3  = self_loop(3, C_OK)

        self.play(FadeIn(lbl_3), run_time=0.30)
        self.play(
            ShowCreation(arc_3_0), ShowCreation(arc_3_1),
            ShowCreation(arc_3_2), ShowCreation(self_3),
            run_time=0.60,
        )
        self.wait(3.0)

        self.play(
            FadeOut(arc_3_0), FadeOut(arc_3_1), FadeOut(arc_3_2),
            FadeOut(self_3), FadeOut(lbl_3),
            run_time=0.40,
        )
        self.wait(1.20)

        # Fade phase 2 cards (keep title2 for phase 3)
        self.play(*[FadeOut(c) for c in cards], FadeOut(title2),
                  run_time=0.40)
        self.wait(1.30)


        # ══════════════════════════════════════════════════════════════
        # PHASE 3 — The Mask Matrix
        # ══════════════════════════════════════════════════════════════
        title3 = Text("The Mask Matrix", font_size=FS_TITLE * 1.65, weight=BOLD)
        title3.set_color(PINK)
        title3.move_to(UP * 3.3)
        self.play(Write(title3))
        self.wait(0.99)

        # Score matrix (before mask)
        N = len(words)
        SZ = 1.12
        score_vals = [
            ["2.1", "3.4", "1.8", "0.9"],
            ["0.5", "4.2", "2.9", "1.7"],
            ["1.3", "0.8", "3.6", "2.4"],
            ["0.7", "1.5", "2.0", "3.8"],
        ]

        score_mat = VGroup()
        for i in range(N):
            row = VGroup()
            for j in range(N):
                sq = Square(side_length=SZ)
                sq.set_fill("#2C3E50", opacity=0.90)
                sq.set_stroke(WHITE, width=1.2)
                num = Text(score_vals[i][j], font_size=30, weight=BOLD)
                num.set_color(WHITE)
                num.move_to(sq.get_center())
                row.add(VGroup(sq, num))
            row.arrange(RIGHT, buff=0)
            score_mat.add(row)
        score_mat.arrange(DOWN, buff=0)
        score_mat.move_to(LEFT * 4 + DOWN * 2)

        # Row / column labels
        row_lbls = VGroup()
        col_lbls = VGroup()
        for i, (w, c) in enumerate(zip(words, w_colors)):
            rl = Text(w, font_size=30, weight=BOLD)
            rl.set_color(c)
            rl.next_to(score_mat[i], LEFT, buff=0.25)
            row_lbls.add(rl)

            cl = Text(w, font_size=30, weight=BOLD)
            cl.set_color(c)
            cl.rotate(PI / 4)
            cl.next_to(score_mat[0][i], UP, buff=0.25)
            col_lbls.add(cl)

        self.play(
            FadeIn(score_mat),
            LaggedStart(*[FadeIn(l) for l in row_lbls], lag_ratio=0.08),
            LaggedStart(*[FadeIn(l) for l in col_lbls], lag_ratio=0.08),
            run_time=0.70,
        )
        self.wait(1.5)


        # Plus sign
        plus_sign = Tex(r"+", font_size=80)
        plus_sign.set_color(WHITE)
        plus_sign.next_to(score_mat, RIGHT, buff=0.50)

        # Mask matrix
        mask_mat = VGroup()
        for i in range(N):
            row = VGroup()
            for j in range(N):
                sq = Square(side_length=SZ)
                is_blocked = j > i
                sq.set_fill(
                    "#4A1010" if is_blocked else "#103A10",
                    opacity=0.90,
                )
                sq.set_stroke(WHITE, width=1.2)
                if is_blocked:
                    num = Tex(r"-\infty", font_size=56)
                    num.set_color(WHITE)
                else:
                    num = Text("0", font_size=45, weight=BOLD)
                    num.set_color(WHITE)
                num.move_to(sq.get_center())
                row.add(VGroup(sq, num))
            row.arrange(RIGHT, buff=0)
            mask_mat.add(row)
        mask_mat.arrange(DOWN, buff=0)
        mask_mat.next_to(plus_sign, RIGHT, buff=0.50)

        mask_lbl = Text("Mask", font_size=FS_SMALL*2, weight=BOLD)
        mask_lbl.set_color(YELLOW)
        mask_lbl.next_to(mask_mat, UP, buff=0.50)

        self.play(FadeIn(plus_sign), run_time=0.25)
        self.play(FadeIn(mask_mat), FadeIn(mask_lbl), run_time=0.60)
        self.wait(2.0)


        # Equals sign + result
        eq_sign = Tex(r"=", font_size=80)
        eq_sign.set_color(WHITE)
        eq_sign.next_to(mask_mat, RIGHT, buff=0.50)

        result_mat = VGroup()
        for i in range(N):
            row = VGroup()
            for j in range(N):
                sq = Square(side_length=SZ)
                is_blocked = j > i
                sq.set_fill(
                    "#4A1010" if is_blocked else "#2C3E50",
                    opacity=0.90,
                )
                sq.set_stroke(WHITE, width=1.2)
                if is_blocked:
                    num = Tex(r"-\infty", font_size=50)
                    num.set_color(WHITE)
                else:
                    num = Text(score_vals[i][j], font_size=35, weight=BOLD)
                    num.set_color(WHITE)
                num.move_to(sq.get_center())
                row.add(VGroup(sq, num))
            row.arrange(RIGHT, buff=0)
            result_mat.add(row)
        result_mat.arrange(DOWN, buff=0)
        result_mat.next_to(eq_sign, RIGHT, buff=0.50)

        result_lbl = Text("Masked Scores", font_size=FS_SMALL*1.7, weight=BOLD)
        result_lbl.set_color(C_POS)
        result_lbl.next_to(result_mat, UP, buff=0.50)

        self.camera.frame.save_state()

        self.play(FadeIn(eq_sign), title3.animate.shift(RIGHT*1.39) ,self.camera.frame.animate.scale(1.1).shift(RIGHT*1.05) ,run_time=0.95)
        self.play(FadeIn(result_mat), FadeIn(result_lbl), run_time=0.60)
        self.wait(3.0)


        # Fade phase 3
        p3 = [title3, score_mat, plus_sign,
              mask_mat, mask_lbl,
              eq_sign, result_mat, result_lbl,
              *row_lbls, *col_lbls]
        self.play(*[FadeOut(m) for m in p3], self.camera.frame.animate.restore() ,run_time=0.50)
        self.wait(0.30)


        # ══════════════════════════════════════════════════════════════
        # PHASE 4 — After Softmax: -inf becomes 0
        # ══════════════════════════════════════════════════════════════
        title4 = Text("After Softmax", font_size=FS_TITLE * 1.4, weight=BOLD)
        title4.set_color(WHITE)
        title4.move_to(UP * 3.44)
        self.play(Write(title4), run_time=0.50)
        self.wait(0.50)

        key_insight = Tex(
            r"\mathrm{softmax}(-\infty) = 0",
            font_size=60,
        )
        key_insight.set_color(C_MASK)
        key_insight.scale(1.5)
        key_insight.next_to(title4, DOWN, buff=0.999)
        self.play(Write(key_insight), run_time=0.70)
        self.wait(2.0)

        explain = Text("Future tokens get ZERO attention weight!",
                       font_size=FS_BODY, weight=BOLD)
        explain.set_color(C_POS)
        explain.scale(1.42)
        explain.next_to(key_insight, DOWN, buff=1.1)
        self.play(FadeIn(explain), run_time=0.50)
        self.wait(2.0)

        # Show before/after softmax matrices side by side
        bf_title = Text("Before Softmax", font_size=FS_SMALL*2, weight=BOLD)
        bf_title.set_color(C_MASK)
        bf_title.move_to(LEFT * 4.0 + UP * 2.55)

        af_title = Text("After Softmax", font_size=FS_SMALL*2, weight=BOLD)
        af_title.set_color(C_OK)
        af_title.move_to(RIGHT * 4.0 + UP * 2.55)

        self.play(FadeIn(bf_title), FadeIn(af_title),FadeOut(title4) ,FadeOut(key_insight) ,FadeOut(explain) ,run_time=0.30)

        # Before softmax matrix (same as masked scores)
        SZ2 = 1.2
        bf_mat = VGroup()
        for i in range(N):
            row = VGroup()
            for j in range(N):
                sq = Square(side_length=SZ2)
                is_blocked = j > i
                sq.set_fill(
                    "#4A1010" if is_blocked else "#2C3E50",
                    opacity=0.90,
                )
                sq.set_stroke(WHITE, width=1.2)
                if is_blocked:
                    num = Tex(r"-\infty", font_size=54)
                    num.set_color(WHITE)
                else:
                    num = Text(score_vals[i][j], font_size=37, weight=BOLD)
                    num.set_color(WHITE)
                num.move_to(sq.get_center())
                row.add(VGroup(sq, num))
            row.arrange(RIGHT, buff=0)
            bf_mat.add(row)
        bf_mat.arrange(DOWN, buff=0)
        bf_mat.next_to(bf_title, DOWN, buff=0.999).shift(LEFT*0.66)

        # After softmax matrix — each row sums to 1
        af_vals = [
            ["1.00", "0", "0", "0"],
            ["0.02", "0.98", "0", "0"],
            ["0.12", "0.07", "0.81", "0"],
            ["0.06", "0.14", "0.23", "0.57"],
        ]
        af_mat = VGroup()
        for i in range(N):
            row = VGroup()
            for j in range(N):
                sq = Square(side_length=SZ2)
                is_blocked = j > i
                val = float(af_vals[i][j])
                if is_blocked:
                    sq.set_fill("#4A1010", opacity=0.90)
                else:
                    sq.set_fill(C_OK, opacity=val * 0.80 + 0.10)
                sq.set_stroke(WHITE, width=1.2)
                num = Text(af_vals[i][j], font_size=30, weight=BOLD).set_color(WHITE)
                num.move_to(sq.get_center())
                row.add(VGroup(sq, num))
            row.arrange(RIGHT, buff=0)
            af_mat.add(row)
        af_mat.arrange(DOWN, buff=0)
        af_mat.next_to(af_title, DOWN, buff=0.99).shift(RIGHT*0.66)

        # Arrow between them
        sm_arrow = Arrow(
            bf_mat.get_right() + RIGHT * 0.10,
            af_mat.get_left() + LEFT * 0.10,
            buff=0.05, stroke_width=3.0,
        )
        sm_arrow.set_color(WHITE)
        sm_lbl = Text("Softmax", font_size=FS_TINY*1.78, weight=BOLD)
        sm_lbl.set_color(ORANGE)
        sm_lbl.next_to(sm_arrow, UP, buff=0.3)

        self.play(FadeIn(bf_mat), run_time=0.50)
        self.wait(0.50)
        self.play(GrowArrow(sm_arrow), FadeIn(sm_lbl), run_time=0.40)
        self.play(FadeIn(af_mat), run_time=0.50)
        self.wait(2.0)


        # Highlight zeros
        zero_rects = VGroup()
        for i in range(N):
            for j in range(N):
                if j > i:
                    rect = SurroundingRectangle(
                        af_mat[i][j], buff=0.02, stroke_width=2.5,
                    )
                    rect.set_color(C_BLOCK)
                    zero_rects.add(rect)

        self.play(
            *[ShowCreation(r) for r in zero_rects],
            run_time=0.50,
        )

        zero_note = Text("All future positions -> exactly 0",
                         font_size=FS_BODY*1.66, weight=BOLD)
        zero_note.set_color(C_BLOCK)
        zero_note.to_edge(DOWN).shift(DOWN*1.9)
        self.play(FadeIn(zero_note), self.camera.frame.animate.shift(DOWN*0.77) ,run_time=0.40)
        self.wait(3.0)

        # Fade phase 4
        p4 = [bf_title, af_title, bf_mat, af_mat, sm_arrow, sm_lbl, zero_rects, zero_note]
        self.play(*[FadeOut(m) for m in p4], run_time=0.50)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 5 — Full formula + comparison with regular attention
        # ══════════════════════════════════════════════════════════════

        # Regular attention formula
        reg_lbl = Text("Regular Self-Attention", font_size=FS_BODY, weight=BOLD)
        reg_lbl.set_color(C_OK)
        reg_lbl.move_to(UP * 2.2).scale(1.6)

        reg_eq = Tex(
            r"\mathrm{Attention}(Q,K,V) = \mathrm{softmax}(\frac{QK^T}{\sqrt{d_k}})\, V",
            font_size=50,
        )
        reg_eq.scale(1.5)
        reg_eq.next_to(reg_lbl, DOWN, buff=0.99)

        self.play(FadeIn(reg_lbl), run_time=0.30)
        self.play(Write(reg_eq), run_time=0.80)
        self.wait(2.0)

        # Masked attention formula
        mask_lbl = Text("Masked Self-Attention", font_size=FS_BODY, weight=BOLD)
        mask_lbl.set_color(C_MASK)
        mask_lbl.scale(1.5).next_to(reg_eq, DOWN, buff=1.1)

        mask_eq = Tex(
            r"\mathrm{Attention}(Q,K,V) = \mathrm{softmax}(\frac{QK^T}{\sqrt{d_k}} + M)\, V",
            font_size=50,
        )
        mask_eq.scale(1.5)
        mask_eq.next_to(mask_lbl, DOWN, buff=0.99)

        self.play(FadeIn(mask_lbl), run_time=0.30)
        self.play(Write(mask_eq), run_time=0.80)
        self.wait(1.5)

        # Highlight the + M difference
        m_note = Text("+ M  is the only difference!",
                      font_size=FS_BODY*1.66, weight=BOLD)
        m_note.set_color(C_POS)
        m_note.scale(1.3)
        m_note.next_to(mask_eq, DOWN, buff=1.1)

        m_rect = SurroundingRectangle(mask_eq, buff=0.12, stroke_width=3.0).scale(1.07)
        m_rect.set_color(YELLOW)

        self.play(ShowCreation(m_rect), self.camera.frame.animate.scale(1.1).shift(DOWN*0.99) ,run_time=0.40)
        self.play(FadeIn(m_note), run_time=0.40)
        self.wait(3.0)


        # Fade phase 5
        p5 = [reg_lbl, reg_eq, mask_lbl, mask_eq,
              m_rect, m_note]
        self.play(*[FadeOut(m) for m in p5], run_time=0.60)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 6 — Multi-Head: same masking in every head
        # ══════════════════════════════════════════════════════════════
        title6 = Text("Masked Multi-Head Attention",
                      font_size=FS_TITLE * 1.55, weight=BOLD)
        title6.set_color(WHITE)
        title6.move_to(UP * 2.35)
        self.play(Write(title6), run_time=0.50)
        self.wait(0.50)

        note6 = Text("Same mask applied to EVERY head independently",
                     font_size=FS_BODY, weight=BOLD)
        note6.set_color(C_POS)
        note6.scale(1.3)
        note6.next_to(title6, DOWN, buff=0.99)
        self.play(FadeIn(note6), run_time=0.40)
        self.wait(1.5)

        # Show 4 heads side by side, each with a small masked matrix
        head_colors = [C_HEAD1, C_HEAD2, C_HEAD3, C_HEAD4]
        head_names = ["Head 1", "Head 2", "Head 3", "Head 4"]
        SZ3 = 0.46

        head_groups = VGroup()
        for hi in range(4):
            hlbl = Text(head_names[hi], font_size=FS_TINY*1.18, weight=BOLD)
            hlbl.set_color(head_colors[hi])

            # Small 4x4 masked matrix
            mat = VGroup()
            for i in range(N):
                row = VGroup()
                for j in range(N):
                    sq = Square(side_length=SZ3)
                    is_blocked = j > i
                    if is_blocked:
                        sq.set_fill(C_BLOCK, opacity=0.35)
                    else:
                        sq.set_fill(head_colors[hi], opacity=0.65)
                    sq.set_stroke(WHITE, width=1.0)
                    row.add(sq)
                row.arrange(RIGHT, buff=0)
                mat.add(row)
            mat.arrange(DOWN, buff=0)

            hlbl_pos = VGroup(hlbl, mat)
            hlbl_pos.arrange(DOWN, buff=0.20)
            head_groups.add(hlbl_pos)

        head_groups.arrange(RIGHT, buff=1)
        head_groups.move_to(DOWN * 2.39).scale(1.6)

        self.play(
            LaggedStart(*[FadeIn(h, shift=UP * 0.10) for h in head_groups],
                        lag_ratio=0.12, run_time=1.00),
        )
        self.wait(2.0)

        same_mask = Text("Same triangular mask in each head",
                         font_size=FS_SMALL, weight=BOLD)
        same_mask.set_color(YELLOW)
        same_mask.scale(1.3)
        same_mask.next_to(head_groups, DOWN, buff=1).scale(1.37)
        self.play(FadeIn(same_mask), run_time=0.40)
        self.wait(2.0)

        # Final formula
        final_eq = Tex(
            r"\mathrm{MaskedMH}(Q,K,V) = \mathrm{Concat}(\mathrm{head}_1, \ldots, \mathrm{head}_h)\, W^O",
            font_size=45,
        )
        final_eq.scale(1.5)
        final_eq.set_color(C_POS)
        final_eq.move_to(same_mask)

        where_eq = Tex(
            r"\mathrm{head}_i = \mathrm{Attention}(X W_Q^{(i)},\ X W_K^{(i)},\ X W_V^{(i)},\ \mathbf{Mask})",
            font_size=44,
        )
        where_eq.scale(1.5)
        where_eq.set_color(WHITE)
        where_eq.next_to(final_eq, DOWN, buff=0.47)

        self.play(FadeOut(same_mask),self.camera.frame.animate.shift(DOWN*0.1) ,run_time=0.40)

        self.play(Write(final_eq), run_time=0.80)
        self.wait(1.0)
        self.play(Write(where_eq), run_time=0.80)
        self.wait(4.0)




# ═══════════════════════════════════════════════════════════════════
#  SCENE — Multi-Head Cross-Attention
#  manimgl a.py MultiHeadCrossAttention -w --hd
# ═══════════════════════════════════════════════════════════════════

class MultiHeadCrossAttention(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.30)

        FS_TITLE = 44
        FS_BODY  = 34
        FS_SMALL = 28
        FS_TINY  = 24

        C_A  = "#5DADE2"   # sequence A color
        C_B  = "#58D68D"   # sequence B color
        C_Q  = "#E74C3C"
        C_K  = "#F39C12"
        C_V  = "#3498DB"

        ARC_SW = 3.0

        ARC_SW = 3.0

        def cell(name, col, fs=80):
            lb = Tex(name, font_size=fs)
            lb.set_color(BLACK)
            bg = RoundedRectangle(
                width=max(lb.get_width() + 1.1, 1.1),
                height=0.9, corner_radius=0.10,
            )
            bg.set_fill(col, opacity=0.99)
            bg.set_stroke(WHITE, width=1.5)
            lb.move_to(bg.get_center())
            return VGroup(bg, lb)

        # ══════════════════════════════════════════════════════════════
        # PHASE 1 — Sequence A with self-attention arcs
        # ══════════════════════════════════════════════════════════════
        title1 = Text("Self-Attention", font_size=68, weight=BOLD)
        title1.set_color(WHITE)
        title1.move_to(UP * 3.7)
        self.play(Write(title1), run_time=0.50)
        self.wait(0.30)


        # 6 cells: a_1 ... a_6
        a_cells = VGroup(*[cell(f"a_{{{i+1}}}", TEAL) for i in range(6)])
        a_cells.arrange(RIGHT, buff=0.65)
        a_cells.move_to(ORIGIN).shift(DOWN*0.56)

        self.play(
            LaggedStart(*[FadeIn(c, shift=DOWN * 0.10) for c in a_cells],
                        lag_ratio=0.08, run_time=0.80),
        )
        self.wait(0.60)

        # Self-attention arcs: each a_i → every other a_j (no self-loop)
        sa_weights = [
            [0.0, 0.3, 0.1, 0.1, 0.2, 0.3],
            [0.2, 0.0, 0.4, 0.1, 0.1, 0.2],
            [0.1, 0.3, 0.0, 0.3, 0.2, 0.1],
            [0.1, 0.1, 0.2, 0.0, 0.4, 0.2],
            [0.2, 0.1, 0.1, 0.3, 0.0, 0.3],
            [0.3, 0.2, 0.1, 0.1, 0.3, 0.0],
        ]

        for src in range(6):
            arcs = VGroup()
            for tgt in range(6):
                if tgt == src:
                    continue
                w = sa_weights[src][tgt]
                op = w * 2.0 + 0.10
                s = a_cells[src].get_top() + UP * 0.06
                e = a_cells[tgt].get_top() + UP * 0.06
                ang = -PI / 4 if src < tgt else PI / 4
                arc = ArcBetweenPoints(s, e, angle=ang)
                arc.set_color(C_A)
                arc.set_stroke(width=ARC_SW, opacity=min(op, 1.0))
                arcs.add(arc)

            self.play(
                LaggedStart(*[ShowCreation(a) for a in arcs],
                            lag_ratio=0.06, run_time=0.45),
            )
            self.wait(0.80)
            self.play(FadeOut(arcs), run_time=0.25)

        self.wait(0.50)


        # ══════════════════════════════════════════════════════════════
        # PHASE 2 — Remove title, shift A up, add B below, cross arcs
        # ══════════════════════════════════════════════════════════════
        title2 = Text("Cross-Attention", font_size=58, weight=BOLD)
        title2.set_color(WHITE)
        title2.move_to(UP * 3.7)

        self.play(
            ReplacementTransform(title1, title2),
            a_cells.animate.move_to(UP * 1.4),
            run_time=0.60,
        )
        self.wait(0.30)

        # A label
        a_lbl = Tex(r"\mathbf{A}", font_size=86)
        a_lbl.set_color(TEAL)
        a_lbl.next_to(a_cells, LEFT, buff=0.69)

        self.play(FadeIn(a_lbl), self.camera.frame.animate.shift(LEFT*0.36) ,run_time=0.75)

        # 5 cells: b_1 ... b_5
        b_cells = VGroup(*[cell(f"b_{{{i+1}}}", YELLOW) for i in range(5)])
        b_cells.arrange(RIGHT, buff=0.50)
        b_cells.move_to(DOWN * 2.5)

        b_lbl = Tex(r"\mathbf{B}", font_size=86)
        b_lbl.set_color(YELLOW)
        b_lbl.next_to(b_cells, LEFT, buff=0.69)

        self.play(
            LaggedStart(*[FadeIn(c, shift=DOWN * 0.10) for c in b_cells],
                        lag_ratio=0.08, run_time=0.70),
            FadeIn(b_lbl),
        )
        self.wait(0.80)

        # Cross-attention arcs: each b_i → all a_j, one b at a time
        for bi in range(5):
            arcs = VGroup()
            for aj in range(6):
                # Weight: stronger for diagonal-ish
                w = 0.60 if aj == bi or aj == bi + 1 else 0.12
                op = w * 1.6 + 0.10
                arc = Arrow(
                    b_cells[bi].get_top() + UP * 0.05,
                    a_cells[aj].get_bottom() + DOWN * 0.05,
                    buff=0.06, stroke_width=ARC_SW,
                    max_tip_length_to_length_ratio=0.10,
                )
                arc.set_color(RED)
                arc.set_stroke(opacity=min(op, 1.0))
                arcs.add(arc)

            self.play(
                LaggedStart(*[GrowArrow(a) for a in arcs],
                            lag_ratio=0.05, run_time=0.50),
            )
            self.wait(1.0)
            self.play(FadeOut(arcs), run_time=0.25)

        self.wait(0.50)

        note_ca = Text("Each element in B attends to every element in A",
                       font_size=FS_SMALL*1.39, weight=BOLD)
        note_ca.set_color(GREEN)
        self.play(b_cells.animate.shift(UP), b_lbl.animate.shift(UP), run_time=0.75)
        note_ca.next_to(b_cells, DOWN, buff=1.40)
    
        self.play(FadeIn(note_ca), run_time=0.35)
        self.wait(3.0)

        # Fade phase 2
        p2 = [title2, a_cells, a_lbl, b_cells, b_lbl, note_ca]
        self.play(*[FadeOut(m) for m in p2], run_time=0.50)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 3 — Left: Self-attn (A → Q,K,V) | Right: Cross-attn
        #           (A → K,V  and  B → Q)
        # ══════════════════════════════════════════════════════════════
        title3 = Text("Where Q, K, V Come From",
                      font_size=FS_TITLE * 1.3, weight=BOLD)
        title3.set_color(WHITE)
        title3.move_to(UP * 3.7)
        self.play(Write(title3), run_time=0.50)
        self.wait(0.30)

        divider = DashedLine(UP * 2.8, DOWN * 3.0, dash_length=0.15,
                             stroke_width=2.0)
        divider.set_color(SOFT_GRAY)
        divider.set_opacity(0.40)
        self.play(ShowCreation(divider), run_time=0.30)

        # ── LEFT: Self-Attention ──
        sa_title = Text("Self-Attention", font_size=FS_BODY*1.2, weight=BOLD)
        sa_title.set_color(C_POS)
        sa_title.move_to(LEFT * 4.2 + UP * 1.8)

        # Small A sequence
        sa_a = VGroup(*[cell(f"a_{{{i+1}}}", C_A, fs=68) for i in range(4)])
        sa_a.arrange(RIGHT, buff=0.30)
        sa_a.scale(0.95)
        sa_a.next_to(sa_title, DOWN, buff=0.50)

        sa_a_lbl = Tex(r"\mathbf{A}", font_size=76)
        sa_a_lbl.set_color(C_A)
        sa_a_lbl.next_to(sa_a, LEFT, buff=0.35)

        # Arrow down to Q K V
        sa_qkv = VGroup(
            Text("Q", font_size=FS_BODY, weight=BOLD).set_color(C_Q),
            Text("K", font_size=FS_BODY, weight=BOLD).set_color(C_K),
            Text("V", font_size=FS_BODY, weight=BOLD).set_color(C_V),
        ).arrange(RIGHT, buff=0.30)
        sa_qkv.next_to(sa_a, DOWN, buff=0.80).shift(DOWN).scale(1.1*1.1)

        sa_arr = Arrow(sa_a.get_bottom() + DOWN * 0.05,
                       sa_qkv.get_top() + UP * 0.05,
                       buff=0.06, stroke_width=2.5,
                       max_tip_length_to_length_ratio=0.12)
        sa_arr.set_color(C_A)

        sa_note = Text("A generates Q, K, V", font_size=36, weight=BOLD)
        sa_note.set_color(YELLOW)
        sa_note.next_to(sa_qkv, DOWN, buff=0.40)

        self.play(FadeIn(sa_title), run_time=0.25)
        self.play(
            LaggedStart(*[FadeIn(c) for c in sa_a], lag_ratio=0.06),
            FadeIn(sa_a_lbl),
            run_time=0.50,
        )
        self.play(GrowArrow(sa_arr), FadeIn(sa_qkv), run_time=0.40)
        self.play(FadeIn(sa_note), run_time=0.30)
        self.wait(2.0)


        # ── RIGHT: Cross-Attention ──
        ca_title = Text("Cross-Attention", font_size=FS_BODY*1.2, weight=BOLD)
        ca_title.set_color(C_ATT)
        ca_title.move_to(RIGHT * 4.2 + UP * 1.8)

        # A sequence → K, V
        ca_a = VGroup(*[cell(f"a_{{{i+1}}}", C_A, fs=73) for i in range(4)])
        ca_a.arrange(RIGHT, buff=0.20)
        ca_a.scale(0.75)
        ca_a.next_to(ca_title, DOWN, buff=0.50)

        ca_a_lbl = Tex(r"\mathbf{A}", font_size=76)
        ca_a_lbl.set_color(C_A)
        ca_a_lbl.next_to(ca_a, LEFT, buff=0.35)

        ca_kv = VGroup(
            Text("K", font_size=FS_BODY, weight=BOLD).set_color(C_K),
            Text("V", font_size=FS_BODY, weight=BOLD).set_color(C_V),
        ).arrange(RIGHT, buff=0.30)
        ca_kv.next_to(ca_a, DOWN, buff=0.55).shift(DOWN*0.67)

        ca_kv_arr = Arrow(ca_a.get_bottom() + DOWN * 0.05,
                          ca_kv.get_top() + UP * 0.05,
                          buff=0.06, stroke_width=2.5,
                          max_tip_length_to_length_ratio=0.12)
        ca_kv_arr.set_color(C_A)

        # B sequence → Q
        ca_b = VGroup(*[cell(f"b_{{{i+1}}}", C_B, fs=66) for i in range(3)])
        ca_b.arrange(RIGHT, buff=0.20)
        ca_b.scale(0.75)
        ca_b.next_to(ca_kv, DOWN, buff=0.55)

        ca_b_lbl = Tex(r"\mathbf{B}", font_size=72)
        ca_b_lbl.set_color(C_B)
        ca_b_lbl.next_to(ca_b, LEFT, buff=0.35)

        ca_q = Text("Q", font_size=FS_BODY, weight=BOLD)
        ca_q.set_color(C_Q)
        ca_q.next_to(ca_b, DOWN, buff=0.9)

        ca_q_arr = Arrow(ca_b.get_bottom() + DOWN * 0.05,
                         ca_q.get_top() + UP * 0.05,
                         buff=0.06, stroke_width=2.5,
                         max_tip_length_to_length_ratio=0.12)
        ca_q_arr.set_color(C_B)

        ca_note = Text("A gives K, V\n B gives Q", font_size=40, weight=BOLD)
        ca_note.set_color(YELLOW)
        ca_note.next_to(ca_q, DOWN, buff=0.16)

        self.play(FadeIn(ca_title), self.camera.frame.animate.shift(DOWN*0.22) ,run_time=0.25)
        self.play(
            LaggedStart(*[FadeIn(c) for c in ca_a], lag_ratio=0.06),
            FadeIn(ca_a_lbl),
            run_time=0.50,
        )
        self.play(GrowArrow(ca_kv_arr), FadeIn(ca_kv), run_time=0.35)
        self.wait(0.50)
        self.play(
            LaggedStart(*[FadeIn(c) for c in ca_b], lag_ratio=0.06),
            FadeIn(ca_b_lbl),
            run_time=0.50,
        )
        self.play(GrowArrow(ca_q_arr), FadeIn(ca_q), run_time=0.35)
        self.play(FadeIn(ca_note), run_time=0.30)
        self.wait(4.0)


        # Fade phase 3
        p3 = [title3, divider,
              sa_title, sa_a, sa_a_lbl, sa_arr, sa_qkv, sa_note,
              ca_title, ca_a, ca_a_lbl, ca_kv_arr, ca_kv,
              ca_b, ca_b_lbl, ca_q_arr, ca_q, ca_note]
        self.play(*[FadeOut(m) for m in p3], run_time=0.60)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 4 — Cross-Attention formula
        # ══════════════════════════════════════════════════════════════
        title4 = Text("Cross-Attention Formula", font_size=56, weight=BOLD)
        title4.set_color(WHITE)
        title4.move_to(UP * 3.7)
        self.play(Write(title4), run_time=0.50)
        self.wait(0.30)

        # Q from B, K V from A
        src_q = Tex(r"Q = B \, W_Q", font_size=78)
        src_q.set_color(C_Q)
        src_q.move_to(UP * 1.5 + LEFT * 5.5)

        src_k = Tex(r"K = A \, W_K", font_size=78)
        src_k.set_color(C_K)
        src_k.next_to(src_q, RIGHT, buff=1.50)

        src_v = Tex(r"V = A \, W_V", font_size=78)
        src_v.set_color(C_V)
        src_v.next_to(src_k, RIGHT, buff=1.50)

        self.play(Write(src_q), run_time=0.50)
        self.wait(0.50)
        self.play(Write(src_k), run_time=0.50)
        self.wait(0.30)
        self.play(Write(src_v), run_time=0.50)
        self.wait(1.5)

        # The attention formula
        attn_eq = Tex(
            r"\mathrm{CrossAttn}(Q,K,V) = \mathrm{softmax}(\frac{Q\, K^T}{\sqrt{d_k}})\, V",
            font_size=48,
        )
        attn_eq.set_color(C_POS)
        attn_eq.scale(1.36)
        attn_eq.next_to(VGroup(src_q, src_k, src_v), DOWN, buff=1.00).shift(DOWN*0.3)

        self.play(Write(attn_eq), run_time=1.00)
        self.wait(2.0)

        same_note = Text("Same formula as self-attention - only Q source differs",
                         font_size=FS_SMALL, weight=BOLD)
        same_note.set_color(PINK)
        same_note.scale(1.29)
        same_note.next_to(attn_eq, DOWN, buff=1.40)
        self.play(FadeIn(same_note), run_time=0.40)
        self.wait(3.0)

        # Fade phase 4
        p4 = [title4, src_q, src_k, src_v, attn_eq, same_note]
        self.play(*[FadeOut(m) for m in p4], run_time=0.50)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 5 — Multi-Head Cross-Attention
        # ══════════════════════════════════════════════════════════════
        title5 = Text("Multi-Head Cross-Attention", font_size=56, weight=BOLD)
        title5.set_color(WHITE)
        title5.move_to(UP * 3.4)
        self.play(Write(title5), run_time=0.50)
        self.wait(0.30)

        # Explain: run h heads in parallel
        mh_note = Text("Run h independent attention heads in parallel",
                       font_size=FS_BODY, weight=BOLD)
        mh_note.set_color(C_POS)
        mh_note.scale(1.2)
        mh_note.next_to(title5, DOWN, buff=0.80)
        self.play(FadeIn(mh_note), run_time=0.40)
        self.wait(1.5)

        # Per-head formula
        head_eq = Tex(
            r"\mathrm{head}_i = \mathrm{Attention}(B W_Q^{(i)},\; A W_K^{(i)},\; A W_V^{(i)})",
            font_size=62,
        )
        head_eq.set_color(WHITE)
        head_eq.scale(1.36)
        head_eq.next_to(mh_note, DOWN, buff=0.990)
        self.play(Write(head_eq), run_time=0.80)
        self.wait(2.0)


        # Show h heads as colored bars
        head_colors = [C_HEAD1, C_HEAD2, C_HEAD3, C_HEAD4]
        head_bars = VGroup()
        for i in range(4):
            bar = RoundedRectangle(width=1.60, height=0.55, corner_radius=0.08)
            bar.set_fill(head_colors[i], opacity=0.80)
            bar.set_stroke(WHITE, width=1.2)
            hl = Tex(r"\mathrm{head}_{" + str(i+1) + "}", font_size=32)
            hl.set_color(WHITE)
            hl.move_to(bar.get_center())
            head_bars.add(VGroup(bar, hl))
        head_bars.arrange(RIGHT, buff=0.40)
        head_bars.next_to(head_eq, DOWN, buff=1).scale(1.8)

        self.play(
            LaggedStart(*[FadeIn(h, shift=UP * 0.10) for h in head_bars],
                        lag_ratio=0.12, run_time=0.70),
        )
        self.wait(1.5)

        # Concat + W^O
        concat_eq = Tex(
            r"\mathrm{MultiHead} = \mathrm{Concat}(\mathrm{head}_1, \ldots, \mathrm{head}_h)\, W^O",
            font_size=42,
        )
        concat_eq.set_color(C_POS)
        concat_eq.scale(1.63)
        concat_eq.next_to(head_bars, DOWN, buff=1.2)
        self.play(Write(concat_eq), run_time=0.80)
        self.wait(2.0)



# ═══════════════════════════════════════════════════════════════════
#  SCENE — Layer Normalization
#  manimgl a.py LayerNorm -w --hd
# ═══════════════════════════════════════════════════════════════════

class LayerNorm(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.30)

        FS_TITLE = 44
        FS_BODY  = 34
        FS_SMALL = 28
        FS_TINY  = 24

        C_X      = "#5DADE2"
        C_RES    = "#E67E22"
        C_MEAN   = "#F1C40F"
        C_NORM   = "#2ECC71"
        C_GAMMA  = "#F39C12"
        C_BETA   = "#9B59B6"
        C_FINAL  = "#1ABC9C"
        C_PROB   = "#E74C3C"

        # ══════════════════════════════════════════════════════════════
        # PHASE 1 — The input: x_i = x + f(x)
        # ══════════════════════════════════════════════════════════════
        title1 = Text("Layer Normalization", font_size=58, weight=BOLD)
        title1.set_color(WHITE)
        title1.move_to(UP * 3.7)
        self.play(Write(title1), run_time=0.50)
        self.wait(0.50)


        # Residual connection
        res_eq = Tex(r"x_i = x + f(x)", font_size=56)
        res_eq.set_color(C_X)
        res_eq.scale(1.4*1.4)
        res_eq.next_to(title1, DOWN, buff=1.13)
        self.play(Write(res_eq), run_time=0.70)
        self.wait(1.5)

        res_note = Text("Residual: original input + sub-layer output",
                        font_size=FS_SMALL, weight=BOLD)
        res_note.set_color(GREEN)
        res_note.next_to(res_eq, DOWN, buff=0.95).scale(1.6)
        self.play(FadeIn(res_note), run_time=0.40)
        self.wait(1.5)

        fx_note = Text("f(x) = Multi-Head Attention or Feed-Forward",
                        font_size=FS_SMALL, weight=BOLD)
        fx_note.set_color(C_RES).scale(1.44)
        fx_note.next_to(res_note, DOWN, buff=0.95)
        self.play(FadeIn(fx_note), run_time=0.40)
        self.wait(2.0)

        dim_note = Tex(
            r"x_i \in \mathbb{R}^d",
            font_size=48,
        )
        dim_note.set_color(WHITE)
        dim_note.scale(1.4*1.99)
        dim_note.next_to(fx_note, DOWN, buff=0.95)
        self.play(Write(dim_note), run_time=0.40)
        self.wait(2.5)

        p1 = [title1, res_eq, res_note, fx_note, dim_note]
        self.play(*[FadeOut(m) for m in p1], run_time=0.50)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 2 — Step 1: Compute mean, center
        # ══════════════════════════════════════════════════════════════
        title2 = Text("Step 1: Subtract the Mean", font_size=52, weight=BOLD)
        title2.set_color(WHITE)
        title2.move_to(UP * 3.7)
        self.play(Write(title2), run_time=0.50)
        self.wait(0.30)

        mean_eq = Tex(
            r"\mu = \frac{1}{d} \sum_{j=1}^{d} x_j",
            font_size=50,
        )
        mean_eq.set_color(C_MEAN)
        mean_eq.scale(1.73)
        mean_eq.next_to(title2, DOWN, buff=0.95)
        self.play(Write(mean_eq), run_time=0.60)
        self.wait(1.5)

        center_eq = Tex(r"x_j - \mu", font_size=54)
        center_eq.set_color(C_NORM)
        center_eq.scale(1.73*1.5)
        center_eq.next_to(mean_eq, DOWN, buff=0.95)
        self.play(Write(center_eq), run_time=0.50)
        self.wait(1.9)

        center_note = Text("Centers the values around zero",
                           font_size=FS_BODY, weight=BOLD)
        center_note.set_color(C_NORM)
        center_note.next_to(center_eq, DOWN, buff=1.18).scale(1.5)
        self.play(FadeIn(center_note), run_time=0.35)
        self.wait(3.0)


        p2 = [title2, mean_eq, center_eq, center_note]
        self.play(*[FadeOut(m) for m in p2], run_time=0.50)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 3 — Step 2: Divide by std + epsilon
        # ══════════════════════════════════════════════════════════════
        title3 = Text("Step 2: Divide by Standard Deviation",
                      font_size=50, weight=BOLD)
        title3.set_color(WHITE)
        title3.move_to(UP * 3.45)
        self.play(Write(title3), run_time=0.50)
        self.wait(0.30)

        var_eq = Tex(
            r"\sigma^2 = \frac{1}{d} \sum_{j=1}^{d} (x_j - \mu)^2",
            font_size=48,
        )
        var_eq.set_color(MAROON_B)
        var_eq.scale(1.2*1.2*1.2)
        var_eq.next_to(title3, DOWN, buff=1.3)
        self.play(Write(var_eq), run_time=0.60)
        self.wait(1.5)

        norm_eq = Tex(
            r"\hat{x}_j = \frac{x_j - \mu}{\sqrt{\sigma^2 + \epsilon}}",
            font_size=52,
        )
        norm_eq.set_color(C_NORM)
        norm_eq.scale(1.8)
        norm_eq.next_to(var_eq, DOWN, buff=1.2)
        self.play(Write(norm_eq), run_time=0.70)
        self.wait(1.5)

        eps_note = Tex(
            r"\epsilon \approx 10^{-5} \quad \text{prevents division by zero}",
            font_size=38,
        )
        eps_note.set_color(C_MEAN)
        eps_note.scale(2)
        eps_note.next_to(norm_eq, RIGHT, buff=1)
        self.play(FadeIn(eps_note), run_time=0.40)
        self.wait(1.5)

        

        result_note = Text("Now: mean = 0, variance = 1",
                           font_size=FS_BODY, weight=BOLD)
        result_note.set_color(ORANGE).scale(1.8)
        result_note.move_to(title3.get_center())
        self.play(FadeIn(result_note),FadeOut(title3) , run_time=0.40)
        self.wait(3.0)

        p3 = [var_eq, norm_eq, eps_note, result_note]
        self.play(*[FadeOut(m) for m in p3], run_time=0.50)
        self.wait(0.30)

        # ══════════════════════════════════════════════════════════════
        # PHASE 4 — Problem + gamma/beta fix
        # ══════════════════════════════════════════════════════════════
        title4 = Text("The Problem With Pure Normalization",
                      font_size=55, weight=BOLD)
        title4.set_color(WHITE)
        title4.move_to(UP * 3.46)
        self.play(Write(title4), run_time=0.50)
        self.wait(0.30)

        prob1 = Text("Forcing mean=0, var=1 is too restrictive!",
                     font_size=FS_BODY, weight=BOLD)
        prob1.set_color(C_PROB)
        prob1.scale(1.35)
        prob1.next_to(title4, DOWN, buff=1.28)
        self.play(FadeIn(prob1), run_time=0.40)
        self.wait(2.0)



        prob2 = Text("Some dimensions NEED larger values or non-zero mean",
                     font_size=FS_SMALL, weight=BOLD)
        prob2.set_color(C_PROB).scale(1.34)
        prob2.next_to(prob1, DOWN, buff=0.85)
        self.play(FadeIn(prob2), run_time=0.40)
        self.wait(2.0)

        fix_title = Text("Fix: Learnable Scale and Shift",
                         font_size=FS_BODY, weight=BOLD)
        fix_title.set_color(C_NORM)
        fix_title.scale(1.69)
        fix_title.next_to(prob2, DOWN, buff=0.85)
        self.play(FadeIn(fix_title), run_time=0.40)
        self.wait(1.0)

        full_eq = Tex(
            r"\mathrm{LayerNorm}(x_j) = \gamma_j \cdot \hat{x}_j + \beta_j",
            font_size=50,
        )
        full_eq.set_color(WHITE)
        full_eq.scale(1.99)
        full_eq.next_to(fix_title, DOWN, buff=1.38)

        full_eq[10:12].set_color(GREEN)
        full_eq[14:16].set_color(C_GAMMA)
        full_eq[-2:].set_color(C_BETA)

        self.play(Write(full_eq), FadeOut(Group(prob1, prob2, title4)) , self.camera.frame.animate.shift(DOWN*4) ,run_time=0.80)
        self.wait(2.0)




        gamma_row = VGroup(
            Tex(r"\gamma_j", font_size=50).set_color(C_GAMMA),
            Text("= learnable scale (per dimension)",
                 font_size=FS_SMALL, weight=BOLD).set_color(C_GAMMA),
        ).arrange(RIGHT, buff=0.20)
        gamma_row.next_to(full_eq, DOWN, buff=1.2).scale(1.4)

        beta_row = VGroup(
            Tex(r"\beta_j", font_size=50).set_color(C_BETA),
            Text("= learnable shift (per dimension)",
                 font_size=FS_SMALL, weight=BOLD).set_color(C_BETA),
        ).arrange(RIGHT, buff=0.20)
        beta_row.next_to(gamma_row, DOWN, buff=0.65).scale(1.4)

        self.play(FadeIn(gamma_row), run_time=0.40)
        self.wait(1.5)
        self.play(FadeIn(beta_row), run_time=0.40)
        self.wait(2.0)

        fix_note = Text("The model can undo the normalization if needed!",
                        font_size=FS_SMALL, weight=BOLD)
        fix_note.set_color(YELLOW)
        fix_note.scale(1.45)
        fix_note.next_to(beta_row, DOWN, buff=1)
        self.play(FadeIn(fix_note),self.camera.frame.animate.shift(DOWN*0.77) ,run_time=0.40)
        self.wait(3.0)






# ═══════════════════════════════════════════════════════════
#  Transformer Architecture — Paper-Style  (ManimGL)
#  manimgl a.py TransformerArchitecture -w --hd
# ═══════════════════════════════════════════════════════════

_ATT     = "#5B9BD5"
_MASKED  = "#7D3C98"
_CROSS_C = "#8B0000"
_FFN_C   = "#27AE60"
_NORM_C  = "#D4A017"
_EMBED_C = "#9B59B6"
_HEAD_C  = "#5DAF5D"
_PE_FILL = "#3DF5B0"
_PLUS_C  = "#FF0000"
_HL      = "#F1C40F"

_BW    = 1.80
_ATT_H = 0.42
_MSK_H = 0.60
_FFN_H = 0.32
_NRM_H = 0.24
_VGAP  = 0.26
_ENC_X = -2.10
_DEC_X =  2.10

_BPAD_BELOW = 0.60
_BPAD_ABOVE = 0.15
_BPAD_SIDE  = 0.35


def _blk(lines, color, w=_BW, h=_ATT_H, fs=14):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.06)
    r.set_fill(color, 0.85).set_stroke(WHITE, 1.3)
    parts = lines.split("\n") if isinstance(lines, str) else lines
    txts = VGroup(*[Text(p, font_size=fs, weight="BOLD") for p in parts])
    txts.arrange(DOWN, buff=0.02)
    txts.move_to(r)
    if txts.get_width() > w - 0.14:
        txts.set_width(w - 0.14)
    if txts.get_height() > h - 0.06:
        txts.set_height(h - 0.06)
    return VGroup(r, txts)


def _nrm():
    return _blk("Add & Norm", _NORM_C, h=_NRM_H, fs=11)


def _flow_arr(src, dst, color=GREY_B):
    return Arrow(src.get_top(), dst.get_bottom(), buff=0.02,
                 fill_color=color, thickness=1.4,
                 max_tip_length_to_length_ratio=0.35)


def _plus_sym(r=0.15):
    c = Circle(radius=r).set_stroke(WHITE, 1.5).set_fill(_PLUS_C, 0.92)
    t = Text("+", font_size=20, weight="BOLD", color=WHITE)
    t.move_to(c)
    return VGroup(c, t)


def _sine_circle(r=0.20):
    c = Circle(radius=r).set_stroke(WHITE, 1.5).set_fill(_PE_FILL, 0.60)
    pts = [np.array([x, 0.06 * np.sin(x * 22), 0])
           for x in np.linspace(-r * 0.6, r * 0.6, 50)]
    wave = VMobject()
    wave.set_points_as_corners(pts).move_to(c).set_stroke(WHITE, 1.5)
    return VGroup(c, wave)


def _pe_group(center, side):
    oplus = _plus_sym()
    oplus.move_to(center)
    sc = _sine_circle()
    lbl = VGroup(
        Text("Positional", font_size=20, color=GREY_A, weight="BOLD"),
        Text("Encoding",   font_size=20, color=GREY_A, weight="BOLD"),
    ).arrange(DOWN, buff=0.02)
    if side == "left":
        sc.move_to(center + LEFT * 0.80)
        lbl.next_to(sc, LEFT, buff=0.26)
        a = Arrow(sc.get_right(), oplus.get_left(), buff=0.04,
                  fill_color=GREY_B, thickness=1.0)
    else:
        sc.move_to(center + RIGHT * 0.80)
        lbl.next_to(sc, RIGHT, buff=0.26)
        a = Arrow(sc.get_left(), oplus.get_right(), buff=0.04,
                  fill_color=GREY_B, thickness=1.0)
    return VGroup(oplus, sc, lbl, a), oplus


def _make_tri(pos, direction, color=GREY_B, size=0.14):
    """Visible filled triangle pointing in the given direction."""
    tri = Triangle().set_height(size).set_width(size * 0.8)
    tri.set_fill(color, 1).set_stroke(color, 1)
    angle = np.arctan2(direction[1], direction[0]) - PI / 2
    tri.rotate(angle)
    tri.scale(0.7)
    tri.move_to(pos)
    return tri


def _skip_conn(mid_y, sub, nrm, border):
    """Right-angle skip as one continuous path + triangle tip at end."""
    x_c = sub.get_center()[0]
    x_r = sub.get_right()[0] + 0.14
    y_end = nrm.get_center()[1]
    x_nrm = nrm.get_right()[0]

    path = VMobject()
    path.set_points_as_corners([
        np.array([x_c, mid_y, 0]),
        np.array([x_r, mid_y, 0]),
        np.array([x_r, y_end, 0]),
        np.array([x_nrm, y_end, 0]),
    ])
    path.set_stroke(GREY_B, 1.5)

    tip = _make_tri(np.array([x_nrm + 0.04, y_end, 0]), LEFT)
    return VGroup(path, tip)


def _trident(oplus_mob, attn_block, spread=0.14):
    """Single continuous stroked path: stem -> bar -> 3 prongs.
    Small triangles at the tips serve as arrowheads."""
    x = attn_block.get_center()[0]
    fork_y = attn_block.get_bottom()[1] - 0.22
    # prongs stop 0.10 below block so triangles sit visibly outside
    tip_y  = attn_block.get_bottom()[1] - 0.08
    lx, rx = x - spread, x + spread
    sw = 2.0

    # one VMobject per branch so stroke is continuous at corners
    left_branch = VMobject()
    left_branch.set_points_as_corners([
        oplus_mob.get_top() + UP * 0.02,
        np.array([x, fork_y, 0]),
        np.array([lx, fork_y, 0]),
        np.array([lx, tip_y, 0]),
    ])
    left_branch.set_stroke(GREY_B, sw)

    mid_branch = VMobject()
    mid_branch.set_points_as_corners([
        np.array([x, fork_y, 0]),
        np.array([x, tip_y, 0]),
    ])
    mid_branch.set_stroke(GREY_B, sw)

    right_branch = VMobject()
    right_branch.set_points_as_corners([
        np.array([x, fork_y, 0]),
        np.array([rx, fork_y, 0]),
        np.array([rx, tip_y, 0]),
    ])
    right_branch.set_stroke(GREY_B, sw)

    # triangles sitting just below the block — clearly visible
    tips = VGroup()
    for tx in [lx, x, rx]:
        tri = _make_tri(np.array([tx, tip_y - 0.01, 0]), UP)
        tips.add(tri)

    return VGroup(left_branch, mid_branch, right_branch, tips)


def _make_border(stk):
    w = stk.get_width()  + 2 * _BPAD_SIDE
    h = stk.get_height() + _BPAD_BELOW + _BPAD_ABOVE
    bdr = RoundedRectangle(width=w, height=h, corner_radius=0.08)
    bdr.set_fill(WHITE, 0.03).set_stroke(GREY_C, 0.8)
    offset = (_BPAD_BELOW - _BPAD_ABOVE) / 2
    bdr.move_to(stk.get_center() + DOWN * offset)
    return bdr


_NORM_GAP = 0.07   # tight gap: sub-block to its Add & Norm
_PAIR_GAP = 0.26   # larger gap between pairs


def _stack_pairs(pairs):
    """Stack (block, norm) pairs: tight within pair, larger between pairs.
    Returns (stk VGroup of all parts, list of connector Lines)."""
    all_parts = []
    connectors = []
    for blk, nrm in pairs:
        all_parts.extend([blk, nrm])

    # Position manually bottom-up
    y = 0.0
    for i, mob in enumerate(all_parts):
        mob.move_to(ORIGIN)
        mob.shift(UP * (y + mob.get_height() / 2))
        if i % 2 == 0:
            # sub-block: next is its norm, use tight gap
            y += mob.get_height() + _NORM_GAP
        else:
            # norm: next pair uses larger gap
            y += mob.get_height() + _PAIR_GAP

    stk = VGroup(*all_parts)
    # center the stack
    stk.move_to(ORIGIN)

    # connector lines between each sub-block top and its norm bottom
    for blk, nrm in pairs:
        ln = Line(blk.get_top(), nrm.get_bottom())
        ln.set_stroke(GREY_B, 1.5)
        connectors.append(ln)

    return stk, connectors


def _enc_layer():
    attn = _blk("Multi-Head\nAttention", _ATT, h=_ATT_H)
    n1   = _nrm()
    ffn  = _blk("Feed Forward", _FFN_C, h=_FFN_H, fs=13)
    n2   = _nrm()
    pairs = [(attn, n1), (ffn, n2)]
    stk, connectors = _stack_pairs(pairs)
    bdr = _make_border(stk)
    parts = [attn, n1, ffn, n2]
    g = VGroup(bdr, stk, *connectors)
    g.parts = parts
    g.attn = attn; g.n1 = n1; g.ffn = ffn; g.n2 = n2
    return g


def _dec_layer():
    masked = _blk("Masked\nMulti-Head\nAttention", _MASKED, h=_MSK_H)
    n1     = _nrm()
    cross  = _blk("Multi-Head\nAttention", _CROSS_C, h=_ATT_H)
    n2     = _nrm()
    ffn    = _blk("Feed Forward", _FFN_C, h=_FFN_H, fs=13)
    n3     = _nrm()
    pairs = [(masked, n1), (cross, n2), (ffn, n3)]
    stk, connectors = _stack_pairs(pairs)
    bdr = _make_border(stk)
    parts = [masked, n1, cross, n2, ffn, n3]
    g = VGroup(bdr, stk, *connectors)
    g.parts = parts
    g.masked = masked; g.n1 = n1; g.cross = cross
    g.n2 = n2; g.ffn = ffn; g.n3 = n3
    return g


class TransformerArchitecture(Scene):
    def construct(self):

        # ── labels ───────────────────────────────────
        inp_lbl = Text("Inputs", font_size=20, color=GREY_A, weight="BOLD")
        inp_lbl.move_to([_ENC_X, -3.5, 0])
        out_lbl = VGroup(
            Text("Outputs", font_size=20, color=GREY_A, weight="BOLD"),
            Text("(shifted right)", font_size=15, color=GREY_A, weight="BOLD"),
        ).arrange(DOWN, buff=0.02).move_to([_DEC_X, -3.5, 0])

        # ── embeddings ──────────────────────────────
        inp_emb = _blk("Input\nEmbedding", _EMBED_C, w=1.65, h=0.40, fs=13)
        inp_emb.move_to([_ENC_X, -2.55, 0])
        out_emb = _blk("Output\nEmbedding", _EMBED_C, w=1.65, h=0.40, fs=13)
        out_emb.move_to([_DEC_X, -2.55, 0])

        # ── positional encoding ─────────────────────
        pe_y = -1.82
        enc_pe, enc_oplus = _pe_group(np.array([_ENC_X, pe_y, 0]), "left")
        dec_pe, dec_oplus = _pe_group(np.array([_DEC_X, pe_y, 0]), "right")

        # ── encoder & decoder layers ────────────────
        enc = _enc_layer()
        dec = _dec_layer()
        bot_y = -1.40
        enc.move_to([_ENC_X, 0, 0])
        enc.shift(UP * (bot_y - enc.get_bottom()[1]))
        dec.move_to([_DEC_X, 0, 0])
        dec.shift(UP * (bot_y - dec.get_bottom()[1]))
        enc_bdr = enc[0]
        dec_bdr = dec[0]

        # ENCODER on the left side, DECODER on the right side
        enc_hdr = Text("ENCODER", font_size=30, color="#5DADE2", weight="BOLD")
        enc_hdr.next_to(enc, LEFT, buff=0.35)
        dec_hdr = Text("DECODER", font_size=30, color="#58D68D", weight="BOLD")
        dec_hdr.next_to(dec, RIGHT, buff=0.55)

        # N× above the ENCODER / DECODER label texts
        enc_nx = Text("N\u00d7", font_size=30, color="#5DADE2", weight="BOLD")
        enc_nx.next_to(enc_hdr, UP, buff=0.4)
        dec_nx = Text("N\u00d7", font_size=30, color="#58D68D", weight="BOLD")

        # ── output head ─────────────────────────────
        linear_b  = _blk("Linear", _HEAD_C, w=1.5, h=0.26, fs=12)
        softmax_b = _blk("Softmax", _HEAD_C, w=1.5, h=0.26, fs=12)
        linear_b.next_to(dec, UP, buff=0.25)
        softmax_b.next_to(linear_b, UP, buff=0.18)
        out_prob = VGroup(
            Text("Output", font_size=18, color=GREY_A, weight="BOLD"),
            Text("Probabilities", font_size=18, color=GREY_A, weight="BOLD"),
        ).arrange(DOWN, buff=0.02)
        out_prob.next_to(softmax_b, UP, buff=0.18)
        dec_hdr.next_to(dec, RIGHT, buff=0.10)

        # ── external arrows (labels -> embed -> PE) ──
        a_inp     = _flow_arr(inp_lbl, inp_emb)
        a_emb_pe  = _flow_arr(inp_emb, enc_oplus)
        a_out     = _flow_arr(out_lbl, out_emb)
        a_oemb_pe = _flow_arr(out_emb, dec_oplus)

        # ══════════════════════════════════════════════
        #  Trident arrows: oplus -> through border -> 3 into attention
        #  (replaces old a_pe_enc / a_pe_dec + internal entry)
        # ══════════════════════════════════════════════
        enc_trident = _trident(enc_oplus, enc.attn)
        dec_trident = _trident(dec_oplus, dec.masked, spread=0.14)

        # ── internal block-to-block arrows ──────────
        # Encoder: attn->n1, n1->ffn, ffn->n2
        enc_int = VGroup(*[_flow_arr(enc.parts[i], enc.parts[i + 1])
                           for i in range(len(enc.parts) - 1)])

        # Decoder: build individually so we can make n1->cross special
        dec_a0 = _flow_arr(dec.masked, dec.n1)       # masked -> n1
        # n1 -> cross: straight arrow (Q from below)
        dec_q = Arrow(dec.n1.get_top(), dec.cross.get_bottom(),
                      fill_color=GREY_B,
                      thickness=1.4, max_tip_length_to_length_ratio=0.35,
                      buff=0.02)
        dec_a2 = _flow_arr(dec.cross, dec.n2)        # cross -> n2
        dec_a3 = _flow_arr(dec.n2, dec.ffn)          # n2 -> ffn
        dec_a4 = _flow_arr(dec.ffn, dec.n3)          # ffn -> n3
        dec_int = VGroup(dec_a0, dec_q, dec_a2, dec_a3, dec_a4)

        a_dec_lin  = _flow_arr(dec, linear_b)
        a_lin_soft = _flow_arr(linear_b, softmax_b)

        # ══════════════════════════════════════════════
        #  Skip connections (slightly past block edge, inside border)
        # ══════════════════════════════════════════════
        # Encoder
        fork_y_enc = enc.attn.get_bottom()[1] - 0.18
        entry_bot_enc = enc_oplus.get_top()[1] + 0.02
        enc_sk1_y = (entry_bot_enc + fork_y_enc) / 2
        enc_sk2_y = (enc.n1.get_top()[1] + enc.ffn.get_bottom()[1]) / 2
        enc_sk = VGroup(
            _skip_conn(enc_sk1_y, enc.attn, enc.n1, enc_bdr),
            _skip_conn(enc_sk2_y, enc.ffn,  enc.n2, enc_bdr),
        )

        # Decoder
        fork_y_dec = dec.masked.get_bottom()[1] - 0.10
        entry_bot_dec = dec_oplus.get_top()[1] + 0.02
        dec_sk1_y = (entry_bot_dec + fork_y_dec) / 2
        dec_sk2_y = (dec.n1.get_top()[1] + dec.cross.get_bottom()[1]) / 2
        dec_sk3_y = (dec.n2.get_top()[1] + dec.ffn.get_bottom()[1]) / 2
        dec_sk = VGroup(
            _skip_conn(dec_sk1_y, dec.masked, dec.n1, dec_bdr),
            _skip_conn(dec_sk2_y, dec.cross,  dec.n2, dec_bdr),
            _skip_conn(dec_sk3_y, dec.ffn,    dec.n3, dec_bdr),
        )

        # ══════════════════════════════════════════════
        #  Encoder -> Decoder cross-attention staircase
        #  K, V from left;  Q enters from below (curvy arrow above)
        # ══════════════════════════════════════════════
        enc_top_y = enc_bdr.get_top()[1]
        up_y      = enc_top_y + 0.25
        cross_y   = dec.cross.get_center()[1]
        mid_x     = (_ENC_X + _DEC_X) / 2

        kv_sp = 0.07
        # staircase as one continuous path — sharp connected corners
        staircase = VMobject()
        staircase.set_points_as_corners([
            np.array([_ENC_X, enc_top_y, 0]),
            np.array([_ENC_X, up_y, 0]),
            np.array([mid_x, up_y, 0]),
            np.array([mid_x, cross_y + kv_sp, 0]),
        ])
        staircase.set_stroke(_HL, 1.8)

        # vertical bar at the fork
        bar = Line(np.array([mid_x, cross_y + kv_sp, 0]),
                   np.array([mid_x, cross_y - kv_sp, 0]))
        bar.set_stroke(_HL, 1.8)

        # two parallel arrows into cross-attn (with arrowheads)
        cross_left_x = dec.cross.get_left()[0]
        a_kw = dict(fill_color=_HL, thickness=1.2,
                    max_tip_length_to_length_ratio=0.20, buff=0.01)
        k_arr = Arrow(np.array([mid_x, cross_y + kv_sp, 0]),
                      np.array([cross_left_x, cross_y + kv_sp, 0]), **a_kw)
        v_arr = Arrow(np.array([mid_x, cross_y - kv_sp, 0]),
                      np.array([cross_left_x, cross_y - kv_sp, 0]), **a_kw)

        cross_grp = VGroup(staircase, bar, k_arr, v_arr)

        # ══════════════════════════════════════════════
        #  Animation
        # ══════════════════════════════════════════════
        frame = self.camera.frame
        frame.save_state()

        # Step 1: all blocks appear at once (GrowFromCenter)
        self.play(
            GrowFromCenter(inp_lbl),
            GrowFromCenter(out_lbl),
            GrowFromCenter(inp_emb),
            GrowFromCenter(out_emb),
            GrowFromCenter(enc_pe),
            GrowFromCenter(dec_pe),
            GrowFromCenter(enc),
            GrowFromCenter(dec),
            GrowFromCenter(linear_b),
            GrowFromCenter(softmax_b),
            GrowFromCenter(out_prob),
            run_time=0.8,
        )
        dec_hdr.shift(RIGHT*0.25)
        dec_nx.next_to(dec_hdr, UP, buff=0.4)

        # Step 2: all arrows, connections, labels at once (no wait)
        self.play(
            # external arrows
            ShowCreation(a_inp),
            ShowCreation(a_emb_pe),
            ShowCreation(a_out),
            ShowCreation(a_oemb_pe),
            # tridents
            ShowCreation(enc_trident),
            ShowCreation(dec_trident),
            # internal arrows
            *[ShowCreation(a) for a in enc_int],
            *[ShowCreation(a) for a in dec_int],
            # skip connections
            *[ShowCreation(s) for s in enc_sk],
            *[ShowCreation(s) for s in dec_sk],
            # cross-attention
            ShowCreation(cross_grp),
            # output head arrows
            ShowCreation(a_dec_lin),
            ShowCreation(a_lin_soft),
            # labels
            FadeIn(enc_hdr),
            FadeIn(dec_hdr),
            FadeIn(enc_nx),
            FadeIn(dec_nx),
            run_time=1.0,
        )

        self.wait(2)


        # ══════════════════════════════════════════════
        #  Pulse walkthrough — SLOW circular dots, bright colors,
        #  residuals follow actual right-angle paths
        # ══════════════════════════════════════════════
        MR = 1.0   # camera move run_time
        W  = 1.0   # wait between steps

        # Fully bright versions of each block color
        B_EMBED  = "#D2A0FF"  # bright purple
        B_PE     = "#66FFCC"  # bright mint
        B_ATT    = "#99CCFF"  # bright blue
        B_MASKED = "#CC77EE"  # bright purple-pink
        B_CROSS  = "#FF4444"  # bright red
        B_FFN    = "#55FF88"  # bright green
        B_NORM   = "#FFD040"  # bright gold
        B_HEAD   = "#88FF88"  # bright lime
        B_HL     = "#FFFF44"  # bright yellow
        B_RES    = "#AAAAAA"  # grey for residual (not white)
        B_GREY   = "#BBBBBB"  # bright grey

        def mk_pulse(col, r=0.12):
            o = Dot(radius=r)
            o.set_fill(col, opacity=0.85)
            o.set_stroke(width=0)
            o.set_z_index(6)
            i = Dot(radius=r * 0.45)
            i.set_fill(WHITE, opacity=1.0)
            i.set_stroke(width=0)
            i.set_z_index(7)
            return VGroup(o, i)

        def run_p(start, end, col, rt=1.0):
            p = mk_pulse(col)
            p.move_to(start)
            self.play(GrowFromCenter(p), run_time=0.10)
            self.play(p.animate.move_to(end), run_time=rt)
            self.play(FadeOut(p), run_time=0.10)

        def run_p_path(waypoints, col, rt_per=0.60):
            """Pulse follows a multi-point path (for residuals)."""
            p = mk_pulse(col)
            p.move_to(waypoints[0])
            self.play(GrowFromCenter(p), run_time=0.10)
            for wp in waypoints[1:]:
                self.play(p.animate.move_to(wp), run_time=rt_per)
            self.play(FadeOut(p), run_time=0.10)

        def zoom_to(target, sc=0.50, rt=MR):
            f = frame.generate_target()
            f.set_height(8 * sc)
            f.move_to(target.get_center())
            return MoveToTarget(frame, run_time=rt)

        def res_waypoints(sub, nrm, mid_y):
            """Residual path: right-angle route ending at norm CENTER."""
            x_c = sub.get_center()[0]
            x_r = sub.get_right()[0] + 0.14
            y_end = nrm.get_center()[1]
            return [
                np.array([x_c, mid_y, 0]),
                np.array([x_r, mid_y, 0]),
                np.array([x_r, y_end, 0]),
                nrm.get_center(),
            ]

        # ── 1. Encoder input ──
        inp_mid = VGroup(inp_lbl, inp_emb, enc_oplus)
        self.play(zoom_to(inp_mid, sc=0.45))
        self.wait(W)

        run_p(inp_lbl.get_center(), inp_emb.get_center(), B_EMBED)
        self.play(Indicate(inp_emb, color=B_EMBED, scale_factor=1.06), run_time=0.35)
        self.wait(W)

        run_p(inp_emb.get_center(), enc_oplus.get_center(), B_EMBED)
        self.play(Indicate(enc_oplus, color=B_EMBED, scale_factor=1.10), run_time=0.35)
        self.wait(W)

        pe_circ_center = enc_pe[1].get_center()
        run_p(pe_circ_center, enc_oplus.get_center(), B_PE)
        self.play(Indicate(enc_oplus, color=B_PE, scale_factor=1.10), run_time=0.35)
        self.wait(W)

        # ── 2. Trident into encoder attention ──
        self.play(zoom_to(enc.attn, sc=0.45), run_time=MR)
        self.wait(W)

        sp = 0.14
        # 3 pulses from oplus center → attn center (fan pattern)
        p_l = mk_pulse(B_GREY); p_l.move_to(enc_oplus.get_center())
        p_m = mk_pulse(B_GREY); p_m.move_to(enc_oplus.get_center())
        p_r = mk_pulse(B_GREY); p_r.move_to(enc_oplus.get_center())
        self.play(GrowFromCenter(p_l), GrowFromCenter(p_m),
                  GrowFromCenter(p_r), run_time=0.10)
        self.play(
            p_l.animate.move_to(enc.attn.get_center() + LEFT * sp),
            p_m.animate.move_to(enc.attn.get_center()),
            p_r.animate.move_to(enc.attn.get_center() + RIGHT * sp),
            run_time=1.0,
        )
        self.play(FadeOut(p_l), FadeOut(p_m), FadeOut(p_r), run_time=0.10)
        self.play(Indicate(enc.attn, color=B_ATT, scale_factor=1.06), run_time=0.40)
        self.wait(W)

        # ── 3. Encoder: Add & Norm around attn ──
        # Residual first (Add), then main flow, then Indicate (Norm)
        rp1 = res_waypoints(enc.attn, enc.n1, enc_sk1_y)
        run_p_path(rp1, B_RES)
        run_p(enc.attn.get_center(), enc.n1.get_center(), B_ATT)
        self.play(Indicate(enc.n1, color=B_NORM, scale_factor=1.06), run_time=0.35)
        self.wait(W)

        # Zoom to FFN
        self.play(zoom_to(enc.ffn, sc=0.45), run_time=MR)
        self.wait(W)

        run_p(enc.n1.get_center(), enc.ffn.get_center(), B_NORM)
        self.play(Indicate(enc.ffn, color=B_FFN, scale_factor=1.06), run_time=0.35)
        self.wait(W)

        # Add & Norm around FFN: residual first
        rp2 = res_waypoints(enc.ffn, enc.n2, enc_sk2_y)
        run_p_path(rp2, B_RES)
        run_p(enc.ffn.get_center(), enc.n2.get_center(), B_FFN)
        self.play(Indicate(enc.n2, color=B_NORM, scale_factor=1.06), run_time=0.35)
        self.wait(W)

        # ── 4. Encoder output → staircase → K,V wait ──
        self.play(zoom_to(VGroup(enc_bdr, dec.cross), sc=0.70), run_time=MR)
        self.wait(W)

        enc_top_pt = np.array([_ENC_X, enc_bdr.get_top()[1], 0])
        up_pt = np.array([_ENC_X, enc_bdr.get_top()[1] + 0.25, 0])
        mid_pt = np.array([mid_x, up_y, 0])
        fork_kv = np.array([mid_x, cross_y, 0])

        run_p_path([enc_top_pt, up_pt, mid_pt, fork_kv], B_HL, rt_per=0.50)
        self.wait(W)

        kv_k_pos = dec.cross.get_left() + UP * kv_sp
        kv_v_pos = dec.cross.get_left() + DOWN * kv_sp
        pk = mk_pulse(B_HL, r=0.10); pk.move_to(fork_kv)
        pv = mk_pulse(B_HL, r=0.10); pv.move_to(fork_kv)
        self.play(GrowFromCenter(pk), GrowFromCenter(pv), run_time=0.10)
        self.play(pk.animate.move_to(kv_k_pos),
                  pv.animate.move_to(kv_v_pos), run_time=1.0)
        self.wait(W)

        # ── 5. Decoder input ──
        dec_inp_mid = VGroup(out_lbl, out_emb, dec_oplus)
        self.play(zoom_to(dec_inp_mid, sc=0.45), run_time=MR)
        self.wait(W)

        run_p(out_lbl.get_center(), out_emb.get_center(), B_EMBED)
        self.play(Indicate(out_emb, color=B_EMBED, scale_factor=1.06), run_time=0.35)
        self.wait(W)
        run_p(out_emb.get_center(), dec_oplus.get_center(), B_EMBED)
        self.play(Indicate(dec_oplus, color=B_EMBED, scale_factor=1.10), run_time=0.35)
        self.wait(W)
        dec_pe_circ = dec_pe[1].get_center()
        run_p(dec_pe_circ, dec_oplus.get_center(), B_PE)
        self.play(Indicate(dec_oplus, color=B_PE, scale_factor=1.10), run_time=0.35)
        self.wait(W)

        # ── 6. Decoder trident into masked attn ──
        self.play(zoom_to(dec.masked, sc=0.45), run_time=MR)
        self.wait(W)

        dl = mk_pulse(B_GREY); dl.move_to(dec_oplus.get_center())
        dm = mk_pulse(B_GREY); dm.move_to(dec_oplus.get_center())
        dr = mk_pulse(B_GREY); dr.move_to(dec_oplus.get_center())
        self.play(GrowFromCenter(dl), GrowFromCenter(dm),
                  GrowFromCenter(dr), run_time=0.10)
        self.play(
            dl.animate.move_to(dec.masked.get_center() + LEFT * sp),
            dm.animate.move_to(dec.masked.get_center()),
            dr.animate.move_to(dec.masked.get_center() + RIGHT * sp),
            run_time=1.0,
        )
        self.play(FadeOut(dl), FadeOut(dm), FadeOut(dr), run_time=0.10)
        self.play(Indicate(dec.masked, color=B_MASKED, scale_factor=1.06), run_time=0.40)
        self.wait(W)

        # Add & Norm around masked: residual first
        rp3 = res_waypoints(dec.masked, dec.n1, dec_sk1_y)
        run_p_path(rp3, B_RES)
        run_p(dec.masked.get_center(), dec.n1.get_center(), B_MASKED)
        self.play(Indicate(dec.n1, color=B_NORM, scale_factor=1.06), run_time=0.35)
        self.wait(W)

        # ── 7. Q at cross-attn + K,V merge ──
        self.play(zoom_to(dec.cross, sc=0.45), run_time=MR)
        self.wait(W)

        run_p(dec.n1.get_center(), dec.cross.get_center(), B_CROSS)
        self.wait(W)

        self.play(
            Flash(pk.get_center(), color=B_HL, line_length=0.15,
                  flash_radius=0.15, num_lines=8),
            Flash(pv.get_center(), color=B_HL, line_length=0.15,
                  flash_radius=0.15, num_lines=8),
            FadeOut(pk), FadeOut(pv),
            Indicate(dec.cross, color=B_HL, scale_factor=1.08),
            run_time=0.60,
        )
        self.wait(W)

        # Add & Norm around cross: residual first
        rp4 = res_waypoints(dec.cross, dec.n2, dec_sk2_y)
        run_p_path(rp4, B_RES)
        run_p(dec.cross.get_center(), dec.n2.get_center(), B_CROSS)
        self.play(Indicate(dec.n2, color=B_NORM, scale_factor=1.06), run_time=0.35)
        self.wait(W)

        # ── 8. n2 → ffn → n3 ──
        self.play(zoom_to(dec.ffn, sc=0.45), run_time=MR)
        self.wait(W)

        run_p(dec.n2.get_center(), dec.ffn.get_center(), B_NORM)
        self.play(Indicate(dec.ffn, color=B_FFN, scale_factor=1.06), run_time=0.35)
        self.wait(W)

        # Add & Norm around FFN: residual first
        rp5 = res_waypoints(dec.ffn, dec.n3, dec_sk3_y)
        run_p_path(rp5, B_RES)
        run_p(dec.ffn.get_center(), dec.n3.get_center(), B_FFN)
        self.play(Indicate(dec.n3, color=B_NORM, scale_factor=1.06), run_time=0.35)
        self.wait(W)

        # ── 9. Output head ──
        self.play(zoom_to(VGroup(linear_b, softmax_b, out_prob), sc=0.45),
                  run_time=MR)
        self.wait(W)

        run_p(dec.n3.get_center(), linear_b.get_center(), B_HEAD)
        self.play(Indicate(linear_b, color=B_HEAD, scale_factor=1.06), run_time=0.35)
        self.wait(W)
        run_p(linear_b.get_center(), softmax_b.get_center(), B_HEAD)
        self.play(Indicate(softmax_b, color=B_HEAD, scale_factor=1.06), run_time=0.35)
        self.wait(W)
        run_p(softmax_b.get_center(), out_prob.get_center(), B_HEAD)
        self.wait(W)

        # ── 10. Output description + zoom back out ──
        prob_txt = VGroup(
            Text("Next token probability distribution", font_size=14, weight="BOLD"),
            Text("e.g.  'the': 0.42,  'a': 0.18,  'an': 0.07 ...", font_size=11, weight="BOLD"),
        ).arrange(DOWN, buff=0.08)
        prob_txt.set_color(B_HEAD)
        prob_txt.next_to(out_prob, UP, buff=0.38).scale(1.23)
        self.play(FadeIn(prob_txt, shift=UP * 0.08), run_time=0.60)
        self.wait(2)

        self.play(FadeOut(prob_txt), frame.animate.restore(), run_time=1.5)
        self.wait(3)




# ═══════════════════════════════════════════════════════════════════
#  SCENE — Why Transformers?  (RNN Encoder-Decoder shortcomings)
#  manimgl a.py WhyTransformers -w --hd
# ═══════════════════════════════════════════════════════════════════



class TransformerWorking(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.30)

        C_ENC   = "#2980B9"
        C_DEC   = "#27AE60"
        C_TOK   = "#34495E"
        C_OUT   = "#F39C12"
        C_PRED  = "#E74C3C"
        C_CROSS = "#F1C40F"
        C_ARR   = "#95A5A6"

        N = 6
        ENC_X = -3.5
        DEC_X =  3.5
        BW, BH = 2.4, 0.55
        GAP = 0.30

        def mk_blk(label, color, pos, fs=18):
            r = RoundedRectangle(width=BW, height=BH, corner_radius=0.08)
            r.set_fill(color, 0.85).set_stroke(WHITE, 1.5)
            r.move_to(pos)
            t = Text(label, font_size=fs, weight="BOLD")
            t.set_color(WHITE).move_to(r)
            return VGroup(r, t)

        def tok(text, color=C_TOK, fs=20):
            t = Text(text, font_size=fs, weight="BOLD")
            t.set_color(WHITE)
            bg = RoundedRectangle(
                width=max(t.get_width() + 0.35, 0.80),
                height=0.45, corner_radius=0.08,
            )
            bg.set_fill(color, 0.88).set_stroke(WHITE, 1.2)
            t.move_to(bg)
            return VGroup(bg, t)

        def mk_pulse(col, r=0.10):
            o = Dot(radius=r).set_fill(col, 0.80).set_stroke(width=0).set_z_index(6)
            i = Dot(radius=r * 0.45).set_fill(WHITE, 1.0).set_stroke(width=0).set_z_index(7)
            return VGroup(o, i)

        def run_p(start, end, col, rt=0.40):
            p = mk_pulse(col)
            p.move_to(start)
            self.play(GrowFromCenter(p), run_time=0.08)
            self.play(p.animate.move_to(end), run_time=rt)
            self.play(FadeOut(p), run_time=0.08)

        # ══════════════════════════════════════════════
        #  Title — show and fade out
        # ══════════════════════════════════════════════
        title = Text("Transformer: Training & Inference", font_size=57, weight="BOLD")
        title.set_color(WHITE).move_to(ORIGIN)
        self.play(FadeIn(title), run_time=0.60)
        self.wait(2)
        self.play(FadeOut(title), run_time=0.40)
        self.wait(0.5)


        # ══════════════════════════════════════════════
        #  BUILD: 6 encoder + 6 decoder stacks
        # ══════════════════════════════════════════════
        enc_blks = VGroup()
        dec_blks = VGroup()
        for i in range(N):
            y = -(N - 1) * (BH + GAP) / 2 + i * (BH + GAP)
            enc_blks.add(mk_blk("Encoder", C_ENC, np.array([ENC_X, y, 0])))
            dec_blks.add(mk_blk("Decoder", C_DEC, np.array([DEC_X, y, 0])))

        enc_arr = VGroup(*[Arrow(enc_blks[i].get_top(), enc_blks[i+1].get_bottom(),
                    buff=0.02, fill_color=C_ARR, thickness=2.0,
                    max_tip_length_to_length_ratio=0.30) for i in range(N-1)])
        dec_arr = VGroup(*[Arrow(dec_blks[i].get_top(), dec_blks[i+1].get_bottom(),
                    buff=0.02, fill_color=C_ARR, thickness=2.0,
                    max_tip_length_to_length_ratio=0.30) for i in range(N-1)])

        # Cross connection as one continuous VMobject path (no gaps)
        enc_top_pt = enc_blks[-1].get_top()
        spine_top_y = enc_top_pt[1] + 0.50
        spine_x = (ENC_X + DEC_X) / 2
        spine_bot_y = dec_blks[0].get_center()[1]

        cross_spine = VMobject()
        cross_spine.set_points_as_corners([
            enc_top_pt,
            np.array([ENC_X, spine_top_y, 0]),
            np.array([spine_x, spine_top_y, 0]),
            np.array([spine_x, spine_bot_y, 0]),
        ])
        cross_spine.set_stroke(C_CROSS, 3.5)

        cross_to_dec = VGroup()
        for i in range(N):
            a = Arrow(np.array([spine_x, dec_blks[i].get_center()[1], 0]),
                      dec_blks[i].get_left(),
                      buff=0.02, fill_color=C_CROSS, thickness=2.5,
                      max_tip_length_to_length_ratio=0.25)
            cross_to_dec.add(a)

        
        self.camera.frame.scale(0.84).shift(UP*0.23)
        # ══════════════════════════════════════════════
        #  PHASE 1 — Show architecture
        # ══════════════════════════════════════════════
        self.play(
            LaggedStart(*[GrowFromCenter(b) for b in enc_blks], lag_ratio=0.06, run_time=0.70),
            LaggedStart(*[GrowFromCenter(b) for b in dec_blks], lag_ratio=0.06, run_time=0.70),
        )
        self.play(*[ShowCreation(a) for a in enc_arr],
                  *[ShowCreation(a) for a in dec_arr], run_time=0.40)
        self.play(ShowCreation(cross_spine), run_time=0.50)
        self.play(*[ShowCreation(a) for a in cross_to_dec], run_time=0.50)
        self.wait(2)

        # ══════════════════════════════════════════════
        #  PHASE 2 — TRAINING (Teacher Forcing)
        # ══════════════════════════════════════════════
        tr_lbl = Text("TRAINING", font_size=48, weight="BOLD")
        tr_lbl.set_color("#E74C3C").to_edge(UP, buff=0).shift(UP*0.1)
        self.play(FadeIn(tr_lbl), run_time=0.30)
        self.wait(1)

        inp_toks = VGroup(tok("I"), tok("love"), tok("you"))
        inp_toks.arrange(RIGHT, buff=0.12)
        inp_toks.next_to(enc_blks[0], DOWN, buff=0.70)
        inp_arr = Arrow(inp_toks.get_top(), enc_blks[0].get_bottom(),
                        buff=0.04, fill_color=C_ARR, thickness=2.0)

        tgt_toks = VGroup(
            tok("<SOS>", C_OUT),
            tok("\u044f", C_OUT),
            tok("\u0442\u0435\u0431\u044f", C_OUT),
            tok("\u043b\u044e\u0431\u043b\u044e", C_OUT),
        )
        tgt_toks.arrange(RIGHT, buff=0.12)
        tgt_toks.next_to(dec_blks[0], DOWN, buff=0.70)
        tgt_arr = Arrow(tgt_toks.get_top(), dec_blks[0].get_bottom(),
                        buff=0.04, fill_color=C_ARR, thickness=2.0)

        pred_toks = VGroup(
            tok("\u044f", C_PRED),
            tok("\u0442\u0435\u0431\u044f", C_PRED),
            tok("\u043b\u044e\u0431\u043b\u044e", C_PRED),
            tok("<EOS>", C_PRED),
        )
        pred_toks.arrange(RIGHT, buff=0.12)
        pred_toks.next_to(dec_blks[-1], UP, buff=0.50)
        out_arr = Arrow(dec_blks[-1].get_top(), pred_toks.get_bottom(),
                        buff=0.04, fill_color=C_ARR, thickness=2.0)

        teach_note = Text("All targets fed at once!", font_size=18, weight="BOLD")
        teach_note.set_color(C_OUT).next_to(tgt_toks, DOWN, buff=0.15)

        # Show input
        self.play(LaggedStart(*[FadeIn(t, shift=UP*0.08) for t in inp_toks],
                  lag_ratio=0.08, run_time=0.50))
        self.play(GrowArrow(inp_arr), run_time=0.30)
        self.wait(1)

        # Encoder pulses
        for i in range(N):
            self.play(Indicate(enc_blks[i], color=WHITE, scale_factor=1.04), run_time=0.12)
        self.wait(0.5)

        # Target (teacher forcing)
        self.play(LaggedStart(*[FadeIn(t, shift=UP*0.08) for t in tgt_toks],
                  lag_ratio=0.08, run_time=0.50), FadeIn(teach_note))
        self.play(GrowArrow(tgt_arr), run_time=0.30)
        self.wait(1)

        # Cross pulses
        for i in range(N):
            run_p(np.array([spine_x, dec_blks[i].get_center()[1], 0]),
                  dec_blks[i].get_center(), C_CROSS, rt=0.15)

        # Decoder pulses
        for i in range(N):
            self.play(Indicate(dec_blks[i], color=WHITE, scale_factor=1.04), run_time=0.12)
        self.wait(0.5)

        # Output
        self.play(GrowArrow(out_arr), tr_lbl.animate.shift(LEFT*1.7) ,run_time=0.30)
        self.play(LaggedStart(*[FadeIn(t, shift=UP*0.08) for t in pred_toks],
                  lag_ratio=0.08, run_time=0.50))
        self.wait(1)

        loss_note = Text("Loss = predicted vs actual", font_size=18, weight="BOLD")
        loss_note.set_color(C_PRED).next_to(pred_toks, UP, buff=0.15)
        par_note = Text("All positions in PARALLEL!", font_size=20, weight="BOLD")
        par_note.set_color("#2ECC71").next_to(loss_note, UP, buff=0.12)
        self.play(FadeIn(loss_note), FadeIn(par_note), run_time=0.30)
        self.wait(3)

        # Fade ALL training stuff
        tr_all = [tr_lbl, inp_toks, inp_arr, tgt_toks, tgt_arr,
                  pred_toks, out_arr, teach_note, loss_note, par_note]
        self.play(*[FadeOut(m) for m in tr_all], run_time=0.40)
        self.wait(0.5)


        # ══════════════════════════════════════════════
        #  PHASE 3 — INFERENCE (Autoregressive)
        # ══════════════════════════════════════════════
        inf_lbl = Text("INFERENCE", font_size=28, weight="BOLD")
        inf_lbl.set_color("#9B59B6").to_edge(UP, buff=0.0).shift(UP*0).scale(1.3)
        self.play(FadeIn(inf_lbl), run_time=0.30)
        self.wait(1)

        inf_inp = VGroup(tok("I"), tok("love"), tok("you"))
        inf_inp.arrange(RIGHT, buff=0.12)
        inf_inp.next_to(enc_blks[0], DOWN, buff=0.70)
        inf_arr = Arrow(inf_inp.get_top(), enc_blks[0].get_bottom(),
                        buff=0.04, fill_color=C_ARR, thickness=2.0)

        self.play(LaggedStart(*[FadeIn(t, shift=UP*0.08) for t in inf_inp],
                  lag_ratio=0.08, run_time=0.40))
        self.play(GrowArrow(inf_arr), run_time=0.25)

        
        for i in range(N):
            self.play(Indicate(enc_blks[i], color=WHITE, scale_factor=1.03), run_time=0.08)
        self.wait(1)

        # Autoregressive: ya tebya lyublyu
        russian = ["\u044f", "\u0442\u0435\u0431\u044f",
                   "\u043b\u044e\u0431\u043b\u044e", "<EOS>"]
        dec_inp_y = dec_blks[0].get_bottom()[1] - 0.70
        out_y = dec_blks[-1].get_top()[1] + 0.55
        step_ref = [None]

        for step in range(len(russian)):
            feed = ["<SOS>"] + russian[:step]
            dec_cards = VGroup(*[tok(w, C_OUT, fs=16) for w in feed])
            dec_cards.arrange(RIGHT, buff=0.08)
            dec_cards.move_to(np.array([DEC_X, dec_inp_y, 0]))

            step_txt = Text(f"Step {step+1}", font_size=18, weight="BOLD")
            step_txt.set_color("#FF6B9D")
            step_txt.move_to(np.array([DEC_X, dec_inp_y - 0.60, 0]))

            if step_ref[0]:
                self.play(FadeOut(step_ref[0]), run_time=0.12)
            step_ref[0] = step_txt
            self.play(FadeIn(step_txt), run_time=0.20)

            d_arr = Arrow(dec_cards.get_top(), dec_blks[0].get_bottom(),
                          buff=0.04, fill_color=C_ARR, thickness=1.5)
            self.play(LaggedStart(*[FadeIn(c, shift=UP*0.06) for c in dec_cards],
                      lag_ratio=0.05, run_time=0.30))
            self.play(GrowArrow(d_arr), run_time=0.20)

            for i in range(N):
                run_p(np.array([spine_x, dec_blks[i].get_center()[1], 0]),
                      dec_blks[i].get_center(), C_CROSS, rt=0.08)
            for i in range(N):
                self.play(Indicate(dec_blks[i], color=WHITE, scale_factor=1.03), run_time=0.06)

            pred_w = russian[step]
            pred_c = tok(pred_w, C_PRED, fs=18)
            pred_c.move_to(np.array([DEC_X, out_y, 0]))
            o_arr = Arrow(dec_blks[-1].get_top(), pred_c.get_bottom(),
                          buff=0.04, fill_color=C_PRED, thickness=1.5)
            self.play(GrowArrow(o_arr), run_time=0.15)
            self.play(FadeIn(pred_c, shift=UP*0.06), run_time=0.25)
            self.play(Indicate(pred_c, color=WHITE, scale_factor=1.08), run_time=0.20)
            self.wait(1)

            if step < len(russian) - 1:
                self.play(*[FadeOut(m) for m in [dec_cards, d_arr, o_arr, pred_c]], run_time=0.20)
            else:
                done = Text("Generation complete!", font_size=20, weight="BOLD")
                done.set_color("#2ECC71").next_to(pred_c, RIGHT, buff=0.21)
                self.play(FadeIn(done), run_time=0.30)
                self.wait(2)
                self.play(*[FadeOut(m) for m in [dec_cards, d_arr, o_arr, pred_c, done]], run_time=0.30)

        if step_ref[0]:
            self.play(FadeOut(step_ref[0]), run_time=0.12)

        # Fade ALL inference stuff + architecture
        inf_all = [inf_lbl, inf_inp, inf_arr,
                   *enc_blks, *dec_blks, *enc_arr, *dec_arr,
                   cross_spine, *cross_to_dec]
        self.play(*[FadeOut(m) for m in inf_all], run_time=0.50)
        self.wait(0.5)

        # ══════════════════════════════════════════════
        #  PHASE 4 — Summary: how encoder/decoder behave
        # ══════════════════════════════════════════════
        sum_title = Text("Summary", font_size=55, weight="BOLD")
        sum_title.set_color(WHITE).move_to(UP * 3.5)
        self.play(FadeIn(sum_title), run_time=0.40)

        # Training summary
        tr_head = Text("Training", font_size=32, weight="BOLD")
        tr_head.set_color("#E74C3C")

        tr_enc = Text("Encoder:  processes full input at once", font_size=22, weight="BOLD")
        tr_enc.set_color("#5DADE2")
        tr_dec = Text("Decoder:  sees ALL target tokens (teacher forcing)", font_size=22, weight="BOLD")
        tr_dec.set_color("#58D68D")
        tr_par = Text("Everything runs in PARALLEL", font_size=22, weight="BOLD")
        tr_par.set_color("#2ECC71")

        tr_grp = VGroup(tr_head, tr_enc, tr_dec, tr_par)
        tr_grp.arrange(DOWN, buff=0.30, aligned_edge=LEFT)
        tr_grp.move_to(UP * 1.8 + LEFT * 0.5)

        # Inference summary
        inf_head = Text("Inference", font_size=32, weight="BOLD")
        inf_head.set_color("#9B59B6")

        inf_enc = Text("Encoder:  runs ONCE on the input", font_size=22, weight="BOLD")
        inf_enc.set_color("#5DADE2")
        inf_dec = Text("Decoder:  generates ONE token at a time", font_size=22, weight="BOLD")
        inf_dec.set_color("#58D68D")
        inf_loop = Text("Each new token feeds back as input", font_size=22, weight="BOLD")
        inf_loop.set_color(C_OUT)
        inf_eos = Text("Stops when <EOS> is predicted", font_size=22, weight="BOLD")
        inf_eos.set_color(C_PRED)

        inf_auto = Text("This is called AUTOREGRESSIVE generation", font_size=22, weight="BOLD")
        inf_auto.set_color("#FF6B9D")
        inf_grp = VGroup(inf_head, inf_enc, inf_dec, inf_loop, inf_eos, inf_auto)
        inf_grp.arrange(DOWN, buff=0.30, aligned_edge=LEFT)
        inf_grp.move_to(DOWN * 1.6 + LEFT * 0.5)
        inf_grp.align_to(tr_grp, LEFT)

        # Divider
        divider = Line(LEFT * 5, RIGHT * 5, stroke_width=1.5)
        divider.set_color(GREY).set_opacity(0.40)
        divider.move_to((tr_grp.get_bottom() + inf_grp.get_top()) / 2)

        # Animate
        for line in tr_grp:
            self.play(FadeIn(line, shift=UP * 0.10), run_time=0.40)
            self.wait(0.8)

        self.play(ShowCreation(divider), run_time=0.25)

        for line in inf_grp:
            self.play(FadeIn(line, shift=UP * 0.10), run_time=0.40)
            self.wait(0.8)

        self.wait(3)

        # ── Parallel vs Sequential visual ──
        self.play(*[FadeOut(m) for m in [sum_title, tr_grp, inf_grp, divider]], run_time=0.40)
        self.wait(0.3)

        pv_title = Text("Parallel vs Sequential", font_size=42, weight="BOLD")
        pv_title.set_color(WHITE).move_to(UP * 3.5)
        self.play(FadeIn(pv_title), run_time=0.40)

        # Training: all 5 tokens processed simultaneously (parallel bars)
        par_lbl = Text("Training (Parallel)", font_size=24, weight="BOLD")
        par_lbl.set_color("#E74C3C").move_to(UP * 2.2 + LEFT * 3.5)

        par_bars = VGroup()
        tok_names = ["<SOS>", "\u044f", "\u0442\u0435\u0431\u044f", "\u043b\u044e\u0431\u043b\u044e"]
        for i, tn in enumerate(tok_names):
            bar = Rectangle(width=4.0, height=0.35)
            bar.set_fill("#2ECC71", 0.70).set_stroke(WHITE, 1.0)
            bar.move_to(UP * (1.4 - i * 0.50) + LEFT * 1.0)
            lbl = Text(tn, font_size=14, weight="BOLD")
            lbl.set_color(WHITE).move_to(bar)
            par_bars.add(VGroup(bar, lbl))

        time_arr_p = Arrow(LEFT * 3.0 + UP * 2.0, LEFT * 3.0 + DOWN * 0.3,
                           buff=0, fill_color=GREY, thickness=2).shift(LEFT*0.17)
        time_lbl_p = Text("time", font_size=25, weight="BOLD")
        time_lbl_p.set_color(GREY).next_to(time_arr_p, LEFT, buff=0.08).rotate(PI/2)

        self.play(FadeIn(par_lbl), run_time=0.25)
        self.play(
            *[GrowFromEdge(b, LEFT) for b in par_bars],
            ShowCreation(time_arr_p), FadeIn(time_lbl_p),
            run_time=0.80,
        )
        self.wait(1)

        same_note = Text("All at the same time!", font_size=20, weight="BOLD")
        same_note.set_color("#2ECC71").next_to(par_bars, RIGHT, buff=0.42).scale(1.3).shift(RIGHT*0.65)
        self.play(FadeIn(same_note), run_time=0.30)
        self.wait(1.5)

        # Inference: tokens processed one after another (staggered bars)
        seq_lbl = Text("Inference (Sequential)", font_size=24, weight="BOLD")
        seq_lbl.set_color("#9B59B6").move_to(DOWN * 1.2 + LEFT * 3.5)

        seq_bars = VGroup()
        for i, tn in enumerate(tok_names):
            bar = Rectangle(width=1.2, height=0.35)
            bar.set_fill("#F39C12", 0.70).set_stroke(WHITE, 1.0)
            bar.move_to(DOWN * (2.0 + i * 0.50) + LEFT * (1.8 - i * 1.1))
            lbl = Text(tn, font_size=12, weight="BOLD")
            lbl.set_color(WHITE).move_to(bar)
            seq_bars.add(VGroup(bar, lbl))

        time_arr_s = Arrow(LEFT * 3.0 + DOWN * 1.5, LEFT * 3.0 + DOWN * 4.2,
                           buff=0, fill_color=GREY, thickness=2)
        time_lbl_s = Text("time", font_size=25, weight="BOLD")
        time_lbl_s.set_color(GREY).next_to(time_arr_s, LEFT, buff=0.08).rotate(PI/2)

        self.play(FadeIn(seq_lbl), ShowCreation(time_arr_s), self.camera.frame.animate.shift(DOWN*0.3) ,FadeIn(time_lbl_s),
                  run_time=0.30)
        for bar in seq_bars:
            self.play(GrowFromEdge(bar, LEFT),run_time=0.40)
            self.wait(0.3)

        wait_note = Text("Must wait for each token!", font_size=20, weight="BOLD")
        wait_note.set_color("#F39C12").next_to(seq_bars, RIGHT, buff=0.30).scale(1.2)
        self.play(FadeIn(wait_note), run_time=0.30)
        self.wait(3)

        pv_all = [pv_title, par_lbl, par_bars, time_arr_p, time_lbl_p, same_note,
                  seq_lbl, seq_bars, time_arr_s, time_lbl_s, wait_note]
        self.play(*[FadeOut(m) for m in pv_all], run_time=0.40)
        self.wait(0.3)

        # ── Why better than LSTMs ──

        vs_title = Text("Transformer vs LSTM", font_size=38, weight="BOLD")
        vs_title.set_color(WHITE).move_to(UP * 3.25)
        self.play(FadeIn(vs_title), run_time=0.40)

        lstm_head = Text("LSTM", font_size=30, weight="BOLD")
        lstm_head.set_color("#E74C3C")
        lstm_items = VGroup(
            Text("Sequential — one token at a time", font_size=21, weight="BOLD"),
            Text("Long-range dependencies fade", font_size=21, weight="BOLD"),
            Text("Can't parallelize training", font_size=21, weight="BOLD"),
            Text("Fixed context bottleneck", font_size=21, weight="BOLD"),
        )
        for item in lstm_items:
            item.set_color("#E8A0A0")
        lstm_col = VGroup(lstm_head, *lstm_items)
        lstm_col.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        lstm_col.move_to(LEFT * 3.8 + UP * 0.6)

        tf_head = Text("Transformer", font_size=30, weight="BOLD")
        tf_head.set_color("#2ECC71")
        tf_items = VGroup(
            Text("Parallel — all tokens at once", font_size=21, weight="BOLD"),
            Text("Attention sees everything directly", font_size=21, weight="BOLD"),
            Text("Massive GPU parallelism", font_size=21, weight="BOLD"),
            Text("No bottleneck — direct connections", font_size=21, weight="BOLD"),
        )
        for item in tf_items:
            item.set_color("#A0E8A0")
        tf_col = VGroup(tf_head, *tf_items)
        tf_col.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        tf_col.move_to(RIGHT * 3.44 + UP * 0.6)

        vs_div = Line(UP * 2.5, DOWN * 1.5, stroke_width=2.0)
        vs_div.set_color(GREY).set_opacity(0.40).shift(LEFT*0.2)

        # Animate side by side
        self.play(FadeIn(lstm_head), FadeIn(tf_head), ShowCreation(vs_div), run_time=0.40)
        for i in range(4):
            self.play(
                FadeIn(lstm_items[i], shift=RIGHT * 0.10),
                FadeIn(tf_items[i], shift=LEFT * 0.10),
                run_time=0.40,
            )
            self.wait(1)


        # Winner text
        winner = Text("Transformers scale to billions of parameters!", font_size=26, weight="BOLD")
        winner.set_color("#F1C40F").move_to(DOWN * 2.5).scale(1.3)
        self.play(FadeIn(winner, shift=UP * 0.10), run_time=0.50)
        self.wait(1)

        winner2 = Text("GPT, BERT, T5, LLaMA — all Transformers", font_size=24, weight="BOLD")
        winner2.set_color(GREEN).next_to(winner, DOWN, buff=0.49).scale(1.3)
        self.play(FadeIn(winner2, shift=UP * 0.10), run_time=0.50)
        self.wait(3)

        self.play(*[FadeOut(m) for m in [vs_title, lstm_col, tf_col, vs_div, winner, winner2]],
                  run_time=0.60)
        self.wait(1)


class WhyTransformers(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.30)

        C_RNN  = "#E74C3C"
        C_TOK  = "#3498DB"
        C_CTX  = "#FF0000"
        C_OK   = "#2ECC71"
        C_WARN = "#F39C12"
        C_GREY = "#95A5A6"
        C_BG   = "#34495E"
        C_ATT  = "#F1C40F"

        BW, BH = 1.85, 1.15

        def cell(label, color, pos, fs=32, w=None, h=None):
            r = RoundedRectangle(width=w or BW, height=h or BH, corner_radius=0.10)
            r.set_fill(color, 0.85).set_stroke(WHITE, 2.0)
            r.move_to(pos)
            t = Text(label, font_size=fs, weight="BOLD")
            t.set_color(WHITE).move_to(r)
            return VGroup(r, t)

        def tok(text, color=C_BG, fs=36):
            t = Text(text, font_size=fs, weight="BOLD")
            t.set_color(WHITE)
            bg = RoundedRectangle(
                width=max(t.get_width() + 0.45, 1.00),
                height=0.55, corner_radius=0.08,
            )
            bg.set_fill(color, 0.88).set_stroke(WHITE, 1.2)
            t.move_to(bg)
            return VGroup(bg, t)

        # ══════════════════════════════════════════════
        #  SCENE 1 — Title
        # ══════════════════════════════════════════════
        title = Text("Why Do RNNs & LSTMs Fail?", font_size=56, weight="BOLD")
        title.set_color(WHITE).move_to(ORIGIN)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.70)
        self.wait(2)
        self.play(FadeOut(title), run_time=0.40)
        self.wait(0.5)

        # ══════════════════════════════════════════════
        #  SCENE 2 — Sequential Processing
        # ══════════════════════════════════════════════
        lbl2 = Text("Problem 1: Sequential Processing", font_size=50, weight="BOLD")
        lbl2.set_color(C_RNN).move_to(UP * 3.3)
        self.play(FadeIn(lbl2), run_time=0.35)

        SP = 2.70
        cells2 = [cell(f"h{i+1}", C_RNN, np.array([-6.75 + i * SP, 0.3, 0]))
                  for i in range(6)]
        words2 = ["The", "cat", "sat", "on", "the", "mat"]
        wds2 = [Text(w, font_size=38, weight="BOLD").set_color("#A8DADC").move_to(
                cells2[i].get_center() + DOWN * 1.2) for i, w in enumerate(words2)]
        arrs2 = [Arrow(cells2[i].get_right(), cells2[i+1].get_left(),
                 buff=0.06, fill_color=C_RNN, thickness=1.8,
                 max_tip_length_to_length_ratio=0.25) for i in range(5)]

        for i in range(6):
            self.play(FadeIn(cells2[i]), FadeIn(wds2[i]), run_time=0.35)
            if i < 5:
                self.play(GrowArrow(arrs2[i]), run_time=0.25)

        slow = Text("Each step must WAIT for the previous one!", font_size=35, weight="BOLD")
        slow.set_color(C_RNN).move_to(DOWN * 3.35).scale(1.26)
        self.play(FadeIn(slow), run_time=0.35)
        self.wait(2)


        rnn_bar = Rectangle(width=8.0, height=0.45).scale(1.7)
        rnn_bar.set_fill(C_RNN, 0.70).set_stroke(WHITE, 1.0)
        rnn_bar.move_to(DOWN * 3.2).align_to(LEFT * 4.0, LEFT).shift(UP*0.57).shift(LEFT*2.65)
        rnn_t = Text("Sequential: SLOW", font_size=20, weight="BOLD")
        rnn_t.set_color(WHITE).move_to(rnn_bar).scale(1.7)

        par_bar = Rectangle(width=3.0, height=0.45).scale(1.7)
        par_bar.set_fill(C_OK, 0.70).set_stroke(WHITE, 1.0)
        par_bar.next_to(rnn_bar, DOWN, buff=0.32).align_to(rnn_bar, LEFT)
        par_t = Text("Parallel: FAST", font_size=20, weight="BOLD")
        par_t.set_color(WHITE).move_to(par_bar).scale(1.7)

        self.play(FadeOut(slow))
        self.play(GrowFromEdge(rnn_bar, LEFT), FadeIn(rnn_t), run_time=0.40)
        self.play(GrowFromEdge(par_bar, LEFT), FadeIn(par_t), run_time=0.40)


 
        gpu = Text("GPUs have 1000s of cores — RNNs use just 1!", font_size=24, weight="BOLD")
        gpu.set_color(C_RNN).move_to(lbl2).scale(1.8)
        self.play(FadeIn(gpu), FadeOut(lbl2) ,run_time=0.35)
        self.wait(3)

        self.play(*[FadeOut(m) for m in cells2 + wds2 + arrs2 +
                  [rnn_bar, rnn_t, par_bar, par_t, gpu]], run_time=0.40)
        self.wait(0.3)


        # ══════════════════════════════════════════════
        #  SCENE 3 — Long-Range Dependencies Fade
        # ══════════════════════════════════════════════
        lbl3 = Text("Problem 2: Long-Range Dependencies Fade", font_size=46, weight="BOLD")
        lbl3.set_color(C_RNN).move_to(UP * 3.5)
        self.play(FadeIn(lbl3), run_time=0.35)

        sent = ["The", "food", "at", "the", "place", "...", "was", "great"]
        T3 = len(sent)
        BW3 = BW * 0.6
        SP3 = 2.10
        hx3 = [-(T3 - 1) * SP3 / 2 + i * SP3 for i in range(T3)]
        Y3 = 0.8

        cells3 = [cell(f"h{i+1}", C_RNN, np.array([hx3[i], Y3, 0]), fs=32, w=BW3)
                  for i in range(T3)]
        wds3 = [Text(w, font_size=30, weight="BOLD").set_color("#A8DADC").move_to(
                np.array([hx3[i], Y3 - 1.2, 0])) for i, w in enumerate(sent)]
        arrs3 = [Arrow(cells3[i].get_right(), cells3[i+1].get_left(),
                 buff=0.04, fill_color=C_RNN, thickness=1.5,
                 max_tip_length_to_length_ratio=0.25) for i in range(T3-1)]

        self.play(
            LaggedStart(*[FadeIn(c) for c in cells3], lag_ratio=0.04, run_time=0.50),
            LaggedStart(*[FadeIn(w) for w in wds3], lag_ratio=0.04, run_time=0.50),
        )
        self.play(*[ShowCreation(a) for a in arrs3], run_time=0.35)
        self.wait(1)

        food_hl = SurroundingRectangle(VGroup(cells3[1], wds3[1]), buff=0.08, stroke_width=3.0).scale(1.1)
        food_hl.set_color(C_ATT)
        was_hl = SurroundingRectangle(VGroup(cells3[6], wds3[6]), buff=0.08, stroke_width=3.0).scale(1.1)
        was_hl.set_color(C_ATT)
        self.play(ShowCreation(food_hl), ShowCreation(was_hl), run_time=0.40)
        self.wait(1)


        opacities = [0.1, 0.2, 0.30, 0.40, 0.5, 0.6, 1.0, 1.0]
        fade_anims = []
        for i in range(T3):
            if opacities[i] < 1.0:
                fade_anims.append(cells3[i].animate.set_opacity(opacities[i]))
                fade_anims.append(wds3[i].animate.set_opacity(opacities[i]))
        self.play(*fade_anims, run_time=0.50)


        dep_arc = ArcBetweenPoints(
            cells3[1].get_top() + UP * 0.08,
            cells3[6].get_top() + UP * 0.08,
            angle=-PI / 5,
        )
        dep_arc.set_stroke(C_RNN, width=2.5, opacity=0.40)
        self.play(ShowCreation(dep_arc), run_time=0.50)

        fade_txt = Text("By the time we reach 'was',  'food' is nearly gone!", font_size=26, weight="BOLD")
        fade_txt.set_color(C_RNN).move_to(DOWN * 3.2).scale(1.46)
        self.play(FadeIn(fade_txt), run_time=0.35)
        self.wait(1)


        vanish = Text("Vanishing Gradient Problem", font_size=48, weight="BOLD")
        vanish.set_color(C_RNN).move_to(fade_txt.get_center())
        self.play(FadeIn(vanish), FadeOut(fade_txt) ,run_time=0.35)
        self.wait(3)

        self.play(*[FadeOut(m) for m in cells3 + wds3 + arrs3 +
                  [lbl3, food_hl, was_hl, dep_arc, vanish]], run_time=0.40)
        self.wait(1)

        # ══════════════════════════════════════════════
        #  SCENE 4 — Information Bottleneck
        # ══════════════════════════════════════════════
        lbl4 = Text("Problem 3: Information Bottleneck", font_size=34, weight="BOLD")
        lbl4.set_color(C_RNN).move_to(UP * 3.5).scale(1.56)
        self.play(FadeIn(lbl4), run_time=0.35)

        BW4 = BW * 0.6
        SP4 = 2.10
        enc4 = [cell(f"E{i+1}", C_TOK, np.array([-7.5 + i * SP4, 0.3, 0]), fs=36, w=BW4)
                for i in range(4)]
        enc4_arr = [Arrow(enc4[i].get_right(), enc4[i+1].get_left(),
                    buff=0.04, fill_color=C_TOK, thickness=1.5) for i in range(3)]

        ctx4 = RoundedRectangle(width=1.10, height=0.90, corner_radius=0.12)
        ctx4.set_fill(C_CTX, 0.95).set_stroke(WHITE, 3.0)
        ctx4.move_to(np.array([2.8, 0.3, 0]))
        ctx4_t = Text("C", font_size=32, weight="BOLD")
        ctx4_t.set_color(WHITE).move_to(ctx4)
        ctx4_node = VGroup(ctx4, ctx4_t).shift(LEFT*1.53)

        dec4 = [cell(f"D{i+1}", C_OK, np.array([3.5 + i * SP4, 0.3, 0]), fs=36, w=BW4)
                for i in range(3)]
        dec4_arr = [Arrow(dec4[i].get_right(), dec4[i+1].get_left(),
                    buff=0.04, fill_color=C_OK, thickness=1.5) for i in range(2)]

        ctx_in = Arrow(enc4[-1].get_right(), ctx4.get_left(),
                       buff=0.04, fill_color=C_TOK, thickness=1.8)
        ctx_out = Arrow(ctx4.get_right(), dec4[0].get_left(),
                        buff=0.04, fill_color=C_OK, thickness=1.8)

        ew4 = [Text(w, font_size=39, weight="BOLD").set_color("#A8DADC").move_to(
                enc4[i].get_center() + DOWN * 1.19)
                for i, w in enumerate(["I", "love", "you", "much"])]
        dw4 = [Text(w, font_size=39, weight="BOLD").set_color(C_WARN).move_to(
                dec4[i].get_center() + DOWN * 1.19)
                for i, w in enumerate(["\u044f", "\u0442\u0435\u0431\u044f", "\u043b\u044e\u0431\u043b\u044e"])]

        self.play(*[FadeIn(c) for c in enc4], *[FadeIn(w) for w in ew4],
                  *[ShowCreation(a) for a in enc4_arr], run_time=0.50)
        self.play(GrowArrow(ctx_in), GrowFromCenter(ctx4_node), run_time=0.40)
        self.play(
            Flash(ctx4_node.get_center(), color=C_CTX, line_length=0.3,
                  flash_radius=0.5, num_lines=12),
            run_time=0.40,
        )
        self.play(GrowArrow(ctx_out),
                  *[FadeIn(c) for c in dec4], *[FadeIn(w) for w in dw4],
                  *[ShowCreation(a) for a in dec4_arr], run_time=0.50)
        self.wait(1)


        neck = Text("ALL information squeezed into ONE vector!", font_size=26, weight="BOLD")
        neck.set_color(C_CTX).move_to(DOWN * 3.2).scale(1.5)
        self.play(FadeIn(neck), run_time=0.35)
        self.wait(1)

        self.play(
            enc4[0].animate.set_opacity(0.12), ew4[0].animate.set_opacity(0.12),
            enc4[1].animate.set_opacity(0.25), ew4[1].animate.set_opacity(0.25),
            enc4_arr[0].animate.set_opacity(0.12),
            run_time=0.40,
        )

        lost = Text("Early information is LOST forever!", font_size=26, weight="BOLD")
        lost.set_color(C_CTX).move_to(DOWN * 3.2).scale(1.5)
        self.play(FadeIn(lost), FadeOut(neck), run_time=0.35)
        self.wait(3)

        self.play(*[FadeOut(m) for m in enc4 + dec4 + ew4 + dw4 + enc4_arr + dec4_arr +
                  [lbl4, ctx4_node, ctx_in, ctx_out, lost]], run_time=0.40)

        # ══════════════════════════════════════════════
        #  SCENE 5 — Attention Is All You Need
        # ══════════════════════════════════════════════
        reveal = Text("Attention Is All You Need", font_size=54, weight="BOLD")
        reveal.set_color(WHITE).move_to(ORIGIN).scale(1.3).shift(UP*0.75)
        self.play(FadeIn(reveal, shift=UP * 0.15), run_time=0.80)
        self.play(
            Flash(ORIGIN, color=C_ATT, line_length=1.0,
                  flash_radius=1.5, num_lines=20),
            run_time=0.70,
        )

        sub = Text("Vaswani et al., 2017", font_size=44, weight="BOLD")
        sub.set_color(C_GREY).next_to(reveal, DOWN, buff=0.65)
        self.play(FadeIn(sub), run_time=0.40)
        self.wait(2)


class FFNBlock(InteractiveScene):
    """Visualise the position-wise FFN as a real neural network diagram.
    512 → 2048 (ReLU) → 512
    """

    def construct(self):

        a = self.camera.frame

        C_IN   = "#3498DB"
        C_HID  = "#9B59B6"
        C_OUT  = "#2ECC71"
        C_GREY = "#95A5A6"
        C_WIRE = "#7F8C8D"

        RADIUS = 0.22

        def make_layer(n_top, n_bot, x, color, top_y=2.0, spacing=0.85):
            """n_top circles, then dots, then n_bot circles."""
            nodes_top = []
            for i in range(n_top):
                c = Circle(radius=RADIUS)
                c.set_fill(color, 0.85).set_stroke(WHITE, 1.5)
                c.move_to(np.array([x, top_y - i * spacing, 0]))
                nodes_top.append(c)

            dots = Text(":", font_size=52, weight="BOLD").set_color(WHITE)
            dots.move_to(np.array([x, top_y - n_top * spacing, 0]))

            nodes_bot = []
            for i in range(n_bot):
                c = Circle(radius=RADIUS)
                c.set_fill(color, 0.85).set_stroke(WHITE, 1.5)
                c.move_to(np.array([x, top_y - (n_top + 1 + i) * spacing, 0]))
                nodes_bot.append(c)

            all_nodes = nodes_top + nodes_bot
            return VGroup(*all_nodes), dots, all_nodes

        # ── three layers: 3 top + dots + 1 bottom for 512, more for 2048 ──
        X_IN, X_HID, X_OUT = -4.0, 0.0, 4.0

        in_group, in_dots, in_nodes = make_layer(3, 1, X_IN, C_IN)
        hid_group, hid_dots, hid_nodes = make_layer(4, 2, X_HID, C_HID, top_y=2.5, spacing=0.75)
        out_group, out_dots, out_nodes = make_layer(3, 1, X_OUT, C_OUT)

        # ── layer labels ──
        in_label = Text("512", font_size=28, weight="BOLD").set_color(C_IN)
        in_label.next_to(in_group, DOWN, buff=0.35)

        hid_label = Text("2048 (ReLU)", font_size=28, weight="BOLD").set_color(C_HID)
        hid_label.next_to(hid_group, DOWN, buff=0.35)

        out_label = Text("512", font_size=28, weight="BOLD").set_color(C_OUT)
        out_label.next_to(out_group, DOWN, buff=0.35)

        # ── formula at bottom ──
        formula = Text("FFN(x) = max(0, xW₁ + b₁)W₂ + b₂", font_size=39, weight="BOLD")
        formula.set_color(C_GREY).to_edge(DOWN, buff=0.55).shift(DOWN*0.75)

        # ── wires: input → hidden ──
        wires_ih = VGroup()
        for n_in in in_nodes:
            for n_hid in hid_nodes:
                l = Line(n_in.get_right(), n_hid.get_left(), stroke_width=0.5)
                l.set_stroke(C_WIRE, opacity=0.25)
                wires_ih.add(l)

        # ── wires: hidden → output ──
        wires_ho = VGroup()
        for n_hid in hid_nodes:
            for n_out in out_nodes:
                l = Line(n_hid.get_right(), n_out.get_left(), stroke_width=0.5)
                l.set_stroke(C_WIRE, opacity=0.25)
                wires_ho.add(l)



        # ── animate ──
        # Input layer
        self.play(
            LaggedStart(*[FadeIn(n, scale=0.5) for n in in_nodes], lag_ratio=0.08),
            FadeIn(in_dots),
            FadeIn(in_label),
            run_time=0.6,
        )
        self.wait(0.5)

        # Wires to hidden
        self.play(
            LaggedStart(*[ShowCreation(w) for w in wires_ih], lag_ratio=0.01),
            run_time=0.8,
        )
        self.wait(0.3)

        # Hidden layer
        self.play(
            LaggedStart(*[FadeIn(n, scale=0.5) for n in hid_nodes], lag_ratio=0.06),
            FadeIn(hid_dots),
            FadeIn(hid_label),
            run_time=0.6,
        )
        self.wait(0.5)

        # Wires to output
        self.play(
            LaggedStart(*[ShowCreation(w) for w in wires_ho], lag_ratio=0.01),
            run_time=0.8,
        )
        self.wait(0.3)

        # Output layer
        self.play(
            LaggedStart(*[FadeIn(n, scale=0.5) for n in out_nodes], lag_ratio=0.08),
            FadeIn(out_dots),
            FadeIn(out_label),
            run_time=0.6,
        )
        self.wait(0.5)


        # Highlight wires briefly
        self.play(
            wires_ih.animate.set_stroke(opacity=0.6),
            wires_ho.animate.set_stroke(opacity=0.6),
            run_time=0.5,
        )
        self.play(
            wires_ih.animate.set_stroke(opacity=0.25),
            wires_ho.animate.set_stroke(opacity=0.25),
            run_time=0.5,
        )
        self.wait(0.5)

        # Formula at the end
        self.play(FadeIn(formula), a.animate.shift(DOWN*0.7) ,run_time=0.5)
        self.wait(2)


        self.embed()


class SelfAttentionIntuition(InteractiveScene):
    """Visualise self-attention: score matrix with colored heatmap,
    showing how every token attends to every other token."""

    def construct(self):
        self.camera.frame.scale(1.25)

        C_Q   = "#E74C3C"
        C_K   = "#3498DB"
        C_V   = "#2ECC71"
        C_ATT = "#F1C40F"
        C_BG  = "#34495E"
        C_GREY = "#95A5A6"

        words = ["The", "cat", "sat", "on", "it"]
        N = len(words)

        # Attention scores (fake but intuitive — "cat" attends to "sat",
        # "it" attends to "cat", etc.)
        # rows = query (who is asking), cols = key (who is being looked at)
        scores = np.array([
            [0.05, 0.15, 0.10, 0.60, 0.10],   # The
            [0.10, 0.15, 0.55, 0.05, 0.15],   # cat → sat
            [0.05, 0.50, 0.10, 0.25, 0.10],   # sat → cat
            [0.10, 0.10, 0.15, 0.10, 0.55],   # on → it
            [0.08, 0.62, 0.10, 0.10, 0.10],   # it → cat
        ])

        CELL = 0.85
        GRID_X = -0.5
        GRID_Y = 1.5

        # ═══════════════════════════════════════
        #  PART 1 — Build the grid
        # ═══════════════════════════════════════

        # Column headers (Keys)
        col_headers = VGroup()
        for j, w in enumerate(words):
            t = Text(w, font_size=28, weight="BOLD")
            t.set_color(C_K)
            t.move_to(np.array([
                GRID_X + j * CELL,
                GRID_Y + CELL * 0.85,
                0
            ]))
            col_headers.add(t)

        # Row headers (Queries)
        row_headers = VGroup()
        for i, w in enumerate(words):
            t = Text(w, font_size=28, weight="BOLD")
            t.set_color(C_Q)
            t.move_to(np.array([
                GRID_X - CELL * 1.1,
                GRID_Y - i * CELL,
                0
            ]))
            row_headers.add(t)

        # Grid cells
        cells = [[None]*N for _ in range(N)]
        cell_texts = [[None]*N for _ in range(N)]
        cell_rects = [[None]*N for _ in range(N)]

        for i in range(N):
            for j in range(N):
                s = scores[i][j]
                # Color interpolation: low=dark grey, high=bright yellow
                r = RoundedRectangle(
                    width=CELL * 0.92, height=CELL * 0.92,
                    corner_radius=0.06,
                )
                color = interpolate_color(C_BG, C_ATT, s)
                r.set_fill(color, opacity=0.9)
                r.set_stroke(WHITE, 1.0)
                r.move_to(np.array([
                    GRID_X + j * CELL,
                    GRID_Y - i * CELL,
                    0
                ]))

                val = Text(f"{s:.2f}", font_size=20, weight="BOLD")
                val.set_color(WHITE if s < 0.4 else BLACK)
                val.move_to(r)

                cell_rects[i][j] = r
                cell_texts[i][j] = val
                cells[i][j] = VGroup(r, val)

        all_cells = VGroup(*[cells[i][j] for i in range(N) for j in range(N)])

        self.camera.frame.scale(0.56).shift(RIGHT*0.97)

        # ═══════════════════════════════════════
        #  ANIMATE — everything in one go
        # ═══════════════════════════════════════
        self.play(
            LaggedStart(*[FadeIn(h, shift=DOWN*0.2) for h in col_headers], lag_ratio=0.06),
            LaggedStart(*[FadeIn(h, shift=RIGHT*0.2) for h in row_headers], lag_ratio=0.06),
            LaggedStart(*[FadeIn(cells[i][j], scale=0.8)
                          for i in range(N) for j in range(N)], lag_ratio=0.02),
            run_time=1.2,
        )
        self.wait(2)

        # ═══════════════════════════════════════
        #  Red highlight that transforms between 3 cells
        # ═══════════════════════════════════════
        highlights = [
            (1, 2),  # cat → sat  (off-diagonal)
            (2, 2),  # sat → sat  (diagonal)
            (4, 1),  # it → cat   (corner-ish)
        ]

        # Create first highlight
        hl = SurroundingRectangle(
            cell_rects[highlights[0][0]][highlights[0][1]],
            buff=0.04, stroke_width=3.5, color=RED,
        )
        self.play(ShowCreation(hl), run_time=0.4)
        self.wait(2.5)

        # Transform to each next cell
        for qi, ki in highlights[1:]:
            new_hl = SurroundingRectangle(
                cell_rects[qi][ki],
                buff=0.04, stroke_width=3.5, color=RED,
            )
            self.play(Transform(hl, new_hl), run_time=0.5)
            self.wait(2.5)

        self.play(FadeOut(hl), run_time=0.3)
        self.wait(1)


class QKVRealLifeIntuition(InteractiveScene):
    """YouTube analogy for Q, K, V:
    Q = what the viewer searches for,
    K = video thumbnail/title (what it advertises),
    V = actual video content delivered."""

    def construct(self):
        self.camera.frame.scale(1.30)

        C_GAMER  = "#E74C3C"
        C_STUDENT = "#3498DB"
        C_CHILL  = "#9B59B6"
        C_Q      = "#E74C3C"
        C_K      = "#F39C12"
        C_V      = "#2ECC71"
        C_ATT    = "#F1C40F"
        C_YT     = "#FF0000"

        def card(text, color, fs=28, pad_w=0.7, pad_h=0.4):
            t = Text(text, font_size=fs, weight="BOLD").set_color(WHITE)
            bg = RoundedRectangle(
                width=t.get_width() + pad_w,
                height=t.get_height() + pad_h,
                corner_radius=0.12,
            )
            bg.set_fill(color, 0.85).set_stroke(WHITE, 2.0)
            t.move_to(bg)
            return VGroup(bg, t)

        def outline_card(text, color, fs=22, pad_w=0.5, pad_h=0.35):
            t = Text(text, font_size=fs, weight="BOLD").set_color(color)
            bg = RoundedRectangle(
                width=t.get_width() + pad_w,
                height=t.get_height() + pad_h,
                corner_radius=0.10,
            )
            bg.set_fill(color, 0.12).set_stroke(color, 2.0)
            t.move_to(bg)
            return VGroup(bg, t)

        # ═══════════════════════════════════════
        #  Layout
        # ═══════════════════════════════════════
        COL_X = [-5.0, 0.0, 5.0]
        ROW_Y = [3.5, 1.8, -0.2, -2.2]

        # ═══════════════════════════════════════
        #  YouTube logo / context
        # ═══════════════════════════════════════
        yt = card("YouTube", C_YT, fs=36, pad_w=0.8, pad_h=0.4)
        yt.move_to(ORIGIN)
        self.play(FadeIn(yt, scale=0.8), run_time=0.5)
        self.wait(1.5)
        self.play(yt.animate.scale(0.55).move_to(np.array([7.5, 4.5, 0])), run_time=0.5)

        # ═══════════════════════════════════════
        #  Row 0 — Three viewers
        # ═══════════════════════════════════════
        viewers_data = [
            ("Gamer",    C_GAMER),
            ("Student",  C_STUDENT),
            ("Night Owl", C_CHILL),
        ]
        viewers = []
        for i, (name, color) in enumerate(viewers_data):
            c = card(name, color, fs=28)
            c.move_to(np.array([COL_X[i], ROW_Y[0], 0]))
            viewers.append(c)

        self.play(
            LaggedStart(*[FadeIn(v, shift=DOWN*0.3) for v in viewers], lag_ratio=0.12),
            run_time=0.7,
        )
        self.wait(2)

        # ═══════════════════════════════════════
        #  Row 1 — Q: What each viewer types in search
        # ═══════════════════════════════════════
        q_data = [
            ("Search:\nbest FPS games",       C_Q),
            ("Search:\nlearn Python fast",     C_Q),
            ("Search:\nrelaxing music",        C_Q),
        ]
        q_cards = []
        q_arrows = []
        for i, (text, color) in enumerate(q_data):
            c = outline_card(text, color, fs=21)
            c.move_to(np.array([COL_X[i], ROW_Y[1], 0]))
            q_cards.append(c)

            arr = Arrow(viewers[i].get_bottom(), c.get_top(), buff=0.10,
                        fill_color=color, thickness=1.5,
                        max_tip_length_to_length_ratio=0.25)
            q_arrows.append(arr)

        for i in range(3):
            self.play(GrowArrow(q_arrows[i]), FadeIn(q_cards[i], shift=DOWN*0.15),
                      run_time=0.4)
            self.wait(1.5)
        self.wait(1)

        # ═══════════════════════════════════════
        #  Row 2 — K: Video thumbnail / title
        #  (what the video advertises to match the search)
        # ═══════════════════════════════════════
        k_data = [
            ("Thumbnail:\nTop 10 FPS 2025",       C_K),
            ("Thumbnail:\nPython in 1 Hour",       C_K),
            ("Thumbnail:\nLofi Beats 24/7",        C_K),
        ]
        k_cards = []
        k_arrows = []
        for i, (text, color) in enumerate(k_data):
            c = outline_card(text, color, fs=21)
            c.move_to(np.array([COL_X[i], ROW_Y[2], 0]))
            k_cards.append(c)

            arr = Arrow(q_cards[i].get_bottom(), c.get_top(), buff=0.10,
                        fill_color=C_ATT, thickness=1.5,
                        max_tip_length_to_length_ratio=0.25)
            k_arrows.append(arr)

        for i in range(3):
            self.play(GrowArrow(k_arrows[i]), FadeIn(k_cards[i], shift=DOWN*0.15),
                      run_time=0.4)
            self.wait(1.5)
        self.wait(1)

        # ═══════════════════════════════════════
        #  Flash Q-K match
        # ═══════════════════════════════════════
        for i in range(3):
            self.play(
                k_arrows[i].animate.set_color(C_ATT),
                Flash(k_arrows[i].get_center(), color=C_ATT,
                      line_length=0.2, flash_radius=0.35, num_lines=8),
                run_time=0.35,
            )
        self.wait(2)

        # ═══════════════════════════════════════
        #  Row 3 — V: Actual video content delivered
        # ═══════════════════════════════════════
        v_data = [
            ("Gameplay footage,\ngun stats, reviews",    C_V),
            ("Code examples,\nprojects, exercises",      C_V),
            ("Calm piano,\nrain sounds, beats",          C_V),
        ]
        v_cards = []
        v_arrows = []
        for i, (text, color) in enumerate(v_data):
            c = outline_card(text, color, fs=21)
            c.move_to(np.array([COL_X[i], ROW_Y[3], 0]))
            v_cards.append(c)

            arr = Arrow(k_cards[i].get_bottom(), c.get_top(), buff=0.10,
                        fill_color=color, thickness=1.8,
                        max_tip_length_to_length_ratio=0.25)
            v_arrows.append(arr)

        for i in range(3):
            self.play(GrowArrow(v_arrows[i]), FadeIn(v_cards[i], shift=DOWN*0.15),
                      run_time=0.4)
            self.wait(1.5)
        self.wait(2)

        # ═══════════════════════════════════════
        #  REVEAL — Q, K, V labels on the left
        # ═══════════════════════════════════════
        def row_label(text, color, y, x=-7.8):
            t = Text(text, font_size=40, weight="BOLD").set_color(color)
            t.move_to(np.array([x, y, 0]))
            return t

        lbl_q = row_label("Q", C_Q,  ROW_Y[1])
        lbl_k = row_label("K", C_K,  ROW_Y[2])
        lbl_v = row_label("V", C_V,  ROW_Y[3])

        self.play(FadeIn(lbl_q, shift=RIGHT*0.2), run_time=0.4)
        self.wait(1.5)
        self.play(FadeIn(lbl_k, shift=RIGHT*0.2), run_time=0.4)
        self.wait(1.5)
        self.play(FadeIn(lbl_v, shift=RIGHT*0.2), run_time=0.4)
        self.wait(4)


class AttentionArcs(InteractiveScene):
    """Show attention as curved arcs between word cards.
    Thicker + opaque = high attention, thinner + faint = low."""

    def construct(self):
        self.camera.frame.scale(1.20)

        words = ["Fish", "swim", "near", "the", "bank"]
        N = len(words)
        colors = ["#E74C3C", "#3498DB", "#95A5A6", "#95A5A6", "#2ECC71"]

        # Attention scores — who attends to whom (row=source)
        #              Fish  swim  near  the   bank
        scores = [
            [0.00, 0.58, 0.05, 0.05, 0.12],   # Fish → swim
            [0.50, 0.00, 0.10, 0.05, 0.15],   # swim → Fish
            [0.08, 0.10, 0.00, 0.12, 0.50],   # near → bank
            [0.05, 0.05, 0.15, 0.00, 0.55],   # the → bank
            [0.15, 0.45, 0.30, 0.05, 0.00],   # bank → swim, near
        ]

        # ═══════════════════════════════════════
        #  Word cards
        # ═══════════════════════════════════════
        cards = VGroup()
        for w, c in zip(words, colors):
            t = Text(w, font_size=48, weight="BOLD").set_color(WHITE)
            bg = RoundedRectangle(
                width=t.get_width() + 0.65,
                height=0.85,
                corner_radius=0.10,
            )
            bg.set_fill(c, 0.85).set_stroke(WHITE, 1.5)
            t.move_to(bg)
            cards.add(VGroup(bg, t))

        cards.arrange(RIGHT, buff=0.9)
        cards.move_to(ORIGIN)

        self.play(
            LaggedStart(*[FadeIn(c, shift=DOWN*0.1) for c in cards], lag_ratio=0.08),
            run_time=0.7,
        )
        self.wait(1.5)

        # ═══════════════════════════════════════
        #  Show arcs — one source word at a time
        # ═══════════════════════════════════════
        for src in range(N):
            arcs = []
            for tgt in range(N):
                if tgt == src:
                    continue
                wt = scores[src][tgt]
                if wt < 0.03:
                    continue

                s = cards[src].get_top() + UP * 0.06
                e = cards[tgt].get_top() + UP * 0.06

                # Arc curves away from the line
                dist = abs(src - tgt)
                angle = -PI / (2.5 + dist * 0.3)
                if src > tgt:
                    angle = -angle

                arc = ArcBetweenPoints(s, e, angle=angle)
                arc.set_stroke(
                    colors[src],
                    width=1.0 + wt * 14,
                    opacity=0.15 + wt * 1.4,
                )
                arcs.append(arc)

            # Highlight source card
            self.play(
                cards[src][0].animate.set_stroke(WHITE, 3.5),
                run_time=0.2,
            )
            self.play(
                *[ShowCreation(a) for a in arcs],
                run_time=0.6,
            )
            self.wait(2.5)
            self.play(
                *[Uncreate(a) for a in arcs],
                cards[src][0].animate.set_stroke(WHITE, 1.5),
                run_time=0.45,
            )
            self.wait(0.3)

        # ═══════════════════════════════════════
        #  Fade out first sentence, show "I went to the bank"
        # ═══════════════════════════════════════
        self.play(*[FadeOut(c) for c in cards], run_time=0.5)
        self.wait(0.5)

        words2 = ["I", "went", "to", "the", "bank"]
        N2 = len(words2)
        colors2 = ["#2ECC71", "#3498DB", "#95A5A6", "#95A5A6", "#E74C3C"]

        #              I     went  to    the   bank
        scores2 = [
            [0.00, 0.55, 0.05, 0.05, 0.15],   # I → went
            [0.45, 0.00, 0.10, 0.08, 0.17],   # went → I
            [0.05, 0.08, 0.00, 0.17, 0.50],   # to → bank
            [0.05, 0.05, 0.10, 0.00, 0.60],   # the → bank
            [0.12, 0.40, 0.25, 0.08, 0.00],   # bank → went, to
        ]

        cards2 = VGroup()
        for w, c in zip(words2, colors2):
            t = Text(w, font_size=48, weight="BOLD").set_color(WHITE)
            bg = RoundedRectangle(
                width=t.get_width() + 0.65,
                height=0.85,
                corner_radius=0.10,
            )
            bg.set_fill(c, 0.85).set_stroke(WHITE, 1.5)
            t.move_to(bg)
            cards2.add(VGroup(bg, t))

        cards2.arrange(RIGHT, buff=0.9)
        cards2.move_to(ORIGIN)

        self.play(
            LaggedStart(*[FadeIn(c, shift=DOWN*0.1) for c in cards2], lag_ratio=0.08),
            run_time=0.7,
        )
        self.wait(1.5)

        # Show arcs word by word
        for src in range(N2):
            arcs2 = []
            for tgt in range(N2):
                if tgt == src:
                    continue
                wt = scores2[src][tgt]
                if wt < 0.03:
                    continue

                s = cards2[src].get_top() + UP * 0.06
                e = cards2[tgt].get_top() + UP * 0.06

                dist = abs(src - tgt)
                angle = -PI / (2.5 + dist * 0.3)
                if src > tgt:
                    angle = -angle

                arc = ArcBetweenPoints(s, e, angle=angle)
                arc.set_stroke(
                    colors2[src],
                    width=1.0 + wt * 14,
                    opacity=0.15 + wt * 1.4,
                )
                arcs2.append(arc)

            self.play(
                cards2[src][0].animate.set_stroke(WHITE, 3.5),
                run_time=0.2,
            )
            self.play(
                *[ShowCreation(a) for a in arcs2],
                run_time=0.6,
            )
            self.wait(2.5)
            self.play(
                *[Uncreate(a) for a in arcs2],
                cards2[src][0].animate.set_stroke(WHITE, 1.5),
                run_time=0.45,
            )
            self.wait(0.3)

        self.wait(2)


class WhyQKV(InteractiveScene):
    """Why naive self-attention fails and why we need Q, K, V.
    Core insight: naive has NO parameters (just E dot E),
    same embedding forced into 3 roles, and W_Q/W_K/W_V fix this."""

    def construct(self):
        self.camera.frame.scale(1.25)

        C_EMB   = "#9B59B6"
        C_Q     = "#E74C3C"
        C_K     = "#F39C12"
        C_V     = "#2ECC71"
        C_GREY  = "#95A5A6"
        C_FAIL  = "#E74C3C"
        C_OK    = "#2ECC71"
        C_ATT   = "#F1C40F"
        C_BG    = "#34495E"
        C_W     = "#1ABC9C"

        def word_card(text, color=C_BG, fs=44):
            t = Text(text, font_size=fs, weight="BOLD").set_color(WHITE)
            bg = RoundedRectangle(
                width=t.get_width() + 0.6, height=0.9,
                corner_radius=0.10,
            )
            bg.set_fill(color, 0.85).set_stroke(WHITE, 1.5)
            t.move_to(bg)
            return VGroup(bg, t)

        def vec_block(color, width=2.0, height=0.55, label=""):
            r = RoundedRectangle(width=width, height=height, corner_radius=0.08)
            r.set_fill(color, 0.75).set_stroke(WHITE, 1.5)
            if label:
                t = Tex(label, font_size=38).set_color(WHITE)
                t.move_to(r)
                return VGroup(r, t)
            return r

        def caption(text, color, pos):
            t = Text(text, font_size=24, weight="BOLD").set_color(color)
            bg = RoundedRectangle(
                width=t.get_width() + 0.4,
                height=t.get_height() + 0.25,
                corner_radius=0.08,
            )
            bg.set_fill(color, 0.12).set_stroke(color, 1.5)
            t.move_to(bg)
            g = VGroup(bg, t)
            g.move_to(pos)
            return g

        TXT_Y = -3.5  # caption position

        # ═══════════════════════════════════════════════
        #  PART 1 — Show the full sentence, highlight relationship
        # ═══════════════════════════════════════════════
        words = ["The", "cat", "sat", "on", "it"]
        w_colors = [C_GREY, "#E74C3C", "#3498DB", C_GREY, "#2ECC71"]

        sent_cards = VGroup()
        for w, c in zip(words, w_colors):
            sent_cards.add(word_card(w, c, fs=42))
        sent_cards.arrange(RIGHT, buff=0.7)
        sent_cards.move_to(UP * 2.8)

        self.camera.frame.shift(UP*0.5)

        self.play(
            LaggedStart(*[FadeIn(c, shift=DOWN*0.1) for c in sent_cards], lag_ratio=0.06),
            run_time=0.6,
        )
        self.wait(1.5)

        # ═══════════════════════════════════════════════
        #  PART 2 — Naive fails: E dot E, no parameters
        # ═══════════════════════════════════════════════

        # Show E vectors under "cat" and "it"
        emb_cat = vec_block(C_EMB, label="E")
        emb_it = vec_block(C_EMB, label="E")
        emb_cat.next_to(sent_cards[1], DOWN, buff=0.35)
        emb_it.next_to(sent_cards[4], DOWN, buff=0.35)

        self.play(FadeIn(emb_cat), FadeIn(emb_it), run_time=0.4)
        self.wait(1)

        # Dashed line: E dot E — naive similarity
        dot_line = DashedLine(
            emb_it.get_left(), emb_cat.get_right(),
            dash_length=0.12,
        )
        dot_line.set_stroke(C_FAIL, width=2.0, opacity=0.6)

        dot_label = Text("E . E", font_size=46, weight="BOLD").set_color(C_GREY)
        dot_label.next_to(dot_line, DOWN, buff=0.42)

        self.play(ShowCreation(dot_line), FadeIn(dot_label), run_time=0.5)
        self.wait(1)

        # X — low score, they are not similar
        x_mark = Text("low score!", font_size=44, weight="BOLD").set_color(C_FAIL)
        x_mark.next_to(dot_label, DOWN, buff=0.42)
        self.play(FadeIn(x_mark, scale=1.3), run_time=0.3)
        self.wait(1.5)

        cap1 = caption("No parameters - just raw similarity. Can't learn relationships!", C_FAIL, np.array([0, TXT_Y, 0])).scale(1.2)
        cap1.shift(UP*1.38)
        self.play(FadeIn(cap1), run_time=0.4)
        self.wait(3)


        # ═══════════════════════════════════════════════
        #  PART 3 — Same E acts as 3 things at once
        # ═══════════════════════════════════════════════
        # Fade sentence but keep "it" card and its E
        self.play(
            *[FadeOut(m) for m in [
                *sent_cards,
                emb_cat, dot_line, dot_label, x_mark,
            ]],
            emb_it.animate.move_to(np.array([0, 1.5, 0])),
            run_time=0.5,
        )

        it_label = word_card("it", C_OK, fs=48)
        it_label.next_to(emb_it, UP, buff=0.35)
        self.play(FadeIn(it_label), self.camera.frame.animate.shift(DOWN*0.7) ,run_time=0.3)
        self.wait(1)


        # Three roles pulling from same E
        role_q = Text("       Asking:\n  who do I refer to?", font_size=28, weight="BOLD").set_color(C_Q)
        role_k = Text(" Advertising:\nI am a pronoun", font_size=28, weight="BOLD").set_color(C_K)
        role_v = Text("    Giving:\n reference info", font_size=28, weight="BOLD").set_color(C_V)

        role_q.move_to(np.array([-4, -0.8, 0]))
        role_k.move_to(np.array([0, -0.8, 0]))
        role_v.move_to(np.array([4, -0.8, 0]))

        arr_q = Arrow(emb_it.get_bottom(), role_q.get_top(), buff=0.08,
                      fill_color=C_Q, thickness=1.2, max_tip_length_to_length_ratio=0.25)
        arr_k = Arrow(emb_it.get_bottom(), role_k.get_top(), buff=0.08,
                      fill_color=C_K, thickness=1.2, max_tip_length_to_length_ratio=0.25)
        arr_v = Arrow(emb_it.get_bottom(), role_v.get_top(), buff=0.08,
                      fill_color=C_V, thickness=1.2, max_tip_length_to_length_ratio=0.25)

        cap2 = caption("Same embedding forced into 3 different roles!", C_FAIL, np.array([0, TXT_Y, 0])).shift(UP*0.34)
        self.play(FadeOut(cap1), FadeIn(cap2), self.camera.frame.animate.scale(0.8).shift(DOWN*0.13) ,run_time=0.35)

        self.play(GrowArrow(arr_q), FadeIn(role_q), run_time=0.4)
        self.wait(1.5)
        self.play(GrowArrow(arr_k), FadeIn(role_k), run_time=0.4)
        self.wait(1.5)
        self.play(GrowArrow(arr_v), FadeIn(role_v), run_time=0.4)
        self.wait(2)


        # X marks
        x1 = Text("X", font_size=50, weight="BOLD").set_color(C_FAIL)
        x2 = Text("X", font_size=50, weight="BOLD").set_color(C_FAIL)
        x3 = Text("X", font_size=50, weight="BOLD").set_color(C_FAIL)
        x1.next_to(role_q, DOWN, buff=0.62)
        x2.next_to(role_k, DOWN, buff=0.62)
        x3.next_to(role_v, DOWN, buff=0.62)

        cap3 = caption("One vector cannot specialise for 3 jobs", C_FAIL, np.array([0, TXT_Y, 0])).shift(UP*0.35)
        self.play(
            FadeOut(cap2), FadeIn(cap3),
            FadeIn(x1, scale=1.5), FadeIn(x2, scale=1.5), FadeIn(x3, scale=1.5),
            run_time=0.4,
        )
        self.wait(3)


        # ═══════════════════════════════════════════════
        #  Fade part 3
        # ═══════════════════════════════════════════════
        self.play(
            *[FadeOut(m) for m in [
                it_label, emb_it,
                role_q, role_k, role_v, arr_q, arr_k, arr_v,
                x1, x2, x3, cap3,
            ]],
            run_time=0.5,
        )
        self.wait(0.5)

        # ═══════════════════════════════════════════════
        #  PART 3 — The fix: learned W matrices
        #  E x W_Q = Q,  E x W_K = K,  E x W_V = V
        # ═══════════════════════════════════════════════

        # Show "it" with its E
        card_it2 = word_card("it", C_OK, fs=52)
        card_it2.move_to(np.array([0, 2.35, 0]))
        emb_it2 = vec_block(C_EMB, width=2.4, label="E")
        emb_it2.next_to(card_it2, DOWN, buff=0.4)

        self.play(FadeIn(card_it2), FadeIn(emb_it2), self.camera.frame.animate.shift(DOWN*0.2) ,run_time=0.4)
        self.wait(1)

        # Three W matrices — the learnable parameters
        w_q = vec_block(C_W, width=1.8, height=0.6, label=r"W_Q")
        w_k = vec_block(C_W, width=1.8, height=0.6, label=r"W_K")
        w_v = vec_block(C_W, width=1.8, height=0.6, label=r"W_V")

        w_q.move_to(np.array([-4.0, -0.35, 0]))
        w_k.move_to(np.array([0, -0.35, 0]))
        w_v.move_to(np.array([4.0, -0.35, 0]))


        # Arrows from E down to each W
        arr_wq = Arrow(emb_it2.get_bottom(), w_q.get_top(), buff=0.15,
                       fill_color=C_Q, thickness=2.0, max_tip_length_to_length_ratio=0.2)
        arr_wk = Arrow(emb_it2.get_bottom(), w_k.get_top(), buff=0.15,
                       fill_color=C_K, thickness=2.0, max_tip_length_to_length_ratio=0.2)
        arr_wv = Arrow(emb_it2.get_bottom(), w_v.get_top(), buff=0.15,
                       fill_color=C_V, thickness=2.0, max_tip_length_to_length_ratio=0.2)

        cap4 = caption("Introduce learnable weight matrices", C_W, np.array([0, TXT_Y, 0]))
        self.play(FadeIn(cap4), run_time=0.35)

        self.play(
            GrowArrow(arr_wq), FadeIn(w_q),
            run_time=0.4,
        )
        self.wait(0.5)
        self.play(
            GrowArrow(arr_wk), FadeIn(w_k), 
            run_time=0.4,
        )
        self.wait(0.5)
        self.play(
            GrowArrow(arr_wv), FadeIn(w_v),
            run_time=0.4,
        )
        self.wait(2)

        # Results: Q, K, V — each specialised
        res_q = vec_block(C_Q, width=2.6, label="Q")
        res_k = vec_block(C_K, width=2.6, label="K")
        res_v = vec_block(C_V, width=2.6, label="V")
        res_q.next_to(w_q, DOWN, buff=0.55)
        res_k.next_to(w_k, DOWN, buff=0.55)
        res_v.next_to(w_v, DOWN, buff=0.55)

        # Labels under each
        rl_q = Text("What am I\nlooking for?", font_size=22, weight="BOLD").set_color(C_Q)
        rl_k = Text("What do I\nadvertise?", font_size=22, weight="BOLD").set_color(C_K)
        rl_v = Text("What info\ndo I carry?", font_size=22, weight="BOLD").set_color(C_V)
        rl_q.next_to(res_q, DOWN, buff=0.3)
        rl_k.next_to(res_k, DOWN, buff=0.3)
        rl_v.next_to(res_v, DOWN, buff=0.3)

        arr_rq = Arrow(w_q.get_bottom(), res_q.get_top(), buff=0.08,
                       fill_color=C_Q, thickness=2.0, max_tip_length_to_length_ratio=0.25)
        arr_rk = Arrow(w_k.get_bottom(), res_k.get_top(), buff=0.08,
                       fill_color=C_K, thickness=2.0, max_tip_length_to_length_ratio=0.25)
        arr_rv = Arrow(w_v.get_bottom(), res_v.get_top(), buff=0.08,
                       fill_color=C_V, thickness=2.0, max_tip_length_to_length_ratio=0.25)

        cap5 = caption("Each W learns to extract a DIFFERENT aspect from E", C_W, np.array([0, TXT_Y, 0]))
        self.play(FadeOut(cap4), FadeIn(cap5), run_time=0.35)

        self.play(
            GrowArrow(arr_rq), FadeIn(res_q), FadeIn(rl_q),
            run_time=0.4,
        )
        self.wait(1)
        self.play(
            GrowArrow(arr_rk), FadeIn(res_k), FadeIn(rl_k),
            run_time=0.4,
        )
        self.wait(1)
        self.play(
            GrowArrow(arr_rv), FadeIn(res_v), FadeIn(rl_v),
            run_time=0.4,
        )
        self.wait(2)

        # Highlight: these W's are LEARNED from data
        cap6 = caption("These weights are LEARNED from data during training!", C_ATT, np.array([0, TXT_Y, 0]))
        self.play(
            FadeOut(cap5), FadeIn(cap6),
            w_q[0].animate.set_stroke(C_ATT, 3),
            w_k[0].animate.set_stroke(C_ATT, 3),
            w_v[0].animate.set_stroke(C_ATT, 3),
            run_time=0.5,
        )
        self.play(
            Flash(w_q.get_center(), color=C_ATT, line_length=0.25, flash_radius=0.5, num_lines=8),
            Flash(w_k.get_center(), color=C_ATT, line_length=0.25, flash_radius=0.5, num_lines=8),
            Flash(w_v.get_center(), color=C_ATT, line_length=0.25, flash_radius=0.5, num_lines=8),
            run_time=0.4,
        )
        self.wait(4)

        self.embed()


class TransformerFixesAndLegacy(InteractiveScene):
    """Summary: how Transformers fixed the 3 RNN/LSTM problems,
    and the family of models that followed (GPT, BERT, LLaMA, ...)."""

    def construct(self):
        self.camera.frame.scale(1.25)

        C_PROB   = "#E74C3C"
        C_FIX    = "#2ECC71"
        C_ACC    = "#F1C40F"
        C_GPT    = "#10A37F"
        C_BERT   = "#F39C12"
        C_LLAMA  = "#9B59B6"
        C_GREY   = "#95A5A6"

        def centered_card(lines, color, width=8.5, line_fs=None, line_colors=None):
            """Build a card where every line is center-aligned horizontally
            and stacked vertically. lines is a list of strings."""
            if line_fs is None:
                line_fs = [28] * len(lines)
            if line_colors is None:
                line_colors = [WHITE] * len(lines)

            texts = VGroup()
            for txt, fs, c in zip(lines, line_fs, line_colors):
                t = Text(txt, font_size=fs, weight="BOLD").set_color(c)
                texts.add(t)
            texts.arrange(DOWN, buff=0.22, aligned_edge=ORIGIN)

            bg = RoundedRectangle(
                width=max(texts.get_width() + 0.8, width),
                height=texts.get_height() + 0.7,
                corner_radius=0.14,
            )
            bg.set_fill(color, 0.12).set_stroke(color, 2.0)
            texts.move_to(bg)
            return VGroup(bg, *texts)

        # ═══════════════════════════════════════════════
        #  PART 1 — Three fix cards, no header
        # ═══════════════════════════════════════════════
        fixes_data = [
            (["Sequential Processing", "Largely reduced — parallel attention"], C_FIX),
            (["Information Bottleneck", "Removed — every token attends to every other"], C_FIX),
            (["Long-Range Dependencies", "Handled naturally — direct connections"], C_FIX),
        ]

        fix_cards = []
        for lines, color in fixes_data:
            c = centered_card(
                lines, color, width=9.0,
                line_fs=[32, 24],
                line_colors=[color, WHITE],
            )
            fix_cards.append(c)

        fix_group = VGroup(*fix_cards).arrange(DOWN, buff=0.45)
        fix_group.move_to(ORIGIN)
        self.camera.frame.scale(0.8)

        for card in fix_cards:
            self.play(FadeIn(card, shift=UP*0.15), run_time=0.5)
            self.wait(2)

        self.wait(2)


        # ═══════════════════════════════════════════════
        #  Fade everything out
        # ═══════════════════════════════════════════════
        self.play(*[FadeOut(c) for c in fix_cards], run_time=0.6)

        # ═══════════════════════════════════════════════
        #  PART 2 — Transformers take over
        # ═══════════════════════════════════════════════
        takeover = Text("Transformers took over deep learning...",
                        font_size=39, weight="BOLD").set_color(WHITE)
        takeover.move_to(ORIGIN)

        self.play(FadeIn(takeover, shift=DOWN*0.15), run_time=0.6)
        self.wait(2.5)


        # Family of models — each line center-aligned
        models_data = [
            (["GPT",   "Generative Pre-trained Transformer", "(decoder-only)"],            C_GPT),
            (["BERT",  "Bidirectional Encoder Representations", "(encoder-only)"],          C_BERT),
            (["LLaMA", "Large Language Model Meta AI", "(decoder-only, open weights)"],     C_LLAMA),
        ]

        model_cards = []
        for lines, color in models_data:
            c = centered_card(
                lines, color, width=7.5,
                line_fs=[38, 22, 20],
                line_colors=[color, WHITE, C_GREY],
            )
            model_cards.append(c)

        models_group = VGroup(*model_cards).arrange(DOWN, buff=0.4)
        models_group.move_to(DOWN*0.033)
        self.play(FadeOut(takeover), self.camera.frame.animate.scale(1.1),run_time=0.5)

        for card in model_cards:
            self.play(FadeIn(card, shift=LEFT*0.2), run_time=0.5)
            self.wait(1.8)

        self.wait(4)
