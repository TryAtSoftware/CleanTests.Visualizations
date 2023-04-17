from manimlib import *


class UtilitiesInCategories(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spacing = 0.1
        self.circle_radius = 0.3
        self.top = 3
        self.left = -2
        self.wait_time = 0.2

        self.utility_objects_map = {}
        self.utilities_by_category = {}

        self.lines_map = {}

        self.categories_data = [("A", 3, RED), ("B", 2, YELLOW), ("C", 4, PURPLE), ("D", 3, GREEN)]

    def construct(self):
        for i, category_data in enumerate(self.categories_data):
            self.render_category(i, category_data[0], category_data[1], category_data[2])

        self.render_connections()
        self.simulate_process(0, None)

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
        for i in range(len(self.categories_data) - 1):
            first_category_name = self.categories_data[i][0]
            second_category_name = self.categories_data[i + 1][0]

            for first_utility_name in self.utilities_by_category[first_category_name]:
                self.lines_map[first_utility_name] = {}
                current_lines = []

                for second_utility_name in self.utilities_by_category[second_category_name]:
                    line = Line(self.utility_objects_map[first_utility_name].get_bottom() + (self.spacing / 4) * DOWN, self.utility_objects_map[second_utility_name].get_top() + (self.spacing / 4) * UP)
                    line.set_stroke(WHITE, width=2, opacity=0.4)

                    self.lines_map[first_utility_name][second_utility_name] = line
                    current_lines.append(line)

                self.play(*[ShowCreation(cl) for cl in current_lines])

    def simulate_process(self, category_index: int, prev_utility_name: str | None) -> None:
        if category_index > len(self.categories_data) - 1:
            return

        category_name = self.categories_data[category_index][0]
        for utility_name in self.utilities_by_category[category_name]:
            line = None

            if prev_utility_name:
                line = self.lines_map[prev_utility_name][utility_name]

                self.bring_to_front(line)
                self.play(line.animate.set_stroke("#3bff00", width=3, opacity=1), run_time=0.1)
                self.wait(0.2)

            self.simulate_process(category_index + 1, utility_name)

            if prev_utility_name:
                self.bring_to_back(line)
                line.set_stroke(WHITE, width=2, opacity=0.4)
