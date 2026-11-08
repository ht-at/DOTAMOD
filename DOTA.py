@bot.command()
async def grab(ctx, *, path: str):
    """Скачивает файл с указанного пути и отправляет в канал."""
    try:
        # Раскрытие переменных окружения и домашних директорий
        full_path = os.path.expandvars(os.path.expanduser(path.strip()))
        
        if not os.path.exists(full_path):
            return await ctx.send(f"Ошибка: Файл не найден по пути `{full_path}`")
            
        if os.path.isdir(full_path):
            return await ctx.send("Ошибка: Указан путь к папке. Архивация папок пока не поддерживается, указывай конкретный файл.")

        file_size = os.path.getsize(full_path)
        if file_size > 25 * 1024 * 1024: # Лимит Discord (с запасом)
             return await ctx.send(f"Ошибка: Файл слишком большой ({file_size // (1024*1024)} MB). Лимит 25 MB.")

        await ctx.send(f"Извлечение `{os.path.basename(full_path)}`...", file=discord.File(full_path))
    except PermissionError:
        await ctx.send("Ошибка: Отказано в доступе (требуются права Администратора).")
    except Exception as e:
        await ctx.send(f"Ошибка передачи: `{e}`")