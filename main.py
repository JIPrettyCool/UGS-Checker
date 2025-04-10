import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import re

class UGSChecker:

    def __init__(self):
        self.regulations = {
            "06:00-13:29": {(1, 2): 13.0, 3: 12.5, 4: 12.0, 5: 11.5, 6: 11.0, 7: 10.5, 8: 10.0, 9: 9.5, 10: 9.0},
            "13:30-13:59": {(1, 2): 12.75, 3: 12.25, 4: 11.75, 5: 11.25, 6: 10.75, 7: 10.25, 8: 9.75, 9: 9.25, 10: 9.0},
            "14:00-14:29": {(1, 2): 12.5, 3: 12.0, 4: 11.5, 5: 11.0, 6: 10.5, 7: 10.0, 8: 9.5, 9: 9.0, 10: 9.0},
            "14:30-14:59": {(1, 2): 12.25, 3: 11.75, 4: 11.25, 5: 10.75, 6: 10.25, 7: 9.75, 8: 9.25, 9: 9.0, 10: 9.0},
            "15:00-15:29": {(1, 2): 12.0, 3: 11.5, 4: 11.0, 5: 10.5, 6: 10.0, 7: 9.5, 8: 9.0, 9: 9.0, 10: 9.0},
            "15:30-15:59": {(1, 2): 11.75, 3: 11.25, 4: 10.75, 5: 10.25, 6: 9.75, 7: 9.25, 8: 9.0, 9: 9.0, 10: 9.0},
            "16:00-16:29": {(1, 2): 11.5, 3: 11.0, 4: 10.5, 5: 10.0, 6: 9.5, 7: 9.0, 8: 9.0, 9: 9.0, 10: 9.0},
            "16:30-16:59": {(1, 2): 11.25, 3: 10.75, 4: 10.25, 5: 9.75, 6: 9.25, 7: 9.0, 8: 9.0, 9: 9.0, 10: 9.0},
            "17:00-04:59": {(1, 2): 11.0, 3: 10.5, 4: 10.0, 5: 9.5, 6: 9.0, 7: 9.0, 8: 9.0, 9: 9.0, 10: 9.0},
            "05:00-05:14": {(1, 2): 12.0, 3: 11.5, 4: 11.0, 5: 10.5, 6: 10.0, 7: 9.5, 8: 9.0, 9: 9.0, 10: 9.0},
            "05:15-05:29": {(1, 2): 12.25, 3: 11.75, 4: 11.25, 5: 10.75, 6: 10.25, 7: 9.75, 8: 9.25, 9: 9.0, 10: 9.0},
            "05:30-05:44": {(1, 2): 12.5, 3: 12.0, 4: 11.5, 5: 11.0, 6: 10.5, 7: 10.0, 8: 9.5, 9: 9.0, 10: 9.0},
            "05:45-05:59": {(1, 2): 12.75, 3: 12.25, 4: 11.75, 5: 11.25, 6: 10.75, 7: 10.25, 8: 9.25, 9: 9.25, 10: 9.0},
        }
    
    def parse_time(self, time_str):
        try:
            return datetime.strptime(time_str, "%H:%M").replace(
                year=datetime.now().year, 
                month=datetime.now().month, 
                day=datetime.now().day
            )
        except ValueError:
            return None
    
    def get_time_range_category(self, start_time):
        hour = start_time.hour
        minute = start_time.minute
        time_val = hour * 60 + minute
        if 360 <= time_val < 809:
            return "06:00-13:29"
        elif 810 <= time_val < 839:
            return "13:30-13:59"
        elif 840 <= time_val < 869:
            return "14:00-14:29"
        elif 870 <= time_val < 899:
            return "14:30-14:59"
        elif 900 <= time_val < 929:
            return "15:00-15:29"
        elif 930 <= time_val < 959:
            return "15:30-15:59"
        elif 960 <= time_val < 989:
            return "16:00-16:29"
        elif 990 <= time_val < 1019:
            return "16:30-16:59"
        elif 1020 <= time_val < 1799 or 0 <= time_val < 300:
            return "17:00-04:59"
        elif 300 <= time_val < 314:
            return "05:00-05:14"
        elif 315 <= time_val < 329:
            return "05:15-05:29"
        elif 330 <= time_val < 344:
            return "05:30-05:44"
        elif 345 <= time_val < 360:
            return "05:45-05:59"
        else:
            return "17:00-04:59"
    
    def get_max_duty_time(self, start_time, num_sectors, skpk_enabled=False):
        time_category = self.get_time_range_category(start_time)
        max_duty_time = 0
        if num_sectors <= 2:
            max_duty_time = self.regulations[time_category][(1, 2)]
        elif num_sectors <= 10:
            max_duty_time = self.regulations[time_category][num_sectors]
        else:
            max_duty_time = self.regulations[time_category][10]
        if skpk_enabled:
            max_duty_time += 2.0
            
        return max_duty_time
    
    def check_duty_time_compliance(self, duty_start, duty_end, num_sectors, skpk_enabled=False):
        start_time = self.parse_time(duty_start)
        end_time = self.parse_time(duty_end)
        if not start_time or not end_time:
            return False, "Geçersiz zaman formatı. SS:DD şeklinde giriniz."
        actual_duty_hours = (end_time - start_time).total_seconds() / 3600
        max_duty_hours = self.get_max_duty_time(start_time, num_sectors, skpk_enabled)
        if actual_duty_hours <= max_duty_hours:
            return True, f"✅ PLANLAMADA HATA YOK.\nGörev Zamanı: {self.decimal_to_hhmm(actual_duty_hours)}\nMaksimum izin verilen: {self.decimal_to_hhmm(max_duty_hours)}"
        else:
            excess = actual_duty_hours - max_duty_hours
            return False, f"❌ PLANLAMADA HATA VAR.\nGörev Zamanı: {self.decimal_to_hhmm(actual_duty_hours)}\nMaksimum izin verilen: {self.decimal_to_hhmm(max_duty_hours)}\nFazlalık: {self.decimal_to_hhmm(excess)}"
    
    def decimal_to_hhmm(self, decimal_hours):
        """Convert decimal hours (e.g., 11.67) to HH:MM format (e.g., 11:40)"""
        hours = int(decimal_hours)
        minutes = int((decimal_hours - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"

def validate_time_format(time_str):
    pattern = re.compile(r'^([01]?[0-9]|2[0-3]):([0-5][0-9])$')
    return bool(pattern.match(time_str))

def validate_sectors(sectors_str):
    try:
        sectors = int(sectors_str)
        return sectors > 0
    except ValueError:
        return False

def main():
    root = tk.Tk()
    root.title("UGS Hesaplayıcı v0.0.1")
    root.geometry("700x800")
    
    checker = UGSChecker()
    
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    tk.Label(main_frame, text="Görev Başlayış Zamanı (SS:DD):", anchor="w").pack(fill=tk.X, pady=(0, 5))
    start_entry = tk.Entry(main_frame)
    start_entry.pack(fill=tk.X, pady=(0, 10))
    
    tk.Label(main_frame, text="Görev Bitiş Zamanı (SS:DD):", anchor="w").pack(fill=tk.X, pady=(0, 5))
    end_entry = tk.Entry(main_frame)
    end_entry.pack(fill=tk.X, pady=(0, 10))
    
    tk.Label(main_frame, text="Sektör Sayısı:", anchor="w").pack(fill=tk.X, pady=(0, 5))
    sectors_entry = tk.Entry(main_frame)
    sectors_entry.pack(fill=tk.X, pady=(0, 15))
    sectors_entry.insert(0, "2")
    
    options_frame = tk.LabelFrame(main_frame, text="Seçenekler", padx=10, pady=10)
    options_frame.pack(fill=tk.X, pady=(0, 15))
    
    skpk_var = tk.BooleanVar()
    skpk_check = tk.Checkbutton(options_frame, text="SKPK ile +2 saat izin", variable=skpk_var)
    skpk_check.pack(anchor=tk.W)
    
    example_frame = tk.LabelFrame(main_frame, text="Nasıl Kullanılır?", padx=10, pady=10)
    example_frame.pack(fill=tk.X, pady=(0, 15))
    
    example_text = (
        "• Kalkış: 06:30, İniş: 19:30, Sektör: 2\n"
        "• Kalkış: 14:15, İniş: 01:45, Sektör: 4\n"
        "• Kalkış: 22:00, İniş: 06:00, Sektör: 6"
    )
    tk.Label(example_frame, text=example_text, justify=tk.LEFT).pack(anchor=tk.W)
    
    def check_compliance():
        start_time = start_entry.get().strip()
        end_time = end_entry.get().strip()
        sectors_str = sectors_entry.get().strip()
        skpk_enabled = skpk_var.get()
        
        if not validate_time_format(start_time):
            messagebox.showerror("Error", "Yanlış saat formatı. SS:DD şeklinde giriniz.")
            return
        
        if not validate_time_format(end_time):
            messagebox.showerror("Error", "Yanlış saat formatı. SS:DD şeklinde giriniz.")
            return
        
        if not validate_sectors(sectors_str):
            messagebox.showerror("Error", "Sektör sayısı hatalı.")
            return
        
        result_text.delete(1.0, tk.END)
        
        num_sectors = int(sectors_str)
        message = checker.check_duty_time_compliance(start_time, end_time, num_sectors, skpk_enabled)
        
        adjusted_start_time = checker.parse_time(start_time)
            
        time_category = checker.get_time_range_category(adjusted_start_time)
        
        options_info = ""
        if skpk_enabled:
            options_info += "• SKPK +2 saat izni kullanıldı\n"
        if options_info:
            options_info = "Uygulanan Ayarlar:\n" + options_info + "\n"
            
        result_text.insert(tk.END, f"SAAT Kategorisi: {time_category}\n")
        result_text.insert(tk.END, f"Sektör Sayısı: {num_sectors}\n")
        if options_info:
            result_text.insert(tk.END, options_info)
        result_text.insert(tk.END, message)
    
    check_button = tk.Button(main_frame, text="UGS Uyuyor mu?", command=check_compliance, 
                           bg="#4CAF50", fg="white", padx=10, pady=5)
    check_button.pack(pady=15)
    
    tk.Label(main_frame, text="Sonuç:", anchor="w").pack(fill=tk.X)
    
    result_frame = tk.Frame(main_frame)
    result_frame.pack(fill=tk.BOTH, expand=True)
    
    result_text = tk.Text(result_frame, wrap=tk.WORD, height=10)
    result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    scrollbar = tk.Scrollbar(result_frame, command=result_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    result_text.config(yscrollcommand=scrollbar.set)
    
    info_text = "UGS Hesaplayıcı - Meriç."
    tk.Label(main_frame, text=info_text, fg="gray").pack(pady=(10, 0))
    
    root.mainloop()

if __name__ == "__main__":
    main()