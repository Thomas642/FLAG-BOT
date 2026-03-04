import discord
from discord.ext import commands
from discord import app_commands
import random
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ---------------------------------------------------------------------------
# Data: country name (FR) → flag emoji  [ISO 3166-1 alpha-2 based emojis]
# ---------------------------------------------------------------------------
COUNTRIES = {
    # ── Europe ──────────────────────────────────────────────────────────────
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
    "Irlande": "🇮🇪",
    "Croatie": "🇭🇷",
    "Roumanie": "🇷🇴",
    "Hongrie": "🇭🇺",
    "République Tchèque": "🇨🇿",
    "Slovaquie": "🇸🇰",
    "Serbie": "🇷🇸",
    "Albanie": "🇦🇱",
    "Andorre": "🇦🇩",
    "Biélorussie": "🇧🇾",
    "Bosnie-Herzégovine": "🇧🇦",
    "Bulgarie": "🇧🇬",
    "Chypre": "🇨🇾",
    "Estonie": "🇪🇪",
    "Islande": "🇮🇸",
    "Lettonie": "🇱🇻",
    "Liechtenstein": "🇱🇮",
    "Lituanie": "🇱🇹",
    "Luxembourg": "🇱🇺",
    "Malte": "🇲🇹",
    "Moldavie": "🇲🇩",
    "Monaco": "🇲🇨",
    "Monténégro": "🇲🇪",
    "Macédoine du Nord": "🇲🇰",
    "Saint-Marin": "🇸🇲",
    "Slovénie": "🇸🇮",
    "Vatican": "🇻🇦",
    "Kosovo": "🇽🇰",
    # ── Amériques ────────────────────────────────────────────────────────────
    "États-Unis": "🇺🇸",
    "Canada": "🇨🇦",
    "Mexique": "🇲🇽",
    "Brésil": "🇧🇷",
    "Argentine": "🇦🇷",
    "Chili": "🇨🇱",
    "Colombie": "🇨🇴",
    "Pérou": "🇵🇪",
    "Venezuela": "🇻🇪",
    "Équateur": "🇪🇨",
    "Bolivie": "🇧🇴",
    "Paraguay": "🇵🇾",
    "Uruguay": "🇺🇾",
    "Cuba": "🇨🇺",
    "Jamaïque": "🇯🇲",
    "Antigua-et-Barbuda": "🇦🇬",
    "Bahamas": "🇧🇸",
    "Barbade": "🇧🇧",
    "Belize": "🇧🇿",
    "Costa Rica": "🇨🇷",
    "Dominique": "🇩🇲",
    "République dominicaine": "🇩🇴",
    "Salvador": "🇸🇻",
    "Grenade": "🇬🇩",
    "Guatemala": "🇬🇹",
    "Guyana": "🇬🇾",
    "Haïti": "🇭🇹",
    "Honduras": "🇭🇳",
    "Nicaragua": "🇳🇮",
    "Panama": "🇵🇦",
    "Saint-Kitts-et-Nevis": "🇰🇳",
    "Sainte-Lucie": "🇱🇨",
    "Saint-Vincent-et-les-Grenadines": "🇻🇨",
    "Suriname": "🇸🇷",
    "Trinité-et-Tobago": "🇹🇹",
    # ── Afrique ──────────────────────────────────────────────────────────────
    "Afrique du Sud": "🇿🇦",
    "Égypte": "🇪🇬",
    "Maroc": "🇲🇦",
    "Nigeria": "🇳🇬",
    "Kenya": "🇰🇪",
    "Éthiopie": "🇪🇹",
    "Ghana": "🇬🇭",
    "Sénégal": "🇸🇳",
    "Algérie": "🇩🇿",
    "Tunisie": "🇹🇳",
    "Angola": "🇦🇴",
    "Bénin": "🇧🇯",
    "Botswana": "🇧🇼",
    "Burkina Faso": "🇧🇫",
    "Burundi": "🇧🇮",
    "Cameroun": "🇨🇲",
    "Cap-Vert": "🇨🇻",
    "République centrafricaine": "🇨🇫",
    "Tchad": "🇹🇩",
    "Comores": "🇰🇲",
    "République du Congo": "🇨🇬",
    "République démocratique du Congo": "🇨🇩",
    "Djibouti": "🇩🇯",
    "Guinée équatoriale": "🇬🇶",
    "Érythrée": "🇪🇷",
    "Eswatini": "🇸🇿",
    "Gabon": "🇬🇦",
    "Gambie": "🇬🇲",
    "Guinée": "🇬🇳",
    "Guinée-Bissau": "🇬🇼",
    "Côte d'Ivoire": "🇨🇮",
    "Lesotho": "🇱🇸",
    "Liberia": "🇱🇷",
    "Libye": "🇱🇾",
    "Madagascar": "🇲🇬",
    "Malawi": "🇲🇼",
    "Mali": "🇲🇱",
    "Mauritanie": "🇲🇷",
    "Maurice": "🇲🇺",
    "Mozambique": "🇲🇿",
    "Namibie": "🇳🇦",
    "Niger": "🇳🇪",
    "Rwanda": "🇷🇼",
    "Sao Tomé-et-Principe": "🇸🇹",
    "Sierra Leone": "🇸🇱",
    "Somalie": "🇸🇴",
    "Soudan du Sud": "🇸🇸",
    "Soudan": "🇸🇩",
    "Tanzanie": "🇹🇿",
    "Togo": "🇹🇬",
    "Ouganda": "🇺🇬",
    "Zambie": "🇿🇲",
    "Zimbabwe": "🇿🇼",
    "Seychelles": "🇸🇨",
    # ── Asie ─────────────────────────────────────────────────────────────────
    "Japon": "🇯🇵",
    "Chine": "🇨🇳",
    "Corée du Sud": "🇰🇷",
    "Inde": "🇮🇳",
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
    "Afghanistan": "🇦🇫",
    "Arménie": "🇦🇲",
    "Azerbaïdjan": "🇦🇿",
    "Bahreïn": "🇧🇭",
    "Bhoutan": "🇧🇹",
    "Brunei": "🇧🇳",
    "Cambodge": "🇰🇭",
    "Timor oriental": "🇹🇱",
    "Géorgie": "🇬🇪",
    "Irak": "🇮🇶",
    "Jordanie": "🇯🇴",
    "Kazakhstan": "🇰🇿",
    "Koweït": "🇰🇼",
    "Kirghizistan": "🇰🇬",
    "Laos": "🇱🇦",
    "Liban": "🇱🇧",
    "Maldives": "🇲🇻",
    "Mongolie": "🇲🇳",
    "Myanmar": "🇲🇲",
    "Népal": "🇳🇵",
    "Corée du Nord": "🇰🇵",
    "Oman": "🇴🇲",
    "Qatar": "🇶🇦",
    "Sri Lanka": "🇱🇰",
    "Syrie": "🇸🇾",
    "Taïwan": "🇹🇼",
    "Tadjikistan": "🇹🇯",
    "Turkménistan": "🇹🇲",
    "Émirats arabes unis": "🇦🇪",
    "Ouzbékistan": "🇺🇿",
    "Yémen": "🇾🇪",
    "Palestine": "🇵🇸",
    # ── Océanie ───────────────────────────────────────────────────────────────
    "Australie": "🇦🇺",
    "Nouvelle-Zélande": "🇳🇿",
    "Fidji": "🇫🇯",
    "Kiribati": "🇰🇮",
    "Îles Marshall": "🇲🇭",
    "Micronésie": "🇫🇲",
    "Nauru": "🇳🇷",
    "Palaos": "🇵🇼",
    "Papouasie-Nouvelle-Guinée": "🇵🇬",
    "Samoa": "🇼🇸",
    "Îles Salomon": "🇸🇧",
    "Tonga": "🇹🇴",
    "Tuvalu": "🇹🇻",
    "Vanuatu": "🇻🇺",
}

COUNTRY_LIST = list(COUNTRIES.keys())

# ---------------------------------------------------------------------------
# Quiz session state  (in-memory, reset on restart)
# ---------------------------------------------------------------------------
class QuizSession:
    def __init__(self, user_id: int, questions: list[str]):
        self.user_id = user_id
        self.remaining = questions
        self.total = len(questions)
        self.score = 0
        self.current_question_index = 1

    def pop_next(self) -> str | None:
        return self.remaining.pop(0) if self.remaining else None


sessions: dict[int, QuizSession] = {}
global_scores: dict[int, int] = {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def build_question_embed(
    session: QuizSession,
    country: str,
    result_text: str = "",
    color: discord.Color = discord.Color.blurple(),
) -> discord.Embed:
    flag = COUNTRIES[country]
    desc = f"## {flag}\n\n**À quel pays appartient ce drapeau ?**"
    if result_text:
        desc += f"\n\n{result_text}"
    desc += (
        f"\n\n📊 Question **{session.current_question_index}/{session.total}**"
        f"  |  ✅ **{session.score}** correcte(s)"
    )
    embed = discord.Embed(title="🌍 Quiz des Drapeaux", description=desc, color=color)
    embed.set_footer(text="Tu as 60 secondes pour répondre. /stop pour abandonner.")
    return embed


def build_choices(correct: str) -> list[str]:
    wrong = random.sample([c for c in COUNTRY_LIST if c != correct], k=3)
    choices = [correct] + wrong
    random.shuffle(choices)
    return choices


def build_final_embed(session: QuizSession, last_result: str) -> discord.Embed:
    pct = round(session.score / session.total * 100)
    if pct == 100:
        medal = "🏆"
    elif pct >= 80:
        medal = "🥇"
    elif pct >= 60:
        medal = "🥈"
    elif pct >= 40:
        medal = "🥉"
    else:
        medal = "📚"
    embed = discord.Embed(
        title="🏁 Quiz terminé !",
        description=(
            f"{last_result}\n\n"
            f"{medal} **Score final : {session.score}/{session.total}** ({pct} %)\n\n"
            "Lance `/drapeau` pour rejouer !"
        ),
        color=discord.Color.green() if pct >= 50 else discord.Color.red(),
    )
    return embed


# ---------------------------------------------------------------------------
# View
# ---------------------------------------------------------------------------
class FlagView(discord.ui.View):
    def __init__(self, session: QuizSession, correct: str, choices: list[str]):
        super().__init__(timeout=60.0)
        self.session = session
        self.correct = correct

        for country in choices:
            btn = discord.ui.Button(label=country, style=discord.ButtonStyle.secondary)
            btn.callback = self._make_callback(country)
            self.add_item(btn)

    def _make_callback(self, chosen: str):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.session.user_id:
                await interaction.response.send_message(
                    "❌ Ce quiz ne t'appartient pas ! Lance `/drapeau` pour démarrer le tien.",
                    ephemeral=True,
                )
                return

            # Disable buttons to prevent double-click
            for item in self.children:
                item.disabled = True

            is_correct = chosen == self.correct
            if is_correct:
                self.session.score += 1
                global_scores[self.session.user_id] = (
                    global_scores.get(self.session.user_id, 0) + 1
                )
                result_text = f"✅ **Bonne réponse !** C'était bien **{self.correct}**."
                color = discord.Color.green()
            else:
                result_text = f"❌ **Mauvaise réponse.** La bonne réponse était **{self.correct}**."
                color = discord.Color.red()

            self.session.current_question_index += 1
            next_country = self.session.pop_next()

            if next_country is None:
                if self.session.user_id in sessions:
                    del sessions[self.session.user_id]
                await interaction.response.edit_message(
                    embed=build_final_embed(self.session, result_text),
                    view=None,
                )
            else:
                next_choices = build_choices(next_country)
                next_view = FlagView(self.session, next_country, next_choices)
                await interaction.response.edit_message(
                    embed=build_question_embed(self.session, next_country, result_text, color),
                    view=next_view,
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
    print(f"✅ Bot connecté : {bot.user} (ID : {bot.user.id})")
    print(f"   {len(COUNTRIES)} pays chargés.")


# ---------------------------------------------------------------------------
# Slash commands
# ---------------------------------------------------------------------------
@bot.tree.command(
    name="drapeau",
    description="Lance un quiz des drapeaux.",
)
@app_commands.describe(questions="Nombre de drapeaux à deviner (1 à 250, défaut : 10)")
async def flag_quiz(interaction: discord.Interaction, questions: int = 10):
    user_id = interaction.user.id

    if user_id in sessions:
        await interaction.response.send_message(
            "⚠️ Tu as déjà un quiz en cours ! Réponds ou tape `/stop` pour abandonner.",
            ephemeral=True,
        )
        return

    questions = max(1, min(questions, len(COUNTRIES)))
    pool = random.sample(COUNTRY_LIST, k=questions)

    session = QuizSession(user_id=user_id, questions=pool)
    sessions[user_id] = session

    first_country = session.pop_next()
    choices = build_choices(first_country)
    view = FlagView(session, first_country, choices)

    await interaction.response.send_message(
        embed=build_question_embed(session, first_country),
        view=view,
    )


@bot.tree.command(name="stop", description="Abandonne ton quiz en cours.")
async def stop_quiz(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id not in sessions:
        await interaction.response.send_message(
            "❌ Tu n'as pas de quiz en cours. Lance `/drapeau` pour jouer !",
            ephemeral=True,
        )
        return

    session = sessions.pop(user_id)
    await interaction.response.send_message(
        f"🛑 Quiz abandonné.\n"
        f"📊 Score à l'arrêt : **{session.score}/{session.total}**\n"
        f"Lance `/drapeau` quand tu veux recommencer !",
        ephemeral=True,
    )


@bot.tree.command(name="score", description="Affiche ton score cumulé (toutes parties).")
async def show_score(interaction: discord.Interaction):
    total = global_scores.get(interaction.user.id, 0)
    await interaction.response.send_message(
        f"🏆 **{interaction.user.display_name}**, tu as **{total}** bonne(s) réponse(s) au total.",
        ephemeral=True,
    )


@bot.tree.command(name="classement", description="Top 10 des meilleurs joueurs du serveur.")
async def leaderboard(interaction: discord.Interaction):
    if not global_scores:
        await interaction.response.send_message(
            "📭 Aucun score enregistré. Lance `/drapeau` pour jouer !",
            ephemeral=True,
        )
        return

    sorted_scores = sorted(global_scores.items(), key=lambda x: x[1], reverse=True)[:10]
    medals = ["🥇", "🥈", "🥉"]
    lines = []
    for i, (uid, score) in enumerate(sorted_scores):
        medal = medals[i] if i < 3 else f"`{i + 1}.`"
        try:
            user = await bot.fetch_user(uid)
            name = user.display_name
        except discord.NotFound:
            name = "Joueur inconnu"
        lines.append(f"{medal} **{name}** | {score} pt(s)")

    embed = discord.Embed(
        title="🏆 Classement | Quiz des Drapeaux",
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
