import pytest
import re
import asyncio

from pages.chat_page import ChatPage

BASE_URL = "https://autofaq.ai/"

@pytest.mark.asyncio
async def test_open_chat_widget(page):
    """Открытие виджета чата"""
    await page.goto(BASE_URL)
    chat = ChatPage(page)
    await chat.open_chat()
    assert await page.is_visible(chat.chat_area_selector), "Виджет чата должен быть виден после открытия"

@pytest.mark.asyncio
async def test_close_chat_widget(page):
    """Закрытие виджета чата"""
    await page.goto(BASE_URL)
    chat = ChatPage(page)
    await chat.open_chat()
    await chat.close_chat()
    assert not await page.is_visible(chat.chat_area_selector), "Виджет чата должен быть скрыт после закрытия"

@pytest.mark.asyncio
async def test_chat_input_presence(page):
    """Проверка инпута в чате"""
    await page.goto(BASE_URL)
    chat = ChatPage(page)
    await chat.open_chat()
    assert await page.is_visible(chat.chat_input_selector), "Инпут чата должен присутствовать и быть видимым"

@pytest.mark.asyncio
async def test_send_and_display_message(page):
    """Проверка отправки и отображения сообщения в чате"""
    await page.goto(BASE_URL)
    chat = ChatPage(page)
    await chat.open_chat()
    message = "Привет, тест!"
    await chat.fill_chat_input(message)
    await chat.click_send()
    await page.wait_for_selector(chat.chat_area_message_sent_selector)
    sent_message = await chat.get_last_message()
    assert message in await sent_message.text_content(), f"Отправленное сообщение должно содержать '{message}'"

@pytest.mark.asyncio
async def test_ai_response_display(page):
    """Проверка ответа и отображения от ИИ в чате"""
    await page.goto(BASE_URL)
    chat = ChatPage(page)
    await chat.open_chat()
    message = "Привет, ИИ!"
    await chat.fill_chat_input(message)
    await chat.click_send()
    await page.wait_for_selector(chat.chat_area_message_receive_selector)
    ai_message = await chat.get_last_received_message()
    assert "Ответ от ИИ" in await ai_message.text_content(), "Ответ ИИ должен содержать 'Ответ от ИИ'"

@pytest.mark.asyncio
async def test_attachment_functionality(page):
    """Проверка прикрепления вложений"""
    await page.goto(BASE_URL)
    chat = ChatPage(page)
    await chat.open_chat()
    async with page.expect_file_chooser() as fc_info:
        await chat.click_attachment()
    file_chooser = await fc_info.value
    assert file_chooser is not None, "При нажатии на кнопку вложения должен открываться диалог выбора файла"

@pytest.mark.asyncio
async def test_send_and_display_attachment(page, tmp_path):
    """Проверка отправки и отображения вложений"""
    await page.goto(BASE_URL)
    chat = ChatPage(page)
    await chat.open_chat()
    file_path = tmp_path / "test.txt"
    file_path.write_text("Тестовый файл")
    async with page.expect_file_chooser() as fc_info:
        await chat.click_attachment()
    file_chooser = await fc_info.value
    await file_chooser.set_files(str(file_path))
    attachment_selector = "css=div.msg_sent >> text=Тестовый файл"
    await page.wait_for_selector(attachment_selector)
    attachment_text = await page.text_content(attachment_selector)
    assert "Тестовый файл" in attachment_text, "Вложение должно отображаться в чате после отправки"

@pytest.mark.asyncio
async def test_functional_buttons_in_chat_input(page):
    """Проверка функциональных кнопок в инпуте чата"""
    await page.goto(BASE_URL)
    chat = ChatPage(page)
    await chat.open_chat()
    attachment_visible = await page.is_visible(chat.chat_panel_attachment_button_selector)
    emoji_visible = await page.is_visible(chat.chat_panel_emoji_button_selector)
    assert attachment_visible, "Кнопка вложения должна быть видна в инпуте чата"
    assert emoji_visible, "Кнопка эмодзи должна быть видна в инпуте чата"

@pytest.mark.asyncio
async def test_open_emoji_window(page):
    """Открытие окна эмодзи"""
    await page.goto(BASE_URL)
    chat = ChatPage(page)
    await chat.open_chat()
    await chat.click_emoji()
    assert await page.is_visible(chat.emoji_panel_selector), "Панель эмодзи должна быть видна после нажатия на кнопку эмодзи"

@pytest.mark.asyncio
async def test_chat_message_date_format(page):
    """Проверка корректности даты в чате с разными часовыми поясами"""
    await page.goto(BASE_URL)
    chat = ChatPage(page)
    await chat.open_chat()
    message = "Проверка времени"
    await chat.fill_chat_input(message)
    await chat.click_send()
    await page.wait_for_selector(chat.chat_area_message_time_selector)
    message_time = await chat.get_message_time()
    assert re.match(r"\d{1,2}:\d{2}(:\d{2})?", message_time), f"Формат времени некорректный: {message_time}"

@pytest.mark.asyncio
async def test_chat_widget_resize(page):
    """Проверка изменений размера виджета чата"""
    await page.goto(BASE_URL)
    chat = ChatPage(page)
    await chat.open_chat()
    initial_box = await page.locator(chat.chat_input_selector).bounding_box()
    await page.set_viewport_size({"width": 800, "height": 600})
    await asyncio.sleep(1)
    resized_box = await page.locator(chat.chat_input_selector).bounding_box()
    assert (resized_box["width"] != initial_box["width"] or resized_box["height"] != initial_box["height"]), "Размер виджета чата должен изменяться при изменении размеров окна"

@pytest.mark.asyncio
async def test_chat_history_preservation(page):
    """Проверка сохранения истории чата при рефреше"""
    await page.goto(BASE_URL)
    chat = ChatPage(page)
    await chat.open_chat()
    message = "История чата"
    await chat.fill_chat_input(message)
    await chat.click_send()
    await page.wait_for_selector(chat.chat_area_message_sent_selector)
    await page.reload()
    chat = ChatPage(page)
    await chat.open_chat()
    assert await page.is_visible(chat.chat_area_message_sent_selector), "История чата должна сохраняться после обновления страницы"

@pytest.mark.asyncio
async def test_chat_history_reset_after_cache_clear(page):
    """Проверка сброса истории чата после очистки кеша"""
    await page.goto(BASE_URL)
    chat = ChatPage(page)
    await chat.open_chat()
    message = "Сброс истории"
    await chat.fill_chat_input(message)
    await chat.click_send()
    await page.wait_for_selector(chat.chat_area_message_sent_selector)
    await page.evaluate("localStorage.clear()")
    await page.reload()
    chat = ChatPage(page)
    await chat.open_chat()
    assert not await page.is_visible(chat.chat_area_message_sent_selector), "История чата должна сбрасываться после очистки кеша"

@pytest.mark.asyncio
async def test_cross_browser_chat_widget(page):
    """Кроссбраузерность – отображение виджета в текущем браузере"""
    await page.goto(BASE_URL)
    chat = ChatPage(page)
    await chat.open_chat()
    assert await page.is_visible(chat.chat_input_selector), "Виджет чата должен быть виден во всех браузерах"

@pytest.mark.asyncio
@pytest.mark.parametrize("viewport", [
    {"width": 1920, "height": 1080},
    {"width": 1366, "height": 768},
    {"width": 375, "height": 667},
])
async def test_responsive_display(page, viewport):
    await page.set_viewport_size(viewport)
    await page.goto(BASE_URL)
    chat = ChatPage(page)
    await chat.open_chat()
    assert await page.is_visible(chat.chat_input_selector), f"Виджет чата должен отображаться на разрешении {viewport}"

@pytest.mark.asyncio
async def test_invalid_message(page):
    """Проверка некорректной отправки сообщения в чате"""
    await page.goto(BASE_URL)
    chat = ChatPage(page)
    await chat.open_chat()
    await chat.fill_chat_input("")
    await chat.click_send()
    await page.wait_for_selector(chat.chat_area_message_message_status_selector)
    status_text = await page.text_content(chat.chat_area_message_message_status_selector)
    assert "Ошибка" in status_text, f"При некорректном вводе должно отображаться сообщение об ошибке, получено: {status_text}"
