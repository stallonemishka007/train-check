import asyncio
from datetime import datetime


async def scheduler(bot, repo):
    """
    Простая реализация планировщика: каждую минуту проверяем таблицу users
    и шлем уведомления пользователям, у которых сегодня тренировка в указанное время.
    """
    last_sent = {}
    weekdays_map = {
        'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6
    }
    while True:
        try:
            rows = await repo.get_scheduled_users()
            now = datetime.now()
            cur_wd = now.weekday()
            cur_time = now.strftime("%H:%M")
            for r in rows:
                uid = r.get('id')
                days = r.get('schedule_days') or ""
                notify_time = (r.get('notify_time') or "").strftime("%H:%M") if hasattr(r.get('notify_time'), 'strftime') else (r.get('notify_time') or "")
                last_notified = r.get('last_notified')
                # parse days like 'Mon,Wed,Fri'
                days_list = [d.strip() for d in days.split(',') if d.strip()]
                # check weekday
                ok_day = any(weekdays_map.get(d, -1) == cur_wd for d in days_list)
                if ok_day and notify_time == cur_time:
                    # check DB last_notified to avoid duplicates across restarts
                    try:
                        if last_notified == now.date():
                            continue
                        await bot.send_message(uid, "У тебя сегодня тренировка")
                        # persist last_notified as date
                        try:
                            await repo.set_last_notified(uid, now.date())
                        except Exception:
                            pass
                    except Exception:
                        # network/send errors — ignore and continue
                        pass
        except Exception:
            pass
        await asyncio.sleep(60)
