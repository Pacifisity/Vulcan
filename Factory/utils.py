import discord

def add_multiple_items(modal: discord.ui.Modal, items: list[discord.ui.TextInput]):
    for item in items:
        modal.add_item(item)

    return modal

def all_different(items: list[str]):
    for i, item1 in enumerate(items):
        for i2, item2 in enumerate(items):
            if i != i2 and item1 == item2:
                return False
    return True