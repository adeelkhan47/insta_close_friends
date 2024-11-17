import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from model import Website
from tasks.celery import DbTask, celery_app
import helpers.scrapers as scrapers

# Set the application start time when the app starts
app_time_when_started = datetime.now()

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__file__)

# Create a ThreadPoolExecutor to manage threads
executor = ThreadPoolExecutor(max_workers=10)  # Adjust max_workers as needed

@celery_app.task(bind=True, base=DbTask)
def process_new(self, *args, **kwargs):
    session = self.session

    # Get the current time when the task runs
    current_time = datetime.now()
    print(f"Current {current_time} ===  Started Time {app_time_when_started}")

    # Query active websites with website_status = True
    websites = session.query(Website).filter(Website.website_status == True).all()

    for each in websites:
        if each.scraper_scheduler:
            run_frequency = each.scraper_scheduler[0].every_hour  # Get the scraper's run frequency

            # Calculate the time difference in seconds
            time_diff_seconds = (current_time - app_time_when_started).total_seconds()

            # Check if the time difference modulo run_frequency is zero
            # if time_diff_seconds % (run_frequency * 3600) == 0:
            if int(time_diff_seconds % (run_frequency * 1)) == 0:
                print(f"Running scraper for website: {each.web_name}")

                # Dynamically call the scraper function based on the website.scraper_name
                scraper_function_name = each.scraper_name
                try:
                    # Get the function from the scrapers module by name
                    scraper_function = getattr(scrapers, scraper_function_name)

                    # Submit the scraper function to run in the background thread
                    executor.submit(scraper_function)

                except AttributeError:
                    logger.error(f"Scraper function '{scraper_function_name}' not found.")
            else:
                print(f"Skipping scraper for website: {each.web_name}")
