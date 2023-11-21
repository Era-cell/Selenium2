from testing.bot import InformationExtractor

try:
    with InformationExtractor() as bot:
        bot.get_details()
except Exception as e:
    if 'in PATH' in str(e):
        print("You are trying to exceute prgram from command line")
    else:
        raise
