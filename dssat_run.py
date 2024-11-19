import pandas as pd
from datetime import datetime, timedelta
from spatialDSSAT.run import GSRun

import os
CWD = os.getcwd()

pixel_data = pd.read_csv(f"data/pixel_input_selected_districts.csv")
pixel_data = pixel_data.set_index("admin_2")

cultivars = pd.read_csv("data/skilled_cultivars.csv")
cultivars = cultivars.set_index("admin_2")

N_FERT_APPS = 10
N_RATIO = 1. # Average Nitrogen content from main fertilzer products
N_ENS = 50

def run_district(admin_2, year, nitro_rate=0, sim_controls={}):
    """
    Runs N_ENS (50) random simulations for the admin_2 district in the specified
    year.
    
    The only management that is direct input in this function is the total 
    nitrogen fertilizer rate in the season. Other management practices such as 
    planting dates and irrigation can be defined by passing as automatic management
    in the 'sim_controls' argument. 
    
    Arguments
    ----------
    admin_2: str
        District name. Districts have been previously defined according to the
        regions where IPs are working. Those districts are: 
            'Buhera', 'Mutare Rural', 'Chivi', 'Zaka', 'Binga', 'Hwange Rural',
            'Lupane', 'Nkayi', 'Tsholotsho'
    year: int
        Season to simulate. 
    nitro_rate: float
        Total nitrogen rate to apply in the season
    sim_controls: dict
        Simulation control options. See 
        https://github.com/daquinterop/spatialDSSAT/blob/main/spatialDSSAT/run.py#L45
    """
    pixels = pixel_data.loc[admin_2]
    pixels = pixels.dropna()
    nitrogen_list = []
    cultivar_list = []
    planting_list = []
    weather_list = []
    soil_list = []
    nitrogen_rate = nitro_rate*N_RATIO/N_FERT_APPS
    for _ in range(N_ENS):
        cultivar_row = cultivars.loc[[admin_2]].sample().iloc[0]
        weather_pixel_row = pixels.sample().iloc[0]
        
        cultivar_list.append(cultivar_row.cultivar)
        # Fertilization timing is relative to the cultivar Length of Season (LOS)
        fert_timerange = int(.7*cultivar_row.los/N_FERT_APPS)
        nitrogen_list.append(
            [(0+i*fert_timerange, nitrogen_rate) for i in range(N_FERT_APPS)]
        )
        planting_list.append(
            datetime(year, 1, 1) + timedelta(days=int(weather_pixel_row.SoS))
        )
        weather_list.append(eval(weather_pixel_row.pixel))
        # Random for Soil. The soil file for that pixel exists.
        soil_pixel_row = pixels.sample().iloc[0]
        soil_list.append(eval(soil_pixel_row.pixel))

    gsRun = GSRun("Maize")
    iterator = list(zip(soil_list, weather_list, nitrogen_list, planting_list, cultivar_list))
    for soil, weather, nitro, pld, cul in iterator:  
        soilfile = f"{soil[0]:07.2f}_{soil[1]:07.2f}".replace(".", "p")+".SOL"
        soil_path = f"{CWD}/data/DSSAT_input/Soil/{soilfile}"
        wthfile = f"{weather[0]:07.2f}_{weather[1]:07.2f}_{str(year)[2:]}01".replace(".", "p")+".WTH"
        wthfile_path = f"{CWD}/data/DSSAT_input/Weather/{wthfile}"
        planting_options = {
            "PDATE": pld, "EDATE": -99, "PPOP": 4.5, "PPOE": 4.5, "PLME": "S",
            "PLDS": "R", "PLRS": 90, "PLRD": 0, "PLDP": 3, "PLWT": 0,
            "PAGE": -99, "PENV": -99, "PLPH": -99, "SPRL": -99
        }
        gsRun.add_treatment(
            soil=soil_path, weather=wthfile_path, 
            nitrogen=nitro, planting=planting_options, cultivar=cul
        )
    
    out = gsRun.run(
        start_date=datetime(year, 8, 10), # Zimbabwe main
        latest_date=max(planting_list) + timedelta(360),
        sim_controls=sim_controls
    )
    out["weather_pixel"] = weather_list
    out["soil_pixel"] = soil_list
    out["cultivar"] = cultivar_list
    out["planting"] = planting_list
    return out, gsRun.overview

# run_district("Chivi", 2020)
