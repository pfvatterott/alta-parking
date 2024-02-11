# Alta Parking Bot

## Installation

1. Have Python and Pip installed
2. Clone this repo
3. Install all dependencies and create virtual environment
4. Create a `.env` file in the root directory with your Alta Parking email and password:

```
email=...
password=...
```
5. Run `main.py`
6. Enter in a date in YYYY-MM-DD format. For example, February 24, 2024 would be `2024-02-24`
7. Press enter.
8. A Firefox browser will open. Do not touch it at all. It will close when it's done. Note that it's expected that a `Not Found` error will pop up.
9. The script will start attempting to make the reservation every few seconds.


## Things to know

* The reservation will be made with the first vehicle listed in your profile. So either adjust the code to use the correct vehicle or change it after the reservation has been made.

* The program will stop running when it has made the reservation. Simply run it and then let it do its thing.

* It can sometimes take 12+ hours for the reservation to go through.