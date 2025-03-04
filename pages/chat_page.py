from playwright.async_api import Page

class ChatPage(Page):
    def __init__(self, page: Page):
        self.page = page
        self.chat_icon_selector = "css=div#chat21-launcher-button"
        self.chat_area_selector = "css=div#chat21-conversations"
        self.chat_header_close_button_selector = "css=a.chat21-sheet-header-close-button"
        self.chat_panel_send_button_selector = "css=div#chat21-button-send"
        self.chat_panel_attachment_button_selector = "css=div#chat21-start-upload-doc"
        self.chat_panel_emoji_button_selector = "css=div#chat21-button-emoji"
        self.chat_input_selector = "css=div#chat21-main-message-context"
        self.chat_area_message_sent_selector = "css=div.msg_sent"
        self.chat_area_message_receive_selector = "css=div.msg_receive"
        self.chat_area_message_message_status_selector = "css=div.status-message"
        self.chat_area_message_time_selector = "css=div.time"
        self.emoji_panel_selector = "css=div#chat21-emoji-picker-container"
        self.chat_area_input_contact_form = "css=div#chat21-message_userForm"
        self.chat_area_input_contact_full_name = "css=input#user-form_field_senderFullName"
        self.chat_area_input_contact_email = "css=input#user-form_field_senderEmail"
        self.chat_area_input_contact_form_submit = "css=button.form_panel_action-submit"

    async def open_chat(self):
        await self.page.click(self.chat_icon_selector)
        await self.page.wait_for_selector(self.chat_area_selector)
        if await self.page.is_visible(self.chat_area_input_contact_form):
            await self.fill_contact_details("Тестовый Пользователь", "test@example.com")

    async def fill_contact_details(self, full_name: str, email: str):
        await self.page.wait_for_selector(self.chat_area_input_contact_form)
        await self.page.fill(self.chat_area_input_contact_full_name, full_name)
        await self.page.fill(self.chat_area_input_contact_email, email)
        await self.page.click(self.chat_area_input_contact_form_submit)
        await self.page.wait_for_selector(self.chat_area_input_contact_form, state="hidden")

    async def close_chat(self):
        await self.page.click(self.chat_header_close_button_selector)
        await self.page.wait_for_selector(self.chat_input_selector, state="hidden")

    async def fill_chat_input(self, text: str):
        await self.page.fill(self.chat_input_selector, text)

    async def click_send(self):
        await self.page.click(self.chat_panel_send_button_selector)

    async def get_last_message(self):
        return await self.page.wait_for_selector(self.chat_area_message_sent_selector)

    async def get_last_received_message(self):
        return await self.page.wait_for_selector(self.chat_area_message_receive_selector)

    async def click_attachment(self):
        await self.page.click(self.chat_panel_attachment_button_selector)

    async def click_emoji(self):
        await self.page.click(self.chat_panel_emoji_button_selector)
        await self.page.wait_for_selector(self.chat_panel_emoji_button_selector)

    async def get_message_time(self):
        return await self.page.text_content(self.chat_area_message_time_selector)
