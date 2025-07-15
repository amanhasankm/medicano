import streamlit as st

def app():
    st.title("🧬 PCOS Type Classifier")
    st.write("Answer the following 12 questions to help determine your PCOS type. The classification is based on common medical indicators.")

    st.markdown("----")

    st.header("🧠 Questionnaire")

    # ------------------ Insulin-Resistant PCOS ------------------
    st.subheader("🍩 Insulin Resistance Symptoms")
    q1 = st.radio("Do you feel tired or sleepy after eating?", ["Yes", "No"])
    q2 = st.radio("Do you crave sugary or carb-rich foods often?", ["Yes", "No"])
    q3 = st.radio("Have you gained weight easily, especially around your abdomen?", ["Yes", "No"])

    # ------------------ Inflammatory PCOS ------------------
    st.subheader("🔥 Inflammatory Symptoms")
    q4 = st.radio("Do you experience frequent headaches or joint pain?", ["Yes", "No"])
    q5 = st.radio("Do you have skin conditions like acne, eczema, or hives?", ["Yes", "No"])
    q6 = st.radio("Do you suffer from chronic fatigue or brain fog?", ["Yes", "No"])

    # ------------------ Adrenal PCOS ------------------
    st.subheader("😰 Adrenal Symptoms")
    q7 = st.radio("Do you feel extremely anxious or overwhelmed often?", ["Yes", "No"])
    q8 = st.radio("Do you have trouble sleeping or wake up tired?", ["Yes", "No"])
    q9 = st.radio("Do you notice hair thinning or facial hair growth?", ["Yes", "No"])

    # ------------------ Post-Pill PCOS ------------------
    st.subheader("💊 Post-Pill Symptoms")
    q10 = st.radio("Did your cycle become irregular or stop after quitting birth control?", ["Yes", "No"])
    q11 = st.radio("Did your acne or weight gain worsen after stopping the pill?", ["Yes", "No"])
    q12 = st.radio("Were your cycles normal before using birth control?", ["Yes", "No"])

    st.markdown("----")

    if st.button("🔎 Classify PCOS Type"):
        st.subheader("🔬 Classification Result")

        # Count Yes responses per type
        insulin_score = sum([q1=="Yes", q2=="Yes", q3=="Yes"])
        inflam_score = sum([q4=="Yes", q5=="Yes", q6=="Yes"])
        adrenal_score = sum([q7=="Yes", q8=="Yes", q9=="Yes"])
        pill_score = sum([q10=="Yes", q11=="Yes", q12=="Yes"])

        scores = {
            "Insulin-Resistant PCOS": insulin_score,
            "Inflammatory PCOS": inflam_score,
            "Adrenal PCOS": adrenal_score,
            "Post-Pill PCOS": pill_score
        }

        # Find highest score
        likely_type = max(scores, key=scores.get)

        if scores[likely_type] == 0:
            st.warning("❗ Not enough symptoms matched to identify a PCOS type.")
        else:
            st.success(f"✅ Most Likely Type: **{likely_type}**")

            if likely_type == "Insulin-Resistant PCOS":
                st.info("""
**What to do:**
- Follow a low-glycemic diet.
- Do strength-based exercises.
- Inositol supplements may help (consult doctor).
- Avoid skipping meals.
""")
            elif likely_type == "Inflammatory PCOS":
                st.info("""
**What to do:**
- Eliminate inflammatory foods (dairy, gluten, sugar).
- Add omega-3s and turmeric to your diet.
- Address gut health and vitamin D levels.
""")
            elif likely_type == "Adrenal PCOS":
                st.info("""
**What to do:**
- Practice stress-reduction daily (yoga, meditation).
- Avoid high-caffeine and HIIT workouts.
- Support adrenal function with adequate sleep.
""")
            elif likely_type == "Post-Pill PCOS":
                st.info("""
**What to do:**
- Support detox pathways (leafy greens, cruciferous veggies).
- Balance estrogen with liver-supporting foods.
- Avoid endocrine disruptors in cosmetics/plastics.
""")

    st.markdown("---")
    st.caption("🛡️ Your answers are not saved. This tool is for educational guidance only, not medical advice.")
