import os
import datetime
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Configuración del bot
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("hora_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Función para crear imagen con la hora
def crear_imagen_hora():
    now = datetime.datetime.now()
    hora_str = now.strftime("%H:%M:%S")
    fecha_str = now.strftime("%d/%m/%Y")
    
    # Crear imagen
    img = Image.new('RGB', (400, 200), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    
    # Usar una fuente (puedes cambiar la ruta o instalar fuentes en Render)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    d.text((100, 50), hora_str, fill=(255, 255, 0), font=font)
    d.text((100, 100), fecha_str, fill=(255, 255, 255), font=font)
    
    # Guardar imagen temporal
    img_path = f"hora_actual.png"
    img.save(img_path)
    return img_path

# Mensaje de bienvenida con menú interactivo
@app.on_message(filters.command("start"))
async def start(client, message):
    welcome_text = (
        "🕒 *¡Bienvenido al Bot de la Hora!* 🕒\n\n"
        "Soy tu asistente personal para mantenerte al tanto de la hora actual.\n"
        "Usa los botones de abajo para interactuar conmigo.\n\n"
        "¡No pierdas el tiempo, que el tiempo no te pierda a ti! ⏳"
    )
    
    # Crear teclado inline
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🕒 Obtener hora en imagen", callback_data="hora_imagen")],
            [InlineKeyboardButton("📅 Fecha actual", callback_data="fecha")],
            [InlineKeyboardButton("ℹ️ Acerca de", callback_data="about")],
            [InlineKeyboardButton("📞 Contacto", callback_data="contact")]
        ]
    )
    
    await message.reply_text(
        welcome_text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# Manejar callbacks de los botones
@app.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    
    if data == "hora_imagen":
        # Crear y enviar imagen con la hora
        img_path = crear_imagen_hora()
        await client.send_photo(
            callback_query.message.chat.id,
            img_path,
            caption=f"🕒 Aquí tienes la hora actual"
        )
        os.remove(img_path)
        
    elif data == "fecha":
        now = datetime.datetime.now()
        fecha_str = now.strftime("%A, %d de %B de %Y")
        await callback_query.answer(f"📅 Hoy es: {fecha_str}", show_alert=True)
        
    elif data == "about":
        about_text = (
            "🤖 *Acerca de este bot*\n\n"
            "Bot desarrollado con Pyrogram\n"
            "Funcionalidad principal: Mostrar la hora actual\n"
            "Versión: 1.0\n"
            "Desarrollador: Tú"
        )
        await callback_query.message.edit_text(
            about_text,
            parse_mode="Markdown"
        )
        
    elif data == "contact":
        await callback_query.answer(
            "📩 Puedes contactar al desarrollador a través de Telegram",
            show_alert=True
        )

# Comando directo para obtener la hora en imagen
@app.on_message(filters.command("hora"))
async def send_hora_image(client, message):
    img_path = crear_imagen_hora()
    await client.send_photo(
        message.chat.id,
        img_path,
        caption="🕒 Aquí tienes la hora actual"
    )
    os.remove(img_path)

if __name__ == "__main__":
    print("Bot iniciado...")
    app.run()