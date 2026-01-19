"""
機械学習の基礎を解説するアニメーション

「データから学習する」という機械学習の本質を、
線形回帰（最小二乗法）を使って視覚的に説明します。

ターゲット: 機械学習を知らない科学好きの高校生・大学生

使用方法:
    manim -pql ml_basics_animation.py MLBasics
    manim -pqh ml_basics_animation.py MLBasics  # 高画質
"""

from manim import *
import numpy as np


class MLBasics(Scene):
    """機械学習の基本的な仕組みを解説するアニメーション"""

    def construct(self):
        # タイトル
        self.show_title()

        # データの準備
        self.show_data()

        # 初期予測（でたらめな線）
        self.show_initial_prediction()

        # ズレ（損失）の可視化
        self.show_loss_visualization()

        # 学習プロセス（勾配降下法）
        self.show_learning_process()

        # 収束・完了
        self.show_convergence()

        # 一般化への橋渡し
        self.show_generalization()

    def show_title(self):
        """タイトルを表示"""
        title = Text("機械学習のしくみ", font_size=48)
        subtitle = Text("データから「パターン」を見つける", font_size=32, color=BLUE)
        subtitle.next_to(title, DOWN)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

    def show_data(self):
        """訓練データを表示"""
        # 座標軸を作成
        self.axes = Axes(
            x_range=[-0.5, 5.5, 1],
            y_range=[-0.5, 5.5, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_tip": True, "include_numbers": False},
        )
        self.axes.shift(LEFT * 1.5)

        axis_labels = VGroup(
            Text("入力 x", font_size=20).next_to(self.axes.x_axis, DOWN, buff=0.1),
            Text("出力 y", font_size=20).next_to(self.axes.y_axis, LEFT, buff=0.1),
        )

        self.play(Create(self.axes), Write(axis_labels))

        # 訓練データを生成（y = 0.7x + 0.5 + ノイズ）
        np.random.seed(42)
        self.x_data = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5])
        true_slope = 0.7
        true_intercept = 0.5
        noise = np.random.normal(0, 0.3, len(self.x_data))
        self.y_data = true_slope * self.x_data + true_intercept + noise

        # データ点を作成
        self.data_dots = VGroup()
        for x, y in zip(self.x_data, self.y_data):
            dot = Dot(
                self.axes.c2p(x, y),
                color=YELLOW,
                radius=0.1,
            )
            self.data_dots.add(dot)

        # データ点を順番に表示
        data_label = Text("訓練データ", font_size=28, color=YELLOW)
        data_label.to_edge(UP).shift(RIGHT * 3)

        self.play(Write(data_label))
        self.play(LaggedStart(*[Create(d) for d in self.data_dots], lag_ratio=0.15))
        self.wait(0.5)

        # 説明テキスト
        explain = VGroup(
            Text("これが「正解」のデータ", font_size=24),
            Text("入力 x から出力 y を予測したい", font_size=24),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        explain.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)

        self.play(Write(explain))
        self.wait(1.5)
        self.play(FadeOut(explain), FadeOut(data_label))

    def show_initial_prediction(self):
        """初期のでたらめな予測を表示"""
        # でたらめな直線（傾きと切片が全然違う）
        self.current_slope = -0.3  # 間違った傾き
        self.current_intercept = 4.0  # 間違った切片

        self.prediction_line = self.axes.plot(
            lambda x: self.current_slope * x + self.current_intercept,
            x_range=[0, 5],
            color=RED,
            stroke_width=3,
        )

        # ラベル
        pred_label = Text("AIの予測", font_size=28, color=RED)
        pred_label.to_edge(UP).shift(RIGHT * 3)

        self.play(Write(pred_label))
        self.play(Create(self.prediction_line))

        # 説明
        bad_explain = Text("最初の予測はでたらめ", font_size=28, color=RED)
        bad_explain.to_edge(DOWN, buff=1)
        self.play(Write(bad_explain))
        self.wait(1)
        self.play(FadeOut(bad_explain), FadeOut(pred_label))

    def show_loss_visualization(self):
        """ズレ（損失）を可視化"""
        # 各データ点から予測線への垂直線（誤差）を描画
        self.error_lines = VGroup()
        for x, y in zip(self.x_data, self.y_data):
            pred_y = self.current_slope * x + self.current_intercept
            error_line = Line(
                self.axes.c2p(x, y),
                self.axes.c2p(x, pred_y),
                color=ORANGE,
                stroke_width=2,
            )
            self.error_lines.add(error_line)

        error_label = Text("予測と正解のズレ", font_size=24, color=ORANGE)
        error_label.to_edge(UP).shift(RIGHT * 3)

        self.play(Write(error_label))
        self.play(LaggedStart(*[Create(e) for e in self.error_lines], lag_ratio=0.1))
        self.wait(0.5)

        # 損失スコアを計算・表示
        loss = self.calculate_loss(self.current_slope, self.current_intercept)
        self.loss_text = VGroup(
            Text("損失（ズレの合計）:", font_size=24),
            DecimalNumber(loss, num_decimal_places=2, font_size=32, color=RED),
        ).arrange(RIGHT, buff=0.3)
        self.loss_text.to_edge(RIGHT, buff=0.5).shift(UP * 2)

        self.play(Write(self.loss_text))
        self.wait(1)

        # 損失を小さくしたいという目標を示す
        goal_text = Text("→ これを小さくしたい！", font_size=24, color=GREEN)
        goal_text.next_to(self.loss_text, DOWN, buff=0.3)
        self.play(Write(goal_text))
        self.wait(1)
        self.play(FadeOut(goal_text), FadeOut(error_label))

    def calculate_loss(self, slope, intercept):
        """MSE（平均二乗誤差）を計算"""
        pred_y = slope * self.x_data + intercept
        mse = np.mean((self.y_data - pred_y) ** 2)
        return mse

    def show_learning_process(self):
        """学習プロセス（勾配降下法）をアニメーション"""
        learn_label = Text("学習中...", font_size=28, color=BLUE)
        learn_label.to_edge(UP).shift(RIGHT * 3)
        self.play(Write(learn_label))

        # 学習のステップを定義（徐々に正解に近づく）
        # 目標: slope ≈ 0.7, intercept ≈ 0.5
        learning_steps = [
            (-0.3, 4.0),   # 初期（現在）
            (-0.1, 3.5),   # ステップ1
            (0.15, 2.8),   # ステップ2
            (0.35, 2.0),   # ステップ3
            (0.50, 1.3),   # ステップ4
            (0.60, 0.9),   # ステップ5
            (0.68, 0.6),   # ステップ6（ほぼ収束）
        ]

        # 反復回数表示
        iteration_text = Text("反復: 0", font_size=24)
        iteration_text.next_to(self.loss_text, DOWN, buff=0.5)
        self.play(Write(iteration_text))

        for i, (slope, intercept) in enumerate(learning_steps[1:], 1):
            # 新しい線を作成
            new_line = self.axes.plot(
                lambda x, s=slope, b=intercept: s * x + b,
                x_range=[0, 5],
                color=RED,
                stroke_width=3,
            )

            # 新しい誤差線を作成
            new_error_lines = VGroup()
            for x, y in zip(self.x_data, self.y_data):
                pred_y = slope * x + intercept
                error_line = Line(
                    self.axes.c2p(x, y),
                    self.axes.c2p(x, pred_y),
                    color=ORANGE,
                    stroke_width=2,
                )
                new_error_lines.add(error_line)

            # 新しい損失を計算
            new_loss = self.calculate_loss(slope, intercept)

            # 新しい反復回数テキスト
            new_iteration_text = Text(f"反復: {i}", font_size=24)
            new_iteration_text.next_to(self.loss_text, DOWN, buff=0.5)

            # アニメーション：線と誤差線を同時に更新
            self.play(
                Transform(self.prediction_line, new_line),
                Transform(self.error_lines, new_error_lines),
                self.loss_text[1].animate.set_value(new_loss),
                Transform(iteration_text, new_iteration_text),
                run_time=0.8,
            )
            self.wait(0.3)

            # パラメータを更新
            self.current_slope = slope
            self.current_intercept = intercept

        self.play(FadeOut(learn_label), FadeOut(iteration_text))

    def show_convergence(self):
        """収束を示す"""
        # 損失が小さくなったことを強調
        success_box = SurroundingRectangle(self.loss_text, color=GREEN, buff=0.15)
        success_label = Text("損失が小さくなった！", font_size=28, color=GREEN)
        success_label.to_edge(UP).shift(RIGHT * 3)

        self.play(Write(success_label), Create(success_box))
        self.wait(0.5)

        # 線がデータにフィットしていることを示す
        fit_label = Text("予測がデータにフィット", font_size=24, color=GREEN)
        fit_label.next_to(self.loss_text, DOWN, buff=0.8)
        self.play(Write(fit_label))
        self.wait(1)

        # 学習完了
        complete_text = VGroup(
            Text("これが「学習」の本質", font_size=32),
            Text("予測と正解のズレを", font_size=28),
            Text("繰り返し小さくしていく", font_size=28),
        ).arrange(DOWN, buff=0.2)
        complete_text.to_edge(DOWN, buff=0.8)

        self.play(Write(complete_text))
        self.wait(2)

        # クリーンアップ
        self.play(
            FadeOut(success_box),
            FadeOut(success_label),
            FadeOut(fit_label),
            FadeOut(complete_text),
            FadeOut(self.error_lines),
            FadeOut(self.loss_text),
        )
        self.wait(0.5)

    def show_generalization(self):
        """より複雑なモデルへの一般化"""
        # 現在の線を保持しつつ、説明を追加
        current_state = VGroup(self.axes, self.data_dots, self.prediction_line)

        # 縮小して左に移動
        self.play(current_state.animate.scale(0.6).to_edge(LEFT, buff=0.5))

        # 右側に説明テキスト
        generalize_text = VGroup(
            Text("今見たのは「直線を1本引く」問題", font_size=26),
            Text("パラメータは2つだけ", font_size=26, color=YELLOW),
            Text("（傾きと切片）", font_size=22, color=GRAY),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        generalize_text.to_edge(RIGHT, buff=0.8).shift(UP * 1.5)

        self.play(Write(generalize_text))
        self.wait(1.5)

        # 「でも...」の展開
        but_text = VGroup(
            Text("では、もし...", font_size=28, color=BLUE),
            Text("・曲線だったら？", font_size=26),
            Text("・画像を認識したい？", font_size=26),
            Text("・言語を理解したい？", font_size=26),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        but_text.next_to(generalize_text, DOWN, buff=0.6, aligned_edge=LEFT)

        self.play(Write(but_text[0]))
        self.wait(0.3)
        for line in but_text[1:]:
            self.play(Write(line), run_time=0.5)
            self.wait(0.2)
        self.wait(1)

        # 結論
        self.play(FadeOut(generalize_text), FadeOut(but_text))

        # 前半：パラメータ数の話
        conclusion_first = VGroup(
            Text("パラメータが2個じゃなくて", font_size=32),
            Text("100万個、10億個になる", font_size=32, color=RED),
        ).arrange(DOWN, buff=0.3)
        conclusion_first.to_edge(RIGHT, buff=0.5)

        self.play(Write(conclusion_first[0]))
        self.play(Write(conclusion_first[1]))
        self.wait(1)

        # 一度フェードアウト
        self.play(FadeOut(conclusion_first))

        # 後半：本質は同じ
        conclusion_second = VGroup(
            Text("でもやってることは同じ", font_size=36, color=GREEN),
            Text("「ズレを小さくする」", font_size=32, color=GREEN),
        ).arrange(DOWN, buff=0.3)
        conclusion_second.to_edge(RIGHT, buff=0.5)

        self.play(FadeIn(conclusion_second[0]))
        self.play(FadeIn(conclusion_second[1]))
        self.wait(2)

        # 最後のクリーンアップ
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # 最終メッセージ
        final = VGroup(
            Text("機械学習の本質", font_size=40),
            Text("= データから「ズレ」を最小化する", font_size=36, color=BLUE),
        ).arrange(DOWN, buff=0.4)
        self.play(Write(final[0]))
        self.play(Write(final[1]))
        self.wait(2)
        self.play(FadeOut(final))


class MLBasicsShort(Scene):
    """機械学習の基本（短縮版）"""

    def construct(self):
        # 核心部分だけを抽出
        title = Text("機械学習のしくみ", font_size=44)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.scale(0.6).to_edge(UP))

        # 3ステップで説明
        steps = VGroup(
            VGroup(
                Text("1.", font_size=32, color=YELLOW),
                Text("データを用意する", font_size=32),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("2.", font_size=32, color=GREEN),
                Text("予測と正解のズレを計算", font_size=32),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("3.", font_size=32, color=BLUE),
                Text("ズレが小さくなるよう調整", font_size=32),
            ).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        steps.next_to(title, DOWN, buff=0.8)

        for step in steps:
            self.play(Write(step), run_time=0.8)
            self.wait(0.5)

        # 矢印で繰り返しを示す
        repeat_arrow = CurvedArrow(
            steps[2].get_right() + RIGHT * 0.3,
            steps[1].get_right() + RIGHT * 0.3,
            angle=-PI / 2,
            color=ORANGE,
        )
        repeat_text = Text("繰り返す", font_size=24, color=ORANGE)
        repeat_text.next_to(repeat_arrow, RIGHT, buff=0.2)

        self.play(Create(repeat_arrow), Write(repeat_text))
        self.wait(1)

        # 強調
        box = SurroundingRectangle(steps, color=WHITE, buff=0.3)
        self.play(Create(box))

        conclusion = Text(
            "これが「学習」の正体",
            font_size=36,
            color=WHITE,
        )
        conclusion.to_edge(DOWN, buff=1)
        self.play(Write(conclusion))
        self.wait(2)


class ProjectileMotionAI(Scene):
    """放物運動を予測するAIモデルの解説アニメーション"""

    # 物理定数
    G = 9.8  # 重力加速度 (m/s²)

    def construct(self):
        # タイトル
        self.show_title()

        # 放物運動の基本
        self.show_basic_projectile()

        # パラメータの説明
        self.show_parameters()

        # 学習データの可視化
        self.show_training_data()

        # モデルの入出力
        self.show_model_io()

    def projectile_trajectory(self, v0, theta_deg, num_points=50):
        """放物線の軌道を計算"""
        theta = np.radians(theta_deg)
        # 滞空時間
        t_flight = 2 * v0 * np.sin(theta) / self.G
        t = np.linspace(0, t_flight, num_points)

        x = v0 * np.cos(theta) * t
        y = v0 * np.sin(theta) * t - 0.5 * self.G * t**2
        y = np.maximum(y, 0)  # 地面より下に行かない

        return x, y

    def show_title(self):
        """タイトル表示"""
        title = Text("放物運動を予測するAI", font_size=48)
        subtitle = Text("シンプルな例で機械学習を体感", font_size=28, color=BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

    def show_basic_projectile(self):
        """放物運動の基本をアニメーション"""
        # 座標軸
        axes = Axes(
            x_range=[0, 12, 2],
            y_range=[0, 4, 1],
            x_length=10,
            y_length=4,
            axis_config={"include_tip": True, "include_numbers": False},
        )
        axes.shift(DOWN * 1)

        x_label = Text("距離", font_size=20)
        x_label.next_to(axes.x_axis, DOWN, buff=0.1)
        y_label = Text("高さ", font_size=20)
        y_label.next_to(axes.y_axis, LEFT, buff=0.1)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # ボールを投げるアニメーション
        v0, theta = 8, 45  # 初速度 8 m/s, 角度 45°
        x_data, y_data = self.projectile_trajectory(v0, theta)

        # 軌道の点を座標系に変換
        # スケーリング: x方向は1m=0.8単位、y方向は1m=1単位
        scale_x, scale_y = 0.8, 1.0
        trajectory_points = [
            axes.c2p(x * scale_x, y * scale_y) for x, y in zip(x_data, y_data)
        ]

        # ボール
        ball = Dot(trajectory_points[0], color=YELLOW, radius=0.15)
        ball_trail = TracedPath(
            ball.get_center, stroke_color=YELLOW, stroke_width=3, stroke_opacity=0.7
        )

        self.add(ball_trail)
        self.play(Create(ball))

        # ボールを軌道に沿って動かす
        for i in range(1, len(trajectory_points), 2):
            self.play(
                ball.animate.move_to(trajectory_points[i]),
                run_time=0.05,
                rate_func=linear,
            )

        self.wait(0.5)

        # 説明テキスト
        explain = Text("ボールを投げると放物線を描く", font_size=28)
        explain.to_edge(UP)
        self.play(Write(explain))
        self.wait(1)

        # 保存して次のシーンへ
        self.axes = axes
        self.ball = ball
        self.ball_trail = ball_trail
        self.play(FadeOut(explain), FadeOut(ball), FadeOut(ball_trail))

    def show_parameters(self):
        """パラメータの説明"""
        title = Text("2つのパラメータで軌道が決まる", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # 初速度の矢印
        v0_arrow = Arrow(
            self.axes.c2p(0, 0),
            self.axes.c2p(1.5, 1.5),
            color=RED,
            stroke_width=4,
            buff=0,
        )
        v0_label = MathTex(r"v_0", font_size=36, color=RED)
        v0_label.next_to(v0_arrow, UP, buff=0.1)

        # 角度の弧
        angle_arc = Arc(
            radius=0.8,
            start_angle=0,
            angle=PI / 4,
            arc_center=self.axes.c2p(0, 0),
            color=GREEN,
        )
        theta_label = MathTex(r"\theta", font_size=36, color=GREEN)
        theta_label.next_to(angle_arc, RIGHT, buff=0.2).shift(UP * 0.2)

        self.play(Create(v0_arrow), Write(v0_label))
        self.play(Create(angle_arc), Write(theta_label))
        self.wait(0.5)

        # パラメータの説明テキスト
        param_box = VGroup(
            VGroup(
                Text("初速度", font_size=24),
                MathTex(r"v_0", font_size=28, color=RED),
                Text(": 5〜10 m/s", font_size=24),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Text("発射角度", font_size=24),
                MathTex(r"\theta", font_size=28, color=GREEN),
                Text(": 30°〜60°", font_size=24),
            ).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        param_box.to_edge(RIGHT, buff=0.5).shift(UP * 0.5)

        box_rect = SurroundingRectangle(param_box, color=WHITE, buff=0.2)

        self.play(Write(param_box), Create(box_rect))
        self.wait(1.5)

        # クリーンアップ（座標軸は残す）
        self.play(
            FadeOut(title),
            FadeOut(v0_arrow),
            FadeOut(v0_label),
            FadeOut(angle_arc),
            FadeOut(theta_label),
            FadeOut(param_box),
            FadeOut(box_rect),
        )

    def show_training_data(self):
        """学習データの可視化"""
        title = Text("様々なパラメータで軌道を生成", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # 異なるパラメータで複数の軌道を描画
        trajectories = []
        colors = [YELLOW, ORANGE, RED, PINK, PURPLE, BLUE, TEAL, GREEN]

        # パラメータの組み合わせ
        params = [
            (5, 30),
            (6, 40),
            (7, 45),
            (8, 50),
            (9, 55),
            (10, 60),
            (7, 35),
            (9, 45),
        ]

        scale_x, scale_y = 0.8, 1.0

        for i, (v0, theta) in enumerate(params):
            x_data, y_data = self.projectile_trajectory(v0, theta)
            points = [
                self.axes.c2p(x * scale_x, y * scale_y)
                for x, y in zip(x_data, y_data)
            ]
            trajectory = VMobject()
            trajectory.set_points_smoothly(points)
            trajectory.set_stroke(colors[i % len(colors)], width=2, opacity=0.8)
            trajectories.append(trajectory)

        # 軌道を順番に描画
        for traj in trajectories[:4]:
            self.play(Create(traj), run_time=0.5)

        # 残りは同時に描画
        self.play(*[Create(traj) for traj in trajectories[4:]], run_time=0.8)

        # 説明
        data_label = Text("これが「学習データ」", font_size=28, color=YELLOW)
        data_label.next_to(self.axes, DOWN, buff=0.3)
        self.play(Write(data_label))
        self.wait(1.5)

        # 保存
        self.trajectories = VGroup(*trajectories)
        self.play(FadeOut(title), FadeOut(data_label))

    def show_model_io(self):
        """モデルの入出力を図式化"""
        # 既存の座標軸と軌道を縮小して左に移動
        old_elements = VGroup(self.axes, self.trajectories)
        self.play(old_elements.animate.scale(0.5).to_edge(LEFT, buff=0.3))

        # モデルの入出力図
        # 入力ボックス
        input_box = VGroup(
            Rectangle(width=2.5, height=1.5, color=RED, fill_opacity=0.2),
            Text("入力", font_size=20, color=RED).shift(UP * 0.4),
            MathTex(r"v_0, \theta", font_size=28).shift(DOWN * 0.15),
        )
        input_box.move_to(LEFT * 1 + UP * 1)

        # AIモデルボックス
        model_box = VGroup(
            Rectangle(width=2, height=1.5, color=BLUE, fill_opacity=0.3),
            Text("AIモデル", font_size=22, color=BLUE),
        )
        model_box.next_to(input_box, RIGHT, buff=0.8)

        # 出力ボックス
        output_box = VGroup(
            Rectangle(width=2.5, height=1.5, color=GREEN, fill_opacity=0.2),
            Text("出力", font_size=20, color=GREEN).shift(UP * 0.4),
            Text("軌道の予測", font_size=22).shift(DOWN * 0.15),
        )
        output_box.next_to(model_box, RIGHT, buff=0.8)

        # 矢印
        arrow1 = Arrow(
            input_box.get_right(),
            model_box.get_left(),
            color=WHITE,
            buff=0.1,
        )
        arrow2 = Arrow(
            model_box.get_right(),
            output_box.get_left(),
            color=WHITE,
            buff=0.1,
        )

        self.play(FadeIn(input_box))
        self.play(Create(arrow1))
        self.play(FadeIn(model_box))
        self.play(Create(arrow2))
        self.play(FadeIn(output_box))
        self.wait(1)

        # 説明テキスト
        explain = VGroup(
            Text("初速度と発射角度を入力するだけで", font_size=26),
            Text("軌道を予測できるようになる", font_size=26, color=GREEN),
        ).arrange(DOWN, buff=0.2)
        explain.to_edge(DOWN, buff=0.8)

        self.play(Write(explain))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # 最終メッセージ
        final = VGroup(
            Text("物理法則を教えなくても", font_size=32),
            Text("データから学習できる", font_size=36, color=BLUE),
        ).arrange(DOWN, buff=0.3)
        self.play(Write(final[0]))
        self.play(Write(final[1]))
        self.wait(2)
        self.play(FadeOut(final))


class TrainingVsInference(Scene):
    """学習と推論のコスト差を解説するアニメーション"""

    def construct(self):
        # タイトル
        self.show_title()

        # 学習フェーズの可視化
        self.show_training_phase()

        # 予測フェーズの可視化
        self.show_inference_phase()

        # コスト比較
        self.show_comparison()

    def show_title(self):
        """タイトル表示"""
        title = Text("学習は大変、でも予測は一瞬", font_size=44)
        self.play(Write(title))
        self.wait(1.5)
        self.play(FadeOut(title))

    def show_training_phase(self):
        """学習フェーズの可視化"""
        # セクションタイトル
        section_title = Text("学習フェーズ", font_size=36, color=RED)
        section_title.to_edge(UP)
        self.play(Write(section_title))

        # AIモデルのボックス（中央）
        model_box = VGroup(
            RoundedRectangle(
                width=3, height=2, corner_radius=0.2, color=BLUE, fill_opacity=0.3
            ),
            Text("AIモデル", font_size=24, color=BLUE),
        )
        model_box.move_to(ORIGIN)

        self.play(FadeIn(model_box))

        # 左側：大量のデータが流れ込む
        data_label = Text("大量のデータ", font_size=20, color=YELLOW)
        data_label.next_to(model_box, LEFT, buff=2)

        self.play(Write(data_label))

        # 画面下にプログレスバーを配置
        progress_bg = Rectangle(width=10, height=0.3, color=GRAY, fill_opacity=0.3)
        progress_bg.to_edge(DOWN, buff=1)
        progress_bar = Rectangle(width=0.1, height=0.3, color=GREEN, fill_opacity=0.8)
        progress_bar.align_to(progress_bg, LEFT)
        progress_bar.move_to(progress_bg.get_left(), aligned_edge=LEFT)

        self.play(Create(progress_bg))
        self.add(progress_bar)

        # データの流れをアニメーション（複数のドットが流れる）+ プログレスバーが伸びる
        num_waves = 6
        bar_width_per_wave = 10 / num_waves

        for wave in range(num_waves):
            data_dots = VGroup(
                *[
                    Dot(color=YELLOW, radius=0.08).move_to(
                        data_label.get_right() + RIGHT * 0.3 + UP * (i - 2) * 0.3
                    )
                    for i in range(5)
                ]
            )

            # データ流入とプログレスバーの伸びを同時に
            target_width = bar_width_per_wave * (wave + 1)
            new_bar = Rectangle(
                width=target_width, height=0.3, color=GREEN, fill_opacity=0.8
            )
            new_bar.align_to(progress_bg, LEFT)
            new_bar.move_to(progress_bg.get_left(), aligned_edge=LEFT)

            self.play(
                *[
                    dot.animate.move_to(model_box.get_left() + LEFT * 0.1)
                    for dot in data_dots
                ],
                Transform(progress_bar, new_bar),
                run_time=0.6,
            )
            self.play(FadeOut(data_dots), run_time=0.15)

        # コストの説明
        cost_text = VGroup(
            Text("大量のGPU", font_size=22, color=RED),
            Text("長い時間", font_size=22, color=RED),
        ).arrange(DOWN, buff=0.2)
        cost_text.to_edge(RIGHT, buff=1).shift(UP * 0.5)

        cost_box = SurroundingRectangle(cost_text, color=RED, buff=0.2)
        self.play(Write(cost_text), Create(cost_box))
        self.wait(1)

        # クリーンアップ
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_inference_phase(self):
        """予測（推論）フェーズの可視化"""
        # セクションタイトル
        section_title = Text("予測フェーズ", font_size=36, color=GREEN)
        section_title.to_edge(UP)
        self.play(Write(section_title))

        # 学習済みモデル
        model_box = VGroup(
            RoundedRectangle(
                width=3, height=2, corner_radius=0.2, color=BLUE, fill_opacity=0.5
            ),
            Text("学習済み", font_size=20, color=WHITE).shift(UP * 0.3),
            Text("モデル", font_size=24, color=WHITE).shift(DOWN * 0.2),
        )
        model_box.move_to(ORIGIN)

        self.play(FadeIn(model_box))

        # 入力
        input_box = VGroup(
            Rectangle(width=2.5, height=1.2, color=YELLOW, fill_opacity=0.2),
            Text("入力データ", font_size=20, color=YELLOW),
        )
        input_box.next_to(model_box, LEFT, buff=1.5)

        # 出力
        output_box = VGroup(
            Rectangle(width=2.5, height=1.2, color=GREEN, fill_opacity=0.2),
            Text("予測結果", font_size=20, color=GREEN),
        )
        output_box.next_to(model_box, RIGHT, buff=1.5)

        self.play(FadeIn(input_box))

        # 矢印と「一瞬」の演出
        arrow1 = Arrow(input_box.get_right(), model_box.get_left(), color=WHITE, buff=0.1)
        arrow2 = Arrow(model_box.get_right(), output_box.get_left(), color=WHITE, buff=0.1)

        # 入力→モデル→出力を一瞬で
        self.play(Create(arrow1), run_time=0.3)

        # 閃光演出
        flash = Circle(radius=0.1, color=WHITE, fill_opacity=1)
        flash.move_to(model_box.get_center())
        self.play(
            flash.animate.scale(20).set_opacity(0),
            Create(arrow2),
            FadeIn(output_box),
            run_time=0.4,
        )

        # 「一瞬！」のテキスト
        instant_text = Text("一瞬！", font_size=48, color=GREEN)
        instant_text.next_to(model_box, DOWN, buff=0.8)
        self.play(FadeIn(instant_text, scale=1.5), run_time=0.3)
        self.wait(1)

        # クリーンアップ
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_comparison(self):
        """学習と推論のコスト比較"""
        title = Text("コストの比較", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # 左側：学習
        training_title = Text("学習", font_size=32, color=RED)
        training_title.move_to(LEFT * 3.5 + UP * 1.5)

        training_bar_bg = Rectangle(width=4, height=0.6, color=GRAY, fill_opacity=0.3)
        training_bar_bg.next_to(training_title, DOWN, buff=0.5)
        training_bar = Rectangle(width=4, height=0.6, color=RED, fill_opacity=0.7)
        training_bar.move_to(training_bar_bg.get_center())

        training_cost = VGroup(
            Text("数日〜数週間", font_size=22),
            Text("大量のGPU", font_size=22),
        ).arrange(DOWN, buff=0.2)
        training_cost.next_to(training_bar_bg, DOWN, buff=0.3)

        # 右側：推論
        inference_title = Text("予測", font_size=32, color=GREEN)
        inference_title.move_to(RIGHT * 3.5 + UP * 1.5)

        inference_bar_bg = Rectangle(width=4, height=0.6, color=GRAY, fill_opacity=0.3)
        inference_bar_bg.next_to(inference_title, DOWN, buff=0.5)
        inference_bar = Rectangle(width=0.15, height=0.6, color=GREEN, fill_opacity=0.7)
        inference_bar.align_to(inference_bar_bg, LEFT)

        inference_cost = VGroup(
            Text("数秒〜数分", font_size=22),
            Text("普通のPC/GPU", font_size=22),
        ).arrange(DOWN, buff=0.2)
        inference_cost.next_to(inference_bar_bg, DOWN, buff=0.3)

        # アニメーション
        self.play(Write(training_title), Write(inference_title))
        self.play(Create(training_bar_bg), Create(inference_bar_bg))
        self.play(FadeIn(training_bar), FadeIn(inference_bar))
        self.play(Write(training_cost), Write(inference_cost))
        self.wait(1)

        # 強調メッセージ
        emphasis = VGroup(
            Text("一度学習すれば", font_size=28),
            Text("予測は何度でも高速に実行できる", font_size=28, color=GREEN),
        ).arrange(DOWN, buff=0.2)
        emphasis.to_edge(DOWN, buff=0.8)

        box = SurroundingRectangle(emphasis, color=GREEN, buff=0.2)
        self.play(Write(emphasis), Create(box))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # 最終メッセージ
        final = VGroup(
            Text("学習コストは「初期投資」", font_size=32),
            Text("予測コストは「運用コスト」", font_size=32, color=BLUE),
        ).arrange(DOWN, buff=0.4)
        self.play(Write(final[0]))
        self.play(Write(final[1]))
        self.wait(2)
        self.play(FadeOut(final))


if __name__ == "__main__":
    # コマンドラインから実行する場合の例
    # manim -pql ml_basics_animation.py MLBasics
    # manim -pql ml_basics_animation.py MLBasicsShort
    # manim -pql ml_basics_animation.py ProjectileMotionAI
    # manim -pql ml_basics_animation.py TrainingVsInference
    pass
