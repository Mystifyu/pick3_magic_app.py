import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# 🌟 App Configuration
st.set_page_config(page_title="Pick 3 Magic Predictor", layout="wide")
st.title("🔮 Pick 3 Magic Predictor")
st.subheader("Let Zara whisper winning patterns from the world of numbers...")

# 📂 Upload File
uploaded_file = st.file_uploader("Upload your Pick 3 Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Sheet1")
    df.columns = ['Date', 'Draw Type', 'D1', 'D2', 'D3']
    df['Draw Type'] = df['Draw Type'].map({'D': 'Day', 'E': 'Evening'})
    df[['D1','D2','D3']] = df[['D1','D2','D3']].astype(str)
    df['Full Number'] = df['D1'] + df['D2'] + df['D3']

    st.success("✅ File loaded successfully!")

    # 🎯 AI Suggested Number
    freq_pos = {pos: df[pos].value_counts() for pos in ['D1','D2','D3']}
    suggested = ''.join(freq_pos[pos].idxmax() for pos in ['D1','D2','D3'])
    st.markdown(f"### 🎯 AI Suggested Pick 3 Number: `{suggested}`")

    # 🔮 Zara’s Whispering Magic
    class ZaraWhispers:
        meanings = {
            '0': "a hidden door", '1': "a beam of light", '2': "twin moons",
            '3': "triangle of truth", '4': "four winds", '5': "the golden spiral",
            '6': "a swirl of time", '7': "dragon’s breath", '8': "infinity’s glow",
            '9': "echoes of fire"
        }

        def whisper(self, digits):
            return [self.meanings[d] for d in digits]

    zara = ZaraWhispers()
    st.markdown("### 🔮 Zara hears:")
    st.write(", ".join(zara.whisper(list(suggested))))

    st.divider()

    # 📊 Digit Frequency by Position
    st.subheader("📊 Digit Frequency by Position")
    for pos in ['D1','D2','D3']:
        st.write(f"**Position {pos}**")
        fig, ax = plt.subplots()
        freq_pos[pos].sort_index().plot(kind='bar', ax=ax, color='#6fa8dc')
        ax.set_xlabel("Digit")
        ax.set_ylabel("Frequency")
        ax.set_title(f"Digit Frequency in {pos}")
        st.pyplot(fig)

    st.divider()

    # 🌞 Day vs 🌒 Evening
    st.subheader("🌞 vs 🌒 Digit Distribution")
    df_melted = pd.melt(df, id_vars=['Draw Type'], value_vars=['D1','D2','D3'],
                        var_name='Position', value_name='Digit')
    fig2, ax2 = plt.subplots()
    sns.countplot(data=df_melted, x='Digit', hue='Draw Type', palette='coolwarm', ax=ax2)
    ax2.set_title("Digit Frequency by Draw Type")
    st.pyplot(fig2)

    st.divider()

    # 🔁 Number Transitions
    st.subheader("🔁 Top Number Transitions")
    df['Previous'] = df['Full Number'].shift(1)
    df['Transition'] = df['Previous'] + " ➜ " + df['Full Number']
    top_trans = df['Transition'].value_counts().head(10)
    fig3, ax3 = plt.subplots()
    top_trans.plot(kind='barh', ax=ax3, color='#b6d7a8')
    ax3.set_title("Top 10 Transitions")
    st.pyplot(fig3)

    st.divider()

    # 🔥 Digit Heatmap
    st.subheader("🔥 Digit Heatmap by Position")
    heatmap_data = pd.DataFrame({
        'D1': df['D1'].value_counts(),
        'D2': df['D2'].value_counts(),
        'D3': df['D3'].value_counts()
    }).fillna(0)
    fig4, ax4 = plt.subplots()
    sns.heatmap(heatmap_data.T, cmap="YlGnBu", annot=True, fmt=".0f", ax=ax4)
    ax4.set_title("Digit Heatmap")
    st.pyplot(fig4)

    st.divider()

    # 📉 Overdue Digits Panel
    st.subheader("📉 Overdue Digits")
    latest_digits = pd.concat([df['D1'], df['D2'], df['D3']])
    all_digits = set(map(str, range(10)))
    last_seen = {digit: df[df[['D1','D2','D3']].isin([digit]).any(axis=1)].sort_values('Date', ascending=False)['Date'].max()
                 for digit in all_digits}
    overdue = pd.Series(last_seen).sort_values()
    st.dataframe(overdue.rename("Last Seen"))

    st.divider()

    # 🍀 Zara’s Lucky Streak Panel
    st.subheader("🍀 Zara’s Lucky Streaks")
    recent_df = df.tail(30)
    streak_digits = pd.concat([recent_df['D1'], recent_df['D2'], recent_df['D3']]).value_counts()
    fig5, ax5 = plt.subplots()
    streak_digits.sort_values().plot(kind='barh', ax=ax5, color='#ffda99')
    ax5.set_title("Most Active Digits (Last 30 Draws)")
    st.pyplot(fig5)

else:
    st.warning("📂 Please upload your Pick 3 Excel file to begin!")
