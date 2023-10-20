import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

Path=st.sidebar.file_uploader('Excelファイル')
ms=st.sidebar.radio('装置',("カンタム","オービ"))
if ms=="カンタム":
    skiprows=7
else:
    skiprows=8
if Path is not None:
    N_round=st.sidebar.slider('四捨五入の桁',0,5,0,1)
    relative=st.sidebar.radio('縦軸',("絶対強度","%"))

    #ExcelからDataFrameの作成
    CE_list=pd.ExcelFile(Path).sheet_names
    for CE in CE_list:
        df=pd.read_excel(Path,sheet_name=CE,skiprows=skiprows)
        df=df.round({"Mass":N_round})
        df=df.groupby("Mass").sum()
        df=df.rename(columns={"Intensity":CE})
        if CE==CE_list[0]:
            DF=df
        else:
            DF=pd.concat([DF,df],axis=1)

    #m/zの選択
    sugest=DF.sum(axis=1).sort_values(ascending=False).head(10).index.tolist()
    if N_round==0:
        sugest=map(int,sugest)
        sugest=",".join(map(str,sugest))
        mass_list=list(map(int,st.sidebar.text_input('m/z',sugest).split(",")))
    else:
        sugest=",".join(map(str,sugest))
        mass_list=list(map(float,st.sidebar.text_input('m/z',sugest).split(",")))

    #m/zリストの抜き出し
    DF=DF.loc[mass_list,:]
    
    #相対化処理と縦軸ラベルの設定
    if relative=="絶対強度":
        y_label="Absolute Intensity (arb)"
    else:
        DF=DF/DF.sum()
        y_label="Relative Intensity (%)"
    x_label=st.sidebar.text_input("x軸ラベル","Collision Energy (eV)")
    
    #プロットとグラフの詳細設定
    fig,ax=plt.subplots()
    ax.ticklabel_format(useOffset=False,useMathText=True)
    marker=st.sidebar.radio("マーカー",("o",".",None))
    for mass in mass_list:
        plt.plot(CE_list,DF.loc[mass],
                marker=marker,
                label="$\it{m/z}$ "+str(mass))
    
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    legend_out=st.sidebar.radio('凡例',("グラフ外","グラフ内"))
    if legend_out=="グラフ外":
        plt.legend(loc='upper left',bbox_to_anchor=(1,1))
    else:
        plt.legend()
    st.pyplot(fig)

    #表の表示
    st.write(DF)
