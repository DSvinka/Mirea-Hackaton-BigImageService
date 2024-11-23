export const rules = {
  name(value) {
    if (value?.length >= 2) return true

    return 'Имя должно содержать больше 2 символов.'
  },
  phone(value) {
    if (/^[0-9-]{12,}$/.test(value)) return true

    return 'Номер телефона должен содержать не менее 12 чисел.'
  },
  email(value) {
    if (/^[a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true

    return 'Некорректный Email.'
  },
  select(value) {
    if (value) return true

    return 'Выберите один элемент.'
  },
  password(value) {
    if (value) return true
    return false;
  }
}
