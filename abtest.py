import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
sns.set(font_scale=2)
st.sidebar.markdown('ABテスト対象のデータを入力してください')
visitors_a = st.sidebar.number_input('Aの分母', value=100)
conversion_a = st.sidebar.number_input('Aの分子', value=50)
cvr_a = conversion_a / visitors_a
st.sidebar.markdown(f'Aの母比率: **{"{:%}".format(cvr_a)}**')

visitors_b = st.sidebar.number_input('Bの分母', value=100)
conversion_b = st.sidebar.number_input('Bの分子', value=50)
cvr_b = conversion_b / visitors_b
st.sidebar.markdown(f'Bの母比率: **{"{:%}".format(cvr_b)}**')
st.header('ABテストアプリ')
st.markdown(r'''ABテスト結果の分母と分子を入力''')
st.subheader('テスト対象')
st.markdown(rf'''
    <table>
      <tr>
        <th>パターン</th><th>分母</th><th>分子</th><th>母比率</th>
      </tr>
      <tr>
        <td>A</td><td>{visitors_a}</td><td>{conversion_a}</td><td>{"{:.2%}".format(cvr_a)}</td>
      </tr>
      <tr>
        <td>B</td><td>{visitors_b}</td><td>{conversion_b}</td><td>{"{:.2%}".format(cvr_b)}</td>
      </tr>
    </table>
    ''', unsafe_allow_html=True)
st.subheader('ABテスト')
st.markdown('二項検定のABテストの結果。')
data = np.matrix([ [ conversion_a, visitors_a ], [ conversion_b, visitors_b ] ])
p_a = visitors_a / (visitors_a+visitors_b)
conversion_total = np.sum(data, axis=0).item(0, 0)
conversion_a  = data.item(0,0)
p_value = stats.binom_test(x=conversion_a, n=conversion_total, p=p_a, alternative="two-sided")
st.markdown(f'p値: **{"{:.4}".format(p_value)}**')
if p_value <= 0.05:
  st.markdown(r'''
    <center><font size=7 color="#00B06B">95%の信頼度で有意差あり</font></center>
    ''', unsafe_allow_html=True)
elif p_value <= 0.1:
  st.markdown(r'''
    <center><font size=7 color="#F2E700">90%の信頼度で有意差あり</font></center>
    ''', unsafe_allow_html=True)
elif p_value <= 0.2:
  st.markdown(r'''
    <center><font size=7 color="#F2E700">80%の信頼度で有意差あり</font></center>
    ''', unsafe_allow_html=True)
else:
  st.markdown(r'''
    <center><font size=7 color="#FF4B00">有意差なし</font></center>
    ''', unsafe_allow_html=True)
