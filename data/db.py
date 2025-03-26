import psycopg2
import json
import os
from dotenv import load_dotenv
load_dotenv()

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_NAME")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        if self.connection:
            self.connection.close()

        self.connection = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD)

        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None, fetchone=False):
        try:
            self.cursor.execute(query, params or ())
            if fetchone:
                return self.cursor.fetchone()
            self.connection.commit()
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            print("⚠️ Втрата з'єднання! Перепідключення...")
            self.connect()
            return self.execute_query(query, params, fetchone)

    def insert_user(self, chat_id):
        query = "INSERT INTO users (chat_id, user_history) VALUES (%s, %s)"
        params = (chat_id, json.dumps([{"role": "user", "content": "Speak with me in english language"}]))
        self.execute_query(query, params)

    def get_language(self, chat_id):
        query = "SELECT language FROM users WHERE chat_id = %s"
        result = self.execute_query(query, (chat_id,), fetchone=True)
        return result[0] if result else None

    def update_language(self, chat_id, new_language):
        language_dict = {'ua': 'Спілкуйся зі мною українською мовою!',
                         'eng': 'Speak with me in english!',
                         'ru': 'Общайся со мной на русском!'}
        answer_dict = {'ua': 'Звичайно, я без проблем можу спілкуватись з вами українською!',
                       'eng': 'Sure, I can communicate with you in English. How can I assist you today?',
                       'ru': 'Без проблем! Я могу общаться с вами на русском!'}
        
        query = "SELECT user_history FROM users WHERE chat_id = %s"
        history_list = self.execute_query(query, (chat_id,), fetchone=True)
        history_list = history_list[0] if history_list else []
        
        if len(history_list) >= 21:
            history_list = history_list[2:]
        
        history_list.append({"role": "user", "content": language_dict[new_language]})
        history_list.append({"role": "assistant", "content": answer_dict[new_language]})
        
        self.execute_query("UPDATE users SET user_history = %s, language = %s WHERE chat_id = %s", 
                           (json.dumps(history_list), new_language, chat_id))

    def delete_history(self, chat_id):
        language = self.get_language(chat_id)
        language_dict = {'ua': 'Спілкуйся зі мною українською мовою!',
                         'eng': 'Speak with me in english!',
                         'ru': 'Общайся со мной на русском!'}
        new_history = json.dumps([{"role": "user", "content": language_dict[language]}])
        self.execute_query("UPDATE users SET user_history = %s WHERE chat_id = %s", (new_history, chat_id))

    def get_history(self, chat_id):
        query = "SELECT user_history FROM users WHERE chat_id = %s"
        result = self.execute_query(query, (chat_id,), fetchone=True)
        return result[0] if result else 'None data'

    def update_history(self, chat_id, message, answer):
        query = "SELECT user_history FROM users WHERE chat_id = %s"
        history_list = self.execute_query(query, (chat_id,), fetchone=True)
        history_list = history_list[0] if history_list else []
        
        if len(history_list) >= 21:
            history_list = history_list[2:]
        
        history_list.append(message)
        history_list.append(answer)
        
        self.execute_query("UPDATE users SET user_history = %s WHERE chat_id = %s", (json.dumps(history_list), chat_id))

    def get_image_prompt(self, chat_id):
        query = "SELECT image_prompt FROM users WHERE chat_id = %s"
        result = self.execute_query(query, (chat_id,), fetchone=True)
        return result[0] if result else None

    def update_image_prompt(self, chat_id, new_prompt):
        self.execute_query("UPDATE users SET image_prompt = %s WHERE chat_id = %s", (new_prompt, chat_id))

    def get_ai_prompt_bool(self, chat_id):
        query = "SELECT ai_prompt_bool FROM users WHERE chat_id = %s"
        result = self.execute_query(query, (chat_id,), fetchone=True)
        return result[0] if result else None

    def update_ai_prompt_bool(self, chat_id, new_value):
        self.execute_query("UPDATE users SET ai_prompt_bool = %s WHERE chat_id = %s", (new_value, chat_id))

    def get_voice_language(self, chat_id):
        query = "SELECT voice_language FROM users WHERE chat_id = %s"
        result = self.execute_query(query, (chat_id,), fetchone=True)
        return result[0] if result[0] != 'None' else None

    def update_voice_language(self, chat_id, language_code):
        self.execute_query("UPDATE users SET voice_language = %s WHERE chat_id = %s", (language_code, chat_id))

    def get_synthesis_settings(self, chat_id):
        query = "SELECT synthesis_settings FROM users WHERE chat_id = %s"
        result = self.execute_query(query, (chat_id,), fetchone=True)
        return result[0] if result else None

    def update_synthesis_settings(self, chat_id, language_code, voice_name, pitch, speaking_rate):
        self.execute_query("UPDATE users SET synthesis_settings = %s WHERE chat_id = %s", (json.dumps({"pitch": pitch, "voice_name": voice_name, "language_code": language_code, "speaking_rate": speaking_rate}), chat_id))

    def update_count_message(self, chat_id):
        query = "SELECT count_message FROM users WHERE chat_id = %s"
        result = self.execute_query(query, (chat_id,), fetchone=True)[0]
        result += 1
        self.execute_query("UPDATE users SET count_message = %s WHERE chat_id = %s", (result, chat_id))

    def update_count_voice_message(self, chat_id):
        query = "SELECT count_voice_message FROM users WHERE chat_id = %s"
        result = self.execute_query(query, (chat_id,), fetchone=True)[0]
        result += 1
        self.execute_query("UPDATE users SET count_voice_message = %s WHERE chat_id = %s", (result, chat_id))

    def update_count_generation(self, chat_id):
        query = "SELECT count_generation FROM users WHERE chat_id = %s"
        result = self.execute_query(query, (chat_id,), fetchone=True)[0]
        result += 1
        self.execute_query("UPDATE users SET count_generation = %s WHERE chat_id = %s", (result, chat_id))

    def get_user_data(self, chat_id):
        query = "SELECT count_message, count_voice_message, count_generation FROM users WHERE chat_id = %s"
        result = self.execute_query(query, (chat_id,), fetchone=True)
        return list(result) if result else [0, 0, 0]

