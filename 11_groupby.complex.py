from setup import *
from configure import simu_bgn_date, simu_stp_date, risk_free_rate
from configure import split_date

method = "COMPLEX"
factor_lbl = sys.argv[1]  # ["MTM231", "RS231", "PVR063"]
universe_id = sys.argv[2]  # ["U0", "U1"]
hold_period_n = int(sys.argv[3])
single_hold_prop = float(sys.argv[4])

latex_cols = ["持有期收益", "年化收益", "夏普比率", "最大回撤", "最大回撤时点", "最长回撤期", "最长恢复期"]

check_and_mkdir(groupby_dir)
check_and_mkdir(os.path.join(groupby_dir, method))

comb_id = "{}.{}.HPN{:03d}.SHP{:02d}".format(
    factor_lbl, universe_id, hold_period_n, int(single_hold_prop * 100)
)

# for each delay in hold period n
pid_list = [comb_id + ".D{:02d}".format(delay_id) for delay_id in range(hold_period_n)]
nav_data = {}
for pid in pid_list:
    model_file = "{}.{}.nav.daily.csv.gz".format(method, pid)
    model_path = os.path.join(complex_simulation_dir, method, "by_pid", method + "." + pid, model_file)
    model_df = pd.read_csv(model_path, dtype={"trade_date": str}).set_index("trade_date")
    nav_data[pid] = model_df["navps"]

# average nav for all the delay
nav_df = pd.DataFrame(nav_data).fillna(1)
filter_date = (nav_df.index >= simu_bgn_date) & (nav_df.index < simu_stp_date)
nav_df = nav_df.loc[filter_date]

# analyze nav by pid
aver_nav_summary_data = []
for pid in pid_list:
    p_nav = CNAV(t_raw_nav_srs=nav_df[pid], t_annual_rf_rate=risk_free_rate, t_freq="D")
    p_nav.cal_all_indicators(t_method="compound")
    d = p_nav.to_dict(t_type="chs")
    d.update({
        "D": "$D_{}$".format(int(pid.split(".")[-1][-2:])),
    })
    aver_nav_summary_data.append(d)

aver_nav_summary_df = pd.DataFrame(aver_nav_summary_data).sort_values(by="D", ascending=True).set_index("D")
aver_nav_summary_file = "summary.{}.{}.by_pid.csv".format(method, comb_id)
aver_nav_summary_path = os.path.join(groupby_dir, method, aver_nav_summary_file)
aver_nav_summary_df.to_csv(aver_nav_summary_path, float_format="%.2f")
aver_nav_summary_df[latex_cols].to_csv(aver_nav_summary_path.replace(".csv", ".latex.csv"), float_format="%.2f")
print(aver_nav_summary_df)
plot_lines(
    t_plot_df=nav_df[pid_list],
    t_vlines_index=[split_date],
    t_colormap="jet",
    t_fig_name="nav.{}.{}.by_pid".format(method, comb_id),
    t_save_dir=os.path.join(groupby_dir, method)
)

# analyze nav by group
for G in [3, 5]:
    sub_nav_summary_data = []
    gid_list = ["G{:02d}".format(gi) for gi in range(G)]
    k = int(hold_period_n / G) if hold_period_n % G == 0 else int(hold_period_n // G + 1)
    for gi, gid in enumerate(gid_list):
        sub_pid_list = [comb_id + ".D{:02d}".format((gi + z*G) % hold_period_n) for z in range(k)]
        nav_df[gid] = nav_df[sub_pid_list].mean(axis=1)
        p_nav = CNAV(t_raw_nav_srs=nav_df[gid], t_annual_rf_rate=risk_free_rate, t_freq="D")
        p_nav.cal_all_indicators(t_method="compound")
        d = p_nav.to_dict(t_type="chs")
        d.update({"G": gid})
        sub_nav_summary_data.append(d)
    sub_nav_summary_df = pd.DataFrame(sub_nav_summary_data).sort_values(by="G", ascending=True).set_index("G")
    sub_nav_summary_file = "summary.{}.{}.by_group.G{}.csv".format(method, comb_id, G)
    sub_nav_summary_path = os.path.join(groupby_dir, method, sub_nav_summary_file)
    sub_nav_summary_df.to_csv(sub_nav_summary_path, float_format="%.2f")
    sub_nav_summary_df[latex_cols].to_csv(sub_nav_summary_path.replace(".csv", ".latex.csv"), float_format="%.2f")
    print(sub_nav_summary_df)

    # plot nav by subgroup
    plot_lines(
        t_plot_df=nav_df[gid_list],
        t_vlines_index=[split_date],
        t_colormap="jet",
        t_fig_name="nav.{}.{}.by_group.G{}".format(method, comb_id, G),
        t_save_dir=os.path.join(groupby_dir, method)
    )
