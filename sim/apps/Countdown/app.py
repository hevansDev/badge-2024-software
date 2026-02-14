import app
from events.input import Buttons, BUTTON_TYPES
import math

class EMFCountdownApp(app.App):
    def __init__(self):
        self.button_states = Buttons(self)
        # EMF 2026 starts July 16, 2026
        # Using a simple day counter approach
        self.emf_year = 2026
        self.emf_month = 7
        self.emf_day = 16
        
        # Try to sync time if WiFi is connected
        self._sync_time_if_connected()
        
    def _sync_time_if_connected(self):
        """Try to sync time via NTP if WiFi is connected"""
        try:
            import network
            import time
            wlan = network.WLAN(network.STA_IF)
            print("WiFi status:", wlan.isconnected())  # Debug
            if wlan.isconnected():
                import ntptime
                print("Syncing time...")  # Debug
                ntptime.settime()
                print("Time synced:", time.localtime())  # Debug
        except Exception as e:
            print("Time sync failed:", e)  # Debug - show the error
            pass
        
    def days_until_emf(self):
        """Calculate days until EMF 2026"""
        try:
            import time
            # Get current date
            current = time.localtime()
            current_year = current[0]
            current_month = current[1]
            current_day = current[2]
            
            # Simple day calculation
            # Days in each month
            days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            
            # Check for leap year
            def is_leap_year(year):
                return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
            
            # Calculate days remaining in current year
            days_left_current_year = 0
            if current_year < self.emf_year:
                # Days left in current month
                if is_leap_year(current_year):
                    days_in_month[1] = 29
                else:
                    days_in_month[1] = 28
                    
                days_left_current_year = days_in_month[current_month - 1] - current_day
                
                # Days in remaining months of current year
                for month in range(current_month, 12):
                    days_left_current_year += days_in_month[month]
            
            # Calculate days in full years between current and EMF year
            days_in_full_years = 0
            for year in range(current_year + 1, self.emf_year):
                if is_leap_year(year):
                    days_in_full_years += 366
                else:
                    days_in_full_years += 365
            
            # Calculate days from start of EMF year to event
            days_to_event = 0
            for month in range(0, self.emf_month - 1):
                if is_leap_year(self.emf_year):
                    days_in_month[1] = 29
                else:
                    days_in_month[1] = 28
                days_to_event += days_in_month[month]
            days_to_event += self.emf_day
            
            # If we're already in the EMF year
            if current_year == self.emf_year:
                # Calculate days from current date to EMF
                days_passed = 0
                for month in range(0, current_month - 1):
                    if is_leap_year(current_year):
                        days_in_month[1] = 29
                    else:
                        days_in_month[1] = 28
                    days_passed += days_in_month[month]
                days_passed += current_day
                
                total_days = days_to_event - days_passed
            else:
                # Total days until EMF
                total_days = days_left_current_year + days_in_full_years + days_to_event
            
            return max(0, total_days)
        except:
            # If time module fails, return a placeholder
            return 999

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

    def draw(self, ctx):
        ctx.save()
        
        # Green background
        ctx.rgb(0.0, 0.6, 0.0).rectangle(-120, -120, 240, 240).fill()
        
        # Set text alignment to center
        ctx.text_align = ctx.CENTER
        
        # Calculate days
        days = self.days_until_emf()
        
        # Draw "EMF 2026" title - white text, centered at x=0
        ctx.font_size = 30
        ctx.rgb(1, 1, 1).move_to(0, -30).text("EMF 2026")
        
        # Draw countdown number (large) - white text, centered at x=0
        ctx.font_size = 50
        ctx.rgb(1, 1, 1).move_to(0, 20).text(str(days))
        
        # Draw "days to go" label - white text, centered at x=0
        ctx.font_size = 20
        if days == 1:
            ctx.rgb(1, 1, 1).move_to(0, 60).text("day to go")
        else:
            ctx.rgb(1, 1, 1).move_to(0, 60).text("days to go")
        
        ctx.restore()

__app_export__ = EMFCountdownApp
