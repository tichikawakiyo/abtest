import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
sns.set(font_scale=2)
st.sidebar.markdown('ABテスト対象のデータを入力してください')
visitors_a = st.sidebar.number_input('AのCLICK数', value=100)
conversion_a = st.sidebar.number_input('AのCV数', value=50)
cvr_a = conversion_a / visitors_a
st.sidebar.markdown(f'AのCV率: **{"{:.1%}".format(cvr_a)}**')

visitors_b = st.sidebar.number_input('BのCLICK数', value=100)
conversion_b = st.sidebar.number_input('BのCV数', value=50)
cvr_b = conversion_b / visitors_b
st.sidebar.markdown(f'BのCV率: **{"{:.1%}".format(cvr_b)}**')
st.header('ABテストアプリ')
st.markdown(r'''ABテスト結果のCLICK数とCV数を入力''')
st.subheader('テスト対象')
st.markdown(rf'''
    <table>
      <tr>
        <th>パターン</th><th>CLICK数</th><th>CV数</th><th>CV率</th>
      </tr>
      <tr>
        <td>A</td><td>{visitors_a}</td><td>{conversion_a}</td><td>{"{:.1%}".format(cvr_a)}</td>
      </tr>
      <tr>
        <td>B</td><td>{visitors_b}</td><td>{conversion_b}</td><td>{"{:.1%}".format(cvr_b)}</td>
      </tr>
    </table>
    ''', unsafe_allow_html=True)
st.subheader('ABテスト')
st.markdown('統計的仮説検定のABテスト(統計的仮説検定)の結果。（分散不均等を仮定したt検定）')
a = np.zeros(visitors_a)
a[:conversion_a] = 1
b = np.zeros(visitors_ｂ)
b[:conversion_ｂ] = 1
res = stats.ttest_ind(a, b, equal_var=False)
st.markdown(f'p値: **{"{:.4}".format(res[1])}**')
if res[1] <= 0.05:
  st.markdown(r'''
    <center><font size=7 color="#00B06B">95%の信頼度で有意差あり</font></center>
    ''', unsafe_allow_html=True)
elif res[1] <= 0.1:
  st.markdown(r'''
    <center><font size=7 color="#F2E700">90%の信頼度で有意差あり</font></center>
    ''', unsafe_allow_html=True)
elif res[1] <= 0.2:
  st.markdown(r'''
    <center><font size=7 color="#F2E700">80%の信頼度で有意差あり</font></center>
    ''', unsafe_allow_html=True)
else:
  st.markdown(r'''
    <center><font size=7 color="#FF4B00">有意差なし</font></center>
    ''', unsafe_allow_html=True)

st.markdown('二項検定のABテストの結果。(サンプル少ない場合に利用)')
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
st.subheader('ベイジアンABテスト')
st.markdown('ベイズ推論を活用したABテスト。A, BそれぞれのCVRがどの程度信用できるのかを確認可能。')
alpha_prior = 1
beta_prior = 1
posterior_A = stats.beta(alpha_prior + conversion_a, beta_prior + visitors_a - conversion_a)
posterior_B = stats.beta(alpha_prior + conversion_b, beta_prior + visitors_b - conversion_b)
samples = 450000
samples_posterior_A = posterior_A.rvs(samples)
samples_posterior_B = posterior_B.rvs(samples)
prob = (samples_posterior_A < samples_posterior_B).mean()
fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)
sns.distplot(samples_posterior_A, ax=ax, label='CVR of A')
sns.distplot(samples_posterior_B, ax=ax, label='CVR of B')
ax.set_ylabel('KDE', fontsize='xx-large')
ax.set_xlabel('CVR', fontsize='xx-large')
ax.set_title('distribution of CVR', fontsize='xx-large')
ax.legend(loc='upper right', fontsize='xx-large')
fig.tight_layout()
st.subheader('CVRの信用度の分布')
st.pyplot(fig)
st.markdown(fr'''
  <center><font size=7>CVRがA < Bとなる確率: {"{:.1%}".format(prob)}</font></center>
  ''', unsafe_allow_html=True)