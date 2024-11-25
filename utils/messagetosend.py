from interactions import Embed


class MessageToSend:
    def __init__(self, content: str, embeds: list[Embed]):
        self.__content: str = content
        self.__embeds: list[Embed] = embeds

    def get_content(self) -> str:
        return self.__content

    def get_embeds(self) -> list[Embed]:
        return self.__embeds
