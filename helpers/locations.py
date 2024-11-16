import pandas as pd

def map_county_id_to_state(geo_id):
    # Dictionary mapping state FIPS codes to state names
    fips_to_state = {
        "01": "Alabama", "02": "Alaska", "04": "Arizona", "05": "Arkansas",
        "06": "California", "08": "Colorado", "09": "Connecticut",
        "10": "Delaware", "11": "District of Columbia", "12": "Florida",
        "13": "Georgia", "15": "Hawaii", "16": "Idaho", "17": "Illinois",
        "18": "Indiana", "19": "Iowa", "20": "Kansas", "21": "Kentucky",
        "22": "Louisiana", "23": "Maine", "24": "Maryland", "25": "Massachusetts",
        "26": "Michigan", "27": "Minnesota", "28": "Mississippi", "29": "Missouri",
        "30": "Montana", "31": "Nebraska", "32": "Nevada", "33": "New Hampshire",
        "34": "New Jersey", "35": "New Mexico", "36": "New York",
        "37": "North Carolina", "38": "North Dakota", "39": "Ohio",
        "40": "Oklahoma", "41": "Oregon", "42": "Pennsylvania",
        "44": "Rhode Island", "45": "South Carolina", "46": "South Dakota",
        "47": "Tennessee", "48": "Texas", "49": "Utah", "50": "Vermont",
        "51": "Virginia", "53": "Washington", "54": "West Virginia",
        "55": "Wisconsin", "56": "Wyoming", "60": "American Samoa",
        "66": "Guam", "69": "Northern Mariana Islands", "72": "Puerto Rico",
        "78": "U.S. Virgin Islands"
    }
    
    # Extract the state FIPS code from the geoId (first two digits)
    state_fips = geo_id.split("/")[1][:2]
    
    # Return the corresponding state name
    return fips_to_state.get(state_fips, "Unknown State")


@pd.api.extensions.register_dataframe_accessor("generate_state_column")
class StateColumnGenerator:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def __call__(self, place_column="placeDcid"):
        # Apply the mapping function to the specified column
        self._obj['state'] = self._obj[place_column].apply(map_county_id_to_state)
        return self._obj