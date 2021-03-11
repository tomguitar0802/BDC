import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
fig,ax=plt.subplots()

st.title('ブレイクダウンカーブ代行')
Data=st.sidebar.file_uploader('Excelファイル')
focus_mz=list(map(int,st.sidebar.text_input('m/z').split()))
collision_energy=list(map(int,st.sidebar.text_input('CE').split()))
standardization=st.sidebar.checkbox('規格化',value=True)
graph_title=st.sidebar.text_input('グラフタイトル','Break Down Curve of ')
x_label=st.sidebar.text_input('x軸ラベル','Collision Energy(eV)')
y_label=st.sidebar.text_input('y軸ラベル','Relative Intensity(%)')
marker=st.sidebar.checkbox('マーカー',value=True)
skip_rows=int(st.sidebar.text_input('スキップ','7'))
mass=st.sidebar.text_input('m/z参照','Mass')
intensity=st.sidebar.text_input('強度参照','Intensity')

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

ax.set_xlabel(x_label)
ax.set_ylabel(y_label)
ax.set_xticks(collision_energy)
ax.set_title(graph_title)
ax.legend()
st.pyplot(fig)


