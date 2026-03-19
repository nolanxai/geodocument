import streamlit as st
from openai import OpenAI
import os

st.set_page_config(page_title="GeoDoc", layout="wide")
st.title("GeoDoc – Geography Decision Guide")

st.markdown("""
Analyze any region, city, plot or comparison. Get:  
• Natural features & scorecard  
• Societal uses (food, logistics, trade, infrastructure, heat reduction, wildlife connectivity)  
• Land-use warnings  
• Prosperity strategies  
• Site integration recommendations (when relevant)  

Free. Instant. Science-based.
""")

geography_input = st.text_area(
    "Describe the geography (region, city, coordinates, comparison, or plot):",
    height=150,
    placeholder="Examples:\n- Saudi Arabia\n- Waco, Texas vs Austin, Texas\n- 10 acres near Temple, TX for a farm\n- Norway vs Iraq"
)

user_goals = st.text_area(
    "Optional: Constraints / Goals",
    height=100,
    placeholder="Examples:\n- Protect bird migration paths\n- Attract pollinators\n- Minimize light pollution\n- Add wildlife passages\n- Reduce urban heat"
)

if st.button("Analyze", type="primary"):
    if not geography_input.strip():
        st.error("Enter a location or description.")
    else:
        with st.spinner("Analyzing..."):
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                st.error("Add OPENAI_API_KEY in environment variables on your deploy platform.")
                st.stop()

            client = OpenAI(api_key=api_key)

            system_prompt = """You are GeoDoc — a geography decision guide. Analyze strictly in this order:

1. Geographic Reality Summary – Objective facts: soil, water, climate, topography, solar/wind patterns, natural corridors, elevation, flood/seismic risk, etc.

2. Advantages & Limitations Scorecard – Clear scoring of natural strengths and constraints.

3. Societal Application Ideas – How this geography can support food distribution, logistics, trade, infrastructure, heat reduction, wildlife connectivity, etc.

4. Human Mistake Warnings – Specific risks (urban sprawl on farmland, aquifer depletion, deforestation, etc.).

5. Prosperity & Stability Suggestions – Long-term ways to build wealth/resilience with the geography.

6. Development & Site Integration Recommendations – Only if a build/site/development is mentioned or user goals imply it. Include:
   - Optimal placement/orientation (science-based NSEW where beneficial for solar/thermal balance)
   - Integration with existing structures, neighbors, hills/mountains/lakes/ridges/valleys
   - Noise reduction (wind direction, topography shielding)
   - Wildlife & biodiversity integration (migration paths, pollinators, passages)
   - Heat island mitigation
   - Visual/spatial integration with landscape
   - Tailor directly to user constraints/goals

Be objective, evidence-based, practical. Use markdown."""

            user_message = f"Geography: {geography_input}\n\nUser constraints/goals: {user_goals if user_goals else 'None provided'}"

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.4,
                max_tokens=1500
            )

            report = response.choices[0].message.content.strip()

            st.markdown("### GeoDoc Analysis")
            st.markdown(report)

            st.markdown("### Map Placeholder")
            st.info("Interactive map coming soon.")

            st.download_button(
                label="Download Report as Text",
                data=report,
                file_name="geodoc_report.txt",
                mime="text/plain"
            )
