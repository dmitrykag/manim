from manim import *
import math

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


class HeavyRopeOnSlope(MovingCameraScene):
    def getAnnotation(self, text: str) -> Text:
        res = Text(text, font="sans-serif")
        res.scale(0.5)
        res.shift(3 * UP)
        return res

    def force(self, start, end: float, text: str, pos: np.ndarray) -> Mobject:
        res = VGroup()
        f = Arrow(start, end, buff=0, color=BLUE)
        res.add(f)
        res.add(Text(text, font="sans-serif").scale(0.5).next_to(f, pos))
        return res


    def construct(self):
        left = LEFT * 5 + 3 * DOWN
        right = RIGHT * 5 + 3 * DOWN
        up = RIGHT * 5 + UP * 4 + 3 * DOWN

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

        coord = Arrow(up, left, color=BLUE)
        coord.shift((left - up) * 0.2)
        coord.set_z_index(-1)
        self.add(coord)

        self.wait()

        self.play(FadeOut(ann))
        ann = self.getAnnotation("Силы, действующие на канат")
        self.play(FadeIn(ann))
        self.wait()

        forces = VGroup()

        start = ropeCopy.get_center()
        end = start + 1.5*DOWN
        forces.add(self.force(start, end, "mg", RIGHT))

        start = ropeCopy.get_end()
        end = start + (up - left) * 0.15
        forces.add(self.force(start, end, "T", UP))

        start = ropeCopy.get_center()
        vec = slope.get_vector()
        perp = np.empty_like(vec)
        perp[0] = -vec[1]
        perp[1] = vec[0]
        end = start + normalize(perp)*1.4
        forces.add(self.force(start, end, "N", RIGHT))

        self.play(FadeIn(forces))
        self.wait()

        self.play(*[FadeOut(mob)for mob in self.mobjects], run_time=5)






