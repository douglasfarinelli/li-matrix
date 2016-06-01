# -*- coding: utf-8 -*-


class InterpreterError(Exception):
    pass


class Interpreter(object):
    """Simple Command Interpreter."""

    def __init__(self):
        self.current_matrix = None

    def do_I(self, x_axis, y_axis):
        """Example: I X N. X and N must be an integer."""
        self.current_matrix = Matrix(int(x_axis), int(y_axis))

    def do_L(self, x_axis, y_axis, color):
        """Example: L X Y C. X and N must be an integer. C must be a pixel value."""
        self.current_matrix.set_pixel(int(x_axis) - 1, int(y_axis) - 1, color)

    def do_V(self, x_axis, start_y, end_y, color):
        """Example: V X Y1 Y2 C."""
        self.current_matrix.draw_vertical_segment(
            x_axis=int(x_axis) - 1, start_y=int(start_y) - 1, end_y=int(end_y) - 1, value=color
        )

    def do_S(self, filename):
        """Example: S name"""
        self.current_matrix.save(filename)

    def execute_command(self, command):
        try:
            args = command.strip().split()
            cmd, args = args[0], args[1:]
            method = getattr(self, 'do_%s' % cmd)
        except (IndexError, AttributeError):
            return None

        if cmd != 'I' and self.current_matrix is None:
            raise InterpreterError('No matrix instance initialized. '
                                   'Start with the command I X Y.')

        method(*args)


class Matrix(object):
    """Simple Graphic Matrix."""

    def __init__(self, x_axis, y_axis, default_pixel=None):
        """
        :param x_axis:
            The number of rows (`int`).
        :param y_axis:
            The number of columns (`int`).
        :param default_pixel:
            Pixel default boot.
        """
        self.x_axis, self.y_axis = x_axis, y_axis
        self.default_pixel = str(default_pixel or 'O')
        self.data = self.init_data(x_axis, y_axis, self.default_pixel)

    def __str__(self):
        return '\n'.join(''.join(str(pixel) for pixel in row) for row in self)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx_row):
        return self.data[idx_row]

    @classmethod
    def init_data(cls, x_axis, y_axis, default_color):
        return [
            [default_color for _ in range(x_axis)] for _ in range(y_axis)
        ]

    def draw_vertical_segment(self, x_axis, start_y, end_y, value):
        """Draw vertical segment.

        :param x_axis:
            The column number (int).
        :param start_y:
            Start segment (int).
        :param end_y:
            End segment (int).
        :param value:
            The pixel value.
        """
        for y_axis in range(start_y, end_y):
            self.set_pixel(x_axis=x_axis, y_axis=y_axis, value=value)

    def set_pixel(self, x_axis, y_axis, value):
        """Defines a pixel X to Y.

        :param x_axis:
            The column number (int).
        :param y_axis:
            The row number (int).
        :param value:
            The pixel value.
        """
        self[y_axis][x_axis] = str(value)

    def save(self, filename):
        """Save the matrix as file."""
        with open(filename, 'w') as f:
            f.write(str(self))
