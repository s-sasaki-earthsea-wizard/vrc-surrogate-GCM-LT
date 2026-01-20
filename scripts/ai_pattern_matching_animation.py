"""
AIの「過去問が得意」比喩を解説するアニメーション

従来の数値予報：毎回ゼロから計算（毎回テストを解く）
AIモデル：過去のパターンを学習して当てはめる（過去問で傾向を掴む）

という比喩を視覚的に説明します。

使用方法:
    manim -pql ai_pattern_matching_animation.py AIPatternMatching
    manim -pqh ai_pattern_matching_animation.py AIPatternMatching  # 高画質
"""

from manim import *
import numpy as np


class AIPatternMatching(Scene):
    """AIの「過去問が得意」比喩を解説するアニメーション"""

    def construct(self):
        # タイトル
        self.show_title()

        # 従来の方法：毎回テストを解く
        self.show_traditional_method()

        # AIモデル：過去問で傾向を掴む
        self.show_ai_method()

        # 比較まとめ
        self.show_comparison()

    def show_title(self):
        """タイトルを表示"""
        title = Text("なぜAIは速いのか？", font_size=48)
        subtitle = Text("「過去問」で傾向を掴むAI", font_size=32, color=BLUE)
        subtitle.next_to(title, DOWN, buff=0.4)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

    def create_exam_paper(self, label_text, color=WHITE, scale=1.0):
        """テスト用紙のグラフィックを作成"""
        paper = VGroup()

        # 用紙の外枠
        rect = Rectangle(
            width=2.5 * scale,
            height=3.2 * scale,
            color=color,
            fill_opacity=0.1,
            stroke_width=2,
        )

        # 上部のラベル
        label = Text(label_text, font_size=int(20 * scale), color=color)
        label.move_to(rect.get_top() + DOWN * 0.3 * scale)

        # 問題を示す線
        lines = VGroup()
        for i in range(4):
            line = Line(
                rect.get_left() + RIGHT * 0.3 * scale + DOWN * (0.8 + i * 0.5) * scale,
                rect.get_right() + LEFT * 0.3 * scale + DOWN * (0.8 + i * 0.5) * scale,
                color=GRAY,
                stroke_width=1,
            )
            lines.add(line)

        paper.add(rect, label, lines)
        return paper

    def create_equation_lines(self, num_lines=5):
        """計算式の行を作成"""
        equations = VGroup()
        # 簡略化した数式のような線
        symbols = [
            r"\partial u / \partial t",
            r"+ u \cdot \nabla u",
            r"= -\nabla p / \rho",
            r"+ \nu \nabla^2 u",
            r"+ f \times u",
        ]
        for i, symbol in enumerate(symbols[:num_lines]):
            eq = MathTex(symbol, font_size=24, color=YELLOW)
            equations.add(eq)

        equations.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        return equations

    def show_traditional_method(self):
        """従来の方法：毎回テストを解く"""
        # セクションタイトル
        section_title = Text("従来の方法", font_size=36, color=RED)
        section_title.to_edge(UP)
        self.play(Write(section_title))

        # サブタイトル
        subtitle = Text("「毎回テストの問題を解く」", font_size=28, color=GRAY)
        subtitle.next_to(section_title, DOWN, buff=0.3)
        self.play(Write(subtitle))

        # 問題用紙を表示
        exam = self.create_exam_paper("問題", color=WHITE)
        exam.shift(LEFT * 4)
        self.play(FadeIn(exam))

        # 「今日の天気」という問題
        question = Text("今日の大気状態\nから明日を予測", font_size=20, line_spacing=1.2)
        question.move_to(exam.get_center())
        self.play(Write(question))

        # 計算プロセスを表示（中央）
        calc_area = VGroup()
        calc_title = Text("計算プロセス", font_size=24, color=YELLOW)
        calc_title.shift(UP * 1)

        self.play(Write(calc_title))

        # 方程式を一行ずつ書いていく
        equations = self.create_equation_lines()
        equations.next_to(calc_title, DOWN, buff=0.4)

        # 時間を示すタイマー
        timer_label = Text("経過時間:", font_size=20)
        timer_label.to_edge(RIGHT, buff=1).shift(UP * 2)

        timer = DecimalNumber(0, num_decimal_places=1, font_size=28, color=RED)
        timer.next_to(timer_label, RIGHT, buff=0.2)
        timer_unit = Text("時間", font_size=20)
        timer_unit.next_to(timer, RIGHT, buff=0.1)

        self.play(Write(timer_label), Write(timer), Write(timer_unit))

        # 計算を一行ずつ書く（時間がかかる演出）
        for i, eq in enumerate(equations):
            self.play(
                Write(eq),
                timer.animate.set_value((i + 1) * 0.5),
                run_time=0.8,
            )

        # 答えを出す
        answer_box = VGroup(
            Rectangle(width=3, height=1.5, color=GREEN, fill_opacity=0.2),
            Text("予測結果", font_size=24, color=GREEN),
        )
        answer_box.shift(RIGHT * 4)

        arrow = Arrow(equations.get_right(), answer_box.get_left(), color=WHITE, buff=0.3)

        self.play(Create(arrow))
        self.play(FadeIn(answer_box), timer.animate.set_value(3.0))
        self.wait(0.5)

        # 強調テキスト
        emphasis = VGroup(
            Text("毎回ゼロから計算", font_size=28, color=RED),
            Text("膨大な時間がかかる", font_size=24),
        ).arrange(DOWN, buff=0.2)
        emphasis.to_edge(DOWN, buff=0.8)

        self.play(Write(emphasis))
        self.wait(1.5)

        # クリーンアップ
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_ai_method(self):
        """AIモデル：過去問で傾向を掴む"""
        # セクションタイトル
        section_title = Text("AIモデル", font_size=36, color=GREEN)
        section_title.to_edge(UP)
        self.play(Write(section_title))

        # サブタイトル
        subtitle = Text("「過去問で傾向を掴む」", font_size=28, color=GRAY)
        subtitle.next_to(section_title, DOWN, buff=0.3)
        self.play(Write(subtitle))

        # フェーズ1: 学習フェーズ
        phase1_label = Text("【学習フェーズ】過去問をたくさん解く", font_size=24, color=BLUE)
        phase1_label.shift(UP * 1.5)
        self.play(Write(phase1_label))

        # 過去問の山を表示
        past_exams = VGroup()
        colors = [YELLOW, ORANGE, RED, PINK, PURPLE, BLUE, TEAL, GREEN]
        for i in range(8):
            exam = self.create_exam_paper(f"過去問{i+1}", color=colors[i % len(colors)], scale=0.6)
            exam.move_to(LEFT * 3 + RIGHT * i * 0.3 + UP * (i % 3) * 0.15)
            past_exams.add(exam)

        # 過去問をスタック表示
        past_exams.arrange_in_grid(rows=2, cols=4, buff=0.1)
        past_exams.shift(LEFT * 2.5 + DOWN * 0.5)

        self.play(LaggedStart(*[FadeIn(e, scale=0.8) for e in past_exams], lag_ratio=0.1))

        # AIモデルのボックス
        ai_box = VGroup(
            RoundedRectangle(
                width=2.5, height=1.8, corner_radius=0.2, color=GREEN, fill_opacity=0.3
            ),
            Text("AI", font_size=32, color=GREEN).shift(UP * 0.2),
            Text("パターン学習", font_size=18, color=WHITE).shift(DOWN * 0.3),
        )
        ai_box.move_to(ORIGIN + DOWN * 0.5)

        # 矢印（過去問 → AI）
        arrow_learn = Arrow(past_exams.get_right(), ai_box.get_left(), color=BLUE, buff=0.2)

        self.play(Create(arrow_learn))
        self.play(FadeIn(ai_box))

        # 学習中のアニメーション（パルス効果）
        for _ in range(3):
            self.play(
                ai_box[0].animate.set_fill(GREEN, opacity=0.6),
                run_time=0.3,
            )
            self.play(
                ai_box[0].animate.set_fill(GREEN, opacity=0.3),
                run_time=0.3,
            )

        # 「傾向」を獲得
        pattern_text = Text("傾向を獲得！", font_size=24, color=YELLOW)
        pattern_text.next_to(ai_box, DOWN, buff=0.3)
        self.play(FadeIn(pattern_text, scale=1.2))
        self.wait(1)

        # フェーズ1をクリーンアップ
        self.play(
            FadeOut(phase1_label),
            FadeOut(past_exams),
            FadeOut(arrow_learn),
            FadeOut(pattern_text),
            ai_box.animate.shift(LEFT * 3),
        )

        # フェーズ2: 予測フェーズ
        phase2_label = Text("【予測フェーズ】本番ではサッと回答", font_size=24, color=GREEN)
        phase2_label.shift(UP * 1.5)
        self.play(Write(phase2_label))

        # 新しい問題
        new_problem = self.create_exam_paper("本番", color=ORANGE, scale=0.8)
        new_problem.move_to(LEFT * 5.5 + DOWN * 0.5)
        self.play(FadeIn(new_problem))

        # 入力矢印
        arrow_input = Arrow(new_problem.get_right(), ai_box.get_left(), color=WHITE, buff=0.2)

        # 出力（一瞬で回答）
        answer = VGroup(
            RoundedRectangle(width=2, height=1.2, corner_radius=0.1, color=GREEN, fill_opacity=0.3),
            Text("予測結果", font_size=22, color=GREEN),
        )
        answer.move_to(RIGHT * 2 + DOWN * 0.5)

        arrow_output = Arrow(ai_box.get_right(), answer.get_left(), color=WHITE, buff=0.2)

        # タイマー
        timer_label = Text("経過時間:", font_size=20)
        timer_label.to_edge(RIGHT, buff=1).shift(UP * 2)
        timer = DecimalNumber(0, num_decimal_places=1, font_size=28, color=GREEN)
        timer.next_to(timer_label, RIGHT, buff=0.2)
        timer_unit = Text("秒", font_size=20)
        timer_unit.next_to(timer, RIGHT, buff=0.1)

        self.play(Write(timer_label), Write(timer), Write(timer_unit))

        # 一瞬で回答！
        self.play(Create(arrow_input), run_time=0.3)

        # 閃光演出
        flash = Circle(radius=0.1, color=WHITE, fill_opacity=1)
        flash.move_to(ai_box.get_center())

        self.play(
            flash.animate.scale(15).set_opacity(0),
            Create(arrow_output),
            FadeIn(answer),
            timer.animate.set_value(0.1),
            run_time=0.5,
        )

        # 「一瞬！」のテキスト
        instant_text = Text("一瞬！", font_size=48, color=GREEN)
        instant_text.next_to(ai_box, UP, buff=0.3)
        self.play(FadeIn(instant_text, scale=1.5), run_time=0.3)
        self.wait(1)

        # 強調テキスト
        emphasis = VGroup(
            Text("パターンを当てはめるだけ", font_size=28, color=GREEN),
            Text("計算量が劇的に少ない", font_size=24),
        ).arrange(DOWN, buff=0.2)
        emphasis.to_edge(DOWN, buff=0.8)

        self.play(Write(emphasis))
        self.wait(1.5)

        # クリーンアップ
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_comparison(self):
        """比較まとめ"""
        title = Text("比較まとめ", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))

        # 左側: 従来の方法
        traditional_box = VGroup(
            RoundedRectangle(
                width=5, height=4, corner_radius=0.2, color=RED, fill_opacity=0.1
            ),
            Text("従来の方法", font_size=28, color=RED).shift(UP * 1.5),
            VGroup(
                Text("• 毎回ゼロから計算", font_size=22),
                Text("• 物理方程式を数値計算", font_size=22),
                Text("• 一歩一歩積み重ねる", font_size=22),
            ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).shift(DOWN * 0.3),
        )
        traditional_box.move_to(LEFT * 3)

        # 比喩テキスト（従来）
        metaphor_trad = Text("「毎回テストを解く」", font_size=20, color=GRAY)
        metaphor_trad.next_to(traditional_box, DOWN, buff=0.2)

        # 右側: AIモデル
        ai_box = VGroup(
            RoundedRectangle(
                width=5, height=4, corner_radius=0.2, color=GREEN, fill_opacity=0.1
            ),
            Text("AIモデル", font_size=28, color=GREEN).shift(UP * 1.5),
            VGroup(
                Text("• 過去データで学習済み", font_size=22),
                Text("• パターンを当てはめる", font_size=22),
                Text("• 傾向に基づき即回答", font_size=22),
            ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).shift(DOWN * 0.3),
        )
        ai_box.move_to(RIGHT * 3)

        # 比喩テキスト（AI）
        metaphor_ai = Text("「過去問で傾向を掴む」", font_size=20, color=GRAY)
        metaphor_ai.next_to(ai_box, DOWN, buff=0.2)

        # アニメーション
        self.play(FadeIn(traditional_box), Write(metaphor_trad))
        self.wait(0.5)
        self.play(FadeIn(ai_box), Write(metaphor_ai))
        self.wait(1)

        # VS
        vs_text = Text("VS", font_size=36, color=YELLOW)
        vs_text.move_to(ORIGIN + UP * 0.5)
        self.play(Write(vs_text))

        # 時間比較のバー
        time_compare = VGroup(
            VGroup(
                Text("計算時間", font_size=20),
                Rectangle(width=4, height=0.4, color=RED, fill_opacity=0.7),
                Text("数時間", font_size=18),
            ).arrange(DOWN, buff=0.1),
            VGroup(
                Text("計算時間", font_size=20),
                Rectangle(width=0.3, height=0.4, color=GREEN, fill_opacity=0.7),
                Text("数秒", font_size=18),
            ).arrange(DOWN, buff=0.1),
        )
        time_compare[0].move_to(LEFT * 3 + DOWN * 2.5)
        time_compare[1].move_to(RIGHT * 3 + DOWN * 2.5)

        self.play(FadeIn(time_compare))
        self.wait(1.5)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # 最終メッセージ
        final = VGroup(
            Text("AIモデルは", font_size=32),
            Text("「学習」という下準備をしておくことで", font_size=28),
            Text("本番では一瞬で答えを出せる", font_size=36, color=GREEN),
        ).arrange(DOWN, buff=0.4)

        self.play(Write(final[0]))
        self.play(Write(final[1]))
        self.play(Write(final[2]))
        self.wait(2)
        self.play(FadeOut(final))


class AIPatternMatchingShort(Scene):
    """AIの過去問比喩（短縮版）"""

    def construct(self):
        title = Text("なぜAIは速い？", font_size=44)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.scale(0.7).to_edge(UP))

        # 2列で比較
        left_title = Text("従来の方法", font_size=28, color=RED)
        right_title = Text("AIモデル", font_size=28, color=GREEN)

        left_title.move_to(LEFT * 3 + UP * 1.5)
        right_title.move_to(RIGHT * 3 + UP * 1.5)

        self.play(Write(left_title), Write(right_title))

        # 従来: テスト用紙と計算
        trad_icon = VGroup(
            Rectangle(width=1.5, height=2, color=WHITE, fill_opacity=0.1),
            Text("問題", font_size=16).shift(UP * 0.6),
            MathTex(r"\partial u/\partial t", font_size=18).shift(DOWN * 0.2),
        )
        trad_icon.move_to(LEFT * 3)

        # AI: 過去問の山とパターン
        ai_icon = VGroup(
            VGroup(
                *[
                    Rectangle(width=0.8, height=1, color=color, fill_opacity=0.3).shift(
                        RIGHT * i * 0.15 + UP * i * 0.05
                    )
                    for i, color in enumerate([YELLOW, ORANGE, RED, PINK])
                ]
            ),
            Text("過去問", font_size=14).shift(DOWN * 0.8),
        )
        ai_icon.move_to(RIGHT * 3)

        self.play(FadeIn(trad_icon), FadeIn(ai_icon))
        self.wait(0.5)

        # 矢印と結果
        trad_arrow = Arrow(LEFT * 3 + DOWN * 1.3, LEFT * 3 + DOWN * 2.3, color=RED)
        ai_arrow = Arrow(RIGHT * 3 + DOWN * 1.3, RIGHT * 3 + DOWN * 2.3, color=GREEN)

        trad_time = Text("数時間かけて計算", font_size=20, color=RED)
        trad_time.move_to(LEFT * 3 + DOWN * 2.8)

        ai_time = Text("一瞬で回答！", font_size=20, color=GREEN)
        ai_time.move_to(RIGHT * 3 + DOWN * 2.8)

        self.play(Create(trad_arrow), Create(ai_arrow))
        self.play(Write(trad_time), Write(ai_time))
        self.wait(1)

        # 強調
        box = SurroundingRectangle(ai_time, color=GREEN, buff=0.15)
        self.play(Create(box))

        # 結論
        conclusion = Text(
            "過去問で傾向を掴めば、本番は楽勝",
            font_size=28,
            color=WHITE,
        )
        conclusion.to_edge(DOWN, buff=0.5)
        self.play(Write(conclusion))
        self.wait(2)


if __name__ == "__main__":
    # コマンドラインから実行する場合の例
    # manim -pql ai_pattern_matching_animation.py AIPatternMatching
    # manim -pql ai_pattern_matching_animation.py AIPatternMatchingShort
    pass
