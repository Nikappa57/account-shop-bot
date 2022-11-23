def group(fun):
    def wrapper(update, *args):
        data = update.message if update.message else update.edited_message

        if not update.callback_query:
            if data.chat.type in ['goup', 'supergroup']:
                fun(update, *args)
        else:
            fun(update, *args)
            
    return wrapper

def private(fun):
    def wrapper(update, *args):
        data = update.message if update.message else update.callback_query \
                if update.callback_query else update.edited_message
        if data:
            if not update.callback_query:
                if data.chat.type == 'private':
                    fun(update, *args)
            else:
                fun(update, *args)
    return wrapper