import math
import streamlit as st

# =========================
# CẤU HÌNH TRANG WEB
# =========================
st.set_page_config(page_title="Tic-Tac-Toe AI Visualizer", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS cho nút bấm bàn cờ và Console
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 100px;
        font-size: 36px !important;
        font-weight: bold;
    }
    .console-box {
        background-color: #000000;
        color: #4ade80;
        font-family: 'Courier New', monospace;
        padding: 15px;
        border-radius: 5px;
        height: 400px;
        overflow-y: auto;
        white-space: pre-wrap;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# GAME STATE (Lưu trạng thái trên Web)
# =========================
if "board" not in st.session_state:
    st.session_state.board = [[' ' for _ in range(3)] for _ in range(3)]
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "status" not in st.session_state:
    st.session_state.status = "👤 Your Turn (X)"
if "log_text" not in st.session_state:
    st.session_state.log_text = "Welcome! You are X (plays first).\nAI is O.\nWaiting for your move...\n"

# =========================
# UI HELPERS
# =========================
def add_log(text):
    st.session_state.log_text += str(text) + "\n"

# =========================
# GAME LOGIC (Giữ nguyên gốc của bạn)
# =========================
def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != ' ': return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ': return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != ' ': return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ': return board[0][2]
    return None

def is_draw(board):
    for row in board:
        if ' ' in row: return False
    return True

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'O': return 1
    if winner == 'X': return -1
    if is_draw(board): return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(best_score, score)
        return best_score

# =========================
# GAME OVER CHECK
# =========================
def check_game_over():
    winner = check_winner(st.session_state.board)
    if winner == 'X':
        st.session_state.status = "🎉 You Won!"
        add_log("\n>>> GAME OVER: PLAYER (X) WINS! <<<")
        st.session_state.game_over = True
        return True
    if winner == 'O':
        st.session_state.status = "🤖 AI Won!"
        add_log("\n>>> GAME OVER: AI (O) WINS! <<<")
        st.session_state.game_over = True
        return True
    if is_draw(st.session_state.board):
        st.session_state.status = "🤝 Draw!"
        add_log("\n>>> GAME OVER: DRAW <<<")
        st.session_state.game_over = True
        return True
    return False

# =========================
# AI TURN
# =========================
def ai_turn():
    best_score = -math.inf
    best_move = None

    add_log("\n=== AI IS ANALYZING POSSIBLE MOVES ===")
    add_log("Score: 1 = AI Wins | 0 = Draw | -1 = Player Wins")
    add_log("-" * 48)

    move_scores = []
    
    for i in range(3):
        for j in range(3):
            if st.session_state.board[i][j] == ' ':
                st.session_state.board[i][j] = 'O'
                score = minimax(st.session_state.board, 0, False)
                st.session_state.board[i][j] = ' '
                move_scores.append(((i, j), score))

                outcome = "AI Wins" if score == 1 else "Draw" if score == 0 else "Player Wins"
                add_log(f"-> Trying ({i}, {j}) | Score: {score} ({outcome})")

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    add_log("-" * 48)
    add_log("AI Choice Report:")
    for move, score in move_scores:
        marker = "<- FIRST OPTIMAL MOVE" if move == best_move else ""
        add_log(f" * Cell {move}: Score = {score} {marker}")

    if best_move:
        r, c = best_move
        st.session_state.board[r][c] = 'O'
        add_log(f"\nAI places O at {best_move}")
        add_log("Waiting for your turn...")
    
    add_log("=" * 48)
    
    if not check_game_over():
        st.session_state.status = "👤 Your Turn (X)"

# =========================
# PLAYER TURN
# =========================
def cell_click(row, col):
    if st.session_state.board[row][col] == ' ' and not st.session_state.game_over:
        st.session_state.board[row][col] = 'X'
        add_log(f"\nYou placed X at ({row}, {col})")
        
        if not check_game_over():
            ai_turn()

def reset_game():
    st.session_state.board = [[' ' for _ in range(3)] for _ in range(3)]
    st.session_state.game_over = False
    st.session_state.status = "👤 Your Turn (X)"
    st.session_state.log_text = "Welcome! You are X (plays first).\nAI is O.\nWaiting for your move...\n"

# =========================
# WINDOW - LAYOUT
# =========================
st.title("Tic-Tac-Toe AI Visualizer")

# Hiển thị thanh trạng thái
if "🎉" in st.session_state.status:
    st.success(st.session_state.status)
elif "🤖" in st.session_state.status:
    st.error(st.session_state.status)
elif "🤝" in st.session_state.status:
    st.warning(st.session_state.status)
else:
    st.info(st.session_state.status)

# Chia màn hình làm 2 cột: Trái là Bàn cờ, Phải là Console
col_board, col_log = st.columns([1, 1.5])

with col_board:
    st.subheader("Bàn cờ")
    for i in range(3):
        row_cols = st.columns(3)
        for j in range(3):
            cell_value = st.session_state.board[i][j]
            button_label = cell_value if cell_value != ' ' else " "
            is_disabled = st.session_state.game_over or cell_value != ' '
            
            with row_cols[j]:
                if st.button(button_label, key=f"btn_{i}_{j}", disabled=is_disabled):
                    cell_click(i, j)
                    st.rerun()
                    
    st.write("")
    if st.button("🔄 Restart Game", use_container_width=True):
        reset_game()
        st.rerun()

with col_log:
    st.subheader("AI CONSOLE")
    # Hiển thị log như một màn hình terminal
    st.markdown(f'<div class="console-box">{st.session_state.log_text}</div>', unsafe_allow_html=True)