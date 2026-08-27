import discord
from textwrap import dedent
AXIOM_BLUE = discord.Color.from_rgb(0, 170, 255)

class Pagination_permissions(discord.ui.View,):
    def __init__(self,pages,titre,titre_all):
        super().__init__()

        self.pages = pages
        self.page = 0
        self.titre = titre
        self.titre_all = titre_all

    def create_embed(self):

        embed = discord.Embed(
            title = self.titre,
            colour=AXIOM_BLUE
        )

        

        embed.add_field(
            name="",
            value="",
            inline=False
        )
        if self.pages["type"] == "membre":
            membres = self.pages["pages"]
            
            if membres is None:
                embed = discord.Embed(
                    title=(f"Le role est vide"),
                    colour=AXIOM_BLUE
                )
                return embed
            
            for membre in membres[self.page]:
                embed.add_field(
                    name=f"{membre}",
                    value="",
                    inline=False
                )

            embed.description = dedent(f"""
                ╭─ Page {self.page + 1}/{len(self.pages["pages"])} ─╮
                \n\n
            """)


        if self.pages["type"] == "permissions":
            permissions = self.pages["pages"]
            for permission in permissions[self.page]:

                if permission.startswith("●"):
                    embed.add_field(
                        name=f"{permission}",
                        value="",
                        inline=False
                    )

            embed.description = dedent(f"""
            ╭─ Page {self.page + 1}/{len(self.pages["pages"])} ─╮
            \n\n
            """)


        embed.set_footer(
            text=f"AxiomBot • Powered by Blues Planet"
        )

        return embed

    
    def creat_page_all(self):

        if self.pages["type"] == "permissions":
            embed = discord.Embed(
                title = self.titre_all,
                description="\n\n".join(self.pages["pages_all"]),
                colour=AXIOM_BLUE
            ) 
        if self.pages["type"] == "membre":
            embed = discord.Embed(
                title = self.titre_all,
                description="\n\n".join(self.pages["pages_all"]),
                colour=AXIOM_BLUE
            ) 
            
        embed.set_footer(
            text="AxiomBot • Powered by Blues Planet"
        )
        return embed

    
    @discord.ui.button(
        label = "‹",
        style = discord.ButtonStyle.blurple 
    )
    async def previous_page(
        self,
        interaction:discord.Interaction,
        button:discord.ui.Button
    ):
        if self.page  > 0:
            self.page -= 1
        elif self.page == 0:
            self.page = (len(self.pages["pages"]) - 1)

        await interaction.response.edit_message(
            embed=self.create_embed(),
            view=self
        )

    @discord.ui.button(
            label="Tout afficher",
            style=discord.ButtonStyle.blurple
        )
        
    async def page_all(
        self,
        interaction:discord.Interaction,
        button:discord.ui.Button
    ):
        await interaction.response.send_message(
            embed=self.creat_page_all(),
            delete_after=60*5
            )


    @discord.ui.button(
        label=" ›",
        style=discord.ButtonStyle.blurple
    )
    
    async def next_page(
        self,
        interaction:discord.Interaction,
        button:discord.ui.Button
    ):
        if self.page < len(self.pages["pages"]) - 1:
            self.page += 1
        elif self.page == (len(self.pages["pages"]) - 1):
            self.page = 0

        await interaction.response.edit_message(
        embed=self.create_embed(),
        view=self
        )