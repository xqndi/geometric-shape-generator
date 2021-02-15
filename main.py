#   ////////////////////////////////////////////////////////////////////////////////////////////////////
from graphics import *
from fpdf import FPDF
from random import randint
from random import choice
from PIL import Image
from PIL import EpsImagePlugin
import os

#   ////////////////////////////////////////////////////////////////////////////////////////////////////
WINDOW_WIDTH = 240
WINDOW_HEIGHT = 720
EXTENDED_WINDOW_HEIGHT = WINDOW_HEIGHT + 240

X_CENTER = int(WINDOW_WIDTH / 2)
Y_CENTER = int(WINDOW_HEIGHT / 2)

CONFIG_DICT = {}


#   ////////////////////////////////////////////////////////////////////////////////////////////////////
#  /////////--------------------------------------MAIN----------------------------------------/////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////
def main():
    EpsImagePlugin.gs_windows_binary = r'C:\Program Files (x86)\gs\gs9.53.3\bin\gswin32c.exe'

    colors_list_1 = [
        "black", "darkgrey", "darkslategray", "dimgrey", "gray", "ivory", "lightsteelblue",
        "midnightblue", "teal", "slateblue", "slategray"
    ]
    colors_list_2 = [
        "black", "darkgrey", "darkslategray", "dimgrey", "gray",  "slategray", "midnightblue"
    ]
    colors_list_3 = [
        "black"
    ]

    pdf = FPDF()
    nr_gens = get_user_input()
    for gen_index in range(nr_gens):
        pdf.add_page()
        create_image(colors_list_1, colors_list_2, colors_list_3, gen_index)
        pdf.image("shape" + str(gen_index) + ".png", 76, 25, 60, 250)

    pdf.output("geometric_shapes.pdf", "F")

    for gen_index in range(nr_gens):
        eps_path = r"C:\Users\Alexander\Documents\GitHub\geometric-shape-generator\image"\
                   + str(gen_index) + ".eps"
        png_path = r"C:\Users\Alexander\Documents\GitHub\geometric-shape-generator\shape"\
                   + str(gen_index) + ".png"
        os.remove(eps_path)
        os.remove(png_path)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////
def create_image(c1, c2, c3, index):
    win = GraphWin("shapes", WINDOW_WIDTH, EXTENDED_WINDOW_HEIGHT)
    win.setBackground("aliceblue")
    init_config_dict()

    if CONFIG_DICT["color_list"] == 1:
        colors = c1
    elif CONFIG_DICT["color_list"] == 2:
        colors = c2
    else:
        colors = c3

    for iteration in range(CONFIG_DICT["nr_iterations"]):
        generate_shape(win, colors)

    print_config_data(win)

    eps_name = "image" + str(index) + ".eps"
    png_name = "shape" + str(index) + ".png"
    win.postscript(file=eps_name, colormode='color',
                   height=EXTENDED_WINDOW_HEIGHT, width=WINDOW_WIDTH)
    img = Image.open(eps_name)
    img.load(scale=4)
    img.save(png_name)
    win.close()


# ///////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////
def init_config_dict():
    CONFIG_DICT["nr_iterations"] = randint(5, 38)
    CONFIG_DICT["color_list"] = randint(1, 3)
    if not randint(0, 10):
        CONFIG_DICT["fill_probability"] = -1
    else:
        CONFIG_DICT["fill_probability"] = randint(10, 100)

    if not randint(0, 8):
        CONFIG_DICT["polygon_max_vertices"] = 3
    else:
        CONFIG_DICT["polygon_max_vertices"] = randint(3, 11)

    if randint(0, 20):
        CONFIG_DICT["circle_threshold"] = randint(0, 45)
        CONFIG_DICT["oval_threshold"] = randint(CONFIG_DICT["circle_threshold"] + 1, 65)
        CONFIG_DICT["line_threshold"] = randint(CONFIG_DICT["oval_threshold"] + 1, 95)
        CONFIG_DICT["polygon_threshold"] = 100
    # special case: only lines and triangles
    else:
        CONFIG_DICT["circle_threshold"] = 0
        CONFIG_DICT["oval_threshold"] = 0

        CONFIG_DICT["line_threshold"] = randint(30, 60)
        CONFIG_DICT["polygon_threshold"] = 100

        CONFIG_DICT["nr_iterations"] -= 5
        CONFIG_DICT["polygon_max_vertices"] = 3

    CONFIG_DICT["line_duplicate_prob"] = randint(0, 50)
    print(CONFIG_DICT)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////
def print_config_data(graph_win):
    # rectangle as background for text
    rect = Rectangle(Point(0, WINDOW_HEIGHT + 15),
                     Point(WINDOW_WIDTH, EXTENDED_WINDOW_HEIGHT))
    rect.setFill("aliceblue")
    rect.draw(graph_win)
    y_pos = WINDOW_HEIGHT + 28
    for key, value in CONFIG_DICT.items():
        data_string = key + ": " + str(value)

        text = Text(Point(118, y_pos), data_string)
        text.setSize(14)
        text.draw(graph_win)
        text.setStyle("italic")

        y_pos += 25


# ///////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////
def color_object(graph_object, colors_list):
    if CONFIG_DICT["fill_probability"] >= randint(0, 100):
        color = choice(colors_list)
        graph_object.setFill(color)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////
def generate_shape(graph_win, colors_list):
    rand_choice = randint(1, 100)
    if rand_choice <= CONFIG_DICT["circle_threshold"]:
        generate_circle(graph_win, colors_list)
        return
    if rand_choice <= CONFIG_DICT["oval_threshold"]:
        generate_oval(graph_win, colors_list)
        return
    if rand_choice <= CONFIG_DICT["line_threshold"]:
        generate_line(graph_win)
        return
    if rand_choice <= CONFIG_DICT["polygon_threshold"]:
        generate_polygon(graph_win, colors_list)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////
def generate_polygon(graph_win, colors_list):
    nr_points = randint(3, CONFIG_DICT["polygon_max_vertices"])

    if nr_points % 2 == 0:
        polygon = generate_even_polygon(nr_points)
        color_object(polygon, colors_list)
        polygon.draw(graph_win)
        return

    else:
        polygon = generate_odd_polygon(nr_points)
        color_object(polygon, colors_list)
        polygon.draw(graph_win)
        return


# ///////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////
def generate_even_polygon(nr_points):
    all_points_list = []
    right_point_list = []
    left_points_list = []

    height_factor = (12 - nr_points) * 10

    starting_point = Point(X_CENTER, randint(0, int(Y_CENTER * 1.5)))
    y_height = starting_point.getY()
    all_points_list.append(starting_point)
    # subtract start- and endpoint
    nr_points -= 2
    for it in range(int(nr_points / 2)):
        y_height += randint(10, height_factor)
        y_pos = y_height
        left_x_pos = randint(30, X_CENTER - 20)
        right_x_pos = WINDOW_WIDTH - left_x_pos

        left_points_list.append(Point(left_x_pos, y_pos))
        right_point_list.append(Point(right_x_pos, y_pos))

    left_points_list.reverse()
    y_height += randint(10, height_factor)
    last_point = Point(X_CENTER, y_height)
    all_points_list.extend(right_point_list)
    all_points_list.append(last_point)
    all_points_list.extend(left_points_list)

    polygon = Polygon(all_points_list)
    return polygon


# ///////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////
def generate_odd_polygon(nr_points):
    all_points_list = []
    right_point_list = []
    left_points_list = []

    height_factor = (12 - nr_points) * 10

    bottom_open = False
    if randint(0, 1):
        bottom_open = True

    print(nr_points)
    if bottom_open:
        starting_point = Point(X_CENTER, randint(0, int(Y_CENTER * 1.5)))
        y_height = starting_point.getY()
        all_points_list.append(starting_point)
    else:
        y_height = randint(0, int(Y_CENTER * 1.5))
    # subtract start- or end-point
    nr_points -= 1
    for it in range(int(nr_points / 2)):
        y_height += randint(10, height_factor)
        y_pos = y_height
        left_x_pos = randint(30, X_CENTER - 20)
        right_x_pos = WINDOW_WIDTH - left_x_pos

        left_points_list.append(Point(left_x_pos, y_pos))
        right_point_list.append(Point(right_x_pos, y_pos))

    all_points_list.extend(right_point_list)

    if not bottom_open:
        y_height += randint(10, height_factor)
        last_point = Point(X_CENTER, y_height)
        all_points_list.append(last_point)

    left_points_list.reverse()
    all_points_list.extend(left_points_list)

    polygon = Polygon(all_points_list)
    return polygon


# ///////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////
def generate_circle(graph_win, colors_list):
    rad = randint(10, 50)
    circle = Circle(Point(X_CENTER, randint(0, WINDOW_HEIGHT)), rad)
    color_object(circle, colors_list)
    circle.draw(graph_win)

    if randint(0, 10):
        return

    # else draw orbit around circle
    x1 = circle.getP1().getX() - int(rad * (1/3))
    x2 = circle.getP2().getX() + int(rad * (1/3))
    y1 = circle.getP1().getY()
    y2 = circle.getP2().getY() - int(rad * 0.7)

    oval = Oval(Point(x1, y1), Point(x2, y2))
    oval.draw(graph_win)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////
def generate_oval(graph_win, colors_list):
    min_x_dist = int(WINDOW_WIDTH / 8)

    left_x_pos = randint(min_x_dist, X_CENTER)
    right_x_pos = (2 * X_CENTER) - left_x_pos
    left_y_pos = randint(0, WINDOW_HEIGHT)
    y_dist = left_x_pos
    right_y_pos = left_y_pos + y_dist

    oval = Oval(Point(left_x_pos, left_y_pos), Point(right_x_pos, right_y_pos))

    color_object(oval, colors_list)
    oval.draw(graph_win)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////
def generate_line(graph_win):
    random_choice = randint(1, 10)
    # vertical line
    if 0 < random_choice <= 4:
        first_y_boundary = WINDOW_HEIGHT - int(WINDOW_HEIGHT / 3)
        lower_y_pos = randint(0, first_y_boundary)
        second_y_boundary = lower_y_pos + int(WINDOW_HEIGHT / 3)
        upper_y_pos = randint(second_y_boundary, WINDOW_HEIGHT)

        line = Line(Point(X_CENTER, lower_y_pos), Point(X_CENTER, upper_y_pos))
        line.draw(graph_win)
        return

    # horizontal line
    if 4 < random_choice <= 8:
        first_y_pos = randint(0, WINDOW_HEIGHT)
        min_x_dist = int(WINDOW_WIDTH / 6)
        first_x_pos = randint(min_x_dist, X_CENTER)
        second_x_pos = (2 * X_CENTER) - first_x_pos
        second_y_pos = first_y_pos

        line = Line(Point(first_x_pos, first_y_pos), Point(second_x_pos, second_y_pos))
        line.draw(graph_win)

    else:
        first_y_boundary = WINDOW_HEIGHT - int(WINDOW_HEIGHT / 3)
        second_y_pos = randint(0, first_y_boundary)
        first_y_pos = randint(second_y_pos, second_y_pos + 175)
        if randint(0, 1):
            second_x_pos = randint(X_CENTER - 115, X_CENTER + 115)
            first_x_pos = X_CENTER
        else:
            second_x_pos = X_CENTER
            first_x_pos = randint(X_CENTER - 115, X_CENTER + 115)

        line = Line(Point(second_x_pos, second_y_pos), Point(first_x_pos, first_y_pos))
        line.draw(graph_win)

    line_offset = randint(5, 25)

    higher_first_y = first_y_pos + line_offset
    higher_second_y = second_y_pos + line_offset
    lower_first_y = first_y_pos - line_offset
    lower_second_y = second_y_pos - line_offset

    while CONFIG_DICT["line_duplicate_prob"] >= randint(1, 100):
        higher_first_y += line_offset
        higher_second_y += line_offset
        lower_first_y -= line_offset
        lower_second_y -= line_offset

        line = Line(Point(second_x_pos, higher_second_y), Point(first_x_pos, higher_first_y))
        line.draw(graph_win)
        line = Line(Point(second_x_pos, lower_second_y), Point(first_x_pos, lower_first_y))
        line.draw(graph_win)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////
def get_user_input():
    valid_input = False
    nr_iter = -1
    while not valid_input:
        print("Enter number of pictures to be generated (1 <= size <= 100):")
        nr_iter = input()
        if nr_iter.isnumeric() and 1 <= int(nr_iter) <= 100:
            valid_input = True
        else:
            print("INVALID INPUT....try again :/")

    return int(nr_iter)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    main()
