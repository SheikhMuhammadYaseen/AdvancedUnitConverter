import streamlit as st
from pint import UnitRegistry

ureg = UnitRegistry()

st.set_page_config(page_title="Advanced Unit Converter", layout="centered")

st.title("🔄 Advanced Unit Converter")
st.write("Convert between different units with precision and ease.")

# Supported Conversion Categories and Units
conversion_data = {
    "Length": ["meter", "kilometer", "mile", "yard", "foot", "inch", "centimeter"],
    "Weight": ["kilogram", "gram", "pound", "ounce", "ton"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Volume": ["liter", "milliliter", "cubic_meter", "cubic_foot", "gallon"],
    "Speed": ["kilometer_per_hour", "meter_per_second", "mile_per_hour", "knot"]
}

# Conversion Selection
category = st.selectbox("Select Conversion Category", list(conversion_data.keys()))

unit_from = st.selectbox("From Unit", conversion_data[category])
unit_to = st.selectbox("To Unit", conversion_data[category])

amount = st.number_input(f"Enter {unit_from} value", min_value=0.0, format="%f")

precision = st.slider("Select Decimal Precision", 0, 10, 2)

try:
    if category == "Temperature":
        if unit_from != unit_to:
            if unit_from == "celsius":
                quantity = amount * ureg.degC
            elif unit_from == "fahrenheit":
                quantity = amount * ureg.degF
            elif unit_from == "kelvin":
                quantity = amount * ureg.kelvin
            
            converted = quantity.to(getattr(ureg, unit_to)).magnitude
        else:
            converted = amount
    else:
        quantity = amount * getattr(ureg, unit_from)
        converted = quantity.to(getattr(ureg, unit_to)).magnitude
    
    st.success(f"{amount} {unit_from} = {round(converted, precision)} {unit_to}")

except Exception as e:
    st.error(f"Conversion Error: {e}")

# Conversion History
if "conversion_history" not in st.session_state:
    st.session_state["conversion_history"] = []

if st.button("Add to History"):
    st.session_state["conversion_history"].append(f"{amount} {unit_from} = {round(converted, precision)} {unit_to}")

if st.session_state["conversion_history"]:
    st.subheader("📜 Conversion History")
    for entry in st.session_state["conversion_history"]:
        st.write(entry)

if st.button("Clear History"):
    st.session_state["conversion_history"] = []