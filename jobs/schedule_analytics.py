"""Trigger a reset every day at the same time using the schedule library"""
import schedule
import time
import requests
import threading

def run_continuously():
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                interval = schedule.idle_seconds()
                if interval is None:
                    # no more jobs
                    break
                elif interval > 0:
                    # sleep exactly the right amount of time
                    print(f"Time till Analytics reset: {interval} seconds")
                    time.sleep(interval)
                schedule.run_pending()

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def analytics_job():
    """trigger at set time"""
    response = requests.get("https://spitfire-interractions.onrender.com/api/analytics")
    print(response.text)

# at 12:01am everyday
schedule.every().day.at("00:01").do(analytics_job)


stop_run_continuously = run_continuously()
if __name__ == "__main__":
    time.sleep(60)
    # Stop the background thread
    stop_run_continuously.set()