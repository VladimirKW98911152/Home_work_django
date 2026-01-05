import os
import django
import logging
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')
django.setup()

def test_all_loggers():
    loggers = {
        'django': logging.getLogger('django'),
        'django.request': logging.getLogger('django.request'),
        'django.security': logging.getLogger('django.security'),
        'django.template': logging.getLogger('django.template'),
        'django.db.backends': logging.getLogger('django.db.backends'),
        'django.server': logging.getLogger('django.server'),
    }
    
    print("=" * 50)
    print("Начинаем тестирование логирования...")
    print("=" * 50)
    
    loggers['django'].debug("DEBUG: Тестовое сообщение уровня DEBUG")
    loggers['django'].info("INFO: Тестовое сообщение уровня INFO")
    loggers['django'].warning("WARNING: Тестовое сообщение с путем")
    
    loggers['django.security'].info("SECURITY: Тест безопасности - обычное сообщение")
    loggers['django.security'].warning("SECURITY: Подозрительная активность")
    
    try:
        raise ValueError("Искусственная ошибка для тестирования")
    except ValueError as e:
        loggers['django.request'].error("REQUEST ERROR: Ошибка в запросе", exc_info=True)
        loggers['django'].error("GENERAL ERROR: Общая ошибка", exc_info=True)
    
    try:
        from news.models import Post
        Post.objects.filter(nonexistent_field=True)
    except Exception as e:
        loggers['django.db.backends'].error("DB ERROR: Ошибка базы данных", exc_info=True)
    
    print("=" * 50)
    print("Тестирование завершено. Проверьте:")
    print("1. Консоль (при DEBUG=True)")
    print("2. Файлы в папке logs/:")
    print("   - general.log")
    print("   - errors.log")
    print("   - security.log")
    print("=" * 50)

if __name__ == "__main__":
    test_all_loggers()
