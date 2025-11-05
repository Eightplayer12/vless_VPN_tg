from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Создание роутера
router = Router()

# Состояния (пока не используются, но заготовка на будущее)
class UserStates(StatesGroup):
    choosing_subscription = State()
    viewing_keys = State()

# Главное меню
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Купить подписку")],
        [KeyboardButton(text="Мои активные ключи")],
        [KeyboardButton(text="Меню")]
    ],
    resize_keyboard=True
)

# Клавиатура для выбора подписки
subscription_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Тестовая")],
        [KeyboardButton(text="1 месяц")],
        [KeyboardButton(text="3 месяца")],
        [KeyboardButton(text="Год")],
        [KeyboardButton(text="Меню")]
    ],
    resize_keyboard=True
)

# Клавиатура для раздела активных ключей
keys_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Купить подписку")],
        [KeyboardButton(text="Меню")]
    ],
    resize_keyboard=True
)

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    welcome_text = """
🤖 Вы в меню!

Выберите действие из меню ниже:
    """
    await message.answer(
        """
        Привет! 
        
Здесь вы можете приобрести доступ к быстрому и безопасному VPN сервису.""",
        reply_markup=main_menu_keyboard
    )
    await message.answer(
        welcome_text,
        reply_markup=main_menu_keyboard
    )

@router.message(F.text == "Меню")
async def menu_handler(message: Message):
    """Обработчик кнопки Меню"""
    await cmd_start(message)

@router.message(F.text == "Купить подписку")
async def buy_subscription_handler(message: Message):
    """Обработчик кнопки Купить подписку"""
    subscription_text = """
📋 Выберите тип подписки:

🔹 **Тестовая** - бесплатный тест на 24 часа
🔹 **1 месяц** - полный доступ на 30 дней
🔹 **3 месяца** - выгодная подписка на 90 дней
🔹 **Год** - максимальная выгода на 365 дней

💳 После выбора тарифа вы будете перенаправлены к оплате.
    """
    
    await message.answer(
        subscription_text,
        reply_markup=subscription_keyboard
    )

@router.message(F.text.in_(["Тестовая", "1 месяц", "3 месяца", "Год"]))
async def subscription_selection_handler(message: Message):
    """Обработчик выбора конкретной подписки"""
    subscription_type = message.text
    prices = {
        "Тестовая": "бесплатно",
        "1 месяц": "100 руб",
        "3 месяца": "250 руб", 
        "Год": "800 руб"
    }
    
    response_text = f"""
🎯 Вы выбрали: **{subscription_type}**

💵 Стоимость: **{prices[subscription_type]}**

🛒 Функционал оплаты находится в разработке...
Скоро здесь будет реализована оплата для выбранного тарифа.
    """
    
    await message.answer(response_text)

@router.message(F.text == "Мои активные ключи")
async def active_keys_handler(message: Message):
    """Обработчик кнопки Мои активные ключи"""
    keys_text = """
🔑 Ваши активные подписки:

❌ Отсутствуют

Для получения доступа к VPN приобретите подписку.
    """
    
    await message.answer(
        keys_text,
        reply_markup=keys_keyboard
    )

# Обработчик для кнопки "Купить подписку" из раздела активных ключей
@router.message(F.text == "Купить подписку")
async def buy_from_keys_handler(message: Message):
    """Обработчик кнопки Купить подписку из раздела ключей"""
    await buy_subscription_handler(message)