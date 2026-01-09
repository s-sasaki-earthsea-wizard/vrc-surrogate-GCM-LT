"""
ルンゲ・クッタ法の解説アニメーション

df/dx = exp(x) という微分方程式を数値的に解く様子を可視化します。
解析解は f(x) = exp(x) + C で、初期条件 f(0) = 1 から C = 0 となり、
f(x) = exp(x) が正確な解となります。

使用方法:
    manim -pql runge_kutta_animation.py RungeKuttaExplanation
    manim -pqh runge_kutta_animation.py RungeKuttaExplanation  # 高画質
"""

from manim import *
import numpy as np


class RungeKuttaExplanation(Scene):
    """ルンゲ・クッタ法による数値計算の可視化"""

    def construct(self):
        # タイトル
        self.show_title()

        # 微分方程式の説明
        self.show_equation()

        # 座標系とアニメーション
        self.show_numerical_solution()

        # 刻み幅の比較
        self.show_step_size_comparison()

    def show_title(self):
        """タイトルを表示"""
        title = Text("数値計算のイメージ", font_size=48)
        subtitle = Text("ルンゲ・クッタ法", font_size=36, color=BLUE)
        subtitle.next_to(title, DOWN)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

    def show_equation(self):
        """微分方程式を説明"""
        # 微分方程式
        eq_text = Text("微分方程式:", font_size=32)
        equation = MathTex(r"\frac{df}{dx} = e^x", font_size=48)
        eq_group = VGroup(eq_text, equation).arrange(RIGHT, buff=0.5)
        eq_group.to_edge(UP)

        self.play(Write(eq_text), Write(equation))
        self.wait(0.5)

        # 解析解
        solution_text = Text("解析解:", font_size=32)
        solution = MathTex(r"f(x) = e^x + C", font_size=48)
        sol_group = VGroup(solution_text, solution).arrange(RIGHT, buff=0.5)
        sol_group.next_to(eq_group, DOWN, buff=0.5)

        self.play(Write(solution_text), Write(solution))
        self.wait(0.5)

        # 初期条件
        initial = MathTex(r"f(0) = 1 \Rightarrow C = 0", font_size=36, color=YELLOW)
        initial.next_to(sol_group, DOWN, buff=0.3)

        self.play(Write(initial))
        self.wait(1)

        # 説明テキスト
        explain = Text(
            "複雑な方程式では解析解が求められない\n→ 数値計算で近似解を求める",
            font_size=28,
            line_spacing=1.5,
        )
        explain.next_to(initial, DOWN, buff=0.5)

        self.play(Write(explain))
        self.wait(2)

        self.play(
            FadeOut(eq_text),
            FadeOut(equation),
            FadeOut(solution_text),
            FadeOut(solution),
            FadeOut(initial),
            FadeOut(explain),
        )

    def show_numerical_solution(self):
        """数値解法のアニメーション"""
        # 座標系を作成
        axes = Axes(
            x_range=[0, 2.5, 0.5],
            y_range=[0, 8, 2],
            x_length=8,
            y_length=5,
            axis_config={"include_numbers": True, "font_size": 24},
            tips=False,
        )
        axes.to_edge(DOWN, buff=0.5)

        x_label = axes.get_x_axis_label("x", edge=RIGHT, direction=DOWN)
        y_label = axes.get_y_axis_label("f(x)", edge=UP, direction=LEFT)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # 解析解のグラフ（薄く表示）
        true_graph = axes.plot(lambda x: np.exp(x), x_range=[0, 2], color=GRAY)
        true_label = Text("解析解 f(x) = eˣ", font_size=20, color=GRAY)
        true_label.next_to(axes, UP, buff=0.3).to_edge(RIGHT)

        self.play(Create(true_graph), Write(true_label))

        # 数値計算のパラメータ
        h = 0.4  # 刻み幅（見やすくするため大きめ）
        x_vals = [0]
        f_vals = [1.0]  # 初期条件 f(0) = 1

        # 初期点をプロット
        current_dot = Dot(axes.c2p(0, 1), color=RED, radius=0.1)
        current_label = MathTex(r"(0, 1)", font_size=24, color=RED)
        current_label.next_to(current_dot, UP + LEFT, buff=0.1)

        self.play(Create(current_dot), Write(current_label))
        self.wait(0.5)

        # 説明テキスト
        step_text = Text("ステップ幅 h = 0.4", font_size=28, color=YELLOW)
        step_text.to_edge(UP)
        self.play(Write(step_text))

        # ルンゲ・クッタ法（4次）でステップを進める
        dots = [current_dot]
        lines = []

        for i in range(5):
            x = x_vals[-1]
            f = f_vals[-1]

            # 4次ルンゲ・クッタ法
            k1 = np.exp(x)
            k2 = np.exp(x + h / 2)
            k3 = np.exp(x + h / 2)
            k4 = np.exp(x + h)
            f_new = f + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
            x_new = x + h

            x_vals.append(x_new)
            f_vals.append(f_new)

            # 傾きを表す矢印
            slope = np.exp(x)
            arrow_end_x = x + 0.3
            arrow_end_y = f + slope * 0.3

            arrow = Arrow(
                axes.c2p(x, f),
                axes.c2p(arrow_end_x, arrow_end_y),
                color=ORANGE,
                buff=0,
                stroke_width=3,
            )

            slope_label = VGroup(
                Text("傾き = ", font_size=20, color=ORANGE),
                MathTex(rf"e^{{{x:.1f}}} \approx {slope:.2f}", font_size=24, color=ORANGE),
            ).arrange(RIGHT, buff=0.1)
            slope_label.next_to(arrow, RIGHT, buff=0.1)

            self.play(Create(arrow), Write(slope_label), run_time=0.5)
            self.wait(0.3)

            # 次の点へ線を引く
            line = Line(
                axes.c2p(x, f), axes.c2p(x_new, f_new), color=BLUE, stroke_width=2
            )

            new_dot = Dot(axes.c2p(x_new, f_new), color=RED, radius=0.08)

            self.play(
                Create(line), Create(new_dot), FadeOut(arrow), FadeOut(slope_label)
            )

            dots.append(new_dot)
            lines.append(line)

            # 新しい点の座標を表示
            coord_label = MathTex(
                rf"({x_new:.1f}, {f_new:.2f})", font_size=20, color=RED
            )
            coord_label.next_to(new_dot, UP + RIGHT, buff=0.05)
            self.play(Write(coord_label), run_time=0.3)

            if i < 4:
                self.play(FadeOut(coord_label), run_time=0.2)

        self.wait(1)

        # 結果の説明
        result_text = Text("数値解が解析解に近い値を示している", font_size=28, color=GREEN)
        result_text.to_edge(UP)
        self.play(Transform(step_text, result_text))
        self.wait(2)

        # クリア
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
        )

    def show_step_size_comparison(self):
        """刻み幅による計算量の違いを説明"""
        title = Text("刻み幅と計算量", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))

        # 比較表
        data = [
            ("0.1", "100回", "高"),
            ("0.01", "1,000回", "より高"),
            ("0.001", "10,000回", "さらに高"),
        ]

        headers = ["刻み幅", "計算回数 (0→10)", "精度"]
        header_group = VGroup(
            *[Text(h, font_size=28, color=YELLOW) for h in headers]
        ).arrange(RIGHT, buff=1.5)
        header_group.next_to(title, DOWN, buff=0.8)

        self.play(Write(header_group))

        rows = []
        for i, (step, count, accuracy) in enumerate(data):
            row = VGroup(
                Text(step, font_size=28),
                Text(count, font_size=28),
                Text(accuracy, font_size=28),
            ).arrange(RIGHT, buff=1.5)
            row.next_to(header_group, DOWN, buff=0.5 + i * 0.8)
            rows.append(row)

        for row in rows:
            self.play(Write(row), run_time=0.5)
            self.wait(0.3)

        self.wait(1)

        # 結論
        conclusion = Text(
            "精度を上げると計算量が爆発的に増加する",
            font_size=32,
            color=RED,
        )
        conclusion.next_to(rows[-1], DOWN, buff=1)
        self.play(Write(conclusion))
        self.wait(1)

        # 地球規模の話
        earth_text = Text(
            "地球全体 × 高度方向 × 時間方向\n→ 天文学的な計算量に",
            font_size=28,
            line_spacing=1.5,
        )
        earth_text.next_to(conclusion, DOWN, buff=0.5)
        self.play(Write(earth_text))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # 最後のメッセージ
        final = Text("だからスーパーコンピュータが必要", font_size=40, color=BLUE)
        self.play(Write(final))
        self.wait(2)
        self.play(FadeOut(final))


class StepByStepRK4(Scene):
    """より詳細なルンゲ・クッタ法のステップ解説"""

    def construct(self):
        title = Text("ルンゲ・クッタ法（4次）の1ステップ", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # 数式
        equations = VGroup(
            MathTex(r"k_1 = f(x_n, y_n)", font_size=32),
            MathTex(r"k_2 = f(x_n + \frac{h}{2}, y_n + \frac{h}{2}k_1)", font_size=32),
            MathTex(r"k_3 = f(x_n + \frac{h}{2}, y_n + \frac{h}{2}k_2)", font_size=32),
            MathTex(r"k_4 = f(x_n + h, y_n + hk_3)", font_size=32),
            MathTex(
                r"y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)", font_size=32
            ),
        ).arrange(DOWN, buff=0.4)
        equations.next_to(title, DOWN, buff=0.5)

        for eq in equations:
            self.play(Write(eq), run_time=0.8)

        self.wait(1)

        # 説明
        explain = Text(
            "複数の傾きを計算して平均を取ることで\nより正確な近似が得られる",
            font_size=28,
            line_spacing=1.5,
            color=YELLOW,
        )
        explain.next_to(equations, DOWN, buff=0.5)
        self.play(Write(explain))
        self.wait(3)


if __name__ == "__main__":
    # コマンドラインから実行する場合の例
    # manim -pql runge_kutta_animation.py RungeKuttaExplanation
    pass
