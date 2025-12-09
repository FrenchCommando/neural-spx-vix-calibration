import datetime as dt
import data.module_external

from market.history_contract import get_strike_list_for_date, get_exp_list_for_date
from utils.dates_and_calendar import count_business_days


def get_expiries(root, date, n_day_threshold):
    out = get_exp_list_for_date(root=root, date=date)
    filtered_out = list(filter(
        lambda d: count_business_days(date_from=date, date_to=d) < n_day_threshold,
        out,
    ))
    return filtered_out


def main():
    chosen_date = dt.date(2025, 12, 1)
    # chosen_date = dt.date(2021, 10, 1)
    chosen_threshold = 21 * 6
    expiries_spx = get_expiries(root="SPX", date=chosen_date, n_day_threshold=chosen_threshold + 21)
    expiries_vix = get_expiries(root="VIX", date=chosen_date, n_day_threshold=chosen_threshold)
    print(f"{len(expiries_spx)} expiries spx {expiries_spx}")
    print(f"{len(expiries_vix)} expiries vix {expiries_vix}")


if __name__ == '__main__':
    main()
