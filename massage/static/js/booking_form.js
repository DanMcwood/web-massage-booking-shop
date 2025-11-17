document.addEventListener('DOMContentLoaded', function () {
  const timeField = document.querySelector('input[name="time"]');
  if (timeField) {
    timeField.setAttribute('type', 'time');
    timeField.setAttribute('min', '09:00');
    timeField.setAttribute('max', '19:00');
    timeField.setAttribute('step', '1800'); // шаг 30 мин
  }
});
