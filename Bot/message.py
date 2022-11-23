from datetime import timedelta

from Bot.decorator import chattype, checkuser

from config import Config
from Bot.utils.bot_emoji import Emoji
from Bot.scheduled_messages import expiried_account, renew_account
from Bot.utils.chat import Chat


@chattype.private
@checkuser.check()
def accountMessage(update, context, currentuser):
    chat_id = update.effective_chat.id
    message = update.message.text
    
    if chat_id in Chat.sendAccount.keys():
        chat_id_user = Chat.sendAccount[chat_id]['chat_id']
        account = Chat.sendAccount[chat_id]['Account']

        email, password = message.split(":", 1)

        mex = f"{Emoji.diamond} <b>HERE IS YOUR ACCOUNT {account.upper()}</b> {Emoji.diamond}" + \
                f"\n\n{Emoji.email} <code>{email}</code>\n{Emoji.lock} <code>{password}</code>\n\n" + \
                    f"{Emoji.point}<i>Before entering your account, follow these steps {Config.guide}</i>"
        
        context.bot.send_message(chat_id=chat_id_user, text=mex)
        context.bot.send_message(chat_id=chat_id, text="Account sent with success")

        if not Chat.sendAccount[chat_id]['Renew']:
            plan = Chat.sendAccount[chat_id]['Plan']
            
            if plan == 0:
                time_expiried = timedelta(days=30)

                context.job_queue.run_once(expiried_account, time_expiried, context=chat_id_user)
            
            elif plan == 1:
                time_expiried = timedelta(days=30 * 6)

                context.job_queue.run_once(expiried_account, time_expiried, context=chat_id_user)

            elif plan == 2:
                time_expiried = timedelta(days=30 * 12)
                
                context.job_queue.run_once(expiried_account, time_expiried, context=chat_id_user)

            if plan in [1, 2]:
                time_expiried = timedelta(days=30)
                time = 5 if plan == 1 else 11

                Chat.sendAccount[chat_id]['time_expiried'] = time_expiried

                for i in range(time):
                    context.job_queue.run_once(
                        renew_account, 
                        time_expiried, 
                        context=[chat_id_user, account, time_expiried]
                    )

                    time_expiried += timedelta(days=30)
        del Chat.sendAccount[chat_id]