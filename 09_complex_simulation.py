from setup import *
from configure import universe_options, cost_reservation, cost_rate, simu_bgn_date, simu_stp_date
from configure import init_premium

# --- load arguments
factor_lbl = sys.argv[1]
universe_id = sys.argv[2].upper()
hold_period_n = int(sys.argv[3])
single_hold_prop = float(sys.argv[4])
start_delay = int(sys.argv[5])

# --- Method ID
method = "COMPLEX"

# --- pid
pid = "{}.{}.HPN{:03d}.SHP{:02d}.D{:02d}".format(
    factor_lbl, universe_id, hold_period_n, int(single_hold_prop * 100), start_delay)

# --- tips
t0 = dt.datetime.now()
print("| {} | {:>12s} | {:>32s} | calculating ... |".format(t0, method, pid))

# --- directory check
check_and_mkdir(complex_simulation_dir)
check_and_mkdir(os.path.join(complex_simulation_dir, method))
check_and_mkdir(os.path.join(complex_simulation_dir, method, "by_pid"))
dir_pid = os.path.join(complex_simulation_dir, method, "by_pid", method + "." + pid)
dir_pid_trades = os.path.join(dir_pid, "trades")
dir_pid_positions = os.path.join(dir_pid, "positions")
check_and_mkdir(dir_pid)
check_and_mkdir(dir_pid_trades)
check_and_mkdir(dir_pid_positions)
remove_files_in_the_dir(dir_pid_trades)
remove_files_in_the_dir(dir_pid_positions)

# 2 - mother universe
mother_universe = universe_options.get(universe_id)

# 3 - load calendar and hist dates list
trade_calendar = CCalendar(SKYRIM_CONST_CALENDAR_PATH)

# 4 - load aux data
instrument_info = CInstrumentInfoTable(t_path=SKYRIM_CONST_INSTRUMENT_INFO_PATH, t_index_label="windCode")
manager_md = CManagerMarketData(t_mother_universe=mother_universe, t_dir_market_data=md_by_instrument_dir, t_dir_major_data=major_minor_dir)
manager_signal = CManagerSignal(
    t_mother_universe=mother_universe, t_available_universe_dir=available_universe_dir,
    t_factors_by_tm_dir=factors_by_tm_dir, t_factor_lbl=factor_lbl,
    t_single_hold_prop=single_hold_prop, t_mgr_md=manager_md,
    t_is_trend_follow=True
)

# 5 - simulation main loop
simu_portfolio = CPortfolio(
    t_pid=method + "." + pid,
    t_init_cash=init_premium, t_cost_reservation=cost_reservation, t_cost_rate=cost_rate,
    t_dir_pid=dir_pid, t_dir_pid_trades=dir_pid_trades, t_dir_pid_positions=dir_pid_positions
)
simu_portfolio.main_loop(
    t_simu_bgn_date=simu_bgn_date, t_simu_stp_date=simu_stp_date, t_start_delay=start_delay, t_hold_period_n=hold_period_n,
    t_trade_calendar=trade_calendar, t_instru_info=instrument_info, t_mgr_signal=manager_signal, t_mgr_md=manager_md
)

#
t1 = dt.datetime.now()
print("| {} | {:>12s} | {:>32s} | calculated  ... | time consuming = {:>6.2f} seconds |".format(t1, method, pid, (t1 - t0).total_seconds()))
