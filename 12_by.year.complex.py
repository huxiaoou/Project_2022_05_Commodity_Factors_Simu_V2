from setup import *
from configure import risk_free_rate, split_date

# arguments
method = "COMPLEX"
factor_lbl = sys.argv[1]  # "RSW252HL063"
universe_id = sys.argv[2].upper()  # "U2"
hold_period_n = int(sys.argv[3])  # 5
single_hold_prop = float(sys.argv[4])  # 0.2
comb_id = "{}.{}.HPN{:03d}.SHP{:02d}".format(
    factor_lbl, universe_id, hold_period_n, int(single_hold_prop * 100)
)

# core settings
check_and_mkdir(by_year_dir)
check_and_mkdir(os.path.join(by_year_dir, method))
index_cols = "年"
latex_cols = ["天数", "持有期收益", "年化收益", "夏普比率", "最大回撤", "最大回撤时点", "最长回撤期", "最长恢复期"]

# load nav file
nav_file = "nav.{}.{}.csv.gz".format(method, comb_id)
nav_path = os.path.join(evaluation_dir, method, "by_comb_id", nav_file)
nav_df = pd.read_csv(nav_path, dtype={"trade_date": str}).set_index("trade_date")
nav_df["trade_year"] = nav_df.index.map(lambda z: z[0:4])
print(nav_df.head(20))

# by year
by_year_nav_summary_data = []
for trade_year, trade_year_df in nav_df.groupby(by="trade_year"):
    # get nav summary
    p_nav = CNAV(t_raw_nav_srs=trade_year_df["AVER"], t_annual_rf_rate=risk_free_rate, t_freq="D")
    p_nav.cal_all_indicators(t_method="compound")
    d = p_nav.to_dict(t_type="chs")
    d.update({
        "年": trade_year,
        "天数": len(trade_year_df),
    })
    by_year_nav_summary_data.append(d)

    plot_lines(
        t_plot_df=trade_year_df[["AVER"]],
        t_vlines_index=[split_date] if trade_year == split_date[0:4] else None,
        t_fig_name="nav.{}.{}.Y{}".format(method, comb_id, trade_year),
        t_save_dir=os.path.join(by_year_dir, method)
    )

aver_nav_summary_df = pd.DataFrame(by_year_nav_summary_data).sort_values(by=index_cols, ascending=True).set_index(index_cols)
aver_nav_summary_file = "summary.{}.{}.by_year.csv".format(method, comb_id)
aver_nav_summary_path = os.path.join(by_year_dir, method, aver_nav_summary_file)
aver_nav_summary_df.to_csv(aver_nav_summary_path, float_format="%.2f")
aver_nav_summary_df[latex_cols].to_csv(aver_nav_summary_path.replace(".csv", ".latex.csv"), float_format="%.2f")
print(aver_nav_summary_df)
