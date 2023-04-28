import requests
from bs4 import BeautifulSoup
import time


def download_page(url):
    response = requests.get(url)
    return response.text


def parse_patent(html):
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


def save_to_file(data, file_name="patents.txt"):
    with open(file_name, "a+") as fw:
        fw.writelines(f"{data[0]}\t{data[1]}\t{data[2]}\n")


def scrape_patent(url):
    html = download_page(url)
    data = parse_patent(html)
    save_to_file(data)
    time.sleep(3)  # add a 3-second delay to avoid overloading the server


def main():
    start_numb = 2640290
    # end_numb = 2789828
    batch = 10
    end_numb = start_numb + batch

    print("batch:", batch)
    for number in range(start_numb, end_numb):
        link = f"https://new.fips.ru/registers-doc-view/fips_servlet?DB=RUPAT&DocNumber={number}&TypeFile=html"
        scrape_patent(link)


if __name__ == "__main__":
    print(time.strftime("%X"))
    main()
    print(time.strftime("%X"))
