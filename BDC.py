import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('ブレイクダウンカーブ代行業者')
st.sidebar.write("【必須項目】")
Data=st.sidebar.file_uploader('Excelファイル')
collision_energy=list(map(int,st.sidebar.text_input('CE').split()))
focus_mz=list(map(int,st.sidebar.text_input('m/z').split()))
st.sidebar.write("【オプション機能】")
standardization=st.sidebar.checkbox('相対化',value=True)
if standardization==True:
    kyoudo="Relative Intensity(%)"
else:
    kyoudo="Absolute Intensity"
graph_title=st.sidebar.text_input('グラフタイトル','')
x_label=st.sidebar.text_input('x軸ラベル','Collision Energy(eV)')
y_label=st.sidebar.text_input('y軸ラベル',kyoudo)
FontSize=st.sidebar.slider('フォントサイズ',5,25,15,1)
yoko=st.sidebar.slider("グラフサイズ横",1.0,10.0,8.0,0.1)
tate=st.sidebar.slider("グラフサイズ縦",1.0,10.0,6.0,0.1)
hanrei=st.sidebar.checkbox('凡例グラフ内表示',value=True)
marker=st.sidebar.checkbox('マーカー',value=True)
st.sidebar.write("【Excel読込設定】")
skip_rows=int(st.sidebar.text_input('スキップ','7'))
mass=st.sidebar.text_input('m/z参照','Mass')
intensity=st.sidebar.text_input('強度参照','Intensity')

fig,ax=plt.subplots(figsize=(yoko,tate))

DF,mz,Sheet=[],[],[]

if Data is not None:
    for i in range(len(collision_energy)):
        Sheet.append("Sheet"+str(i+1))

    def read_sheet(a):
        df=pd.read_excel(Data,sheet_name=Sheet[a],skiprows=skip_rows)
        if standardization==True:
            df=pd.DataFrame({'mz':round(df[mass]),'%':df[intensity]/sum(df[intensity])*100})
        else:
            df=pd.DataFrame({'mz':round(df[mass]),'%':df[intensity]})
        Df= df.loc[df.groupby('mz')['%'].idxmax()]
        DF.append(Df.set_index('mz'))

    for b in range(len(collision_energy)):
        read_sheet(b)

    for c in range(len(focus_mz)):
        sublist=[]
        for d in DF:
            sublist.append(d.at[focus_mz[c],'%'])
        mz.append(sublist)

    for e in range(len(focus_mz)):
        if marker==True:
            ax.plot(collision_energy,mz[e],marker='o',label="m/z"+str(focus_mz[e]))
        else:
            ax.plot(collision_energy,mz[e],label="m/z"+str(focus_mz[e]))

ax.set_xlabel(x_label,size=FontSize)
ax.set_ylabel(y_label,size=FontSize)
ax.set_xticks(collision_energy)
ax.set_title(graph_title,size=FontSize+3)
ax.ticklabel_format(useOffset=False,useMathText=True)
if hanrei==True:
    ax.legend()
else:
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
st.pyplot(fig)

