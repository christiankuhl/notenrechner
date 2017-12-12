#!/usr/bin/env python3

import toga

def build(app):
    number_box = toga.Box()
    f_box = toga.Box()
    box = toga.Box()




    c_input = toga.TextInput(readonly=True)
    f_input = toga.TextInput()

    c_label = toga.Label('Celsius', alignment=toga.LEFT_ALIGNED)
    f_label = toga.Label('Fahrenheit', alignment=toga.LEFT_ALIGNED)
    join_label = toga.Label('is equivalent to', alignment=toga.RIGHT_ALIGNED)

    def calculate(widget):
        try:
            c_input.value = (float(f_input.value) - 32.0) * 5.0 / 9.0
        except:
            c_input.value = '???'

    button = toga.Button('Calculate', on_press=calculate)

    f_box.add(f_input)
    f_box.add(f_label)

    c_box.add(join_label)
    c_box.add(c_input)
    c_box.add(c_label)

    box.add(f_box)
    box.add(c_box)
    box.add(button)

    box.style.set(flex_direction='column', padding_top=10)
    f_box.style.set(flex_direction='row', margin=5)
    c_box.style.set(flex_direction='row', margin=5)

    c_input.style.set(flex=1)
    f_input.style.set(flex=1, margin_left=160)
    c_label.style.set(width=100, margin_left=10)
    f_label.style.set(width=100, margin_left=10)
    join_label.style.set(width=150, margin_right=10)

    button.style.set(margin=15)

    return box


def main():
    return toga.App('Notenrechner', 'org.musicofreason.notenrechner', startup=build)
#
#
# import toga
# from colosseum import CSS
#
#
# class Graze(toga.App):
#     def startup(self):
#         self.main_window = toga.MainWindow(self.name)
#         self.main_window.app = self
#
#         self.webview = toga.WebView(style=CSS(flex=1))
#         self.url_input = toga.TextInput(
#             initial='https://github.com/',
#             style=CSS(flex=1, margin=5)
#         )
#
#         box = toga.Box(
#             children = [
#                 toga.Box(
#                     children = [
#                         self.url_input,
#                         toga.Button('Go', on_press=self.load_page, style=CSS(width=50)),
#                     ],
#                     style=CSS(
#                         flex_direction='row'
#                     )
#                 ),
#                 self.webview,
#             ],
#             style=CSS(
#                 flex_direction='column'
#             )
#         )
#
#         self.main_window.content = box
#         self.webview.url = self.url_input.value
#
#         # Show the main window
#         self.main_window.show()
#
#     def load_page(self, widget):
#         self.webview.url = self.url_input.value
#
# def main():
#     return Graze('Graze', 'org.pybee.graze')


if __name__ == '__main__':
    main().main_loop()
