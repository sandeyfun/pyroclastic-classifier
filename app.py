import streamlit as st
import matplotlib.pyplot as plt
import ternary

# Mengatur judul halaman website
st.set_page_config(page_title="Pyroclastic Classifier", layout="centered")
st.title("🌋 Pyroclastic Rock Classifier & Plotter")
st.write("Masukkan persentase atau jumlah material piroklastik di bawah ini:")

# 1. User Inputs (Menggantikan fungsi input() di terminal)
col1, col2, col3 = st.columns(3)
with col1:
    in_blocks = st.number_input("Blocks/Bombs (>64mm)", min_value=0.0, value=0.0)
with col2:
    in_lapilli = st.number_input("Lapilli (2-64mm)", min_value=0.0, value=0.0)
with col3:
    in_ash = st.number_input("Ash (<2mm)", min_value=0.0, value=0.0)

# Tombol untuk memproses data
if st.button("Classify & Plot Diagram"):
    total = in_blocks + in_lapilli + in_ash

    if total == 0:
        st.error("Error: Total material tidak boleh nol. Silakan masukkan angka.")
    else:
        # 2. Normalization
        B = (in_blocks / total) * 100
        L = (in_lapilli / total) * 100
        A = (in_ash / total) * 100

        # 3. Classification (IUGS / Schmid)
        if B >= 75:
            name = "Pyroclastic Breccia / Agglomerate"
        elif A >= 75:
            name = "Tuff / Ash Tuff"
        elif L >= 75:
            name = "Lapillistone"
        elif B >= 25 and L >= 25 and A < 25:
            name = "Lapilli Breccia"
        elif B >= 25 and A >= 25 and L < 25:
            name = "Tuff Breccia"
        elif A >= 25 and L >= 25 and B < 25:
            name = "Lapilli Tuff"
        elif B >= 25:
            name = "Tuff Breccia"
        else:
            name = "Lapilli Tuff"

        # 4. Setup Ternary Plot
        scale = 100
        fig, tax = ternary.figure(scale=scale)
        fig.set_size_inches(8, 6)

        # 5. Draw Reference Lines
        tax.line((0, 75, 25), (25, 75, 0), linewidth=1.5, color='black')
        tax.line((0, 25, 75), (75, 25, 0), linewidth=1.5, color='black')
        tax.line((0, 25, 75), (25, 0, 75), linewidth=1.5, color='black')
        tax.line((75, 25, 0), (75, 0, 25), linewidth=1.5, color='black')

        # 6. Plot the Data Point
        point = (A, B, L)
        tax.scatter([point], marker='o', color='red', s=150, edgecolors='black', zorder=5, label=name)

        # 7. Labelling
        ax = tax.get_axes()
        tax.set_title(f"Classification: {name}\n", fontsize=14, pad=15)

        ax.text(50, 103, "Blocks and Bombs (> 64 mm)", fontsize=10, fontweight='bold', ha='center')
        ax.text(-8, -8, "Lapilli (2–64 mm)", fontsize=10, fontweight='bold', ha='center')
        ax.text(108, -8, "Ash (< 2 mm)", fontsize=10, fontweight='bold', ha='center')

        # Formatting diagram
        tax.boundary(linewidth=2)
        tax.gridlines(color="gray", multiple=10, linewidth=0.5, linestyle=':')
        tax.clear_matplotlib_ticks()
        ax.axis('off')

        # 8. Menampilkan Hasil di Website (Menggantikan print dan plt.show)
        st.success(f"**Classification Result:** {name}")

        st.write(f"**Composition:** Blocks: {B:.1f}% | Lapilli: {L:.1f}% | Ash: {A:.1f}%")

        # Menampilkan grafik Matplotlib ke web Streamlit
        st.pyplot(fig)