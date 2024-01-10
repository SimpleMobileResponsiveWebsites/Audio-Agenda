import streamlit as st
import pandas as pd

# Define the list of instruments
instruments = ["Bass Guitar", "Acoustic Guitar", "Electric Guitar", "Drums", "Piano",
               "Vocals", "Hand Drums", "Cajon", "Tambourine", "Shaker", "Maracas",
               "Wood Block", "Sleigh Bells", "Aux Percussion"]

# Define the production status options
status_options = ["needs to be recorded", "needs to be re-recorded", "scratch track recorded", "recording completed",
                  "arrangement completed", "editing completed", "mixing completed", "mastering completed",
                  "track printed", "music video created",
                  "music video published"]

# Define the musical key options
key_options = ["C", "C#", "D", "D#", "Db", "E", "Eb", "F", "F#", "G", "G#", "Gb", "A", "A#", "Ab", "B", "Bb"]

# Initialize session state for storing selections, BPM values, key selections, instrument additional info, and gear information
if 'status_selections' not in st.session_state:
    st.session_state['status_selections'] = {instrument: status_options[0] for instrument in instruments}
if 'bpm_values' not in st.session_state:
    st.session_state['bpm_values'] = {instrument: 120 for instrument in instruments}
if 'key_selections' not in st.session_state:
    st.session_state['key_selections'] = {instrument: key_options[0] for instrument in instruments}
if 'instrument_info' not in st.session_state:
    st.session_state['instrument_info'] = {instrument: '' for instrument in instruments}
if 'gear_info' not in st.session_state:
    st.session_state['gear_info'] = {instrument: '' for instrument in instruments}

# Define the Streamlit application
def app():
    st.title("Audio Agenda")

    # Create a form for submission
    with st.form("status_form"):
        # Loop through each instrument and create a row with five columns
        for instrument in instruments:
            col1, col2, col3, col4, col5 = st.columns([2, 2, 3, 3, 3])

            with col1:
                bpm_value = st.number_input(
                    "BPM",
                    min_value=1,
                    max_value=300,
                    value=st.session_state['bpm_values'].get(instrument, 120),
                    key=instrument + "_bpm"
                )
                st.session_state['bpm_values'][instrument] = bpm_value

            with col2:
                key_value = st.selectbox(
                    "Key",
                    key_options,
                    index=key_options.index(st.session_state['key_selections'].get(instrument, "C")),
                    key=instrument + "_key"
                )
                st.session_state['key_selections'][instrument] = key_value

            with col3:
                instrument_info_value = st.text_input(
                    instrument,
                    value=st.session_state['instrument_info'].get(instrument, ''),
                    key=instrument + "_info"
                )
                st.session_state['instrument_info'][instrument] = instrument_info_value

            with col4:
                status_value = st.selectbox(
                    "Production Status",
                    status_options,
                    index=status_options.index(st.session_state['status_selections'].get(instrument, "needs to be recorded")),
                    key=instrument + "_status"
                )
                st.session_state['status_selections'][instrument] = status_value

            with col5:
                gear_info_value = st.text_input(
                    "Gear Used",
                    value=st.session_state['gear_info'].get(instrument, ''),
                    key=instrument + "_gear"
                )
                st.session_state['gear_info'][instrument] = gear_info_value

        # Submit button at the end of the form
        submitted = st.form_submit_button("Submit")

    # Create and display the table upon submission
    if submitted:
        data = []
        for instrument in instruments:
            data.append([
                st.session_state['bpm_values'][instrument],
                st.session_state['key_selections'][instrument],
                st.session_state['instrument_info'][instrument],
                st.session_state['status_selections'][instrument],
                st.session_state['gear_info'][instrument]
            ])

        # Create a DataFrame for the table
        df = pd.DataFrame(data, columns=["BPM", "Key", "Instrument", "Production Status", "Gear Used"], index=instruments)
        st.table(df)

        # Convert DataFrame to CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='audio_data.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    app()
