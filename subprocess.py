import streamlit as st
import subprocess

st.title("Streamlit Terminal Commands")

# Display a text input for the user to enter terminal commands
terminal_command = st.text_input("Enter terminal command:")

# Execute the terminal command when a button is clicked
if st.button("Execute Command"):
    try:
        # Use subprocess to run the terminal command
        result = subprocess.run(terminal_command, capture_output=True, text=True, shell=True)

        # Display the output of the terminal command
        st.text("Terminal Output:")
        st.code(result.stdout)
    except Exception as e:
        st.error(f"Error executing the command: {e}")
