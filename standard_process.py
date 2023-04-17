from manimlib import *


class UtilitiesInCategories(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spacing = 0.15
        self.circle_radius = 0.5
        self.top = 3
        self.left = -2.5
        self.wait_time = 0.2

        self.utility_objects_map = {}
        self.utilities_by_category = {}

        self.lines_map = {}

        self.categories_data = [("A", 3, RED), ("B", 2, YELLOW), ("C", 4, PURPLE), ("D", 3, GREEN)]
        self.incompatible_utilities = {}

    def construct(self):
        for i, category_data in enumerate(self.categories_data):
            self.render_category(i, category_data[0], category_data[1], category_data[2])

        self.render_connections()
        self.simulate_process()

        self.incompatible_utilities["A1"] = ["B2", "C1"]
        self.incompatible_utilities["B2"] = ["D1", "D2"]
        self.simulate_process()

    def render_category(self, index: int, name: str, utilities_count: int, color: Color):
        category_surface = Rectangle(
            width=utilities_count * 2 * self.circle_radius + (utilities_count + 1) * self.spacing,
            height=2 * self.circle_radius + 2 * self.spacing)
        category_surface.set_stroke(WHITE, width=0)
        category_surface.set_fill(color, opacity=0.1)

        category_surface.set_x(self.left + category_surface.get_width() / 2)
        category_surface.set_y(self.top - (category_surface.get_height() + self.spacing) * index)

        category_label = Text(f'Category "{name}"', font_size=24)
        category_label.set_x(category_surface.get_left()[0] - category_label.get_width() / 2 - self.spacing)
        category_label.set_y(category_surface.get_y())

        self.play(ShowCreation(category_surface), Write(category_label))
        self.wait(self.wait_time)

        self.utilities_by_category[name] = []
        for i in range(utilities_count):
            self.render_utility(category_surface.get_bottom()[1], category_surface.get_left()[0], name, i)

    def render_utility(self, bottom, left, category, index):
        utility = Circle(radius=self.circle_radius)
        utility.set_stroke(WHITE, width=0)
        utility.set_fill(BLUE, opacity=0.5)
        utility.set_x(left + self.circle_radius * (2 * index + 1) + self.spacing * (index + 1))
        utility.set_y(bottom + self.circle_radius + self.spacing)

        utility_name = f'{category}{index + 1}'
        utility_label = Text(utility_name, font_size=16)
        utility_label.set_x(utility.get_x())
        utility_label.set_y(utility.get_y())

        self.utility_objects_map[utility_name] = VGroup(utility, utility_label)
        self.utilities_by_category[category].append(utility_name)
        self.play(ShowCreation(utility), Write(utility_label))

    def render_connections(self):
        for utility_name in self.utility_objects_map:
            self.lines_map[utility_name] = {}

        for i in range(len(self.categories_data) - 1):
            first_category_name = self.categories_data[i][0]
            second_category_name = self.categories_data[i + 1][0]

            for first_utility_name in self.utilities_by_category[first_category_name]:
                current_lines = []

                for second_utility_name in self.utilities_by_category[second_category_name]:
                    line = Line(self.utility_objects_map[first_utility_name].get_bottom() + (self.spacing / 4) * DOWN, self.utility_objects_map[second_utility_name].get_top() + (self.spacing / 4) * UP)
                    line.set_stroke(WHITE, width=2, opacity=0.4)

                    self.lines_map[first_utility_name][second_utility_name] = line
                    self.lines_map[second_utility_name][first_utility_name] = line
                    current_lines.append(line)

                self.play(*[ShowCreation(cl) for cl in current_lines])

    def simulate_process(self) -> None:
        utilities_to_ignore = dict()

        def simulate_process(category_index: int, prev_utility_name: str | None) -> None:
            if category_index > len(self.categories_data) - 1:
                return

            category_name = self.categories_data[category_index][0]
            for utility_name in self.utilities_by_category[category_name]:
                if utility_name in utilities_to_ignore and utilities_to_ignore[utility_name] > 0:
                    continue

                line = None

                if prev_utility_name:
                    line = self.lines_map[prev_utility_name][utility_name]

                    self.bring_to_front(line)
                    self.play(line.animate.set_stroke("#3bff00", width=3, opacity=1), run_time=0.1)
                    self.wait(0.2)

                if utility_name in self.incompatible_utilities:
                    for incompatible_utility_name in self.incompatible_utilities[utility_name]:
                        if incompatible_utility_name not in utilities_to_ignore:
                            utilities_to_ignore[incompatible_utility_name] = 0
                        utilities_to_ignore[incompatible_utility_name] += 1

                    self.hide_utilities(self.incompatible_utilities[utility_name], run_time=0.5)

                simulate_process(category_index + 1, utility_name)

                if utility_name in self.incompatible_utilities:
                    for incompatible_utility_name in self.incompatible_utilities[utility_name]:
                        utilities_to_ignore[incompatible_utility_name] -= 1

                    self.show_utilities(self.incompatible_utilities[utility_name], run_time=0.5)

                if prev_utility_name:
                    self.bring_to_back(line)
                    line.set_stroke(WHITE, width=2, opacity=0.4)

        simulate_process(0, None)

    def hide_utilities(self, utilities, **kwargs):
        fade_out_animations = []

        for utility_name in utilities:
            fade_out_animations.append(FadeOut(self.utility_objects_map[utility_name]))
            for line in self.lines_map[utility_name].values():
                fade_out_animations.append(FadeOut(line))

        self.play(*fade_out_animations, **kwargs)

    def show_utilities(self, utilities, **kwargs):
        fade_in_animations = []

        for utility_name in utilities:
            fade_in_animations.append(FadeIn(self.utility_objects_map[utility_name]))
            for line in self.lines_map[utility_name].values():
                fade_in_animations.append(FadeIn(line))

        self.play(*fade_in_animations, **kwargs)