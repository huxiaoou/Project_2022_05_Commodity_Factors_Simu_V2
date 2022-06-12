import os
import sys
import datetime as dt
import numpy as np
import pandas as pd
from skyrim.whiterun import CCalendar, CInstrumentInfoTable
from skyrim.winterhold import check_and_mkdir, remove_files_in_the_dir, plot_lines, plot_corr, plot_twinx, plot_bar
from skyrim.riften import CNAV
# from skyrim.configurationOffice import SKYRIM_CONST_CALENDAR_PATH, SKYRIM_CONST_INSTRUMENT_INFO_PATH
from skyrim.configurationHome import SKYRIM_CONST_CALENDAR_PATH, SKYRIM_CONST_INSTRUMENT_INFO_PATH
from skyrim.riverwood import CManagerSignal, CManagerMarketData, CPortfolio

pd.set_option("display.width", 0)
pd.set_option("display.float_format", "{:.2f}".format)
np.set_printoptions(6, suppress=True)

factor_lib = os.path.join("G:\\", "Works", "2022", "Project_2022_05_Commodity_Factors_Library_V2", "data")
instrument_return_dir = os.path.join(factor_lib, "instruments_return")
factors_by_tm_dir = os.path.join(factor_lib, "factors_by_tm")
available_universe_dir = os.path.join(factor_lib, "available_universe")

futures_dir = os.path.join("C:\\", "Users", "huxia", "OneDrive", "文档", "Trading", "", "DataBase", "Futures")
futures_instrument_mkt_data_dir = os.path.join(futures_dir, "instrument_mkt_data")
major_minor_dir = os.path.join(futures_dir, "by_instrument", "major_minor")
md_by_instrument_dir = os.path.join(futures_dir, "by_instrument", "md")


project_data_dir = os.path.join(".", "data")
complex_simulation_dir = os.path.join(project_data_dir, "complex_simulation")
evaluation_dir = os.path.join(project_data_dir, "evaluation")
by_year_dir = os.path.join(project_data_dir, "by_year")
evaluation_robust_dir = os.path.join(project_data_dir, "evaluation_robust")
groupby_dir = os.path.join(project_data_dir, "groupby")
