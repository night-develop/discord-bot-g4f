import json

from os.path import exists


class LinksGuilds:
    __linsk: dict = None

    def __init__(self) -> None:
        if not self.__check_linsk_file():
            self.__create_links_file()

    def __check_linsk_file(self) -> bool:
        return exists('links')
    
    def __create_links_file(self, links: dict = {}) -> None:    
        f = open("links", "w")
        f.write(json.dumps(links))
        f.close()

    def _read_links_file(self) -> None:
        f = open("links", "r")
        result = f.read()
        self.__linsk = json.loads(result)

    async def get_refresh_links(self) -> dict:
        self._read_links_file()
        return self.__linsk
    
    async def set_links(self, guild_id: int, channel_id: int) -> dict:
        links = self.__linsk
        links.update({
            str(guild_id): channel_id
        })
        self.__create_links_file(links=links)
        return await self.get_refresh_links()
    
    async def delete_link(self, guild_id: int) -> dict:
        links = self.__linsk
        if str(guild_id) in links:
            del links[str(guild_id)]

        self.__create_links_file(links=links)
        return await self.get_refresh_links()