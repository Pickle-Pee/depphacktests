import pytest
import asyncio
from playwright.async_api import async_playwright

@pytest.fixture(scope="session")
def event_loop():
    """Создаёт event loop для сессии, чтобы избежать ScopeMismatch."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        yield browser
        await browser.close()

@pytest.fixture()
async def page(browser):
    context = await browser.new_context()
    page = await context.new_page()
    yield page
    await page.close()
