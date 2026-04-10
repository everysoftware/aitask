import uuid
from typing import Any

import matplotlib.pyplot as plt
from matplotlib import patches

from wilde.stats.config import stats_settings
from wilde.tasks.constants import TEST_STATUSES


def paint_pie_plot(stats: dict[Any, int], *, title: str = "Total tasks: {count}") -> str:
    # Разделяем классы и их количество для построения графика
    class_names = [TEST_STATUSES[status]["text"] for status in stats]
    class_values = list(stats.values())

    # Получаем цвета
    colors = [TEST_STATUSES[status]["color"] for status in stats]

    # Строим круговую диаграмму
    plt.figure()
    my_circle = patches.Circle((0, 0), 0.8, color="white")
    plt.pie(class_values, labels=class_names, autopct="%.0f%%", colors=colors)

    p = plt.gcf()
    p.gca().add_artist(my_circle)
    plt.title(title.format(count=sum(class_values)))
    pie_path = f"{stats_settings.stats_dir}/pie_{uuid.uuid4().hex}.png"
    plt.savefig(pie_path)
    plt.close()

    return pie_path
