from json import JSONDecodeError
from pathlib import Path
from gradio import json
from supabase import create_client, Client
import os

from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")


class AtlasDatabase:
    supabase: Client

    def __init__(self):
        """
        Initialize Supabase Client
        """
        supabase: Client = create_client(
            SUPABASE_URL,
            SUPABASE_KEY,
        )
        print("[Atlas] ✅ Established connection to Supabase!")

        self.supabase = supabase

    """

    Upload the paper & the images to the bucket

    """

    def upload_files(self, paper_file, image_files, gr, upload_id):
        try:
            # Upload paper to decadal_papers bucket
            if paper_file:
                paper_filename = os.path.basename(paper_file)
                with open(paper_file, "rb") as f:
                    paper_data = f.read()

                paper_result = self.supabase.storage.from_("Decadals_Papers").upload(
                    paper_filename, paper_data
                )

                if paper_result:
                    print("Uploaded " + paper_file)
            gr.Info("Uploaded " + Path(paper_file).name + " To the Database")

            # Upload images to decadal_images bucket
            for image_file in image_files:
                image_data = None
                print("Uploading " + image_file)
                image_filename = os.path.basename(image_file)
                with open(image_file, "rb") as f:
                    image_data = f.read()
                print("Successfully read the data for the image")

                # Modify the image file path to include the folder
                image_path = os.path.join(upload_id, image_filename)
                print("Uploading the image to path: " + image_path)
                image_result = self.supabase.storage.from_("Decadal_Images").upload(
                    image_path, image_data
                )

                if image_result:
                    print("Uploaded " + image_path)
            gr.Info("Uploaded all Images for " + Path(paper_file).name)

        except Exception as e:
            print(f"An error occurred: {str(e)}")

            try:
                error_json = json.loads(str(e))
                gr.Warning(
                    f"There was an error uploading the file(s), {str(error_json['message'])}"
                )

            except JSONDecodeError:
                gr.Warning(f"An error has occured, {str(e)}")

            return None

    """

    Add Decadal Entry

    """

    def add_decadal_entry(
        self, decadal_id, title, parsed_by, date_published, date_parsed, source
    ):
        data = {
            "decadal_id": decadal_id,
            "title": title,
            "parsed_by": parsed_by,
            "date_published": date_published,
            "date_parsed": date_parsed,
            "source": source,
        }

        response = self.supabase.table("Decadals").insert(data).execute()

        if response:
            print("Entry added successfully")
        else:
            print(f"Failed to add entry: {response.data}")
