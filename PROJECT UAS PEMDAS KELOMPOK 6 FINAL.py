import tkinter as tk
import random
import os
import time

try:
    import winsound
except Exception:
    winsound = None

W, H = 420, 650


class RealisticClawApp:
    def __init__(self, root):
        self.root = root
        root.title("Claw Machine - Realistic (Final)")
        root.geometry(f"{W}x{H}")
        root.resizable(False, False)

        # state
        self.player_name = ""   # <<< TAMBAHAN
        self.prize_type = ""
        self.coin_count_choice = 1
        self.coins_left_to_insert = 0
        self.coin_items = []
        self.prizes_collected = []

        self.claw_busy = False
        self.attached = None
        self.toys = []
        self.use_image = False
        self.toy_photo = None

        self.machine_lamps = []
        self.lamp_blinking = False
        self.lamp_speed_ms = 200

        if os.path.exists("toy.png"):
            try:
                self.toy_photo = tk.PhotoImage(file="toy.png")
                self.use_image = True
            except:
                self.use_image = False

        # START DARI INPUT NAMA
        self.build_name_input_screen()

    # Helper untuk play sound (support alias atau custom beep)
    def play_sound(self, alias=None, freq=None, dur=None):
        if winsound:
            try:
                if alias:
                    winsound.PlaySound(alias, winsound.SND_ALIAS | winsound.SND_ASYNC)
                elif freq is not None and dur is not None:
                    winsound.Beep(freq, dur)
            except:
                pass

    # ========================== NAME INPUT SCREEN ==============================
    def build_name_input_screen(self):
        self.clear_root()

        canvas = tk.Canvas(self.root, width=W, height=H, bg="#ffeef3", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        canvas.create_rectangle(40, 60, W-40, 140,
                                fill="#ff4fa5", outline="#b0005d", width=4)
        canvas.create_text(W//2, 100, text="SELAMAT DATANG",
                           font=("Cooper Black", 22), fill="white")

        canvas.create_text(W//2, 210,
                           text="Masukkan Nama Kamu",
                           font=("Arial", 13, "bold"),
                           fill="#7a0b5a")

        name_entry = tk.Entry(self.root, font=("Arial", 14), justify="center")
        canvas.create_window(W//2, 250, window=name_entry, width=220)

        def lanjut():
            self.player_name = name_entry.get().strip()
            if not self.player_name:
                self.player_name = "Pemain"
            self.build_selection_screen()

        btn = tk.Button(self.root, text="Mulai",
                        font=("Arial", 13, "bold"),
                        bg="#ff73c7", fg="white",
                        activebackground="#ff4fa5",
                        width=12, command=lanjut)
        canvas.create_window(W//2, 310, window=btn)

        canvas.create_text(W//2, 370,
                           text="Semoga beruntung 🍀",
                           font=("Arial", 10, "italic"),
                           fill="#7a0b5a")

    # ========================== SELECTION SCREEN ==============================
    def build_selection_screen(self):
        self.clear_root()

        self.sel_canvas = tk.Canvas(self.root, width=W, height=H, bg="#ffeef3", highlightthickness=0)
        self.sel_canvas.pack(fill="both", expand=True)

        self.sel_canvas.create_rectangle(40, 20, W-40, 90,
                                         fill="#ff4fa5", outline="#b0005d", width=4)
        self.sel_canvas.create_text(
            W//2, 55,
            text=f"Halo, {self.player_name}!",
            font=("Cooper Black", 20),
            fill="white"
        )

        self.sel_canvas.create_text(W//2, 130,
                                    text="Pilih hadiah yang ingin kamu coba capit:",
                                    font=("Arial", 12, "bold"), fill="#7a0b5a")

        def make_btn(y, label):
            b = tk.Button(self.root, text=label, font=("Arial", 13, "bold"),
                          bg="#ff73c7", fg="white", activebackground="#ff4fa5",
                          width=18, height=1, command=lambda: self._select_and_go_coin(label))
            self.sel_canvas.create_window(W//2, y, window=b)

        make_btn(190, "Boneka")
        make_btn(250, "Bola")
        make_btn(310, "Coklat")
        make_btn(370, "Permen")

        self.sel_choice_label = self.sel_canvas.create_text(
            W//2, 430, text="Terpilih: -", font=("Arial", 11, "italic"), fill="#7a0b5a")

        self.sel_canvas.create_text(
            W//2, 480,
            text="1. Nadhila Alya (25031554051)\n2. Laurensia Fernanda (25031554055)\n3. Nita Amalia (25031554196)",
            font=("Arial", 10, "bold"), fill="#7a0b5a"
        )

        tk.Button(self.root, text="Keluar", command=self.root.destroy).place(x=W-60, y=H-30)

        self.sel_lamps = []
        for x in range(50, W-50, 25):
            lamp = self.sel_canvas.create_oval(x, 100, x+15, 115, fill="#fffa8b", outline="")
            self.sel_lamps.append(lamp)
        self._blink_selection_lights()

    def _blink_selection_lights(self):
        colors = ["#fffa8b", "#ffd1e8", "#ff9beb", "#7efcff"]
        for lamp in self.sel_lamps:
            self.sel_canvas.itemconfig(lamp, fill=random.choice(colors))
        self.root.after(350, self._blink_selection_lights)

    def _select_and_go_coin(self, label):
        self.prize_type = label
        self.sel_canvas.itemconfig(self.sel_choice_label, text=f"Terpilih: {label}")
        self.root.after(450, self.build_coin_screen)

    # ========================== COIN SCREEN ==============================
    def build_coin_screen(self):
        self.clear_root()

        self.frame = tk.Frame(self.root, bg="#fff4f8")
        self.frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame, width=W, height=H, bg="#fff4f8", highlightthickness=0)
        self.canvas.pack()

        stripes = ["#ffdede", "#fff2cc", "#dceeff", "#f8eafd"]
        for y in range(0, H, 30):
            self.canvas.create_rectangle(0, y, W, y+30, fill=stripes[(y//30) % 4], outline="")

        self.canvas.create_text(W//2, 38, text="MESIN CLAW", font=("Cooper Black", 24), fill="#8a2be2")
        self.canvas.create_text(W//2, 70, text=f"Hadiah terpilih: {self.prize_type}", font=("Arial", 10))

        self.slot_left, self.slot_top = 90, 150
        self.slot_right, self.slot_bottom = 330, 360

        self.canvas.create_rectangle(self.slot_left, self.slot_top, self.slot_right, self.slot_bottom,
                                     fill="#ffd54f", outline="#b8860b", width=4)
        self.canvas.create_oval(self.slot_left+20, self.slot_top+20, self.slot_right-20, self.slot_top+120,
                                fill="#fff9d6", outline="#d4a017")
        self.canvas.create_rectangle(self.slot_left+60, self.slot_top+160, self.slot_right-60, self.slot_bottom-30,
                                     fill="#222")

        self.canvas.create_text((self.slot_left+self.slot_right)//2, self.slot_bottom+18,
                                text="MASUKKAN KOIN", font=("Arial", 12, "bold"))

        tk.Label(self.frame, text="Pilih jumlah koin (1-3):", bg="#fff4f8").place(x=30, y=450)
        tk.Button(self.frame, text="1 Koin", command=lambda: self._generate_coins(1)).place(x=180, y=445)
        tk.Button(self.frame, text="2 Koin", command=lambda: self._generate_coins(2)).place(x=240, y=445)
        tk.Button(self.frame, text="3 Koin", command=lambda: self._generate_coins(3)).place(x=300, y=445)

        self.coin_info_lbl = tk.Label(self.frame, text="Masukkan koin ke slot, lalu permainan akan dimulai.",
                                      font=("Arial", 10), bg="#fff4f8")
        self.coin_info_lbl.place(x=40, y=480)

        self.coin_items = []
        self.coins_left_to_insert = 0

        # default generate 1 coin
        self._generate_coins(1)

    def _generate_coins(self, n):
        for oval, txt in self.coin_items:
            try:
                self.canvas.delete(oval)
                self.canvas.delete(txt)
            except:
                pass
        self.coin_items.clear()

        self.coin_count_choice = max(1, min(3, n))
        self.coins_left_to_insert = self.coin_count_choice

        start_x = 40
        y = 520
        spacing = 70
        for i in range(self.coin_count_choice):
            cx = start_x + i * spacing
            oval = self.canvas.create_oval(cx, y, cx+48, y+48, fill="#ffd54f", outline="#d4a017", width=3)
            txt = self.canvas.create_text(cx+24, y+24, text=str(i+1), font=("Arial", 12, "bold"))
            self.coin_items.append((oval, txt))
            for tag in (oval, txt):
                self.canvas.tag_bind(tag, "<ButtonPress-1>", self.on_coin_press)
                self.canvas.tag_bind(tag, "<B1-Motion>", self.on_coin_motion)
                self.canvas.tag_bind(tag, "<ButtonRelease-1>", self.on_coin_release)
        self._update_coin_info()

    def _update_coin_info(self):
        self.coin_info_lbl.config(text=f"Koin tersisa untuk dimasukkan: {self.coins_left_to_insert}")

    def on_coin_press(self, event):
        item = self.canvas.find_withtag("current")
        if not item:
            return
        item = item[0]
        for oval, txt in self.coin_items:
            if item in (oval, txt):
                self.drag_active = (oval, txt)
                self.drag_start_x = event.x
                self.drag_start_y = event.y
                return
        self.drag_active = None 

    def on_coin_motion(self, event):
        if not getattr(self, "drag_active", None):
            return
        oval, txt = self.drag_active
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        self.canvas.move(oval, dx, dy)
        self.canvas.move(txt, dx, dy)
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        if self._is_item_over_slot(oval):
            if not self.canvas.find_withtag("slot_highlight"):
                self.canvas.create_rectangle(self.slot_left+2, self.slot_top+2, self.slot_right-2, self.slot_bottom-2,
                                             outline="#ff9a9a", width=3, tags=("slot_highlight",))
        else:
            self.canvas.delete("slot_highlight")

    def on_coin_release(self, event):
        if not getattr(self, "drag_active", None):
            return
        oval, txt = self.drag_active
        if self._is_item_over_slot(oval):
            self.canvas.delete("slot_highlight")
            self._animate_coin_into_slot(oval, txt)
        self.drag_active = None

    def _is_item_over_slot(self, item):
        coords = self.canvas.coords(item)
        if not coords:
            return False
        cx = (coords[0] + coords[2]) / 2
        cy = (coords[1] + coords[3]) / 2
        return (self.slot_left+10 < cx < self.slot_right-10 and self.slot_top+10 < cy < self.slot_bottom-10)

    def _animate_coin_into_slot(self, oval, txt):
        target_x = (self.slot_left + self.slot_right) / 2 - 24
        target_y = self.slot_top + 30
        def step():
            coords = self.canvas.coords(oval)
            if not coords:
                return
            cx = (coords[0] + coords[2]) / 2
            cy = (coords[1] + coords[3]) / 2
            dx = (target_x + 24 - cx) * 0.25
            dy = (target_y + 24 - cy) * 0.25
            if abs(dx) < 1 and abs(dy) < 1:
                self._shrink_and_remove_coin(oval, txt)
            else:
                self.canvas.move(oval, dx, dy)
                self.canvas.move(txt, dx, dy)
                self.root.after(20, step)
        step()

    def _shrink_and_remove_coin(self, oval, txt):
        def s():
            coords = self.canvas.coords(oval)
            if coords and coords[2]-coords[0] > 6:
                self.canvas.coords(oval, coords[0]+2, coords[1]+2, coords[2]-2, coords[3]-2)
                self.canvas.coords(txt, (coords[0]+coords[2])/2, (coords[1]+coords[3])/2)
                self.root.after(35, s)
            else:
                try:
                    self.canvas.delete(oval)
                    self.canvas.delete(txt)
                except:
                    pass
                for c in list(self.coin_items):
                    if c[0] == oval:
                        self.coin_items.remove(c)
                        break
                self.coins_left_to_insert -= 1
                self._update_coin_info()
                # <<< SOUND KOIN MASUK REALISTIS: Cling tinggi + clang rendah >>>
                self.play_sound(freq=1200, dur=100)  # Cling masuk slot
                self.root.after(150, lambda: self.play_sound(freq=800, dur=200))  # Clang jatuh dalam mesin

                if self.coins_left_to_insert == 0:
                    self.plays_remaining = self.coin_count_choice
                    self.root.after(300, self.play_welcome_animation)
        s()

    # welcome typing
    def play_welcome_animation(self):
        self.clear_root()
        frame = tk.Frame(self.root, bg="#111827")
        frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(frame, width=W, height=H, bg="#111827", highlightthickness=0)
        canvas.pack()
        text = "SELAMAT BERMAIN!"
        label = canvas.create_text(W//2, H//2, text="", font=("Cooper Black", 28), fill="#ffd54f")
        self._type_idx = 0
        self._type_msg = text
        self._type_canvas = canvas
        self._type_label = label
        self._typing_step()

    def _typing_step(self):
        if self._type_idx < len(self._type_msg):
            cur = self._type_canvas.itemcget(self._type_label, "text")
            cur += self._type_msg[self._type_idx]
            self._type_canvas.itemconfig(self._type_label, text=cur)
            self._type_idx += 1
            self.root.after(90, self._typing_step)
        else:
            self.root.after(600, self.play_one)

    def play_one(self):
        if getattr(self, "plays_remaining", 0) <= 0:
            self.root.after(600, self.show_prize_screen)
            return
        self.plays_remaining -= 1
        self.build_game_screen()

    def build_game_screen(self):
        self.clear_root()
        self.frame_game = tk.Frame(self.root, bg="#f7fbff")
        self.frame_game.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(self.frame_game, width=W, height=H, bg="#f7fbff", highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_rectangle(20, 20, W-20, H-20, outline="#7c3aed", width=6, fill="#fff5fb")
        self.left, self.top, self.right, self.bottom = 70, 90, 350, 520
        self.canvas.create_rectangle(self.left, self.top, self.right, self.bottom,
                                     outline="#2b2b2b", width=3, fill="#ddf6ff")
        self.machine_lamps = []
        lamp_positions = []
        for x in range(self.left+10, self.right-10, 24):
            lamp_positions.append((x, self.top-18, x+12, self.top-6))
        for y in range(self.top+6, self.bottom-6, 24):
            lamp_positions.append((self.left-18, y, self.left-6, y+12))
        for y in range(self.top+6, self.bottom-6, 24):
            lamp_positions.append((self.right+6, y, self.right+18, y+12))
        for x1, y1, x2, y2 in lamp_positions:
            lamp = self.canvas.create_oval(x1, y1, x2, y2, fill="#ffd1e8", outline="")
            self.machine_lamps.append(lamp)
        self.lamp_blinking = True
        self._blink_game_lamps()
        chute_w = 100
        self.chute_x = (self.left + self.right) // 2
        self.canvas.create_rectangle(self.chute_x-chute_w//2, self.bottom+5, self.chute_x+chute_w//2,
                                     self.bottom+40, fill="#ffe8b0", outline="#b37b00")
        self.canvas.create_text(self.chute_x, self.bottom+50, text="PRIZE", font=("Arial", 9))
        self.status_text = self.canvas.create_text(W//2, H-10, text="Gerakkan capit, lalu tekan GRAB",
                                                   font=("Arial", 9), fill="#333")
        self.claw_x = (self.left + self.right) // 2
        self.claw_top_y = self.top + 20
        self.claw_y = self.claw_top_y
        self.jaw_open = True
        self.jaw_w = 22
        self.draw_claw()
        self.toys = []
        self.spawn_prizes(8)
        tk.Button(self.frame_game, text="◀ LEFT", font=("Arial", 12, "bold"), width=10,
                  command=self.move_left).place(x=25, y=580)
        tk.Button(self.frame_game, text="RIGHT ▶", font=("Arial", 12, "bold"), width=10,
                  command=self.move_right).place(x=145, y=580)
        tk.Button(self.frame_game, text="GRAB ▼", font=("Arial", 12, "bold"), width=10,
                  bg="#ff6f00", fg="white", command=self.start_drop).place(x=265, y=580)

    def _blink_game_lamps(self):
        if not self.lamp_blinking:
            return
        colors = ["#ff3b3b", "#ffd60a", "#7efcff", "#ff7ab6", "#a78bfa", "#8aff8a"]
        for lamp in self.machine_lamps:
            try:
                self.canvas.itemconfig(lamp, fill=random.choice(colors))
            except:
                pass
        self.root.after(self.lamp_speed_ms, self._blink_game_lamps)

    def draw_claw(self):
        for attr in ("jaw_l", "jaw_r", "rope"):
            if hasattr(self, attr):
                try:
                    self.canvas.delete(getattr(self, attr))
                except:
                    pass
        gap = 6 if self.jaw_open else 0
        self.rope = self.canvas.create_line(self.claw_x, 40, self.claw_x, self.claw_y-8, width=4, fill="#444")
        left_poly = (self.claw_x-gap-self.jaw_w, self.claw_y, self.claw_x-gap, self.claw_y-8, self.claw_x-gap+8, self.claw_y)
        right_poly = (self.claw_x+gap+self.jaw_w, self.claw_y, self.claw_x+gap, self.claw_y-8, self.claw_x+gap-8, self.claw_y)
        self.jaw_l = self.canvas.create_polygon(left_poly, fill="#c0c0c0", outline="#444")
        self.jaw_r = self.canvas.create_polygon(right_poly, fill="#c0c0c0", outline="#444")

    def spawn_prizes(self, n):
        for _ in range(n):
            tx = random.randint(self.left+30, self.right-30)
            ty = random.randint(self.top+140, self.bottom-120)
            color = random.choice(["#ff9aa2", "#ffd6a5", "#cfe8ff", "#d4f7d6"])
            if self.prize_type == "Bola":
                r = random.randint(12, 24)
                parts = [self.canvas.create_oval(tx-r, ty-r, tx+r, ty+r, fill=color, outline="#333")]
            elif self.prize_type == "Coklat":
                w = random.randint(28, 40); h = random.randint(18, 28)
                parts = [self.canvas.create_rectangle(tx-w//2, ty-h//2, tx+w//2, ty+h//2, fill="#8b5a2b", outline="#3b2f2f")]
            elif self.prize_type == "Permen":
                w = random.randint(28, 40); h = random.randint(16, 24)
                body = self.canvas.create_rectangle(tx-w//2, ty-h//2, tx+w//2, ty+h//2, fill=color, outline="#333")
                l = self.canvas.create_polygon(tx-w//2-6, ty, tx-w//2+2, ty-h//2, tx-w//2+2, ty+h//2, fill=color)
                r = self.canvas.create_polygon(tx+w//2+6, ty, tx+w//2-2, ty-h//2, tx+w//2-2, ty+h//2, fill=color)
                parts = [body, l, r]
            else:
                r = 20
                head = self.canvas.create_oval(tx-r, ty-r, tx+r, ty+r, fill=color, outline="#333")
                e1 = self.canvas.create_oval(tx-8, ty-8, tx-4, ty-4, fill="black")
                e2 = self.canvas.create_oval(tx+4, ty-8, tx+8, ty-4, fill="black")
                mouth = self.canvas.create_arc(tx-8, ty+2, tx+8, ty+14, start=0, extent=-180, style="arc", width=2)
                parts = [head, e1, e2, mouth]
            self.toys.append({"id": parts[0], "parts": parts, "color": color})

    def move_left(self):
        if self.claw_busy: return
        if self.claw_x - 20 >= self.left + 30:
            self.claw_x -= 20; self.draw_claw()

    def move_right(self):
        if self.claw_busy: return
        if self.claw_x + 20 <= self.right - 30:
            self.claw_x += 20; self.draw_claw()

    def start_drop(self):
        if self.claw_busy: return
        self.claw_busy = True
        self.jaw_open = True
        self.draw_claw()
        self._drop_step()

    def _drop_step(self):
        bottom_limit = self.bottom - 80
        closest, closest_dist = None, float("inf")
        for toy in self.toys:
            coords = self.canvas.coords(toy["id"])
            if not coords:
                continue
            if len(coords) >= 4:
                tx = (coords[0]+coords[2])/2; ty = (coords[1]+coords[3])/2
            else:
                tx, ty = coords[0], coords[1]
            if ty >= self.claw_y:
                dist = ty - self.claw_y
                if dist < closest_dist:
                    closest_dist = dist; closest = (toy, tx, ty)
        if closest and closest_dist <= 28:
            toy, tx, ty = closest
            self.claw_y += max(0, closest_dist - 4)
            self.draw_claw(); self.jaw_open = False; self.draw_claw()
            self.play_sound(alias="SystemExclamation")
            self.root.after(120, self._realistic_check_and_raise)
            return
        if self.claw_y < bottom_limit:
            self.claw_y += 8; self.draw_claw(); self.root.after(20, self._drop_step)
        else:
            self.jaw_open = False; self.draw_claw()
            self.play_sound(alias="SystemExclamation")
            self.root.after(120, self._realistic_check_and_raise)

    def _realistic_check_and_raise(self):
        grabbed = None
        jaw_left = self.claw_x - (self.jaw_w - 6)
        jaw_right = self.claw_x + (self.jaw_w - 6)
        for toy in list(self.toys):
            coords = self.canvas.coords(toy["id"])
            if not coords: continue
            if len(coords) >= 4:
                tx = (coords[0]+coords[2])/2; ty = (coords[1]+coords[3])/2
            else:
                tx, ty = coords[0], coords[1]
            if jaw_left-36 < tx < jaw_right+36 and abs(ty - self.claw_y) <= 34:
                grabbed = toy; break
        if grabbed:
            self.attached = grabbed
            try:
                self.toys.remove(grabbed)
            except:
                pass
            coords = self.canvas.coords(grabbed["id"])
            if len(coords) >= 4:
                cx = (coords[0]+coords[2])/2; cy = (coords[1]+coords[3])/2
            else:
                cx, cy = coords[0], coords[1]
            dx = self.claw_x - cx; dy = (self.claw_y + 12) - cy
            for p in grabbed["parts"]:
                self.canvas.move(p, dx, dy)
            self.play_sound(alias="SystemAsterisk")  # Success grab
        else:
            self.attached = None
        self.root.after(80, self._raise_step)

    def _raise_step(self):
        if self.claw_y > self.claw_top_y:
            self.claw_y -= 10
            if self.attached:
                for p in self.attached["parts"]:
                    try:
                        self.canvas.move(p, 0, -10)
                    except:
                        pass
            self.draw_claw()
            self.root.after(25, self._raise_step)
        else:
            if self.attached:
                self._exit_attached(self.attached)
            else:
                self.jaw_open = True
                self.draw_claw()
                self.claw_busy = False
                if getattr(self, "plays_remaining", 0) > 0:
                    self.root.after(800, self.play_one)
                else:
                    self.root.after(800, self.show_prize_screen)

    def _exit_attached(self, toy):
        chute_cx = self.chute_x
        chute_top = self.bottom + 10

        def move_to_center():
            coords = self.canvas.coords(toy["id"])
            if not coords:
                drop_into_chute()
                return
            if len(coords) >= 4:
                cx = (coords[0]+coords[2])/2; cy = (coords[1]+coords[3])/2
            else:
                cx, cy = coords[0], coords[1]
            dx = (chute_cx - cx) * 0.15
            dy = (chute_top - cy) * 0.15
            for p in toy["parts"]:
                self.canvas.move(p, dx, dy)
            if abs(cx - chute_cx) > 3 or abs(cy - chute_top) > 3:
                self.root.after(20, move_to_center)
            else:
                drop_into_chute()

        def drop_into_chute():
            def step():
                for p in toy["parts"]:
                    self.canvas.move(p, 0, 18)
                coords2 = self.canvas.coords(toy["id"])
                if not coords2:
                    finish()
                    return
                ty2 = coords2[3] if len(coords2) >= 4 else coords2[1]
                if ty2 < H + 60:
                    self.root.after(28, step)
                else:
                    finish()
            step()

        def finish():
            color = toy.get("color", "#ff9aa2")
            self.prizes_collected.append({"type": self.prize_type, "color": color})
            for p in toy["parts"]:
                try:
                    self.canvas.delete(p)
                except:
                    pass
            self.attached = None
            self.jaw_open = True
            self.draw_claw()
            self.claw_busy = False
            if getattr(self, "plays_remaining", 0) > 0:
                self.root.after(600, self.play_one)
            else:
                self.root.after(600, self.show_prize_screen)
        move_to_center()

    def _firework_once(self, canvas):
        colors = ["#ff3b3b", "#ffed4a", "#4af0ff", "#ff7af6", "#8aff8a", "#ffd1e8"]
        x = random.randint(40, W-40)
        y = random.randint(80, H-120)
        rings = []
        for r in (6, 12, 20, 30):
            col = random.choice(colors)
            o = canvas.create_oval(x-r, y-r, x+r, y+r, outline=col, width=2)
            rings.append(o)
        def fade(step=0):
            if step < 6:
                for o in rings:
                    try: canvas.delete(o)
                    except: pass
                new_rings = []
                for r in (int(6 - step), int(12-step*1.5), int(20-step*2), int(30-step*3)):
                    if r > 0:
                        col = random.choice(colors)
                        o = canvas.create_oval(x-r, y-r, x+r, y+r, outline=col, width=2)
                        new_rings.append(o)
                rings[:] = new_rings
                self.root.after(80, lambda: fade(step+1))
            else:
                for o in rings:
                    try: canvas.delete(o)
                    except: pass
        self.root.after(50, fade)

    def show_prize_screen(self):
        # <<< SOUND MERIAH AKHIR: Fanfare victory cheerful panjang >>>
        self.play_sound(freq=600, dur=150)
        self.root.after(200, lambda: self.play_sound(freq=800, dur=150))
        self.root.after(400, lambda: self.play_sound(freq=1000, dur=150))
        self.root.after(600, lambda: self.play_sound(freq=1200, dur=200))
        self.root.after(850, lambda: self.play_sound(freq=1400, dur=150))
        self.root.after(1100, lambda: self.play_sound(freq=1600, dur=300))  # Chime akhir panjang
        self.root.after(1500, lambda: self.play_sound(alias="SystemAsterisk"))  # Bonus win chime

        win = tk.Toplevel(self.root)
        win.title("SELAMAT!")
        win.geometry(f"{W}x{H}")
        win.resizable(False, False)
        c = tk.Canvas(win, width=W, height=H, bg="#111827")
        c.pack()

        c.create_text(W//2, 60, text="SELAMAT!", font=("Cooper Black", 34), fill="#ffd54f")
        jumlah = len(self.prizes_collected)
        c.create_text(W//2, 110, text=f"Kamu Mendapatkan {jumlah} hadiah:",
                      font=("Arial", 12), fill="white")

        start_y = 160
        gap = 120
        for i, p in enumerate(self.prizes_collected):
            cx, cy = W//2, start_y + i*gap
            if p["type"] == "Bola":
                r = 36; c.create_oval(cx-r, cy-r, cx+r, cy+r, fill=p["color"], outline="#333")
            elif p["type"] == "Coklat":
                c.create_rectangle(cx-60, cy-20, cx+60, cy+20, fill="#8b5a2b", outline="#3b2f2f")
            elif p["type"] == "Permen":
                c.create_rectangle(cx-60, cy-16, cx+60, cy+16, fill=p["color"], outline="#333")
            else:
                c.create_oval(cx-48, cy-48, cx+48, cy+48, fill=p["color"], outline="#333")
                c.create_oval(cx-24, cy-16, cx-12, cy-4, fill="black")
                c.create_oval(cx+12, cy-16, cx+24, cy-4, fill="black")
                c.create_arc(cx-24, cy+8, cx+24, cy+40, start=0, extent=-180, style="arc", width=3)

        def loop_fireworks():
            self._firework_once(c)
            c.after(600, loop_fireworks)
        loop_fireworks()

        tk.Button(win, text="Main Lagi", font=("Arial", 12, "bold"),
                  command=lambda: [win.destroy(), self.prizes_collected.clear(), self.build_selection_screen()]).place(x=60, y=560)
        tk.Button(win, text="Tutup", font=("Arial", 12), command=win.destroy).place(x=300, y=560)

    def clear_root(self):
        self.lamp_blinking = False
        for w in self.root.winfo_children():
            try:
                w.destroy()
            except:
                pass


if __name__ == "__main__":
    root = tk.Tk()
    app = RealisticClawApp(root)
    root.mainloop()