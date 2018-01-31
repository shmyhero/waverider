
class BackTestHelper(object):

    @staticmethod
    def get_max_draw_down(return_values):
        max_value = 0
        max_draw_down = 0
        for value in return_values:
            if value > max_value:
                max_value = value
            else:
                draw_down = (max_value - value)/max_value
                if draw_down > max_draw_down:
                    max_draw_down = draw_down
        return max_draw_down


if __name__ == '__main__':
    print BackTestHelper.get_max_draw_down([1, 2.3, 0.5, 2, 5, 1, 9])