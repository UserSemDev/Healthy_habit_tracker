from rest_framework import serializers
from rest_framework.exceptions import ValidationError


def time_limit(value):
    """Функция валидации времени выполнения привычки"""
    if value > 120:
        raise serializers.ValidationError('Время выполнения привычки должно быть не более 120 секунд!')
    if value == 0:
        raise serializers.ValidationError('Время выполнения привычки не может равняться нулю!')


def periodicity_limit(value):
    """Функция валидации максимальной периодичности привычки"""
    if int(value) > 7:
        raise serializers.ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней!')
    if int(value) <= 0:
        raise serializers.ValidationError('Периодичность выполнения не может быть меньше или равна нулю!')


class HabitValidator:
    """Валидатор привычки"""

    def __init__(self, is_nice_habit, related_habit, reward):
        self.is_nice_habit = is_nice_habit
        self.related_habit = related_habit
        self.reward = reward

    def __call__(self, value):
        is_nice_habit = value.get(self.is_nice_habit)
        related_habit = value.get(self.related_habit)
        reward = value.get(self.reward)

        if related_habit and reward:
            raise ValidationError('Нельзя одновременно выбрать связанную привычку и вознаграждение')

        if related_habit and not is_nice_habit:
            raise ValidationError('В связанные привычки могут попадать только привычки с признаком приятной привычки')

        if is_nice_habit and (related_habit or reward):
            raise ValidationError('У приятной привычки не может быть связанной привычки или вознаграждения')

        if not (is_nice_habit, reward):
            raise ValidationError('У полезной привычки необходимо указать приятную привычку или вознаграждение')
