import datetime
import json

def load_highscore():
    try:
        max_lvl = 1
        with open("../highscore.txt", "r") as f:
            for line in f:
                if "Level:" in line:
                    try:
                        # Čitamo broj odmah posle "Level: "
                        lvl_str = line.split("Level:")[1].split("-")[0].strip()
                        lvl = int(lvl_str)
                        if lvl > max_lvl: max_lvl = lvl
                    except:
                        continue
        return max_lvl
    except FileNotFoundError:
        return 1


def save_highscore(info, status="DEAD"):
    try:
        now = datetime.datetime.now()
        date_string = now.strftime("%d.%m.%Y %I:%M %p")
        with open("../highscore.txt", "a") as f:
            # Format: Level: 5 - Date: 03.03.2026 10:30 AM - DEAD
            f.write(f"Level: {info} - Date: {date_string} - {status}\n")
    except OSError as e:
        print(f"Greška pri čuvanju: {e}")


def get_score_history():
    try:
        with open("../highscore.txt", "r") as f:
            lines = f.readlines()
            return [line.strip() for line in lines[-7:][::-1]]
    except FileNotFoundError:
        return ["No records yet!"]


def load_best_times():
    try:
        with open("../best_times.json", "r") as f:
            # Učitavamo rečnik npr. {"1": 45, "2": 38}
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_if_best(level, current_seconds):
    best_times = load_best_times()
    level_str = str(level)

    # Ako nivo ne postoji ili je trenutno vreme bolje (manje) od starog
    if level_str not in best_times or current_seconds < best_times[level_str]:
        best_times[level_str] = current_seconds
        with open("../best_times.json", "w") as f:
            json.dump(best_times, f)
        return True  # Vratio je True jer je postavljen novi rekord
    return False  # Nije rekord