class Observer:
    # Лист всех наблюдателей
    observers = []

    def __init__(self, *event_names: str,
                 callback=None,
                 obj=None):
        # Сохраняем ссылку на объект наблюдатель
        self.obj = obj
        # Словарь отслеживаемых событий
        self.observable_events = {}
        Observer.observers.append(self)
        self._add_listen_events(*event_names, callback=callback)

    # Метод для добавления событий и реакции/функции на них
    def _add_listen_events(self, *event_names: str, callback=None):
        for event_id, event in enumerate(event_names):
            # само событие и связанная с ним функция
            self.observable_events[event] = callback
            # статус события случилось или нет
            self.observable_events[event + "_status"] = False
            # связанные события
            if len(event_names) > 1:
                self.observable_events[event + "_relative"] = event_names[event_id+1:] + event_names[:event_id]
