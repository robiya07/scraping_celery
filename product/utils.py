from product.models import ScheduleModel


def clock_file():
    schedule = ScheduleModel.objects.all()
    with open("clock.csv", "w") as file:
        file.write("id, hour, minute\n")
        for i, v in enumerate(schedule):
            file.write(
                f"{i}, {v.time.hour}, {v.time.minute}\n")
