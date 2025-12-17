// Эта часть отвечает за пересчет цены при выборе размера
document.querySelectorAll('.size-btn').forEach(button => {
    button.addEventListener('click', function() {
        // Убираем активный класс у всех кнопок в этой группе
        this.parentElement.querySelectorAll('.size-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        // Добавляем активный класс нажатой кнопке
        this.classList.add('active');

        // Находим родительский элемент товара
        const product = this.closest('.product');
        const basePrice = parseInt(product.dataset.basePrice);
        const priceMod = parseInt(this.dataset.priceMod);
        const totalPrice = basePrice + priceMod;

        // Обновляем отображение цены для этого товара
        // (находим span с ценой внутри того же product)
        const priceSpan = product.querySelector('.price span');
        priceSpan.textContent = totalPrice;
    });
});

// Эта часть отвечает за отправку данных в Telegram бота
document.getElementById('submitBtn').addEventListener('click', function() {
    const contactInfo = document.getElementById('contactInput').value.trim();

    if (!contactInfo) {
        alert('Пожалуйста, введите ваш @username или номер телефона.');
        return;
    }

    // Собираем данные выбранного товара (берем первый, для примера логики)
    const activeProduct = document.querySelector('.product');
    const itemName = activeProduct.dataset.item;
    const selectedSize = activeProduct.querySelector('.size-btn.active').dataset.size;
    const finalPrice = activeProduct.querySelector('.price span').textContent;

    // Формируем объект с данными заказа
    const orderData = {
        item: itemName,
        size: selectedSize,
        price: finalPrice + '₽',
        contact: contactInfo,
        user_id: window.Telegram.WebApp.initDataUnsafe.user?.id // ID пользователя в Telegram (если доступен)
    };

    // Отправляем данные обратно в бота
    // Telegram.WebApp.sendData() – это специальная функция, которая передает строку в родительского бота
    window.Telegram.WebApp.sendData(JSON.stringify(orderData));

    // Закрываем веб-приложение
    window.Telegram.WebApp.close();
});