import streamlit as st

# إعدادات الصفحة لتكون باللغة العربية ومن اليمين لليسار
st.set_page_config(page_title="نظام خبير لتشخيص الأمراض", page_icon="🩺", layout="centered")

st.markdown("""
    <style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

class DiseaseExpertSystem:
    def __init__(self):
        # قاعدة المعرفة: كل مرض له قائمة بالأعراض المرتبطة به ونصيحة مبدئية
        self.knowledge_base = {
            "نزلة برد (Common Cold)": {
                "symptoms": {"سيلان الأنف", "عطاس", "احتقان الحلق", "سعال خفيف"},
                "advice": "الراحة، شرب السوائل الدافئة، ومتابعة الأعراض."
            },
            "الإنفلونزا (Influenza)": {
                "symptoms": {"ارتفاع الحرارة", "آلام الجسم", "إرهاق شديد", "سعال جاف", "صداع"},
                "advice": "الراحة التامة في المنزل، الإكثار من السوائل، واستشارة طبيب عند استمرار الحرارة."
            },
            "حساسية موسمية (Allergy)": {
                "symptoms": {"عطاس", "حكة في العين", "سيلان الأنف", "احتقان الأنف"},
                "advice": "تجنب مسببات الحساسية قدر الإمكان واستشارة طبيب أو صيدلي."
            },
            "التهاب المعدة (Gastritis)": {
                "symptoms": {"ألم أعلى البطن", "غثيان", "حموضة", "انتفاخ"},
                "advice": "تجنب الأطعمة الحارة أو الدسمة وتناول وجبات خفيفة ومراجعة الطبيب."
            },
            "الصداع النصفي (Migraine)": {
                "symptoms": {"صداع", "حساسية للضوء", "غثيان", "ألم في جهة واحدة من الرأس"},
                "advice": "الجلوس في غرفة هادئة ومظلمة والراحة واستشارة مختص."
            }
        }

        # تجميع كل الأعراض المتاحة في قائمة مرتبة
        all_symptoms = set()
        for info in self.knowledge_base.values():
            all_symptoms.update(info["symptoms"])
        self.available_symptoms = sorted(list(all_symptoms))

    def diagnose(self, user_symptoms):
        results = []
        for disease, info in self.knowledge_base.items():
            disease_symptoms = info["symptoms"]
            matched = user_symptoms.intersection(disease_symptoms)

            if matched:
                score = len(matched) / len(disease_symptoms)
                results.append({
                    "disease": disease,
                    "score": score,
                    "matched": matched,
                    "total": len(disease_symptoms),
                    "advice": info["advice"]
                })

        # ترتيب النتائج من الأعلى تطابقاً إلى الأقل
        results.sort(key=lambda x: x["score"], reverse=True)
        return results


# --- بناء واجهة الموقع باستخدام Streamlit ---
expert = DiseaseExpertSystem()

st.title("🩺 نظام خبير مبدئي لتشخيص الأمراض")
st.warning("⚠️ تنبيه: هذا النظام تعليمي واسترشادي فقط ولا يغني عن استشارة الطبيب المختص.")

st.subheader("1. اختر الأعراض التي تشعر بها:")
selected_list = st.multiselect(
    "ابحث واختر عرضاً واحداً أو أكثر:",
    options=expert.available_symptoms,
    placeholder="اضغط هنا لاختيار الأعراض..."
)

# زر بدء التشخيص
if st.button("🔍 تحليل الأعراض والتشخيص", type="primary"):
    if not selected_list:
        st.error("من فضلك اختر عرضاً واحداً على الأقل أولاً.")
    else:
        user_symptoms = set(selected_list)
        results = expert.diagnose(user_symptoms)

        st.divider()
        st.subheader("📋 نتائج التقييم المبدئي:")

        if not results:
            st.info("لا توجد مطابقة واضحة مع قاعدة المعرفة الحالية.")
        else:
            for item in results:
                percentage = round(item["score"] * 100, 1)
                with st.container(border=True):
                    st.markdown(f"### {item['disease']} — نسبة التطابق: `{percentage}%`")
                    st.progress(item["score"])
                    st.write(f"**الأعراض المتطابقة ({len(item['matched'])}/{item['total']}):** {', '.join(item['matched'])}")
                    st.success(f"💡 **إرشاد مبدئي:** {item['advice']}")

# قسم جانبي لعرض قاعدة المعرفة (IF-THEN)
with st.sidebar:
    st.header("🧠 قاعدة المعرفة (Rules)")
    st.write("يعمل النظام وفق القواعد التالية:")
    for disease, info in expert.knowledge_base.items():
        with st.expander(disease):
            st.write("**IF الأعراض تشمل:**")
            st.write("، ".join(info["symptoms"]))