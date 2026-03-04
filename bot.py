import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ---------------------------------------------------------------------------
# Data: country name → flag emoji
# ---------------------------------------------------------------------------
COUNTRIES = {
    "France": "🇫🇷",
    "Allemagne": "🇩🇪",
    "Espagne": "🇪🇸",
    "Italie": "🇮🇹",
    "Portugal": "🇵🇹",
    "Royaume-Uni": "🇬🇧",
    "Pays-Bas": "🇳🇱",
    "Belgique": "🇧🇪",
    "Suisse": "🇨🇭",
    "Autriche": "🇦🇹",
    "Suède": "🇸🇪",
    "Norvège": "🇳🇴",
    "Danemark": "🇩🇰",
    "Finlande": "🇫🇮",
    "Pologne": "🇵🇱",
    "Grèce": "🇬🇷",
    "Turquie": "🇹🇷",
    "Russie": "🇷🇺",
    "Ukraine": "🇺🇦",
    "États-Unis": "🇺🇸",
    "Canada": "🇨🇦",
    "Mexique": "🇲🇽",
    "Brésil": "🇧🇷",
    "Argentine": "🇦🇷",
    "Chili": "🇨🇱",
    "Colombie": "🇨🇴",
    "Pérou": "🇵🇪",
    "Japon": "🇯🇵",
    "Chine": "🇨🇳",
    "Corée du Sud": "🇰🇷",
    "Inde": "🇮🇳",
    "Australie": "🇦🇺",
    "Nouvelle-Zélande": "🇳🇿",
    "Afrique du Sud": "🇿🇦",
    "Égypte": "🇪🇬",
    "Maroc": "🇲🇦",
    "Nigeria": "🇳🇬",
    "Kenya": "🇰🇪",
    "Arabie Saoudite": "🇸🇦",
    "Israël": "🇮🇱",
    "Iran": "🇮🇷",
    "Pakistan": "🇵🇰",
    "Bangladesh": "🇧🇩",
    "Thaïlande": "🇹🇭",
    "Vietnam": "🇻🇳",
    "Philippines": "🇵🇭",
    "Indonésie": "🇮🇩",
    "Malaisie": "🇲🇾",
    "Singapour": "🇸🇬",
    "Cuba": "🇨🇺",
    "Jamaïque": "🇯🇲",
    "Irlande": "🇮🇪",
    "Croatie": "🇭🇷",
    "Roumanie": "🇷🇴",
    "Hongrie": "🇭🇺",
    "République Tchèque": "🇨🇿",
    "Slovaquie": "🇸🇰",
    "Serbie": "🇷🇸",
    "Algérie": "🇩🇿",
    "Tunisie": "🇹🇳",
    "Éthiopie": "🇪🇹",
    "Ghana": "🇬🇭",
    "Sénégal": "🇸🇳",
    "Colombie": "🇨🇴",
    "Venezuela": "🇻🇪",
    "Équateur": "🇪🇨",
    "Bolivie": "🇧🇴",
    "Paraguay": "🇵🇾",
    "Uruguay": "🇺🇾",
}

COUNTRY_LIST = list(COUNTRIES.keys())

# ---------------------------------------------------------------------------
# Score tracking (in-memory, resets on bot restart)
# ---------------------------------------------------------------------------
scores: dict[int, int] = {}   # user_id → total correct answers


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------
class FlagView(discord.ui.View):
    """4-button multiple choice view for a single flag question."""

    def __init__(
        self,
        correct: str,
        choices: list[str],
        timeout: float = 30.0,
    ):
        super().__init__(timeout=timeout)
        self.correct = correct
        self.answered_users: set[int] = set()

        random.shuffle(choices)
        for country in choices:
            button = discord.ui.Button(
                label=country,
                style=discord.ButtonStyle.secondary,
                custom_id=country,
            )
            button.callback = self._make_callback(country)
            self.add_item(button)

    def _make_callback(self, country: str):
        async def callback(interaction: discord.Interaction):
            user_id = interaction.user.id

            if user_id in self.answered_users:
                await interaction.response.send_message(
                    "❌ Tu as déjà répondu à cette question !", ephemeral=True
                )
                return

            self.answered_users.add(user_id)

            if country == self.correct:
                scores[user_id] = scores.get(user_id, 0) + 1
                await interaction.response.send_message(
                    f"✅ **Bonne réponse !** C'était bien **{self.correct}**.\n"
                    f"🏆 Ton score total : **{scores[user_id]}** point(s).",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    f"❌ **Mauvaise réponse !** La bonne réponse était **{self.correct}**.",
                    ephemeral=True,
                )

        return callback

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True


# ---------------------------------------------------------------------------
# Bot setup
# ---------------------------------------------------------------------------
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot connecté en tant que {bot.user} (ID: {bot.user.id})")
    print("Commandes slash synchronisées.")


# ---------------------------------------------------------------------------
# Slash commands
# ---------------------------------------------------------------------------
@bot.tree.command(name="drapeau", description="Devine à quel pays appartient ce drapeau !")
async def flag_quiz(interaction: discord.Interaction):
    correct = random.choice(COUNTRY_LIST)
    wrong_choices = random.sample(
        [c for c in COUNTRY_LIST if c != correct], k=3
    )
    choices = [correct] + wrong_choices

    flag_emoji = COUNTRIES[correct]

    embed = discord.Embed(
        title="🌍 Quiz des Drapeaux",
        description=(
            f"## {flag_emoji}\n\n"
            "**À quel pays appartient ce drapeau ?**\n\n"
            "Tu as **30 secondes** pour répondre !"
        ),
        color=discord.Color.blurple(),
    )
    embed.set_footer(text="Clique sur l'un des 4 boutons ci-dessous.")

    view = FlagView(correct=correct, choices=choices)
    await interaction.response.send_message(embed=embed, view=view)


@bot.tree.command(name="score", description="Affiche ton score au quiz des drapeaux.")
async def show_score(interaction: discord.Interaction):
    user_id = interaction.user.id
    total = scores.get(user_id, 0)
    await interaction.response.send_message(
        f"🏆 **{interaction.user.display_name}**, tu as **{total}** bonne(s) réponse(s) au total.",
        ephemeral=True,
    )


@bot.tree.command(name="classement", description="Affiche le classement des meilleurs joueurs.")
async def leaderboard(interaction: discord.Interaction):
    if not scores:
        await interaction.response.send_message(
            "📭 Aucun score enregistré pour le moment. Lance `/drapeau` pour jouer !",
            ephemeral=True,
        )
        return

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]

    lines = []
    medals = ["🥇", "🥈", "🥉"]
    for i, (user_id, score) in enumerate(sorted_scores):
        medal = medals[i] if i < 3 else f"`{i + 1}.`"
        try:
            user = await bot.fetch_user(user_id)
            name = user.display_name
        except discord.NotFound:
            name = f"Utilisateur inconnu ({user_id})"
        lines.append(f"{medal} **{name}** — {score} pt(s)")

    embed = discord.Embed(
        title="🏆 Classement — Quiz des Drapeaux",
        description="\n".join(lines),
        color=discord.Color.gold(),
    )
    await interaction.response.send_message(embed=embed)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("DISCORD_TOKEN manquant. Vérifie ton fichier .env")
    bot.run(TOKEN)
