#-*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import aiohttp
import asyncio
import async_timeout
import locale
import time

# use fr_FR on linux instead of fra
locale.setlocale(locale.LC_ALL, "fra")
# use - instead of # on linux
#print(time.strftime("%#d_%B_%Y"))

class Wikihandler:

    def __init__(self):
        self.session = aiohttp.ClientSession()


    async def fetch(self, url):
        """ Get the source code of an URL"""
        with async_timeout.timeout(10):
            async with self.session.get(url) as response:
                return await response.text(encoding="utf8")

    def packString(self, line):
        """ Extract text from a BeautifulSoup soup """
        ret = ""
        
        for s in line.contents:
            if s.__class__.__name__ == "Tag":
                ret += s.text
            else:
                ret += s

            
        return str(ret).lstrip()

    async def getContentImageOfTheDay(self):
        """ Get the source and the description of the daily image"""
        pagesource = BeautifulSoup(await self.fetch("https://fr.wikipedia.org/wiki/Wikipédia:Image_du_jour/"+time.strftime("%#d_%B_%Y")), "html.parser")

        entry = pagesource.find('div', {"class":"mw-parser-output"}).find('img')

        src = entry['src'].replace("thumb/", "")
        src = src[:src.rfind('/')]
        src = "https:"+src

        desc = entry['alt']

        return (src, desc)
        
    async def getContentDidYouKnow(self):
        """ Get last two trivias """
        ret = ""
        
        html = await self.getWikiSource()

        entries = html.findAll('div', {"class":"accueil_2017_cadre"})[2].findAll('li')
        
        ret += "- " + self.packString(entries[0]) + "\n"
        ret += "- " + self.packString(entries[1]) + "\n"
            
        return ret
        
    async def getWikiSource(self):
        """" Get source code of the main wikipedia page """
        html = await self.fetch("http://fr.wikipedia.org")
        #with open("test.txt", "w", encoding="utf8") as file:
        #    file.write(html)
        return BeautifulSoup(html, "html.parser")
        

    async def getContentLightOn(self):
        """ Get the URL of the daily article """
        html = await self.getWikiSource()
        
        url = html.findAll('div', {"class":"accueil_2017_cadre"})[0].findAll('li')[0].find('a')["href"]

        return "https://fr.wikipedia.org" + url 

    async def getContentRandomPage(self):
        """ Get a random page """
        async with self.session.get("https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard") as response:
            return response.url

    async def cleanup(self):
        """ Clean everything that was left opened"""
        await self.session.close()

async def main():
    wh = Wikihandler()
    await wh.cleanup()
    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())



        
