import os
import streamlit as st

def render_theme_toggle():
    config_path = os.path.join(".streamlit", "config.toml")
    
    # Define current theme based on config file contents
    current_theme = "light"
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            if 'base = "dark"' in f.read():
                current_theme = "dark"
                
    # UI Icon rendering
    theme_icon = "☀️ Mode Clair" if current_theme == "dark" else "🌙 Mode Sombre"
    
    if st.sidebar.button(theme_icon, use_container_width=True):
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            if current_theme == "dark":
                new_content = content.replace('base = "dark"', 'base = "light"')
            else:
                new_content = content.replace('base = "light"', 'base = "dark"')
                
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(new_content)
                
            # Rerun forces Streamlit to reload the config and apply the new theme instantly
            st.rerun()
