import asyncio
import os
import sys
from pathlib import Path
from threading import Thread

from playwright.async_api import async_playwright


def convert_html_to_png(
    html_filepath,
    output_image_path,
    width=1600,
    height=1200,
):
    """Render a local HTML file to PNG.

    Runs Playwright on a worker thread so it works inside Jupyter on
    Windows, where the kernel loop cannot spawn subprocesses and the
    sync API refuses to start.
    """
    out = Path(output_image_path)
    os.makedirs(out.parent, exist_ok=True)
    html_uri = Path(html_filepath).resolve().as_uri()

    result = {}

    def runner():
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

        async def _run():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page(
                    viewport={"width": width, "height": height}
                )
                await page.goto(html_uri, wait_until="networkidle")
                await page.wait_for_selector("img")
                await page.screenshot(path=str(out), full_page=True)
                await browser.close()
            return str(out)

        try:
            result["path"] = asyncio.run(_run())
        except Exception as exc:
            result["error"] = exc

    thread = Thread(target=runner)
    thread.start()
    thread.join()

    if "error" in result:
        raise result["error"]
    return result["path"]