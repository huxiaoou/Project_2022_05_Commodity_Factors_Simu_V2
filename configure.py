"""
created @ 2022-03-03
0.  this project is designed to provide some simple simulations to some factors

updated @ 2022-06-07
0.  update the stp_date = "20220607"
"""

stp_date = "20220607"
simu_bgn_date, simu_stp_date = "20150901", stp_date

# universe
concerned_instrument_universe = [
    "AU.SHF",  # "20080109"
    "AG.SHF",  # "20120510"
    "CU.SHF",  # "19950417"
    "AL.SHF",  # "19950417"
    "PB.SHF",  # "20140801"
    "ZN.SHF",  # "20070326"
    "SN.SHF",  # "20151102"
    "NI.SHF",  # "20150327"
    "SS.SHF",  # "20190925"
    "RB.SHF",  # "20090327"
    "HC.SHF",  # "20140321"
    "J.DCE",  # "20110415"
    "JM.DCE",  # "20130322"
    "I.DCE",  # "20131018"
    "FG.CZC",  # "20121203"
    "SA.CZC",  # "20191206"
    "UR.CZC",  # "20190809"
    "ZC.CZC",  # "20151201"
    "SF.CZC",  # "20140808"
    "SM.CZC",  # "20140808"
    "Y.DCE",  # "20060109"
    "P.DCE",  # "20071029"
    "OI.CZC",  # "20130423"
    "M.DCE",  # "20000717"
    "RM.CZC",  # "20121228"
    "A.DCE",  # "19990104"
    "RU.SHF",  # "19950516"
    "BU.SHF",  # "20131009"
    "FU.SHF",  # "20040825"  # re-active since 20180801
    "L.DCE",  # "20070731"
    "V.DCE",  # "20090525"
    "PP.DCE",  # "20140228"
    "EG.DCE",  # "20181210"
    "EB.DCE",  # "20191206"
    "PG.DCE",  # "20200330"
    "TA.CZC",  # "20061218"
    "MA.CZC",  # "20141224"
    "CF.CZC",  # "20040601"
    "CY.CZC",  # "20170808"
    "SR.CZC",  # "20060106"
    "C.DCE",  # "20040922"
    "CS.DCE",  # "20141219"
    "SP.SHF",  # "20181127"
    "JD.DCE",  # "20131108"
    "AP.CZC",  # "20171222"
    "CJ.CZC",  # "20190430"
]
ciu_size = len(concerned_instrument_universe)  # should be 46

universe_options = {
    "U2": [
        "CU.SHF",  # "19950417"
        "AL.SHF",  # "19950417"
        "PB.SHF",  # "20140801"
        "ZN.SHF",  # "20070326"
        "SN.SHF",  # "20151102"
        "NI.SHF",  # "20150327"
        "RB.SHF",  # "20090327"
        "HC.SHF",  # "20140321"
        "J.DCE",  # "20110415"
        "JM.DCE",  # "20130322"
        "I.DCE",  # "20131018"
        "FG.CZC",  # "20121203"
        "Y.DCE",  # "20060109"
        "P.DCE",  # "20071029"
        "OI.CZC",  # "20130423"
        "M.DCE",  # "20000717"
        "RM.CZC",  # "20121228"
        "A.DCE",  # "19990104"
        "RU.SHF",  # "19950516"
        "BU.SHF",  # "20131009"
        "L.DCE",  # "20070731"
        "V.DCE",  # "20090525"
        "PP.DCE",  # "20140228"
        "TA.CZC",  # "20061218"
        "MA.CZC",  # "20141224"
        "CF.CZC",  # "20040601"
        "SR.CZC",  # "20060106"
        "C.DCE",  # "20040922"
        "CS.DCE",  # "20141219"
    ],
}

# --- test return ---
single_hold_prop_list = [0.2, 0.3, 0.4]
hold_period_n_list = [5, 10, 15, 20]
robust_single_hold_prop_list = [0.15, 0.20, 0.25]
robust_hold_period_n_list = [8, 10, 12]
test_lag = 1

# secondary parameters
RETURN_SCALE = 100
cost_rate = 5e-4
cost_reservation = 0e-4
risk_free_rate = 0
top_n = 5
init_premium = 10000 * 1e4

# additional
split_date = "20220301"
