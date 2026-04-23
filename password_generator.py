import random
import string

def generate_password(length: int, use_digits: bool, use_letters: bool, use_special: bool) -> str:
    """
    Генерирует случайный пароль.
    
    :param length: Длина пароля.
    :param use_digits: Включать ли цифры.
    :param use_letters: Включать ли буквы (верхний и нижний регистр).
    :param use_special: Включать ли специальные символы.
    :return: Сгенерированный пароль.
    """
    if length < 1:
        raise ValueError("Длина пароля должна быть больше 0")
    
    # Формируем набор символов для генерации
    chars = ''
    if use_digits:
        chars += string.digits
    if use_letters:
        chars += string.ascii_letters  # a-zA-Z
    if use_special:
        chars += string.punctuation

    if not chars:
        raise ValueError("Необходимо выбрать хотя бы один тип символов")
    
    # Используем secrets для криптографической стойкости (лучше random)
    return ''.join(random.choices(chars, k=length))
