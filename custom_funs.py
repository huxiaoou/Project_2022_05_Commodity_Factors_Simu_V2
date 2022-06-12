from setup import *
from itertools import product
import subprocess


def split_nav_by_year(t_nav_srs: pd.Series):
    _nav_df = pd.DataFrame({"nav": t_nav_srs})
    _nav_df["ret"] = _nav_df["nav"] / _nav_df["nav"].shift(1).fillna(method="bfill") - 1
    _nav_df["year"] = _nav_df.index.map(lambda z: z[0:4])
    _res = {}
    for trade_year, trade_year_df in _nav_df.groupby(by="year"):
        _res[trade_year] = trade_year_df["ret"]
    return _res


def get_opt_weight_df_fixed_single_hold_prop(t_available_universe_df: pd.DataFrame, t_factor_df: pd.DataFrame, t_factor_lbl: str, t_single_hold_prop: float, t_type: int):
    """

    :param t_available_universe_df:
    :param t_factor_df: strategy would long instrument with large factor value and short instrument with small factor value
    :param t_factor_lbl:
    :param t_single_hold_prop:
    :param t_type: {0:"Both", 1:"Long only", 2:"Short only"}
    :return:
    """
    _opt_weight_df = pd.merge(
        left=t_available_universe_df, right=t_factor_df,
        left_on="instrument", right_index=True, how="inner"
    ).set_index("instrument").sort_values(by=t_factor_lbl, ascending=False)
    _opt_universe = list(_opt_weight_df.index)
    _opt_universe_size = len(_opt_universe)
    if _opt_universe_size > 1:
        _k0 = max(min(int(np.ceil(_opt_universe_size * t_single_hold_prop)), int(_opt_universe_size / 2)), 1)
        _k1 = _opt_universe_size - 2 * _k0
        if t_type == 1:
            _opt_weight_df["opt"] = [1 / _k0] * _k0 + [0.0] * _k1 + [0.0] * _k0
        elif t_type == 2:
            _opt_weight_df["opt"] = [0.0] * _k0 + [0.0] * _k1 + [-1 / _k0] * _k0
        else:
            _opt_weight_df["opt"] = [1 / 2 / _k0] * _k0 + [0.0] * _k1 + [-1 / 2 / _k0] * _k0
    else:
        _opt_weight_df["opt"] = 0
    return _opt_weight_df["opt"].to_dict(), _opt_universe


def fun_for_cal_complex_simulation(t_group_id: int, t_gn: int,
                                   t_factor_lbl_list: list, t_universe_id_list: list,
                                   t_hold_period_n_list: list, t_single_hold_prop_list: list,
                                   t_skip_when_exists: bool
                                   ):
    iter_list = product(t_factor_lbl_list, t_universe_id_list, t_hold_period_n_list, t_single_hold_prop_list)
    method = "COMPLEX"
    for it, (factor_lbl, universe_id, hold_period_n, single_hold_prop) in enumerate(iter_list):
        if it % t_gn == t_group_id:
            for start_delay in range(hold_period_n):
                pid = "{}.{}.HPN{:03d}.SHP{:02d}.D{:02d}".format(
                    factor_lbl, universe_id, hold_period_n, int(single_hold_prop * 100), start_delay)
                model_file = "{}.{}.nav.daily.csv.gz".format(method, pid)
                model_path = os.path.join(complex_simulation_dir, method, "by_pid", method + "." + pid, model_file)
                if os.path.exists(model_path) and t_skip_when_exists:
                    continue
                else:
                    subprocess.run([
                        "python", "09_complex_simulation.py",
                        factor_lbl, universe_id, str(hold_period_n), "{:.2f}".format(single_hold_prop), str(start_delay)
                    ])
    return 0


def fun_for_cal_evaluation(t_factor_list: list, t_uid_list: list):
    for factor_lbl, universe_id in product(t_factor_list, t_uid_list):
        subprocess.run(["python", "10_evaluation.complex.py", factor_lbl, universe_id])
    return 0


def fun_for_cal_evaluation_robust(t_factor_list: list, t_uid_list: list):
    for factor_lbl, universe_id in product(t_factor_list, t_uid_list):
        subprocess.run(["python", "10_evaluation.complex.robust.py", factor_lbl, universe_id])
    return 0
