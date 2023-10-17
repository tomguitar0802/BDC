import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#-----------------------入力-----------------------
Path="BDC.xlsx"                         #ファイル名
mass_list=[100,200,300]                 #m/zリスト
N_round=0                               #四捨五入の桁
relative=True                           #相対or絶対
legend_out=True                         #凡例の位置
#--------------------------------------------------

Path=st.sidebar.file_uploader('Excelファイル')
y_label="Relative Intensity (%)"

if Path is not None:
    mass_list=list(map(int,st.sidebar.text_input('m/z').split(",")))
    relative=st.sidebar.radio('強度',("相対","絶対"))
    N=st.sidebar.slider('四捨五入の桁',0,5,0,1)
    legend_out=st.sidebar.radio('凡例',("グラフ外","グラフ内"))
    
    #ExcelからDataFrameの作成
    CE_list=pd.ExcelFile(Path).sheet_names
    for CE in CE_list:
        df=pd.read_excel(Path,sheet_name=CE,skiprows=7)
        df=df.round({"Mass":N_round})
        df=df.groupby("Mass").sum()
        df=df.rename(columns={"Intensity":CE})
        if CE==CE_list[0]:
            DF=df
        else:
            DF=pd.concat([DF,df],axis=1)

    #相対化処理と縦軸ラベルの設定
    if relative=="相対":
        DF=DF/DF.sum()
        y_label="Relative Intensity (%)"
    else:
        y_label="Absolute Intensity (arb)"

    #m/zリストを抜き出してプロット
    fig,ax=plt.subplots()
    ax.ticklabel_format(useOffset=False,useMathText=True)
    for mass in mass_list:
        plt.plot(CE_list,DF.loc[mass],
                marker="o",
                label="$\it{m/z}$"+str(mass))

#グラフの詳細設定
plt.xlabel("Collision Energy (eV)")
plt.ylabel(y_label)
if legend_out=="グラフ外":
    plt.legend(loc='upper left',bbox_to_anchor=(1,1))
else:
    plt.legend()
st.pyplot(fig)
