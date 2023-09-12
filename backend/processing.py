########################
# ASTRO PERFECT MATCH #
########################

########################
# Required Libraries
########################
import requests
import os
from dotenv import load_dotenv
import pandas as pd
import json
import warnings
from spritbounds import ruh_ikizi_durumu, ruh_esi
warnings.filterwarnings("ignore", category=FutureWarning)

# Required libraries for the model
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

###################
# Display settings
###################
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', 200)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

########################################
# READING ENV FILE - FOR API
####################################### 

path= f"{os.getcwd()}/.env"

load_dotenv(path) # should return true when this runs

print(os.getcwd()) # shows the directory where you are working

print(path) # Make sure that the output of path actually references where the .env file is located.

######################################
# DATE OF BIRTH INFORMATION OF PERSONS 
######################################

##########################
# Perfect Macth Function
##########################

def perfectmatch(json1,json2):


    def apiRequester(DAY,MONTH,YEAR,HOUR,MIN,LAT,LON,TZONE):
        headers = {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Authorization': f'Basic {os.getenv("AUTH")}'
                }

        url = f'{os.getenv("API")}'
        payload = f"day={DAY}&month={MONTH}&year={YEAR}&hour={HOUR}&min={MIN}&lat={LAT}&lon={LON}&tzone={TZONE}"
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text

    astroinfo = apiRequester(**json1)
    astroinfo2 = apiRequester(**json2)

    astroinfo_f = json.loads(astroinfo)
    astroinfo_s = json.loads(astroinfo2)

    #####################
    # first person's df
    #####################

    # Extract planets data
    planets_data1 = astroinfo_f['planets']

    # Create a DataFrame for planets
    planets_df1 = pd.DataFrame(planets_data1)

    # Extract houses data
    houses_data1 = astroinfo_f['houses']

    # Create a DataFrame for houses
    houses_df1 = pd.DataFrame(houses_data1)

    # Extract lilith data
    lilith_data1 = astroinfo_f['lilith']

    # Create a DataFrame for lilith
    lilith_df1 = pd.DataFrame([lilith_data1])

    # Extract aspects data
    aspects_data1 = astroinfo_f['aspects']

    # Create a DataFrame for aspects
    aspects_df1 = pd.DataFrame(aspects_data1)

    #####################
    # second person's df
    #####################

    # Extract planets data
    planets_data2 = astroinfo_s['planets']

    # Create a DataFrame for planets
    planets_df2 = pd.DataFrame(planets_data2)

    # Extract houses data
    houses_data2 = astroinfo_s['houses']

    # Create a DataFrame for houses
    houses_df2 = pd.DataFrame(houses_data2)

    # Extract lilith data
    lilith_data2 = astroinfo_s['lilith']

    # Create a DataFrame for lilith
    lilith_df2 = pd.DataFrame([lilith_data2])

    # Extract aspects data
    aspects_data2 = astroinfo_s['aspects']

    # Create a DataFrame for aspects
    aspects_df2 = pd.DataFrame(aspects_data2)

    ##################
    # Project Workflow
    ##################

    # A- Data Preparation
    # Line 12 of 1- df's Part of Fortune will fly
    # 2- Lilith dfler will be completely deleted
    # 3- Full degree, speed and retro will be deleted from the columns.
    # 4- Aspect df's will be deleted completely. (We will create new aspects according to two df's).
    # 5- Planets_df1 and houses_df1 will be merged to get rid of the df crowd. (According to the house, the signs will be preserved with two separate columns)
    # 6- Planets_df2 and houses_df2 will be merged to get rid of the Df clutter (by house, with two separate columns to keep the signs)
    # 7- Two people's dfi will be merged. (1 and 2 will be added at the end of the column names to protect the person information)

    # B- Feature Extraction
    # 1- From the node (the node in the df is the NORTH Lunar Node i.e. NAD, we will assign the opposite sign as GAD i.e. SOUTH Lunar Node).
    # 2- MC, ASC, DSC and IC will be calculated (MC = 10th house, ASC=1st house, DSC=7th house, IC=4th house, House will be subtracted from df)
    # 3- Juno Asteroid will be added. (The standard will be set to 15 degrees as the degree cannot be determined)
    # 4- The angles will be calculated (the angles between the planets in the merge dft will be calculated. THE CONDITION OF BEING IN THE SAME SIGN MUST BE TAKEN INTO ACCOUNT)

    # C- Model Building 
    # 1- Operations such as classifying POSITIVE and NEGATIVE descriptions, scoring or making 1-0 will be done. It will be tried.
    # 2- The option to create a data set with conditions will be tried.

    ##############################################################################################################################
    #####################
    # A- Data Preparation
    #####################

    ################################################
    # 1- Line 12 Part of Fortune deleted from df's
    ################################################
    planets_df1 = planets_df1[planets_df1['name'] != 'Part of Fortune']
    planets_df2 = planets_df2[planets_df2['name'] != 'Part of Fortune']

    ##########################
    # 2- Lilith dfs deleted 
    ##########################
    del lilith_df1
    del lilith_df2

    ##########################################################
    # 3- Full degree, speed and retro deleted from the columns.
    ##########################################################

    columns_to_drop1 = ["full_degree", "speed", "is_retro"]
    planets_df1.drop(columns=columns_to_drop1, inplace=True)

    columns_to_drop2 = ["full_degree", "speed", "is_retro"]
    planets_df2.drop(columns=columns_to_drop2, inplace=True)

    #################################################################################
    # 4- Aspect df's deleted. (We will create new aspects according to the two df's).
    #################################################################################
    del aspects_df1
    del aspects_df2

    ################################################################################################################################
    # 5- Planets_df1 and houses_df1 will be merged to get rid of df clutter (by house, with two separate columns to keep the signs)
    ################################################################################################################################
    person_df1 = planets_df1.merge(houses_df1, on='house', suffixes=('_planet', '_house'))

    ################################################################################################################################
    # 6- Planets_df2 and houses_df2 will be merged to get rid of df clutter (by house, with two separate columns to keep the signs)
    ################################################################################################################################
    person_df2 = planets_df2.merge(houses_df2, on='house', suffixes=('_planet', '_house'))

    ###########################################################################################################################
    # 7- The dfi of two people will be merged (1 and 2 added at the end of the column names to protect the person information)
    ###########################################################################################################################

    # Column name adjustment in first and second person's df
    person_df1.rename(columns={"name": "name1", "norm_degree": "norm_degree1", "sign_id": "sign_id1", "sign_planet": "sign_planet1",
                                "house": "house1", "sign_house": "sign_house1", "degree": "degree1"}, inplace=True)

    person_df2.rename(columns={"name": "name2", "norm_degree": "norm_degree2", "sign_id": "sign_id2", "sign_planet": "sign_planet2",
                                "house": "house2", "sign_house": "sign_house2", "degree": "degree2"}, inplace=True)


    # Let's create a list containing the order we have determined for the index to be regular
    custom_order = ["Sun", "Moon", "Venus", "Mars", "Mercury", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Chiron", "Node"]

    # We convert the "name1" column to categorical data
    person_df1['name1'] = pd.Categorical(person_df1['name1'], categories=custom_order, ordered=True)

    # We sort by column "name1"
    sorted_df = person_df1.sort_values('name1').reset_index(drop=True)

    # We convert the "name2" column to categorical data
    person_df2['name2'] = pd.Categorical(person_df2['name2'], categories=custom_order, ordered=True)

    # Sort by column "name2"
    sorted_df2 = person_df2.sort_values('name2').reset_index(drop=True)

    # Merging two df
    merged_df_ = pd.concat([sorted_df, sorted_df2], axis=1)

    #########################################################
    # A copy of the df to get back quickly
    merged_df = merged_df_.copy()

    #########################################################

    #####################
    # B- Feature Extraction
    #####################

    ####################################
    # 1- Generating a SNode from a Node
    ####################################
    
    def find_snode (sign1):
        opposite = {
            "Aries": "Libra",
            "Taurus": "Scorpio",
            "Gemini": "Sagittarius",
            "Cancer": "Capricorn",
            "Leo": "Aquarius",
            "Virgo": "Pisces",
            "Libra": "Aries",
            "Scorpio": "Taurus",
            "Sagittarius": "Gemini",
            "Capricorn": "Cancer",
            "Aquarius": "Leo",
            "Pisces": "Virgo"
        }

        return opposite.get(sign1,None)


    def find_signid (signid1):
        opposite = {
            1: 7,
            2: 8,
            3: 9,
            4: 10,
            5: 11,
            6: 12,
            7: 1,
            8: 2,
            9: 3,
            10: 4,
            11: 5,
            12: 6
        }

        return opposite.get(signid1,None)


    def find_house (house1):
        opposite = {
            1: 7,
            2: 8,
            3: 9,
            4: 10,
            5: 11,
            6: 12,
            7: 1,
            8: 2,
            9: 3,
            10: 4,
            11: 5,
            12: 6
        }

        return opposite.get(house1,None)

    def find_shouse (signhouse):
        opposite = {
            "Aries": "Libra",
            "Taurus": "Scorpio",
            "Gemini": "Sagittarius",
            "Cancer": "Capricorn",
            "Leo": "Aquarius",
            "Virgo": "Pisces",
            "Libra": "Aries",
            "Scorpio": "Taurus",
            "Sagittarius": "Gemini",
            "Capricorn": "Cancer",
            "Aquarius": "Leo",
            "Pisces": "Virgo"
        }

        return opposite.get(signhouse,None)

    # Duplicate line 11
    row_11_copy = merged_df.iloc[11].copy()

    # Replace "name1" and "name2" columns with the opposite of "Node"
    row_11_copy["sign_planet1"] = find_snode(row_11_copy["sign_planet1"])
    row_11_copy["sign_planet2"] = find_snode(row_11_copy["sign_planet2"])

    # "Replace "sign_id1" and "sign_id2" columns with the opposite
    row_11_copy["sign_id1"] = find_signid(row_11_copy["sign_id1"])
    row_11_copy["sign_id2"] = find_signid(row_11_copy["sign_id2"])

    # Replace columns "house1" and "house2" with the opposite
    row_11_copy["house1"] = find_house(row_11_copy["house1"])
    row_11_copy["house2"] = find_house(row_11_copy["house2"])

    # Replace "sign_house1" and "sign_house2" columns with the opposite
    row_11_copy["sign_house1"] = find_shouse(row_11_copy["sign_house1"])
    row_11_copy["sign_house2"] = find_shouse(row_11_copy["sign_house2"])

    # Insert as line 12
    merged_df = merged_df.append(row_11_copy, ignore_index=True)

    merged_df.iloc[12] = merged_df.iloc[12].replace("Node", "SNode")

    ########################################
    # MC,ASC,DSC and IC calculated. 
    ########################################

    # for house_df1;

    # In column "house" we select rows with value 10
    selected_rows_MC = houses_df1[houses_df1["house"] == 10]
    selected_rows_IC = houses_df1[houses_df1["house"] == 4]
    selected_rows_ASC = houses_df1[houses_df1["house"] == 1]
    selected_rows_DSC = houses_df1[houses_df1["house"] == 7]

    # We add the new column "name" and fill it with "MC"
    selected_rows_MC["name1"] = "MC"
    selected_rows_IC["name1"] = "IC"
    selected_rows_ASC["name1"] = "ASC"
    selected_rows_DSC["name1"] = "DSC"

    # We add the selected rows to the existing DataFrame
    houses_df1 = houses_df1.append(selected_rows_MC, ignore_index=True)
    houses_df1 = houses_df1.append(selected_rows_IC, ignore_index=True)
    houses_df1 = houses_df1.append(selected_rows_ASC, ignore_index=True)
    houses_df1 = houses_df1.append(selected_rows_DSC, ignore_index=True)


    # Add MC, IC, ASC, DSC of houses_df1 to merged_df;
    def add_rows_from_another_df1(main_df, source_df, row_indices, rename_columns=None):
        """
        This function inserts specific rows from another DataFrame into a DataFrame.

        :param main_df: The destination DataFrame, the DataFrame where the new rows should be inserted.
        :param source_df: Source DataFrame, the DataFrame containing the rows to be inserted.
        :param row_indices: List of indexes of the rows to be added.
        :param rename_columns: Can be used to rename the names of the columns, if desired.
        """
        for index in row_indices:
            selected_row = source_df.iloc[index]
            # Adding the selected row to the "merged_df" DataFrame and assigning it to columns
            new_data = {
                'name1': selected_row['name1'],
                'sign_planet1': selected_row['sign'],
                'degree1': selected_row['degree'],
                'house1': selected_row['house']
            }

            main_df = main_df.append(new_data, ignore_index=True)

        return main_df

    h_df1_s = (12, 13, 14, 15)  # MC, IC, ASC, DSC rows of houses_df1.

    add_rows_from_another_df1(merged_df, houses_df1, h_df1_s)

    merged_df = add_rows_from_another_df1(merged_df, houses_df1, h_df1_s)

    # for house_df2;

    # In column "house" we select rows with value 10
    selected_rows_MC = houses_df2[houses_df2["house"] == 10]
    selected_rows_IC = houses_df2[houses_df2["house"] == 4]
    selected_rows_ASC = houses_df2[houses_df2["house"] == 1]
    selected_rows_DSC = houses_df2[houses_df2["house"] == 7]

    # We add the new column "name" and fill it with "MC"
    selected_rows_MC["name2"] = "MC"
    selected_rows_IC["name2"] = "IC"
    selected_rows_ASC["name2"] = "ASC"
    selected_rows_DSC["name2"] = "DSC"

    # We add the selected rows to the existing DataFrame
    houses_df2 = houses_df2.append(selected_rows_MC, ignore_index=True)
    houses_df2 = houses_df2.append(selected_rows_IC, ignore_index=True)
    houses_df2 = houses_df2.append(selected_rows_ASC, ignore_index=True)
    houses_df2 = houses_df2.append(selected_rows_DSC, ignore_index=True)

    # MC, IC, ASC, DSC of houses_df2 add to merged_df;

    # Indexes of the rows want to add
    insert_indices = [13, 14, 15, 16]

    # Select the relevant rows and copy the required columns
    selected_rows = houses_df2.iloc[12:]

    # Add the data to the main DataFrame in the corresponding rows
    merged_df.loc[insert_indices, 'name2'] = selected_rows['name2'].values
    merged_df.loc[insert_indices, 'sign_planet2'] = selected_rows['sign'].values
    merged_df.loc[insert_indices, 'house2'] = selected_rows['house'].values
    merged_df.loc[insert_indices, 'degree2'] = selected_rows['degree'].values

    # In merged_df, we wrote "0" instead of NaN in sign_id1, sign_id2, house2 variables, we made it integer.

    merged_df["sign_id1"] = merged_df["sign_id1"].fillna(0).astype(int)
    merged_df["sign_id2"] = merged_df["sign_id2"].fillna(0).astype(int)
    merged_df["house2"] = merged_df["house2"].fillna(0).astype(int)

    # We filled the NaN values in sign_house1 & sign_house2 with the values in sign_planet1 & sign_planet2 in the same row.

    # Select specific indexes you want to copy
    seçilen_indeksler = [13, 14, 15, 16]
    # Copy values from column 'column1' to specific indexes
    merged_df.loc[seçilen_indeksler, 'sign_house1'] = merged_df.loc[seçilen_indeksler, 'sign_planet1']
    merged_df.loc[seçilen_indeksler, 'sign_house2'] = merged_df.loc[seçilen_indeksler, 'sign_planet2']

    # We filled the "0" in sign_id1 & sign_id2 with the values in sign_planet1 & sign_planet2.

    # Create a dictionary for sign id
    sign_mapping = {
        'Aries': 1,
        'Taurus': 2,
        'Gemini': 3,
        'Cancer': 4,
        'Leo': 5,
        'Virgo': 6,
        'Libra': 7,
        'Scorpio': 8,
        'Sagittarius': 9,
        'Capricorn': 10,
        'Aquarius': 11,
        'Pisces': 12
    }

    # Detect the sign_id1 corresponding to sign_planet1
    merged_df['sign_id1'] = merged_df['sign_planet1'].map(sign_mapping)
    merged_df['sign_id2'] = merged_df['sign_planet2'].map(sign_mapping)

    # Write the number corresponding to sign_planet1 where there is 0 in sign_id1
    merged_df.loc[merged_df['sign_id1'] == 0, 'sign_id1'] = merged_df.loc[merged_df['sign_id1'] == 0, 'sign_planet1'].map(sign_mapping)
    merged_df.loc[merged_df['sign_id2'] == 0, 'sign_id2'] = merged_df.loc[merged_df['sign_id2'] == 0, 'sign_planet2'].map(sign_mapping)

    ##################################################
    ######### DEGREE CALCULATION FUNCTION ############
    #  Calculating norm_degree for MC, IC, ASC, DSC  #
    ##################################################

    def calculate_degree(degree, sign_planet):
        # Define zodiac sign starting degrees
        zodiac_degrees = {
            "Aries": 0,
            "Taurus": 30,
            "Gemini": 60,
            "Cancer": 90,
            "Leo": 120,
            "Virgo": 150,
            "Libra": 180,
            "Scorpio": 210,
            "Sagittarius": 240,
            "Capricorn": 270,
            "Aquarius": 300,
            "Pisces": 330
        }

        # Get the starting degree of MC
        mc_start_degree = zodiac_degrees[sign_planet]

        # Calculate the degree of MC
        mc_degree = (degree - mc_start_degree) % 30

        return mc_degree


    ################################################
    # MC RATING CALCULATION for 1st Person - 13th INDEX
    # Add MC degree to norm_degree1 in df.
    ################################################

    mc_degree_list1 = []
    for index, row in merged_df.iterrows():
        if pd.isna(row['norm_degree1']) and index == 13:
            mc_degree_list1.append(calculate_degree(row['degree1'], row['sign_planet1']))
        else:
            mc_degree_list1.append(row['norm_degree1'])

    # Get a value by calculating the degree of MC
    mc_degree_value1 = calculate_degree(merged_df.at[13, 'degree1'], merged_df.at[13, 'sign_planet1'])

    # Assign the resulting MC value to the corresponding cell
    merged_df.at[13, 'norm_degree1'] = mc_degree_value1

    ################################################
    # MC RATING CALCULATION for 2nd Person - 13th INDEX
    # Add MC degree to norm_degree1 in df.
    ################################################

    mc_degree_list2 = []
    for index, row in merged_df.iterrows():
        if pd.isna(row['norm_degree2']) and index == 13:
            mc_degree_list2.append(calculate_degree(row['degree2'], row['sign_planet2']))
        else:
            mc_degree_list2.append(row['norm_degree2'])

    # Get a value by calculating the degree of MC
    mc_degree_value2 = calculate_degree(merged_df.at[13, 'degree2'], merged_df.at[13, 'sign_planet2'])

    # Assign the resulting MC value to the corresponding cell
    merged_df.at[13, 'norm_degree2'] = mc_degree_value2

    ################################################
    # IC RATING CALCULATION for 1st Person - 14th INDEX
    # Add the IC degree to norm_degree1 in df.
    ################################################
    IC_degree_list1 = []
    for index, row in merged_df.iterrows():
        if pd.isna(row['norm_degree1']) and index == 14:
            IC_degree_list1.append(calculate_degree(row['degree1'], row['sign_planet1']))
        else:
            IC_degree_list1.append(row['norm_degree1'])

    # Get a value by calculating the degree of IC
    IC_degree_value1 = calculate_degree(merged_df.at[14, 'degree1'], merged_df.at[14, 'sign_planet1'])

    # Assign the resulting IC value to the corresponding cell
    merged_df.at[14, 'norm_degree1'] = IC_degree_value1

    ################################################
    # IC RATING CALCULATION for 2nd Person - 14th INDEX
    # Add the IC degree to norm_degree1 in df.
    ################################################
    IC_degree_list2 = []
    for index, row in merged_df.iterrows():
        if pd.isna(row['norm_degree2']) and index == 14:
            IC_degree_list2.append(calculate_degree(row['degree2'], row['sign_planet2']))
        else:
            IC_degree_list2.append(row['norm_degree2'])

    # Get a value by calculating the degree of IC
    IC_degree_value1 = calculate_degree(merged_df.at[14, 'degree2'], merged_df.at[14, 'sign_planet2'])

    # Assign the resulting IC value to the corresponding cell
    merged_df.at[14, 'norm_degree2'] = IC_degree_value1

    ################################################
    # ASC RATING CALCULATION for 1st Person - 15th INDEX
    # Add the ASC degree to norm_degree1 in df.
    ################################################
    ASC_degree_list1 = []
    for index, row in merged_df.iterrows():
        if pd.isna(row['norm_degree1']) and index == 15:
            ASC_degree_list1.append(calculate_degree(row['degree1'], row['sign_planet1']))
        else:
            ASC_degree_list1.append(row['norm_degree1'])

    # Get a value by calculating the degree of ASCC
    ASC_degree_value1 = calculate_degree(merged_df.at[15, 'degree1'], merged_df.at[15, 'sign_planet1'])

    # Assign the resulting ASC value to the corresponding cell
    merged_df.at[15, 'norm_degree1'] = ASC_degree_value1

    ################################################
    # ASC RATING CALCULATION for 2nd Person - 15th INDEX
    # Add the ASC degree to norm_degree1 in df.
    ################################################
    ASC_degree_list2 = []
    for index, row in merged_df.iterrows():
        if pd.isna(row['norm_degree2']) and index == 15:
            ASC_degree_list2.append(calculate_degree(row['degree2'], row['sign_planet2']))
        else:
            ASC_degree_list2.append(row['norm_degree2'])

    # Get a value by calculating the degree of ASC
    ASC_degree_value2 = calculate_degree(merged_df.at[15, 'degree2'], merged_df.at[15, 'sign_planet2'])

    # Assign the resulting ASC value to the corresponding cell
    merged_df.at[15, 'norm_degree2'] = ASC_degree_value2

    ################################################
    # Calculating DSC RATING for 1st Person - 16th INDEX
    # Add DSC degree to norm_degree1 in df.
    ################################################
    DSC_degree_list1 = []
    for index, row in merged_df.iterrows():
        if pd.isna(row['norm_degree1']) and index == 16:
            DSC_degree_list1.append(calculate_degree(row['degree1'], row['sign_planet1']))
        else:
            DSC_degree_list1.append(row['norm_degree1'])

    # Get a value by calculating the degree of DSC
    DSC_degree_value1 = calculate_degree(merged_df.at[16, 'degree1'], merged_df.at[16, 'sign_planet1'])

    # Assign the resulting DSC value to the corresponding cell
    merged_df.at[16, 'norm_degree1'] = DSC_degree_value1

    ################################################
    # Calculating DSC RATING for 2nd Person - 16th INDEX
    # Add DSC degree to norm_degree1 in df.
    ################################################
    DSC_degree_list2 = []
    for index, row in merged_df.iterrows():
        if pd.isna(row['norm_degree2']) and index == 16:
            DSC_degree_list2.append(calculate_degree(row['degree2'], row['sign_planet2']))
        else:
            DSC_degree_list2.append(row['norm_degree2'])

    # Get a value by calculating the degree of DSC
    DSC_degree_value2 = calculate_degree(merged_df.at[16, 'degree2'], merged_df.at[16, 'sign_planet2'])

    # Assign the resulting DSC value to the corresponding cell
    merged_df.at[16, 'norm_degree2'] = DSC_degree_value2

    ########
    # Juno 
    ########

    df_birthinfo1 = pd.DataFrame([json1])
    df_birthinfo2 = pd.DataFrame([json2])

    df_extracted_1 = df_birthinfo1[["DAY", "MONTH", "YEAR"]]
    df_extracted_2 = df_birthinfo2[["DAY", "MONTH", "YEAR"]]

    excel_df=pd.read_excel("sinastri.xlsx", sheet_name="Juno")

    df_extracted_1['BIRTHDAY1'] = df_extracted_1.apply(lambda row: f"{row['YEAR']} {row['MONTH']} {row['DAY']}", axis=1)
    df_extracted_1['BIRTHDAY1']= pd.to_datetime(df_extracted_1['BIRTHDAY1'])
    df_extracted_2['BIRTHDAY2'] = df_extracted_2.apply(lambda row: f"{row['YEAR']} {row['MONTH']} {row['DAY']}", axis=1)
    df_extracted_2['BIRTHDAY2']= pd.to_datetime(df_extracted_2['BIRTHDAY2'])

    df_extracted_1 = df_extracted_1['BIRTHDAY1']
    df_extracted_2 = df_extracted_2['BIRTHDAY2']

    df_extracted_1 = pd.DataFrame(df_extracted_1)
    df_extracted_2 = pd.DataFrame(df_extracted_2)

    birth_date = df_extracted_1['BIRTHDAY1'].iloc[0]
    birth_date2 = df_extracted_2['BIRTHDAY2'].iloc[0]

    # 1. Find the juno sign corresponding to the person's Date of Birth
    sign_juno1 = excel_df[(excel_df["start_date"] <= birth_date) & (excel_df["end_date"] >= birth_date)]["Sign"].values[0]
    df_extracted_1["sign_planet1"] = sign_juno1

    # 2. Find the juno zodiac sign corresponding to the person's Date of Birth
    sign_juno2 = excel_df[(excel_df["start_date"] <= birth_date2) & (excel_df["end_date"] >= birth_date2)]["Sign"].values[0]
    df_extracted_2["sign_planet2"] = sign_juno2

    df_extracted_1["name1"] = "Juno"
    df_extracted_2["name2"] = "Juno"

    df_extracted_1.drop(columns="BIRTHDAY1", inplace=True)
    df_extracted_2.drop(columns="BIRTHDAY2", inplace=True)

    df_junos = pd.concat([df_extracted_1, df_extracted_2], axis=1)

    ##########################
    # Add Juno to the merge_df
    ##########################

    merged_df = merged_df.append(df_junos, ignore_index = True)

    # We fill Juno degrees with a fixed 15 degrees

    merged_df["norm_degree1"] = merged_df["norm_degree1"].fillna(15).astype(int)
    merged_df["norm_degree2"] = merged_df["norm_degree2"].fillna(15).astype(int)

    # sign id number

    # Detect the sign_id1 corresponding to sign_planet1
    merged_df['sign_id1'] = merged_df['sign_planet1'].map(sign_mapping)
    merged_df['sign_id2'] = merged_df['sign_planet2'].map(sign_mapping)

    # Write the number corresponding to sign_planet1 where there is 0 in sign_id1
    merged_df.loc[merged_df['sign_id1'] == "NaN", 'sign_id1'] = merged_df.loc[merged_df['sign_id1'] == "NaN", 'sign_planet1'].map(sign_mapping)
    merged_df.loc[merged_df['sign_id2'] == "NaN", 'sign_id2'] = merged_df.loc[merged_df['sign_id2'] == "NaN", 'sign_planet2'].map(sign_mapping)

    # conversion of houses from float
    merged_df["house1"] = merged_df["house1"].fillna(0).astype(int)
    merged_df["house2"] = merged_df["house2"].fillna(0).astype(int)

    merged_df["degree1"] = merged_df["degree1"].fillna(0).astype(float)
    merged_df["degree2"] = merged_df["degree2"].fillna(0).astype(float)


    def calculate_junodegree(signplanet1):
        # Define zodiac sign starting degrees
        zodiac_degrees = {
            "Aries": 0,
            "Taurus": 30,
            "Gemini": 60,
            "Cancer": 90,
            "Leo": 120,
            "Virgo": 150,
            "Libra": 180,
            "Scorpio": 210,
            "Sagittarius": 240,
            "Capricorn": 270,
            "Aquarius": 300,
            "Pisces": 330
        }

        return zodiac_degrees.get(signplanet1,None)


    # For Person 1 - get a value by calculating the Juno rating
    juno_degree_value1 = calculate_junodegree(merged_df.at[17, 'sign_planet1'])

    # Assign the resulting Juno value to the corresponding cell
    merged_df.at[17, 'degree1'] = juno_degree_value1

    # 2. For the person - get a value by calculating the Juno rating
    juno_degree_value2 = calculate_junodegree(merged_df.at[17, 'sign_planet2'])

    # Assign the resulting Juno value to the corresponding cell
    merged_df.at[17, 'degree2'] = juno_degree_value2

    # 17. We filled the empty sign_house1 values in the indext with sign_planet1
    merged_df["sign_house1"] = merged_df["sign_house1"].fillna(merged_df.at[17, "sign_planet1"])

    # 17. We filled the empty sign_house2 values in the indext with sign_planet2
    merged_df["sign_house2"] = merged_df["sign_house2"].fillna(merged_df.at[17, "sign_planet2"])


    ####################################
    # 4 - The angles will be calculated 
    ####################################

    df = merged_df.copy()

    # We create a list to store the orb values
    orb_values = []

    ## We calculate orb values by traversing the data
    for index1, row1 in df.iterrows():
        for index2, row2 in df.iterrows():
            orb_value = abs(row1['norm_degree1'] - row2['norm_degree2']) if row1['sign_planet1'] == row2['sign_planet2']\
                  and row1['name1'] != row2['name2'] else abs(row1['degree1'] - row2['degree2'])
            orb_values.append({
                'name1': row1['name1'],
                'name2': row2['name2'],
                'aspect': orb_value
            })


    # Convert the result to a DataFrame
    aspectsorb_df = pd.DataFrame(orb_values)

    # Select the columns
    aspect_df = aspectsorb_df[['name1', 'aspect', 'name2']]

    ####################################################
    ###########  TwinFlame Function  ###################
    ####################################################
    
    ruh_ikizi_durum = ruh_ikizi_durumu(aspect_df)

    ####################################################
    ########### Soul Mate Function #####################
    ####################################################


    ruh_esi_durum = ruh_esi(aspect_df)

    ########################
    # Our aspect_df is Ok.
    ########################

    ################################
    # Let's Process Synastry Excel
    ################################

    sinastri = pd.read_excel("sinastri.xlsx")

    sinastri["Orb"].fillna(sinastri["Orb"].mode()[0], inplace=True)

    sinastri.drop(columns="Description", inplace=True)


    #########################################################################################
    ################################  TIME TO BUILD A MODEL   ###############################
    #########################################################################################

    # Feature Engineering: Encoding
    label_encoder = LabelEncoder()

    sinastri['Result'] = label_encoder.fit_transform(sinastri['Result'])

    sinastri['Orb'] = sinastri['Orb'].str.replace('-', '').astype(float)

    sinastri['Orb'].fillna(sinastri['Orb'].mode()[0], inplace=True)
    sinastri['Planet1'].fillna(sinastri['Planet1'].mode()[0], inplace=True)
    sinastri['Planet2'].fillna(sinastri['Planet2'].mode()[0], inplace=True)

    # Convert 'Planet1', 'Planet2' and 'Aspect' columns
    sinastri['Planet1'] = label_encoder.fit_transform(sinastri['Planet1'])
    sinastri['Planet2'] = label_encoder.fit_transform(sinastri['Planet2'])


    # Separation of features and target variable
    X = sinastri[['Planet1', 'Planet2', 'Aspect']]
    y = sinastri['Result']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define and train the RandomForestClassifier model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    ######################
    #  Apply to aspect_df
    ######################

    # Convert columns 'name1' and 'name2'
    aspect_df['name1'] = label_encoder.fit_transform(aspect_df['name1'])
    aspect_df['name2'] = label_encoder.fit_transform(aspect_df['name2'])

    # Make predictions using the model
    predictions = model.predict(aspect_df[['name1', 'name2', 'aspect']].values)

    # Add the forecast results as a new column named 'Result'
    aspect_df['Result'] = predictions

    aspect_df

    #############################
    #######   SCORING  ##########
    #############################

    # 'Calculate the proportion of 1s in the 'Result' column
    one_count = aspect_df['Result'].sum()  # Number of 1s in the 'Result' column
    total_count = len(aspect_df)  # Total number of data

    # Calculate the ratio of 1s as a percentage
    percentage = (one_count / total_count) * 100

    # Check if either 'ruh_esi_durum' or 'ruh_ikizi_durum' is True and update 'percentage' accordingly
    if (ruh_esi_durum == "Ruh Eşisiniz") and (ruh_ikizi_durum == "Ruh Eşisiniz"):
        percentage += 5  # Add 5 points if either condition is met
    
    elif (ruh_esi_durum == "Ruh Eşisiniz") or (ruh_ikizi_durum == "Ruh Eşisiniz"):
        percentage += 10  # Add an additional 5 points if both conditions are met

    elif (ruh_esi_durum != "Ruh Eşisiniz") and (ruh_ikizi_durum != "Ruh Eşisiniz"):
        percentage -= 10  # Deduct 10 points if neither condition is met  
          
    else: 
        percentage

    # Print the result
    print("İlişki Uyumu:", percentage, "%")

    percentage = round(percentage, 2)

    return percentage, ruh_esi_durum, ruh_ikizi_durum

#perfectmatch(example_json,example_json2)