"""
計算量爆発の解説アニメーション

空間3成分+時間1成分の複雑な微分方程式（プリミティブ方程式など）を
数値的に解く際に、計算量が爆発的に増加することを可視化します。

使用方法:
    manim -pql computational_explosion_animation.py ComputationalExplosion
    manim -pqh computational_explosion_animation.py ComputationalExplosion  # 高画質
"""

from manim import *
import numpy as np


class ComputationalExplosion(Scene):
    """計算量の爆発的増加を可視化するアニメーション"""

    def construct(self):
        # タイトル
        self.show_title()

        # 1次元の例
        self.show_1d_case()

        # 次元拡張による計算量増加
        self.show_dimension_explosion()

        # 地球規模の計算
        self.show_earth_scale()

        # まとめ
        self.show_summary()

    def show_title(self):
        """タイトルを表示"""
        title = Text("計算量の爆発", font_size=48)
        subtitle = Text("次元が増えると何が起きるか", font_size=32, color=BLUE)
        subtitle.next_to(title, DOWN)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

    def show_1d_case(self):
        """1次元の場合を表示"""
        title = Text("1次元の場合", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))

        # 1次元のグリッドを表示（水平線上の点）
        line = Line(LEFT * 5, RIGHT * 5, color=WHITE)
        line.shift(UP * 0.5)

        # 10個の点を配置
        n_points_1d = 10
        dots = VGroup()
        for i in range(n_points_1d + 1):
            x = -5 + i * 10 / n_points_1d
            dot = Dot(point=[x, 0.5, 0], color=YELLOW, radius=0.08)
            dots.add(dot)

        self.play(Create(line))
        self.play(LaggedStart(*[Create(d) for d in dots], lag_ratio=0.1))

        # 説明テキスト
        explain = Text(f"空間を{n_points_1d}分割 → {n_points_1d + 1}個の計算点", font_size=28)
        explain.next_to(line, DOWN, buff=0.8)
        self.play(Write(explain))
        self.wait(1)

        # 計算回数の強調
        calc_text = VGroup(
            Text("時間を100ステップ進めると:", font_size=28),
            MathTex(r"11 \times 100 = 1,100", font_size=36, color=GREEN),
            Text("回の計算", font_size=28),
        ).arrange(RIGHT, buff=0.3)
        calc_text.next_to(explain, DOWN, buff=0.5)

        self.play(Write(calc_text))
        self.wait(1)

        conclusion_1d = Text("これくらいなら一瞬で終わる", font_size=28, color=GRAY)
        conclusion_1d.next_to(calc_text, DOWN, buff=0.5)
        self.play(Write(conclusion_1d))
        self.wait(1)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_dimension_explosion(self):
        """次元拡張による計算量の爆発を視覚化"""
        title = Text("次元を増やすと...", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))

        # 1次元 → 2次元 → 3次元の視覚的比較
        # 1次元: 線
        line_1d = Line(LEFT * 1.5, RIGHT * 1.5, color=YELLOW, stroke_width=4)
        label_1d = Text("1次元", font_size=24)
        dots_1d = VGroup(*[
            Dot(point=[LEFT * 1.5 + RIGHT * 0.3 * i], color=YELLOW, radius=0.05)
            for i in range(11)
        ])
        group_1d = VGroup(line_1d, dots_1d, label_1d)
        label_1d.next_to(line_1d, DOWN, buff=0.3)

        # 2次元: 面
        square_2d = Square(side_length=2.5, color=GREEN, fill_opacity=0.3)
        label_2d = Text("2次元", font_size=24)
        # グリッド線
        grid_2d = VGroup()
        for i in range(6):
            h_line = Line(
                square_2d.get_corner(UL) + DOWN * i * 0.5,
                square_2d.get_corner(UR) + DOWN * i * 0.5,
                color=GREEN,
                stroke_width=1,
            )
            v_line = Line(
                square_2d.get_corner(UL) + RIGHT * i * 0.5,
                square_2d.get_corner(DL) + RIGHT * i * 0.5,
                color=GREEN,
                stroke_width=1,
            )
            grid_2d.add(h_line, v_line)
        group_2d = VGroup(square_2d, grid_2d, label_2d)
        label_2d.next_to(square_2d, DOWN, buff=0.3)

        # 3次元: 小さな立方体を並べた大きな立方体
        cube_grid_3d = VGroup()
        cube_size = 0.5
        n_cubes = 4  # 4x4x4のグリッド
        offset = (n_cubes - 1) * cube_size / 2
        for i in range(n_cubes):
            for j in range(n_cubes):
                for k in range(n_cubes):
                    small_cube = Cube(side_length=cube_size * 0.9, fill_opacity=0.15, stroke_width=1)
                    small_cube.set_color(BLUE)
                    # 3D配置（奥行きは斜め上方向で表現）
                    x = (i - offset / cube_size) * cube_size
                    y = (j - offset / cube_size) * cube_size
                    z_offset = (k - offset / cube_size) * cube_size * 0.5  # 奥行き方向
                    small_cube.move_to([x + z_offset * 0.7, y + z_offset * 0.7, 0])
                    cube_grid_3d.add(small_cube)
        label_3d = Text("3次元", font_size=24)
        group_3d = VGroup(cube_grid_3d, label_3d)
        label_3d.next_to(cube_grid_3d, DOWN, buff=0.5)

        # 配置
        group_1d.move_to(LEFT * 4.5)
        group_2d.move_to(ORIGIN)
        group_3d.move_to(RIGHT * 4.5)

        # 計算量のテキスト
        calc_1d = MathTex(r"n", font_size=32, color=YELLOW)
        calc_2d = MathTex(r"n^2", font_size=32, color=GREEN)
        calc_3d = MathTex(r"n^3", font_size=32, color=BLUE)

        calc_1d.next_to(group_1d, UP, buff=0.3)
        calc_2d.next_to(group_2d, UP, buff=0.3)
        calc_3d.next_to(group_3d, UP, buff=0.3)

        # アニメーション
        self.play(Create(line_1d), LaggedStart(*[Create(d) for d in dots_1d], lag_ratio=0.05))
        self.play(Write(label_1d), Write(calc_1d))
        self.wait(0.5)

        self.play(Create(square_2d), Create(grid_2d))
        self.play(Write(label_2d), Write(calc_2d))
        self.wait(0.5)

        # 小さな立方体を順番に表示（奥から手前へ）
        self.play(LaggedStart(*[Create(c) for c in cube_grid_3d], lag_ratio=0.02), run_time=1.5)
        self.play(Write(label_3d), Write(calc_3d))
        self.wait(1)

        # 具体的な数値で比較
        self.play(
            group_1d.animate.scale(0.7).to_edge(LEFT, buff=0.5),
            group_2d.animate.scale(0.7).move_to(LEFT * 2),
            group_3d.animate.scale(0.7).move_to(RIGHT * 1),
            calc_1d.animate.scale(0.8).next_to(group_1d, UP, buff=0.2),
            calc_2d.animate.scale(0.8).next_to(group_2d, UP, buff=0.2),
            calc_3d.animate.scale(0.8).next_to(group_3d, UP, buff=0.2),
        )

        # 具体例: n = 100 の場合
        example_title = Text("各方向を100分割すると...", font_size=28)
        example_title.to_edge(RIGHT, buff=0.3).shift(UP * 1.5)
        self.play(Write(example_title))

        numbers = VGroup(
            VGroup(
                Text("1次元:", font_size=24, color=YELLOW),
                Text("100点", font_size=24),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("2次元:", font_size=24, color=GREEN),
                Text("10,000点", font_size=24),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("3次元:", font_size=24, color=BLUE),
                Text("1,000,000点", font_size=24),
            ).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        numbers.next_to(example_title, DOWN, buff=0.5)

        for num in numbers:
            self.play(Write(num), run_time=0.6)
            self.wait(0.3)

        self.wait(1)

        # 強調: 100倍ではなく、100万倍に
        emphasis = Text(
            "次元が増えると\n指数関数的に増加！",
            font_size=28,
            color=RED,
            line_spacing=1.3,
        )
        emphasis.to_edge(DOWN, buff=0.8)
        self.play(Write(emphasis))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_earth_scale(self):
        """地球規模での計算を説明"""
        title = Text("地球規模のシミュレーション", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))

        # 地球の概念図（円）
        earth = Circle(radius=1.5, color=BLUE, fill_opacity=0.3)
        earth.shift(LEFT * 3.5)

        # グリッドを重ねる
        grid_lines = VGroup()
        for i in range(-3, 4):
            # 緯度線（楕円で表現）
            if abs(i) < 3:
                lat_line = Ellipse(
                    width=3 * np.sqrt(1 - (i / 3) ** 2),
                    height=0.3,
                    color=YELLOW,
                    stroke_width=1,
                )
                lat_line.shift(LEFT * 3.5 + UP * i * 0.5)
                grid_lines.add(lat_line)

        # 経度線（弧で近似）
        for angle in range(0, 180, 30):
            lon_line = Arc(
                radius=1.5,
                start_angle=PI / 2 + angle * DEGREES,
                angle=PI,
                color=YELLOW,
                stroke_width=1,
            )
            lon_line.shift(LEFT * 3.5)
            grid_lines.add(lon_line)

        self.play(Create(earth))
        self.play(Create(grid_lines))

        # 説明テキスト
        specs = VGroup(
            Text("25km四方のグリッド", font_size=26, color=YELLOW),
            Text("　→ 水平方向: 約100万点", font_size=26),
            Text("高度方向: 約50層", font_size=26, color=GREEN),
            Text("　→ 合計: 約5000万点", font_size=26),
            Text("時間ステップ: 数千〜数万回", font_size=26, color=ORANGE),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        specs.next_to(title, DOWN, buff=0.6)
        specs.to_edge(RIGHT, buff=1.0)

        for spec in specs:
            self.play(Write(spec), run_time=0.5)

        self.wait(1)

        # 計算量の計算
        calc_box = VGroup(
            Text("1回の予報に必要な計算:", font_size=28),
            Text("5000万点 × 10000ステップ", font_size=32),
            Text("= 5000億回", font_size=36, color=RED),
        ).arrange(DOWN, buff=0.3)
        calc_box.to_edge(DOWN, buff=0.8)

        self.play(Write(calc_box[0]))
        self.play(Write(calc_box[1]))
        self.play(Write(calc_box[2]))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_summary(self):
        """まとめを表示"""
        # 比較表
        title = Text("計算量の比較", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))

        # 表形式で比較
        comparison = VGroup(
            VGroup(
                Text("1次元", font_size=28, color=YELLOW),
                Text("×", font_size=28),
                Text("100ステップ", font_size=28),
                Text("=", font_size=28),
                Text("約1,000回", font_size=28),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("3次元", font_size=28, color=BLUE),
                Text("×", font_size=28),
                Text("100ステップ", font_size=28),
                Text("=", font_size=28),
                Text("約1億回", font_size=28),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("地球規模", font_size=28, color=RED),
                Text("×", font_size=28),
                Text("10,000ステップ", font_size=28),
                Text("=", font_size=28),
                Text("数千億回", font_size=28),
            ).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        comparison.next_to(title, DOWN, buff=0.8)

        for row in comparison:
            self.play(Write(row), run_time=0.8)
            self.wait(0.5)

        self.wait(1)

        # 矢印で増加を強調
        arrow1 = Arrow(
            comparison[0].get_right() + RIGHT * 0.3,
            comparison[1].get_right() + RIGHT * 0.3,
            color=ORANGE,
            stroke_width=3,
        )
        arrow2 = Arrow(
            comparison[1].get_right() + RIGHT * 0.3,
            comparison[2].get_right() + RIGHT * 0.3,
            color=ORANGE,
            stroke_width=3,
        )

        mult1 = Text("10万倍", font_size=20, color=ORANGE)
        mult1.next_to(arrow1, RIGHT, buff=0.1)
        mult2 = Text("数千倍", font_size=20, color=ORANGE)
        mult2.next_to(arrow2, RIGHT, buff=0.1)

        self.play(Create(arrow1), Write(mult1))
        self.play(Create(arrow2), Write(mult2))
        self.wait(1)

        # 結論
        conclusion = Text(
            "普通のパソコンでは計算できない！",
            font_size=36,
            color=RED,
        )
        conclusion.to_edge(DOWN, buff=1)
        self.play(Write(conclusion))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # 最後のメッセージ
        final = VGroup(
            Text("だから", font_size=36),
            Text("スーパーコンピュータが必要", font_size=44, color=BLUE),
        ).arrange(DOWN, buff=0.3)
        self.play(Write(final[0]))
        self.play(Write(final[1]))
        self.wait(2)
        self.play(FadeOut(final))


class DimensionComparison(Scene):
    """次元による計算量比較（短縮版）"""

    def construct(self):
        title = Text("次元と計算量", font_size=44)
        title.to_edge(UP)
        self.play(Write(title))

        # シンプルな比較
        data = [
            ("1次元 (線)", "n", "100", YELLOW),
            ("2次元 (面)", "n²", "10,000", GREEN),
            ("3次元 (立体)", "n³", "1,000,000", BLUE),
            ("3次元 + 時間", "n³ × t", "100,000,000+", RED),
        ]

        rows = VGroup()
        for dim, formula, value, color in data:
            row = VGroup(
                Text(dim, font_size=28, color=color),
                MathTex(formula, font_size=32),
                Text(f"n=100 → {value}点", font_size=24),
            ).arrange(RIGHT, buff=1.0)
            rows.add(row)

        rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        rows.next_to(title, DOWN, buff=0.8)

        for row in rows:
            self.play(Write(row), run_time=0.8)
            self.wait(0.3)

        self.wait(1)

        # 強調
        box = SurroundingRectangle(rows[-1], color=RED, buff=0.2)
        self.play(Create(box))

        explain = Text(
            "天気予報はここに該当",
            font_size=28,
            color=RED,
        )
        explain.next_to(box, RIGHT, buff=0.3)
        self.play(Write(explain))
        self.wait(2)


if __name__ == "__main__":
    # コマンドラインから実行する場合の例
    # manim -pql computational_explosion_animation.py ComputationalExplosion
    pass
