import openai
import os
import telebot
from telebot import types

# Set up the Telegram Bot API token
TELE_API_TOKEN = "YOUR BOTS API"
bot = telebot.TeleBot(TELE_API_TOKEN)

# Set up the OpenAI API credentials
openai.api_key = "OPENAI API KEY"

user_dict = {}

class User:
    def __init__(self, name):
        self.age = None
        self.sex = None
        self.height = None
        self.weight = None
        self.allergy = None
        self.goal = None
        self.days = None
        self.meals = None
        self.snacks = None
        self.preference = None

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    chat_id = message.chat.id

    if message.text == '/start':
        # Remove the existing user from the user_dict if it exists
        if chat_id in user_dict:
            del user_dict[chat_id]
        bot.send_message(chat_id, "Welcome! Let's start from the beginning.")
        msg = bot.send_message(chat_id, """\
        I am FitnessGPT \U0001f3cb\uFE0F I will take the following information about you and create a custom diet and exercise plan. \nHow old are you? (1/10)
        """)
        bot.register_next_step_handler(msg, process_age_step)
    elif message.text == '/stop':
        # Remove the existing user from the user_dict if it exists
        if chat_id in user_dict:
            del user_dict[chat_id]
        bot.send_message(chat_id, "Chat ended. If you need assistance, feel free to start a new chat using the /start command.")

def process_age_step(message):
    try:
        chat_id = message.chat.id
        # Check for restart or stop
        if message.text == '/start':
            send_welcome(message)
            return
        elif message.text == '/stop':
            send_welcome(message)
            return
        age = message.text

        if not age.isdigit():
            msg = bot.reply_to(message, 'Age should be a number. How old are you? (1/10)')
            bot.register_next_step_handler(msg, process_age_step)
            return
        
        # Initialize the User object for the current chat_id
        user = User(chat_id)
        user_dict[chat_id] = user
        user.age = age

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Male', 'Female')
        msg = bot.reply_to(message, 'What is your gender (2/10)', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, f'Oops! An error occurred: {str(e)}')

def process_sex_step(message):
    try:
        chat_id = message.chat.id
        # Check for restart or stop
        if message.text == '/start':
            send_welcome(message)
            return
        elif message.text == '/stop':
            send_welcome(message)
            return
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Male') or (sex == u'Female'):
            user.sex = sex
        else:
            raise Exception("Unknown sex")
        
        # Create a custom keyboard markup with buttons for each height option
        markup = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)

        # Create a list of height options in feet and inches
        height_options = ['4\'0"', '4\'1"', '4\'2"', '4\'3"', '4\'4"', '4\'5"', '4\'6"', '4\'7"', '4\'8"', '4\'9"',
                          '4\'10"', '4\'11"', '5\'0"', '5\'1"', '5\'2"', '5\'3"', '5\'4"', '5\'5"', '5\'6"', '5\'7"',
                          '5\'8"', '5\'9"', '5\'10"', '5\'11"', '6\'0"', '6\'1"', '6\'2"', '6\'3"', '6\'4"',
                          '6\'5"', '6\'6"', '6\'7"', '6\'8"', '6\'9"', '6\'10"', '6\'11"', '7\'0"']

        # Generate buttons for each height option
        buttons = [types.KeyboardButton(height) for height in height_options]

        # Add the buttons to the custom keyboard markup
        markup.add(*buttons)

        msg = bot.reply_to(message, 'Select your height (3/10):', reply_markup=markup)
        bot.register_next_step_handler(msg, process_height_step)
    except Exception as e:
        bot.reply_to(message, f'Oops! An error occurred: {str(e)}')

def process_height_step(message):
    try:
        chat_id = message.chat.id
        # Check for restart or stop
        if message.text == '/start':
            send_welcome(message)
            return
        elif message.text == '/stop':
            send_welcome(message)
            return
        height = message.text
        user = user_dict[chat_id]
        user.height = height
        msg = bot.reply_to(message, 'Enter your weight in pounds (4/10)')
        bot.register_next_step_handler(msg, process_weight_step)
    except Exception as e:
        bot.reply_to(message, f'Oops! An error occurred: {str(e)}')

def process_weight_step(message):
    try:
        chat_id = message.chat.id
        # Check for restart or stop
        if message.text == '/start':
            send_welcome(message)
            return
        elif message.text == '/stop':
            send_welcome(message)
            return
        weight = message.text
        user = user_dict[chat_id]
        user.weight = weight
        msg = bot.reply_to(message, 'List any food allergies (5/10)')
        bot.register_next_step_handler(msg, process_allergy_step)
    except Exception as e:
        bot.reply_to(message, f'Oops! An error occurred: {str(e)}')
        
def process_allergy_step(message):
    try:
        chat_id = message.chat.id
        # Check for restart or stop
        if message.text == '/start':
            send_welcome(message)
            return
        elif message.text == '/stop':
            send_welcome(message)
            return
        allergy = message.text
        user = user_dict[chat_id]
        user.allergy = allergy
        msg = bot.reply_to(message, 'What is your fitness goal? (6/10)')
        bot.register_next_step_handler(msg, process_goal_step)
    except Exception as e:
        bot.reply_to(message, f'Oops! An error occurred: {str(e)}')

def process_goal_step(message):
    try:
        chat_id = message.chat.id
        # Check for restart or stop
        if message.text == '/start':
            send_welcome(message)
            return
        elif message.text == '/stop':
            send_welcome(message)
            return
        goal = message.text
        user = user_dict[chat_id]
        user.goal = goal
        msg = bot.reply_to(message, 'How many days per week can you commit to working out? (7/10)')
        bot.register_next_step_handler(msg, process_days_step)
    except Exception as e:
        bot.reply_to(message, f'Oops! An error occurred: {str(e)}')

def process_days_step(message):
    try:
        chat_id = message.chat.id
        # Check for restart or stop
        if message.text == '/start':
            send_welcome(message)
            return
        elif message.text == '/stop':
            send_welcome(message)
            return
        days = message.text
        user = user_dict[chat_id]
        user.days = days
        msg = bot.reply_to(message, 'What is your preference for the type of workout? (8/10)')
        bot.register_next_step_handler(msg, process_preference_step)
    except Exception as e:
        bot.reply_to(message, f'Oops! An error occurred: {str(e)}')

def process_preference_step(message):
    try:
        chat_id = message.chat.id
        # Check for restart or stop
        if message.text == '/start':
            send_welcome(message)
            return
        elif message.text == '/stop':
            send_welcome(message)
            return
        preference = message.text
        user = user_dict[chat_id]
        user.preference = preference

        msg = bot.reply_to(message, 'How many meals do you want per day? (9/10)')
        bot.register_next_step_handler(msg, process_meals_step)
    except Exception as e:
        bot.reply_to(message, f'Oops! An error occurred: {str(e)}')

def process_meals_step(message):
    try:
        chat_id = message.chat.id
        # Check for restart or stop
        if message.text == '/start':
            send_welcome(message)
            return
        elif message.text == '/stop':
            send_welcome(message)
            return
        meals = message.text
        user = user_dict[chat_id]
        user.meals = meals

        msg = bot.reply_to(message, 'How many snacks do you want per day? (10/10)')
        bot.register_next_step_handler(msg, process_snacks_step)
    except Exception as e:
        bot.reply_to(message, f'Oops! An error occurred: {str(e)}')

def process_snacks_step(message):
    try:
        chat_id = message.chat.id
        # Check for restart or stop
        if message.text == '/start':
            send_welcome(message)
            return
        elif message.text == '/stop':
            send_welcome(message)
            return
        snacks = message.text
        user = user_dict[chat_id]
        user.snacks = snacks
        # Call the function to generate the fitness plan
        bot.send_message(chat_id, 'You\'re all done! Generating your fitness plan now...\n')
        generate_fitness_plan(message)
    except Exception as e:
        bot.reply_to(message, f'Oops! An error occurred: {str(e)}')

# Function to generate fitness plan using OpenAI GPT
def generate_fitness_plan(message):
    try:
        chat_id = message.chat.id
        # Check for restart or stop
        if message.text == '/start':
            send_welcome(message)
            return
        elif message.text == '/stop':
            send_welcome(message)
            return
        meals = message.text
        user = user_dict[chat_id]
        user.meals = meals
        # Generate fitness plan using OpenAI GPT
        prompt = f"You are a highly renowned health and nutrition expert FitnessGPT. Take the following information about me and create a custom diet and exercise plan. I am {user.age} years old, {user.sex}, {user.height}. My current weight is {user.weight}. I have food allergies to {user.allergy}. My primary fitness and health goals are {user.goal}. I can commit to working out {user.days} days per week. I prefer and enjoy his type of workout {user.preference}.  I have a diet preference Protein based. I want to have {user.meals} Meals and {user.snacks} Snacks per day. Create a summary of my diet and exercise plan. Create a detailed workout program that targets a different muscle group each day for my exercise plan. Create a detailed Meal Plan for my diet. Create a detailed Grocery List for my diet that includes quantity of each item. Do not reiterate the question."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=600,
            n=1,
            stop=None,
            temperature=0.7
        )
        fitness_plan = response.choices[0].text.strip()
        bot.send_message(chat_id, fitness_plan)
        
        # Remove the user from the dictionary to end the current session
        del user_dict[chat_id]
    except Exception as e:
        bot.reply_to(message, f'Oops! An error occurred: {str(e)}')


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()
