from authentication import get_crypto_stats, print_err
from db_connection import get_db_cursor
from time import sleep

stats = {}
cursor = get_db_cursor()
cursor.execute("select name from crypto_currencies")
cryptos = [crypto[0] for crypto in cursor.fetchall()]
# cryptos = ["LTC"]
print("CRYPTOS: ",cryptos)
for crypto in cryptos:
    try:
        stats[crypto] = get_crypto_stats(crypto)
    except Exception as e:
        print("EXCEPTION........")
        print_err(e)

cursor.execute("""SELECT  email, array_agg(cc.name) cryptos 
	FROM public.users u JOIN public.user_settings us ON u.id = us.user_id
	JOIN public.crypto_settings cs ON cs.user_setting_id = us.id
	JOIN public.crypto_currencies cc ON cc.id = cs.crypto_id
	GROUP BY u.email"""
    )
accounts = cursor.fetchall()

for account in accounts:
    email = account[0]
    cryptos = account[1]
    for c in cryptos:
        crypto_stats = stats[c]
        print(crypto_stats)

def advisor(data):
    story = "{ticker}:\n"
    one_month_change = data["changes"]["percent"]["month"]
    three_months_change = data["changes"]["percent"]["month_3"]
    six_months_change = data["changes"]["percent"]["month_6"]
    current_price = data["averages"]["day"]
    day_change = data["changes"]["price"]["day"]
    week_change = data["changes"]["price"]["week"]
    month_change = data["changes"]["price"]["month"]
    month_3_change = data["changes"]["price"]["month_3"]
    month_6_change = data["changes"]["price"]["month_6"]

    if one_month_change < -50:
        story += "The price has dropped by {percentage}% over the month. We strongly advice that you buy!".format(percentage=one_month_change)
    elif one_month_change < -20:
        story += "The price has dropped by {percentage}% over the month. You may buy or watch the trend to see if it'll drop further!".format(percentage=one_month_change)
    elif one_month_change > 50:
        story += "The price has risen by {percentage}% over the month. We strongly recommend you sell!".format(percentage=one_month_change)
    elif one_month_change > 30:
        story += "The price has risen by {percentage}% over the month. You may sell to make some profit or watch the price carefully for some time.".format(percentage=one_month_change)
 
    elif three_months_change < -50:
        story += "The price has dropped by {percentage}% over the past 3 months. We strongly advice that you buy!".format(percentage=three_months_change)
    elif three_months_change < -20:
        story += "The price has dropped by {percentage}% over the past 3 months. You may buy or watch the trend to see if it'll drop further!".format(percentage=three_months_change)
    elif three_months_change > 50:
        story += "The price has risen by {percentage}% over the past 3 months. We strongly recommend you sell!".format(percentage=three_months_change)
    elif three_months_change > 30:
        story += "The price has risen by {percentage}% over the past 3 months. You may sell to make some profit or watch the price carefully for some time.".format(percentage=three_months_change)
 
    elif six_months_change < -50:
        story += "The price has dropped by {percentage}% over the past 6 months. We strongly advice that you buy!".format(percentage=six_months_change)
    elif six_months_change < -20:
        story += "The price has dropped by {percentage}% over the past 6 months. You may buy or watch the trend to see if it'll drop further!".format(percentage=six_months_change)
    elif six_months_change > 50:
        story += "The price has risen by {percentage}% over the past 6 months. We strongly recommend you sell!".format(percentage=six_months_change)
    elif six_months_change > 30:
        story += "The price has risen by {percentage}% over the past 6 months. You may sell to make some profit or watch the price carefully for some time.".format(percentage=six_months_change)

    #general
    story += "\nDaily Updates\n"
    story += "Current Price: {current_price}\n" + 
             "Price Change (Day): {day_change}\n" +
             "Price Change (Week): {week_change}\n" +
             "Price Change (Month): {month_change}\n" +
             "Price Change (3 Months): {month_3_change}\n"+
             "Price Change (6 Months): {month_6_change}"

    story.format(
        current_price=current_price,
        day_change=day_change,
        week_change=week_change,
        month_change=month_change,
        month_3_change=month_3_change,
        month_6_change=month_6_change,
        ticker=data["display_symbol"]
    )
    return story + "\n\n"
