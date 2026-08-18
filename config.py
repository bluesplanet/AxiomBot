import discord



class Durations:
    """Durées d'affichage des messages temporaires d'AxiomBot."""

    # Messages d'erreur
    ERROR = 10

    # Messages de réussite
    SUCCESS = 8

    # Messages de réussite(Embed)
    SUCCESS_EMBED = 8*2

    # Avertissements
    WARNING = 12

    # Informations
    INFO = 15

    # Messages de configuration
    CONFIG = 20

    # Messages d'aide
    HELP = 30

    # Message permanent
    PERMANENT = None






class Colors:
    """Palette officielle des couleurs d'AxiomBot."""

    # 🔵 Couleur principale — bleu turquoise
    BOT = discord.Colour.from_str("#20C9C9")

    # 🔴 Erreur
    ERROR = discord.Colour.from_str("#ED4245")

    # 🟢 Succès
    SUCCESS = discord.Colour.from_str("#57F287")

    # 🟠 Avertissement
    WARNING = discord.Colour.from_str("#FEE75C")

    # 🔷 Information
    INFO = discord.Colour.from_str("#3498DB")

    BOT = discord.Colour.from_str("#109457")

