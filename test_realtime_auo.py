from market_data.twse_realtime import TWSERealtime

q = TWSERealtime().get_price("2409")
print(q)
