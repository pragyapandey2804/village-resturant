# Village Restaurant Project

## Setup

1. Clone this repository to your local machine:
   ```
   git clone https://github.com/pragyapandey2804/village-resturant.git
   ```

2. Navigate to the project directory:
   ```
   cd village-resturant
   ```

3. Set up a virtual environment:
   - If you're using `venv`, run:
     ```
     python -m venv venv
     ```

4. Activate the virtual environment:
   - On Windows:
     ```
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Set up your environment variables:
   - Create a `.env` file in the root directory with the following content:
     ```
     API_KEY=your_api_key_here (openwetherapikey)
     ```

7. Apply database migrations:
   ```
   python manage.py migrate
   ```

8. Start the Django server:
   ```
   python manage.py runserver
   ```

9. Open your browser and go to:
   ```
   http://127.0.0.1:8000/
   ```

## Additional Information
- If you want to test the website with different data, feel free to update the `consolidated_menu_prices.csv` or other data files in the `extraction data/` folder.
