import streamlit as st

# -----------------------------------------------------------------------------
# CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Kalkulator Titrasi Kimia Analitik",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Header Banner
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #0f2027, #203a43, #2c5364);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.1rem;
        font-weight: 300;
        color: #e0e0e0;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def validate_inputs(volume, weight=None, second_vol=None):
    """
    Checks for Division by Zero or Invalid Physical Values.
    Returns True if inputs are valid, False otherwise.
    """
    if volume <= 0:
        st.error("❌ Error: Volume Titik Akhir (TA) tidak boleh nol atau negatif.")
        return False
    if weight is not None and weight <= 0:
        st.error("❌ Error: Berat sampel tidak boleh nol atau negatif.")
        return False
    if second_vol is not None and second_vol <= 0:
        st.error("❌ Error: Volume pendukung tidak boleh nol atau negatif.")
        return False
    return True

def display_result(label, value, unit):
    """Displays result in a metric box."""
    st.metric(label=label, value=f"{value:.4f}", delta=unit)

# -----------------------------------------------------------------------------
# APPLICATION LOGIC
# -----------------------------------------------------------------------------

# Header
st.markdown("""
    <div class="main-header">
        <h1>Aplikasi Kalkulator Titrasi</h1>
        <div class="sub-header">Praktikum Kimia Analitik</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("⚙️ Navigasi Menu")
menu_options = [
    "1. Argentometri (Klorida)",
    "2. Kompleksometri (Kesadahan/EDTA)",
    "3. Redoks (Permanganat/Iodometri)",
    "4. Alkalimetri (NaOH)",
    "5. Asidimetri (HCl/Warder)"
]
branch = st.sidebar.selectbox("Pilih Metode Titrasi:", menu_options)

# -----------------------------------------------------------------------------
# BRANCH 1: ARGENTOMETRI
# -----------------------------------------------------------------------------
if branch == "1. Argentometri (Klorida)":
    st.header("⚗️ Argentometri: Penetapan Kadar Klor")
    st.markdown("Metode ini digunakan untuk menentukan kadar ion klorida (Cl⁻) dalam sampel menggunakan larutan AgNO₃ standar.")
    
    with st.form("form_argentometri"):
        col1, col2 = st.columns(2)
        with col1:
            method = st.selectbox("Cara Penetapan", ["Cara Fayan's", "Cara Mohr"])
            vol_ta = st.number_input("Volume Titik Akhir / TA (mL)", min_value=0.0, value=10.0, step=0.1, format="%.2f")
            conc_agno3 = st.number_input("Konsentrasi Larutan AgNO₃ (N)", min_value=0.0, value=0.1, step=0.01, format="%.4f")
        
        with col2:
            weight_sample = st.number_input("Berat Sampel Klorida (mg)", min_value=0.0, value=500.0, step=1.0, format="%.1f")
            st.info("Masukkan berat sampel dalam miligram (mg).")
            
        submitted = st.form_submit_button("Hitung Kadar Klor", type="primary")

    if submitted:
        if validate_inputs(vol_ta, weight_sample):
            weight_in_grams = weight_sample / 1000.0
            kadar_cl = (vol_ta * conc_agno3 * 35.45 / weight_in_grams) * 100
            
            st.success("Perhitungan Selesai")
            res_col1, res_col2 = st.columns(2)
            res_col1.metric("Volume TA", f"{vol_ta} mL")
            res_col2.metric("Kadar Klor", f"{kadar_cl:.4f}", delta="%")

# -----------------------------------------------------------------------------
# BRANCH 2: KOMPLEKSOMETRI
# -----------------------------------------------------------------------------
elif branch == "2. Kompleksometri (Kesadahan/EDTA)":
    st.header("⚗️ Kompleksometri")
    st.markdown("Metode комплексometric untuk penetapan kesadahan air atau standarisasi EDTA.")

    task_option = st.radio("Pilih Tugas:", ["Penetapan Kesadahan Total (CaCO3)", "Standarisasi Larutan EDTA"], horizontal=True)

    if task_option == "Penetapan Kesadahan Total (CaCO3)":
        st.subheader("Tugas A: Kadar Kesadahan")
        with st.form("form_kesadahan"):
            c1, c2 = st.columns(2)
            with c1:
                vol_ta = st.number_input("Volume TA EDTA (mL)", min_value=0.0, value=15.0, step=0.1)
                molar_edta = st.number_input("Molaritas EDTA (M)", min_value=0.0, value=0.01, step=0.001, format="%.5f")
            with c2:
                vol_sampel = st.number_input("Volume Sampel Air (mL)", min_value=0.0, value=50.0, step=1.0)
            
            submitted = st.form_submit_button("Hitung Kesadahan", type="primary")

            if submitted:
                if validate_inputs(vol_ta, second_vol=vol_sampel):
                    mg_L_caCO3 = (vol_ta * molar_edta * 100.08 * 1000) / vol_sampel
                    st.success("Perhitungan Selesai")
                    st.metric("Kadar CaCO3", f"{mg_L_caCO3:.4f}", delta="mg/L")

    else:
        st.subheader("Tugas B: Standarisasi EDTA")
        with st.form("form_edta_std"):
            c1, c2 = st.columns(2)
            with c1:
                vol_ta = st.number_input("Volume TA EDTA (mL)", min_value=0.0, value=12.5, step=0.1)
                weight_caco3 = st.number_input("Berat CaCO3 Induk (mg)", min_value=0.0, value=100.0, step=1.0)
            with c2:
                vol_aliquot = st.number_input("Volume Aliquot (mL)", min_value=0.0, value=10.0, step=1.0)
                total_vol = st.number_input("Volume Total Larutan Induk (mL)", min_value=0.0, value=100.0, step=1.0)
            
            submitted = st.form_submit_button("Hitung Normalitas EDTA", type="primary")

            if submitted:
                if validate_inputs(vol_ta, weight_caco3) and vol_aliquot > 0:
                    # Calculation: Molarity = (Weight/100.08) * (Vol_Aliq/Total_Vol) / TA
                    mol_caco3 = (weight_caco3 / 100.08) # moles in total solution
                    conc_edta = mol_caco3 * (vol_aliquot / total_vol) / vol_ta
                    
                    st.success("Perhitungan Selesai")
                    st.metric("Konsentrasi EDTA", f"{conc_edta:.5f}", delta="M")

# -----------------------------------------------------------------------------
# BRANCH 3: REDOKS
# -----------------------------------------------------------------------------
elif branch == "3. Redoks (Permanganat/Iodometri)":
    st.header("⚗️ Redoks")
    st.markdown("Metode titrasi redoks dengan perubahan bilangan oksidasi.")

    redoks_option = st.radio("Pilih Metode:", ["Permanganometri", "Iodometri"], horizontal=True)

    if redoks_option == "Permanganometri":
        st.subheader("Permanganometri")
        perm_option = st.selectbox("Pilih Tugas:", ["Standarisasi KMnO4 (Asam Oksalat)", "Penetapan Kadar Fe"])
        
        with st.form("form_permanganat"):
            if "Standarisasi" in perm_option:
                vol_ta = st.number_input("Volume TA (mL)", min_value=0.0, value=10.0, step=0.1)
                weight_ox = st.number_input("Berat Asam Oksalat (mg)", min_value=0.0, value=100.0, step=1.0)
                be_ox = 63.03 # Default
                
                submitted = st.form_submit_button("Hitung Normalitas KMnO4", type="primary")
                if submitted:
                    if validate_inputs(vol_ta, weight_ox):
                        norm = weight_ox / (vol_ta * be_ox)
                        st.success("Perhitungan Selesai")
                        st.metric("Normalitas KMnO4", f"{norm:.5f}", delta="N")
            
            else:
                vol_ta = st.number_input("Volume TA (mL)", min_value=0.0, value=15.0, step=0.1)
                norm_kmno4 = st.number_input("Normalitas KMnO4 (N)", min_value=0.0, value=0.1, step=0.01)
                weight_fe = st.number_input("Berat Sampel Fe (mg)", min_value=0.0, value=250.0, step=1.0)
                
                submitted = st.form_submit_button("Hitung Kadar Fe", type="primary")
                if submitted:
                    if validate_inputs(vol_ta, weight_fe):
                        # % Fe = (V * N * 55.85 / W) * 100
                        weight_fe_g = weight_fe / 1000
                        pct_fe = (vol_ta * norm_kmno4 * 55.85 / weight_fe_g) * 100
                        st.success("Perhitungan Selesai")
                        st.metric("Kadar Fe", f"{pct_fe:.4f}", delta="%")

    else:
        st.subheader("Iodometri")
        iod_option = st.selectbox("Pilih Tugas:", ["Standarisasi Tio (Na2S2O3)", "Penetapan DO"])

        with st.form("form_iodometri"):
            if "Standarisasi" in iod_option:
                vol_ta = st.number_input("Volume TA Tio (mL)", min_value=0.0, value=10.0, step=0.1)
                vol_k2cr2o7 = st.number_input("Volume K2Cr2O7 (mL)", min_value=0.0, value=10.0, step=0.1)
                norm_k2cr2o7 = st.number_input("Normalitas K2Cr2O7 (N)", min_value=0.0, value=0.1, step=0.01)

                submitted = st.form_submit_button("Hitung Normalitas Tio", type="primary")
                if submitted:
                    if validate_inputs(vol_ta, second_vol=vol_k2cr2o7):
                        norm_tio = (vol_k2cr2o7 * norm_k2cr2o7) / vol_ta
                        st.success("Perhitungan Selesai")
                        st.metric("Normalitas Tio", f"{norm_tio:.5f}", delta="N")
            
            else:
                vol_ta = st.number_input("Volume TA Tio (mL)", min_value=0.0, value=5.0, step=0.1)
                norm_tio = st.number_input("Normalitas Tio (N)", min_value=0.0, value=0.1, step=0.01)
                vol_sampel = st.number_input("Volume Sampel Air (mL)", min_value=0.0, value=100.0, step=1.0)

                submitted = st.form_submit_button("Hitung DO", type="primary")
                if submitted:
                    if validate_inputs(vol_ta, second_vol=vol_sampel):
                        # DO = (V * N * 8 * 1000) / Vol_Sample
                        do_val = (vol_ta * norm_tio * 8 * 1000) / vol_sampel
                        st.success("Perhitungan Selesai")
                        st.metric("DO Terlarut", f"{do_val:.4f}", delta="mg/L")

# -----------------------------------------------------------------------------
# BRANCH 4: ALKALIMETRI
# -----------------------------------------------------------------------------
elif branch == "4. Alkalimetri (NaOH)":
    st.header("⚗️ Alkalimetri: Standarisasi NaOH")
    st.markdown("Standarisasi larutan NaOH menggunakan KHP (Kalium Hidrogen Ftalat).")

    with st.form("form_alkalimetri"):
        col1, col2 = st.columns(2)
        with col1:
            vol_ta = st.number_input("Volume TA NaOH (mL)", min_value=0.0, value=15.0, step=0.1)
            weight_khp = st.number_input("Berat KHP (mg)", min_value=0.0, value=204.22, step=0.1, format="%.2f")
        with col2:
            be_khp = 204.22
            st.metric("BE KHP", f"{be_khp} g/eq")
            
        submitted = st.form_submit_button("Hitung Normalitas NaOH", type="primary")

        if submitted:
            if validate_inputs(vol_ta, weight_khp):
                norm_naoh = weight_khp / (vol_ta * be_khp)
                st.success("Perhitungan Selesai")
                st.metric("Normalitas NaOH", f"{norm_naoh:.5f}", delta="N")

# -----------------------------------------------------------------------------
# BRANCH 5: ASIDIMETRI
# -----------------------------------------------------------------------------
elif branch == "5. Asidimetri (HCl/Warder)":
    st.header("⚗️ Asidimetri")
    st.markdown("Penetapan kadar asam atau campuran alkali.")

    asid_option = st.radio("Pilih Metode:", ["Standarisasi HCl", "Penetapan Campuran Warder"], horizontal=True)

    with st.form("form_asidimetri"):
        if asid_option == "Standarisasi HCl":
            st.subheader("Standarisasi HCl dengan Na2CO3")
            
            vol_ta = st.number_input("Volume TA HCl (mL)", min_value=0.0, value=20.0, step=0.1)
            weight_nac = st.number_input("Berat Na2CO3 (mg)", min_value=0.0, value=106.0, step=1.0)
            be_nac = 53.00 # Na2CO3 = 106/2 = 53
            
            submitted = st.form_submit_button("Hitung Normalitas HCl", type="primary")
            
            if submitted:
                if validate_inputs(vol_ta, weight_nac):
                    norm_hcl = weight_nac / (vol_ta * be_nac)
                    st.success("Perhitungan Selesai")
                    st.metric("Normalitas HCl", f"{norm_hcl:.5f}", delta="N")

        else:
            st.subheader("Penetapan Kadar NaOH & Na2CO3 (Warder)")
            
            c1, c2 = st.columns(2)
            with c1:
                ta_1 = st.number_input("TA 1 (Fenolftalein) mL", min_value=0.0, value=10.0, step=0.1)
                ta_2 = st.number_input("TA 2 (Metil Jingga) mL", min_value=0.0, value=25.0, step=0.1)
            with c2:
                norm_hcl = st.number_input("Normalitas HCl (N)", min_value=0.0, value=0.1, step=0.01)
                vol_sampel = st.number_input("Volume Sampel (mL)", min_value=0.0, value=10.0, step=1.0)
            
            submitted = st.form_submit_button("Hitung Kadar Campuran", type="primary")
            
            if submitted:
                if validate_inputs(ta_1) and ta_2 > 0:
                    # Logic for Warder method
                    # Vol HCl for NaOH = 2*TA1 - TA2
                    # Vol HCl for Na2CO3 = 2*(TA2 - TA1)
                    
                    vol_hcl_naoh = 2 * ta_1 - ta_2
                    vol_hcl_nac = 2 * (ta_2 - ta_1)
                    
                    # Check for negative volumes (indicates pure NaOH or pure Na2CO3)
                    if vol_hcl_naoh < 0:
                        st.warning("Hasil Negatif: Sampel")
