$(document).ready(function() {
    $('#getWeather').click(function() {
        const city = $('input[name="city"]').val();
        if (city.trim()) {
            $.ajax({
                url: '/get_weather/',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ city }),
                success: function(response) {
                    const weatherResult = $('#weatherResult');
                    weatherResult.empty(); // Очистка предыдущих данных
                    const htmlContent = `
                        <h2 class="weather-title">Погода в городе ${response.name}</h2>
                        <p class="weather-info"><strong>Температура:</strong> ${response.main.temp}°C (ощущается как ${response.main.feels_like}°C)</p>
                        <p class="weather-info"><strong>Максимальная температура:</strong> ${response.main.temp_max}°C</p>
                        <p class="weather-info"><strong>Минимальная температура:</strong> ${response.main.temp_min}°C</p>
                        <p class="weather-info"><strong>Давление:</strong> ${response.main.pressure} гПа</p>
                        <p class="weather-info"><strong>Влажность:</strong> ${response.main.humidity}%</p>
                        <p class="weather-info"><strong>Облачность:</strong> ${response.clouds.all}% (${response.weather[0].description})</p>
                        <p class="weather-info"><strong>Скорость ветра:</strong> ${response.wind.speed} м/с (направление: ${response.wind.deg}°)</p>
                        <p class="weather-info"><strong>Видимость:</strong> ${response.visibility} метров</p>
                    `;
                    weatherResult.append(htmlContent);
                },
                error: function() {
                    alert('Не удалось получить данные о погоде.');
                }
            });
        } else {
            alert('Пожалуйста, введите название города.');
        }
    });

    $('#viewHistory').click(function() {
        $.ajax({
            url: '/show_history/',
            method: 'GET',
            contentType: 'application/json',
            success: function(response) {
                const weatherResult = $('#weatherResult');
                weatherResult.empty();
                
                let htmlContent = '<h2 class="weather-title">История запросов</h2>';
                
                response.forEach(function(item) {
                    htmlContent += `
                        <p class="weather-info">${item.city}, ${item.date_time}, ${item.temp}°C, ${item.description}</p>
                    `;
                });
                
                weatherResult.append(htmlContent);
            },
            error: function() {
                alert('Не удалось получить данные о погоде.');
            }
        });
    });
});

        