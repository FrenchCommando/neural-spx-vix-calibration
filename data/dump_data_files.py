# create csv files with the right format
import os
import datetime as dt
import pandas as pd

import data.module_external
from data.expiry_selection import get_expiries
from market.history_quotes import get_option_series_with_cache_blocking
from market.history_contract import get_strike_list_for_date


data_folder = os.path.join(os.getcwd(), 'data', 'csv')
spx_file = os.path.join(data_folder, 'spx_bid_ask.csv')
vix_file = os.path.join(data_folder, 'vix_bid_ask.csv')
yield_file = os.path.join(data_folder, 'yield-curve.csv')


def load_data(date, timestamp_index, root):
    expiries = get_expiries(root=root, date=date, n_day_threshold=21 * 12)
    l_data = []
    for expiration in expiries:
        strikes = get_strike_list_for_date(root=root, exp=expiration, date=date)
        for strike in strikes:
            for option_type in "PC":
                option_series = get_option_series_with_cache_blocking(
                    root=root, exp=expiration, date=date,
                    strike=strike, option_type=option_type,
                )
                ask_value = float(option_series['ask'][timestamp_index])
                bid_value = float(option_series['bid'][timestamp_index])
                l_data.append([
                    dt.datetime.strftime(date, "%Y/%m/%d"),
                    dt.datetime.strftime(expiration, "%Y/%m/%d"),
                    option_type,
                    strike * 1000,
                    bid_value,
                    ask_value,
                    100.,  # unused
                    "0",
                ])
    header = "date,exdate,cp_flag,strike_price,best_bid,best_offer,impl_volatility,am_settlement"
    data = pd.DataFrame(l_data, columns=header.split(","))
    return data


def create_spx(date, timestamp_index):
    out = load_data(date=date, timestamp_index=timestamp_index, root="SPX")
    return out

def create_vix(date, timestamp_index):
    out = load_data(date=date, timestamp_index=timestamp_index, root="VIX")
    return out

def create_yield(date, timestamp_index):
    #     t = data["yield_curve"]["days"] / 365
    #     rate = data["yield_curve"]["rate"]

    # actually seems unused - just dump some data
    out = load_data(date=date, timestamp_index=timestamp_index, root="VIX")
    return out


def main():
    chosen_date = dt.date(2021, 10, 1)
    # chosen_date = dt.date(2025, 12, 1)

    spx = create_spx(date=chosen_date, timestamp_index=3600 * 7)
    vix = create_vix(date=chosen_date, timestamp_index=3600 * 7)
    discount = create_yield(date=chosen_date, timestamp_index=3600 * 7)

    spx.to_csv(spx_file, index=False)
    vix.to_csv(vix_file, index=False)
    discount.to_csv(yield_file, index=False)



if __name__ == '__main__':
    main()
