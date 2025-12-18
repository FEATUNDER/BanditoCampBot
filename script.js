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
        const priceSpan = product.querySelector('.price span');
        priceSpan.textContent = totalPrice;
        
        // Помечаем товар как выбранный (добавляем атрибут)
        document.querySelectorAll('.product').forEach(p => {
            p.removeAttribute('data-selected');
        });
        product.setAttribute('data-selected', 'true');
    });
});

// Эта часть отвечает за отправку данных в Telegram бота
document.getElementById('submitBtn').addEventListener('click', function() {
    const contactInfo = document.getElementById('contactInput').value.trim();

    if (!contactInfo) {
        alert('Пожалуйста, введите ваш @username или номер телефона.');
        return;
    }

    // Ищем товар, у которого выбран размер (имеет data-selected="true")
    const activeProduct = document.querySelector('.product[data-selected="true"]');
    
    if (!activeProduct) {
        alert('Пожалуйста, выберите размер товара, кликнув на один из вариантов размера.');
        return;
    }

    const itemName = activeProduct.dataset.item;
    const selectedSize = activeProduct.querySelector('.size-btn.active').dataset.size;
    const finalPrice = activeProduct.querySelector('.price span').textContent;

    // Формируем объект с данными заказа
    const orderData = {
        item: itemName,
        size: selectedSize,
        price: finalPrice + '₽',
        contact: contactInfo,
        user_id: window.Telegram.WebApp.initDataUnsafe.user?.id
    };

    console.log("Отправляемые данные:", orderData); // Для отладки в консоли браузера
    
    // Отправляем данные обратно в бота
    window.Telegram.WebApp.sendData(JSON.stringify(orderData));
    
    // Показываем пользователю, что данные отправляются
    this.textContent = "Отправляется...";
    this.disabled = true;
    
    // Закрываем веб-приложение через небольшую задержку
    setTimeout(() => {
        window.Telegram.WebApp.close();
    }, 500);
});
