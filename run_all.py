from threading import Thread
from configure import universe_options
from configure import hold_period_n_list, single_hold_prop_list
from configure import robust_hold_period_n_list, robust_single_hold_prop_list
from custom_funs import fun_for_cal_evaluation, fun_for_cal_evaluation_robust
from custom_funs import fun_for_cal_complex_simulation

switch = {
    "complex": True,
    "complex_robust": False,
    "evaluation": True,
    "evaluation_robust": False,
}

if switch["complex"]:
    target_factors_lbl_list = [
        "SKEW010", "SKEW021", "SKEW063", "SKEW126", "SKEW189", "SKEW252",
        "BETA010", "BETA021", "BETA063", "BETA126", "BETA189", "BETA252",
    ]
    target_universe_id_list = list(universe_options.keys())
    target_hold_period_n_list = hold_period_n_list
    target_single_hold_prop_list = single_hold_prop_list
    skip_when_exists = True

    gn = 8  #
    join_list = []
    for group_id in range(gn):
        t = Thread(
            target=fun_for_cal_complex_simulation,
            args=(
                group_id, gn,
                target_factors_lbl_list, target_universe_id_list,
                target_hold_period_n_list, target_single_hold_prop_list,
                skip_when_exists
            )
        )
        t.start()
        join_list.append(t)
    for t in join_list:
        t.join()

if switch["complex_robust"]:
    target_factors_lbl_list = ["RS240", "RS252", "RS260"]
    target_universe_id_list = list(universe_options.keys())
    target_hold_period_n_list = robust_hold_period_n_list
    target_single_hold_prop_list = robust_single_hold_prop_list
    skip_when_exists = True

    gn = 4  #
    join_list = []
    for group_id in range(gn):
        t = Thread(
            target=fun_for_cal_complex_simulation,
            args=(
                group_id, gn,
                target_factors_lbl_list, target_universe_id_list,
                target_hold_period_n_list, target_single_hold_prop_list,
                skip_when_exists
            )
        )
        t.start()
        join_list.append(t)
    for t in join_list:
        t.join()

if switch["evaluation"]:
    fun_for_cal_evaluation(
        [
            "SKEW010", "SKEW021", "SKEW063", "SKEW126", "SKEW189", "SKEW252",
            "BETA010", "BETA021", "BETA063", "BETA126", "BETA189", "BETA252",
        ],
        list(universe_options.keys())
    )

if switch["evaluation_robust"]:
    fun_for_cal_evaluation_robust(
        ["RS240", "RS252", "RS260"],
        list(universe_options.keys())
    )
