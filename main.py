import sys, pygame as pg
import numpy as np
import webbrowser
import tkinter as tk
from tkinter import ttk

from button import Button
from draw import Draw
from game import WumpusWorld


space = 85

AQUA = (49, 255, 255)
WHITE = (255, 255, 255)
GREEN = (67, 83, 24)
LIGHT_GREEN = (194, 203, 159)
BLUE = (6, 61, 81)
TRANSPARENT = (0, 0, 0, 255)

HEIGHT = 550
WIDTH = 780

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Wumpus World AI Agent")

def generate_board():
    board = np.zeros((4, 4))
    return board


def over():
    draw = Draw(screen)

    while True:
        MOUSE_POS = pg.mouse.get_pos()
        btn_reset = Button((550, 250), " Reset ", GREEN, LIGHT_GREEN)
        btn_back = Button((680, 250), " Menu ", GREEN, LIGHT_GREEN)

        for button in [btn_reset, btn_back]:
            button.update_color(MOUSE_POS)
            button.draw_button(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                if confirm_quit():
                    pg.quit()
                    sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                    
                if btn_reset.click_button(MOUSE_POS):
                    wumpus_world()

                if btn_back.click_button(MOUSE_POS):
                    main() 

        draw.board()
        pg.display.flip()

def wumpus_world():
    pg.event.clear()

    arrows_count = 3
    grabbed = killed = False   

    draw = Draw(screen)
    ww = WumpusWorld()
    ww.prepare_environment()
    
    game_bg = pg.image.load("assets/game-bg1.png")
    screen.blit(game_bg, (0,0)) 
    while True:
        
        MOUSE_POS = pg.mouse.get_pos()

        btn_ai = Button((550, 180), "Play AI", GREEN, LIGHT_GREEN)
        btn_reset = Button((550, 250), " Reset ", GREEN, LIGHT_GREEN)
        btn_back = Button((680, 250), " Menu ", GREEN, LIGHT_GREEN)
       
        for button in [btn_ai, btn_reset, btn_back]:
            button.update_color(MOUSE_POS)
            button.draw_button(screen)
            
        draw.fill_env(ww.cur_row, ww.cur_col, ww.world)        
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                if confirm_quit():
                    pg.quit()
                    sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                
                if btn_reset.click_button(MOUSE_POS):
                    wumpus_world()

                if btn_back.click_button(MOUSE_POS):
                    main()

                if btn_ai.click_button(MOUSE_POS):
                    while True:
                        ww.cur_row, ww.cur_col = ww.agent.get_move(ww.agent.has_gold)
                        ww.agent.direction(ww.cur_row, ww.cur_col)
                        draw.fill_env(ww.cur_row, ww.cur_col, ww.world)  
                        ww.move_agent(ww.cur_row, ww.cur_col)
                        ww.path[ww.cur_row][ww.cur_col] = 1     

                        pg.time.delay(500)
                        draw.agent(ww.cur_row, ww.cur_col, ww.agent.facing)  
                        draw.score(f"{ww.agent.score}", GREEN)
                        for row in range(4):
                            for col in range(4):
                                if ww.path[row][col]:
                                    draw.fill_env(row, col, ww.world)
                                draw.agent(ww.cur_row, ww.cur_col, ww.agent.facing)  
                        
                        stats = ww.game_status()
                        if stats == -1:
                            draw.status("Game is ongoing!", LIGHT_GREEN)            
                        elif stats == 0 and not grabbed:
                            draw.status(" You found the  golden treasure!", WHITE)                  
                            ww.world = ww.agent.grab(ww.cur_row, ww.cur_col, ww.world)
                            draw.agent(ww.cur_row, ww.cur_col, ww.agent.facing)   
                            ww.g_w_p_coords[0] = None
                            pg.display.update()
                            grabbed = True
                        elif stats == 1:
                            draw.status(" Game over. You met the Wumpus!", WHITE) 
                            draw.environment(ww.world)
                            over()
                        elif 2 <= stats < 5:
                            draw.status(" Game over. You fall into the pit!", WHITE) 
                            draw.environment(ww.world)
                            over()
                        elif stats == 9 and grabbed:
                            if ww.agent.location == (0, 0):
                                draw.status("   Agent win!   Congratulations!", WHITE) 
                                draw.environment(ww.world)
                                draw.agent(ww.cur_row, ww.cur_col, 'V')  
                                over()
                        elif stats == 10:
                            if arrows_count != 0:
                                draw.fill_env(ww.agent.w_pos[0], ww.agent.w_pos[1], ww.world)  
                                draw.arrows(ww.agent.facing, ww.agent.location)
                                ww.agent.score -= 10

                                if ww.is_wumpus_killed(ww.agent.facing):
                                    ww.g_w_p_coords[1] = None
                                    draw.status(" Wumpus scream! You killed Wumpus.", WHITE)  
                                    ww.agent.score += 2000
                                else:
                                    draw.status("Wumpus not killed!", AQUA)  
                                arrows_count -= 1

                            ww.agent.w_found = False
                            pg.display.update()

                        else:
                            pass      

                        pg.display.update()
                            
        draw.score(f"{ww.agent.score}", GREEN)
        draw.status("Click the 'Play AI' button!", WHITE)    
        draw.agent(ww.cur_row, ww.cur_col, ww.agent.facing)  
        
        draw.board()
        pg.display.flip()


def description():
    game_bg = pg.image.load("assets/description-bg.png")
    screen.blit(game_bg, (0,0))
    
    while True:
        MOUSE_POS = pg.mouse.get_pos()

        btn_back = Button((710, 490), "Back \u25BA", BLUE, LIGHT_GREEN)
       
        btn_back.update_color(MOUSE_POS)
        btn_back.draw_button_transparent(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                if confirm_quit():
                    pg.quit()
                    sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:

                if btn_back.click_button(MOUSE_POS):
                    main()
        
        pg.display.flip()


def confirm_quit():
    global confirm
    def center_window(window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def open_repo_link():
        webbrowser.open("https://github.com/Getachew0557/Wumpus-world-AI-agent.git")

    def quit_game():
        global confirm
        custom_dialog.destroy()
        confirm = True

    def destroy_dialog():
        global confirm
        custom_dialog.destroy()
        confirm = False

    root = tk.Tk()
    root.withdraw()
    custom_dialog = tk.Toplevel(root, bg="white")
    custom_dialog.title("Quit")

    custom_style = ttk.Style()
    custom_style.configure("Custom.TButton", borderwidth=0, relief="solid", border_radius=5, background="white")
    
    message_label = tk.Label(custom_dialog, text="Leaving the Wumpus World.\nIs it time to conquer new realms? 🚀", bg="white")
    message_label.pack(padx=40, pady=20)

    no_button = ttk.Button(custom_dialog, text="No", style="Custom.TButton", command=destroy_dialog)
    no_button.pack(side="right", padx=(5, 25), pady=15)
    yes_button = ttk.Button(custom_dialog, text="Yes", style="Custom.TButton", command=quit_game)
    yes_button.pack(side="right", padx=(25, 5), pady=15)
    
    repo_label = tk.Label(custom_dialog, text="Click here to explore the Git repository👋🏼", fg="blue", cursor="hand2", bg="white")
    repo_label.pack(padx=10, pady=15)
    repo_label.bind("<Button-1>", lambda event: open_repo_link())

    center_window(custom_dialog)
    root.wait_window(custom_dialog)
    return confirm


def main():
    menu_bg = pg.image.load("assets/background1.png")
    screen.blit(menu_bg, (0,0))

    while True:
        MOUSE_POS = pg.mouse.get_pos()

        start = Button((370, 480), "Start Game", BLUE, LIGHT_GREEN)
        controls = Button((485, 480), " ? ", BLUE, LIGHT_GREEN)
       
        for button in [start, controls]:
            button.update_color(MOUSE_POS)
            start.draw_button(screen)
            controls.draw_button_transparent(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                if confirm_quit():
                    pg.quit()
                    sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if start.click_button(MOUSE_POS):
                    wumpus_world()

                if controls.click_button(MOUSE_POS):
                    description()

        pg.display.flip()


if __name__ == "__main__":
    main()