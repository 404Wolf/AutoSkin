from pyppeteer import launch
import asyncio

#function using pypeteer (a pupeteer wrapper for python) to visit the namemc page
async def skinRefresh(ign):
    browser = await launch(headless=False) #launch a headed browser
    page = await browser.newPage() #make a new tab
    url = ("https://namemc.com/profile/"+ign).lower() #visit url
    await page.goto(url,waitUntil='networkidle0') #go to the url 
    await asyncio.sleep(4)
    await browser.close() #close browser
    await asyncio.sleep(.2)