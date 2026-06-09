import streamlit as st
import random

# 1. إعدادات الصفحة
st.set_page_config(page_title="لعبة إكس أو الذكية", page_icon="❌", layout="centered")

st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎮 لعبة Tic-Tac-Toe (إكس أو) 🎮</h1>", unsafe_allow_html=True)
st.write("العب ضد الكمبيوتر! أنت تلعب بـ **X** والكمبيوتر يلعب بـ **O**.")
st.markdown("---")

# 2. تهيئة الذاكرة لحفظ حالة اللعبة واللوحة
if 'board' not in st.session_state:
    st.session_state.board = [" "] * 9
if 'player_score' not in st.session_state:
    st.session_state.player_score = 0
if 'bot_score' not in st.session_state:
    st.session_state.bot_score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None

# دالة للتحقق من وجود فائز
def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # الخطوط الأفقية
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # الخطوط العمودية
        [0, 4, 8], [2, 4, 6]             # الخطوط المائلة
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != " ":
            return board[condition[0]]
    if " " not in board:
        return "تعادل"
    return None

# دالة لحركة الكمبيوتر (الذكاء الاصطناعي البسيط)
def bot_move():
    if st.session_state.game_over:
        return
    
    # البحث عن المربعات الفارغة
    empty_cells = [i for i, cell in enumerate(st.session_state.board) if cell == " "]
    
    if empty_cells:
        # الكمبيوتر يختار مربع عشوائي من المربعات الفاضية
        move = random.choice(empty_cells)
        st.session_state.board[move] = "O"
        
        # التحقق من الفوز بعد حركة الكمبيوتر
        result = check_winner(st.session_state.board)
        if result:
            st.session_state.game_over = True
            st.session_state.winner = result
            if result == "O":
                st.session_state.bot_score += 1

# 3. عرض لوحة النقاط في الأعلى
col_s1, col_s2 = st.columns(2)
with col_s1:
    st.metric(label="👤 نقاطك (X)", value=st.session_state.player_score)
with col_s2:
    st.metric(label="🤖 نقاط الكمبيوتر (O)", value=st.session_state.bot_score)

st.markdown("###")

# 4. رسم لوحة اللعبة (3 أسطر × 3 أعمدة)
grid = [st.columns(3) for _ in range(3)]

for i in range(9):
    row = i // 3
    col = i % 3
    
    # تحديد النص المعروض داخل الزر
    cell_text = st.session_state.board[i]
    
    # عند الضغط على المربع من قبل اللاعب
    if grid[row][col].button(cell_text if cell_text != " " else "  ", key=f"btn_{i}", disabled=st.session_state.game_over or cell_text != " "):
        st.session_state.board[i] = "X"
        
        # التحقق هل فاز اللاعب؟
        result = check_winner(st.session_state.board)
        if result:
            st.session_state.game_over = True
            st.session_state.winner = result
            if result == "X":
                st.session_state.player_score += 1
        else:
            # إذا لم يفز اللاعب، يحين دور الكمبيوتر ليلعب فوراً
            bot_move()
            
        st.rerun()

# 5. عرض النتيجة النهائية للجولة
if st.session_state.game_over:
    st.markdown("---")
    if st.session_state.winner == "X":
        st.success("🎉 كفووو! لقد فزت على الكمبيوتر! 🎉")
        st.balloons()
    elif st.session_state.winner == "O":
        st.error("🤖 الكمبيوتر فاز هذه المرة! حاول مجدداً واهزمه.")
    else:
        st.info("🤝 جولة قوية! انتهت المباراة بالتعادل.")
    
    # زر لإعادة اللعب وتصفير اللوحة فقط مع الاحتفاظ بالنقاط
    if st.button("جولة جديدة 🔄"):
        st.session_state.board = [" "] * 9
        st.session_state.game_over = False
        st.session_state.winner = None
        st.rerun()

# زر اختياري لتصفير كل شيء من البداية
if st.sidebar.button("إعادة تصغير النقاط بالكامل 🧹"):
    st.session_state.board = [" "] * 9
    st.session_state.player_score = 0
    st.session_state.bot_score = 0
    st.session_state.game_over = False
    st.session_state.winner = None
    st.rerun()
