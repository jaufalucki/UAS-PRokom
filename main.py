import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

st.set_page_config(page_title="Produksi Minyak Mentah di Dunia", page_icon=":earth_asia:", layout="wide")

# ---- READ DATA ----
@st.cache

def get_data_from_csv():
    df = pd.read_csv('data/produksi_minyak_mentah.csv')
    return df

def get_data_from_json():
    df = pd.read_json('data/kode_negara_lengkap.json')
    return df

df1 = get_data_from_json()
df2 = get_data_from_csv()

plot = [1,2,3,4]

# Penggabungan dataframe
df = pd.merge(df1, df2, how='inner', left_on = 'alpha-3', right_on = 'kode_negara')
n_negara = len(df2.groupby(["kode_negara"]).sum())

# ---- SIDEBAR ----
st.sidebar.markdown("""---""")
st.sidebar.header("** Muhammad Jaufa Lucki Fernanda  **\n ** 12220106 **")
st.sidebar.markdown("""---""")

# Daftar Grafik
st.sidebar.markdown("""
### Daftar grafik:
1. Jumlah produksi minyak mentah terhadap waktu
1. Negara dengan jumlah produksi terbesar pada tahun T
1. Negara dengan jumlah produksi terbesar secara kumulatif
1. Informasi negara dengan produksi terbesar, terkecil dan 0 
""")

# Choose Graph
plot_kind = st.sidebar.multiselect(
    "Silahkan pilih grafik yang ingin ditampilkan: ",
    options=plot,
    default=plot,
    key="1"
)

# ---- MAINPAGE ----
st.markdown("""---""")

st.title(":earth_asia: Produksi Minyak Mentah di Dunia")

st.markdown("""---""")

# ---- GRAPH PLOT -----

# Graph No 1
def show_plot1():
    st.title("** 1. Grafik jumlah produksi minyak mentah terhadap waktu **")
    nama_negara = st.selectbox(
        "Silahkan pilih negara yang ingin ditampilkan: ",
        options=df["name"].unique(),
        key="2"
        )
    negara_dipilih = df.query(
        "name == @nama_negara"
    )
    st.markdown("""---""")
    if len(negara_dipilih) == 0:
        st.markdown(f"""
        
            ### Tidak ada data negara {nama_negara}
        
        """)
    else:
        fig_produksi_terhadap_tahun = px.line(
            negara_dipilih,
            x="tahun",
            y="produksi",
            # orientation="h",
            title=f"<b>Grafik jumlah produksi minyak terhadap waktu negara {nama_negara}</b>",
            template="plotly_white",
            markers=True
        )
        fig_produksi_terhadap_tahun.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        st.write(fig_produksi_terhadap_tahun)
    st.markdown("""---""")

# Graph No 2
def show_plot2():
    st.title("** 2. Negara dengan jumlah produksi terbesar pada tahun T **")
    left_input, right_input = st.columns(2)
    with left_input:
        tahun2 = st.selectbox(
            "Silahkan pilih tahun yang ingin ditampilkan: ",
            options=df2["tahun"].unique(),
            key="4"
        )
    df_tahun2 = df.loc[(df["tahun"] == tahun2)]
    n_negara_t = len(df_tahun2.groupby(["name"]).sum())
    lst_negara = list(range(1,n_negara_t+1))
    with right_input:
        banyak_negara2 = st.selectbox(
            "Silahkan pilih banyak negara yang ingin ditampilkan: ",
            options=lst_negara,
            key="3"
        )
    df_sorted2 = df_tahun2.sort_values(["produksi"], ascending =[0])[0:banyak_negara2]
    fig_produksi_terhadap_negara = px.bar(
    df_sorted2,
    x="produksi",
    y="name",
    orientation="h",
    title=f"<b>Grafik negara produsen minyak terbesar pada tahun {tahun2} (n={banyak_negara2}).</b>",
    template="plotly_white",
    )
    fig_produksi_terhadap_negara.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    st.write(fig_produksi_terhadap_negara)

# Graph No 3
def show_plot3():
    st.title("** 3. Negara dengan jumlah produksi terbesar secara kumulatif **")
    lst_negara3 = list(range(1,n_negara+1))
    banyak_negara3 = st.selectbox(
        "Silahkan pilih banyak negara yang ingin ditampilkan: ",
        options=lst_negara3,
        key="5"
    )
    df3_sum = df.groupby(["name"]).sum()
    df_sorted2 = df3_sum.sort_values(["produksi"], ascending =[0])[0:banyak_negara3]
    fig_produksi_terhadap_negara_kum = px.bar(
    df_sorted2,
    x="produksi",
    y=df_sorted2.index,
    orientation="h",
    title=f"<b>Grafik negara produsen minyak terbesar kumulatif (n={banyak_negara3}).</b>",
    template="plotly_white",
    )
    fig_produksi_terhadap_negara_kum.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    st.write(fig_produksi_terhadap_negara_kum)

# Informasi no 4
def informasi_no4():
    df_selected4 = df[["name","alpha-2","alpha-3","region","sub-region","produksi"]]
    df2_sum = df_selected4.groupby(["name","alpha-2","alpha-3","region","sub-region"], as_index=False).sum()
    value_highest_alltime = df2_sum["produksi"].max()
    non_zero = df2_sum.loc[(df2_sum["produksi"] > 0)]
    value_lowest_alltime = non_zero["produksi"].min()
    st.title("** 4. Informasi negara dengan produksi terbesar, terkecil dan 0 **")
    # Keseluruhan
    st.markdown("""---""")
    st.subheader("** a. Negara dengan produksi minyak terbesar, terkecil dan 0 secara keseluruhan **")
    n_highest = df2_sum.loc[(df2_sum["produksi"] == value_highest_alltime)]
    n_lowest = df2_sum.loc[(df2_sum["produksi"] == value_lowest_alltime)]
    n_zero = df2_sum.loc[(df2_sum["produksi"] == 0)]
    left, right = st.columns(2)
    with left:
        st.write(f"Negara dengan produksi minyak total terbesar")
        st.write(f" Total produksi: {value_highest_alltime}")
        for index, row in n_highest.iterrows():
            st.write(f"Name : {row['name']}")
            st.write(f"Kode negara: {row['alpha-3']}")
            st.write(f"Region: {row['region']}")
            st.write(f"Sub-region: {row['sub-region']}")
    with right: 
        st.write("Negara dengan produksi minyak total terkecil")
        st.write(f" Total produksi: {value_lowest_alltime}")
        for index, row in n_lowest.iterrows():
            st.write(f"Name : {row['name']}")
            st.write(f"Kode negara: {row['alpha-3']}")
            st.write(f"Region: {row['region']}")
            st.write(f"Sub-region: {row['sub-region']}")
    st.markdown("""---""")
    st.write("Negara dengan produksi minyak total adalah 0")
    st.write(n_zero.reset_index()[["name","alpha-2","alpha-3","region","sub-region"]])

    st.markdown("""---""")
    # Pada T tahun
    st.subheader("** b. Negara dengan produksi minyak terbesar, terkecil dan 0 berdasarkan tahun **")
    tahun = st.selectbox(
        "Silahkan pilih tahun yang ingin ditampilkan: ",
        options=df["tahun"].unique(),
        key="6"
        )
    df2_tahun = df.loc[(df["tahun"] == tahun)]
    value_highest = df2_tahun["produksi"].max()
    non_zero_t = df2_tahun[(df2_tahun["produksi"] > 0)]
    value_lowest = non_zero_t["produksi"].min()    
    n_highest_t = df2_tahun.loc[(df2_tahun["produksi"] == value_highest)]
    n_lowest_t = df2_tahun.loc[(df2_tahun["produksi"] == value_lowest)]
    n_zero_thn = df2_tahun.loc[(df2_tahun["produksi"] == 0)]
    left_t, right_t = st.columns(2)
    with left_t:
        st.write(f"Negara dengan produksi minyak total terbesar tahun {tahun}")
        st.write(f" Total produksi: {value_highest}")
        for index, row in n_highest_t.iterrows():
            st.write(f"Name : {row['name']}")
            st.write(f"Kode negara: {row['alpha-3']}")
            st.write(f"Region: {row['region']}")
            st.write(f"Sub-region: {row['sub-region']}")
        
    with right_t:
        st.write(f"Negara dengan produksi minyak total terkecil tahun {tahun}")
        st.write(f" Total produksi: {value_lowest}")
        for index, row in n_lowest_t.iterrows():
            st.write(f"Name : {row['name']}")
            st.write(f"Kode negara: {row['alpha-3']}")
            st.write(f"Region: {row['region']}")
            st.write(f"Sub-region: {row['sub-region']}")
    st.markdown("""---""")
    st.write(f"Negara dengan produksi minyak total adalah 0 tahun {tahun}")
    st.write(n_zero_thn.reset_index()[["name","alpha-2","alpha-3","region","sub-region"]])

    
# Show Plot
if 1 in plot_kind:
    show_plot1()
if 2 in plot_kind:
    show_plot2()
if 3 in plot_kind:
    show_plot3()
if 4 in plot_kind:
    informasi_no4()

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
