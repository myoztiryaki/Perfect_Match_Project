import streamlit as st
import requests
from PIL import Image

# Load the banner image
banner_image = Image.open("perfectmatch.png")

# Display the banner image at the top of the page
st.image(banner_image, width=800)  # Adjust the width as needed

# Şehir isimlerini koordinat verilerine dönüştüren bir fonksiyon
def get_coordinates(city_name, city_data):
    city_info = city_data.get(city_name)
    if city_info:
        return city_info.get("Enlem"), city_info.get("Boylam")
    else:
        return None, None

sehir_bilgileri = {
    "Adana": {"Enlem": 37.0000, "Boylam": 35.3213},
    "Adıyaman": {"Enlem": 37.7648, "Boylam": 38.2766},
    "Afyonkarahisar": {"Enlem": 38.7507, "Boylam": 30.5567},
    "Ağrı": {"Enlem": 39.7191, "Boylam": 43.0503},
    "Amasya": {"Enlem": 40.6530, "Boylam": 35.8337},
    "Ankara": {"Enlem": 39.9334, "Boylam": 32.8597},
    "Antalya": {"Enlem": 36.8969, "Boylam": 30.7133},
    "Artvin": {"Enlem": 41.1830, "Boylam": 41.8183},
    "Aydın": {"Enlem": 37.8402, "Boylam": 27.8416},
    "Balıkesir": {"Enlem": 39.6484, "Boylam": 27.8826},
    "Bilecik": {"Enlem": 40.1430, "Boylam": 29.9838},
    "Bingöl": {"Enlem": 38.8848, "Boylam": 40.4982},
    "Bitlis": {"Enlem": 38.3938, "Boylam": 42.1228},
    "Bolu": {"Enlem": 40.5760, "Boylam": 31.5788},
    "Burdur": {"Enlem": 37.7267, "Boylam": 30.2889},
    "Bursa": {"Enlem": 40.1824, "Boylam": 29.0670},
    "Çanakkale": {"Enlem": 40.1553, "Boylam": 26.4142},
    "Çankırı": {"Enlem": 40.6013, "Boylam": 33.6150},
    "Çorum": {"Enlem": 40.5463, "Boylam": 34.9509},
    "Denizli": {"Enlem": 37.7765, "Boylam": 29.0864},
    "Diyarbakır": {"Enlem": 37.9204, "Boylam": 40.2137},
    "Edirne": {"Enlem": 41.6719, "Boylam": 26.5587},
    "Elazığ": {"Enlem": 38.6752, "Boylam": 39.2208},
    "Erzincan": {"Enlem": 39.7500, "Boylam": 39.5000},
    "Erzurum": {"Enlem": 39.9000, "Boylam": 41.2700},
    "Eskişehir": {"Enlem": 39.7667, "Boylam": 30.5250},
    "Gaziantep": {"Enlem": 37.0662, "Boylam": 37.3833},
    "Giresun": {"Enlem": 40.9128, "Boylam": 38.3895},
    "Gümüşhane": {"Enlem": 40.4606, "Boylam": 39.4819},
    "Hakkari": {"Enlem": 37.5736, "Boylam": 43.7408},
    "Hatay": {"Enlem": 36.1529, "Boylam": 36.1469},
    "Isparta": {"Enlem": 37.7667, "Boylam": 30.5667},
    "Mersin": {"Enlem": 36.8000, "Boylam": 34.6333},
    "İstanbul": {"Enlem": 41.0082, "Boylam": 28.9784},
    "İzmir": {"Enlem": 38.4237, "Boylam": 27.1428},
    "Kars": {"Enlem": 40.5927, "Boylam": 43.0777},
    "Kastamonu": {"Enlem": 41.3753, "Boylam": 33.7759},
    "Kayseri": {"Enlem": 38.7312, "Boylam": 35.4787},
    "Kırklareli": {"Enlem": 41.7331, "Boylam": 27.2149},
    "Kırşehir": {"Enlem": 39.1425, "Boylam": 34.1709},
    "Kocaeli": {"Enlem": 40.7650, "Boylam": 29.9403},
    "Konya": {"Enlem": 37.8667, "Boylam": 32.4833},
    "Kütahya": {"Enlem": 39.4167, "Boylam": 29.9833},
    "Malatya": {"Enlem": 38.3552, "Boylam": 38.3095},
    "Manisa": {"Enlem": 38.6191, "Boylam": 27.4289},
    "Kahramanmaraş": {"Enlem": 37.5736, "Boylam": 36.9372},
    "Mardin": {"Enlem": 37.3212, "Boylam": 40.7248},
    "Muğla": {"Enlem": 37.2136, "Boylam": 28.3631},
    "Muş": {"Enlem": 38.7452, "Boylam": 41.5064},
    "Nevşehir": {"Enlem": 38.6242, "Boylam": 34.7236},
    "Niğde": {"Enlem": 37.9667, "Boylam": 34.6833},
    "Ordu": {"Enlem": 40.9833, "Boylam": 37.8833},
    "Rize": {"Enlem": 41.0201, "Boylam": 40.5234},
    "Sakarya": {"Enlem": 40.7592, "Boylam": 30.3967},
    "Samsun": {"Enlem": 41.2867, "Boylam": 36.3300},
    "Siirt": {"Enlem": 37.9322, "Boylam": 41.9569},
    "Sinop": {"Enlem": 42.0231, "Boylam": 35.1531},
    "Sivas": {"Enlem": 39.7477, "Boylam": 37.0179},
    "Tekirdağ": {"Enlem": 40.9833, "Boylam": 27.5167},
    "Tokat": {"Enlem": 40.3080, "Boylam": 36.5538},
    "Trabzon": {"Enlem": 41.0050, "Boylam": 39.7269},
    "Tunceli": {"Enlem": 39.1102, "Boylam": 39.5486},
    "Şanlıurfa": {"Enlem": 37.1671, "Boylam": 38.7939},
    "Uşak": {"Enlem": 38.6823, "Boylam": 29.4082},
    "Van": {"Enlem": 38.5017, "Boylam": 43.3750},
    "Yozgat": {"Enlem": 39.8208, "Boylam": 34.8047},
    "Zonguldak": {"Enlem": 41.4564, "Boylam": 31.7987},
    "Aksaray": {"Enlem": 38.3727, "Boylam": 33.4166},
    "Bayburt": {"Enlem": 40.2600, "Boylam": 40.2244},
    "Karaman": {"Enlem": 37.1811, "Boylam": 33.2150},
    "Kırıkkale": {"Enlem": 39.8468, "Boylam": 33.5153},
    "Batman": {"Enlem": 37.8812, "Boylam": 41.1351},
    "Şırnak": {"Enlem": 37.5133, "Boylam": 42.4543},
    "Bartın": {"Enlem": 41.5811, "Boylam": 32.4610},
    "Ardahan": {"Enlem": 41.1105, "Boylam": 42.7022},
    "Iğdır": {"Enlem": 39.9228, "Boylam": 44.0450},
    "Yalova": {"Enlem": 40.6500, "Boylam": 29.2667},
    "Karabük": {"Enlem": 41.2054, "Boylam": 32.6243},
    "Kilis": {"Enlem": 36.7184, "Boylam": 37.1159},
    "Osmaniye": {"Enlem": 37.2500, "Boylam": 36.2667},
    "Düzce": {"Enlem": 40.8500, "Boylam":31.1667},
    "İtalya": {"Enlem": 41.8719, "Boylam": 12.5674},
    "İsveç": {"Enlem": 60.1282, "Boylam": 18.6435},
    "İsviçre": {"Enlem": 46.8182, "Boylam": 8.2275},
    "Fransa": {"Enlem": 46.6034, "Boylam": 1.8883},
    "Almanya": {"Enlem": 51.1657, "Boylam": 10.4515},
    "Belçika": {"Enlem": 50.8503, "Boylam": 4.3517},
    "Hollanda": {"Enlem": 52.1326, "Boylam": 5.2913},
    "Azerbaycan": {"Enlem": 40.1431, "Boylam": 47.5769},
    "Özbekistan": {"Enlem": 41.3775, "Boylam": 64.5853},
    "İran": {"Enlem": 32.4279, "Boylam": 53.6880},
    "Suriye": {"Enlem": 34.8021, "Boylam": 38.9968},
    "Afganistan": {"Enlem": 33.9391, "Boylam": 67.7100},
    "Fas": {"Enlem": 31.7917, "Boylam": -7.0926},
    "İspanya": {"Enlem": 40.4637, "Boylam": -3.7492},
    "Portekiz": {"Enlem": 39.3999, "Boylam": -8.2245},
    "Avusturya": {"Enlem": 47.5162, "Boylam": 14.5501},
    "Yunanistan": {"Enlem": 39.0742, "Boylam": 21.8243},
    "Bulgaristan": {"Enlem": 42.7339, "Boylam": 25.4858},
    "Makedonya": {"Enlem": 41.6086, "Boylam": 21.7453},
    "Sırbistan": {"Enlem": 44.0165, "Boylam": 21.0059},
    "Çek": {"Enlem": 49.8175, "Boylam": 15.4729},
    "Macaristan": {"Enlem": 47.1625, "Boylam": 19.5033},
    "Letonya": {"Enlem": 56.8796, "Boylam": 24.6032},
    "Litvanya": {"Enlem": 55.1694, "Boylam": 23.8813},
    "Slovenya": {"Enlem": 46.1512, "Boylam": 14.9955},
    "Ukrayna": {"Enlem": 48.3794, "Boylam": 31.1656},
    "Rusya": {"Enlem": 61.5240, "Boylam": 105.3188},
    "Danimarka": {"Enlem": 56.2639, "Boylam": 9.5018}
}

# Streamlit UI
st.title("Jr.Eros is at your service")

# Create two columns for user input sections
col1, col2 = st.columns(2)

# User Input (First Set)
with col1:
    st.header("First Person")
    day1 = st.text_input("Day")
    month1 = st.text_input("Month")
    year1 = st.text_input("Year")
    hour1 = st.text_input("Hour")
    minute1 = st.text_input("Minute")
    city1 = st.selectbox("Location", list(sehir_bilgileri.keys()))
    timezone1 = st.text_input("Timezone")


# User Input (Second Set)
with col2:
    st.header("Second person")
    day2 = st.text_input("Day ")
    month2 = st.text_input("Month ")
    year2 = st.text_input("Year ")
    hour2 = st.text_input("Hour ")
    minute2 = st.text_input("Minute ")
    city2 = st.selectbox("Location 2", list(sehir_bilgileri.keys()))
    timezone2 = st.text_input("Timezone ")


# Kullanıcının girdiği şehir isimlerini koordinat verilerine dönüştürün
latitude1, longitude1 = get_coordinates(city1, sehir_bilgileri)
latitude2, longitude2 = get_coordinates(city2, sehir_bilgileri)


# Make POST requests to the FastAPI model when the single "Get Predictions" button is clicked
if st.button("Get Predictions :heart: "):
    api_url = "http://localhost:8001/astroinfo"  # Change to the actual FastAPI endpoint URL
    
    user_input = {
        "day": day1,
        "month": month1,
        "year": year1,
        "hour": hour1,
        "min": minute1,
        "lat": latitude1,
        "lon": longitude1,
        "tzone": timezone1,
        "day2": day2,
        "month2": month2,
        "year2": year2,
        "hour2": hour2,
        "min2": minute2,
        "lat2": latitude2,
        "lon2": longitude2,
        "tzone2": timezone2,
    }
    
    response = requests.post(api_url, json=user_input)


    if response.status_code == 200:
        prediction = response.json()
        st.success(f" Prediction: {prediction['percentage']} \n Ruh ikizi durumunuz: {prediction['ruh_ikizi_durum']} \n Ruh eşi durum: {prediction['ruh_esi_durum']}")
    elif response.status_code == 422:
        st.error("Please be sure all fields has been filled.")
    else:
        st.error("Error occurred while making the predictions.")