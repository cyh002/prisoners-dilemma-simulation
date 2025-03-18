import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_leaderboard(leaderboard, coop_rate_history):
    root = tk.Tk()
    root.title("Tournament Leaderboard & Cooperation Rate")
    # Leaderboard frame
    frame_lb = ttk.Frame(root)
    frame_lb.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame_lb, columns=("Rank", "Player", "Score"), show="headings")
    tree.heading("Rank", text="Rank")
    tree.heading("Player", text="Player")
    tree.heading("Score", text="Score")
    for rank, (player, score) in enumerate(leaderboard, start=1):
        tree.insert("", "end", values=(rank, player, score))
    tree.pack(fill=tk.BOTH, expand=True)

    # Plot frame
    frame_plot = ttk.Frame(root)
    frame_plot.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    fig, ax = plt.subplots(figsize=(5,3))
    ax.plot(coop_rate_history, marker="o")
    ax.set_title("Global Cooperation Rate Over Matches")
    ax.set_xlabel("Match Index")
    ax.set_ylabel("Cooperation Rate")
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    root.mainloop()
