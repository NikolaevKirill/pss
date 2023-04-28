import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time


async def parse_patent(html):
    soup = BeautifulSoup(html, "lxml")
    number = (
        soup.find("table", class_="tp")
        .find("div", id="top4")
        .text[1:-1]
        .replace(" ", "")
    )
    link = f"https://new.fips.ru/registers-doc-view/fips_servlet?DB=RUPAT&DocNumber={number}&TypeFile=html"
    abstract = soup.find("div", id="Abs").findAll("p")[1].text[:-1]

    return number, link, abstract


async def save_to_file(data, file_name="patents.txt"):
    with open(file_name, "a+") as fw:
        fw.writelines(f"{data[0]}\t{data[1]}\t{data[2]}\n")


async def scrape_patent(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
            try:
                data = await parse_patent(html)
            except:
                data = html
            await save_to_file(data)
        await asyncio.sleep(3)


async def main():
    start_numb = 2640290
    # end_numb = 2789828
    batch = 10
    end_numb = start_numb + batch
    tasks = []

    print("batch", batch)
    for number in range(start_numb, end_numb):
        link = f"https://new.fips.ru/registers-doc-view/fips_servlet?DB=RUPAT&DocNumber={number}&TypeFile=html"
        task = asyncio.create_task(scrape_patent(link))
        tasks.append(task)
    for task in tasks:
        await task


if __name__ == "__main__":
    print(time.strftime("%X"))
    asyncio.run(main())
    print(time.strftime("%X"))
