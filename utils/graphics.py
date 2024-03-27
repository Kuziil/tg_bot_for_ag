import io

from matplotlib import pyplot as plt


def create_graphics_for_pages():
    days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт']
    customer_calls = [20, 30, 25, 35, 40]

    with plt.style.context('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle'):
        plt.plot(days, customer_calls, marker='o')
        plt.title('Коли')
        plt.xlabel('День недели')
        plt.ylabel('Количество обращений')
        plt.grid(True)
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.clf()
    return buffer
