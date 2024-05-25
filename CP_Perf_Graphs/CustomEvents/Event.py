import CustomEvents.Observer as Observer


class Event:
    def __init__(self, event_name, data=None):
        self.event_name = event_name
        self.data = data
        # Вызов callback для этого события
        # или просто регистрация наступления события
        self._run_action()

    def _run_action(self):
        # Обращаемся к списку всех наблюдателей
        for observer in Observer.Observer.observers:
            # Получаем статус события
            # Или None если наблюдатель не отслеживает это событие
            status = observer.observable_events.get(
                self.event_name + "_status",
                None
            )
            if status:
                # Изменяем статус события, т.к. оно произошло
                observer.observable_events[self.event_name + "_status"] = True
                # Выясняем есть связанные события
                relatives = observer.observable_events.get(
                    self.event_name + "_relative",
                    None
                )
                # Если связанные события есть смотрим их статус
                if relatives:
                    if Event._check_relatives_status(observer, relatives):
                        self._choose_callback(observer)
                else:
                    self._choose_callback(observer)

    @staticmethod
    def _check_relatives_status(observer, relatives):
        relatives_stat = True
        # Если хотя бы одно связанное событие не состоялось, то общий статус False
        for relative in relatives:
            if not observer.observable_events[relative + "_status"]:
                relatives_stat = False
                break
        return relatives_stat

    def _choose_callback(self, observer):
        if self.data:
            observer.observable_events.get(self.event_name)(self.data)
        else:
            observer.observable_events.get(self.event_name)()
