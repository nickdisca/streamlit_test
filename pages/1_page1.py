import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

st.title('This is a subpage (page 1)')

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

# from streamlit_gtag import st_gtag
# st_gtag(
#     key="gtag_send_event_b",
#     id="G-PBXS9SB8FP",
#     event_name="app_page1",
#     params={
#         "event_category": "test_category_b",
#         "event_label": "test_label_b",
#         "value": 97,
#     },
# )

if st.button("Click me to know in which subpage you are"):
    st.write("You are on subpage 1")
