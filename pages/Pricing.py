import streamlit as st

st.header("Pricing")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div style="border: 2px solid green; width: 300px;height:200px; text-align: center;">
            <h2>Monthly Plan</h2>
            <p>This is the monthly plan information.<br>100 Queries</p>
        </div>
        """, unsafe_allow_html=True
    )

    st.button("Select Monthly Plan")
st.divider()
with col2:
    st.markdown(
        """
        <div style="border: 2px solid green; width: 300px; height:200px;text-align: center;">
            <h2>Yearly Plan</h2>
            <p>This is the yearly plan information.<br>1500 Queries</p>
        </div>
        """, unsafe_allow_html=True
    )

    st.button("Select Yearly Plan")
