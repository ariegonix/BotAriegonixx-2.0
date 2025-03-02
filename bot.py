import discord
import requests
import os
from discord.ext import commands
from dotenv import load_dotenv

# Cargar el token de un archivo .env
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Configurar Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Crear el bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.command()
async def buscar(ctx, codigo: str, cantidad: float = 100):
    """Busca un alimento por su código de barras y muestra la información nutricional ajustada a la cantidad ingresada."""
    url = f"https://world.openfoodfacts.org/api/v0/product/{codigo}.json"
    response = requests.get(url)
    data = response.json()
    
    if data.get("status") == 1:
        producto = data["product"]
        nombre = producto.get("product_name", "Desconocido")
        calorias_100g = producto["nutriments"].get("energy-kcal_100g", None)
        imagen = producto.get("image_url", None)
        
        if calorias_100g is not None:
            calorias_totales = (calorias_100g * cantidad) / 100
            mensaje = f"🍽️ **{nombre}**\n✅🔥 Calorías por {cantidad}g: {calorias_totales:.2f} kcal 🔥✅"
        else:
            mensaje = f"🍽️ **{nombre}**\n❌🔥 No se encontraron datos de calorías 🔥❌"
        
        if imagen:
            embed = discord.Embed(title=nombre, description=mensaje, color=0x00FF00)
            embed.set_image(url=imagen)
            await ctx.send(embed=embed)
        else:
            await ctx.send(mensaje)
    else:
        await ctx.send("❌ Producto no encontrado ❌")

# Iniciar el bot
bot.run(TOKEN)
