"""
プリミティブ方程式の解説アニメーション

大気の運動を記述する基本方程式（プリミティブ方程式）を可視化します。
気象現象がどのような微分方程式で記述されるかを説明します。

使用方法:
    manim -pql primitive_equations_animation.py PrimitiveEquations
    manim -pqh primitive_equations_animation.py PrimitiveEquations  # 高画質
"""

from manim import *


class PrimitiveEquations(Scene):
    """プリミティブ方程式の表示アニメーション"""

    def construct(self):
        # タイトル
        self.show_title()

        # 気象現象の説明
        self.show_phenomena()

        # プリミティブ方程式の表示
        self.show_equations()

        # まとめ
        self.show_summary()

    def show_title(self):
        """タイトルを表示"""
        title = Text("気象を記述する微分方程式", font_size=48)
        subtitle = Text("プリミティブ方程式", font_size=36, color=BLUE)
        subtitle.next_to(title, DOWN)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

    def show_phenomena(self):
        """気象現象と対応する物理を説明"""
        title = Text("大気中で起きる現象", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))

        # 現象とそれを記述する物理
        phenomena = [
            ("空気の流れ", "→", "流体力学"),
            ("温度変化", "→", "熱力学"),
            ("水蒸気・雲・雨", "→", "相変化・輸送"),
            ("気圧の変化", "→", "状態方程式"),
        ]

        rows = VGroup()
        for phenomenon, arrow, physics in phenomena:
            row = VGroup(
                Text(phenomenon, font_size=32, color=YELLOW),
                Text(arrow, font_size=32),
                Text(physics, font_size=32, color=GREEN),
            ).arrange(RIGHT, buff=0.5)
            rows.add(row)

        rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        rows.next_to(title, DOWN, buff=0.8)

        for row in rows:
            self.play(Write(row), run_time=0.8)
            self.wait(0.3)

        self.wait(1)

        # まとめテキスト
        summary = Text(
            "これらを数学的に記述したのが\nプリミティブ方程式",
            font_size=32,
            line_spacing=1.5,
        )
        summary.next_to(rows, DOWN, buff=0.8)
        self.play(Write(summary))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_equations(self):
        """プリミティブ方程式を順番に表示（2列構成）"""
        title = Text("プリミティブ方程式", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))

        # 1列目: 運動方程式と静力学平衡
        left_equations = [
            (
                "運動方程式（東西方向）",
                r"\frac{\partial u}{\partial t} + \mathbf{v} \cdot \nabla u - fv = -\frac{1}{\rho}\frac{\partial p}{\partial x}",
            ),
            (
                "運動方程式（南北方向）",
                r"\frac{\partial v}{\partial t} + \mathbf{v} \cdot \nabla v + fu = -\frac{1}{\rho}\frac{\partial p}{\partial y}",
            ),
            (
                "静力学平衡（鉛直方向）",
                r"\frac{\partial p}{\partial z} = -\rho g",
            ),
        ]

        # 2列目: 連続の式と熱力学方程式
        right_equations = [
            (
                "連続の式（質量保存）",
                r"\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \mathbf{v}) = 0",
            ),
            (
                "熱力学方程式",
                r"\frac{\partial T}{\partial t} + \mathbf{v} \cdot \nabla T = \frac{Q}{c_p}",
            ),
        ]

        def create_eq_group(name, equation):
            """方程式グループを作成"""
            name_text = Text(name, font_size=24, color=YELLOW)
            eq_math = MathTex(equation, font_size=28)
            return VGroup(name_text, eq_math).arrange(DOWN, buff=0.2, aligned_edge=LEFT)

        # 左列を作成
        left_column = VGroup(*[create_eq_group(n, e) for n, e in left_equations])
        left_column.arrange(DOWN, buff=0.5, aligned_edge=LEFT)

        # 右列を作成
        right_column = VGroup(*[create_eq_group(n, e) for n, e in right_equations])
        right_column.arrange(DOWN, buff=0.5, aligned_edge=LEFT)

        # 2列を横に配置
        columns = VGroup(left_column, right_column).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        columns.next_to(title, DOWN, buff=0.5)

        # 左列のアニメーション
        for eq_group in left_column:
            self.play(Write(eq_group), run_time=1.0)
            self.wait(0.3)

        # 右列のアニメーション
        for eq_group in right_column:
            self.play(Write(eq_group), run_time=1.0)
            self.wait(0.3)

        self.wait(2)

        # 変数の説明を追加
        var_explain = VGroup(
            Text("u, v: 風速", font_size=18),
            Text("p: 気圧", font_size=18),
            Text("ρ: 空気密度", font_size=18),
            Text("T: 温度", font_size=18),
            Text("f: コリオリパラメータ", font_size=18),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        var_explain.to_edge(RIGHT, buff=0.3)
        var_explain.set_color(GRAY)

        self.play(FadeIn(var_explain))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_summary(self):
        """まとめを表示"""
        # ポイント
        point1 = Text(
            "これらの方程式は互いに結合している",
            font_size=32,
        )
        point2 = Text(
            "風が変われば温度が変わり、",
            font_size=28,
            color=GRAY,
        )
        point3 = Text(
            "温度が変われば気圧が変わり、",
            font_size=28,
            color=GRAY,
        )
        point4 = Text(
            "気圧が変われば風が変わる...",
            font_size=28,
            color=GRAY,
        )

        points = VGroup(point1, point2, point3, point4).arrange(DOWN, buff=0.4)
        points.move_to(ORIGIN)

        self.play(Write(point1))
        self.wait(0.5)

        for point in [point2, point3, point4]:
            self.play(Write(point), run_time=0.8)
            self.wait(0.3)

        self.wait(1)

        # 結論
        conclusion = Text(
            "→ 複雑に絡み合った非線形連立微分方程式",
            font_size=32,
            color=RED,
        )
        conclusion.next_to(points, DOWN, buff=0.8)
        self.play(Write(conclusion))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # 最後のメッセージ
        final = Text("紙と鉛筆では解けない", font_size=44, color=BLUE)
        self.play(Write(final))
        self.wait(2)
        self.play(FadeOut(final))


class EquationsSimplified(Scene):
    """簡略化された方程式表示（短縮版）"""

    def construct(self):
        title = Text("気象の基本方程式", font_size=44)
        title.to_edge(UP)
        self.play(Write(title))

        # 簡略化した主要方程式
        equations = VGroup(
            VGroup(
                Text("運動方程式", font_size=28, color=YELLOW),
                MathTex(
                    r"\frac{D\mathbf{v}}{Dt} = -\frac{1}{\rho}\nabla p - f\mathbf{k} \times \mathbf{v} + \mathbf{g}",
                    font_size=36,
                ),
            ).arrange(DOWN, buff=0.2),
            VGroup(
                Text("連続の式", font_size=28, color=YELLOW),
                MathTex(r"\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \mathbf{v}) = 0", font_size=36),
            ).arrange(DOWN, buff=0.2),
            VGroup(
                Text("熱力学方程式", font_size=28, color=YELLOW),
                MathTex(r"\frac{DT}{Dt} = \frac{Q}{c_p}", font_size=36),
            ).arrange(DOWN, buff=0.2),
            VGroup(
                Text("状態方程式", font_size=28, color=YELLOW),
                MathTex(r"p = \rho R T", font_size=36),
            ).arrange(DOWN, buff=0.2),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)

        equations.next_to(title, DOWN, buff=0.6)
        equations.to_edge(LEFT, buff=1)

        for eq in equations:
            self.play(Write(eq), run_time=1)
            self.wait(0.3)

        self.wait(2)

        # 説明
        explain = Text(
            "これらの方程式で大気の運動を記述",
            font_size=30,
            color=GREEN,
        )
        explain.to_edge(DOWN, buff=1)
        self.play(Write(explain))
        self.wait(2)


if __name__ == "__main__":
    # コマンドラインから実行する場合の例
    # manim -pql primitive_equations_animation.py PrimitiveEquations
    pass
