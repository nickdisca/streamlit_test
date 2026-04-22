import pathlib
from bs4 import BeautifulSoup
import logging
import shutil
import argparse

# Inject GA in the index file 
# Adapted from https://discuss.streamlit.io/t/how-to-add-google-analytics-or-js-code-in-a-streamlit-app/1610/38


def inject_ga(index_location, ga_id):

    GA_ID = "google_analytics"
    GA_JS = f"""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());

      gtag('config', '{ga_id}');
    </script>
    """
    
    # Insert the script in the head tag of the static template inside your virtual
    index_path = pathlib.Path(index_location)
    logging.info(f'editing {index_path}')
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")
    if not soup.find(id=GA_ID):  # if cannot find tag
        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)  # recover from backup
        else:
            shutil.copy(index_path, bck_index)  # keep a backup
        html = str(soup)
        new_html = html.replace('<head>', '<head>\n' + GA_JS)
        index_path.write_text(new_html)


def main():
    
    # Parse arguments (where is the index file I want to modify)
    parser = argparse.ArgumentParser(description="Modify index file")
    parser.add_argument("index_location", help="Location of the original index file")
    parser.add_argument("ga_id", help="Your GA ID of the form G-...")

    args = parser.parse_args()

    # Where is my index file
    index_location = args.index_location
    ga_id = args.ga_id

    # Then we call the actual function
    inject_ga(index_location, ga_id)

    # Return
    print(f'Successfully injected {ga_id} in {index_location}')

if __name__ == '__main__':
    main()

