import asyncio
from playwright.async_api import async_playwright


async def launch_chrome_dev():
    # 启动 Playwright
    async with async_playwright() as playwright:
        # 获取 Chromium 浏览器类型的引用
        chromium = playwright.chromium

        # 指定已安装的 Chrome Dev 浏览器的路径
        chrome_executable_path =   r"C:\Program Files\Google\Chrome Dev\Application\chrome.exe"
   

        # 启动已安装的 Chrome Dev 浏览器
        browser = await chromium.launch_persistent_context(
            user_data_dir=None, headless=False,   executable_path=chrome_executable_path
        )

        # 创建一个新的页面
        page = await browser.new_page()

        # 导航到一个网页
        await page.goto("https://tongyi.aliyun.com/")

        # 打印标题
        print(await page.title())

        # 关闭浏览器


asyncio.run(launch_chrome_dev())
