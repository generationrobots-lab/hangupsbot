import hangups

from hangupsbot.handlers import handler


@handler.register(priority=5, event=hangups.MembershipChangeEvent)
def handle_membership_change(bot, event):
    """Handle conversation membership change"""
    # Test if watching for membership changes is enabled
    if not bot.get_config_suboption(event.conv_id, 'membership_watching_enabled'):
        return

    # Generate list of added or removed users
    event_users = [event.conv.get_user(user_id) for user_id
                   in event.conv_event.participant_ids]
    names = ', '.join([user.full_name for user in event_users])

    # JOIN
    if event.conv_event.type_ == hangups.MembershipChangeType.JOIN:
        # Test if user who added new participants is admin
        admins_list = bot.get_config_suboption(event.conv_id, 'admins')
        if event.user_id.chat_id in admins_list:
            bot.send_message(event.conv,
                             '{}: Ahoj, {} mezi nás!'.format(names,
                                                             'vítejte' if len(event_users) > 1 else 'vítej'))
        else:
            segments = [hangups.ChatMessageSegment('!!! POZOR !!!', is_bold=True),
                        hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
                        hangups.ChatMessageSegment('{} neoprávněně přidal do tohoto Hangoutu uživatele {}!'.format(
                                                   event.user.full_name, names)),
                        hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
                        hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
                        hangups.ChatMessageSegment('{}: Opusťte prosím urychleně tento Hangout!'.format(names))]
            bot.send_message_segments(event.conv, segments)
    # LEAVE
    else:
        bot.send_message(event.conv,
                         '{} nám {} košem :-( Řekněte pá pá!'.format(names,
                                                                     'dali' if len(event_users) > 1 else 'dal'))
