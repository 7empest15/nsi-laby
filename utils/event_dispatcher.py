import pygame

class EventDispatcher:
    def __init__(self):
        self.subscribers = []
        self.keydown_subscribers = {}

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def unsubscribe(self, callback):
        self.subscribers.remove(callback)

    def subscribe_keydown(self, key, callback):
        if key not in self.keydown_subscribers:
            self.keydown_subscribers[key] = []
        self.keydown_subscribers[key].append(callback)

    def unsubscribe_keydown(self, key, callback):
        if key in self.keydown_subscribers:
            self.keydown_subscribers[key].remove(callback)
            if not self.keydown_subscribers[key]:
                del self.keydown_subscribers[key]

    def dispatch(self, event):
        for subscriber in self.subscribers:
            subscriber(event)
        if event.type == pygame.KEYDOWN:
            if event.key in self.keydown_subscribers:
                for callback in self.keydown_subscribers[event.key]:
                    callback(event)

dispatcher = EventDispatcher()