from setup import *
from configure import simu_bgn_date, simu_stp_date, risk_free_rate, top_n
from configure import hold_period_n_list, single_hold_prop_list
from configure import split_date
from itertools import product

method = "COMPLEX"
factor_lbl = sys.argv[1]  # ["MTM231", "RS231", "PVR063"]
universe_id = sys.argv[2]  # ["U0", "U1"]

index_cols = ["HPN", "SHP"]
latex_cols = ["持有期收益", "年化收益", "夏普比率", "最大回撤", "最大回撤时点", "最长回撤期", "最长恢复期"]

check_and_mkdir(evaluation_dir)
check_and_mkdir(os.path.join(evaluation_dir, method))
check_and_mkdir(os.path.join(evaluation_dir, method, "by_comb_id"))

aver_nav_summary_data = []
for hold_period_n, single_hold_prop in product(hold_period_n_list, single_hold_prop_list):
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
    nav_df["AVER"] = nav_df[pid_list].mean(axis=1)
    nav_file = "nav.{}.{}.csv.gz".format(method, comb_id)
    nav_path = os.path.join(evaluation_dir, method, "by_comb_id", nav_file)
    nav_df.to_csv(nav_path, float_format="%.6f")

    # get nav summary
    p_nav = CNAV(t_raw_nav_srs=nav_df["AVER"], t_annual_rf_rate=risk_free_rate, t_freq="D")
    p_nav.cal_all_indicators(t_method="compound")
    d = p_nav.to_dict(t_type="chs")
    d.update({
        "HPN": hold_period_n,
        "SHP": single_hold_prop,
    })
    aver_nav_summary_data.append(d)

    # plot AVER nav
    plot_lines(
        t_plot_df=nav_df[["AVER"]],
        t_vlines_index=[split_date],
        t_fig_name="nav.{}.{}".format(method, comb_id),
        t_save_dir=os.path.join(evaluation_dir, method, "by_comb_id")
    )

aver_nav_summary_df = pd.DataFrame(aver_nav_summary_data).sort_values(by=index_cols, ascending=True).set_index(index_cols)
aver_nav_summary_file = "summary.{}.{}.{}.aver.csv".format(method, factor_lbl, universe_id)
aver_nav_summary_path = os.path.join(evaluation_dir, method, aver_nav_summary_file)
aver_nav_summary_df.to_csv(aver_nav_summary_path, float_format="%.2f")
aver_nav_summary_df[latex_cols].to_csv(aver_nav_summary_path.replace(".csv", ".latex.csv"), float_format="%.2f")
aver_nav_summary_df["年化收益"] = aver_nav_summary_df["年化收益"].astype(float)
aver_nav_summary_df["夏普比率"] = aver_nav_summary_df["夏普比率"].astype(float)

# plot top n
for evaluation_idx in ["年化收益", "夏普比率"]:
    # load summary
    sorted_summary_df = aver_nav_summary_df.sort_values(by=evaluation_idx, ascending=False).head(top_n)
    sorted_summary_file = "summary.{}.{}.{}.aver.top{:02d}.{}.csv".format(method, factor_lbl, universe_id, top_n, evaluation_idx)
    sorted_summary_path = os.path.join(evaluation_dir, method, sorted_summary_file)
    sorted_summary_df.to_csv(sorted_summary_path, float_format="%.2f")

    # load nav data
    top_nav_data = {}
    for hold_period_n, single_hold_prop in sorted_summary_df.index:
        comb_id = "{}.{}.HPN{:03d}.SHP{:02d}".format(
            factor_lbl, universe_id, hold_period_n, int(single_hold_prop * 100)
        )
        nav_file = "nav.{}.{}.csv.gz".format(method, comb_id)
        nav_path = os.path.join(evaluation_dir, method, "by_comb_id", nav_file)
        nav_df = pd.read_csv(nav_path, dtype={"trade_date": str}).set_index("trade_date")
        top_nav_data[comb_id] = nav_df["AVER"]
    top_nav_df = pd.DataFrame(top_nav_data)
    plot_lines(
        t_plot_df=top_nav_df,
        t_vlines_index=[split_date],
        t_fig_name="nav.{}.{}.{}.top{:02d}.{}.aver".format(method, factor_lbl, universe_id, top_n, evaluation_idx),
        t_save_dir=os.path.join(evaluation_dir, method))

    print("=" * 120)
    print(evaluation_idx + "-" + factor_lbl + "-" + universe_id)
    print("-" * 120)
    print(sorted_summary_df)
    print("=" * 120)
    print("\n")
