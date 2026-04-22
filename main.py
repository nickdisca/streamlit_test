import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')
st.subheader(f"This is copied from streamlit by {st.secrets['my_username']} :sunglasses:")

#Adding a streamlit component (st.components.v1 is replaced by st.iframe)
# html_code = """
# <div style="padding:20px; background-color:#f0f2f6; border-radius:10px;">
#     <h2 style="color:#4CAF50;">Hello Streamlit 👋</h2>
#     <p>This is a custom HTML component inside Streamlit.</p>
#     <button onclick="alert('Button clicked!')">Click Me</button>
# </div>
# """
# st.iframe(html_code, height=200)

# GA_code = """
# <!-- Google tag (gtag.js) -->
# <script async src="https://www.googletagmanager.com/gtag/js?id=G-PBXS9SB8FP"></script>
# <script>
#     window.dataLayer = window.dataLayer || [];
#     function gtag(){dataLayer.push(arguments);}
#     gtag('js', new Date());

#   gtag('config', 'G-PBXS9SB8FP');
# </script>
# """
# st.iframe(GA_code, height=200)

# Inject GA as suggested in https://discuss.streamlit.io/t/how-to-add-google-analytics-or-js-code-in-a-streamlit-app/1610/38
# import pathlib
# from bs4 import BeautifulSoup
# import logging
# import shutil

# def inject_ga():
#     GA_ID = "google_analytics"
#     GA_JS = """
#     <!-- Google tag (gtag.js) -->
#     <script async src="https://www.googletagmanager.com/gtag/js?id=G-PBXS9SB8FP"></script>
#     <script>
#         window.dataLayer = window.dataLayer || [];
#         function gtag(){dataLayer.push(arguments);}
#         gtag('js', new Date());

#       gtag('config', 'G-PBXS9SB8FP');
#     </script>
#     """

#     # Insert the script in the head tag of the static template inside your virtual
#     index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
#     logging.info(f'editing {index_path}')
#     soup = BeautifulSoup(index_path.read_text(), features="html.parser")
#     if not soup.find(id=GA_ID):  # if cannot find tag
#         bck_index = index_path.with_suffix('.bck')
#         if bck_index.exists():
#             shutil.copy(bck_index, index_path)  # recover from backup
#         else:
#             shutil.copy(index_path, bck_index)  # keep a backup
#         html = str(soup)
#         new_html = html.replace('<head>', '<head>\n' + GA_JS)
#         index_path.write_text(new_html)

# # Call the actual function
# inject_ga()

# Use streamlit-gtag
# from streamlit_gtag import st_gtag
# st_gtag(
#     gtag_id="G-PBXS9SB8FP",
#     config={"send_page_view": True}
# )

# st_gtag(
#     event="custom_event",
#     parameters={"event_category": "engagement", "event_label": "button_click"}
# )

# st_gtag(
#     key="gtag_send_event_a",
#     id="G-PBXS9SB8FP",
#     event_name="app_main_page",
#     params={
#         "event_category": "test_category_a",
#         "event_label": "test_label_a",
#         "value": 97,
#     },
# )

# Adding a fake button to be clicked to keep the app awake
if st.button("keep me up"):
    st.write("I am awake")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)
