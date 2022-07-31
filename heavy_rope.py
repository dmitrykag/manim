from manim import *
import math
from typing import Tuple

from numpy import float64

def patch_tex_template():
    myTemplate = TexTemplate()
    print(myTemplate.preamble)
    preamble = myTemplate.preamble.replace(r'\usepackage[english]{babel}',
                                           r'\usepackage[english,russian]{babel}')
    return TexTemplate(preamble=preamble)



class Matrix(Scene):
    def construct(self):
        tex_template = patch_tex_template()

        texlhs = "\\begin{equation*}" \
              "\\begin{pmatrix}" \
              "\\cos \\frac{\\pi}{6} & -\\sin \\frac{\\pi}{6} \\\\ \\sin \\frac{\\pi}{6} & \\cos \\frac{\\pi}{6}" \
              "\\end{pmatrix}" \
              "\\begin{pmatrix}" \
              "x \\\\ y" \
              "\\end{pmatrix} = " \
              "\\end{equation*}"

        texrhs = "$$" \
              "\\begin{pmatrix}" \
              "x \\\\ y" \
              "\\end{pmatrix}" \
              "$$"

        matrix = Tex(texlhs, texrhs, tex_template=tex_template)

        self.play(Write(matrix))
        # self.wait()
        # self.play(ClockwiseTransform(matrix[1], matrix[1]))
        self.play(Rotating(matrix[1], radians=PI/6), run_time=1)

class Test(Scene):

    def cos(self, vec: np.ndarray) -> float64:
        return vec[0] / math.sqrt(np.dot(vec, vec))

    def sin(self, vec: np.ndarray) -> float64:
        return vec[1] / math.sqrt(np.dot(vec, vec))

    def construct(self):
        def norm_perpendicular(vec: np.ndarray) -> np.ndarray:
            perp = np.empty_like(vec)
            perp[0] = -vec[1]
            perp[1] = vec[0]
            perp /= np.linalg.norm(perp)
            return perp

        def perp_to_line(point_from: np.ndarray, line_start: np.ndarray, line_end: np.ndarray) -> np.ndarray:
            direction = norm_perpendicular(line_end - line_start)
            distance = np.linalg.norm(np.cross(line_end - line_start, point_from - line_start))
            distance /= np.linalg.norm(line_end - line_start)
            return point_from - direction * distance

        def projection(vec: Line, to_proj: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
            prj = to_proj * vec.get_vector().dot(to_proj)
            prj /= to_proj.dot(to_proj)
            return vec.get_start(), prj + vec.get_start()

        left = LEFT * 5 + 3 * DOWN
        right = RIGHT * 5 + 3 * DOWN
        up = RIGHT * 5 + UP * 4 + 3 * DOWN

        cos = (right-left)[0] / math.sqrt(np.dot(up-left, up-left))
        sin = (up-right)[1] / math.sqrt(np.dot(up-left, up-left))
        tg = sin/cos
        print('sin, cos, tg', sin, cos, tg, sin*sin + cos*cos)

        horiz = Line(left, right)
        vert = Line(right, up)
        slope = Line(left, up)

        rope = Line(left, up, stroke_width=12, color=MAROON)
        rope.scale(0.5)
        rope.shift(UP*0.1)

        self.add(rope)

        coord = Arrow(up, left, buff=0, color=BLUE)
        print('coord', coord.get_vector())
        coord.shift((left - up) * 0.2)
        print('coord', coord.get_vector())
        # coord.set_z_index(-1)

        self.add(coord)

        start = rope.get_center()
        end = start + 2*DOWN
        mg = Arrow(start, end, buff=0, color=BLUE)

        self.add(mg)

        # mg_proj = projection(mg, coord.get_vector())
        start, end = projection(mg, coord.get_vector())
        # mg_proj = mg.copy()
        mg_proj = Arrow(start, end, buff=0, color=BLUE)
        # mg_proj.shift(RIGHT)
        # mg_proj.set_points_by_ends(mg.get_start(), mg.get_end() + RIGHT)
        self.add(mg_proj)

        # perp = norm_perpendicular(coord.get_vector())
        # perp *= np.linalg.norm(np.cross(rope.get_end() - rope.get_start(), mg.get_end() - rope.get_end()))
        # perp /= np.linalg.norm(rope.get_end() - rope.get_start())

        perp = perp_to_line(mg.get_end(), coord.get_start(), coord.get_end())
        dashed = DashedLine(mg.get_end(), perp, color=BLUE)

        # dashed = DashedLine(mg.get_end(), mg.get_end() - perp, color=BLUE)
        # mg_proj.shift(RIGHT)
        # mg_proj.set_points_by_ends(mg.get_start(), mg.get_end() + RIGHT)
        self.add(dashed)




class HeavyRopeOnSlope(MovingCameraScene):
    def getAnnotation(self, text: str) -> Text:
        res = Text(text, font="sans-serif")
        res.scale(0.5)
        res.shift(3 * UP)
        return res

    def getMathTexAnnotation(self, text: str) -> Text:
        res = SingleStringMathTex(text, tex_template=patch_tex_template())
        res.scale(0.5)
        res.shift(3 * UP)
        return res

    def force(self, start: float, end: float, text: str = "", pos: np.ndarray = ORIGIN, *vmobjects, **kwargs) -> VGroup:
        class Force(VGroup):
            def __init__(self, start: float, end: float, text: str, pos: np.ndarray):
                super().__init__(*vmobjects, **kwargs)
                self.arrow = Arrow(start, end, buff=0, color=BLUE)
                super().add(self.arrow)
                super().add(Text(text, font="sans-serif").scale(0.5).next_to(self.arrow, pos))
                print('force: ', start, end, text)

        return Force(start, end, text, pos)

    def construct(self):
        def norm_perpendicular(vec: np.ndarray) -> np.ndarray:
            perp = np.empty_like(vec)
            perp[0] = -vec[1]
            perp[1] = vec[0]
            perp /= np.linalg.norm(perp)
            return perp

        def perp_to_line(point_from: np.ndarray, line_start: np.ndarray, line_end: np.ndarray) -> np.ndarray:
            direction = norm_perpendicular(line_end - line_start)
            distance = np.linalg.norm(np.cross(line_end - line_start, point_from - line_start))
            distance /= np.linalg.norm(line_end - line_start)
            return point_from - direction * distance

        def projection(vec: Line, to_proj: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
            prj = to_proj * vec.get_vector().dot(to_proj)
            prj /= to_proj.dot(to_proj)
            return vec.get_start(), prj + vec.get_start()


        left = LEFT * 5 + 3 * DOWN
        right = RIGHT * 5 + 3 * DOWN
        up = RIGHT * 5 + UP * 4 + 3 * DOWN

        cos = (right-left)[0] / math.sqrt(np.dot(up-left, up-left))
        sin = (up-right)[1] / math.sqrt(np.dot(up-left, up-left))
        tg = sin/cos
        print('sin, cos, tg', sin, cos, tg, sin*sin + cos*cos)

        horiz = Line(left, right)
        vert = Line(right, up)
        slope = Line(left, up)

        inclinedPlane = Group()
        inclinedPlane.add(horiz, vert, slope, Angle(horiz, slope))

        self.play(FadeIn(inclinedPlane))
        self.wait()

        ann = self.getAnnotation("Положим на наклонную плоскость тяжелый канат")
        self.play(FadeIn(ann))
        self.wait()

        rope = Line(left, up, stroke_width=12, color=MAROON)
        rope.scale(0.5)
        ropeCopy = rope.copy()
        rope.shift(UP)
        ropeCopy.shift(UP*0.1)

        self.play(Transform(rope, ropeCopy))
        self.wait()

        self.play(FadeOut(ann))
        ann = self.getAnnotation("Закрепим его сверху")
        self.play(FadeIn(ann))
        self.wait()

        dot = Dot(rope.get_end(), color=YELLOW, stroke_width=20)
        inclinedPlane.add(dot)

        self.add(inclinedPlane)
        self.wait()

        self.play(FadeOut(ann))
        ann = self.getAnnotation("Ось координат выберем вдоль плоскости")
        self.play(FadeIn(ann))
        self.wait()

        coord = Arrow(up, left, buff=0, color=BLUE)
        print('coord', coord.get_vector())
        coord.shift((left - up) * 0.2)
        print('coord', coord.get_vector())
        coord.set_z_index(-1)
        self.add(coord)

        self.wait()

        self.play(FadeOut(ann))
        ann = self.getAnnotation("Силы, действующие на канат")
        self.play(FadeIn(ann))
        self.wait()

        forces = VGroup()

        start = ropeCopy.get_center()
        end = start + 2*DOWN
        mg = self.force(start, end, "mg", RIGHT)
        forces.add(mg)

        start = ropeCopy.get_end()
        end = start + (up - left) * 0.1
        forces.add(self.force(start, end, "T", UP))

        start = ropeCopy.get_center()
        end = start + norm_perpendicular(slope.get_vector())*1.2
        forces.add(self.force(start, end, "N", RIGHT))

        self.play(FadeIn(forces))
        self.wait()

        projections = VGroup()

        mg_proj = projection(mg.arrow, coord.get_vector())
        projections.add(self.force(mg_proj[0], mg_proj[1]))

        perp = perp_to_line(mg.arrow.get_end(), coord.get_start(), coord.get_end())
        dashed = DashedLine(mg.arrow.get_end(), perp, color=BLUE)
        projections.add(dashed)

        self.play(FadeIn(projections))
        self.wait()

        self.play(FadeOut(ann))
        ann = self.getAnnotation("Сила натяжения каната")
        tex = self.getMathTexAnnotation("T = mg\\sin{\\alpha}").next_to(ann, DOWN)
        self.play(FadeIn(ann, tex))
        self.wait()

        tex1 = self.getMathTexAnnotation("m = l\\rho = \\frac{H\\rho}{\\sin{\\alpha}}").next_to(tex, DOWN)
        self.play(FadeIn(tex1))
        self.wait()

        self.play(FadeOut(tex, tex1))
        tex = self.getMathTexAnnotation("T = \\rho g H").next_to(ann, DOWN)
        self.play(FadeIn(tex))

        self.wait()


        self.play(*[FadeOut(mob)for mob in self.mobjects], run_time=5)






